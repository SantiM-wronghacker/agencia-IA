"""Distributed tracing integration (Jaeger-compatible)."""

from src.agencia.tracing.jaeger_config import JaegerConfig, initialize_tracer
from src.agencia.tracing.decorators import trace_span, trace_agent_execution

__all__ = [
    "JaegerConfig",
    "initialize_tracer",
    "trace_span",
    "trace_agent_execution",
]
