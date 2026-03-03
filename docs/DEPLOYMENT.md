# Deployment - Agencia IA

## Requisitos Previos

- Docker 24+ y Docker Compose v2
- 8 GB RAM mínimo (16 GB recomendado)
- 20 GB disco libre
- API keys de al menos un proveedor LLM

## Inicio Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/SantiM-wronghacker/agencia-IA.git
cd agencia-IA

# 2. Configurar variables de entorno
cp .env.example .env
nano .env  # Editar con tus API keys

# 3. Levantar todo
docker-compose up -d

# 4. Verificar estado
docker-compose ps

# 5. Ver logs
docker-compose logs -f api_agencia
```

## Variables de Entorno

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `GROQ_API_KEY` | API key de Groq | Sí (al menos uno) |
| `OPENAI_API_KEY` | API key de OpenAI | No |
| `ANTHROPIC_API_KEY` | API key de Anthropic | No |
| `POSTGRES_PASSWORD` | Password de PostgreSQL | Sí |
| `REDIS_PASSWORD` | Password de Redis | Sí |
| `RABBITMQ_PASSWORD` | Password de RabbitMQ | Sí |

## Servicios y Puertos

| Servicio | Puerto | Healthcheck |
|----------|--------|-------------|
| API Agencia | 8000 | GET /health |
| Dashboard Web | 8080 | GET /health |
| App Dashboard | 5000 | GET /health |
| Streamlit | 8501 | GET /_stcore/health |
| PostgreSQL | 5432 | pg_isready |
| Redis | 6379 | redis-cli ping |
| RabbitMQ | 5672/15672 | rabbitmq-diagnostics ping |
| Prometheus | 9090 | - |
| Grafana | 3000 | - |
| Jaeger | 16686 | - |
| Elasticsearch | 9200 | GET /_cluster/health |
| Kibana | 5601 | - |

## Troubleshooting

### Servicio no arranca

```bash
# Ver logs del servicio específico
docker-compose logs api_agencia

# Reiniciar un servicio
docker-compose restart api_agencia

# Reconstruir imagen
docker-compose build --no-cache api_agencia
docker-compose up -d api_agencia
```

### Base de datos no conecta

```bash
# Verificar que PostgreSQL está corriendo
docker-compose exec postgres pg_isready -U agencia

# Ejecutar schema manualmente
docker-compose exec postgres psql -U agencia -d agencia_ia -f /docker-entrypoint-initdb.d/01-schema.sql
```

### Limpiar todo y empezar de nuevo

```bash
docker-compose down -v  # Elimina volúmenes
docker-compose up -d    # Recrea todo
```
