"""
Agencia IA - Prometheus Metrics

Defines metrics for monitoring agent execution, API latency,
database connections, and system health.
"""

import time
from typing import Any

# Metrics storage (compatible with prometheus_client when available)
_metrics: dict[str, Any] = {
    "agent_execution_total": {},
    "agent_execution_duration_seconds": {},
    "agent_errors_total": {},
    "api_request_total": {},
    "api_request_duration_seconds": {},
    "db_connections_active": 0,
    "system_memory_bytes": 0,
}


def record_agent_execution(
    agent_name: str, category: str, duration_seconds: float, status: str
) -> None:
    """Record an agent execution metric."""
    key = f"{agent_name}:{category}"
    _metrics["agent_execution_total"][key] = (
        _metrics["agent_execution_total"].get(key, 0) + 1
    )
    _metrics["agent_execution_duration_seconds"][key] = duration_seconds
    if status == "error":
        _metrics["agent_errors_total"][key] = (
            _metrics["agent_errors_total"].get(key, 0) + 1
        )


def record_api_request(
    endpoint: str, method: str, duration_seconds: float, status_code: int
) -> None:
    """Record an API request metric."""
    key = f"{method}:{endpoint}:{status_code}"
    _metrics["api_request_total"][key] = (
        _metrics["api_request_total"].get(key, 0) + 1
    )
    _metrics["api_request_duration_seconds"][key] = duration_seconds


def set_db_connections(count: int) -> None:
    """Set the current number of active database connections."""
    _metrics["db_connections_active"] = count


def set_memory_usage(bytes_used: int) -> None:
    """Set current memory usage."""
    _metrics["system_memory_bytes"] = bytes_used


def get_metrics_summary() -> dict[str, Any]:
    """Get a summary of all metrics."""
    total_executions = sum(_metrics["agent_execution_total"].values())
    total_errors = sum(_metrics["agent_errors_total"].values())
    total_requests = sum(_metrics["api_request_total"].values())

    return {
        "agent_executions_total": total_executions,
        "agent_errors_total": total_errors,
        "agent_success_rate": (
            round((1 - total_errors / total_executions) * 100, 2)
            if total_executions > 0
            else 100.0
        ),
        "api_requests_total": total_requests,
        "db_connections_active": _metrics["db_connections_active"],
        "system_memory_bytes": _metrics["system_memory_bytes"],
    }


def generate_prometheus_text() -> str:
    """Generate Prometheus text exposition format."""
    lines: list[str] = []

    lines.append("# HELP agent_execution_total Total agent executions")
    lines.append("# TYPE agent_execution_total counter")
    for key, value in _metrics["agent_execution_total"].items():
        agent, category = key.split(":", 1)
        lines.append(
            f'agent_execution_total{{agent="{agent}",category="{category}"}} {value}'
        )

    lines.append("# HELP agent_errors_total Total agent errors")
    lines.append("# TYPE agent_errors_total counter")
    for key, value in _metrics["agent_errors_total"].items():
        agent, category = key.split(":", 1)
        lines.append(
            f'agent_errors_total{{agent="{agent}",category="{category}"}} {value}'
        )

    lines.append("# HELP db_connections_active Active database connections")
    lines.append("# TYPE db_connections_active gauge")
    lines.append(
        f'db_connections_active {_metrics["db_connections_active"]}'
    )

    lines.append("# HELP system_memory_bytes System memory usage")
    lines.append("# TYPE system_memory_bytes gauge")
    lines.append(f'system_memory_bytes {_metrics["system_memory_bytes"]}')

    return "\n".join(lines) + "\n"
