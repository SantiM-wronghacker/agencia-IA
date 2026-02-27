"""
AREA: CEREBRO
DESCRIPCION: Fabrica de agentes en bucle infinito. Genera lotes de 15 agentes,
             prueba cada uno, repara los que fallan hasta que pasen, y en cuanto
             los 15 estan aprobados arranca automaticamente el siguiente lote.
             Nunca para. Cubre todas las areas de negocio posibles.
TECNOLOGIA: llm_router (multi-proveedor), ast, subprocess
"""

import os
import sys
import ast
import json
import time
import random
import subprocess
import shutil
import io as _io
from datetime import datetime

# Fix Unicode para Windows (cp1252)
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = _io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = _io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    from llm_router import completar_simple as ia
except ImportError:
    from groq import Groq
    _g = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
    def ia(prompt, **kw):
        r = _g.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4, max_tokens=3000
        )
        return r.choices[0].message.content.strip()

LOG               = "registro_noche.txt"
HABILIDADES       = "habilidades.json"
CARPETA_LOTE      = "lote_nuevo"
TAMANO_LOTE       = 15
PAUSA_AGENTE      = 3
PAUSA_LOTE        = 5
UMBRAL_MODO_MEJORA = 500   # objetivo: 500 agentes en modo CREAR
MAX_LLM_FALLOS    = 6      # reintentos LLM antes de saltar al siguiente agente

