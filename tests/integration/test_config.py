"""Integration tests for the centralized configuration module."""

import os
import pytest


def test_config_loads():
    from agencia.agents.herramientas.config import load_config
    cfg = load_config()
    assert isinstance(cfg, dict)
    assert "BASE_DIR" in cfg
    assert "GROQ_API_KEY" in cfg


def test_model_names_are_groq_format():
    """Model names should be Groq-compatible, not legacy ollama format."""
    from agencia.agents.herramientas.config import MODEL_FAST, MODEL_STRONG
    for name in (MODEL_FAST, MODEL_STRONG):
        assert ":" not in name, f"Model '{name}' looks like ollama format (contains ':')"
        assert "llama" in name.lower() or "mixtral" in name.lower(), (
            f"Model '{name}' doesn't look like a valid Groq model"
        )


def test_groq_api_key_placeholder():
    """Default GROQ_API_KEY should be a placeholder, not empty."""
    from agencia.agents.herramientas.config import GROQ_API_KEY
    assert GROQ_API_KEY, "GROQ_API_KEY should have a placeholder value"


def test_directories_created():
    """RUNS_DIR and KB_DIR should exist after import."""
    from agencia.agents.herramientas.config import RUNS_DIR, KB_DIR
    assert RUNS_DIR.exists(), f"RUNS_DIR does not exist: {RUNS_DIR}"
    assert KB_DIR.exists(), f"KB_DIR does not exist: {KB_DIR}"


def test_api_host_and_port():
    from agencia.agents.herramientas.config import API_HOST, API_PORT
    assert isinstance(API_PORT, int)
    assert 1 <= API_PORT <= 65535
    assert isinstance(API_HOST, str)
