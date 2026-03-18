# 🗺️ Mapa Completo de Documentos — Agencia Santi v2

> **Última actualización**: 2026-03-03
> **Total de archivos**: 564 en raíz | ~1,138 en todo el repositorio (sin .git)
> **Agentes Python**: 510 | **Categorías**: 19

---

## 📊 Resumen General

| Tipo de Archivo | Cantidad | Extensión |
|---|---|---|
| Agentes / Scripts Python | 510 | `.py` |
| Datos y configuración JSON | 12 | `.json` |
| Documentación Markdown | 7 | `.md` |
| Guías y notas de texto | 18 | `.txt` |
| Scripts de Windows | 11 | `.bat` |
| Páginas HTML | 2 | `.html` |
| Datos CSV | 1 | `.csv` |
| Dependencias | 1 | `requirements.txt` |

---

## 🧠 Categorías de Agentes (19 categorías — 510 agentes)

Cada agente Python vive en la raíz del proyecto y está clasificado en `categorias/` mediante enlaces.

| # | Categoría | Agentes | Descripción |
|---|---|---|---|
| 1 | BIENES_RAÍCES_COMERCIALES | 4 | Análisis de locales, rentas de oficina, ROI de bodegas, aforo |
| 2 | CEREBRO | 51 | Core del sistema: routers, memoria, RAG, evolución, diagnóstico |
| 3 | CONTABILIDAD | 21 | IVA, SAT, balances, CFDI, facturas, acta constitutiva |
| 4 | EDUCACIÓN | 9 | Estilos de aprendizaje, becas, rúbricas, temarios, planes de estudio |
| 5 | FINANZAS | 73 | ROI, flujo de caja, depreciación, ISR, puntos de equilibrio, inversiones |
| 6 | HERRAMIENTAS | 158 | Utilidades generales: API, dashboard, monitores, limpiadores, parsers |
| 7 | LEGAL | 16 | Contratos, cláusulas, finiquitos, poderes notariales, NDA |
| 8 | LOGÍSTICA | 10 | Envíos, importación, rutas de entrega, almacén, tracking |
| 9 | MARKETING | 18 | Copy para redes, buyer persona, funnels, hashtags, email marketing |
| 10 | MICRO_TAREAS | 14 | Formateadores, validadores, extractores, normalizadores |
| 11 | OPERACIONES | 17 | KPIs, capacidad de planta, órdenes, SOP, cuellos de botella |
| 12 | REAL_ESTATE | 20 | Plusvalía, hipotecas, fichas técnicas, due diligence, crowdfunding |
| 13 | RECURSOS_HUMANOS | 17 | Nómina, prestaciones, clima laboral, rotación, onboarding |
| 14 | RESTAURANTES | 13 | Recetas, menús, merma, food cost, turnos, platillos rentables |
| 15 | SALUD | 9 | IMC, dosis, calorías, hábitos, signos vitales, plan nutricional |
| 16 | SEGUROS | 10 | Pólizas, siniestros, primas, comparador de seguros |
| 17 | TECNOLOGÍA | 16 | API, stack tecnológico, SLA, cloud, seguridad, licencias |
| 18 | TURISMO | 10 | Itinerarios, paquetes, hospedaje, presupuesto de viaje |
| 19 | VENTAS | 24 | Pipeline, CRM, scripts de ventas, cotizaciones, forecasting |

---

## 🧠 CEREBRO (51 agentes) — Núcleo del Sistema

Componentes fundamentales que dirigen la inteligencia del sistema.