AREAS_TEMAS = {
    # ── ÁREAS ORIGINALES (ampliadas) ──────────────────────────
    "FINANZAS": [
        "analisis_estados_financieros", "control_presupuesto_mensual",
        "calculo_depreciacion_activos", "analisis_punto_equilibrio",
        "simulador_inversion_cetes", "calculo_rendimiento_fondos",
        "analizador_deuda_empresarial", "proyector_flujo_caja_3_anos",
        "calculo_capital_trabajo", "comparador_instrumentos_inversion",
        "calculo_nomina_mensual_mexico", "analizador_razones_financieras",
        "estimador_valor_empresa", "calculadora_afore_retiro",
        "calculo_impuesto_sobre_renta_mensual", "simulador_fondo_emergencia",
        # nuevos
        "calculadora_tasa_efectiva_anual", "simulador_pago_deuda_acelerado",
        "analizador_portafolio_acciones", "calculadora_intereses_compuestos",
        "proyector_patrimonio_neto", "calculadora_rendimiento_cetes_28dias",
        "simulador_prestamo_personal", "analizador_riesgo_credito_empresa",
        "calculadora_wacc_empresa", "generador_estado_resultados_proyectado",
        "calculadora_flujo_libre_caja", "analizador_cobertura_servicio_deuda",
    ],
    "REAL ESTATE": [
        "comparador_zonas_inversion_cdmx", "calculadora_renta_justa_m2",
        "reporte_avaluo_basico", "detector_oportunidades_compra",
        "analizador_tendencias_mercado_inmobiliario",
        "calculadora_retorno_desarrollo_obra",
        "simulador_crowdfunding_inmobiliario", "evaluador_credito_puente",
        "plan_comercializacion_propiedad", "calculadora_gastos_escrituracion",
        "analizador_cartera_propiedades", "estimador_costos_remodelacion",
        "calculadora_ocupacion_renta", "comparador_hipotecas_bancos_mexico",
        # nuevos
        "calculadora_roi_departamento_cdmx", "analizador_plusvalia_colonia",
        "comparador_fraccionamientos_mexico", "calculadora_costo_construccion_m2",
        "estimador_plusvalia_5_anos", "calculadora_arrendamiento_financiero_inmueble",
        "generador_due_diligence_inmobiliario", "calculadora_cap_rate_inmueble",
        "analizador_oferta_demanda_vivienda", "calculadora_enganche_credito_infonavit",
    ],
    "CEREBRO": [
        "orquestador_agentes_industria", "router_consultas_complejidad",
        "agente_memoria_contextual", "generador_prompts_optimizados",
        "coordinador_pipeline_datos", "monitor_performance_agentes",
        "agente_resumen_ejecutivo", "clasificador_intencion_usuario",
        "dispatcher_multiagente", "agente_validacion_resultados",
        # nuevos
        "sintetizador_informes_ejecutivos", "extractor_insights_datos",
        "generador_briefing_diario", "clasificador_prioridad_tareas",
        "agente_fact_checking", "comparador_escenarios_decision",
        "generador_hipotesis_negocio", "analizador_causa_raiz",
    ],
    "HERRAMIENTAS": [
        "generador_reportes_csv", "scheduler_tareas_programadas",
        "validador_datos_entrada", "compresor_archivador_logs",
        "monitor_uso_apis", "generador_backups_automaticos",
        "parser_archivos_configuracion", "monitor_salud_sistema",
        "notificador_alertas_consola", "limpiador_archivos_temporales",
        "generador_hash_verificacion", "conversor_formatos_datos",
        # nuevos
        "generador_reporte_json_a_html", "comparador_versiones_archivo",
        "calculadora_uso_disco", "generador_graficas_ascii",
        "conversor_csv_a_json", "validador_formato_rfc_mexico",
        "generador_password_seguro", "calculadora_tiempo_ejecucion",
        "monitor_cambios_directorio", "generador_uuid_masivo",
    ],
    "LEGAL": [
        "generador_carta_poder", "checklist_requisitos_notariales",
        "convenio_prestacion_servicios", "analizador_clausulas_riesgo",
        "guia_constitucion_empresa_mexico", "generador_finiquito_laboral",
        "calculadora_indemnizacion_imss", "checklist_cumplimiento_sat",
        "generador_acta_acuerdos", "template_contrato_servicios_profesionales",
        # nuevos
        "generador_contrato_confidencialidad_nda", "checklist_due_diligence_legal",
        "guia_registro_marca_impi_mexico", "generador_carta_reclamo_formal",
        "calculadora_multas_sat", "checklist_obligaciones_patrones_imss",
        "generador_contrato_arrendamiento_comercial", "guia_disolucion_empresa_mexico",
    ],
    "MARKETING": [
        "generador_plan_contenidos", "analizador_buyer_persona",
        "calculadora_presupuesto_publicitario", "generador_propuesta_valor",
        "analizador_funnel_ventas", "generador_copy_facebook_ads",
        "calculadora_cac_ltv", "generador_estrategia_referidos",
        "analizador_metricas_campana", "generador_calendario_editorial",
        "generador_bio_redes_sociales", "analizador_hashtags_instagram",
        # nuevos
        "calculadora_roi_google_ads", "generador_copy_email_marketing",
        "calculadora_costo_por_lead", "analizador_competencia_seo_basico",
        "generador_keywords_negocio_mexico", "calculadora_tasa_conversion_web",
        "generador_plan_redes_sociales_90dias", "calculadora_presupuesto_influencer",
        "analizador_share_of_voice", "generador_copy_google_ads",
        "calculadora_frecuencia_publicacion", "analizador_engagement_rate",
    ],
    "VENTAS": [
        "calculadora_pipeline_ventas", "generador_propuesta_comercial",
        "analizador_objeciones", "tracker_seguimiento_prospectos",
        "calculadora_forecast_mensual", "generador_argumentario_ventas",
        "analizador_ciclo_venta", "script_cierre_ventas",
        "calculadora_descuentos_margen", "generador_email_cotizacion",
        # nuevos
        "calculadora_comision_ventas_equipo", "generador_script_llamada_fria",
        "analizador_win_rate", "calculadora_precio_psicologico",
        "generador_seguimiento_postventa", "calculadora_ticket_promedio",
        "analizador_mix_productos_ventas", "generador_reporte_ventas_semanal",
    ],
    "OPERACIONES": [
        "gestor_inventario_basico", "calculadora_costo_operacion",
        "generador_procedimientos_sop", "analizador_kpis_operativos",
        "calculadora_capacidad_instalada", "gestor_ordenes_trabajo",
        "analizador_cuellos_botella", "calculadora_eficiencia_operativa",
        "generador_checklist_procesos", "calculadora_tiempo_produccion",
        # nuevos
        "calculadora_oee_eficiencia_equipos", "analizador_downtime_produccion",
        "generador_plan_mantenimiento_preventivo", "calculadora_lote_economico_compra",
        "analizador_lead_time_proveedor", "calculadora_stock_seguridad",
        "generador_layout_almacen", "calculadora_costo_calidad_total",
    ],
    "RECURSOS HUMANOS": [
        "calculadora_costo_empleado_mexico", "generador_descripcion_puesto",
        "calculadora_prestaciones_ley", "generador_evaluacion_desempenio",
        "calculadora_liquidacion_laboral", "analizador_clima_organizacional",
        "generador_plan_onboarding", "calculadora_horas_extra",
        "generador_encuesta_satisfaccion", "calculadora_rotacion_personal",
        # nuevos
        "calculadora_costo_reclutamiento", "generador_plan_capacitacion_anual",
        "calculadora_absentismo_laboral", "generador_politica_home_office",
        "calculadora_sueldo_competitivo_mexico", "analizador_brecha_salarial",
        "generador_plan_carrera_empleado", "calculadora_bono_productividad",
    ],
    "TECNOLOGIA": [
        "calculadora_costo_infraestructura_cloud",
        "generador_especificaciones_tecnicas", "analizador_stack_tecnologico",
        "calculadora_roi_automatizacion", "plan_migracion_cloud",
        "analizador_deuda_tecnica", "calculadora_sla_uptime",
        "generador_documentacion_api", "calculadora_licencias_software",
        "analizador_seguridad_basica",
        # nuevos
        "calculadora_costo_desarrollo_software", "analizador_vulnerabilidades_web",
        "generador_arquitectura_microservicios", "calculadora_tco_servidor",
        "analizador_performance_base_datos", "generador_politica_seguridad_it",
        "calculadora_ahorro_contenedores_docker", "analizador_deuda_tecnica_codigo",
        "generador_plan_disaster_recovery", "calculadora_roi_devops",
    ],
    "SALUD": [
        "calculadora_imc_riesgo", "generador_plan_nutricional",
        "calculadora_calorias_actividad", "analizador_costos_seguro_medico",
        "checklist_consulta_medica", "calculadora_dosis_medicamento",
        "generador_recordatorio_medicamentos", "analizador_habitos_saludables",
        # nuevos
        "calculadora_costo_consulta_medica_privada", "generador_dieta_diabetes",
        "calculadora_frecuencia_cardiaca_objetivo", "analizador_indice_cintura_cadera",
        "generador_plan_ejercicio_semanal", "calculadora_hidratacion_diaria",
        "analizador_costo_medicamentos_genericos", "checklist_prevencion_enfermedades",
    ],
    "EDUCACION": [
        "generador_plan_estudio", "calculadora_costo_carrera_mexico",
        "generador_ejercicios_practica", "analizador_tecnicas_aprendizaje",
        "calculadora_roi_educativo", "generador_rubrica_evaluacion",
        "generador_temario_curso", "calculadora_becas_disponibles",
        # nuevos
        "generador_syllabus_curso_online", "calculadora_precio_curso_online",
        "analizador_plataformas_elearning", "generador_examen_autocorregible",
        "calculadora_horas_estudio_certificacion", "generador_material_didactico",
        "analizador_estadisticas_curso", "calculadora_roi_certificacion_tech",
    ],
    "LOGISTICA": [
        "calculadora_costo_envio_mexico", "optimizador_ruta_entregas",
        "calculadora_tiempo_transito", "analizador_costo_ultima_milla",
        "generador_manifiesto_carga", "calculadora_capacidad_almacen",
        "tracker_pedidos_basico", "calculadora_costo_importacion",
        # nuevos
        "calculadora_costo_exportacion_mexico", "analizador_carriers_mexico",
        "calculadora_seguro_carga", "generador_etiqueta_envio",
        "calculadora_costo_almacenamiento_externo", "analizador_tasa_devolucion",
        "calculadora_cross_docking", "generador_plan_distribucion_nacional",
    ],
    "TURISMO": [
        "calculadora_presupuesto_viaje", "generador_itinerario_viaje",
        "comparador_hospedaje", "calculadora_roi_renta_vacacional",
        "analizador_temporadas", "generador_paquete_turistico",
        # nuevos
        "calculadora_costo_viaje_negocios", "generador_guia_destino_mexico",
        "calculadora_ocupacion_hotel", "analizador_reseñas_tripadvisor",
        "generador_politica_cancelacion_hotel", "calculadora_tarifa_rack_hotel",
    ],
    "RESTAURANTES": [
        "calculadora_costo_platillo", "generador_menu_precios",
        "calculadora_punto_equilibrio_restaurante",
        "analizador_merma_desperdicio", "generador_receta_estandarizada",
        "calculadora_precio_venta_platillo",
        # nuevos
        "calculadora_food_cost_semanal", "generador_carta_digital_qr",
        "calculadora_rotacion_mesa", "analizador_popularidad_platillos",
        "calculadora_costo_delivery_restaurante", "generador_plan_apertura_restaurante",
        "calculadora_precio_buffet", "analizador_competencia_restaurantes_zona",
    ],
    "BIENES RAICES COMERCIALES": [
        "calculadora_renta_oficina_cdmx", "analizador_local_comercial",
        "calculadora_roi_bodega_industrial", "comparador_zonas_comerciales",
        "estimador_aforo_local", "calculadora_contrato_arrendamiento_comercial",
        # nuevos
        "calculadora_roi_nave_industrial", "analizador_zonas_industria_cdmx",
        "calculadora_costo_remodelacion_oficina", "generador_contrato_coworking",
        "calculadora_plusvalia_zona_industrial",
    ],
    "SEGUROS": [
        "calculadora_seguro_vida_mexico", "comparador_seguros_auto",
        "analizador_cobertura_gastos_medicos", "calculadora_prima_seguro",
        "generador_reporte_siniestro", "checklist_contratacion_seguro",
        # nuevos
        "calculadora_seguro_empresarial", "comparador_seguros_vida_mexico",
        "calculadora_deducible_seguro_gmm", "analizador_exclusiones_poliza",
        "generador_inventario_activos_asegurables", "calculadora_infraseguro",
    ],
    "CONTABILIDAD": [
        "calculadora_iva_desglosado", "generador_factura_conceptos",
        "calculadora_ptu_empleados", "analizador_deducciones_fiscales",
        "calculadora_regimen_fiscal_adecuado", "generador_balance_general_simple",
        # nuevos
        "calculadora_depreciacion_fiscal_mexico", "generador_auxiliar_cuentas",
        "calculadora_conciliacion_bancaria", "analizador_cuentas_por_cobrar",
        "calculadora_provision_impuestos", "generador_catalogo_cuentas_sat",
        "calculadora_costo_contabilidad_externa", "analizador_indices_liquidez",
    ],

    # ── NUEVAS ÁREAS ──────────────────────────────────────────
    "FISCAL": [
        "calculadora_isr_personas_morales", "generador_declaracion_anual_resumen",
        "calculadora_iva_mensual_empresa", "checklist_obligaciones_fiscales_sat",
        "calculadora_isr_asimilados_salarios", "analizador_regimenes_especiales_sat",
        "calculadora_impuesto_sobre_nomina", "generador_aviso_compensacion_sat",
        "calculadora_actualizacion_recargos_sat", "analizador_beneficios_resico",
        "calculadora_isr_honorarios", "checklist_auditoria_fiscal_interna",
        "generador_papeles_trabajo_fiscal", "calculadora_diferimiento_impuestos",
    ],
    "ECOMMERCE": [
        "calculadora_margen_ecommerce", "analizador_abandono_carrito",
        "generador_descripcion_producto_seo", "calculadora_costo_logistica_ecommerce",
        "analizador_competencia_precios_amazon", "generador_politica_devoluciones",
        "calculadora_pricing_dinamico", "analizador_temporadas_ventas_online",
        "calculadora_costo_mercadolibre", "analizador_ranking_productos_ml",
        "calculadora_roi_tienda_shopify", "generador_ficha_tecnica_producto",
        "calculadora_costo_fulfillment", "analizador_reseñas_productos",
        "calculadora_costo_publicidad_amazon",
    ],
    "MANUFACTURA": [
        "calculadora_costo_produccion_unitario", "analizador_eficiencia_linea_produccion",
        "calculadora_tiempo_ciclo_proceso", "calculadora_costo_scrap_merma",
        "analizador_capacidad_planta", "calculadora_costo_cambio_herramienta",
        "generador_orden_produccion", "calculadora_productividad_operario",
        "analizador_calidad_ppm", "calculadora_costo_garantia_producto",
        "generador_plan_produccion_semanal", "calculadora_punto_equilibrio_fabrica",
        "analizador_proveedores_materia_prima", "calculadora_lote_minimo_produccion",
    ],
    "CONSTRUCCION": [
        "calculadora_costo_obra_gris_m2", "estimador_materiales_construccion",
        "calculadora_costo_mano_obra_cdmx", "generador_presupuesto_remodelacion_casa",
        "analizador_precios_materiales_construmat", "calculadora_costo_instalacion_electrica",
        "calculadora_costo_plomeria", "generador_programa_obra_gannt",
        "calculadora_rendimiento_cemento", "analizador_costo_subcontratistas",
        "calculadora_anticipo_contratista", "generador_estimado_pintura_m2",
        "calculadora_costo_acabados_lujo",
    ],
    "FRANQUICIAS": [
        "calculadora_roi_franquicia_mexico", "comparador_franquicias_inversion_baja",
        "analizador_territorio_franquicia", "calculadora_inversion_inicial_franquicia",
        "generador_plan_negocio_franquicia", "calculadora_regalias_franquicia",
        "checklist_due_diligence_franquicia", "analizador_franquicias_comida_mexico",
        "calculadora_break_even_franquicia", "generador_manual_operaciones_franquicia",
        "calculadora_costo_capacitacion_franquicia",
    ],
    "EVENTOS": [
        "calculadora_costo_evento_empresarial", "generador_checklist_evento_corporativo",
        "calculadora_aforo_espacio_eventos", "generador_cronograma_evento",
        "calculadora_costo_catering_por_persona", "generador_cotizacion_evento",
        "calculadora_roi_evento_marketing", "analizador_proveedores_eventos",
        "calculadora_costo_produccion_audiovisual", "generador_plan_contingencia_evento",
        "calculadora_precio_entrada_evento",
    ],
    "FINANZAS PERSONALES": [
        "calculadora_libertad_financiera", "simulador_ahorro_meta_personal",
        "analizador_gastos_personales_50_30_20", "calculadora_fondo_retiro_personal",
        "simulador_independencia_financiera", "calculadora_presupuesto_familiar_mexico",
        "analizador_deudas_bola_nieve", "calculadora_seguro_gastos_medicos_mayores",
        "calculadora_fondo_emergencia_6_meses", "analizador_patrimonio_neto_personal",
        "generador_plan_ahorro_casa", "calculadora_pension_imss_estimada",
        "simulador_inversion_mensual_30_anos",
    ],
    "GOBIERNO Y TRAMITES": [
        "guia_tramites_sat_rfc", "checklist_apertura_empresa_sas_mexico",
        "generador_carta_no_adeudo_fiscal", "guia_registro_marca_impi",
        "checklist_permisos_uso_suelo", "guia_importacion_primera_vez",
        "calculadora_aranceles_importacion", "checklist_certificacion_iso_9001",
        "guia_licitaciones_gobierno_federal", "generador_acta_constitutiva_resumen",
    ],
    "TRANSPORTE": [
        "calculadora_costo_flota_vehiculos", "analizador_rendimiento_combustible_km",
        "calculadora_depreciacion_flotilla", "generador_bitacora_vehiculos",
        "calculadora_costo_operacion_trailer", "analizador_rutas_reparto_optimas",
        "calculadora_costo_seguro_flotilla", "generador_reporte_kilometraje",
        "calculadora_costo_taxi_vs_uber_empresa", "analizador_emision_co2_flota",
    ],
    "AGRICULTURA": [
        "calculadora_costo_cosecha_hectarea", "analizador_rentabilidad_cultivo_mexico",
        "calculadora_riego_eficiente_litros", "generador_calendario_agricola_mexico",
        "calculadora_precio_venta_cosecha", "analizador_apoyos_sagarpa",
        "calculadora_costo_fertilizante", "generador_plan_rotacion_cultivos",
        "calculadora_roi_invernadero", "analizador_mercados_agricolas_mexico",
    ],
    "STARTUPS": [
        "calculadora_runway_startup", "generador_pitch_deck_estructura",
        "calculadora_valuation_startup", "analizador_product_market_fit",
        "generador_lean_canvas", "calculadora_dilusion_ronda_inversion",
        "analizador_metricas_saas", "calculadora_mrr_arr_startup",
        "generador_term_sheet_resumen", "calculadora_costo_adquisicion_usuario",
        "analizador_churn_rate", "calculadora_lTV_usuario_app",
        "generador_roadmap_producto",
    ],
}


