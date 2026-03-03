"""
Agencia IA - Orchestrator

Coordinates multi-agent workflows, handling task distribution,
dependency resolution, and result aggregation.
"""

import logging
import time
from typing import Any, Optional

from src.agencia.core.agent_registry import AgentRegistry
from src.agencia.core.router import DynamicRouter

logger = logging.getLogger("agencia.orchestrator")


class Orchestrator:
    """Orchestrates multi-agent task execution."""

    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        self.router = DynamicRouter(registry)
        self._task_history: list[dict[str, Any]] = []

    def execute_task(
        self,
        query: str,
        category: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Execute a task by routing to the appropriate agent."""
        start = time.monotonic()

        agent_record = self.router.route_with_fallback(query, category)
        if not agent_record:
            return {
                "status": "error",
                "error": "No suitable agent found",
                "query": query,
            }

        if agent_record.instance is None:
            return {
                "status": "error",
                "error": f"Agent '{agent_record.name}' has no running instance",
                "agent": agent_record.name,
            }

        try:
            input_data = {"query": query, "context": context or {}}
            result = agent_record.instance.run(input_data)
            duration_ms = (time.monotonic() - start) * 1000

            self.registry.log_execution(
                agent_name=agent_record.name,
                duration_ms=duration_ms,
                status="success",
                model_used=agent_record.preferred_model,
            )

            task_record = {
                "query": query,
                "agent": agent_record.name,
                "category": agent_record.category,
                "duration_ms": round(duration_ms, 2),
                "status": "success",
                "timestamp": time.time(),
            }
            self._task_history.append(task_record)

            return {
                "status": "success",
                "agent": agent_record.name,
                "category": agent_record.category,
                "result": result,
                "duration_ms": round(duration_ms, 2),
            }

        except Exception as exc:
            duration_ms = (time.monotonic() - start) * 1000

            self.registry.log_execution(
                agent_name=agent_record.name,
                duration_ms=duration_ms,
                status="error",
                error_message=str(exc),
            )

            logger.error(
                "task_execution_error",
                extra={
                    "agent": agent_record.name,
                    "error": str(exc),
                },
            )

            return {
                "status": "error",
                "agent": agent_record.name,
                "error": str(exc),
                "duration_ms": round(duration_ms, 2),
            }

    def execute_pipeline(
        self, tasks: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Execute a pipeline of sequential tasks."""
        results: list[dict[str, Any]] = []
        context: dict[str, Any] = {}

        for task in tasks:
            query = task.get("query", "")
            category = task.get("category")

            result = self.execute_task(query, category, context)
            results.append(result)

            if result["status"] == "success":
                context[f"step_{len(results)}"] = result.get("result", {})

        return results

    def get_task_history(self) -> list[dict[str, Any]]:
        """Return task execution history."""
        return self._task_history

    def get_stats(self) -> dict[str, Any]:
        """Get orchestrator stats."""
        total = len(self._task_history)
        successes = len(
            [t for t in self._task_history if t["status"] == "success"]
        )
        return {
            "total_tasks": total,
            "successful": successes,
            "failed": total - successes,
            "success_rate": (
                round(successes / total * 100, 2) if total > 0 else 100.0
            ),
            "registry": self.registry.get_health_summary(),
        }
