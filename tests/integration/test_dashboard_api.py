"""Integration tests for the Dashboard V2 FastAPI backend with SQLite persistence."""

import json
import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from src.agencia.api.dashboard.models import TaskStatus
from src.agencia.api.dashboard.repository import TaskRepository
from src.agencia.api.dashboard.routes import app, _task_store, set_repo, get_repo


@pytest.fixture(autouse=True)
def _setup_test_repo(tmp_path):
    """Use a temporary SQLite database for each test."""
    db_path = str(tmp_path / "test_tasks.db")
    repo = TaskRepository(db_path=db_path)
    set_repo(repo)
    _task_store.clear()
    yield repo
    _task_store.clear()
    # Reset repo so next test gets a fresh one
    set_repo(None)


@pytest.fixture()
def client():
    from src.agencia.api.dashboard.routes import app
    return TestClient(app)


# ---- Health ----


def test_health_endpoint(client):
    resp = client.get("/api/v2/dashboard/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "database" in data["services"]


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


def test_cancel_completed_task(client, _setup_test_repo):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Done task"})
    task_id = create_resp.json()["id"]
    # Manually mark as completed via repository
    repo = _setup_test_repo
    task = repo.get(task_id)
    task.status = TaskStatus.COMPLETED
    repo.update(task)
    resp = client.post(f"/api/v2/dashboard/tasks/{task_id}/cancel")
    assert resp.status_code == 400


# ---- PATCH (update) ----


def test_update_task_status(client):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Patchable"})
    task_id = create_resp.json()["id"]
    resp = client.patch(f"/api/v2/dashboard/tasks/{task_id}", json={"status": "running"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "running"


def test_update_task_name(client):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Old"})
    task_id = create_resp.json()["id"]
    resp = client.patch(f"/api/v2/dashboard/tasks/{task_id}", json={"name": "New"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New"


def test_update_task_not_found(client):
    resp = client.patch("/api/v2/dashboard/tasks/nope", json={"name": "X"})
    assert resp.status_code == 404


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


# ---- Update (PATCH) ----


def test_update_task_name(client):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Old Name"})
    task_id = create_resp.json()["id"]
    resp = client.patch(f"/api/v2/dashboard/tasks/{task_id}", json={"name": "New Name"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"


def test_update_task_status(client):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Run me"})
    task_id = create_resp.json()["id"]
    resp = client.patch(f"/api/v2/dashboard/tasks/{task_id}", json={"status": "running"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "running"


def test_update_task_not_found(client):
    resp = client.patch("/api/v2/dashboard/tasks/nonexistent", json={"name": "X"})
    assert resp.status_code == 404


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


# ---- PATCH (update) ----


def test_patch_task(client):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Original"})
    task_id = create_resp.json()["id"]
    resp = client.patch(
        f"/api/v2/dashboard/tasks/{task_id}",
        json={"name": "Updated", "status": "running"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Updated"
    assert data["status"] == "running"


def test_patch_task_not_found(client):
    resp = client.patch(
        "/api/v2/dashboard/tasks/nonexistent-id",
        json={"name": "X"},
    )
    assert resp.status_code == 404


# ---- Export ----


def test_export_json(client):
    client.post("/api/v2/dashboard/tasks", json={"name": "Export Test"})
    resp = client.get("/api/v2/dashboard/tasks/export?format=json")
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("content-type", "")
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_export_csv(client):
    client.post("/api/v2/dashboard/tasks", json={"name": "CSV Test"})
    resp = client.get("/api/v2/dashboard/tasks/export?format=csv")
    assert resp.status_code == 200
    assert "text/csv" in resp.headers.get("content-type", "")
    lines = resp.text.strip().split("\n")
    assert len(lines) == 2  # header + 1 row
    assert "CSV Test" in lines[1]


# ---- Run Agent (stub) ----


def test_run_agent_stub(client):
    resp = client.post(
        "/api/v2/dashboard/run-agent",
        json={"category": "test", "agent_name": "echo", "input": "hello"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "Agent: test/echo" in data["name"]
    assert data["status"] == "completed"
    assert len(data["logs"]) > 0


# ---- Alerts ----


def test_get_alert_config(client):
    resp = client.get("/api/v2/dashboard/alerts/config")
    assert resp.status_code == 200
    data = resp.json()
    assert "max_failed" in data
    assert "min_success_rate" in data


def test_update_alert_config(client):
    resp = client.put(
        "/api/v2/dashboard/alerts/config",
        json={"max_failed": 3, "min_success_rate": 90.0},
    )
    assert resp.status_code == 200
    assert resp.json()["max_failed"] == 3


def test_get_alerts(client):
    resp = client.get("/api/v2/dashboard/alerts")
    assert resp.status_code == 200
    data = resp.json()
    assert "alerts" in data
    assert "config" in data


# ---- SQLite Persistence ----


def test_persistence_after_restart(_setup_test_repo):
    """Simulate restart: create tasks, then create a new repo on same DB."""
    repo = _setup_test_repo
    from datetime import datetime, timezone
    from src.agencia.api.dashboard.models import TaskSchema, TaskStatus
    import uuid

    now = datetime.now(timezone.utc)
    task = TaskSchema(
        id=str(uuid.uuid4()),
        name="Persistent Task",
        status=TaskStatus.PENDING,
        created_at=now,
        updated_at=now,
    )
    repo.create(task)

    # Simulate restart: create a new repository pointing to same DB
    repo2 = TaskRepository(db_path=repo.db_path)
    tasks = repo2.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].name == "Persistent Task"
    assert tasks[0].id == task.id


# ---- WebSocket ----


def test_websocket_connection(client):
    with client.websocket_connect("/api/v2/dashboard/ws") as ws:
        ws.send_text("hello")
        data = ws.receive_text()
        assert "hello" in data


def test_websocket_endpoint_exists(client):
    """Verify the WebSocket endpoint exists and can be connected to."""
    with client.websocket_connect("/api/v2/dashboard/ws") as ws:
        ws.send_text("ping")
        resp = ws.receive_json(mode="text")
        assert resp["event"] == "echo"
        assert resp["data"] == "ping"
