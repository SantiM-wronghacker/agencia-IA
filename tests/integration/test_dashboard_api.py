"""Integration tests for the Dashboard V2 FastAPI backend."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from src.agencia.api.dashboard.models import TaskStatus
from src.agencia.api.dashboard.routes import app, _task_store


@pytest.fixture(autouse=True)
def clear_task_store():
    """Clear the in-memory task store before every test."""
    _task_store.clear()
    yield
    _task_store.clear()


@pytest.fixture()
def client():
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


def test_cancel_completed_task(client):
    create_resp = client.post("/api/v2/dashboard/tasks", json={"name": "Done task"})
    task_id = create_resp.json()["id"]
    # Manually mark as completed
    _task_store[task_id].status = TaskStatus.COMPLETED
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
