"""Integration tests for the Dashboard V2 FastAPI backend."""

import json
import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from src.agencia.api.dashboard.models import TaskStatus
from src.agencia.api.dashboard.repository import TaskRepository
from src.agencia.api.dashboard import routes


@pytest.fixture(autouse=True)
def _use_tmp_db(tmp_path, monkeypatch):
    """Point the repository at a temporary SQLite database for each test."""
    db_path = str(tmp_path / "test.db")
    new_repo = TaskRepository(db_path=db_path)
    monkeypatch.setattr(routes, "repo", new_repo)
    yield


@pytest.fixture()
def client():
    return TestClient(routes.app)


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


def test_cancel_completed_task(client):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Done task"})
    task_id = create_resp.json()["id"]
    # Use PATCH to mark as completed
    client.patch(f"/api/v2/dashboard/tasks/{task_id}", json={"status": "completed"})
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


# ---- WebSocket event envelope ----


def test_websocket_receives_task_created(client):
    """WS client receives task_created with the unified envelope."""
    with client.websocket_connect("/api/v2/dashboard/ws") as ws:
        client.post("/api/v2/dashboard/tasks", json={"name": "WS test"})
        raw = ws.receive_text()
        msg = json.loads(raw)
        assert msg["event"] == "task_created"
        assert "ts" in msg
        assert msg["payload"]["name"] == "WS test"


def test_websocket_receives_task_updated(client):
    """WS client receives task_updated after PATCH."""
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Upd"})
    task_id = create_resp.json()["id"]

    with client.websocket_connect("/api/v2/dashboard/ws") as ws:
        client.patch(f"/api/v2/dashboard/tasks/{task_id}", json={"status": "running"})
        raw = ws.receive_text()
        msg = json.loads(raw)
        assert msg["event"] == "task_updated"
        assert msg["payload"]["status"] == "running"


def test_websocket_receives_task_cancelled(client):
    """WS client receives task_cancelled on cancel."""
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Canc"})
    task_id = create_resp.json()["id"]

    with client.websocket_connect("/api/v2/dashboard/ws") as ws:
        client.post(f"/api/v2/dashboard/tasks/{task_id}/cancel")
        raw = ws.receive_text()
        msg = json.loads(raw)
        assert msg["event"] == "task_cancelled"
        assert msg["payload"]["status"] == "cancelled"
