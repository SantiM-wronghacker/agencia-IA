"""
Individual health-check functions for external dependencies.

Each function returns a dict ``{"status": "healthy"|"unhealthy", "details": ...}``.
Thresholds are configurable via environment variables.
"""

import os
import shutil
import socket
import urllib.request
import urllib.error
from typing import Any


def _tcp_check(host: str, port: int, timeout: float = 2.0) -> bool:
    """Return ``True`` if a TCP connection to *host*:*port* succeeds."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, ConnectionRefusedError):
        return False


def _http_check(url: str, timeout: float = 3.0) -> bool:
    """Return ``True`` if a GET request to *url* returns 2xx."""
    try:
        resp = urllib.request.urlopen(url, timeout=timeout)
        return 200 <= resp.status < 300
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------


def check_database() -> dict[str, Any]:
    """Check PostgreSQL connectivity."""
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = int(os.getenv("POSTGRES_PORT", "5432"))
    ok = _tcp_check(host, port)
    return {
        "status": "healthy" if ok else "unhealthy",
        "service": "postgresql",
        "host": host,
        "port": port,
    }


# ---------------------------------------------------------------------------
# Redis
# ---------------------------------------------------------------------------


def check_redis() -> dict[str, Any]:
    """Check Redis connectivity."""
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    ok = _tcp_check(host, port)
    return {
        "status": "healthy" if ok else "unhealthy",
        "service": "redis",
        "host": host,
        "port": port,
    }


# ---------------------------------------------------------------------------
# Elasticsearch
# ---------------------------------------------------------------------------


def check_elasticsearch() -> dict[str, Any]:
    """Check Elasticsearch connectivity via its cluster health API."""
    url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    ok = _http_check(f"{url}/_cluster/health")
    return {
        "status": "healthy" if ok else "unhealthy",
        "service": "elasticsearch",
        "url": url,
    }


# ---------------------------------------------------------------------------
# LLM Providers
# ---------------------------------------------------------------------------


def check_llm_providers() -> dict[str, Any]:
    """Check connectivity to configured LLM providers (Groq, Cerebras, etc.)."""
    results: dict[str, str] = {}
    groq_key = os.getenv("GROQ_API_KEY", "")
    if groq_key and not groq_key.startswith("gsk_configurar"):
        results["groq"] = "configured"
    else:
        results["groq"] = "not_configured"

    cerebras_key = os.getenv("CEREBRAS_API_KEY", "")
    results["cerebras"] = "configured" if cerebras_key else "not_configured"

    any_ok = any(v == "configured" for v in results.values())
    return {
        "status": "healthy" if any_ok else "unhealthy",
        "service": "llm_providers",
        "providers": results,
    }


# ---------------------------------------------------------------------------
# Disk space
# ---------------------------------------------------------------------------


def check_disk_space() -> dict[str, Any]:
    """Check available disk space on the root (or project) partition."""
    threshold_mb = int(os.getenv("DISK_SPACE_THRESHOLD_MB", "500"))
    usage = shutil.disk_usage("/")
    free_mb = usage.free // (1024 * 1024)
    return {
        "status": "healthy" if free_mb >= threshold_mb else "unhealthy",
        "service": "disk_space",
        "free_mb": free_mb,
        "threshold_mb": threshold_mb,
    }


# ---------------------------------------------------------------------------
# Memory
# ---------------------------------------------------------------------------


def check_memory() -> dict[str, Any]:
    """Check available system memory.

    Falls back to a simple ``/proc/meminfo`` read on Linux; returns unknown
    on unsupported platforms.
    """
    threshold_mb = int(os.getenv("MEMORY_THRESHOLD_MB", "256"))
    try:
        with open("/proc/meminfo") as fh:
            for line in fh:
                if line.startswith("MemAvailable:"):
                    avail_kb = int(line.split()[1])
                    avail_mb = avail_kb // 1024
                    return {
                        "status": "healthy" if avail_mb >= threshold_mb else "unhealthy",
                        "service": "memory",
                        "available_mb": avail_mb,
                        "threshold_mb": threshold_mb,
                    }
    except FileNotFoundError:
        pass
    return {
        "status": "unknown",
        "service": "memory",
        "detail": "/proc/meminfo not available",
    }


# ---------------------------------------------------------------------------
# Queue depth
# ---------------------------------------------------------------------------


def check_queue_depth() -> dict[str, Any]:
    """Check the RabbitMQ management API for queue depth."""
    host = os.getenv("RABBITMQ_HOST", "localhost")
    port = int(os.getenv("RABBITMQ_MANAGEMENT_PORT", "15672"))
    threshold = int(os.getenv("QUEUE_DEPTH_THRESHOLD", "1000"))
    url = f"http://{host}:{port}/api/queues"
    ok = _http_check(url)
    return {
        "status": "healthy" if ok else "unhealthy",
        "service": "rabbitmq",
        "host": host,
        "port": port,
        "threshold": threshold,
    }
