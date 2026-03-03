# API Reference - Agencia IA

## Base URL

- **Desarrollo**: `http://localhost:8000`
- **Via Nginx**: `http://localhost/api`

## Endpoints

### Health Check

```http
GET /health
```

**Response (200 OK)**:
```json
{
  "status": "ok",
  "service": "agencia-ia-api"
}
```

### Chat

```http
POST /chat
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "Calcular el ROI de una inversión de $100,000",
  "session_id": "user-123",
  "category": "finanzas"
}
```

**Response (200 OK)**:
```json
{
  "response": "El ROI calculado es...",
  "agent": "calculadora_roi",
  "category": "finanzas",
  "duration_ms": 150.5
}
```

### Metrics (Prometheus)

```http
GET /metrics
```

**Response**: Prometheus text exposition format with agent execution metrics, API latency, and system health data.

## Error Responses

| Code | Description |
|------|-------------|
| 400 | Bad Request - Parámetros inválidos |
| 404 | Not Found - Endpoint no existe |
| 500 | Internal Server Error |
| 503 | Service Unavailable - Servicio no disponible |

## Rate Limiting

El API Gateway (Nginx) implementa rate limiting para proteger los servicios.
Configurar en `nginx/nginx.conf` según necesidad.
