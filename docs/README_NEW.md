# 🏢 Agencia IA

> Plataforma multi-agente de IA con 510+ agentes especializados en 19 categorías, diseñada para automatizar operaciones empresariales.

[![CI](https://github.com/SantiM-wronghacker/agencia-IA/actions/workflows/ci.yml/badge.svg)](https://github.com/SantiM-wronghacker/agencia-IA/actions/workflows/ci.yml)

## ✨ Features

- **510+ Agentes Especializados** organizados en 19 categorías (finanzas, legal, ventas, marketing, etc.)
- **Multi-Modelo IA** - Soporte para GPT-4o, Claude, Groq, Mistral, Gemini, Cerebras
- **Dynamic Router** - Routing inteligente por categoría, capacidad y semántica
- **Observabilidad Completa** - Prometheus + Grafana + Jaeger + ELK Stack
- **Docker Compose** - Infraestructura completa en un solo comando
- **CI/CD** - GitHub Actions para lint, test y deploy automático

## 🚀 Quick Start

```bash
# 1. Clonar el repositorio
git clone https://github.com/SantiM-wronghacker/agencia-IA.git
cd agencia-IA

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# 3. Levantar todo con Docker Compose
docker-compose up -d

# 4. Verificar que todo está corriendo
docker-compose ps
```

### Servicios disponibles:

| Servicio | Puerto | URL |
|----------|--------|-----|
| API Agencia | 8000 | http://localhost:8000 |
| Dashboard Web | 8080 | http://localhost:8080 |
| App Dashboard | 5000 | http://localhost:5000 |
| Streamlit | 8501 | http://localhost:8501 |
| Nginx Gateway | 80 | http://localhost |
| Grafana | 3000 | http://localhost:3000 |
| Prometheus | 9090 | http://localhost:9090 |
| Jaeger | 16686 | http://localhost:16686 |
| Kibana | 5601 | http://localhost:5601 |
| RabbitMQ Management | 15672 | http://localhost:15672 |

## 📁 Estructura del Proyecto

```
agencia-IA/
├── docker-compose.yml          # Infraestructura completa
├── docker/                     # Dockerfiles para cada servicio
│   ├── Dockerfile.api
│   ├── Dockerfile.dashboard
│   ├── Dockerfile.app
│   ├── Dockerfile.streamlit
│   ├── Dockerfile.celery
│   ├── Dockerfile.maestro
│   └── Dockerfile.health
├── nginx/nginx.conf            # API Gateway
├── database/
│   ├── schema.sql              # Schema PostgreSQL
│   └── migrations/             # Migraciones
├── monitoring/
│   └── prometheus/prometheus.yml
├── src/agencia/
│   ├── core/                   # Módulos core
│   │   ├── base_agent.py       # Clase base para todos los agentes
│   │   ├── agent_registry.py   # Registry centralizado
│   │   ├── router.py           # Dynamic Router
│   │   ├── orchestrator.py     # Orquestador multi-agente
│   │   ├── llm_router_mejorado.py  # Router multi-modelo
│   │   ├── logging_config.py   # Logging JSON centralizado
│   │   ├── metrics.py          # Métricas Prometheus
│   │   └── health_check.py     # Health checks
│   ├── models/                 # ORM models
│   └── agents/                 # 510+ agentes organizados
│       ├── cerebro/            # Agentes de orquestación
│       ├── finanzas/           # Agentes financieros
│       ├── herramientas/       # Herramientas y utilidades
│       ├── legal/              # Agentes legales
│       ├── ventas/             # Agentes de ventas
│       └── ...                 # 14 categorías más
├── tests/
│   ├── unit/                   # Tests unitarios
│   ├── integration/            # Tests de integración
│   └── e2e/                    # Tests end-to-end
├── docs/                       # Documentación
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── API.md
│   ├── AGENTS.md
│   └── CONTRIBUTING.md
└── .github/workflows/          # CI/CD
    ├── ci.yml
    └── deploy.yml
```

## 🧪 Testing

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest tests/ -v

# Con coverage
pytest tests/ -v --cov=src/agencia --cov-report=term-missing
```

## 🤖 Categorías de Agentes

| Categoría | Agentes | Modelo Preferido |
|-----------|---------|------------------|
| Cerebro | 51 | Claude (Anthropic) |
| Finanzas | 73 | GPT-4o (OpenAI) |
| Herramientas | 158 | Groq (Llama 3.3) |
| Contabilidad | 21 | GPT-4o (OpenAI) |
| Legal | 16 | GPT-4o (OpenAI) |
| Operaciones | 17 | Groq (Llama 3.3) |
| Real Estate | 20 | Groq (Llama 3.3) |
| Ventas | 24 | Mistral Large |
| Recursos Humanos | 17 | Mistral Large |
| Marketing | 18 | Mistral Large |
| + 9 más | ... | ... |

## 📖 Documentación

- [Arquitectura](docs/ARCHITECTURE.md) - Diagrama y flujo del sistema
- [Deployment](docs/DEPLOYMENT.md) - Guía de despliegue
- [API](docs/API.md) - Endpoints y ejemplos
- [Agentes](docs/AGENTS.md) - Catálogo de agentes
- [Contribuir](docs/CONTRIBUTING.md) - Guía de contribución
- [Migración](MIGRATION_GUIDE.md) - Guía de migración

## 📄 Licencia

Proyecto privado - Todos los derechos reservados.
