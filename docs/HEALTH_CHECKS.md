# Health Checks Guide

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health/live` | GET | Liveness probe — is the process running? |
| `/health/ready` | GET | Readiness probe — is the service ready for traffic? |
| `/health/detailed` | GET | Full results of every health check |
| `/health/services` | GET | Status of all external services |
| `/metrics` | GET | Prometheus metrics (text exposition format) |

## Response Format

### Liveness (`/health/live`)

```json
{
  "status": "alive",
  "uptime_seconds": 3600.12
}
```

### Readiness (`/health/ready`)

```json
{
  "status": "ready",
  "checks": {
    "disk_space": {"status": "healthy", "free_mb": 10240, "threshold_mb": 500},
    "memory": {"status": "healthy", "available_mb": 4096, "threshold_mb": 256},
    "llm_providers": {"status": "healthy", "providers": {"groq": "configured"}}
  }
}
```

### Detailed (`/health/detailed`)

Returns all checks (database, redis, elasticsearch, llm_providers,
disk_space, memory, queue_depth) with individual status, plus an overall
`"healthy"` or `"degraded"` status.

### Services (`/health/services`)

Returns only the external-service checks (database, redis, elasticsearch,
llm_providers).

## Interpretation

| Status | Meaning |
|---|---|
| `healthy` | The dependency is reachable and functioning |
| `unhealthy` | The dependency is unreachable or failing |
| `unknown` | The check could not determine status (e.g., unsupported OS) |
| `alive` | The process is running (liveness) |
| `ready` | All critical checks passed (readiness) |
| `not_ready` | One or more critical checks failed |
| `degraded` | Some non-critical checks failed |

## Configuration

All thresholds are configurable via environment variables:

| Variable | Default | Description |
|---|---|---|
| `POSTGRES_HOST` | `localhost` | PostgreSQL host |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |
| `REDIS_HOST` | `localhost` | Redis host |
| `REDIS_PORT` | `6379` | Redis port |
| `ELASTICSEARCH_URL` | `http://localhost:9200` | Elasticsearch URL |
| `DISK_SPACE_THRESHOLD_MB` | `500` | Minimum free disk space (MB) |
| `MEMORY_THRESHOLD_MB` | `256` | Minimum free memory (MB) |
| `RABBITMQ_HOST` | `localhost` | RabbitMQ host |
| `RABBITMQ_MANAGEMENT_PORT` | `15672` | RabbitMQ management API port |
| `QUEUE_DEPTH_THRESHOLD` | `1000` | Maximum acceptable queue depth |
