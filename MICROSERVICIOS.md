# Microservicios de la Agencia IA

Este documento lista los **microservicios reales** del sistema — procesos independientes que exponen su propia API HTTP, corren en un puerto propio, o funcionan como worker de cola de tareas.

> Los 510 scripts de agentes en `categorias/` son **agentes normales** (scripts invocados por los microservicios). Los microservicios son los procesos del backend que los orquestan y exponen al exterior.

---

## 🚀 Microservicios (servicios ejecutables independientes)

| # | Archivo | Tipo | Puerto | Descripción |
|---|---------|------|--------|-------------|
| 1 | `api_agencia.py` | REST API | **8000** | API principal de la agencia. Expone todos los agentes como endpoints HTTP. Servidor ThreadedHTTPServer. Incluye el dashboard web. |
| 2 | `api.py` | FastAPI | **8000** | Backend FastAPI para el sistema multi-agente. Endpoints `/health`, `/chat`, `/index`. Corre con uvicorn. |
| 3 | `dashboard_web.py` | HTTP Server | **8080** | Dashboard web v2.0 con CRUD completo de agentes, estado del sistema y logs en tiempo real. HTTPServer nativo. |
| 4 | `app_dashboard.py` | Flask App | **5000** | Aplicación web Flask con integración Celery para gestión de tareas asíncronas. Endpoints `/query`, `/submit_task`, `/task_status`, `/panic`. |
| 5 | `app.py` | Streamlit UI | **streamlit** | Interfaz web Streamlit: panel de empresas → proyectos → agentes. Chat interactivo, KB editor, memory viewer. Se inicia con `streamlit run app.py`. |
| 6 | `celery_app.py` | Worker | **Redis** | Worker Celery con Redis como broker y backend. Procesa tareas asíncronas enviadas por `app_dashboard.py`. |
| 7 | `sistema_maestro.py` | Orquestador | interno | Proceso maestro que arranca con Windows. Gestiona en paralelo: fábrica de agentes, modo noche, monitor de salud, limpieza de logs, procesamiento de proyectos. |

---

## 🔧 Módulos de infraestructura compartida

Estos módulos no corren como servidores propios pero son **servicios compartidos** que todos los microservicios importan:

| Módulo | Descripción |
|--------|-------------|
| `llm_router.py` | Motor LLM con rotación automática de proveedores (Groq → Cerebras → Gemini → Mistral → OpenRouter). Cualquier agente lo importa en lugar de llamar a la API directamente. |
| `bus_mensajes.py` | Bus de mensajes central (sistema nervioso). Permite comunicación asíncrona entre agentes vía JSON en disco. |
| `database.py` | Capa de datos SQLite. Gestiona sesiones y mensajes de conversación. |
| `web_bridge.py` | Puente de internet. Módulo importable por cualquier agente para búsqueda web, fetch de URLs, precios, vuelos, hoteles. |
| `memory_manager.py` | Gestión de memoria conversacional. Comprime y actualiza resúmenes de sesión. |
| `rag_index.py` | Indexador de base de conocimiento en ChromaDB. |
| `rag_pro.py` | Agente de búsqueda semántica en la base de conocimiento. |
| `rag_query.py` | Consultor RAG: responde preguntas usando la KB indexada. |
| `gestor_credenciales.py` | Vault de credenciales cifradas (Fernet/AES) por proyecto/cliente. |
| `conector_plataformas.py` | Conector universal de APIs externas (redes sociales, email, hosting, ecommerce). |
| `config.py` | Configuración centralizada del sistema (modelos, rutas, puertos, timeouts). |

---

## 📐 Arquitectura de servicios

```
┌──────────────────────────────────────────────────────────────┐
│                    CLIENTES / FRONTENDS                      │
│                                                              │
│   app.py (Streamlit)    dashboard_web.py (:8080)             │
│   app_dashboard.py (:5000)                                   │
└───────────────────┬──────────────────────────────────────────┘
                    │ HTTP
┌───────────────────▼──────────────────────────────────────────┐
│                    APIS BACKEND                               │
│                                                              │
│   api_agencia.py (:8000)     api.py (:8000, FastAPI)         │
└───────────────────┬──────────────────────────────────────────┘
                    │ import / subprocess
┌───────────────────▼──────────────────────────────────────────┐
│               INFRAESTRUCTURA COMPARTIDA                     │
│                                                              │
│   llm_router.py   bus_mensajes.py   database.py             │
│   web_bridge.py   memory_manager.py  rag_*.py               │
│   gestor_credenciales.py  conector_plataformas.py            │
└───────────────────┬──────────────────────────────────────────┘
                    │ subprocess
┌───────────────────▼──────────────────────────────────────────┐
│            510 AGENTES NORMALES (categorias/)                │
│                                                              │
│  CEREBRO │ FINANZAS │ MARKETING │ VENTAS │ LEGAL │ ...      │
└──────────────────────────────────────────────────────────────┘

Procesos de fondo:
  sistema_maestro.py  →  fábrica + monitor + noche + proyectos
  celery_app.py       →  worker de tareas asíncronas (Redis)
```

---

## Resumen

| Capa | Archivos | Rol |
|------|---------|-----|
| Frontends / Dashboards | `app.py`, `dashboard_web.py`, `app_dashboard.py` | Interfaces de usuario |
| APIs REST principales | `api_agencia.py`, `api.py` | Exposición de endpoints |
| Workers / Orquestadores | `celery_app.py`, `sistema_maestro.py` | Procesos de fondo |
| Infraestructura compartida | `llm_router.py`, `bus_mensajes.py`, `database.py`, `web_bridge.py`, `memory_manager.py`, `rag_*.py`, etc. | Servicios internos |
| Agentes normales | 510 scripts en `categorias/` | Lógica de negocio específica |

---

*Actualizado: 2026-03-03*

