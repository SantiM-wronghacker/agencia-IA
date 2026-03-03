"""Tests for the intent router (LLM calls mocked)."""
from unittest.mock import patch


def test_route_intent_chat():
    from agencia.agents.cerebro.agent_router_projects import route_intent
    state = {"summary": "", "recent": []}
    with patch("agencia.agents.cerebro.agent_router_projects.llm", return_value="CHAT"):
        assert route_intent(state, "hola, como estas?") == "CHAT"


def test_route_intent_save():
    from agencia.agents.cerebro.agent_router_projects import route_intent
    state = {"summary": "", "recent": []}
    with patch("agencia.agents.cerebro.agent_router_projects.llm", return_value="SAVE"):
        assert route_intent(state, "guardar: Titulo | contenido") == "SAVE"


def test_route_intent_task():
    from agencia.agents.cerebro.agent_router_projects import route_intent
    state = {"summary": "", "recent": []}
    with patch("agencia.agents.cerebro.agent_router_projects.llm", return_value="TASK"):
        assert route_intent(state, "hazme un plan de marketing") == "TASK"


def test_route_intent_rag():
    from agencia.agents.cerebro.agent_router_projects import route_intent
    state = {"summary": "", "recent": []}
    with patch("agencia.agents.cerebro.agent_router_projects.llm", return_value="RAG"):
        assert route_intent(state, "cuanto cuesta el paquete pro?") == "RAG"


def test_route_intent_invalid_defaults_to_chat():
    """If the LLM returns garbage, default to CHAT."""
    from agencia.agents.cerebro.agent_router_projects import route_intent
    state = {"summary": "", "recent": []}
    with patch("agencia.agents.cerebro.agent_router_projects.llm", return_value="BANANA something"):
        assert route_intent(state, "test") == "CHAT"
