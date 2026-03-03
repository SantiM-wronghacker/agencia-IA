# Docker Setup Guide

Instructions to run the Agencia Santi system with Docker Compose.

## Prerequisites

- Docker Engine 24+
- Docker Compose v2+
- A valid Groq API key (get one at <https://console.groq.com>)

## 1. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set at minimum:

```dotenv
GROQ_API_KEY=gsk_your_actual_key_here
MODEL_FAST=llama3:8b
MODEL_STRONG=gpt-oss:20b
API_HOST=0.0.0.0
API_PORT=8000
```

## 2. Build and Start Services

```bash
docker-compose up -d
```

This starts:

| Service     | Port  | Description                        |
|-------------|-------|------------------------------------|
| `api`       | 8000  | FastAPI backend                    |
| `dashboard` | 5000  | Flask web dashboard                |
| `redis`     | 6379  | Celery broker / backend            |
| `worker`    | —     | Celery worker for async tasks      |

## 3. Verify All Services

```bash
# Check containers are running
docker-compose ps

# Health check
curl http://localhost:8000/health

# View logs
docker-compose logs -f api
```

## 4. Run Migrations Inside Container

```bash
docker-compose exec api python scripts/consolidate_routers.py --execute
docker-compose exec api python scripts/migrate_to_src.py --execute
docker-compose exec api python scripts/verify_migration.py
```

## 5. Run Tests

```bash
docker-compose exec api python -m pytest tests/ -v
```

## 6. Stop Services

```bash
docker-compose down           # stop and remove containers
docker-compose down -v        # also remove volumes (data loss!)
```

## 7. Rebuild After Code Changes

```bash
docker-compose build --no-cache
docker-compose up -d
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 already in use | Change `API_PORT` in `.env` or stop the conflicting process |
| Redis connection refused | Ensure the `redis` service is running: `docker-compose up -d redis` |
| Permission denied on volumes | Run `sudo chown -R $USER:$USER .` on the repo directory |
| API returns 503 | Verify `GROQ_API_KEY` is set correctly in `.env` |
