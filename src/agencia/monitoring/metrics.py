"""
Prometheus metrics definitions for the agencia-IA system.

All metrics follow Prometheus naming conventions and use labels
for dimensional data (status, agent, category, provider, error type).
"""

import os
import threading
import time

# ---------------------------------------------------------------------------
# Lightweight Prometheus-compatible metrics (no external dependency required)
# ---------------------------------------------------------------------------


class _Counter:
    """Thread-safe counter metric."""

    def __init__(self, name: str, description: str, label_names: tuple = ()):
        self.name = name
        self.description = description
        self.label_names = label_names
        self._values: dict[tuple, float] = {}
        self._lock = threading.Lock()

    def labels(self, **kwargs) -> "_Counter":
        key = tuple(kwargs.get(l, "") for l in self.label_names)
        clone = _CounterChild(self, key)
        return clone

    def inc(self, amount: float = 1.0) -> None:
        self._inc((), amount)

    def _inc(self, key: tuple, amount: float = 1.0) -> None:
        with self._lock:
            self._values[key] = self._values.get(key, 0.0) + amount

    def collect(self) -> list[dict]:
        with self._lock:
            return [
                {"labels": dict(zip(self.label_names, k)), "value": v}
                for k, v in self._values.items()
            ]


class _CounterChild:
    def __init__(self, parent: _Counter, key: tuple):
        self._parent = parent
        self._key = key

    def inc(self, amount: float = 1.0) -> None:
        self._parent._inc(self._key, amount)


class _Histogram:
    """Thread-safe histogram metric with configurable buckets."""

    DEFAULT_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)

    def __init__(self, name: str, description: str, label_names: tuple = (), buckets=None):
        self.name = name
        self.description = description
        self.label_names = label_names
        self.buckets = buckets or self.DEFAULT_BUCKETS
        self._sums: dict[tuple, float] = {}
        self._counts: dict[tuple, int] = {}
        self._bucket_counts: dict[tuple, list[int]] = {}
        self._lock = threading.Lock()

    def labels(self, **kwargs) -> "_HistogramChild":
        key = tuple(kwargs.get(l, "") for l in self.label_names)
        return _HistogramChild(self, key)

    def observe(self, value: float) -> None:
        self._observe((), value)

    def _observe(self, key: tuple, value: float) -> None:
        with self._lock:
            self._sums[key] = self._sums.get(key, 0.0) + value
            self._counts[key] = self._counts.get(key, 0) + 1
            if key not in self._bucket_counts:
                self._bucket_counts[key] = [0] * len(self.buckets)
            # Cumulative: every bucket whose bound >= value is incremented.
            for i, b in enumerate(self.buckets):
                if value <= b:
                    self._bucket_counts[key][i] += 1

    def collect(self) -> list[dict]:
        with self._lock:
            results = []
            for k in self._sums:
                results.append({
                    "labels": dict(zip(self.label_names, k)),
                    "sum": self._sums[k],
                    "count": self._counts[k],
                    "buckets": list(zip(self.buckets, self._bucket_counts.get(k, []))),
                })
            return results


class _HistogramChild:
    def __init__(self, parent: _Histogram, key: tuple):
        self._parent = parent
        self._key = key

    def observe(self, value: float) -> None:
        self._parent._observe(self._key, value)


class _Gauge:
    """Thread-safe gauge metric."""

    def __init__(self, name: str, description: str, label_names: tuple = ()):
        self.name = name
        self.description = description
        self.label_names = label_names
        self._values: dict[tuple, float] = {}
        self._lock = threading.Lock()

    def labels(self, **kwargs) -> "_GaugeChild":
        key = tuple(kwargs.get(l, "") for l in self.label_names)
        return _GaugeChild(self, key)

    def set(self, value: float) -> None:
        self._set((), value)

    def _set(self, key: tuple, value: float) -> None:
        with self._lock:
            self._values[key] = value

    def inc(self, amount: float = 1.0) -> None:
        self._inc((), amount)

    def _inc(self, key: tuple, amount: float = 1.0) -> None:
        with self._lock:
            self._values[key] = self._values.get(key, 0.0) + amount

    def dec(self, amount: float = 1.0) -> None:
        self._dec((), amount)

    def _dec(self, key: tuple, amount: float = 1.0) -> None:
        with self._lock:
            self._values[key] = self._values.get(key, 0.0) - amount

    def collect(self) -> list[dict]:
        with self._lock:
            return [
                {"labels": dict(zip(self.label_names, k)), "value": v}
                for k, v in self._values.items()
            ]


