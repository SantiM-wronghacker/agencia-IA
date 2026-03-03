"""
Logging filters for request ID propagation, user context, and sensitive data
sanitisation.
"""

import logging
import os
import re
import uuid
from typing import Optional

from src.agencia.logging.json_logger import get_current_request_id


# ---------------------------------------------------------------------------
# AddRequestIDFilter
# ---------------------------------------------------------------------------


class AddRequestIDFilter(logging.Filter):
    """Inject a ``request_id`` attribute into every log record.

    If a ``LogContext`` is active its ID is used; otherwise a new UUID is
    generated per filter instance so that records within the same process
    share a single ID.
    """

    def __init__(self, name: str = "", default_id: Optional[str] = None) -> None:
        super().__init__(name)
        self._default_id = default_id or uuid.uuid4().hex

    def filter(self, record: logging.LogRecord) -> bool:
        ctx_id = get_current_request_id()
        record.request_id = ctx_id if ctx_id else self._default_id  # type: ignore[attr-defined]
        return True


# ---------------------------------------------------------------------------
# AddUserContextFilter
# ---------------------------------------------------------------------------


class AddUserContextFilter(logging.Filter):
    """Attach ``user_id`` and ``tenant_id`` from environment variables or
    explicit parameters to every log record.
    """

    def __init__(
        self,
        name: str = "",
        user_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> None:
        super().__init__(name)
        self.user_id = user_id or os.getenv("AGENCIA_USER_ID", "")
        self.tenant_id = tenant_id or os.getenv("AGENCIA_TENANT_ID", "")

    def filter(self, record: logging.LogRecord) -> bool:
        record.user_id = self.user_id  # type: ignore[attr-defined]
        record.tenant_id = self.tenant_id  # type: ignore[attr-defined]
        return True


# ---------------------------------------------------------------------------
# SanitizeFilter
# ---------------------------------------------------------------------------

# Patterns that look like API keys, passwords, or bearer tokens.
_SENSITIVE_PATTERNS = [
    re.compile(r"(gsk_)[A-Za-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"(sk-)[A-Za-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"(bearer\s+)[A-Za-z0-9._\-]{20,}", re.IGNORECASE),
    re.compile(r"(api[_-]?key\s*[:=]\s*)['\"]?[A-Za-z0-9._\-]{8,}['\"]?", re.IGNORECASE),
    re.compile(r"(password\s*[:=]\s*)['\"]?[^\s'\"]{4,}['\"]?", re.IGNORECASE),
]


class SanitizeFilter(logging.Filter):
    """Redact sensitive information (API keys, passwords, tokens) from log
    messages before they are emitted.
    """

    REDACTED = "***REDACTED***"

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for pattern in _SENSITIVE_PATTERNS:
            msg = pattern.sub(lambda m: m.group(1) + self.REDACTED, msg)
        record.msg = msg
        record.args = None
        return True
