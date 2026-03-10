# Dashboard V2 – Setup & Usage Guide

## Windows Setup (No Docker)

### Prerequisites
- Python 3.10+
- Node.js 18+ (for frontend)
- Git

### 1. Clone & Install Backend

```powershell
git clone https://github.com/SantiM-wronghacker/agencia-IA.git
cd agencia-IA

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
pip install -e .
```

### 2. (Optional) Streamlit Dashboard

```powershell
pip install -r requirements-dashboard.txt
streamlit run src/agencia/agents/herramientas/app.py
```

### 3. Start the FastAPI Backend

```powershell
uvicorn src.agencia.api.dashboard.routes:app --host 0.0.0.0 --port 8001 --reload
```

The API is now at `http://localhost:8001`.
Health check: `http://localhost:8001/api/v2/dashboard/health`

### 4. Start the React Frontend

```powershell
cd frontend
npm install
npm start
```

The frontend opens at `http://localhost:3000`.

### 5. Enable TeamDirector (Optional)

```powershell
set USE_TEAM_DIRECTOR=true
uvicorn src.agencia.api.dashboard.routes:app --host 0.0.0.0 --port 8001 --reload
```

Then call:
```
POST http://localhost:8001/api/v2/agents/run
{"goal": "Launch MVP", "roles": ["strategy", "tech"]}
```

Or via CLI:
```powershell
python -m src.agencia.agents.builder.run --goal "Launch MVP" --roles strategy,tech
```

---

## Running Tests

### Backend (pytest)

```powershell
pytest -q
```

Specific test files:
```powershell
pytest tests/integration/test_dashboard_api.py -v     # API endpoints + WS
pytest tests/integration/test_repository.py -v         # SQLite persistence
pytest tests/integration/test_team_director.py -v      # RoleAgent/TeamDirector
pytest tests/integration/test_smoke.py -v              # Full lifecycle smoke test
```

### Frontend (Jest)

```powershell
cd frontend
npm test -- --watchAll=false
```

---

## SQLite Persistence

Tasks are persisted in SQLite. Configure the path:

```powershell
set DASHBOARD_DB_PATH=C:\Users\you\data\dashboard.db
```

Default: `./data/dashboard.db` (directory auto-created).

Tasks survive application restarts.

---

## WebSocket Event Contract

All WS messages follow the **EventEnvelope** format:

```json
{
  "event": "task_created",
  "ts": "2025-01-01T00:00:00+00:00",
  "payload": { "id": "...", "name": "...", "status": "pending", ... }
}
```

Events emitted:
| Event | Trigger |
|-------|---------|
| `task_created` | POST `/tasks` |
| `task_updated` | PATCH `/tasks/{id}` |
| `task_cancelled` | POST `/tasks/{id}/cancel` |
| `echo` | Client sends a message to the WS |

The React frontend accepts both `event` (new) and `type` (legacy) fields for backward compatibility.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v2/dashboard/health` | Health status |
| GET | `/api/v2/dashboard/metrics` | Aggregated metrics |
| POST | `/api/v2/dashboard/tasks` | Create task |
| GET | `/api/v2/dashboard/tasks` | List tasks (filter: `?status=`, `?search=`) |
| GET | `/api/v2/dashboard/tasks/{id}` | Get task |
| PATCH | `/api/v2/dashboard/tasks/{id}` | Update task fields |
| POST | `/api/v2/dashboard/tasks/{id}/cancel` | Cancel task |
| GET | `/api/v2/dashboard/tasks/{id}/logs` | Task logs |
| WS | `/api/v2/dashboard/ws` | Real-time updates |
| POST | `/api/v2/agents/run` | Run TeamDirector (requires `USE_TEAM_DIRECTOR=true`) |

---

## Files Changed

### Backend
- `src/agencia/api/dashboard/routes.py` – SQLite persistence, PATCH endpoint, unified WS envelope
- `src/agencia/api/dashboard/repository.py` – **NEW** SQLite TaskRepository
- `src/agencia/api/dashboard/websocket.py` – unchanged
- `src/agencia/api/dashboard/models.py` – unchanged
- `src/agencia/api/agents_endpoint.py` – **NEW** TeamDirector FastAPI endpoint
- `src/agencia/agents/builder/` – **NEW** package: RoleAgent, TeamDirector, CLI

### Frontend
- `frontend/src/components/RealtimeUpdates.tsx` – Fixed to read `event` field (was `type`)

### Tests
- `tests/integration/test_dashboard_api.py` – Updated for SQLite, added PATCH + WS event tests
- `tests/integration/test_repository.py` – **NEW** SQLite CRUD + persistence tests
- `tests/integration/test_team_director.py` – **NEW** RoleAgent/TeamDirector security tests
- `tests/integration/test_smoke.py` – **NEW** Full lifecycle smoke test
- `frontend/__tests__/RealtimeUpdates.test.tsx` – **NEW** RTL test for event rendering

### Config
- `requirements.txt` – Removed `streamlit` (moved to optional)
- `requirements-dashboard.txt` – **NEW** Optional Streamlit deps
- `pyproject.toml` – Added `[dashboard]` extras