| Archivo | Función |
|---|---|
| `agent_router.py` | Router principal de tareas a agentes |
| `agent_router_memory.py` | Router con memoria persistente |
| `agent_router_memory_pro.py` | Router avanzado con memoria y contexto |
| `agent_router_projects.py` | Router especializado en proyectos |
| `agent_router_state_autoscale.py` | Router con autoescalado de estado |
| `agent_router_state_pro.py` | Router de estado profesional |
| `agent_files.py` | Gestión de archivos del agente |
| `agent_rag.py` | Agente RAG (Retrieval Augmented Generation) |
| `agent_team.py` | Gestión de equipos de agentes |
| `agente_arquitecto_web.py` | Arquitecto de proyectos web |
| `agente_estrategia.py` | Estrategia empresarial |
| `agente_fact_checking.py` | Verificación de hechos |
| `agente_memoria_contextual.py` | Memoria contextual del sistema |
| `agente_resumen_ejecutivo.py` | Generador de resúmenes ejecutivos |
| `agente_validacion_resultados.py` | Validación de resultados de agentes |
| `auto_evolucion.py` | Auto-evolución del sistema |
| `auto_evolucion_pro.py` | Auto-evolución avanzada |
| `auto_run.py` | Ejecución autónoma de tareas |
| `clasificador_intencion_usuario.py` | Clasifica la intención del usuario |
| `clasificador_prioridad_tareas.py` | Priorización automática de tareas |
| `clasificador_tickets.py` | Clasificación de tickets de soporte |
| `clasificador_viviendas.py` | Clasificación de tipos de vivienda |
| `consola_maestra.py` | Consola de control central |
| `diagnostico_agentes.py` | Diagnóstico de salud de agentes |
| `dispatcher_multiagente.py` | Despacho de tareas a múltiples agentes |
| `fabrica_agentes.py` | Fábrica para crear nuevos agentes |
| `generador_estrategia_referidos.py` | Estrategias de referidos |
| `generador_nota_evolucion.py` | Notas de evolución del sistema |
| `generador_politica_devolucion.py` | Políticas de devolución |
| `generador_prompts_optimizados.py` | Optimización de prompts |
| `hub_control.py` | Hub central de control |
| `integrador_router.py` | Integrador de routers |
| `llm_router.py` | Router de modelos LLM |
| `maestro_ceo.py` | Agente maestro director |
| `memory_manager.py` | Gestión de memoria persistente |
| `monitor_performance_agentes.py` | Monitor de rendimiento |
| `noche_total.py` | Proceso nocturno de mantenimiento |
| `notificador_alertas_consola.py` | Alertas por consola |
| `patcher_pro.py` | Parcheo automático de agentes |
| `rag_index.py` | Indexador para RAG |
| `rag_pro.py` | RAG profesional |
| `rag_query.py` | Consultas RAG |
| `reclasificar_agentes.py` | Reclasificación automática de agentes |
| `resumen_diario_agente.py` | Resumen diario del sistema |
| `root_assistant.py` | Asistente raíz |
| `router_consultas_complejidad.py` | Router por complejidad |
| `router_tareas_proyectos.py` | Router de tareas por proyecto |
| `sistema_maestro.py` | Sistema maestro de coordinación |
| `supervisor_qa.py` | Supervisor de calidad |
| `test_agentes_list.py` | Test de listado de agentes |
| `test_evolucion.py` | Test de evolución |

---

## 💰 FINANZAS (73 agentes)

| Archivo | Función |
|---|---|
| `analisis_estados_financieros.py` | Análisis de estados financieros |
| `analisis_punto_equilibrio.py` | Punto de equilibrio |
| `analizador_flujo_caja.py` | Flujo de caja |
| `analizador_flujo_efectivo.py` | Flujo de efectivo |
| `analizador_rendimiento_grupo.py` | Rendimiento grupal |
| `calculadora_acero.py` | Cálculos de acero |
| `calculadora_afore_retiro.py` | AFORE y retiro |
| `calculadora_break_even_producto.py` | Break-even por producto |
| `calculadora_cap_rate_inmueble.py` | Cap Rate inmobiliario |
| `calculadora_comision.py` | Comisiones |
| `calculadora_comisiones.py` | Comisiones (variante) |
| `calculadora_concreto.py` | Cálculos de concreto |
| `calculadora_costo_produccion_agro.py` | Costo producción agrícola |
| `calculadora_costo_tratamiento.py` | Costo de tratamientos |
| `calculadora_depreciacion.py` | Depreciación de activos |
| `calculadora_descuento_precio.py` | Descuentos sobre precio |
| `calculadora_descuentos_margen.py` | Descuentos y margen |
| `calculadora_diferencia_fechas.py` | Diferencia entre fechas |
| `calculadora_dosis.py` | Dosis (genérica) |
| `calculadora_enganche_credito_infonavit.py` | Enganche INFONAVIT |
| `calculadora_estadisticas.py` | Estadísticas generales |
| `calculadora_evapotranspiracion.py` | Evapotranspiración agrícola |
| `calculadora_fertilizante.py` | Fertilizantes |
| `calculadora_food_cost.py` | Food cost |
| `calculadora_gastos_escrituracion.py` | Gastos de escrituración |
| `calculadora_horas_extra.py` | Horas extra |
| `calculadora_indemnizacion_imss.py` | Indemnización IMSS |
| `calculadora_isr_basica.py` | ISR básico |
| `calculadora_liquidacion_laboral.py` | Liquidación laboral |
| `calculadora_lote_economico.py` | Lote económico |
| `calculadora_margen_producto.py` | Margen por producto |
| `calculadora_materiales.py` | Materiales de construcción |
| `calculadora_ocupacion_renta.py` | Ocupación para renta |
| `calculadora_oee.py` | OEE (Eficiencia global) |
| `calculadora_penalizaciones.py` | Penalizaciones |
| `calculadora_peso_volumetrico.py` | Peso volumétrico |
| `calculadora_plazo_vencimiento.py` | Plazo de vencimiento |
| `calculadora_plusvalia.py` | Plusvalía |
| `calculadora_porciones.py` | Porciones |
| `calculadora_presupuesto_publicitario.py` | Presupuesto publicitario |
| `calculadora_regalias_franquicia.py` | Regalías de franquicia |
| `calculadora_rendimiento_cultivo.py` | Rendimiento de cultivo |
| `calculadora_retorno_desarrollo_obra.py` | Retorno de obra |
| `calculadora_riesgo_cardiovascular.py` | Riesgo cardiovascular |
| `calculadora_roi.py` | ROI general |
| `calculadora_roi_agro.py` | ROI agrícola |
| `calculadora_roi_automatizacion.py` | ROI de automatización |
| `calculadora_roi_campanas.py` | ROI de campañas |
| `calculadora_roi_educativo.py` | ROI educativo |
| `calculadora_roi_mexico.py` | ROI México |
| `calculadora_scrap_rate.py` | Scrap rate (desperdicio) |
| `calculadora_shipping_internacional.py` | Shipping internacional |
| `calculadora_takt_time.py` | Takt time |
| `calculadora_tiempo_produccion.py` | Tiempo de producción |
| `calculadora_tiempo_transito.py` | Tiempo de tránsito |
| `calculadora_volumetria_tierra.py` | Volumetría de tierra |
| `calculo_depreciacion_activos.py` | Depreciación de activos |
| `calculo_impuesto_sobre_renta_mensual.py` | ISR mensual |
| `calculo_rendimiento_fondos.py` | Rendimiento de fondos |
| `control_presupuesto_mensual.py` | Presupuesto mensual |
| `conversor_formatos_datos.py` | Conversor de formatos |
| `conversor_pesos_dolar.py` | Pesos a dólares |
| `generador_estado_resultados.py` | Estado de resultados |
| `generador_estado_resultados_proyectado.py` | Estado de resultados proyectado |
| `generador_presupuesto_obra.py` | Presupuesto de obra |
| `orquestador_agentes_industria.py` | Orquestador industrial |
| `orquestador_clawbot.py` | Orquestador Clawbot |
| `orquestador_proyectos.py` | Orquestador de proyectos |
| `proyeccion_utilidades.py` | Proyección de utilidades |
| `proyector_flujo_caja_3_anos.py` | Flujo de caja a 3 años |
| `proyector_flujo_caja_3_años.py` | Flujo de caja a 3 años (variante) |
| `simulador_inversion_cetes.py` | Simulador CETES |
| `verificador_documentacion.py` | Verificador de documentación |