class _GaugeChild:
    def __init__(self, parent: _Gauge, key: tuple):
        self._parent = parent
        self._key = key

    def set(self, value: float) -> None:
        self._parent._set(self._key, value)

    def inc(self, amount: float = 1.0) -> None:
        self._parent._inc(self._key, amount)

    def dec(self, amount: float = 1.0) -> None:
        self._parent._dec(self._key, amount)


# ---------------------------------------------------------------------------
# Metric instances
# ---------------------------------------------------------------------------

task_counter = _Counter(
    "agencia_tasks_total",
    "Total tasks processed by status",
    label_names=("status",),
)

task_duration_histogram = _Histogram(
    "agencia_task_duration_seconds",
    "Task execution duration in seconds",
    label_names=("task_type",),
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0),
)

agent_execution_counter = _Counter(
    "agencia_agent_executions_total",
    "Agent executions by category and agent name",
    label_names=("category", "agent"),
)

router_decision_histogram = _Histogram(
    "agencia_router_decision_seconds",
    "Time taken for routing decisions",
    label_names=("route",),
)

llm_provider_counter = _Counter(
    "agencia_llm_provider_requests_total",
    "LLM provider usage count",
    label_names=("provider", "model"),
)

cache_hit_ratio = _Counter(
    "agencia_cache_operations_total",
    "Cache operations (hits and misses)",
    label_names=("result",),
)

memory_usage_gauge = _Gauge(
    "agencia_memory_usage_bytes",
    "Current memory usage in bytes",
    label_names=("type",),
)

queue_depth_gauge = _Gauge(
    "agencia_queue_depth",
    "Number of pending tasks in queue",
    label_names=("queue_name",),
)

error_rate_counter = _Counter(
    "agencia_errors_total",
    "Total errors by type and agent",
    label_names=("error_type", "agent"),
)

# ---------------------------------------------------------------------------
# Registry & exposition
# ---------------------------------------------------------------------------

_ALL_METRICS = [
    task_counter,
    task_duration_histogram,
    agent_execution_counter,
    router_decision_histogram,
    llm_provider_counter,
    cache_hit_ratio,
    memory_usage_gauge,
    queue_depth_gauge,
    error_rate_counter,
]


def generate_metrics_text() -> str:
    """Generate Prometheus text exposition format output."""
    lines: list[str] = []
    for metric in _ALL_METRICS:
        lines.append(f"# HELP {metric.name} {metric.description}")
        if isinstance(metric, _Counter):
            lines.append(f"# TYPE {metric.name} counter")
            for entry in metric.collect():
                label_str = ",".join(f'{k}="{v}"' for k, v in entry["labels"].items())
                label_part = f"{{{label_str}}}" if label_str else ""
                lines.append(f"{metric.name}{label_part} {entry['value']}")
        elif isinstance(metric, _Histogram):
            lines.append(f"# TYPE {metric.name} histogram")
            for entry in metric.collect():
                label_str = ",".join(f'{k}="{v}"' for k, v in entry["labels"].items())
                base_label = f"{{{label_str}}}" if label_str else ""
                for bound, count in entry["buckets"]:
                    le_label = f'{label_str},le="{bound}"' if label_str else f'le="{bound}"'
                    lines.append(f"{metric.name}_bucket{{{le_label}}} {count}")
                inf_label = f'{label_str},le="+Inf"' if label_str else 'le="+Inf"'
                lines.append(f"{metric.name}_bucket{{{inf_label}}} {entry['count']}")
                lines.append(f"{metric.name}_sum{base_label} {entry['sum']}")
                lines.append(f"{metric.name}_count{base_label} {entry['count']}")
        elif isinstance(metric, _Gauge):
            lines.append(f"# TYPE {metric.name} gauge")
            for entry in metric.collect():
                label_str = ",".join(f'{k}="{v}"' for k, v in entry["labels"].items())
                label_part = f"{{{label_str}}}" if label_str else ""
                lines.append(f"{metric.name}{label_part} {entry['value']}")
    return "\n".join(lines) + "\n"
