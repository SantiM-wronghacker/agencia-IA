"""Integration tests for Prometheus metrics."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.agencia.api.health import router
from src.agencia.monitoring.metrics import (
    task_counter,
    task_duration_histogram,
    agent_execution_counter,
    error_rate_counter,
    generate_metrics_text,
)


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_metrics_endpoint(client):
    """GET /metrics returns Prometheus text format."""
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "text/plain" in r.headers["content-type"]
    assert "agencia_tasks_total" in r.text


def test_task_counter_records():
    """Incrementing task_counter should be reflected in text output."""
    task_counter.labels(status="test_success").inc()
    text = generate_metrics_text()
    assert 'agencia_tasks_total{status="test_success"}' in text


def test_histogram_records():
    """Observing a histogram should produce sum and count."""
    task_duration_histogram.labels(task_type="test_op").observe(0.42)
    text = generate_metrics_text()
    assert "agencia_task_duration_seconds_sum" in text
    assert "agencia_task_duration_seconds_count" in text


def test_agent_execution_counter():
    agent_execution_counter.labels(category="test_cat", agent="test_agent").inc()
    text = generate_metrics_text()
    assert 'agencia_agent_executions_total{category="test_cat",agent="test_agent"}' in text


def test_error_rate_counter():
    error_rate_counter.labels(error_type="ValueError", agent="test_agent").inc()
    text = generate_metrics_text()
    assert 'agencia_errors_total{error_type="ValueError",agent="test_agent"}' in text


def test_metrics_text_format():
    """Metrics output must contain HELP and TYPE lines."""
    text = generate_metrics_text()
    assert "# HELP agencia_tasks_total" in text
    assert "# TYPE agencia_tasks_total counter" in text
    assert "# TYPE agencia_task_duration_seconds histogram" in text
    assert "# TYPE agencia_memory_usage_bytes gauge" in text
