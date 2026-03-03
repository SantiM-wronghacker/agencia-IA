"""Integration tests for health-check endpoints."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.agencia.api.health import router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_health_live(client):
    r = client.get("/health/live")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "alive"
    assert "uptime_seconds" in data


def test_health_ready(client):
    r = client.get("/health/ready")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] in ("ready", "not_ready")
    assert "checks" in data


def test_health_detailed(client):
    r = client.get("/health/detailed")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] in ("healthy", "degraded")
    assert "checks" in data
    assert "timestamp" in data
    for service in ("database", "redis", "elasticsearch", "llm_providers",
                    "disk_space", "memory", "queue_depth"):
        assert service in data["checks"]


def test_health_services(client):
    r = client.get("/health/services")
    assert r.status_code == 200
    data = r.json()
    for service in ("database", "redis", "elasticsearch", "llm_providers"):
        assert service in data
    assert "timestamp" in data


def test_health_detailed_status_values(client):
    """Each check must have a 'status' and 'service' key."""
    r = client.get("/health/detailed")
    data = r.json()
    for name, check in data["checks"].items():
        assert "status" in check, f"{name} missing 'status'"
        assert check["status"] in ("healthy", "unhealthy", "unknown")