# ---------------------------------------------
#  UTILIDADES
# ---------------------------------------------

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linea = "[" + ts + "] [FABRICA] " + str(msg)
    try:
        print(linea, flush=True)
    except Exception:
        pass
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception:
        pass

def cargar_habilidades():
    if not os.path.exists(HABILIDADES):
        return {}
    try:
        with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return {}

def registrar_en_habilidades(archivo, area, descripcion):
    habilidades = cargar_habilidades()
    habilidades[archivo] = {
        "descripcion": descripcion,
        "categoria": area,
        "salud": "OK",
        "tecnologia": ["Python estandar"],
        "ultima_actualizacion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "ordenes": [archivo.replace(".py", "").replace("_", " ")]
    }
    bak = HABILIDADES + ".bak"
    if os.path.exists(HABILIDADES):
        try:
            shutil.copy2(HABILIDADES, bak)
        except Exception:
            pass
    tmp = HABILIDADES + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(habilidades, f, indent=4, ensure_ascii=False)
    os.replace(tmp, HABILIDADES)

def agentes_existentes():
    return set(cargar_habilidades().keys())

def validar_sintaxis(codigo):
    try:
        ast.parse(codigo)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def limpiar_codigo(texto):
    if "```python" in texto:
        return texto.split("```python")[1].split("```")[0].strip()
    if "```" in texto:
        return texto.split("```")[1].split("```")[0].strip()
    return texto.strip()