---

## 🔧 HERRAMIENTAS (158 agentes)

Utilidades generales del sistema. Incluyen API, dashboard, monitores, generadores genéricos, limpiadores, parsers y más. Archivo completo listado en `categorias/HERRAMIENTAS/`.

### Subcategorías principales:

| Tipo | Ejemplos | Cant. aprox. |
|---|---|---|
| Generadores | `generador_*.py` — brief, calendario, checklist, encuesta, etc. | ~60 |
| Analizadores | `analizador_*.py` — anomalías, demanda, defectos, tendencias | ~25 |
| Planificadores | `planificador_*.py` — producción, riego, siembra, capacitación | ~10 |
| Monitores | `monitor_*.py` — GPU, internet, cambios directorio | ~5 |
| Comparadores | `comparador_*.py` — créditos, escenarios, zonas | ~5 |
| API/Web | `api.py`, `app.py`, `dashboard_web.py`, `web_bridge.py` | ~5 |
| Limpiadores | `limpiador_*.py` — archivos temporales, backups, datos | 3 |
| Infraestructura | `config.py`, `core.py`, `database.py`, `celery_app.py`, `logging_config.py` | ~5 |
| Otros | `chatbot_faq.py`, `ejecutar_mision.py`, `scheduler_tareas_programadas.py` | ~40 |

---

## 📑 CONTABILIDAD (21 agentes)

| Archivo | Función |
|---|---|
| `analizador_balances.py` | Análisis de balances |
| `analizador_cumplimiento_fiscal.py` | Cumplimiento fiscal |
| `analizador_deducciones_fiscales.py` | Deducciones fiscales |
| `asistente_iva.py` | Asistente de IVA |
| `asistente_iva_contable.py` | IVA contable |
| `calculadora_eficiencia_operativa.py` | Eficiencia operativa |
| `calculadora_iva_desglosado.py` | IVA desglosado |
| `calculadora_iva_rapida.py` | IVA rápida |
| `calculadora_ptu_empleados.py` | PTU empleados |
| `calculadora_regimen_fiscal_adecuado.py` | Régimen fiscal |
| `calculadora_tasa_efectiva_anual.py` | Tasa efectiva anual |
| `checklist_cumplimiento_sat.py` | Checklist SAT |
| `compresor_archivador_logs.py` | Archivador de logs |
| `generador_acta_constitutiva.py` | Acta constitutiva |
| `generador_aviso_privacidad.py` | Aviso de privacidad |
| `generador_balance_general_simple.py` | Balance general |
| `generador_comparativa_seguros.py` | Comparativa de seguros |
| `generador_encuesta_csat.py` | Encuesta CSAT |
| `generador_encuesta_satisfaccion.py` | Encuesta de satisfacción |
| `generador_factura_conceptos.py` | Factura con conceptos |
| `validador_cfdi.py` | Validador de CFDI |

---

## ⚖️ LEGAL (16 agentes)

