# Monitoring Setup Guide

## Prometheus

### Access
- **URL**: `http://localhost:9090`
- Prometheus scrapes metrics from all configured targets at regular intervals.

### How to Query Metrics

Open the Prometheus web UI and enter PromQL queries in the expression browser.

#### Key Metrics

| Metric | Description |
|---|---|
| `agencia_tasks_total` | Total tasks processed, labelled by `status` |
| `agencia_task_duration_seconds` | Histogram of task execution durations |
| `agencia_agent_executions_total` | Agent executions by `category` and `agent` |
| `agencia_router_decision_seconds` | Time taken for routing decisions |
| `agencia_llm_provider_requests_total` | LLM requests by `provider` and `model` |
| `agencia_cache_operations_total` | Cache hits / misses |
| `agencia_memory_usage_bytes` | Current memory usage |
| `agencia_queue_depth` | Pending tasks in queue |
| `agencia_errors_total` | Errors by `error_type` and `agent` |

### Example Queries

```promql
# Error rate over the last 5 minutes
rate(agencia_errors_total[5m])

# 95th percentile task duration
histogram_quantile(0.95, rate(agencia_task_duration_seconds_bucket[5m]))

# Tasks per second by status
rate(agencia_tasks_total[1m])

# Top 5 agents by execution count
topk(5, agencia_agent_executions_total)
```

### Alert Examples

See `monitoring/alerts/alert_rules.yml` for pre-configured alerts:
- **HighErrorRate** — fires when the error rate exceeds the threshold.
- **ServiceDown** — fires when a health-check target is unreachable.
- **HighMemoryUsage** — fires when memory exceeds 90 % of available.
- **HighQueueDepth** — fires when the task queue grows too large.
- **LLMProviderDown** — fires when no LLM provider responds.

## Grafana

- **URL**: `http://localhost:3000`
- Default credentials: `admin` / `admin`
- Pre-built dashboards are in `monitoring/grafana/dashboards/`.
