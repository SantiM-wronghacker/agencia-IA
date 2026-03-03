"""
Readiness probe — answers *"Is the service ready to accept traffic?"*

Unlike liveness, readiness runs all critical dependency checks. If readiness
fails the load balancer should stop sending traffic but the container should
**not** be restarted.
"""

from typing import Any

from src.agencia.health.checks import (
    check_disk_space,
    check_memory,
    check_llm_providers,
)


class ReadinessProbe:
    """Readiness probe that aggregates critical dependency checks."""

    def __init__(self, checks=None) -> None:
        self._checks = checks or [
            check_disk_space,
            check_memory,
            check_llm_providers,
        ]

    def check(self) -> dict[str, Any]:
        results = {}
        overall = "ready"
        for fn in self._checks:
            result = fn()
            service = result.get("service", fn.__name__)
            results[service] = result
            if result.get("status") == "unhealthy":
                overall = "not_ready"
        return {"status": overall, "checks": results}