| Archivo | Función |
|---|---|
| `analizador_clausulas_riesgo.py` | Cláusulas de riesgo |
| `analizador_riesgo_legal.py` | Riesgo legal |
| `calculadora_contrato_arrendamiento_comercial.py` | Arrendamiento comercial |
| `calculadora_finiquito.py` | Finiquito |
| `checklist_requisitos_notariales.py` | Requisitos notariales |
| `generador_acta_acuerdos.py` | Acta de acuerdos |
| `generador_carta_poder.py` | Carta poder |
| `generador_contrato_arrendamiento.py` | Contrato arrendamiento |
| `generador_contrato_arrendamiento_comercial.py` | Contrato arrendamiento comercial |
| `generador_contrato_freelance.py` | Contrato freelance |
| `generador_contrato_laboral.py` | Contrato laboral |
| `generador_contrato_obra.py` | Contrato de obra |
| `generador_contrato_servicios.py` | Contrato de servicios |
| `generador_finiquito_laboral.py` | Finiquito laboral |
| `generador_poder_notarial.py` | Poder notarial |
| `template_contrato_servicios_profesionales.py` | Template contrato profesional |

---

## 📦 LOGÍSTICA (10 agentes)

| Archivo | Función |
|---|---|
| `calculadora_costo_envio_mexico.py` | Costo envío México |
| `calculadora_costo_importacion.py` | Costo importación |
| `calculadora_costos_envio.py` | Costos de envío |
| `generador_guia_envio.py` | Guía de envío |
| `generador_politica_envio.py` | Política de envío |
| `optimizador_ruta_entregas.py` | Optimización de rutas |
| `optimizador_rutas_entrega.py` | Optimización de rutas (variante) |
| `planificador_almacen.py` | Planificación de almacén |
| `tracker_pedidos.py` | Seguimiento de pedidos |
| `tracker_pedidos_basico.py` | Seguimiento de pedidos (básico) |

---

## 📢 MARKETING (18 agentes)

| Archivo | Función |
|---|---|
| `analizador_buyer_persona.py` | Buyer persona |
| `analizador_funnel_conversion.py` | Funnel de conversión |
| `analizador_funnel_ventas.py` | Funnel de ventas |
| `analizador_hashtags_instagram.py` | Hashtags Instagram |
| `calculadora_cac_ltv.py` | CAC / LTV |
| `calculadora_calificaciones.py` | Calificaciones |
| `calculadora_roi_renta_vacacional.py` | ROI renta vacacional |
| `generador_bio_redes_sociales.py` | Bio para redes |
| `generador_buyer_persona_pro.py` | Buyer persona pro |
| `generador_copy_facebook.py` | Copy Facebook |
| `generador_copy_facebook_ads.py` | Copy Facebook Ads |
| `generador_copy_instagram.py` | Copy Instagram |
| `generador_email_marketing.py` | Email marketing |
| `generador_especificaciones_tecnicas.py` | Especificaciones técnicas |
| `generador_hash_verificacion.py` | Hash de verificación |
| `generador_plan_contenidos.py` | Plan de contenidos |
| `planificador_contenido_mensual.py` | Contenido mensual |
| `planificador_redes_sociales.py` | Redes sociales |

---

## 🏢 OPERACIONES (17 agentes)

| Archivo | Función |
|---|---|
| `analizador_capacidad_planta.py` | Capacidad de planta |
| `analizador_cuellos_botella.py` | Cuellos de botella |
| `analizador_kpis_operativos.py` | KPIs operativos |
| `analizador_tendencias_soporte.py` | Tendencias de soporte |
| `calculadora_capacidad_almacen.py` | Capacidad de almacén |
| `calculadora_capacidad_instalada.py` | Capacidad instalada |
| `calculadora_capacidad_produccion.py` | Capacidad de producción |
| `calculadora_costo_operacion.py` | Costo de operación |
| `calculadora_punto_reorden.py` | Punto de reorden |
| `generador_faq_soporte.py` | FAQ de soporte |
| `generador_macro_soporte.py` | Macros de soporte |
| `generador_orden_compra.py` | Orden de compra |
| `generador_orden_produccion.py` | Orden de producción |
| `generador_procedimientos_sop.py` | Procedimientos SOP |
| `generador_reporte_kpi.py` | Reporte de KPI |
| `gestor_ordenes_trabajo.py` | Órdenes de trabajo |
| `mapeador_capacidades.py` | Mapeo de capacidades |

---

## 🏠 REAL_ESTATE (20 agentes)

