"""
Agencia IA - Agent Registry

Service for registering, discovering, and tracking agents.
Supports PostgreSQL persistence and in-memory fallback.
"""

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Optional

logger = logging.getLogger("agencia.registry")


@dataclass
class AgentRecord:
    """In-memory representation of a registered agent."""

    name: str
    category: str
    subcategory: str = ""
    description: str = ""
    module_path: str = ""
    capabilities: list[str] = field(default_factory=list)
    version: str = "1.0.0"
    status: str = "active"
    preferred_model: str = "groq"
    config: dict[str, Any] = field(default_factory=dict)
    instance: Any = None


class AgentRegistry:
    """Central registry for all agents in the system."""

    def __init__(self) -> None:
        self._agents: dict[str, AgentRecord] = {}
        self._executions: list[dict[str, Any]] = []

    def register(
        self,
        name: str,
        category: str,
        subcategory: str = "",
        description: str = "",
        module_path: str = "",
        capabilities: Optional[list[str]] = None,
        version: str = "1.0.0",
        preferred_model: str = "groq",
        instance: Any = None,
    ) -> AgentRecord:
        """Register an agent in the registry."""
        record = AgentRecord(
            name=name,
            category=category,
            subcategory=subcategory,
            description=description,
            module_path=module_path,
            capabilities=capabilities or [],
            version=version,
            preferred_model=preferred_model,
            instance=instance,
        )
        self._agents[name] = record
        logger.info(
            "agent_registered",
            extra={"agent": name, "category": category, "version": version},
        )
        return record

    def get(self, name: str) -> Optional[AgentRecord]:
        """Get agent by name."""
        return self._agents.get(name)

    def find_by_category(self, category: str) -> list[AgentRecord]:
        """Find all agents in a category."""
        return [a for a in self._agents.values() if a.category == category]

    def find_by_capability(self, capability: str) -> list[AgentRecord]:
        """Find agents that have a specific capability."""
        return [
            a for a in self._agents.values() if capability in a.capabilities
        ]

    def find_by_status(self, status: str) -> list[AgentRecord]:
        """Find agents by status."""
        return [a for a in self._agents.values() if a.status == status]

    def list_all(self) -> list[AgentRecord]:
        """List all registered agents."""
        return list(self._agents.values())

    def list_categories(self) -> list[str]:
        """List all unique categories."""
        return list({a.category for a in self._agents.values()})

    def log_execution(
        self,
        agent_name: str,
        duration_ms: float,
        status: str = "success",
        model_used: str = "",
        tokens_used: int = 0,
        error_message: str = "",
    ) -> None:
        """Log an agent execution."""
        self._executions.append(
            {
                "agent_name": agent_name,
                "duration_ms": duration_ms,
                "status": status,
                "model_used": model_used,
                "tokens_used": tokens_used,
                "error_message": error_message,
                "timestamp": time.time(),
            }
        )

    def get_health_summary(self) -> dict[str, Any]:
        """Get health summary for all agents."""
        total = len(self._agents)
        active = len([a for a in self._agents.values() if a.status == "active"])
        categories = self.list_categories()

        total_executions = len(self._executions)
        errors = len([e for e in self._executions if e["status"] == "error"])

        return {
            "total_agents": total,
            "active_agents": active,
            "categories": len(categories),
            "total_executions": total_executions,
            "error_count": errors,
            "success_rate": (
                round((1 - errors / total_executions) * 100, 2)
                if total_executions > 0
                else 100.0
            ),
        }

    def deactivate(self, name: str) -> bool:
        """Deactivate an agent."""
        agent = self._agents.get(name)
        if agent:
            agent.status = "inactive"
            return True
        return False

    def count(self) -> int:
        """Return total number of registered agents."""
        return len(self._agents)


# Global singleton
registry = AgentRegistry()