def probar_agente(ruta):
    try:
        r = subprocess.run(
            [sys.executable, ruta],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=25
        )
        salida = (r.stdout or "").strip()
        if len(salida) < 10:
            err = (r.stderr or "").strip()
            return False, err[:200] or "Output vacio o muy corto"
        return True, salida[:200]
    except subprocess.TimeoutExpired:
        return False, "Timeout de 25s"
    except Exception as e:
        return False, str(e)

# ---------------------------------------------
#  GENERADOR DE PLAN
# ---------------------------------------------

def generar_plan_lote(numero_lote, existentes):
    areas_base   = ["FINANZAS", "REAL ESTATE", "CEREBRO", "HERRAMIENTAS"]
    areas_extras = [a for a in AREAS_TEMAS if a not in areas_base]

    plan = []
    usados = set()

    for area in areas_base:
        temas = list(AREAS_TEMAS.get(area, []))
        random.shuffle(temas)
        agregados = 0
        for tema in temas:
            nombre = tema + ".py"
            if nombre not in existentes and nombre not in usados:
                plan.append({"archivo": nombre, "area": area, "tema": tema.replace("_", " ")})
                usados.add(nombre)
                agregados += 1
                if agregados >= 2:
                    break

    random.shuffle(areas_extras)
    for area in areas_extras * 3:
        if len(plan) >= TAMANO_LOTE:
            break
        temas = list(AREAS_TEMAS.get(area, []))
        random.shuffle(temas)
        for tema in temas:
            nombre = tema + ".py"
            if nombre not in existentes and nombre not in usados:
                plan.append({"archivo": nombre, "area": area, "tema": tema.replace("_", " ")})
                usados.add(nombre)
                break

    return plan[:TAMANO_LOTE]

