"""
Agencia IA - End-to-End Tests

Tests for complete workflow scenarios.
"""

import pytest
from src.agencia.core.agent_registry import AgentRegistry
from src.agencia.core.router import DynamicRouter
from src.agencia.core.orchestrator import Orchestrator
from src.agencia.core.base_agent import BaseAgent
from src.agencia.core.llm_router_mejorado import AdvancedLLMRouter, CATEGORY_MODEL_MAP


class FinanceAgent(BaseAgent):
    def execute(self, input_data):
        return {"analysis": "ROI is 15%", "agent": self.name}


class LegalAgent(BaseAgent):
    def execute(self, input_data):
        return {"review": "Contract is valid", "agent": self.name}


class TestEndToEndWorkflows:
    def setup_method(self):
        """Set up a registry with multiple agents for e2e testing."""
        self.registry = AgentRegistry()

        self.finance_agent = FinanceAgent(
            name="finance_analyzer",
            category="finanzas",
            preferred_model="openai",
        )
        self.legal_agent = LegalAgent(
            name="legal_reviewer",
            category="legal",
            preferred_model="openai",
        )

        self.registry.register(
            name="finance_analyzer",
            category="finanzas",
            capabilities=["roi", "investment", "analysis", "dinero"],
            instance=self.finance_agent,
        )
        self.registry.register(
            name="legal_reviewer",
            category="legal",
            capabilities=["contract", "compliance", "legal"],
            instance=self.legal_agent,
        )

    def test_full_workflow_finance(self):
        orchestrator = Orchestrator(self.registry)
        result = orchestrator.execute_task(
            "Analizar inversión y dinero", category="finanzas"
        )
        assert result["status"] == "success"
        assert result["agent"] == "finance_analyzer"
        assert "ROI" in result["result"]["analysis"]

    def test_full_workflow_legal(self):
        orchestrator = Orchestrator(self.registry)
        result = orchestrator.execute_task(
            "Revisar contrato legal", category="legal"
        )
        assert result["status"] == "success"
        assert result["agent"] == "legal_reviewer"

    def test_semantic_routing_workflow(self):
        router = DynamicRouter(self.registry)
        agent = router.route_semantic("necesito calcular el ROI de mi inversión y dinero")
        assert agent is not None
        assert agent.category == "finanzas"

    def test_multi_step_pipeline(self):
        orchestrator = Orchestrator(self.registry)
        tasks = [
            {"query": "analizar inversión y dinero", "category": "finanzas"},
            {"query": "revisar contrato legal", "category": "legal"},
        ]
        results = orchestrator.execute_pipeline(tasks)
        assert len(results) == 2
        assert results[0]["status"] == "success"
        assert results[1]["status"] == "success"

    def test_llm_router_model_selection(self):
        assert CATEGORY_MODEL_MAP["finanzas"] == "openai"
        assert CATEGORY_MODEL_MAP["legal"] == "openai"

    def test_health_summary_after_workflow(self):
        orchestrator = Orchestrator(self.registry)
        orchestrator.execute_task("test dinero", category="finanzas")
        stats = orchestrator.get_stats()
        assert stats["total_tasks"] >= 1
        assert stats["successful"] >= 1
