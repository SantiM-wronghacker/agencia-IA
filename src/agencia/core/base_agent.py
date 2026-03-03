"""
Agencia IA - BaseAgent

Universal base class for all 510 agents.
Provides automatic logging, metrics, error handling, caching, and tracing.
"""

import time
import logging
import hashlib
from abc import ABC, abstractmethod
from typing import Any, Optional

logger = logging.getLogger("agencia.agent")


class BaseAgent(ABC):
    """Base class that all agents must inherit from."""

    def __init__(
        self,
        name: str,
        category: str,
        description: str = "",
        version: str = "1.0.0",
        preferred_model: str = "groq",
    ):
        self.name = name
        self.category = category
        self.description = description
        self.version = version
        self.preferred_model = preferred_model
        self._cache: dict[str, Any] = {}
        self._execution_count = 0
        self._error_count = 0
        self._total_duration_ms = 0.0

    @abstractmethod
    def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Execute the agent's main logic. Must be implemented by subclasses."""

    def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Run the agent with logging, metrics, caching, and error handling."""
        cache_key = self._make_cache_key(input_data)
        cached = self._cache.get(cache_key)
        if cached is not None:
            logger.info(
                "cache_hit",
                extra={"agent": self.name, "category": self.category},
            )
            return cached

        start = time.monotonic()
        self._execution_count += 1

        try:
            result = self.execute(input_data)
            duration_ms = (time.monotonic() - start) * 1000
            self._total_duration_ms += duration_ms

            logger.info(
                "agent_executed",
                extra={
                    "agent": self.name,
                    "category": self.category,
                    "duration_ms": round(duration_ms, 2),
                    "status": "success",
                },
            )

            self._cache[cache_key] = result
            return result

        except Exception as exc:
            duration_ms = (time.monotonic() - start) * 1000
            self._error_count += 1

            logger.error(
                "agent_error",
                extra={
                    "agent": self.name,
                    "category": self.category,
                    "duration_ms": round(duration_ms, 2),
                    "error": str(exc),
                },
            )
            raise

    def health_check(self) -> dict[str, Any]:
        """Return health status of this agent."""
        avg_duration = (
            self._total_duration_ms / self._execution_count
            if self._execution_count > 0
            else 0
        )
        success_rate = (
            (1 - self._error_count / self._execution_count) * 100
            if self._execution_count > 0
            else 100.0
        )
        return {
            "name": self.name,
            "category": self.category,
            "version": self.version,
            "status": "healthy",
            "execution_count": self._execution_count,
            "error_count": self._error_count,
            "avg_duration_ms": round(avg_duration, 2),
            "success_rate": round(success_rate, 2),
        }

    def clear_cache(self) -> None:
        """Clear the agent's result cache."""
        self._cache.clear()

    def get_capabilities(self) -> list[str]:
        """Return list of capabilities. Override in subclasses."""
        return []

    def _make_cache_key(self, input_data: dict[str, Any]) -> str:
        raw = str(sorted(input_data.items()))
        return hashlib.sha256(raw.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} category={self.category!r}>"
