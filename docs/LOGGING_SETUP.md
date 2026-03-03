# Logging Setup Guide

## Overview

All application logs are emitted in **JSON format** so they can be ingested
directly by Elasticsearch, Logstash, or Filebeat.

## How Elasticsearch Stores Logs

Logs are written to daily indices following the pattern:

```
agencia-logs-YYYY.MM.DD
```

Each document contains:

| Field | Description |
|---|---|
| `timestamp` | ISO-8601 UTC timestamp |
| `level` | Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `module` | Python module that produced the log |
| `function` | Function name |
| `line` | Source line number |
| `message` | Log message |
| `request_id` | Unique request ID propagated through the call stack |
| `user_id` | (optional) User identifier |
| `tenant_id` | (optional) Tenant identifier |

## How to Query in Kibana

1. Open Kibana at `http://localhost:5601`.
2. Go to **Discover** and select the `agencia-logs-*` index pattern.
3. Use KQL queries:

```kql
level: "ERROR" AND module: "api"
request_id: "abc123"
message: "timeout" AND level: "WARNING"
```

## Log Levels and Filtering

| Level | When to use |
|---|---|
| `DEBUG` | Verbose diagnostic output (disabled in production) |
| `INFO` | Normal operational messages |
| `WARNING` | Unexpected but recoverable situations |
| `ERROR` | Failures that need attention |
| `CRITICAL` | System-level failures |

Set the minimum level via the `LOG_LEVEL` environment variable (default: `INFO`).

## Sensitive Data Sanitisation

The `SanitizeFilter` automatically redacts:

- API keys matching `gsk_*`, `sk-*` patterns
- Bearer tokens
- Values next to `api_key=` or `password=`

Redacted values are replaced with `***REDACTED***`.

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `ELASTICSEARCH_URL` | `http://localhost:9200` | ES cluster URL |
| `LOG_LEVEL` | `INFO` | Minimum log level |
| `AGENCIA_USER_ID` | *(empty)* | Default user ID for log context |
| `AGENCIA_TENANT_ID` | *(empty)* | Default tenant ID for log context |
