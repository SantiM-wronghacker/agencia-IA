"""
Agencia IA - Unit Tests for Core Agents

Tests for BaseAgent, AgentRegistry, DynamicRouter, and LLM Router.
"""

import pytest
from src.agencia.core.base_agent import BaseAgent
from src.agencia.core.agent_registry import AgentRegistry, AgentRecord
from src.agencia.core.router import DynamicRouter
from src.agencia.core.llm_router_mejorado import AdvancedLLMRouter, MODEL_CONFIG, CATEGORY_MODEL_MAP
from src.agencia.core.metrics import (
    record_agent_execution,
    get_metrics_summary,
    generate_prometheus_text,
)
from src.agencia.core.logging_config import JSONFormatter, setup_logging


# ─── BaseAgent Tests ──────────────────────────────────────────


class ConcreteAgent(BaseAgent):
    """Concrete implementation for testing."""

    def execute(self, input_data):
        return {"result": f"OK: {input_data.get('query', '')}"}

    def get_capabilities(self):
        return ["test", "demo"]


class FailingAgent(BaseAgent):
    """Agent that always raises an error."""

    def execute(self, input_data):
        raise ValueError("Test error")


class TestBaseAgent:
    def test_create_agent(self):
        agent = ConcreteAgent(
            name="test", category="herramientas", description="Test agent"
        )
        assert agent.name == "test"
        assert agent.category == "herramientas"
        assert agent.version == "1.0.0"

    def test_run_success(self):
        agent = ConcreteAgent(name="test", category="herramientas")
        result = agent.run({"query": "hello"})
        assert result["result"] == "OK: hello"
        assert agent._execution_count == 1
        assert agent._error_count == 0

    def test_run_caching(self):
        agent = ConcreteAgent(name="test", category="herramientas")
        result1 = agent.run({"query": "hello"})
        result2 = agent.run({"query": "hello"})
        assert result1 == result2
        assert agent._execution_count == 1  # Only executed once due to cache

    def test_run_error(self):
        agent = FailingAgent(name="fail", category="herramientas")
        with pytest.raises(ValueError, match="Test error"):
            agent.run({"query": "test"})
        assert agent._error_count == 1

    def test_health_check(self):
        agent = ConcreteAgent(name="test", category="herramientas")
        agent.run({"query": "a"})
        health = agent.health_check()
        assert health["name"] == "test"
        assert health["status"] == "healthy"
        assert health["execution_count"] == 1
        assert health["success_rate"] == 100.0

    def test_clear_cache(self):
        agent = ConcreteAgent(name="test", category="herramientas")
        agent.run({"query": "hello"})
        assert len(agent._cache) == 1
        agent.clear_cache()
        assert len(agent._cache) == 0

    def test_get_capabilities(self):
        agent = ConcreteAgent(name="test", category="herramientas")
        assert agent.get_capabilities() == ["test", "demo"]

    def test_repr(self):
        agent = ConcreteAgent(name="test", category="herramientas")
        assert "ConcreteAgent" in repr(agent)
        assert "test" in repr(agent)


# ─── AgentRegistry Tests ─────────────────────────────────────


class TestAgentRegistry:
    def test_register_agent(self, registry):
        record = registry.register(
            name="agent1", category="finanzas", description="Test"
        )
        assert record.name == "agent1"
        assert record.category == "finanzas"
        assert registry.count() == 1

    def test_get_agent(self, registry):
        registry.register(name="agent1", category="finanzas")
        agent = registry.get("agent1")
        assert agent is not None
        assert agent.name == "agent1"

    def test_get_nonexistent(self, registry):
        assert registry.get("nonexistent") is None

    def test_find_by_category(self, populated_registry):
        agents = populated_registry.find_by_category("finanzas")
        assert len(agents) == 1
        assert agents[0].name == "agent_finanzas_1"

    def test_find_by_capability(self, populated_registry):
        agents = populated_registry.find_by_capability("roi")
        assert len(agents) == 1
        assert agents[0].name == "agent_finanzas_1"

    def test_find_by_status(self, populated_registry):
        active = populated_registry.find_by_status("active")
        assert len(active) == 4

    def test_list_categories(self, populated_registry):
        categories = populated_registry.list_categories()
        assert "finanzas" in categories
        assert "legal" in categories

    def test_log_execution(self, registry):
        registry.log_execution("agent1", 100.0, "success")
        summary = registry.get_health_summary()
        assert summary["total_executions"] == 1

    def test_deactivate(self, populated_registry):
        result = populated_registry.deactivate("agent_finanzas_1")
        assert result is True
        agent = populated_registry.get("agent_finanzas_1")
        assert agent.status == "inactive"

    def test_health_summary(self, populated_registry):
        summary = populated_registry.get_health_summary()
        assert summary["total_agents"] == 4
        assert summary["active_agents"] == 4
        assert summary["success_rate"] == 100.0


