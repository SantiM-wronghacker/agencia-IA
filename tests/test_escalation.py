"""Tests for the auto-escalation heuristic."""


def test_escalation_empty_answer():
    from agencia.agents.cerebro.agent_router_state_autoscale import needs_escalation
    assert needs_escalation("", route="CHAT") is True


def test_escalation_red_flag():
    from agencia.agents.cerebro.agent_router_state_autoscale import needs_escalation
    assert needs_escalation("No sé la respuesta", route="CHAT") is True


def test_escalation_short_chat_no_escalate():
    """Short answers in CHAT should NOT trigger escalation."""
    from agencia.agents.cerebro.agent_router_state_autoscale import needs_escalation
    assert needs_escalation("Hola, estoy bien.", route="CHAT") is False


def test_escalation_short_task_escalates():
    """Short answers in TASK should trigger escalation."""
    from agencia.agents.cerebro.agent_router_state_autoscale import needs_escalation
    assert needs_escalation("Ok.", route="TASK") is True


def test_escalation_short_rag_escalates():
    """Short answers in RAG should trigger escalation."""
    from agencia.agents.cerebro.agent_router_state_autoscale import needs_escalation
    assert needs_escalation("Si.", route="RAG") is True


def test_escalation_long_answer_no_escalate():
    from agencia.agents.cerebro.agent_router_state_autoscale import needs_escalation
    long_answer = "Esta es una respuesta suficientemente larga que no deberia activar la escalacion automatica al modelo fuerte."
    assert needs_escalation(long_answer, route="TASK") is False
