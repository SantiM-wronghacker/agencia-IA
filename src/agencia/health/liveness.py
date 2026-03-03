"""
Liveness probe — answers the question *"Is the service process running?"*

A liveness check should be cheap: if it fails, the orchestrator (e.g.
Kubernetes) will restart the container.
"""

import time
from typing import Any


class LivenessProbe:
    """Simple liveness probe.

    Succeeds as long as the Python process is responsive.
    """

    def __init__(self) -> None:
        self._started_at = time.time()

    def check(self) -> dict[str, Any]:
        """Return a liveness response."""
        return {
            "status": "alive",
            "uptime_seconds": round(time.time() - self._started_at, 2),
        }
