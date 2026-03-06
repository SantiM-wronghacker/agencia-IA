"""Integration tests: validate docker-compose.yml configuration."""

import pytest
import yaml
from pathlib import Path

COMPOSE_FILE = Path(__file__).resolve().parent.parent.parent / "docker-compose.yml"


@pytest.fixture(scope="module")
def compose():
    assert COMPOSE_FILE.exists(), f"docker-compose.yml not found at {COMPOSE_FILE}"
    with open(COMPOSE_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_compose_has_services(compose):
    assert "services" in compose
    assert len(compose["services"]) >= 5


def test_agencia_api_service(compose):
    api = compose["services"].get("agencia-api")
    assert api is not None, "agencia-api service not found"
    assert "8000:8000" in api.get("ports", [])
    assert "healthcheck" in api


def test_elasticsearch_service(compose):
    es = compose["services"].get("elasticsearch")
    assert es is not None
    assert "9200:9200" in es.get("ports", [])


def test_jaeger_healthcheck_port(compose):
    """Jaeger health check must target port 16686 (UI port), not 16687."""
    jaeger = compose["services"].get("jaeger")
    assert jaeger is not None
    hc = jaeger.get("healthcheck", {})
    test_cmd = " ".join(hc.get("test", []))
    assert "16686" in test_cmd, f"Jaeger health check should use port 16686, got: {test_cmd}"
    assert "16687" not in test_cmd, "Jaeger health check should NOT use port 16687"


def test_redis_service(compose):
    redis = compose["services"].get("redis")
    assert redis is not None
    assert "6379:6379" in redis.get("ports", [])


def test_all_services_have_healthchecks(compose):
    """Every service should define a healthcheck."""
    for name, svc in compose["services"].items():
        if name == "agencia-api":
            continue  # API healthcheck depends on build
        assert "healthcheck" in svc, f"Service '{name}' is missing a healthcheck"


def test_networks_defined(compose):
    assert "networks" in compose
    assert "agencia-net" in compose["networks"]


def test_volumes_defined(compose):
    assert "volumes" in compose
    expected = {"es-data", "prom-data", "grafana-data"}
    assert expected.issubset(set(compose["volumes"].keys()))
