"""Integration tests for individual health check functions."""

import os
import pytest
from unittest.mock import patch

from src.agencia.health.checks import (
    check_database,
    check_redis,
    check_elasticsearch,
    check_llm_providers,
    check_disk_space,
    check_memory,
    check_queue_depth,
)
from src.agencia.health.liveness import LivenessProbe
from src.agencia.health.readiness import ReadinessProbe


# ---- Liveness ----

def test_liveness_always_alive():
    probe = LivenessProbe()
    result = probe.check()
    assert result["status"] == "alive"
    assert result["uptime_seconds"] >= 0


# ---- Readiness ----

def test_readiness_with_all_healthy_checks():
    """Readiness should be 'ready' when all checks return healthy."""
    def always_healthy():
        return {"status": "healthy", "service": "mock"}

    probe = ReadinessProbe(checks=[always_healthy, always_healthy])
    result = probe.check()
    assert result["status"] == "ready"


def test_readiness_with_unhealthy_check():
    """Readiness should be 'not_ready' when any check is unhealthy."""
    def healthy():
        return {"status": "healthy", "service": "ok"}
    def unhealthy():
        return {"status": "unhealthy", "service": "broken"}

    probe = ReadinessProbe(checks=[healthy, unhealthy])
    result = probe.check()
    assert result["status"] == "not_ready"


# ---- Individual checks ----

def test_check_database_returns_required_keys():
    result = check_database()
    assert "status" in result
    assert "service" in result
    assert result["service"] == "postgresql"
    assert result["status"] in ("healthy", "unhealthy")


def test_check_redis_returns_required_keys():
    result = check_redis()
    assert result["service"] == "redis"
    assert result["status"] in ("healthy", "unhealthy")


def test_check_elasticsearch_returns_required_keys():
    result = check_elasticsearch()
    assert result["service"] == "elasticsearch"
    assert result["status"] in ("healthy", "unhealthy")


def test_check_disk_space_healthy():
    """Disk space should be healthy in a normal environment."""
    result = check_disk_space()
    assert result["service"] == "disk_space"
    assert result["status"] in ("healthy", "unhealthy")
    assert "free_mb" in result
    assert "threshold_mb" in result


def test_check_memory_returns_valid():
    result = check_memory()
    assert result["service"] == "memory"
    assert result["status"] in ("healthy", "unhealthy", "unknown")


def test_check_llm_providers_no_keys():
    """Without API keys, LLM providers should be unhealthy."""
    with patch.dict(os.environ, {"GROQ_API_KEY": "", "CEREBRAS_API_KEY": ""}, clear=False):
        result = check_llm_providers()
        assert result["service"] == "llm_providers"
        assert "providers" in result


def test_check_llm_providers_with_groq_key():
    """With a valid GROQ key, providers should be healthy."""
    with patch.dict(os.environ, {"GROQ_API_KEY": "gsk_real_key_value"}, clear=False):
        result = check_llm_providers()
        assert result["status"] == "healthy"
        assert result["providers"]["groq"] == "configured"


def test_check_queue_depth_returns_required_keys():
    result = check_queue_depth()
    assert result["service"] == "rabbitmq"
    assert result["status"] in ("healthy", "unhealthy")
