"""
JSON-formatted logger and Elasticsearch handler for the agencia-IA system.

All log records are emitted as single-line JSON objects suitable for
ingestion by Elasticsearch / Logstash / Filebeat.
"""

import json
import logging
import os
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Optional

import urllib.request
import urllib.error

# Context variable holding the current request ID.
_request_id_var: ContextVar[str] = ContextVar("request_id", default="")


# ---------------------------------------------------------------------------
# JSONFormatter
# ---------------------------------------------------------------------------


class JSONFormatter(logging.Formatter):
    """Format log records as JSON with timestamp, level, module, function, and line."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
            "logger": record.name,
        }

        # Attach extra fields added by filters or callers.
        for attr in ("request_id", "user_id", "tenant_id"):
            value = getattr(record, attr, None)
            if value:
                log_entry[attr] = value

        if record.exc_info and record.exc_info[1] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, default=str, ensure_ascii=False)


# ---------------------------------------------------------------------------
# ElasticsearchHandler
# ---------------------------------------------------------------------------


class ElasticsearchHandler(logging.Handler):
    """Ship log records to an Elasticsearch index via its REST API.

    Parameters
    ----------
    es_url : str
        Base URL of the Elasticsearch instance (e.g. ``http://localhost:9200``).
        Falls back to the ``ELASTICSEARCH_URL`` environment variable.
    index_prefix : str
        Prefix used for daily index names (``{prefix}-YYYY.MM.DD``).
    """

    def __init__(
        self,
        es_url: Optional[str] = None,
        index_prefix: str = "agencia-logs",
        level: int = logging.NOTSET,
    ) -> None:
        super().__init__(level)
        self.es_url = (es_url or os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")).rstrip("/")
        self.index_prefix = index_prefix
        self.setFormatter(JSONFormatter())

    def emit(self, record: logging.LogRecord) -> None:
        try:
            today = datetime.now(timezone.utc).strftime("%Y.%m.%d")
            index_name = f"{self.index_prefix}-{today}"
            url = f"{self.es_url}/{index_name}/_doc"
            body = self.format(record).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            self.handleError(record)


# ---------------------------------------------------------------------------
# LogContext
# ---------------------------------------------------------------------------


class LogContext:
    """Context manager that attaches a unique request ID to all log records
    produced within its scope.

    Usage::

        with LogContext(request_id="abc-123"):
            logger.info("processing request")
    """

    def __init__(self, request_id: Optional[str] = None) -> None:
        self.request_id = request_id or uuid.uuid4().hex

    def __enter__(self) -> "LogContext":
        self._token = _request_id_var.set(self.request_id)
        return self

    def __exit__(self, *exc: Any) -> None:
        _request_id_var.reset(self._token)


def get_current_request_id() -> str:
    """Return the request ID stored in the current context (empty string if unset)."""
    return _request_id_var.get()
