"""
ASGI middleware for logging, metrics, tracing, and health-check interception.
"""

import time
import uuid
import logging
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.agencia.monitoring.metrics import (
    task_counter,
    task_duration_histogram,
    error_rate_counter,
)
from src.agencia.logging.json_logger import LogContext
from src.agencia.tracing.jaeger_config import get_tracer

logger = logging.getLogger("agencia.middleware")


# ---------------------------------------------------------------------------
# 1. LoggingMiddleware
# ---------------------------------------------------------------------------


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log every incoming HTTP request with method, path, status, and duration.

    Assigns a unique ``X-Request-ID`` header that propagates through the
    call stack via :class:`LogContext`.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("x-request-id", uuid.uuid4().hex)
        start = time.time()

        with LogContext(request_id=request_id):
            logger.info(
                "request_start method=%s path=%s",
                request.method,
                request.url.path,
            )
            response = await call_next(request)
            elapsed = time.time() - start
            logger.info(
                "request_end method=%s path=%s status=%s duration=%.4f",
                request.method,
                request.url.path,
                response.status_code,
                elapsed,
            )

        response.headers["X-Request-ID"] = request_id
        return response


# ---------------------------------------------------------------------------
# 2. MetricsMiddleware
# ---------------------------------------------------------------------------


class MetricsMiddleware(BaseHTTPMiddleware):
    """Record Prometheus metrics for every HTTP request."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.time()
        response = await call_next(request)
        elapsed = time.time() - start

        task_duration_histogram.labels(task_type="http_request").observe(elapsed)

        status_class = f"{response.status_code // 100}xx"
        task_counter.labels(status=status_class).inc()

        if response.status_code >= 400:
            error_rate_counter.labels(
                error_type=f"http_{response.status_code}", agent="api"
            ).inc()

        return response


# ---------------------------------------------------------------------------
# 3. TracingMiddleware
# ---------------------------------------------------------------------------


class TracingMiddleware(BaseHTTPMiddleware):
    """Create a Jaeger span for each HTTP request and propagate trace context."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        tracer = get_tracer()
        span = tracer.start_span(f"HTTP {request.method} {request.url.path}")
        span.set_tag("http.method", request.method)
        span.set_tag("http.url", str(request.url))

        try:
            response = await call_next(request)
            span.set_tag("http.status_code", response.status_code)
            span.set_tag("status", "ok" if response.status_code < 400 else "error")
            return response
        except Exception as exc:
            span.set_tag("status", "error")
            span.set_tag("error.type", type(exc).__name__)
            span.log_kv({"event": "error", "message": str(exc)})
            raise
        finally:
            tracer.finish_span(span)


# ---------------------------------------------------------------------------
# 4. HealthCheckMiddleware
# ---------------------------------------------------------------------------


class HealthCheckMiddleware(BaseHTTPMiddleware):
    """Fast-path interception for ``/health/*`` requests.

    This middleware is intentionally a no-op pass-through: the actual
    health-check endpoints are registered via the ``health`` router.
    The middleware exists as an extension point (e.g. to add caching or
    rate-limiting around health probes).
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        return await call_next(request)
