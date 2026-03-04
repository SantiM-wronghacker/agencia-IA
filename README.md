# Agencia IA – Dashboard

Multi-agent AI system with a full-featured dashboard for task management, monitoring, and real-time updates.

## Architecture

- **Primary UI**: React (TypeScript) at `http://localhost:3000`
- **Dashboard API**: FastAPI (Python) at `http://localhost:8001`
- **Persistence**: SQLite (`data/tasks.db`) — tasks survive API restarts
- **Real-time**: WebSocket at `ws://localhost:8001/api/v2/dashboard/ws`
- **Polling fallback**: React Query auto-refreshes tasks every 10s, metrics every 5s, health every 10s

> Streamlit (`dashboard_streamlit.py`) is available as an optional lightweight alternative for quick Windows use.

## Windows sin Docker (without Docker) – Setup from scratch

### Prerequisites

- **Python 3.10+** (tested on 3.12 and 3.13)
- **Node.js 18+** with npm
- **Git**

### 1. Clone and set up Python

```bash
git clone https://github.com/SantiM-wronghacker/agencia-IA.git
cd agencia-IA

# Create virtual environment
python -m venv .venv

# Activate (Windows CMD)
.venv\Scripts\activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode (fixes ModuleNotFoundError: agencia)
pip install -e .
```

### 2. Run Dashboard API (:8001)

```bash
# From the project root, with venv activated:
uvicorn src.agencia.api.dashboard.routes:app --host 0.0.0.0 --port 8001 --reload
```

The API docs are available at: `http://localhost:8001/docs`

### 3. Run React Frontend (:3000)

```bash
cd frontend
npm install
npm start
```

Open `http://localhost:3000` in your browser.

### 4. (Optional) Run Streamlit Dashboard

```bash
# From project root
streamlit run dashboard_streamlit.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/dashboard/health` | Health check |
| GET | `/api/v2/dashboard/metrics` | Aggregated metrics |
| POST | `/api/v2/dashboard/tasks` | Create a task |
| GET | `/api/v2/dashboard/tasks` | List tasks (`?status=&search=`) |
| GET | `/api/v2/dashboard/tasks/{id}` | Get a task |
| PATCH | `/api/v2/dashboard/tasks/{id}` | Update a task |
| POST | `/api/v2/dashboard/tasks/{id}/cancel` | Cancel a task |
| GET | `/api/v2/dashboard/tasks/{id}/logs` | Get task logs |
| GET | `/api/v2/dashboard/tasks/export?format=csv\|json` | Export tasks |
| POST | `/api/v2/dashboard/run-agent` | Run agent (stub) |
| GET | `/api/v2/dashboard/alerts` | Get active alerts |
| GET | `/api/v2/dashboard/alerts/config` | Get alert config |
| PUT | `/api/v2/dashboard/alerts/config` | Update alert config |
| WS | `/api/v2/dashboard/ws` | Real-time events |

## WebSocket

Connect to `ws://localhost:8001/api/v2/dashboard/ws` to receive real-time events:

```json
{"event": "task_created", "task": {...}}
{"event": "task_updated", "task": {...}}
{"event": "task_cancelled", "task": {...}}
```

### Testing WebSocket manually

**With websocat:**
```bash
websocat ws://localhost:8001/api/v2/dashboard/ws
```

**With Python:**
```python
import asyncio
import websockets

async def listen():
    async with websockets.connect("ws://localhost:8001/api/v2/dashboard/ws") as ws:
        async for msg in ws:
            print(msg)

asyncio.run(listen())
```

**With browser console:**
```javascript
const ws = new WebSocket('ws://localhost:8001/api/v2/dashboard/ws');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
ws.onopen = () => console.log('Connected!');
```

## Export

- **CSV**: `GET http://localhost:8001/api/v2/dashboard/tasks/export?format=csv`
- **JSON**: `GET http://localhost:8001/api/v2/dashboard/tasks/export?format=json`

The React UI has Export CSV / Export JSON buttons on the Tasks page.

## Alerts

Alerts are triggered when:
- Failed tasks exceed a configurable threshold (default: 5)
- Success rate drops below a configurable threshold (default: 80%)

Configure via API:
```bash
curl -X PUT http://localhost:8001/api/v2/dashboard/alerts/config \
  -H "Content-Type: application/json" \
  -d '{"max_failed": 3, "min_success_rate": 90.0}'
```

## SQLite Persistence

Tasks are stored in `data/tasks.db` (auto-created). Override with the `DASHBOARD_DB_PATH` environment variable.

Data survives API restarts — no Docker required.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DASHBOARD_DB_PATH` | `data/tasks.db` | SQLite database file path |
| `DASHBOARD_CORS_ORIGINS` | `*` | CORS allowed origins (comma-separated) |
| `DASHBOARD_SECRET_KEY` | `dev-secret-key-...` | JWT signing key |
| `DASHBOARD_ALERT_CONFIG` | `data/alert_config.json` | Alert config file path |
| `REACT_APP_API_URL` | `http://localhost:8001` | API base URL for frontend |
| `REACT_APP_WS_URL` | `ws://localhost:8001/api/v2/dashboard/ws` | WebSocket URL |

## Running Tests

```bash
# From project root with venv activated
pip install pytest httpx
python -m pytest tests/integration/test_dashboard_api.py -v
```

## Compatibility Notes

- **Python 3.10–3.13**: Fully compatible on Windows, Linux, and macOS
- **No Docker required**: SQLite is used for persistence
- **Windows-friendly**: No Unix-specific dependencies
- The `pip install -e .` step resolves import issues with the `agencia` package
