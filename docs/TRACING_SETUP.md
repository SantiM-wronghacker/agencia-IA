# Tracing Setup Guide

## Overview

Distributed tracing lets you follow a single request as it flows through
the multi-agent system. The agencia-IA system uses a Jaeger-compatible
tracing backend.

## How to View Traces in Jaeger

1. Open the Jaeger UI at `http://localhost:16686`.
2. Select the **agencia-ia** service from the dropdown.
3. Click **Find Traces** to see recent traces.
4. Click on a trace to view its timeline of spans.

## Understanding Trace Spans

Each span represents a unit of work:

| Tag | Meaning |
|---|---|
| `service` | Service that produced the span |
| `http.method` | HTTP method (for request spans) |
| `http.url` | Full URL of the request |
| `http.status_code` | Response status code |
| `agent.category` | Agent category (for agent spans) |
| `agent.name` | Agent name |
| `status` | `ok` or `error` |
| `error.type` | Exception class name (on errors) |

### Span Hierarchy

```
HTTP POST /chat
  └── agent.router
        └── agent.chat_handler
              └── llm.groq.call
```

## Performance Bottleneck Identification

1. Sort traces by duration to find the slowest requests.
2. Drill into a slow trace to see which span took the most time.
3. Look for spans with `status=error` to find failures.
4. Compare span durations across different LLM providers.

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `JAEGER_SERVICE_NAME` | `agencia-ia` | Service name in Jaeger |
| `JAEGER_AGENT_HOST` | `localhost` | Jaeger agent hostname |
| `JAEGER_AGENT_PORT` | `6831` | Jaeger agent UDP port |
| `JAEGER_COLLECTOR_ENDPOINT` | `http://localhost:14268/api/traces` | HTTP collector |
| `JAEGER_ENABLED` | `false` | Enable span shipping |
| `JAEGER_SAMPLE_RATE` | `1.0` | Sampling rate (0.0 – 1.0) |
