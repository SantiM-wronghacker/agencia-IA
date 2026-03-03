"""Prometheus metrics and monitoring for the agencia-IA system."""

from src.agencia.monitoring.metrics import (
    task_counter,
    task_duration_histogram,
    agent_execution_counter,
    router_decision_histogram,
    llm_provider_counter,
    cache_hit_ratio,
    memory_usage_gauge,
    queue_depth_gauge,
    error_rate_counter,
)
from src.agencia.monitoring.decorators import (
    track_execution,
    track_performance,
    track_errors,
)

__all__ = [
    "task_counter",
    "task_duration_histogram",
    "agent_execution_counter",
    "router_decision_histogram",
    "llm_provider_counter",
    "cache_hit_ratio",
    "memory_usage_gauge",
    "queue_depth_gauge",
    "error_rate_counter",
    "track_execution",
    "track_performance",
    "track_errors",
]
