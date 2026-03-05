"""Integration tests for the Dashboard V2 FastAPI backend."""

import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from src.agencia.api.dashboard.models import TaskStatus
from src.agencia.api.dashboard.store import TaskStore


@pytest.fixture(autouse=True)
def _use_tmp_db(monkeypatch, tmp_path):
    """Point the dashboard store to a temporary SQLite DB for every test."""
    db_path = str(tmp_path / "test_dashboard.db")

    # Patch the module-level _task_store in routes before import
    import src.agencia.api.dashboard.routes as routes_mod

    store = TaskStore(db_path=db_path)
    monkeypatch.setattr(routes_mod, "_task_store", store)
    yield store
    store.close()


@pytest.fixture()
def client():
    from src.agencia.api.dashboard.routes import app
    return TestClient(app)


# ---- Health ----


def test_health_endpoint(client):
    resp = client.get("/api/v2/dashboard/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# ---- Create ----


def test_create_task(client):
    payload = {"name": "Train model", "description": "Fine-tune LLM"}
    resp = client.post("/api/v2/dashboard/tasks", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Train model"
    assert data["status"] == "pending"
    assert "id" in data


# ---- List ----


def test_list_tasks(client):
    client.post("/api/v2/dashboard/tasks", json={"name": "Task A"})
    client.post("/api/v2/dashboard/tasks", json={"name": "Task B"})
    resp = client.get("/api/v2/dashboard/tasks")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) == 2


# ---- Get single task ----


def test_get_task(client):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "My Task"})
    task_id = create_resp.json()["id"]
    resp = client.get(f"/api/v2/dashboard/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "My Task"


def test_get_task_not_found(client):
    resp = client.get("/api/v2/dashboard/tasks/invalid-id-999")
    assert resp.status_code == 404


# ---- Cancel ----


def test_cancel_task(client):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Cancel me"})
    task_id = create_resp.json()["id"]
    resp = client.post(f"/api/v2/dashboard/tasks/{task_id}/cancel")
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"


def test_cancel_completed_task(client, _use_tmp_db):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Done task"})
    task_id = create_resp.json()["id"]
    # Manually mark as completed via the store
    task = _use_tmp_db.get(task_id)
    task.status = TaskStatus.COMPLETED
    _use_tmp_db.update(task)
    resp = client.post(f"/api/v2/dashboard/tasks/{task_id}/cancel")
    assert resp.status_code == 400


# ---- Logs ----


def test_get_task_logs(client):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Log task"})
    task_id = create_resp.json()["id"]
    resp = client.get(f"/api/v2/dashboard/tasks/{task_id}/logs")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ---- Metrics ----


def test_metrics(client):
    client.post("/api/v2/dashboard/tasks", json={"name": "T1"})
    client.post("/api/v2/dashboard/tasks", json={"name": "T2"})
    resp = client.get("/api/v2/dashboard/metrics")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_tasks"] == 2
    assert data["pending"] == 2


# ---- Filtering & Search ----


def test_filter_tasks_by_status(client):
    client.post("/api/v2/dashboard/tasks", json={"name": "A"})
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "B"})
    task_id = create_resp.json()["id"]
    client.post(f"/api/v2/dashboard/tasks/{task_id}/cancel")

    resp = client.get("/api/v2/dashboard/tasks?status=cancelled")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["status"] == "cancelled"


def test_search_tasks(client):
    client.post("/api/v2/dashboard/tasks", json={"name": "Deploy API"})
    client.post("/api/v2/dashboard/tasks", json={"name": "Train model"})

    resp = client.get("/api/v2/dashboard/tasks?search=deploy")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert "Deploy" in results[0]["name"]


# ---- WebSocket ----


def test_websocket_connection(client):
    with client.websocket_connect("/api/v2/dashboard/ws") as ws:
        ws.send_text("hello")
        data = ws.receive_text()
        assert "hello" in data


# ---- WebSocket contract: events include {event, ts, payload} ----


