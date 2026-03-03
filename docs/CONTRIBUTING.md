# Contribuir a Agencia IA

## Cómo Agregar un Nuevo Agente

### 1. Crear el archivo

Coloca tu agente en la categoría correcta:

```
src/agencia/agents/<categoría>/mi_agente.py
```

### 2. Heredar de BaseAgent

```python
from src.agencia.core.base_agent import BaseAgent


class MiAgente(BaseAgent):
    def __init__(self):
        super().__init__(
            name="mi_agente",
            category="herramientas",
            description="Descripción de lo que hace",
            version="1.0.0",
            preferred_model="groq",
        )

    def execute(self, input_data):
        query = input_data.get("query", "")
        # Tu lógica aquí
        return {"result": "..."}

    def get_capabilities(self):
        return ["mi_capacidad_1", "mi_capacidad_2"]
```

### 3. Agregar tests

```python
# tests/unit/test_mi_agente.py
from src.agencia.agents.herramientas.mi_agente import MiAgente


def test_mi_agente():
    agent = MiAgente()
    result = agent.run({"query": "test"})
    assert "result" in result
```

### 4. Registrar en el registry

```python
from src.agencia.core.agent_registry import registry

agent = MiAgente()
registry.register(
    name=agent.name,
    category=agent.category,
    capabilities=agent.get_capabilities(),
    instance=agent,
)
```

## Estándares de Código

- **Formateo**: `black` con línea máxima de 120
- **Linting**: `flake8` con línea máxima de 120
- **Types**: `mypy` para type checking
- **Tests**: `pytest` con coverage > 80%

```bash
# Formatear código
black src/ tests/

# Verificar linting
flake8 src/ tests/ --max-line-length=120

# Type checking
mypy src/agencia/core/ --ignore-missing-imports

# Correr tests
pytest tests/ -v --cov=src/agencia
```

## Proceso de PR

1. Crear branch desde `main`: `git checkout -b feature/mi-agente`
2. Hacer cambios y agregar tests
3. Correr linting y tests localmente
4. Crear Pull Request
5. CI/CD corre automáticamente (lint, test, build)
6. Revisión de código
7. Merge a `main`
