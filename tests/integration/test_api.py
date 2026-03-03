"""
Agencia IA - Integration Tests

Tests for API endpoints and service interactions.
"""

import pytest
from src.agencia.core.agent_registry import AgentRegistry
from src.agencia.core.orchestrator import Orchestrator
from src.agencia.core.base_agent import BaseAgent


class EchoAgent(BaseAgent):
    """Simple agent that echoes input for integration testing."""

    def execute(self, input_data):
        return {"echo": input_data.get("query", ""), "agent": self.name}


class TestOrchestratorIntegration:
    def test_execute_task_no_agents(self):
        registry = AgentRegistry()
        orchestrator = Orchestrator(registry)
        result = orchestrator.execute_task("test query")
        assert result["status"] == "error"
        assert "No suitable agent" in result["error"]

    def test_execute_task_with_agent(self):
        registry = AgentRegistry()
        agent = EchoAgent(
            name="echo", category="herramientas", description="Echo agent"
        )
        registry.register(
            name="echo",
            category="herramientas",
            capabilities=["herramienta", "generador"],
            instance=agent,
        )

        orchestrator = Orchestrator(registry)
        result = orchestrator.execute_task(
            "necesito una herramienta generador", category="herramientas"
        )
        assert result["status"] == "success"
        assert result["agent"] == "echo"

    def test_execute_pipeline(self):
        registry = AgentRegistry()
        agent = EchoAgent(
            name="pipeline_agent",
            category="herramientas",
            description="Pipeline test",
        )
        registry.register(
            name="pipeline_agent",
            category="herramientas",
            capabilities=["herramienta"],
            instance=agent,
        )

        orchestrator = Orchestrator(registry)
        tasks = [
            {"query": "herramienta paso 1", "category": "herramientas"},
            {"query": "herramienta paso 2", "category": "herramientas"},
        ]
        results = orchestrator.execute_pipeline(tasks)
        assert len(results) == 2
        assert all(r["status"] == "success" for r in results)

    def test_orchestrator_stats(self):
        registry = AgentRegistry()
        orchestrator = Orchestrator(registry)
        stats = orchestrator.get_stats()
        assert "total_tasks" in stats
        assert "registry" in stats