# ---------------------------------------------
#  GENERADOR DE CODIGO
# ---------------------------------------------

def generar_codigo(spec):
    prompt = (
        "Eres experto Python creando agentes para Agencia Santi (Mexico).\n\n"
        "ARCHIVO: " + spec['archivo'] + "\n"
        "AREA: " + spec['area'] + "\n"
        "FUNCION: " + spec['tema'] + "\n\n"
        "REGLAS ABSOLUTAS:\n"
        "1. Encabezado al inicio con AREA/DESCRIPCION/TECNOLOGIA\n"
        "2. NUNCA uses input() - solo sys.argv con defaults realistas\n"
        "3. Output: minimo 5 lineas con datos concretos y numeros reales mexicanos\n"
        "4. Solo stdlib: os, sys, json, datetime, math, re, random\n"
        "5. Funcion main() + if __name__ == '__main__': main()\n"
        "6. try/except en main\n"
        "7. Completamente autonomo - corre solo sin intervencion humana\n\n"
        "DEVUELVE SOLO CODIGO PYTHON. Sin markdown. Sin explicaciones."
    )
    r = ia(prompt)
    return limpiar_codigo(r) if r else None

def reparar_codigo(spec, codigo_roto, error, intento):
    prompt = (
        "Repara este agente Python. Intento #" + str(intento) + "\n\n"
        "ARCHIVO: " + spec['archivo'] + "\n"
        "ERROR: " + str(error) + "\n\n"
        "CODIGO ACTUAL:\n" + str(codigo_roto)[:2500] + "\n\n"
        "SOLUCIONES COMUNES:\n"
        "- input() -> sys.argv[1] if len(sys.argv) > 1 else 'default'\n"
        "- Output vacio -> agregar print() con calculos\n"
        "- ImportError -> usar solo stdlib\n"
        "- SyntaxError -> corregir indentacion\n\n"
        "DEVUELVE SOLO EL CODIGO CORREGIDO. Sin markdown."
    )
    r = ia(prompt)
    return limpiar_codigo(r) if r else None