| Archivo | Función |
|---|---|
| `analizador_cartera_propiedades.py` | Cartera de propiedades |
| `analizador_plusvalia_colonia.py` | Plusvalía por colonia |
| `analizador_tendencias_mercado_inmobiliario.py` | Tendencias inmobiliarias |
| `buscador_plusvalia.py` | Buscador de plusvalía |
| `calculadora_renta_justa_m2.py` | Renta justa por m² |
| `calificador_leads.py` | Calificador de leads |
| `comparador_hipotecas_bancos_mexico.py` | Comparador hipotecas |
| `generador_copy_google_ads.py` | Copy Google Ads |
| `generador_copy_propiedades.py` | Copy para propiedades |
| `generador_due_diligence_inmobiliario.py` | Due diligence inmobiliario |
| `generador_ficha_producto.py` | Ficha de producto |
| `generador_fichas_tecnicas.py` | Fichas técnicas |
| `mapa_competencia.py` | Mapa de competencia |
| `plan_comercializacion_propiedad.py` | Comercialización de propiedad |
| `reporte_avaluo_basico.py` | Avalúo básico |
| `seguimiento_whatsapp.py` | Seguimiento WhatsApp |
| `simulador_ahorro_meta_personal.py` | Ahorro meta personal |
| `simulador_crowdfunding_inmobiliario.py` | Crowdfunding inmobiliario |
| `simulador_fondo_emergencia.py` | Fondo de emergencia |
| `simulador_hipoteca.py` | Simulador de hipoteca |

---

## 🏗️ BIENES_RAÍCES_COMERCIALES (4 agentes)

| Archivo | Función |
|---|---|
| `analizador_local_comercial.py` | Análisis de local comercial |
| `calculadora_renta_oficina_cdmx.py` | Renta oficina CDMX |
| `calculadora_roi_bodega_industrial.py` | ROI bodega industrial |
| `estimador_aforo_local.py` | Estimador de aforo |

---

## 👥 RECURSOS_HUMANOS (17 agentes)

| Archivo | Función |
|---|---|
| `analizador_clima_laboral.py` | Clima laboral |
| `analizador_clima_organizacional.py` | Clima organizacional |
| `calculadora_costo_empleado_mexico.py` | Costo empleado México |
| `calculadora_imss_empleado.py` | IMSS empleado |
| `calculadora_nomina.py` | Nómina |
| `calculadora_prestaciones.py` | Prestaciones |
| `calculadora_prestaciones_ley.py` | Prestaciones de ley |
| `calculadora_rotacion.py` | Rotación de personal |
| `calculadora_rotacion_mesa.py` | Rotación de mesa |
| `calculadora_rotacion_personal.py` | Rotación de personal (variante) |
| `calculo_nomina_mensual_mexico.py` | Nómina mensual México |
| `convenio_prestacion_servicios.py` | Convenio de servicios |
| `evaluador_desempeno.py` | Evaluación de desempeño |
| `generador_onboarding.py` | Proceso de onboarding |
| `generador_plan_onboarding.py` | Plan de onboarding |
| `generador_plan_rotacion_cultivos.py` | Plan rotación cultivos |
| `generador_politica_rrhh.py` | Política RRHH |

---

## 🍽️ RESTAURANTES (13 agentes)

| Archivo | Función |
|---|---|
| `analizador_merma.py` | Merma |
| `analizador_merma_desperdicio.py` | Merma y desperdicio |
| `analizador_platillos_rentables.py` | Platillos rentables |
| `calculadora_costo_platillo.py` | Costo por platillo |
| `calculadora_costo_receta.py` | Costo por receta |
| `calculadora_punto_equilibrio_restaurante.py` | Punto equilibrio restaurante |
| `generador_ficha_tecnica_receta.py` | Ficha técnica de receta |
| `generador_menu_precios.py` | Menú con precios |
| `generador_menu_semanal.py` | Menú semanal |
| `generador_receta_estandarizada.py` | Receta estandarizada |
| `generador_receta_medica.py` | Receta médica |
| `generador_receta_nutricion.py` | Receta de nutrición |
| `planificador_turnos_restaurante.py` | Turnos de restaurante |

---

## 🏥 SALUD (9 agentes)

| Archivo | Función |
|---|---|
| `analizador_cobertura_gastos_medicos.py` | Cobertura gastos médicos |
| `analizador_costos_seguro_medico.py` | Costos seguro médico |
| `analizador_habitos_saludables.py` | Hábitos saludables |
| `calculadora_calorias_actividad.py` | Calorías por actividad |
| `calculadora_dosis_medicamento.py` | Dosis de medicamento |
| `calculadora_imc_riesgo.py` | IMC y riesgo |
| `generador_plan_nutricional.py` | Plan nutricional |
| `generador_recordatorio_medicamentos.py` | Recordatorio medicamentos |
| `monitor_salud_sistema.py` | Salud del sistema |

---

## 🛡️ SEGUROS (10 agentes)

| Archivo | Función |
|---|---|
| `analizador_siniestros.py` | Siniestros |
| `calculadora_prima.py` | Prima de seguro |
| `calculadora_prima_seguro.py` | Prima de seguro (variante) |
| `calculadora_seguro_vida_mexico.py` | Seguro de vida México |
| `checklist_contratacion_seguro.py` | Checklist contratación |
| `comparador_seguros_auto.py` | Comparador seguros auto |
| `cotizador_seguro_empresarial.py` | Seguro empresarial |
| `cotizador_seguro_hogar.py` | Seguro de hogar |
| `generador_dictamen_siniestro.py` | Dictamen siniestro |
| `generador_reporte_siniestro.py` | Reporte de siniestro |

