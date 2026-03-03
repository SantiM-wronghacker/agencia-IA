"""
Tracing decorators for automatic span creation around function calls.
"""

import functools
from typing import Any, Optional

from src.agencia.tracing.jaeger_config import get_tracer, Span


def trace_span(operation_name: Optional[str] = None):
    """Create a Jaeger span wrapping the decorated function.

    If *operation_name* is ``None`` the function's qualified name is used.
    """

    def decorator(func):
        _op = operation_name or func.__qualname__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            parent = tracer.active_span()
            span = tracer.start_span(_op, parent=parent)
            try:
                result = func(*args, **kwargs)
                span.set_tag("status", "ok")
                return result
            except Exception as exc:
                span.set_tag("status", "error")
                span.set_tag("error.type", type(exc).__name__)
                span.log_kv({"event": "error", "message": str(exc)})
                raise
            finally:
                tracer.finish_span(span)

        return wrapper

    return decorator


def trace_agent_execution(category: str = "default", agent: str = "unknown"):
    """Like ``trace_span`` but adds agent-specific tags."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            parent = tracer.active_span()
            span = tracer.start_span(f"agent.{agent}", parent=parent)
            span.set_tag("agent.category", category)
            span.set_tag("agent.name", agent)
            try:
                result = func(*args, **kwargs)
                span.set_tag("status", "ok")
                return result
            except Exception as exc:
                span.set_tag("status", "error")
                span.set_tag("error.type", type(exc).__name__)
                span.log_kv({"event": "error", "message": str(exc)})
                raise
            finally:
                tracer.finish_span(span)

        return wrapper

    return decorator