# ---------------------------------------------
#  PROCESAR UN AGENTE
# ---------------------------------------------

def procesar_agente(spec, numero, total):
    archivo = spec["archivo"]
    area    = spec["area"]
    tema    = spec["tema"]

    log("  [" + str(numero) + "/" + str(total) + "] " + archivo + " [" + area + "]")

    os.makedirs(CARPETA_LOTE, exist_ok=True)
    ruta_temp    = os.path.join(CARPETA_LOTE, archivo)
    codigo       = None
    ultimo_error = "Sin codigo generado aun"
    intento      = 0
    fallos_llm   = 0

    while True:
        intento += 1

        if codigo is None:
            log("    -> Generando...")
            codigo = generar_codigo(spec)
        else:
            log("    [FIX] Reparando intento " + str(intento) + "...")
            codigo_nuevo = reparar_codigo(spec, codigo, ultimo_error, intento)
            if codigo_nuevo:
                codigo = codigo_nuevo

        if not codigo:
            fallos_llm += 1
            if fallos_llm >= MAX_LLM_FALLOS:
                log("    [SKIP] " + archivo + " saltado tras " + str(MAX_LLM_FALLOS) + " fallos LLM — API saturada")
                return
            espera = min(30 * fallos_llm, 120)  # backoff: 30s, 60s, 90s, 120s...
            log("    [WARN] Sin respuesta del LLM (" + str(fallos_llm) + "/" + str(MAX_LLM_FALLOS) + "), esperando " + str(espera) + "s...")
            time.sleep(espera)
            codigo = None
            continue
        else:
            fallos_llm = 0  # reset al recibir respuesta

        valido, err_sintaxis = validar_sintaxis(codigo)
        if not valido:
            ultimo_error = "SyntaxError: " + str(err_sintaxis)
            log("    [WARN] Sintaxis: " + str(err_sintaxis)[:80])
            time.sleep(2)
            continue

        with open(ruta_temp, "w", encoding="utf-8") as f:
            f.write(codigo)

        exito, output = probar_agente(ruta_temp)

        if exito:
            shutil.copy2(ruta_temp, archivo)
            try:
                os.remove(ruta_temp)
            except Exception:
                pass
            registrar_en_habilidades(archivo, area, "Agente que realiza " + tema)
            log("    [OK] APROBADO tras " + str(intento) + " intento(s): " + str(output)[:80])
            return

        ultimo_error = output
        log("    [WARN] Fallo: " + str(output)[:80])
        time.sleep(2)