---

## 🎓 EDUCACIÓN (9 agentes)

| Archivo | Función |
|---|---|
| `analizador_estilos_aprendizaje.py` | Estilos de aprendizaje |
| `analizador_tecnicas_aprendizaje.py` | Técnicas de aprendizaje |
| `asistente_estudio_finanzas.py` | Estudio de finanzas |
| `calculadora_becas_disponibles.py` | Becas disponibles |
| `calculadora_costo_carrera_mexico.py` | Costo carrera México |
| `generador_plan_estudio.py` | Plan de estudio |
| `generador_rubrica.py` | Rúbrica |
| `generador_rubrica_evaluacion.py` | Rúbrica de evaluación |
| `generador_temario_curso.py` | Temario de curso |

---

## 💻 TECNOLOGÍA (16 agentes)

| Archivo | Función |
|---|---|
| `analizador_seguridad_basica.py` | Seguridad básica |
| `analizador_stack_tecnologico.py` | Stack tecnológico |
| `api.py` | API principal |
| `api_agencia.py` | API de la agencia |
| `calculadora_comision_rapida.py` | Comisión rápida |
| `calculadora_costo_infraestructura_cloud.py` | Infra cloud |
| `calculadora_isr_mensual_rapido.py` | ISR mensual rápido |
| `calculadora_licencias_software.py` | Licencias de software |
| `calculadora_sla_uptime.py` | SLA y uptime |
| `calculo_capital_trabajo.py` | Capital de trabajo |
| `check_api_code.py` | Verificador de código API |
| `generador_documentacion_api.py` | Documentación de API |
| `generador_sla_reporte.py` | Reporte SLA |
| `monitor_uso_apis.py` | Monitor de uso API |
| `plan_migracion_cloud.py` | Plan migración cloud |
| `restart_api.py` | Reinicio de API |

---

## ✈️ TURISMO (10 agentes)

| Archivo | Función |
|---|---|
| `calculadora_fee_viaje.py` | Fee de viaje |
| `calculadora_presupuesto_viaje.py` | Presupuesto de viaje |
| `calculadora_tipo_cambio_viaje.py` | Tipo de cambio viaje |
| `comparador_hospedaje.py` | Comparador hospedaje |
| `cotizador_paquete_turistico.py` | Paquete turístico |
| `cotizador_viaje.py` | Cotizador de viaje |
| `generador_checklist_viaje.py` | Checklist de viaje |
| `generador_itinerario.py` | Itinerario |
| `generador_itinerario_viaje.py` | Itinerario de viaje |
| `generador_paquete_turistico.py` | Paquete turístico |

---

## 💼 VENTAS (24 agentes)

| Archivo | Función |
|---|---|
| `analizador_ciclo_venta.py` | Ciclo de venta |
| `analizador_cierre_ventas.py` | Cierre de ventas |
| `analizador_objeciones.py` | Objeciones |
| `analizador_territorio_ventas.py` | Territorio de ventas |
| `calculadora_forecast_mensual.py` | Forecast mensual |
| `calculadora_pipeline_ventas.py` | Pipeline de ventas |
| `calculadora_precio_venta_platillo.py` | Precio venta platillo |
| `coordinador_pipeline_datos.py` | Pipeline de datos |
| `generador_argumentario_ventas.py` | Argumentario de ventas |
| `generador_cotizacion.py` | Cotización |
| `generador_email_cotizacion.py` | Email de cotización |
| `generador_email_postventa.py` | Email postventa |
| `generador_email_prospecto.py` | Email a prospecto |
| `generador_presentacion_ventas.py` | Presentación de ventas |
| `generador_propuesta_comercial.py` | Propuesta comercial |
| `generador_propuesta_valor.py` | Propuesta de valor |
| `generador_script_ventas.py` | Script de ventas |
| `gestor_inventario_basico.py` | Inventario básico |
| `script_cierre_ventas.py` | Script cierre ventas |
| `script_llamada_ventas.py` | Script llamada ventas |
| `seguimiento_pipeline.py` | Seguimiento de pipeline |
| `tracker_inventario.py` | Tracker inventario |
| `tracker_metas_ventas.py` | Tracker metas ventas |
| `tracker_seguimiento_prospectos.py` | Seguimiento prospectos |

---

## 🔢 MICRO_TAREAS (14 agentes)

| Archivo | Función |
|---|---|
| `extractor_numeros_texto.py` | Extrae números de texto |
| `formateador_codigo_limpio.py` | Formatea código limpio |
| `formateador_moneda_mx.py` | Formatea moneda MX |
| `formateador_numero_palabras_mx.py` | Número a palabras MX |
| `formateador_telefono_mx.py` | Formatea teléfono MX |
| `normalizador_nombre_persona.py` | Normaliza nombres |
| `parseador_fecha_espanol.py` | Parsea fechas en español |
| `parseador_monto_texto.py` | Parsea montos de texto |
| `validador_clabe_bancaria.py` | Valida CLABE bancaria |
| `validador_curp_mexico.py` | Valida CURP |
| `validador_datos_entrada.py` | Valida datos de entrada |
| `validador_formato_rfc_mexico.py` | Valida formato RFC |
| `validador_leads.py` | Valida leads |
| `validador_rfc_mexico.py` | Valida RFC |

