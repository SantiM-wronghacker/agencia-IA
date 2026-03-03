# Dashboard V2 — Architecture & Documentation

## Architecture Overview

The original dashboard (`app_dashboard.py`) is a monolithic Flask application that serves
both HTML templates and data endpoints from a single process on port 5000.

**Dashboard V2** decouples the stack into three layers:

| Layer       | Technology       | Port | Role                        |
|-------------|------------------|------|-----------------------------|
| Frontend    | React + TailwindCSS | 3000 | SPA served by Nginx         |
| Backend API | FastAPI          | 8001 | REST + WebSocket endpoints  |
| Reverse Proxy | Nginx          | 80   | Unified entry point         |

The legacy Flask dashboard remains available at port 5000 and can run in parallel
during migration (see `MIGRATION_DASHBOARD.md`).

---

## Architecture Diagram

```
                         ┌──────────────┐
                         │   Browser    │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │  Nginx :80   │
                         └──┬───┬───┬───┘
                            │   │   │
              ┌─────────────┘   │   └─────────────┐
              │                 │                 │
     ┌────────▼────────┐ ┌─────▼──────┐ ┌────────▼────────┐
     │  React SPA      │ │ FastAPI    │ │ Flask Dashboard  │
     │  :3000          │ │ :8001      │ │ :5000 (legacy)   │
     │  /dashboard/*   │ │ /api/v2/*  │ │ /                │
     └─────────────────┘ └─────┬──────┘ └─────────────────┘
                                │
                         ┌──────▼───────┐
                         │  In-Memory   │
                         │  Task Store  │
                         └──────────────┘
```

---

## Feature Comparison

| Feature                  | Flask Dashboard (v1) | FastAPI + React (v2) |
|--------------------------|----------------------|----------------------|
| Server-rendered HTML     | ✅                    | —                    |
| Single-page application  | —                    | ✅                    |
| REST API                 | Partial              | ✅ Full               |
| WebSocket real-time      | —                    | ✅                    |
| Task management          | Basic                | Full CRUD + cancel   |
| Metrics endpoint         | —                    | ✅                    |
| Filtering & search       | —                    | ✅                    |
| Hot reload (dev)         | —                    | ✅                    |
| Docker support           | Manual               | ✅ docker-compose     |

---

## API Endpoints

All endpoints are prefixed with `/api/v2/dashboard`.

| Method | Path                        | Description                     |
|--------|-----------------------------|---------------------------------|
| GET    | `/health`                   | Health check — returns `{ "status": "ok" }` |
| GET    | `/tasks`                    | List all tasks (supports `?status=` and `?search=` query params) |
| POST   | `/tasks`                    | Create a new task (201)         |
| GET    | `/tasks/{task_id}`          | Get a single task by ID         |
| POST   | `/tasks/{task_id}/cancel`   | Cancel a pending task           |
| GET    | `/tasks/{task_id}/logs`     | Retrieve logs for a task        |
| GET    | `/metrics`                  | Aggregated task metrics         |
| WS     | `/ws`                       | WebSocket for real-time events  |

### Query Parameters

- `GET /tasks?status=pending` — filter tasks by status (`pending`, `running`, `completed`, `cancelled`).
- `GET /tasks?search=keyword` — search tasks by name (case-insensitive substring match).

---

## WebSocket Events

Connect to `ws://<host>/api/v2/dashboard/ws`.

| Event            | Direction      | Description                       |
|------------------|----------------|-----------------------------------|
| `task_created`   | Server → Client | Fired when a new task is created  |
| `task_cancelled` | Server → Client | Fired when a task is cancelled    |
| `echo`           | Client ↔ Server | Server echoes any message back    |

### Example Message (JSON)

```json
{
  "event": "task_created",
  "data": {
    "id": "abc-123",
    "name": "Run pipeline",
    "status": "pending"
  }
}
```

---

## Tech Stack

- **Frontend:** React 18, TypeScript, TailwindCSS, React Query, React Router
- **Backend:** FastAPI, Uvicorn, Pydantic
- **Proxy:** Nginx
- **Containerisation:** Docker, Docker Compose
- **Testing:** pytest (backend), Jest + React Testing Library (frontend)
