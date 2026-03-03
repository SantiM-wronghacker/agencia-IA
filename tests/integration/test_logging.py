"""Integration tests for structured JSON logging."""

import io
import json
import logging
import pytest

from src.agencia.logging.json_logger import JSONFormatter, LogContext
from src.agencia.logging.filters import (
    AddRequestIDFilter,
    AddUserContextFilter,
    SanitizeFilter,
)


class _BufferHandler(logging.Handler):
    """Handler that writes formatted output to a StringIO buffer."""

    def __init__(self):
        super().__init__()
        self.buffer = io.StringIO()

    def emit(self, record):
        self.buffer.write(self.format(record) + "\n")

    def get_last(self) -> str:
        """Return the last non-empty line written to the buffer."""
        lines = [l for l in self.buffer.getvalue().splitlines() if l.strip()]
        return lines[-1] if lines else ""


@pytest.fixture
def json_logger():
    """Create a logger with JSONFormatter, all filters, and a buffer handler."""
    logger = logging.getLogger("test_json_logger")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    logger.propagate = False
    handler = _BufferHandler()
    handler.setFormatter(JSONFormatter())
    handler.addFilter(AddRequestIDFilter(default_id="test-req-id"))
    handler.addFilter(AddUserContextFilter(user_id="u1", tenant_id="t1"))
    handler.addFilter(SanitizeFilter())
    logger.addHandler(handler)
    return logger, handler


def test_json_format(json_logger):
    logger, handler = json_logger
    logger.info("hello world")
    record = json.loads(handler.get_last())
    assert record["level"] == "INFO"
    assert record["message"] == "hello world"
    assert "timestamp" in record
    assert "module" in record
    assert "function" in record
    assert "line" in record


def test_required_fields(json_logger):
    logger, handler = json_logger
    logger.warning("check fields")
    record = json.loads(handler.get_last())
    required = {"timestamp", "level", "module", "function", "line", "message", "logger"}
    assert required.issubset(record.keys())


def test_request_id_present(json_logger):
    logger, handler = json_logger
    logger.info("with request id")
    record = json.loads(handler.get_last())
    assert record.get("request_id") == "test-req-id"


def test_user_context(json_logger):
    logger, handler = json_logger
    logger.info("with user context")
    record = json.loads(handler.get_last())
    assert record.get("user_id") == "u1"
    assert record.get("tenant_id") == "t1"


def test_sensitive_data_redacted(json_logger):
    logger, handler = json_logger
    logger.info("api_key=gsk_abcdefghij1234567890xyz secret")
    record = json.loads(handler.get_last())
    assert "gsk_abcdefghij1234567890xyz" not in record["message"]
    assert "REDACTED" in record["message"]


def test_password_redacted(json_logger):
    logger, handler = json_logger
    logger.info("password=super_secret_password123")
    record = json.loads(handler.get_last())
    assert "super_secret_password123" not in record["message"]
    assert "REDACTED" in record["message"]


def test_bearer_redacted(json_logger):
    logger, handler = json_logger
    logger.info("bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
    record = json.loads(handler.get_last())
    assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in record["message"]
    assert "REDACTED" in record["message"]


def test_log_context_sets_request_id():
    logger = logging.getLogger("test_log_context")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    logger.propagate = False
    handler = _BufferHandler()
    handler.setFormatter(JSONFormatter())
    handler.addFilter(AddRequestIDFilter())
    logger.addHandler(handler)

    with LogContext(request_id="ctx-123"):
        logger.info("inside context")

    record = json.loads(handler.get_last())
    assert record.get("request_id") == "ctx-123"
