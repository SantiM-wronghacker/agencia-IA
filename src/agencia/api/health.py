"""
Health and metrics API endpoints.

Provides:
- GET /health/live       → LivenessProbe response
- GET /health/ready      → ReadinessProbe response
- GET /health/detailed   → Full health check results
- GET /health/services   → Status of all services (DB, Redis, ES, LLMs)
- GET /metrics           → Prometheus metrics (text format)
"""

from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from src.agencia.health.liveness import LivenessProbe
from src.agencia.health.readiness import ReadinessProbe
from src.agencia.health.checks import (
    check_database,
    check_redis,
    check_elasticsearch,
    check_llm_providers,
    check_disk_space,
    check_memory,
    check_queue_depth,
)
from src.agencia.monitoring.metrics import generate_metrics_text

router = APIRouter()

_liveness = LivenessProbe()
_readiness = ReadinessProbe()


@router.get("/health/live")
def health_live():
    """Liveness probe — is the service process running?"""
    return _liveness.check()


@router.get("/health/ready")
def health_ready():
    """Readiness probe — is the service ready to accept traffic?"""
    result = _readiness.check()
    return result


@router.get("/health/detailed")
def health_detailed():
    """Run every available health check and return the full results."""
    checks = {
        "database": check_database(),
        "redis": check_redis(),
        "elasticsearch": check_elasticsearch(),
        "llm_providers": check_llm_providers(),
        "disk_space": check_disk_space(),
        "memory": check_memory(),
        "queue_depth": check_queue_depth(),
    }
    all_healthy = all(
        c.get("status") in ("healthy", "unknown") for c in checks.values()
    )
    return {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
    }


@router.get("/health/services")
def health_services():
    """Return the status of all external services."""
    return {
        "database": check_database(),
        "redis": check_redis(),
        "elasticsearch": check_elasticsearch(),
        "llm_providers": check_llm_providers(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/metrics")
def metrics():
    """Prometheus text exposition endpoint."""
    return PlainTextResponse(
        content=generate_metrics_text(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
