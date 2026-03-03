"""
Agencia IA - Test Configuration (conftest.py)

Shared fixtures for all tests.
"""

import sys
import os
import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture
def sample_agent():
    """Create a sample agent for testing."""
    from src.agencia.core.base_agent import BaseAgent

    class SampleAgent(BaseAgent):
        def execute(self, input_data):
            return {"result": f"Processed: {input_data.get('query', '')}"}

        def get_capabilities(self):
            return ["testing", "sample"]

    return SampleAgent(
        name="test_agent",
        category="herramientas",
        description="A test agent",
        version="1.0.0",
        preferred_model="groq",
    )


@pytest.fixture
def registry():
    """Create a fresh AgentRegistry for testing."""
    from src.agencia.core.agent_registry import AgentRegistry

    return AgentRegistry()


@pytest.fixture
def populated_registry(registry, sample_agent):
    """Create a registry with some agents registered."""
    registry.register(
        name="agent_finanzas_1",
        category="finanzas",
        capabilities=["roi", "analysis"],
        description="Financial analyzer",
    )
    registry.register(
        name="agent_legal_1",
        category="legal",
        capabilities=["contracts", "compliance"],
        description="Legal agent",
    )
    registry.register(
        name="agent_ventas_1",
        category="ventas",
        capabilities=["leads", "pipeline"],
        description="Sales agent",
    )
    registry.register(
        name="agent_herramientas_1",
        category="herramientas",
        capabilities=["testing", "sample"],
        description="Tool agent",
        instance=sample_agent,
    )
    return registry
