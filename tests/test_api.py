"""Tests for the FastAPI endpoints."""
from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from agencia.agents.tecnologia.api import app
    return TestClient(app)


def test_health_groq_not_configured(client):
    with patch("agencia.agents.tecnologia.api.GROQ_API_KEY", "gsk_not_set"):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "warning"


def test_health_groq_configured(client):
    with patch("agencia.agents.tecnologia.api.GROQ_API_KEY", "real_key_value"):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


def test_chat_endpoint(client):
    """Test /chat with mocked LLM."""
    with patch("agencia.agents.cerebro.agent_router_projects.llm", return_value="CHAT"), \
         patch("agencia.agents.herramientas.core.llm", return_value="Hola, test response"):
        r = client.post("/chat", json={
            "company": "test_co",
            "project": "test_proj",
            "message": "hola"
        })
        assert r.status_code == 200
        data = r.json()
        assert "output" in data
        assert "timestamp" in data