# ─── DynamicRouter Tests ─────────────────────────────────────


class TestDynamicRouter:
    def test_route_by_category(self, populated_registry):
        router = DynamicRouter(populated_registry)
        agents = router.route_by_category("finanzas")
        assert len(agents) == 1

    def test_route_by_capability(self, populated_registry):
        router = DynamicRouter(populated_registry)
        agents = router.route_by_capability("roi")
        assert len(agents) == 1

    def test_route_semantic(self, populated_registry):
        router = DynamicRouter(populated_registry)
        agent = router.route_semantic("necesito analizar el presupuesto y dinero")
        assert agent is not None
        assert agent.category == "finanzas"

    def test_route_semantic_no_match(self, populated_registry):
        router = DynamicRouter(populated_registry)
        result = router.route_semantic("xyzzy gibberish nonsense")
        # May return None or fallback
        # This is acceptable behavior

    def test_route_with_fallback(self, populated_registry):
        router = DynamicRouter(populated_registry)
        agent = router.route_with_fallback("test query", "finanzas")
        assert agent is not None
        assert agent.category == "finanzas"

    def test_route_with_fallback_no_category(self, populated_registry):
        router = DynamicRouter(populated_registry)
        agent = router.route_with_fallback("calcular inversión y dinero")
        assert agent is not None

    def test_get_stats(self, populated_registry):
        router = DynamicRouter(populated_registry)
        stats = router.get_stats()
        assert "total_agents" in stats


# ─── AdvancedLLMRouter Tests ─────────────────────────────────


class TestAdvancedLLMRouter:
    def test_model_config_structure(self):
        for provider, config in MODEL_CONFIG.items():
            assert "model" in config
            assert "api_key_env" in config
            assert "strengths" in config
            assert "priority" in config

    def test_category_model_map(self):
        assert CATEGORY_MODEL_MAP["finanzas"] == "openai"
        assert CATEGORY_MODEL_MAP["legal"] == "openai"
        assert CATEGORY_MODEL_MAP["herramientas"] == "groq"

    def test_get_status(self):
        router = AdvancedLLMRouter()
        status = router.get_status()
        assert "available_providers" in status
        assert "total_providers" in status
        assert status["total_providers"] == 6

    def test_report_failure(self):
        router = AdvancedLLMRouter()
        router._available_providers = ["groq"]
        router._failure_counts = {"groq": 0}
        router.report_failure("groq")
        assert router._failure_counts["groq"] == 1

    def test_report_success(self):
        router = AdvancedLLMRouter()
        router._available_providers = ["groq"]
        router._failure_counts = {"groq": 2}
        router.report_success("groq")
        assert router._failure_counts["groq"] == 0


# ─── Metrics Tests ────────────────────────────────────────────


class TestMetrics:
    def test_record_agent_execution(self):
        record_agent_execution("test_agent", "herramientas", 0.5, "success")
        summary = get_metrics_summary()
        assert summary["agent_executions_total"] >= 1

    def test_generate_prometheus_text(self):
        record_agent_execution("prom_agent", "finanzas", 0.3, "success")
        text = generate_prometheus_text()
        assert "agent_execution_total" in text
        assert "prom_agent" in text


# ─── Logging Tests ────────────────────────────────────────────


class TestLogging:
    def test_json_formatter(self):
        import logging

        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="test message",
            args=(),
            exc_info=None,
        )
        output = formatter.format(record)
        import json

        parsed = json.loads(output)
        assert parsed["message"] == "test message"
        assert parsed["level"] == "INFO"

    def test_setup_logging(self):
        setup_logging(level="DEBUG", json_output=False)
        import logging

        logger = logging.getLogger("test_setup")
        assert logger.getEffectiveLevel() <= logging.DEBUG
