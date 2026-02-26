"""Tests for the FastAPI endpoints."""
from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from api import app
    return TestClient(app)


def test_health_ollama_down(client):
    with patch("api.http_requests.get", side_effect=ConnectionError("refused")):
        r = client.get("/health")
        assert r.status_code == 503


def test_health_ollama_up(client):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"models": []}
    mock_resp.raise_for_status = MagicMock()
    with patch("api.http_requests.get", return_value=mock_resp):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


def test_chat_endpoint(client):
    """Test /chat with mocked LLM."""
    with patch("agent_router_projects.llm", return_value="CHAT"), \
         patch("core.llm", return_value="Hola, test response"):
        r = client.post("/chat", json={
            "company": "test_co",
            "project": "test_proj",
            "message": "hola"
        })
        assert r.status_code == 200
        data = r.json()
        assert "response" in data
        assert "route" in data
