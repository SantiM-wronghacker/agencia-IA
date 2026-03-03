"""
Agencia IA - Advanced LLM Router (Multi-Model)

Supports multiple LLM providers with automatic failover:
- GPT-4o (OpenAI) - Precision tasks (finance, legal)
- Claude 3.5 Sonnet (Anthropic) - Comprehension tasks
- Llama 3.3 70B (Groq) - Fast/Free
- Mistral Large (Mistral) - Good balance
- Gemini 2.0 (Google) - Fast/Good
- Cerebras (Cerebras) - Super fast/Free
"""

import os
import logging
import time
from typing import Any, Optional

logger = logging.getLogger("agencia.llm_router")

# Model configurations per provider
MODEL_CONFIG: dict[str, dict[str, Any]] = {
    "openai": {
        "model": "gpt-4o",
        "api_key_env": "OPENAI_API_KEY",
        "strengths": ["precision", "finanzas", "legal", "complex_reasoning"],
        "priority": 1,
    },
    "anthropic": {
        "model": "claude-3-5-sonnet-20241022",
        "api_key_env": "ANTHROPIC_API_KEY",
        "strengths": ["comprehension", "writing", "analysis", "creative"],
        "priority": 2,
    },
    "groq": {
        "model": "llama-3.3-70b-versatile",
        "api_key_env": "GROQ_API_KEY",
        "strengths": ["speed", "classification", "extraction", "general"],
        "priority": 3,
    },
    "mistral": {
        "model": "mistral-large-latest",
        "api_key_env": "MISTRAL_API_KEY",
        "strengths": ["balance", "general", "multilingual"],
        "priority": 4,
    },
    "google": {
        "model": "gemini-2.0-flash",
        "api_key_env": "GOOGLE_API_KEY",
        "strengths": ["speed", "general", "multimodal"],
        "priority": 5,
    },
    "cerebras": {
        "model": "llama3.1-70b",
        "api_key_env": "CEREBRAS_API_KEY",
        "strengths": ["speed", "free", "general"],
        "priority": 6,
    },
}

# Category to preferred model mapping
CATEGORY_MODEL_MAP: dict[str, str] = {
    "finanzas": "openai",
    "contabilidad": "openai",
    "legal": "openai",
    "salud": "anthropic",
    "educacion": "anthropic",
    "cerebro": "anthropic",
    "marketing": "mistral",
    "ventas": "mistral",
    "herramientas": "groq",
    "operaciones": "groq",
    "logistica": "groq",
    "real_estate": "groq",
    "restaurantes": "groq",
    "seguros": "mistral",
    "turismo": "mistral",
    "tecnologia": "groq",
    "recursos_humanos": "mistral",
    "micro_tareas": "cerebras",
}


class AdvancedLLMRouter:
    """Routes LLM requests to the best available provider."""

    def __init__(self) -> None:
        self._available_providers: list[str] = []
        self._failure_counts: dict[str, int] = {}
        self._detect_available_providers()

    def _detect_available_providers(self) -> None:
        """Detect which providers have API keys configured."""
        self._available_providers = []
        for provider, config in MODEL_CONFIG.items():
            key = os.environ.get(config["api_key_env"], "")
            if key:
                self._available_providers.append(provider)
                self._failure_counts[provider] = 0

        logger.info(
            "llm_providers_detected",
            extra={"providers": self._available_providers},
        )

    def get_provider_for_category(self, category: str) -> Optional[str]:
        """Get the best provider for a given agent category."""
        preferred = CATEGORY_MODEL_MAP.get(category, "groq")

        if preferred in self._available_providers:
            if self._failure_counts.get(preferred, 0) < 3:
                return preferred

        # Fallback: try providers by priority
        sorted_providers = sorted(
            self._available_providers,
            key=lambda p: MODEL_CONFIG[p]["priority"],
        )
        for provider in sorted_providers:
            if self._failure_counts.get(provider, 0) < 3:
                return provider

        # Reset failure counts and try again
        self._failure_counts = {p: 0 for p in self._available_providers}
        return sorted_providers[0] if sorted_providers else None

    def get_model_config(self, provider: str) -> dict[str, Any]:
        """Get model configuration for a provider."""
        return MODEL_CONFIG.get(provider, {})

    def report_failure(self, provider: str) -> None:
        """Report a failure for a provider (for circuit breaker)."""
        self._failure_counts[provider] = (
            self._failure_counts.get(provider, 0) + 1
        )
        logger.warning(
            "llm_provider_failure",
            extra={
                "provider": provider,
                "failure_count": self._failure_counts[provider],
            },
        )

    def report_success(self, provider: str) -> None:
        """Report a success for a provider."""
        self._failure_counts[provider] = 0

    def get_available_providers(self) -> list[str]:
        """Get list of available providers."""
        return self._available_providers.copy()

    def get_status(self) -> dict[str, Any]:
        """Get status of all providers."""
        return {
            "available_providers": self._available_providers,
            "failure_counts": self._failure_counts.copy(),
            "total_providers": len(MODEL_CONFIG),
        }


# Global singleton
llm_router = AdvancedLLMRouter()
