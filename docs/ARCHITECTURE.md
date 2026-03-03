# Arquitectura - Agencia IA

## Visión General

Agencia IA es un sistema multi-agente compuesto por 510+ agentes especializados, organizados en 19 categorías empresariales. El sistema utiliza una arquitectura de microservicios con Docker Compose.

## Diagrama de Arquitectura

```
                    ┌─────────────┐
                    │   Nginx     │ :80
                    │  (Gateway)  │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
   ┌──────▼──────┐ ┌──────▼──────┐ ┌───────▼─────┐
   │ API Agencia │ │ Dashboard   │ │ Streamlit   │
   │   :8000     │ │  Web :8080  │ │   :8501     │
   └──────┬──────┘ └─────────────┘ └─────────────┘
          │
   ┌──────▼──────┐
   │   Core      │
   │  Modules    │
   ├─────────────┤
   │BaseAgent    │
   │AgentRegistry│
   │DynamicRouter│
   │Orchestrator │
   │LLMRouter    │
   └──────┬──────┘
          │
   ┌──────▼──────┐    ┌──────────────┐
   │ PostgreSQL  │    │    Redis     │
   │    :5432    │    │   :6379     │
   └─────────────┘    └──────────────┘
          │
   ┌──────▼──────┐    ┌──────────────┐
   │  RabbitMQ   │    │   Celery    │
   │    :5672    │    │  Workers    │
   └─────────────┘    └──────────────┘

   ┌──────────────────────────────────┐
   │        Observabilidad            │
   ├──────────┬───────────┬───────────┤
   │Prometheus│  Grafana  │  Jaeger   │
   │  :9090   │   :3000   │  :16686   │
   ├──────────┴───────────┴───────────┤
   │  Elasticsearch :9200 + Kibana    │
   └──────────────────────────────────┘
```

## Flujo de Datos

1. **Request → Nginx** - API Gateway recibe la solicitud
2. **Nginx → API** - Se enruta al servicio apropiado
3. **API → DynamicRouter** - El router identifica la categoría
4. **DynamicRouter → AgentRegistry** - Busca el mejor agente disponible
5. **AgentRegistry → BaseAgent** - Ejecuta el agente seleccionado
6. **BaseAgent → LLMRouter** - Selecciona el modelo IA apropiado
7. **LLMRouter → Provider** - Llama al proveedor de IA (OpenAI, Groq, etc.)
8. **Response → Cliente** - Retorna el resultado

## Cómo Agregar un Nuevo Agente

1. Crear archivo en la categoría correspondiente (`src/agencia/agents/<categoria>/`)
2. Heredar de `BaseAgent`
3. Implementar el método `execute()`
4. Registrar en el `AgentRegistry`

```python
from src.agencia.core.base_agent import BaseAgent

class MiNuevoAgente(BaseAgent):
    def execute(self, input_data):
        query = input_data.get("query", "")
        # Lógica del agente
        return {"result": "..."}

    def get_capabilities(self):
        return ["mi_capacidad"]
```

## Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Runtime | Python | 3.13 |
| Base de datos | PostgreSQL | 15 |
| Cache | Redis | 7 |
| Message Broker | RabbitMQ | 3.12 |
| API Gateway | Nginx | 1.25 |
| Metrics | Prometheus | 2.48 |
| Dashboards | Grafana | 10.2 |
| Tracing | Jaeger | 1.51 |
| Logs | Elasticsearch + Kibana | 8.11 |
| CI/CD | GitHub Actions | - |
