"""
Decorators for automatic metric tracking of agent executions and function calls.
"""

import functools
import time

from src.agencia.monitoring.metrics import (
    task_counter,
    task_duration_histogram,
    agent_execution_counter,
    error_rate_counter,
)


def track_execution(category: str = "default", agent: str = "unknown"):
    """Wrap an agent execution function to record metrics.

    Records:
    - ``agent_execution_counter`` labelled by *category* and *agent*
    - ``task_counter`` labelled by resulting status (``success`` / ``error``)
    - ``task_duration_histogram`` labelled by *category*
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                task_counter.labels(status="success").inc()
                agent_execution_counter.labels(category=category, agent=agent).inc()
                return result
            except Exception as exc:
                task_counter.labels(status="error").inc()
                error_rate_counter.labels(
                    error_type=type(exc).__name__, agent=agent
                ).inc()
                raise
            finally:
                elapsed = time.time() - start
                task_duration_histogram.labels(task_type=category).observe(elapsed)

        return wrapper

    return decorator


def track_performance(metric_name: str = "default"):
    """Record the duration of any function call in ``task_duration_histogram``."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.time() - start
                task_duration_histogram.labels(task_type=metric_name).observe(elapsed)

        return wrapper

    return decorator


def track_errors(agent: str = "unknown"):
    """Catch exceptions, record them in ``error_rate_counter``, then re-raise."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                error_rate_counter.labels(
                    error_type=type(exc).__name__, agent=agent
                ).inc()
                raise

        return wrapper

    return decorator
