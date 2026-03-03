# Dashboard Migration Guide

This guide explains how to run the legacy Flask dashboard and the new
FastAPI + React dashboard **side by side** and how to switch between them.

---

## Dashboard URLs

| Dashboard        | URL                     | Tech          |
|------------------|-------------------------|---------------|
| Old (Flask)      | http://localhost:5000    | Flask + Jinja |
| New — Frontend   | http://localhost:3000    | React SPA     |
| New — API        | http://localhost:8001    | FastAPI       |

---

## Method 1 — Docker (recommended)

Start every service with a single command:

```bash
docker-compose up --build
```

This launches:

| Service          | Container               | Port |
|------------------|-------------------------|------|
| `api`            | agencia-api             | 8000 |
| `dashboard-api`  | agencia-dashboard-api   | 8001 |
| `frontend`       | agencia-frontend        | 3000 |
| `flask-dashboard`| agencia-flask-dashboard | 5000 |

To stop everything:

```bash
docker-compose down
```

---

## Method 2 — Manual (no Docker)

Open **four** separate terminals:

### Terminal 1 — Main API (port 8000)

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Terminal 2 — Dashboard API (port 8001)

```bash
uvicorn src.agencia.api.dashboard:app --host 0.0.0.0 --port 8001
```

### Terminal 3 — React Frontend (port 3000)

```bash
cd frontend
npm install   # first time only
npm start
```

### Terminal 4 — Flask Dashboard (port 5000)

```bash
python app_dashboard.py
```

---

## Switching from Old to New

1. **Run both** dashboards in parallel using either method above.
2. **Validate** the new dashboard at http://localhost:3000 — ensure all
   tasks, metrics, and real-time updates work as expected.
3. **Redirect users** by updating bookmarks, links, or reverse-proxy rules
   to point to the new frontend.
4. **Retire the Flask dashboard** once the new dashboard is fully validated
   by removing the `flask-dashboard` service from `docker-compose.yml`
   (or stopping Terminal 4 in the manual method).
