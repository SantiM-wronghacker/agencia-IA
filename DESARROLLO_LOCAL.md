# Desarrollo Local - Sin Docker

## Requisitos
- Python 3.10+
- pip
- Git

## Setup (5 minutos)

### 1. Clonar y entrar al repo
```bash
cd agencia-IA
```

### 2. Crear venv e instalar deps
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configurar env
```bash
# Copiar template
cp .env.local .env

# EDITAR .env con tu GROQ_API_KEY
nano .env
```

## Ejecutar Tests (sin Docker)

```bash
# Todos los tests (621 tests, ~5 segundos)
pytest tests/ -v

# Solo compilación de agentes (verificar que compilan)
pytest tests/integration/test_agent_compilation.py -v

# Solo config
pytest tests/integration/test_config.py -v

# Ver cobertura
pytest tests/ --cov=src/agencia --cov-report=html
```

## Ejecutar API en vivo

```bash
# Terminal 1: Arrancar API
uvicorn src.agencia.api.api:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Test endpoint
curl http://localhost:8000/health
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"company": "test", "project": "test", "message": "hola"}'
```

## Ejecutar Agentes Directamente

```bash
# Test seguimiento de ventas
python -m agencia.agents.ventas.seguimiento_pipeline

# Test optimización de rutas
python -m agencia.agents.logistica.optimizador_ruta_entregas

# Test config
python -m agencia.agents.herramientas.config
```

## Servicios Opcionales (si los necesitas)

Si quieres Elasticsearch, Redis, etc sin Docker:

### Opción A: Brew (Mac/Linux)
```bash
# Instalar
brew install elasticsearch redis postgresql

# Arrancar en background
brew services start elasticsearch
brew services start redis
brew services start postgresql

# Ver status
brew services list
```

### Opción B: Manual (cualquier SO)
```bash
# Elasticsearch (requiere Java)
# Descargar desde: https://www.elastic.co/downloads/elasticsearch
elasticsearch

# Redis
# Descargar desde: https://redis.io/download
redis-server

# PostgreSQL
# Descargar desde: https://www.postgresql.org/download
postgres
```

## Estructura de Carpetas

```
agencia-IA/
├── src/agencia/
│   ├── agents/          ← 530+ agentes
│   ├── api/             ← API REST
│   ├── health/          ← Health checks
│   ├── monitoring/      ← Métricas Prometheus
│   └── logging/         ← Logs JSON
├── tests/
│   ├── test_*.py        ← Unit tests
│   └── integration/     ← Integration tests (569 tests)
├── .env.local           ← Config local (NO COMMIT)
├── requirements.txt     ← Dependencias Python
└── docker-compose.yml   ← Para prod (opcional)
```

## Desarrollo Normal

```bash
# Editar código
nano src/agencia/agents/ventas/seguimiento_pipeline.py

# Test rápido
pytest tests/test_api.py -v

# Ejecutar agente
python -m agencia.agents.ventas.seguimiento_pipeline

# Commit
git add .
git commit -m "feat: description"
git push origin main
```

## Troubleshooting

**Error: `GROQ_API_KEY not configured`**
```bash
# Edita .env y añade tu key
nano .env
# Busca GROQ_API_KEY=gsk_tu_key_aqui
# Reemplaza con tu key real
```

**Error: `ModuleNotFoundError: No module named 'agencia'`**
```bash
# Asegúrate que instalaste deps y estás en venv
pip install -r requirements.txt
source venv/bin/activate
```

**Error: `Connection refused` en health checks**
```bash
# Normal si no tienes los servicios opcionales (Redis, ES, etc)
# Los tests ignoran servicios no disponibles - es OK
pytest tests/ -v
```

## Performance

- Tests: ~5 segundos (621 tests)
- Compilación agentes: ~2 segundos (530 files)
- API startup: ~1 segundo
- Primer request: ~2 segundos (Groq API call)

## Próximo Paso: Producción

Cuando esté listo, despliega en:
- DigitalOcean
- AWS
- Heroku
- Tu servidor

Ver `docker-compose.yml` para servicios en producción.