---

## 📄 Archivos de Datos y Configuración (JSON)

| Archivo | Contenido |
|---|---|
| `habilidades.json` | Catálogo completo de habilidades de todos los agentes |
| `habilidades.json.bak_reclasif_*` | Backup pre-reclasificación |
| `estado_maestro.json` | Estado actual del sistema maestro |
| `expansion_plan.json` | Plan de expansión de agentes |
| `tareas_pendientes.json` | Cola de tareas pendientes |
| `datos.json` | Datos de ejemplo/prueba |
| `datos.csv` | Datos en formato CSV |
| `Propuesta_Comercial_2023.json` | Propuesta comercial de ejemplo |
| `amef.json` | Análisis AMEF generado |
| `bitacora_vehiculos.json` | Bitácora de vehículos |
| `cotizacion_poliza_auto.json` | Cotización de póliza auto |
| `cotizacion_seguro_hogar.json` | Cotización seguro hogar |
| `orden_produccion.json` | Orden de producción |
| `reporte_deducciones_2026.json` | Reporte de deducciones 2026 |

---

## 📝 Documentación (Markdown)

| Archivo | Contenido |
|---|---|
| `STATUS.md` | Estado actual del sistema y arquitectura |
| `RESUMEN_CAMBIOS.md` | Resumen de cambios del dashboard |
| `DASHBOARD_SETUP.md` | Guía de configuración del dashboard |
| `DIAGNOSTICO_COMPLETO.md` | Diagnóstico de salud de todos los agentes |
| `MIGRACION_GROQ_COMPLETADA.md` | Documentación de migración a Groq |
| `PLAN_DASHBOARD_MEJORADO.md` | Plan del dashboard mejorado |
| `RESUMEN_SOLUCION_ARRANQUE.md` | Solución de arranque del sistema |
| `MAPA_DOCUMENTOS.md` | Este documento — mapa completo |

---

## 📋 Guías y Notas (TXT)

| Archivo | Contenido |
|---|---|
| `EMPEZAR_AQUI.txt` | Punto de entrada para usuarios nuevos |
| `QUICK_START.txt` | Inicio rápido |
| `GUIA_ARRANQUE.txt` | Guía de arranque del sistema |
| `GUIA_USAR_CREAR_EXPANSION.txt` | Guía para crear plan de expansión |
| `CREAR_EXPANSION_PLAN.txt` | Instrucciones de expansión |
| `INSTRUCCIONES_DASHBOARD.txt` | Instrucciones del dashboard |
| `MODO_SELECTOR_DASHBOARD.txt` | Selector de modo del dashboard |
| `PRUEBA_DASHBOARD.txt` | Pruebas del dashboard |
| `LISTO_PARA_PROBAR.txt` | Confirmación de ready-to-test |
| `MENU_PRIORIDADES.txt` | Menú de prioridades |
| `RESUMEN_IMPLEMENTACION.txt` | Resumen de implementación |
| `requirements.txt` | Dependencias Python |
| `mision_del_arquitecto.txt` | Misión del agente arquitecto |
| `descripcion_tour.txt` | Descripción de tour (generada) |
| `ficha_producto.txt` | Ficha de producto (generada) |
| `informe_plagas.txt` | Informe de plagas (generado) |
| `nota_evolucion.txt` | Nota de evolución (generada) |
| `script_ventas.txt` | Script de ventas (generado) |

---

## 🖥️ Scripts de Windows (BAT)

| Archivo | Función |
|---|---|
| `arrancar_simple.bat` | ✅ Arranque principal del sistema |
| `arrancar.bat` | Arranque alternativo |
| `arrancar_con_menu.bat` | Arranque con menú (deprecado) |
| `LAUNCHER_MENU.bat` | Menú launcher |
| `abrir_dashboard.bat` | Abre el dashboard |
| `test_dashboard.bat` | Test del dashboard |
| `estado_sistema.bat` | Ver estado del sistema |
| `limpiar_sistema.bat` | Limpieza de puertos y procesos |
| `VERIFICAR_INSTALACION.bat` | Verificar instalación |
| `activar_autostart.bat` | Activar auto-inicio |
| `desactivar_autostart.bat` | Desactivar auto-inicio |

---

## 🌐 Archivos Web (HTML)

| Archivo | Función |
|---|---|
| `dashboard_standalone.html` | Dashboard principal auto-contenido |
| `agentes.html` | Página de visualización de agentes |
| `templates/index.html` | Template principal de la web |

---

## 🧪 Tests

