"""
Smoke test script – verifies the full lifecycle:
1. Create a task
2. Update to RUNNING
3. Cancel
4. Verify WS events for each step

Usage::

    pytest tests/integration/test_smoke.py -v
"""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from src.agencia.api.dashboard.repository import TaskRepository
from src.agencia.api.dashboard import routes


@pytest.fixture(autouse=True)
def _use_tmp_db(tmp_path, monkeypatch):
    db_path = str(tmp_path / "smoke.db")
    monkeypatch.setattr(routes, "repo", TaskRepository(db_path=db_path))
    yield


@pytest.fixture()
def client():
    return TestClient(routes.app)


def test_full_lifecycle(client):
    """End-to-end smoke test: create → update → cancel with WS events."""

    with client.websocket_connect("/api/v2/dashboard/ws") as ws:
        # 1) Create task
        resp = client.post(
            "/api/v2/dashboard/tasks",
            json={"name": "Smoke Task", "description": "End-to-end check"},
        )
        assert resp.status_code == 201
        task_id = resp.json()["id"]

        evt1 = json.loads(ws.receive_text())
        assert evt1["event"] == "task_created"
        assert evt1["payload"]["name"] == "Smoke Task"
        assert "ts" in evt1

        # 2) Update to RUNNING
        resp = client.patch(
            f"/api/v2/dashboard/tasks/{task_id}",
            json={"status": "running"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "running"

        evt2 = json.loads(ws.receive_text())
        assert evt2["event"] == "task_updated"
        assert evt2["payload"]["status"] == "running"

        # 3) Cancel
        resp = client.post(f"/api/v2/dashboard/tasks/{task_id}/cancel")
        assert resp.status_code == 200
        assert resp.json()["status"] == "cancelled"

        evt3 = json.loads(ws.receive_text())
        assert evt3["event"] == "task_cancelled"
        assert evt3["payload"]["status"] == "cancelled"

    # 4) Verify final state via REST
    resp = client.get(f"/api/v2/dashboard/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"

    # 5) Verify metrics
    resp = client.get("/api/v2/dashboard/metrics")
    assert resp.status_code == 200
    assert resp.json()["total_tasks"] == 1
