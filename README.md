# 🚀 Agencia IA - Multi-Agent System

Sistema de 500+ agentes IA especializados en 21 categorías de negocio. Automatizan tareas complejas con Groq AI.

## ⚡ Quick Start (5 min)

### Opción 1: Desarrollo Local (Recomendado)
```bash
chmod +x start_dev.sh
./start_dev.sh              # Linux/Mac
# o
start_dev.bat              # Windows
```

### Opción 2: Con Podman (Servicios optimizados)
```bash
brew install podman         # Instalar Podman
podman machine init         # Mac solamente
chmod +x start_podman.sh
./start_podman.sh           # Arranca Elasticsearch, Redis, etc
```
Ver [PODMAN_SETUP.md](PODMAN_SETUP.md) para más detalles.

### Opción 3: Manual
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env.local
# Edita .env.local y añade tu GROQ_API_KEY
```

## 📋 Main Commands

```bash
# Run all tests (621 tests)
pytest tests/ -v

# Start API locally
uvicorn src.agencia.api.api:app --reload --host 127.0.0.1 --port 8000

# Test an agent
python -m agencia.agents.ventas.seguimiento_pipeline

# Check config
python -m agencia.agents.herramientas.config
```

## 📚 Documentation

- **[DESARROLLO_LOCAL.md](DESARROLLO_LOCAL.md)** - Full local dev guide
- **[STATUS.md](STATUS.md)** - System status and metrics
- **[DIAGNOSTICO_COMPLETO.md](DIAGNOSTICO_COMPLETO.md)** - Health diagnostics

## 🏗️ Architecture

```
src/agencia/
├── agents/          (530+ agent scripts)
│   ├── cerebro/     (Routing, memory, strategy)
│   ├── ventas/      (Sales agents)
│   ├── logistica/   (Logistics)
│   ├── finanzas/    (Finance)
│   └── ...
├── api/             (FastAPI + Dashboard)
├── health/          (Health checks)
├── monitoring/      (Prometheus metrics)
└── logging/         (JSON structured logs)
```

## 📊 Stats

- **Agents**: 305+ (growing to 500)
- **Categories**: 21
- **Tests**: 621 ✅
- **Python**: 3.10+

## 🔑 Requirements

- **Required**: GROQ_API_KEY (get from https://console.groq.com/keys)
- **Optional**: Docker (for Elasticsearch, Redis, RabbitMQ, Prometheus)

## 🌐 Endpoints

```
GET  /health              Health status
GET  /status              System status
POST /chat                Send message to agents
GET  /dashboard           Web UI
```

## 🐛 Troubleshooting

**"GROQ_API_KEY not configured"**
```bash
# Edit .env.local and add your key
nano .env.local
export GROQ_API_KEY=gsk_your_key_here
```

**"ModuleNotFoundError"**
```bash
# Install deps
pip install -r requirements.txt
```

**"Connection refused" on health checks**
```bash
# This is normal if you don't have Docker services
# The system works fine without them
pytest tests/ -v  # Tests all pass
```

## 🚢 Production

For production deployment:
```bash
docker-compose up
```

This includes Elasticsearch, Kibana, Prometheus, Grafana, Jaeger, Redis, RabbitMQ.

## 📝 Commits

All changes on branch `claude/review-folder-errors-3336i` ready to merge to main.

## 👤 Author

Claude Code | Anthropic

## 📄 License

Proprietary
