# Reporte de Cambios — Últimas 24-48 horas (3-4 Marzo 2026)

> **Branch:** `main`
> **Último commit:** [`e2f3c0a`](https://github.com/SantiM-wronghacker/agencia-IA/commit/e2f3c0a675917c2c24709fb26401456eebae7637) — *Update to match main branch* (4 Mar 2026 00:42 CST)
> **PRs mergeados:** [#5](https://github.com/SantiM-wronghacker/agencia-IA/pull/5), [#6](https://github.com/SantiM-wronghacker/agencia-IA/pull/6), [#7](https://github.com/SantiM-wronghacker/agencia-IA/pull/7)

---

## Summary

Se realizaron **3 grandes bloques de trabajo** en las últimas 24-48 horas, todos ya mergeados en `main`:

1. **Dashboard API v2 (Backend FastAPI)** — Nuevo backend con endpoints CRUD de tareas, métricas, health check y WebSocket en tiempo real.
2. **Frontend React 18 + TypeScript + Tailwind CSS** — SPA completa con páginas Dashboard, Tasks, Monitoring, Settings, dark mode, y Panic Button.
3. **Monitoreo y observabilidad** — Prometheus metrics, structured JSON logging, Jaeger tracing, health checks (liveness/readiness), Grafana dashboards.

Adicionalmente se migró la estructura de archivos a `src/agencia/agents/` y se añadió infraestructura Docker + Nginx.

---

## File Changes

### Backend — Dashboard API v2

| Archivo | Estado | Qué cambió |
|---------|--------|-------------|
| `src/agencia/api/dashboard/__init__.py` | ✅ Nuevo | Exporta `app`, `ConnectionManager`, modelos, auth. |
| `src/agencia/api/dashboard/routes.py` | ✅ Nuevo | App FastAPI v2.0.0 con 8 endpoints REST + 1 WebSocket. CORS configurable vía `DASHBOARD_CORS_ORIGINS`. Store de tareas en memoria. |
| `src/agencia/api/dashboard/models.py` | ✅ Nuevo | Modelos Pydantic: `TaskStatus` (5 estados), `UserRole`, `TaskCreate`, `TaskSchema`, `DashboardMetrics`, `HealthResponse`, `TokenData`. |
| `src/agencia/api/dashboard/websocket.py` | ✅ Nuevo | `ConnectionManager` — gestiona conexiones WS, broadcast, envío personal, desconexión automática en error. |
| `src/agencia/api/dashboard/auth.py` | ✅ Nuevo | Autenticación JWT (HS256, 24h expiry) con `python-jose` y fallback a `base64`. `HTTPBearer` security scheme. |

### Backend — Monitoreo y observabilidad

| Archivo | Estado | Qué cambió |
|---------|--------|-------------|
| `src/agencia/api/health.py` | ✅ Nuevo | Endpoints `/live`, `/ready`, `/detailed` para health checks con verificación de servicios (DB, Redis, Elasticsearch, LLM). |
| `src/agencia/api/middleware.py` | ✅ Nuevo | Middleware Starlette: logging de requests, recolección de métricas Prometheus, integración con tracing distribuido. |
| `src/agencia/monitoring/__init__.py` | ✅ Nuevo | Exporta decoradores y métricas. |
| `src/agencia/monitoring/metrics.py` | ✅ Nuevo | Métricas Prometheus: contadores de requests, histogramas de latencia (buckets acumulativos), gauges de agentes activos. |
| `src/agencia/monitoring/decorators.py` | ✅ Nuevo | Decoradores `@track_time`, `@count_calls` para instrumentar funciones automáticamente. |
| `src/agencia/health/__init__.py` | ✅ Nuevo | Exporta `LivenessProbe`, `ReadinessProbe`. |
| `src/agencia/health/checks.py` | ✅ Nuevo | Verificaciones: base de datos, Redis, Elasticsearch, proveedores LLM, espacio en disco, memoria, cola de mensajes. Sanitiza argumentos de filtro. |
| `src/agencia/health/liveness.py` | ✅ Nuevo | `LivenessProbe` — verifica que el proceso esté vivo y respondiendo. |
| `src/agencia/health/readiness.py` | ✅ Nuevo | `ReadinessProbe` — verifica que todas las dependencias estén listas. |
| `src/agencia/logging/__init__.py` | ✅ Nuevo | Exporta `JSONLogger`, filtros. |
| `src/agencia/logging/json_logger.py` | ✅ Nuevo | Logger JSON estructurado para integración con ELK stack. |
| `src/agencia/logging/filters.py` | ✅ Nuevo | Filtros de logging con sanitización de argumentos para seguridad. |
| `src/agencia/tracing/__init__.py` | ✅ Nuevo | Exporta configuración Jaeger y decoradores. |
| `src/agencia/tracing/jaeger_config.py` | ✅ Nuevo | Configuración de Jaeger para tracing distribuido (OpenTelemetry). |
| `src/agencia/tracing/decorators.py` | ✅ Nuevo | Decoradores `@trace` para instrumentación automática de spans. |

### Frontend — React 18 + TypeScript + Tailwind CSS

| Archivo | Estado | Qué cambió |
|---------|--------|-------------|
| `frontend/package.json` | ✅ Nuevo | React 18.2, TypeScript 4.9, Tailwind 3.3.6, Axios 1.13.5, React Query 5.12, react-router-dom 6.20. |
| `frontend/package-lock.json` | ✅ Nuevo | Lock file (~17,522 líneas). |
| `frontend/tsconfig.json` | ✅ Nuevo | Target ES2017, strict mode, JSX react-jsx. |
| `frontend/tailwind.config.js` | ✅ Nuevo | Dark mode con `class`, content paths configurados. |
| `frontend/postcss.config.js` | ✅ Nuevo | PostCSS con Tailwind y Autoprefixer. |
| `frontend/public/index.html` | ✅ Nuevo | HTML base con meta tags. |
| `frontend/.env.example` | ✅ Nuevo | Variables de entorno de ejemplo (`REACT_APP_API_URL`, `REACT_APP_WS_URL`). |
| `frontend/src/App.tsx` | ✅ Nuevo | Router principal con rutas: `/`, `/tasks`, `/monitoring`, `/settings`. React Query provider. |
| `frontend/src/index.tsx` | ✅ Nuevo | Entry point React 18 con `createRoot`. |
| `frontend/src/styles/globals.css` | ✅ Nuevo | Tailwind `@tailwind base/components/utilities`. |
| **Páginas** | | |
| `frontend/src/pages/Dashboard.tsx` | ✅ Nuevo | Vista principal: `MetricsPanel`, `RealtimeUpdates`, `HealthStatus`, `PanicButton`. |
| `frontend/src/pages/Tasks.tsx` | ✅ Nuevo | CRUD de tareas con formulario de creación, filtros de estado, búsqueda. |
| `frontend/src/pages/Monitoring.tsx` | ✅ Nuevo | Health status + métricas en tiempo real. |
| `frontend/src/pages/Settings.tsx` | ✅ Nuevo | Configuración de API URL, WS URL, dark mode toggle, notificaciones. |
| **Componentes** | | |
| `frontend/src/components/Navbar.tsx` | ✅ Nuevo | Barra de navegación responsive con menú hamburguesa para móvil. |
| `frontend/src/components/TaskCard.tsx` | ✅ Nuevo | Tarjeta individual de tarea con badge de estado, botón cancelar. |
| `frontend/src/components/TaskList.tsx` | ✅ Nuevo | Lista de tareas con filtro y búsqueda integrados. |
| `frontend/src/components/MetricsPanel.tsx` | ✅ Nuevo | Panel de métricas: total, completadas, fallidas, pendientes, running, success_rate (0-100). |
| `frontend/src/components/HealthStatus.tsx` | ✅ Nuevo | Indicador visual de salud del API (status, uptime, servicios). |
| `frontend/src/components/RealtimeUpdates.tsx` | ✅ Nuevo | Muestra eventos WS en tiempo real (task_created, task_cancelled, etc.). |
| `frontend/src/components/PanicButton.tsx` | ✅ Nuevo | Botón de emergencia para cancelar todas las tareas activas. |
| **Hooks** | | |
| `frontend/src/hooks/useTasks.ts` | ✅ Nuevo | React Query hooks: `useTasksQuery`, `useCreateTask`, `useCancelTask`. |
| `frontend/src/hooks/useMetrics.ts` | ✅ Nuevo | React Query hook para métricas (auto-refresh cada 10s). |
| `frontend/src/hooks/useWebSocket.ts` | ✅ Nuevo | Hook para conexión WS con auto-reconnect exponencial. |
| `frontend/src/hooks/useAuth.ts` | ✅ Nuevo | Hook de autenticación (mock/placeholder para JWT). |
| **Services** | | |
| `frontend/src/services/api.ts` | ✅ Nuevo | Axios instance con base URL configurable e interceptors. |
| `frontend/src/services/dashboardApi.ts` | ✅ Nuevo | Funciones API: `getTasks`, `createTask`, `cancelTask`, `getMetrics`, `getHealth`. |
| `frontend/src/services/websocketService.ts` | ✅ Nuevo | Singleton `WebSocketService` con auto-reconnect exponencial (1s→30s), handlers de mensaje/conexión/desconexión. |
| **Types** | | |
| `frontend/src/types/task.ts` | ✅ Nuevo | Interfaces `Task`, `TaskCreate`, `TaskStatus` enum. |
| `frontend/src/types/metrics.ts` | ✅ Nuevo | Interfaces `DashboardMetrics`, `HealthResponse`. |
| `frontend/src/types/auth.ts` | ✅ Nuevo | Interfaces `AuthUser`, `LoginCredentials`. |

### Infraestructura

| Archivo | Estado | Qué cambió |
|---------|--------|-------------|
| `docker-compose.yml` | ✅ Nuevo | Services: `agencia-api`, `dashboard-api` (:8001), `frontend` (:3000), `elasticsearch`, `redis`, `postgres`, `rabbitmq`, `jaeger`, `prometheus`, `grafana`. |
| `frontend/Dockerfile` | ✅ Nuevo | Multi-stage build: Node 18 → Nginx con config inline para puerto 3000. |
| `nginx/dashboard.conf` | ✅ Nuevo | Reverse proxy: `/dashboard/` → React (:3000), `/api/v2/dashboard/` → FastAPI (:8001), soporte WebSocket (`Upgrade`, `Connection`). |

### Documentación

| Archivo | Estado | Qué cambió |
|---------|--------|-------------|
| `docs/DASHBOARD_V2.md` | ✅ Nuevo | Arquitectura, endpoints, modelos, WebSocket, configuración. |
| `docs/FRONTEND_SETUP.md` | ✅ Nuevo | Guía de desarrollo del frontend (instalación, scripts, estructura). |
| `docs/HEALTH_CHECKS.md` | ✅ Nuevo | Documentación de health checks (liveness, readiness, detailed). |
| `docs/LOGGING_SETUP.md` | ✅ Nuevo | Guía de logging JSON estructurado y configuración ELK. |
| `docs/MONITORING_SETUP.md` | ✅ Nuevo | Setup de Prometheus + Grafana con dashboards incluidos. |
| `docs/TRACING_SETUP.md` | ✅ Nuevo | Configuración de Jaeger para tracing distribuido. |
| `MIGRATION_REPORT.md` | ✅ Nuevo | Reporte de migración de archivos a `src/agencia/agents/`. |
| `MIGRATION_DASHBOARD.md` | ✅ Nuevo | Guía de migración paralela del dashboard legacy al v2. |

### Tests

| Archivo | Estado | Qué cambió |
|---------|--------|-------------|
| `tests/integration/test_dashboard_api.py` | ✅ Nuevo | 12 tests de integración: health, create, list, get, cancel, logs, metrics, filter, search, WebSocket. |
| `tests/integration/test_health_checks.py` | ✅ Nuevo | Tests de health checks (liveness, readiness). |
| `tests/integration/test_logging.py` | ✅ Nuevo | Tests de logging JSON estructurado y filtros. |
| `tests/integration/test_metrics.py` | ✅ Nuevo | Tests de métricas Prometheus. |
| `frontend/__tests__/Dashboard.test.tsx` | ✅ Nuevo | Test de renderizado del componente Dashboard. |
| `frontend/__tests__/TaskCard.test.tsx` | ✅ Nuevo | Tests del componente TaskCard (render, cancel button). |
| `frontend/__tests__/useWebSocket.test.ts` | ✅ Nuevo | Test del hook useWebSocket. |
| `conftest.py` | ✅ Nuevo | Configuración de pytest a nivel raíz con `sys.path` fix. |

### Migración de estructura

| Archivo | Estado | Qué cambió |
|---------|--------|-------------|
| `scripts/migrate_to_src.py` | ✅ Nuevo | Script de migración automática de archivos a `src/agencia/agents/`. |
| `scripts/verify_migration.py` | ✅ Nuevo | Script de verificación post-migración (imports, estructura). |
| `pyproject.toml` | ✅ Nuevo | Configuración de paquete Python con `src/` layout. |
| `src/agencia/agents/` | ✅ Nuevo | ~510 archivos Python migrados/renombrados organizados por categoría. |
| `config.py` | ❌ Eliminado | Movido a `categorias/HERRAMIENTAS/config.py`. |

### Grafana / Prometheus / Alertas

| Archivo | Estado | Qué cambió |
|---------|--------|-------------|
| `monitoring/prometheus/prometheus.yml` | ✅ Nuevo | Configuración de scraping para agencia-api y dashboard-api. |
| `monitoring/alerts/alert_rules.yml` | ✅ Nuevo | Reglas de alerta: alta tasa de error, latencia elevada, agentes caídos. |
| `monitoring/grafana/dashboards/system_overview.json` | ✅ Nuevo | Dashboard Grafana: overview general del sistema. |
| `monitoring/grafana/dashboards/agent_performance.json` | ✅ Nuevo | Dashboard Grafana: rendimiento por agente. |
| `monitoring/grafana/dashboards/infrastructure.json` | ✅ Nuevo | Dashboard Grafana: métricas de infraestructura. |
| `monitoring/grafana/dashboards/llm_providers.json` | ✅ Nuevo | Dashboard Grafana: métricas de proveedores LLM. |

### Otros archivos modificados

| Archivo | Estado | Qué cambió |
|---------|--------|-------------|
| `.gitignore` | 📝 Modificado | Se añadieron entradas para `node_modules/`, `__pycache__/`, `.env`, `build/`, `dist/`. |
| `requirements.txt` | 📝 Modificado | Se añadieron `prometheus-client`, `opentelemetry-api` como dependencias. |
| `estado_maestro.json` | 📝 Modificado | Actualización de estado del sistema (timestamps, contadores). |

---

## API Changes

### Endpoints nuevos (Dashboard API v2)

Base URL: `http://localhost:8001`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v2/dashboard/health` | Estado de salud del servicio (status, version, uptime, servicios). |
| `GET` | `/api/v2/dashboard/metrics` | Métricas agregadas (total_tasks, completed, failed, pending, running, success_rate). |
| `POST` | `/api/v2/dashboard/tasks` | Crear tarea (body: `{name, description?}`). Retorna 201 + broadcast WS. |
| `GET` | `/api/v2/dashboard/tasks` | Listar tareas. Query params: `?status=pending&search=texto`. |
| `GET` | `/api/v2/dashboard/tasks/{id}` | Obtener tarea por ID. |
| `POST` | `/api/v2/dashboard/tasks/{id}/cancel` | Cancelar tarea (solo si PENDING/RUNNING). Broadcast WS. |
| `GET` | `/api/v2/dashboard/tasks/{id}/logs` | Obtener logs de una tarea. |
| `WS` | `/api/v2/dashboard/ws` | WebSocket para actualizaciones en tiempo real. |

### Endpoints de health/observabilidad

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/health/live` | Liveness probe (Kubernetes-compatible). |
| `GET` | `/health/ready` | Readiness probe (verifica dependencias). |
| `GET` | `/health/detailed` | Estado detallado de todos los servicios. |

### WebSocket protocol

```
Conexión: ws://localhost:8001/api/v2/dashboard/ws

Eventos enviados por el servidor:
  {"event": "task_created", "task": {...}}
  {"event": "task_cancelled", "task": {...}}

Echo (al enviar texto):
  {"event": "echo", "data": "tu texto"}
```

---

## Frontend Changes

### Arquitectura

```
React 18.2 + TypeScript 4.9 + Tailwind CSS 3.3.6
├── React Router v6 (4 rutas: /, /tasks, /monitoring, /settings)
├── React Query v5 (caché, auto-refresh, mutations)
├── Axios (HTTP client con interceptors)
└── WebSocket singleton (auto-reconnect exponencial 1s→30s, max 10 intentos)
```

### Funcionalidades

- **Dashboard principal** — Métricas en tiempo real, estado de salud, eventos WebSocket, panic button.
- **Gestión de tareas** — Crear, listar, filtrar por estado, buscar por texto, cancelar.
- **Monitoreo** — Health status visual, métricas auto-refresh.
- **Settings** — Configuración de URLs, dark mode toggle, preferencias de notificación.
- **Dark mode** — Toggle con clase CSS en `<html>`, persistido.
- **Responsive** — Menú hamburguesa en móvil.
- **Panic Button** — Cancela todas las tareas PENDING/RUNNING de un click.

### Cambios clave en el frontend

```diff
// MetricsPanel.tsx — fix success_rate display
- <span>{(metrics.success_rate * 100).toFixed(1)}%</span>
+ <span>{metrics.success_rate.toFixed(1)}%</span>
// Backend ya retorna 0-100, no era necesario multiplicar por 100.

// websocketService.ts — constantes con nombre
+ const INITIAL_DELAY_MS = 1000;
+ const MAX_DELAY_MS = 30_000;
- const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
+ const delay = Math.min(INITIAL_DELAY_MS * Math.pow(2, this.reconnectAttempts), MAX_DELAY_MS);

// tsconfig.json
- "target": "es5"
+ "target": "es2017"

// Dockerfile — fix nginx config
- COPY ../nginx/default.conf /etc/nginx/conf.d/default.conf
+ RUN echo 'server { listen 3000; ... }' > /etc/nginx/conf.d/default.conf
```

---

## How to Run (Windows, sin Docker)

### Prerrequisitos

```bash
# Python 3.10+
python --version     # Python 3.10.x o superior

# Node.js 18+
node --version       # v18.x o superior
npm --version        # 9.x o superior

# Git
git --version
```

### 1. Clonar y preparar

```bash
git clone https://github.com/SantiM-wronghacker/agencia-IA.git
cd agencia-IA
```

### 2. Levantar API Dashboard (:8001)

```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Levantar el API en puerto 8001
uvicorn src.agencia.api.dashboard.routes:app --host 0.0.0.0 --port 8001 --reload
```

**Resultado esperado:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
```

**Validar:**
```bash
curl http://localhost:8001/api/v2/dashboard/health
# {"status":"ok","version":"2.0.0","uptime":...,"services":{"api":"running","websocket":"0 conexiones"}}
```

### 3. Levantar Frontend (:3000)

```bash
# En otra terminal
cd frontend

# Instalar dependencias
npm install

# Configurar variables (opcional, ya tiene defaults)
copy .env.example .env
# Editar .env si es necesario:
# REACT_APP_API_URL=http://localhost:8001
# REACT_APP_WS_URL=ws://localhost:8001/api/v2/dashboard/ws

# Levantar
npm start
```

**Resultado esperado:**
```
Compiled successfully!
You can now view agencia-ia-dashboard in the browser.
  Local:            http://localhost:3000
```

### 4. Validar WebSocket

**Opción A — Desde el navegador:**
```javascript
// Abrir DevTools → Console en http://localhost:3000
const ws = new WebSocket('ws://localhost:8001/api/v2/dashboard/ws');
ws.onopen = () => { console.log('Conectado'); ws.send('ping'); };
ws.onmessage = (e) => console.log('Recibido:', e.data);
// Esperado: Recibido: {"event": "echo", "data": "ping"}
```

**Opción B — Con Python:**
```python
# pip install websockets
import asyncio, websockets, json

async def test_ws():
    async with websockets.connect("ws://localhost:8001/api/v2/dashboard/ws") as ws:
        await ws.send("test")
        response = json.loads(await ws.recv())
        print(f"Evento: {response['event']}, Data: {response['data']}")
        assert response["event"] == "echo"
        print("✅ WebSocket OK")

asyncio.run(test_ws())
```

**Opción C — Con PowerShell:**
```powershell
# Requiere Invoke-WebRequest
Invoke-RestMethod -Uri http://localhost:8001/api/v2/dashboard/health
# Debería retornar el JSON de health
```

### 5. Validar CRUD de Tasks

```bash
# Crear tarea
curl -X POST http://localhost:8001/api/v2/dashboard/tasks -H "Content-Type: application/json" -d "{\"name\": \"Test Task\", \"description\": \"Prueba\"}"
# Esperado: 201 Created, {"id":"uuid...","name":"Test Task","status":"pending",...}

# Listar tareas
curl http://localhost:8001/api/v2/dashboard/tasks
# Esperado: 200, [{"id":"uuid...","name":"Test Task",...}]

# Obtener tarea por ID (reemplazar UUID)
curl http://localhost:8001/api/v2/dashboard/tasks/{task_id}
# Esperado: 200, {"id":"uuid...",...}

# Cancelar tarea
curl -X POST http://localhost:8001/api/v2/dashboard/tasks/{task_id}/cancel
# Esperado: 200, {"status":"cancelled",...}

# Listar tareas filtradas
curl "http://localhost:8001/api/v2/dashboard/tasks?status=cancelled"
# Esperado: 200, tareas con status cancelled

# Buscar tareas
curl "http://localhost:8001/api/v2/dashboard/tasks?search=test"
# Esperado: 200, tareas que contengan "test" en name o description

# Métricas
curl http://localhost:8001/api/v2/dashboard/metrics
# Esperado: 200, {"total_tasks":1,"completed":0,"failed":0,"pending":0,"running":0,"success_rate":0.0,...}
```

### 6. Correr tests

```bash
# Backend tests (desde raíz del proyecto)
venv\Scripts\activate
pip install pytest httpx
pytest tests/integration/test_dashboard_api.py -v
# Esperado: 12 passed

# Frontend tests (desde frontend/)
cd frontend
npm test -- --watchAll=false
# Esperado: Tests pass
```

---

## Test Plan

| # | Prueba | Comando | Resultado esperado |
|---|--------|---------|-------------------|
| 1 | API Health | `curl http://localhost:8001/api/v2/dashboard/health` | `{"status":"ok","version":"2.0.0",...}` |
| 2 | Crear tarea | `curl -X POST .../tasks -d '{"name":"T1"}'` | 201, JSON con id y status "pending" |
| 3 | Listar tareas | `curl .../tasks` | 200, array con la tarea creada |
| 4 | Obtener tarea | `curl .../tasks/{id}` | 200, JSON de la tarea |
| 5 | Cancelar tarea | `curl -X POST .../tasks/{id}/cancel` | 200, status "cancelled" |
| 6 | Cancelar completada | Marcar como COMPLETED, luego cancel | 400, error |
| 7 | Filtrar por status | `curl .../tasks?status=cancelled` | Solo tareas cancelled |
| 8 | Buscar | `curl .../tasks?search=test` | Solo tareas que matchean |
| 9 | Logs | `curl .../tasks/{id}/logs` | 200, array vacío (sin logs aún) |
| 10 | Métricas | `curl .../metrics` | JSON con contadores correctos |
| 11 | WebSocket echo | Conectar + enviar "hello" | `{"event":"echo","data":"hello"}` |
| 12 | WS broadcast | Crear tarea mientras WS conectado | Recibir `{"event":"task_created",...}` |
| 13 | Frontend render | Abrir `http://localhost:3000` | Dashboard carga, navbar visible |
| 14 | Frontend crear | Click "New Task", llenar form | Tarea aparece en lista |
| 15 | Frontend cancel | Click "Cancel" en tarea | Status cambia a cancelled |
| 16 | Dark mode | Toggle en Settings | Tema oscuro aplica |
| 17 | Integration tests | `pytest tests/integration/test_dashboard_api.py -v` | 12 tests passed |

---

## Known Issues / Next Steps

### Limitaciones conocidas

1. **Store en memoria** — Las tareas se almacenan en un `dict` en memoria. Al reiniciar el API, se pierden todos los datos. No hay persistencia en base de datos todavía.
2. **Auth no integrada en endpoints** — El módulo `auth.py` existe con JWT, pero los endpoints de `routes.py` no lo usan como dependency (no hay `Depends(get_current_user)`). Cualquiera puede crear/cancelar tareas.
3. **No hay endpoint PATCH/PUT** — No se puede actualizar el estado de una tarea manualmente (ej. marcar como COMPLETED). Solo se puede cancelar.
4. **WebSocket sin autenticación** — El endpoint WS acepta conexiones sin verificar token.
5. **Frontend tests mínimos** — Solo 3 tests de frontend (Dashboard render, TaskCard, useWebSocket). Faltan tests para Tasks page, forms, etc.
6. **No hay CI/CD pipeline** — No hay GitHub Actions configurado para lint/test automáticos.
7. **Dependencias de observabilidad opcionales** — Prometheus, Jaeger, ELK requieren Docker. Sin Docker, solo la API y frontend funcionan.
8. **CORS configurado como `*` por defecto** — En producción se debe restringir vía `DASHBOARD_CORS_ORIGINS`.
9. **`package-lock.json` no auditado** — No se ha corrido `npm audit` para verificar vulnerabilidades en dependencias frontend.
10. **Migración de agentes parcial** — Los archivos se copiaron/renombraron a `src/agencia/agents/` pero los imports en archivos legacy (raíz) no se actualizaron universalmente.

### Próximos pasos sugeridos

- [ ] Añadir persistencia SQLite/PostgreSQL al task store
- [ ] Integrar `auth.py` como middleware en todos los endpoints
- [ ] Agregar endpoint `PATCH /tasks/{id}` para actualizar status
- [ ] Configurar GitHub Actions CI (lint + tests)
- [ ] Correr `npm audit fix` en frontend
- [ ] Añadir más tests de frontend (cobertura mínima 80%)
- [ ] Documentar variables de entorno requeridas

---

## New Dependencies

### Python (requirements.txt)

| Paquete | Versión | Por qué |
|---------|---------|---------|
| `fastapi` | ≥0.115.0 | Framework del Dashboard API v2 |
| `uvicorn` | ≥0.34.0 | Servidor ASGI para FastAPI |
| `pydantic` | ≥2.0 | Validación de modelos de datos |
| `httpx` | ≥0.27.0 | Cliente HTTP async para tests |
| `pytest` | ≥8.0.0 | Framework de testing |
| `starlette` | ≥0.40.0 | Base de FastAPI (middleware) |
| `prometheus-client` | (nuevo) | Métricas Prometheus |
| `opentelemetry-api` | (nuevo) | Tracing distribuido |

### Node.js (frontend/package.json)

| Paquete | Versión | Por qué |
|---------|---------|---------|
| `react` | ^18.2.0 | UI framework |
| `react-dom` | ^18.2.0 | React DOM renderer |
| `react-router-dom` | ^6.20.0 | Client-side routing |
| `react-scripts` | 5.0.1 | Create React App toolchain |
| `typescript` | ^4.9.5 | Type safety |
| `axios` | ^1.13.5 | HTTP client |
| `@tanstack/react-query` | ^5.12.0 | Data fetching/caching |
| `tailwindcss` | ^3.3.6 | Utility-first CSS (devDep) |
| `autoprefixer` | ^10.4.16 | CSS vendor prefixes (devDep) |
| `postcss` | ^8.4.32 | CSS processing (devDep) |
| `@testing-library/react` | ^14.1.2 | Component testing (devDep) |
| `@testing-library/jest-dom` | ^6.1.4 | DOM assertions (devDep) |
| `@testing-library/user-event` | ^14.5.1 | User interaction testing (devDep) |

---

## Links (PR / Commits)

### PRs mergeados en main (últimas 24-48h)

| PR | Título | Estado |
|----|--------|--------|
| [#5](https://github.com/SantiM-wronghacker/agencia-IA/pull/5) | Migrate 510 Python files from root to `src/agencia/agents/` | ✅ Closed/Merged |
| [#6](https://github.com/SantiM-wronghacker/agencia-IA/pull/6) | Add modern FastAPI + React dashboard (parallel with legacy Flask) | ✅ Closed/Merged |
| [#7](https://github.com/SantiM-wronghacker/agencia-IA/pull/7) | Add monitoring, observability, and health checks | ✅ Closed/Merged |

### PRs abiertos (trabajo en progreso)

| PR | Título | Estado |
|----|--------|--------|
| [#8](https://github.com/SantiM-wronghacker/agencia-IA/pull/8) | Add Streamlit dashboard and PATCH endpoint | 🟡 Open |
| [#9](https://github.com/SantiM-wronghacker/agencia-IA/pull/9) | Dashboard: SQLite persistence, WebSocket fixes, export, alerts | 🟡 Open |
| [#10](https://github.com/SantiM-wronghacker/agencia-IA/pull/10) | Agencia Builder — roles-only TeamDirector | 🟡 Open |
| [#11](https://github.com/SantiM-wronghacker/agencia-IA/pull/11) | Generate detailed changelog report (este reporte) | 🟡 Open |

### Commits principales (3-4 Mar 2026)

| SHA | Fecha | Descripción |
|-----|-------|-------------|
| [`ffcf4fd`](https://github.com/SantiM-wronghacker/agencia-IA/commit/ffcf4fd1) | 3 Mar 02:48 | Primer subida de archivos (base completa) |
| [`3cbcb11`](https://github.com/SantiM-wronghacker/agencia-IA/commit/3cbcb112) | 3 Mar 05:14 | Add FastAPI Dashboard API v2 backend |
| [`36bcef9`](https://github.com/SantiM-wronghacker/agencia-IA/commit/36bcef9f) | 3 Mar 05:17 | Complete file migration to `src/agencia/agents/` |
| [`e922b82`](https://github.com/SantiM-wronghacker/agencia-IA/commit/e922b82e) | 3 Mar 05:22 | Add React 18 + TypeScript + Tailwind CSS frontend |
| [`3a60249`](https://github.com/SantiM-wronghacker/agencia-IA/commit/3a60249c) | 3 Mar 05:23 | Fix success_rate display |
| [`6b24073`](https://github.com/SantiM-wronghacker/agencia-IA/commit/6b240732) | 3 Mar 05:28 | Add Docker, Nginx, docs, tests for Dashboard V2 |
| [`50c1572`](https://github.com/SantiM-wronghacker/agencia-IA/commit/50c15724) | 3 Mar 05:29 | Fix WebSocketService import + Dockerfile |
| [`8ea4866`](https://github.com/SantiM-wronghacker/agencia-IA/commit/8ea48665) | 3 Mar 05:31 | Fix integration test (TaskStatus enum) |
| [`f0d4d27`](https://github.com/SantiM-wronghacker/agencia-IA/commit/f0d4d27c) | 3 Mar 05:32 | Code review: tsconfig es2017, WS named constants |
| [`c730ffb`](https://github.com/SantiM-wronghacker/agencia-IA/commit/c730ffb2) | 3 Mar 05:44 | Add monitoring, observability, health checks |
| [`4795970`](https://github.com/SantiM-wronghacker/agencia-IA/commit/47959701) | 3 Mar 05:45 | Fix code review: sanitize filters, histogram buckets |
| [`777a0b0`](https://github.com/SantiM-wronghacker/agencia-IA/commit/777a0b0a) | 3 Mar 16:18 | Save local changes before merging |
| [`b1cbc0b`](https://github.com/SantiM-wronghacker/agencia-IA/commit/b1cbc0b8) | 3 Mar 16:20 | Resolve conflicts: use migrated versions |
| [`76d83d1`](https://github.com/SantiM-wronghacker/agencia-IA/commit/76d83d14) | 3 Mar 16:20 | Merge: dashboard |
| [`0633fd5`](https://github.com/SantiM-wronghacker/agencia-IA/commit/0633fd59) | 3 Mar 16:21 | Resolve conflict: use agent's docker-compose.yml |
| [`e2f3c0a`](https://github.com/SantiM-wronghacker/agencia-IA/commit/e2f3c0a6) | 4 Mar 00:42 | Update to match main branch |

---

## Definition of Done — Checklist

- [x] Dashboard API v2 endpoints funcionando (health, metrics, CRUD tasks, WS)
- [x] Frontend React 18 compila y sirve en `:3000`
- [x] WebSocket funcional con auto-reconnect
- [x] 12 integration tests del backend pasan (`pytest`)
- [x] 3 tests de frontend existen (Dashboard, TaskCard, useWebSocket)
- [x] Docker Compose definido (multi-service)
- [x] Nginx reverse proxy configurado
- [x] Documentación de setup y arquitectura en `docs/`
- [x] Health checks (liveness/readiness) implementados
- [x] Prometheus metrics + Grafana dashboards definidos
- [x] Structured JSON logging configurado
- [x] Jaeger tracing configurado
- [ ] ❌ Persistencia de datos (actualmente en memoria)
- [ ] ❌ Auth integrada en endpoints (JWT módulo existe pero no se usa)
- [ ] ❌ CI/CD pipeline (GitHub Actions)
- [ ] ❌ `npm audit` y revisión de vulnerabilidades frontend
- [ ] ❌ Cobertura de tests frontend > 80%
- [ ] ❌ Endpoint PATCH para actualizar tareas
