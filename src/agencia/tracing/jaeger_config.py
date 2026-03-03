"""
Jaeger tracing configuration for the agencia-IA system.

Provides a lightweight tracing abstraction that can ship spans to Jaeger
via the Thrift-over-HTTP collector endpoint.
"""

import os
import json
import time
import uuid
import threading
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class JaegerConfig:
    """Configuration for the Jaeger tracing backend."""

    service_name: str = os.getenv("JAEGER_SERVICE_NAME", "agencia-ia")
    agent_host: str = os.getenv("JAEGER_AGENT_HOST", "localhost")
    agent_port: int = int(os.getenv("JAEGER_AGENT_PORT", "6831"))
    collector_endpoint: str = os.getenv(
        "JAEGER_COLLECTOR_ENDPOINT", "http://localhost:14268/api/traces"
    )
    enabled: bool = os.getenv("JAEGER_ENABLED", "false").lower() in ("1", "true", "yes")
    sample_rate: float = float(os.getenv("JAEGER_SAMPLE_RATE", "1.0"))


# ---------------------------------------------------------------------------
# Lightweight span representation
# ---------------------------------------------------------------------------


@dataclass
class Span:
    """A single trace span."""

    operation_name: str
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    parent_span_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    tags: dict[str, Any] = field(default_factory=dict)
    logs: list[dict[str, Any]] = field(default_factory=list)

    def finish(self) -> None:
        self.end_time = time.time()

    def set_tag(self, key: str, value: Any) -> "Span":
        self.tags[key] = value
        return self

    def log_kv(self, kv: dict[str, Any]) -> "Span":
        self.logs.append({"timestamp": time.time(), **kv})
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_name": self.operation_name,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": (
                round((self.end_time - self.start_time) * 1000, 2) if self.end_time else None
            ),
            "tags": self.tags,
            "logs": self.logs,
        }


# ---------------------------------------------------------------------------
# Tracer
# ---------------------------------------------------------------------------

_current_span: threading.local = threading.local()


class Tracer:
    """A very small tracer that records spans and optionally ships them."""

    def __init__(self, config: Optional[JaegerConfig] = None) -> None:
        self.config = config or JaegerConfig()
        self.spans: list[Span] = []
        self._lock = threading.Lock()

    def start_span(
        self, operation_name: str, parent: Optional[Span] = None
    ) -> Span:
        span = Span(
            operation_name=operation_name,
            trace_id=parent.trace_id if parent else uuid.uuid4().hex,
            parent_span_id=parent.span_id if parent else None,
        )
        span.set_tag("service", self.config.service_name)
        _current_span.span = span
        return span

    def finish_span(self, span: Span) -> None:
        span.finish()
        with self._lock:
            self.spans.append(span)
        if self.config.enabled:
            self._report(span)

    @staticmethod
    def active_span() -> Optional[Span]:
        return getattr(_current_span, "span", None)

    def _report(self, span: Span) -> None:
        """Best-effort send to the Jaeger collector."""
        try:
            payload = json.dumps(span.to_dict()).encode("utf-8")
            req = urllib.request.Request(
                self.config.collector_endpoint,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            pass  # tracing must never break the application


# Module-level singleton
_tracer: Optional[Tracer] = None


def initialize_tracer(config: Optional[JaegerConfig] = None) -> Tracer:
    """Create (or return) the global tracer instance."""
    global _tracer
    if _tracer is None:
        _tracer = Tracer(config)
    return _tracer


def get_tracer() -> Tracer:
    """Return the global tracer, initialising with defaults if necessary."""
    return initialize_tracer()