# ---------------------------------------------
#  PROCESAR LOTE
# ---------------------------------------------

def procesar_lote(plan, numero_lote):
    log("=" * 55)
    log("LOTE #" + str(numero_lote) + " — " + str(len(plan)) + " agentes")
    log("Areas: " + ", ".join(sorted(set(s['area'] for s in plan))))
    log("=" * 55)

    inicio = time.time()
    for i, spec in enumerate(plan, 1):
        procesar_agente(spec, i, len(plan))
        time.sleep(PAUSA_AGENTE)

    duracion  = int(time.time() - inicio)
    total_hab = len(cargar_habilidades())
    log("[OK] LOTE #" + str(numero_lote) + " COMPLETO en " + str(duracion) + "s — Total: " + str(total_hab) + " agentes")

# ---------------------------------------------
#  MODO MEJORA
# ---------------------------------------------

def seleccionar_agentes_a_mejorar(n=15):
    hab = cargar_habilidades()
    candidatos = []
    for archivo, info in hab.items():
        if not archivo.endswith(".py") or not os.path.exists(archivo):
            continue
        try:
            size = os.path.getsize(archivo)
            candidatos.append((size, archivo, info))
        except Exception:
            continue
    candidatos.sort(key=lambda x: x[0])
    return candidatos[:n]

def mejorar_agente(archivo, info):
    try:
        with open(archivo, "r", encoding="utf-8", errors="replace") as f:
            codigo_actual = f.read()
    except Exception as e:
        log("    No se pudo leer " + archivo + ": " + str(e))
        return None

    area        = info.get("categoria", "GENERAL")
    descripcion = info.get("descripcion", "")

    prompt = (
        "Mejora este agente Python de la Agencia Santi.\n\n"
        "ARCHIVO: " + archivo + "\n"
        "AREA: " + area + "\n"
        "DESCRIPCION: " + descripcion + "\n\n"
        "CODIGO ACTUAL:\n" + codigo_actual[:2000] + "\n\n"
        "MEJORAS: mas output util, mejor manejo de errores, datos mas reales de Mexico, "
        "permitir parametros por sys.argv, agregar resumen ejecutivo al final.\n\n"
        "REGLAS: mantener main(), solo stdlib, NUNCA input(), output minimo 5 lineas.\n\n"
        "DEVUELVE SOLO EL CODIGO MEJORADO. Sin markdown."
    )
    respuesta = ia(prompt)
    return limpiar_codigo(respuesta) if respuesta else None

