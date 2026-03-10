# 🚀 SUPER AGENTES - AGENCIA SANTI

## Agentes Especializados (CEREBRO)

### 1. **Auto-Evolución** 
- `auto_evolucion.py` - Investiga tecnologías y mejora código automáticamente
- `auto_evolucion_pro.py` - Versión profesional con ciclos de mejora continua
- `test_evolucion.py` - Tests para validar evolución

### 2. **Enrutamiento Inteligente**
- `agent_router.py` - Router principal (64 agentes, 6 rutas)
  - CHAT, SAVE, TASK, FINANZAS, REAL_ESTATE, RAG
- `agent_router_memory.py` - Router con contexto/memoria
- `agent_router_memory_pro.py` - Versión profesional con persistencia
- `agent_router_projects.py` - Router especializado en proyectos
- `agent_router_state_autoscale.py` - Router auto-escalable
- `agent_router_state_pro.py` - Router profesional con estado

### 3. **Coordinación de Agentes**
- `agent_team.py` - Planificación y ejecución de tareas en equipo
- `agent_files.py` - Gestión de archivos y RAG
- `agent_rag.py` - Retrieval-Augmented Generation
- `dispatcher_multiagente.py` - Distribuidor de tareas multi-agente

### 4. **Inteligencia y Memoria**
- `agente_memoria_contextual.py` - Memoria con contexto conversacional
- `memory_manager.py` - Gestor centralizado de memoria
- `llm_router.py` - Router LLM (Groq) con modelos optimizados

### 5. **Validación y QA**
- `supervisor_qa.py` - Supervisor de calidad (auditoría completa)
- `agente_validacion_resultados.py` - Validar outputs
- `agente_fact_checking.py` - Verificar hechos
- `diagnostico_agentes.py` - Diagnosticar agentes

### 6. **Análisis y Reportes**
- `agente_estrategia.py` - Generador de estrategias
- `agente_resumen_ejecutivo.py` - Resúmenes ejecutivos
- `agente_arquitecto_web.py` - Arquitecto de soluciones web
- `monitor_performance_agentes.py` - Monitor de performance
- `resumen_diario_agente.py` - Reportes diarios

### 7. **Utilidades Avanzadas**
- `auto_run.py` - Ejecución automática de agentes
- `integrador_router.py` - Integración de routers
- `fabrica_agentes.py` - Fábrica para generar agentes dinámicamente
- `generador_nota_evolucion.py` - Documentar evolución
- `reclasificar_agentes.py` - Re-clasificar agentes por performance

## Características Clave

✅ **64 Agentes Especializados** en 20 categorías (510 total)
✅ **Enrutamiento Inteligente** - clasifica y distribuye automáticamente
✅ **Auto-Evolución** - mejora código y estrategias automáticamente  
✅ **Memoria Contextual** - mantiene contexto conversacional
✅ **Coordinación Multi-Agente** - ejecutan tareas complejas en equipo
✅ **QA Automático** - supervisor audita toda la agencia
✅ **RAG Integrado** - busqueda semántica de conocimiento

## Acceso Vía API

```bash
# Listar todos los agentes (510)
curl http://localhost:8000/agentes?key=santi-agencia-2026

# Agrupar por áreas
curl http://localhost:8000/areas?key=santi-agencia-2026

# Ejecutar un super agente
curl -X POST http://localhost:8000/ejecutar \
  -H "Authorization: Bearer santi-agencia-2026" \
  -d '{"agente": "agent_router.py", "input": "tu pregunta"}'
```

## Ubicación

```
categorias/CEREBRO/
  ├── auto_evolucion.py
  ├── agent_router.py
  ├── agent_team.py
  ├── agent_rag.py
  ├── llm_router.py
  ├── supervisor_qa.py
  └── [30 más...]
```

---
**Estado**: ✅ Todos detectados por API, 115/115 tests pasando, 510 agentes disponibles
**Próxima Iteración**: Activar super agentes en dashboard interactivo
