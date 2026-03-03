"""
Agencia IA - Core Module

Provides base classes and utilities for the agent system.
"""

from src.agencia.core.base_agent import BaseAgent
from src.agencia.core.agent_registry import AgentRegistry
from src.agencia.core.router import DynamicRouter
from src.agencia.core.orchestrator import Orchestrator

__all__ = ["BaseAgent", "AgentRegistry", "DynamicRouter", "Orchestrator"]