def procesar_lote_mejora(numero_lote):
    candidatos = seleccionar_agentes_a_mejorar(TAMANO_LOTE)
    if not candidatos:
        log("Sin agentes para mejorar")
        return

    log("LOTE MEJORA #" + str(numero_lote) + " — " + str(len(candidatos)) + " agentes")
    mejorados = 0

    for i, (size, archivo, info) in enumerate(candidatos, 1):
        log("  [" + str(i) + "/" + str(len(candidatos)) + "] Mejorando " + archivo)
        codigo_mejorado = mejorar_agente(archivo, info)
        if not codigo_mejorado:
            time.sleep(2)
            continue
        valido, err = validar_sintaxis(codigo_mejorado)
        if not valido:
            log("    Sintaxis invalida: " + str(err)[:60])
            time.sleep(2)
            continue
        bak = archivo.replace(".py", ".bak.mejora_" + datetime.now().strftime('%Y%m%d_%H%M%S'))
        try:
            shutil.copy2(archivo, bak)
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(codigo_mejorado)
            nuevo_size = os.path.getsize(archivo)
            log("    Mejorado: " + str(size) + " -> " + str(nuevo_size) + " bytes")
            mejorados += 1
        except Exception as e:
            log("    Error guardando: " + str(e))
        time.sleep(PAUSA_AGENTE)

    total_hab = len(cargar_habilidades())
    log("LOTE MEJORA #" + str(numero_lote) + " COMPLETO — " + str(mejorados) + "/" + str(len(candidatos)) + " mejorados — " + str(total_hab) + " agentes")

# ---------------------------------------------
#  BUCLE INFINITO
# ---------------------------------------------

def detectar_modo(arg=None):
    if arg:
        return arg.lower()
    total = len(cargar_habilidades())
    return "crear" if total < UMBRAL_MODO_MEJORA else "mejorar"

def bucle_infinito(modo_forzado=None):
    log("=" * 55)
    log("FABRICA DE AGENTES — BUCLE INFINITO")
    log("Umbral auto-switch: " + str(UMBRAL_MODO_MEJORA) + " agentes")
    log("Modo: " + str(modo_forzado or "automatico"))
    log("Ctrl+C para detener")
    log("=" * 55)

    numero_lote     = 1
    total_creados   = 0
    total_mejorados = 0

    while True:
        try:
            modo         = modo_forzado or detectar_modo()
            total_actual = len(cargar_habilidades())
            log("Modo: " + modo.upper() + " | Agentes: " + str(total_actual))

            if modo == "crear":
                existentes = agentes_existentes()
                plan = generar_plan_lote(numero_lote, existentes)
                if not plan:
                    log("Catalogo agotado — cambiando a modo MEJORAR")
                    modo_forzado = "mejorar"
                    continue
                procesar_lote(plan, numero_lote)
                total_creados += len(plan)
                log("Acumulado: " + str(total_creados) + " creados en " + str(numero_lote) + " lotes")
            else:
                procesar_lote_mejora(numero_lote)
                total_mejorados += TAMANO_LOTE
                log("Acumulado: " + str(total_mejorados) + " mejoras en " + str(numero_lote) + " lotes")

            numero_lote += 1
            log("Siguiente lote en " + str(PAUSA_LOTE) + "s...")
            time.sleep(PAUSA_LOTE)

        except KeyboardInterrupt:
            log("Fabrica detenida. Lotes: " + str(numero_lote-1) + " | Creados: " + str(total_creados) + " | Mejorados: " + str(total_mejorados))
            sys.exit(0)
        except Exception as e:
            log("Error en lote #" + str(numero_lote) + ": " + str(e))
            log("Reintentando en 10s...")
            time.sleep(10)


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else None
    if modo and modo not in ("crear", "mejorar"):
        print("Uso: python fabrica_agentes.py [crear|mejorar]")
        sys.exit(1)
    bucle_infinito(modo)