def test_ws_receives_task_created_event(client):
    """Creating a task emits a task_created event over WS with the unified contract."""
    import json

    with client.websocket_connect("/api/v2/dashboard/ws") as ws:
        # Create a task via the REST API (will broadcast to WS)
        resp = client.post("/api/v2/dashboard/tasks", json={"name": "WS task"})
        assert resp.status_code == 201

        raw = ws.receive_text()
        msg = json.loads(raw)

        assert msg["event"] == "task_created"
        assert "ts" in msg
        assert "payload" in msg
        assert msg["payload"]["name"] == "WS task"


def test_ws_receives_task_cancelled_event(client):
    """Cancelling a task emits a task_cancelled event over WS with the unified contract."""
    import json

    with client.websocket_connect("/api/v2/dashboard/ws") as ws:
        # Create + cancel
        resp = client.post("/api/v2/dashboard/tasks", json={"name": "To cancel"})
        task_id = resp.json()["id"]
        # consume the task_created event
        ws.receive_text()

        client.post(f"/api/v2/dashboard/tasks/{task_id}/cancel")
        raw = ws.receive_text()
        msg = json.loads(raw)

        assert msg["event"] == "task_cancelled"
        assert "ts" in msg
        assert "payload" in msg
        assert msg["payload"]["status"] == "cancelled"


# ---- SQLite persistence ----


def test_sqlite_crud(_use_tmp_db, client):
    """Tasks survive in SQLite – full CRUD cycle."""
    # Create
    resp = client.post("/api/v2/dashboard/tasks", json={"name": "Persist me", "description": "d"})
    assert resp.status_code == 201
    task_id = resp.json()["id"]

    # Read
    resp = client.get(f"/api/v2/dashboard/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Persist me"

    # Cancel (update)
    resp = client.post(f"/api/v2/dashboard/tasks/{task_id}/cancel")
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"

    # List
    resp = client.get("/api/v2/dashboard/tasks")
    assert resp.status_code == 200
    assert any(t["id"] == task_id for t in resp.json())


def test_sqlite_persistence_across_restarts(tmp_path):
    """Simulates a restart by creating a new TaskStore pointing to the same DB file."""
    from src.agencia.api.dashboard.store import TaskStore
    from src.agencia.api.dashboard.models import TaskSchema, TaskStatus
    from datetime import datetime, timezone
    import uuid

    db_path = str(tmp_path / "restart_test.db")

    # First "run" – create a task
    store1 = TaskStore(db_path=db_path)
    now = datetime.now(timezone.utc)
    task = TaskSchema(
        id=str(uuid.uuid4()),
        name="Survive restart",
        status=TaskStatus.PENDING,
        created_at=now,
        updated_at=now,
    )
    store1.add(task)
    store1.close()

    # Second "run" – new store instance must find the task
    store2 = TaskStore(db_path=db_path)
    found = store2.get(task.id)
    assert found is not None
    assert found.name == "Survive restart"
    assert found.status == TaskStatus.PENDING
    store2.close()


# ---- TeamDirector / Role enforcement ----


def test_director_assign_valid_role(client):
    resp = client.post(
        "/api/v2/dashboard/director/assign",
        json={"role": "admin", "task": "Deploy v2"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["role"] == "admin"
    assert data["status"] == "assigned"


def test_director_reject_unregistered_role(client):
    resp = client.post(
        "/api/v2/dashboard/director/assign",
        json={"role": "hacker", "task": "Do something"},
    )
    assert resp.status_code == 400
    assert "not registered" in resp.json()["detail"]


def test_director_missing_fields(client):
    resp = client.post(
        "/api/v2/dashboard/director/assign",
        json={"role": "admin"},
    )
    assert resp.status_code == 400


def test_team_director_class_rejects_unknown_role():
    """Unit-level: TeamDirector.assign raises ValueError for unknown roles."""
    from src.agencia.api.dashboard.team_director import TeamDirector
    import pytest

    director = TeamDirector()
    with pytest.raises(ValueError, match="not registered"):
        director.assign("supervillain", "take over")