| Archivo | Función |
|---|---|
| `tests/__init__.py` | Inicializador del módulo de tests |
| `tests/test_api.py` | Tests de la API |
| `tests/test_core.py` | Tests del core |
| `tests/test_escalation.py` | Tests de escalación |
| `tests/test_router.py` | Tests del router |
| `test_agentes_list.py` | Test de listado de agentes (raíz) |
| `test_crear_expansion.py` | Test de creación de expansión (raíz) |
| `test_evolucion.py` | Test de evolución (raíz) |
| `test_script.py` | Test script general (raíz) |

---

## 📂 Subdirectorios Especiales

### `agents/` — Agentes adicionales (2 archivos)
| Archivo | Función |
|---|---|
| `analista_flujos.py` | Analista de flujos |
| `invstigador de IAs nuevas.py` | Investigador de nuevas IAs |

### `kb/` — Base de Conocimiento (27 archivos)
Investigaciones y documentos de referencia para el sistema RAG.

| Archivo | Contenido |
|---|---|
| `arquitecturas_avanzadas_de_agentes_de_ia_autonomos_2026.txt` | Arquitecturas de agentes IA |
| `modelos_de_negocio_para_agencias_de_agentes_de_ia_2026.txt` | Modelos de negocio IA |
| `precios.txt` | Información de precios |
| `investigacion_*.txt` (11 archivos) | Investigaciones indexadas |
| `research_*.txt` (12 archivos) | Resultados de investigación |

### `proyectos/way2theunknown/` — Proyecto de agencia de viajes
| Archivo | Función |
|---|---|
| `README.md` | Documentación del proyecto |
| `TAREA_GENERAR_SITIO_WEB.txt` | Tarea de generación del sitio |
| `orquestador.py` | Orquestador del proyecto |
| `agentes/buscador_plusvalia.py` | Buscador de plusvalía |
| `agentes/calculadora_fee_viaje.py` | Calculadora fee viaje |
| `agentes/cotizador_viaje.py` | Cotizador de viaje |
| `agentes/generador_itinerario_viaje.py` | Generador itinerario |
| `agentes/web_builder.py` | Constructor web |
| `sitio_web/index.html` | Página principal |
| `sitio_web/destinos.html` | Página de destinos |
| `sitio_web/servicios.html` | Página de servicios |
| `sitio_web/js/funciones.js` | JavaScript del sitio |

### `projects/mi_empresa/` — Proyecto empresarial
| Archivo | Función |
|---|---|
| `default/config.json` | Configuración del proyecto |
| `default/runs/state.json` | Estado de ejecución |

### `runs/` — Historial de ejecuciones
| Archivo | Contenido |
|---|---|
| `session.json` | Sesión actual |
| `state.json` | Estado actual |
| `20260205-003447_Ideas_de_automatización.md` | Ideas de automatización |
| `20260205-003649_equipo_agentes.md` | Equipo de agentes |
| `20260205-010158_tarea_router.md` | Tarea del router |
| `20260205-144426_nota.md` | Nota general |

### `reportes/` — Reportes generados
| Archivo | Contenido |
|---|---|
| `due_diligence_20260226_222030.json` | Due diligence generado |

### `proyectos_queue/` — Cola de proyectos
| Archivo | Contenido |
|---|---|
| `procesados/agencia_de_viajes_llamada_way2theunknow.txt` | Tarea procesada |

### `.vault/` — Credenciales encriptadas
| Archivo | Función |
|---|---|
| `.vault_key` | Clave de vault |
| `credenciales.enc` | Credenciales encriptadas |

### `.fabricamode` — Modo de fábrica actual
Valor actual: `MEJORAR`

---

## 📈 Estadísticas Consolidadas

```
📁 Archivos totales (sin .git):     ~1,138
🐍 Agentes Python (raíz):              510
📊 Categorías de agentes:               19
📄 Archivos JSON:                        12
📝 Documentación MD:                      8
📋 Guías/Notas TXT:                      18
🖥️ Scripts BAT:                          11
🌐 HTML:                                  3
🧪 Tests:                                 8
📚 Base de conocimiento (kb/):           27
🗂️ Proyecto way2theunknown:             12
📂 Projects/mi_empresa:                   2
📜 Runs (historial):                      6
📦 Reportes:                              1
```

---

## 🔄 Flujo del Sistema

```
Usuario
  │
  ▼
arrancar_simple.bat  →  api_agencia.py (puerto 8000)
                              │
                    ┌─────────┼──────────┐
                    ▼         ▼          ▼
              /dashboard  /status    /tarea
                    │         │          │
                    ▼         ▼          ▼
            dashboard_     estado_    agent_router.py
            standalone     maestro       │
            .html          .json    ┌────┼────┐
                                    ▼    ▼    ▼
                                 510 agentes en
                                 19 categorías
                                    │
                                    ▼
                              memory_manager.py
                              rag_pro.py
                              habilidades.json
```

---

**Generado**: 2026-03-03
**Sistema**: Agencia Santi v2.0
**Agentes totales**: 510+
