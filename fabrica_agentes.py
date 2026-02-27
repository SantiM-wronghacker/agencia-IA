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
UMBRAL_MODO_MEJORA = 300   # antes 500; con 255 agentes ya conviene mejorar
MAX_LLM_FALLOS    = 6      # reintentos LLM antes de saltar al siguiente agente

AREAS_TEMAS = {
    "FINANZAS": [
        "analisis_estados_financieros", "control_presupuesto_mensual",
        "calculo_depreciacion_activos", "analisis_punto_equilibrio",
        "simulador_inversion_cetes", "calculo_rendimiento_fondos",
        "analizador_deuda_empresarial", "proyector_flujo_caja_3_anos",
        "calculo_capital_trabajo", "comparador_instrumentos_inversion",
        "calculo_nomina_mensual_mexico", "analizador_razones_financieras",
        "estimador_valor_empresa", "calculadora_afore_retiro",
        "calculo_impuesto_sobre_renta_mensual", "simulador_fondo_emergencia",
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
    ],
    "CEREBRO": [
        "orquestador_agentes_industria", "router_consultas_complejidad",
        "agente_memoria_contextual", "generador_prompts_optimizados",
        "coordinador_pipeline_datos", "monitor_performance_agentes",
        "agente_resumen_ejecutivo", "clasificador_intencion_usuario",
        "dispatcher_multiagente", "agente_validacion_resultados",
    ],
    "HERRAMIENTAS": [
        "generador_reportes_csv", "scheduler_tareas_programadas",
        "validador_datos_entrada", "compresor_archivador_logs",
        "monitor_uso_apis", "generador_backups_automaticos",
        "parser_archivos_configuracion", "monitor_salud_sistema",
        "notificador_alertas_consola", "limpiador_archivos_temporales",
        "generador_hash_verificacion", "conversor_formatos_datos",
    ],
    "LEGAL": [
        "generador_carta_poder", "checklist_requisitos_notariales",
        "convenio_prestacion_servicios", "analizador_clausulas_riesgo",
        "guia_constitucion_empresa_mexico", "generador_finiquito_laboral",
        "calculadora_indemnizacion_imss", "checklist_cumplimiento_sat",
        "generador_acta_acuerdos", "template_contrato_servicios_profesionales",
    ],
    "MARKETING": [
        "generador_plan_contenidos", "analizador_buyer_persona",
        "calculadora_presupuesto_publicitario", "generador_propuesta_valor",
        "analizador_funnel_ventas", "generador_copy_facebook_ads",
        "calculadora_cac_ltv", "generador_estrategia_referidos",
        "analizador_metricas_campana", "generador_calendario_editorial",
        "generador_bio_redes_sociales", "analizador_hashtags_instagram",
    ],
    "VENTAS": [
        "calculadora_pipeline_ventas", "generador_propuesta_comercial",
        "analizador_objeciones", "tracker_seguimiento_prospectos",
        "calculadora_forecast_mensual", "generador_argumentario_ventas",
        "analizador_ciclo_venta", "script_cierre_ventas",
        "calculadora_descuentos_margen", "generador_email_cotizacion",
    ],
    "OPERACIONES": [
        "gestor_inventario_basico", "calculadora_costo_operacion",
        "generador_procedimientos_sop", "analizador_kpis_operativos",
        "calculadora_capacidad_instalada", "gestor_ordenes_trabajo",
        "analizador_cuellos_botella", "calculadora_eficiencia_operativa",
        "generador_checklist_procesos", "calculadora_tiempo_produccion",
    ],
    "RECURSOS HUMANOS": [
        "calculadora_costo_empleado_mexico", "generador_descripcion_puesto",
        "calculadora_prestaciones_ley", "generador_evaluacion_desempenio",
        "calculadora_liquidacion_laboral", "analizador_clima_organizacional",
        "generador_plan_onboarding", "calculadora_horas_extra",
        "generador_encuesta_satisfaccion", "calculadora_rotacion_personal",
    ],
    "TECNOLOGIA": [
        "calculadora_costo_infraestructura_cloud",
        "generador_especificaciones_tecnicas", "analizador_stack_tecnologico",
        "calculadora_roi_automatizacion", "plan_migracion_cloud",
        "analizador_deuda_tecnica", "calculadora_sla_uptime",
        "generador_documentacion_api", "calculadora_licencias_software",
        "analizador_seguridad_basica",
    ],
    "SALUD": [
        "calculadora_imc_riesgo", "generador_plan_nutricional",
        "calculadora_calorias_actividad", "analizador_costos_seguro_medico",
        "checklist_consulta_medica", "calculadora_dosis_medicamento",
        "generador_recordatorio_medicamentos", "analizador_habitos_saludables",
    ],
    "EDUCACION": [
        "generador_plan_estudio", "calculadora_costo_carrera_mexico",
        "generador_ejercicios_practica", "analizador_tecnicas_aprendizaje",
        "calculadora_roi_educativo", "generador_rubrica_evaluacion",
        "generador_temario_curso", "calculadora_becas_disponibles",
    ],
    "LOGISTICA": [
        "calculadora_costo_envio_mexico", "optimizador_ruta_entregas",
        "calculadora_tiempo_transito", "analizador_costo_ultima_milla",
        "generador_manifiesto_carga", "calculadora_capacidad_almacen",
        "tracker_pedidos_basico", "calculadora_costo_importacion",
    ],
    "TURISMO": [
        "calculadora_presupuesto_viaje", "generador_itinerario_viaje",
        "comparador_hospedaje", "calculadora_roi_renta_vacacional",
        "analizador_temporadas", "generador_paquete_turistico",
    ],
    "RESTAURANTES": [
        "calculadora_costo_platillo", "generador_menu_precios",
        "calculadora_punto_equilibrio_restaurante",
        "analizador_merma_desperdicio", "generador_receta_estandarizada",
        "calculadora_precio_venta_platillo",
    ],
    "BIENES RAICES COMERCIALES": [
        "calculadora_renta_oficina_cdmx", "analizador_local_comercial",
        "calculadora_roi_bodega_industrial", "comparador_zonas_comerciales",
        "estimador_aforo_local", "calculadora_contrato_arrendamiento_comercial",
    ],
    "SEGUROS": [
        "calculadora_seguro_vida_mexico", "comparador_seguros_auto",
        "analizador_cobertura_gastos_medicos", "calculadora_prima_seguro",
        "generador_reporte_siniestro", "checklist_contratacion_seguro",
    ],
    "CONTABILIDAD": [
        "calculadora_iva_desglosado", "generador_factura_conceptos",
        "calculadora_ptu_empleados", "analizador_deducciones_fiscales",
        "calculadora_regimen_fiscal_adecuado", "generador_balance_general_simple",
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