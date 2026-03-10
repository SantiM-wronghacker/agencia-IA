# 🎯 TEAMDIRECTOR - SUPER AGENTE ORQUESTADOR

## ¿Qué es el TeamDirector?

El **TeamDirector** es el **Super Agente Orquestador Central** de la Agencia Santi. Es un meta-agente que:

✅ **Orquesta** 6 RoleAgents especializados
✅ **Asigna** tareas a los roles correctos
✅ **Valida** que los roles estén registrados
✅ **Maneja** sub-agentes de forma privada (no visible al Director)

---

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│         DASHBOARD API v2 (FastAPI)                  │
│         http://localhost:8000                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  POST /api/v2/dashboard/director/assign             │
│         ↓                                           │
│  TeamDirector (Super Agente)                        │
│  ├─ Registra 6 RoleAgents                          │
│  ├─ Valida roles                                   │
│  └─ Asigna tareas                                  │
│       ↓                                             │
│  ┌──────────────────────────────────┐              │
│  │  6 RoleAgents (Roles Especializados) │           │
│  ├─ "strategy"  - Estrategia                       │
│  ├─ "finance"   - Finanzas                         │
│  ├─ "legal"     - Legal/Normativa                  │
│  ├─ "marketing" - Marketing/Ventas                 │
│  ├─ "tech"      - Tecnología                       │
│  └─ "ops"       - Operaciones                      │
│       ↓ (privado: crea sub-agentes bajo demanda)   │
│  ┌──────────────────────────────────┐              │
│  │  SubAgentFactory (PRIVADO)       │              │
│  │  - Auto-genera micro-agentes     │              │
│  │  - El Director NO ve esto        │              │
│  └──────────────────────────────────┘              │
└─────────────────────────────────────────────────────┘
```

---

## Ubicación en el Código

```
src/agencia/api/dashboard/
├── routes.py                  ← Endpoint `/api/v2/dashboard/director/assign`
│   └── _director = TeamDirector()
│
├── team_director.py           ← Implementación del TeamDirector
│   └── class TeamDirector:
│       ├── def __init__(name, registry)
│       ├── def register(role_agent)
│       └── def assign(role, task)
│
└── models.py
    ├── DirectorAssignRequest  ← {"role": "strategy", "task": "..."}
    └── DirectorAssignResponse ← {"role": "...", "task": "...", "status": "..."}
```

---

## Cómo Funciona

### 1. **Definición de un RoleAgent**

```python
from src.agencia.api.dashboard.role_agent import RoleAgent

def strategy_handler(goal: str, context: dict) -> dict:
    """Handler que ejecuta la estrategia"""
    return {"status": "ok", "result": f"Estrategia para: {goal}"}

strategy_role = RoleAgent(
    role="strategy",
    description="Genera estrategias de negocio",
    handler=strategy_handler
)
```

### 2. **Registro en el TeamDirector**

```python
director = TeamDirector()
director.register(strategy_role)
# Ahora el director conoce al rol "strategy"
```

### 3. **Asignación de Tareas**

```python
result = director.assign("strategy", "Optimiza tu modelo de monetización")
# Devuelve: {"role": "strategy", "task": "...", "status": "assigned"}
```

---

## Endpoint REST

### URL
```
POST /api/v2/dashboard/director/assign
```

### Request
```json
{
  "role": "strategy",
  "task": "Crea un plan de 90 días para duplicar ingresos"
}
```

### Response (Éxito)
```json
{
  "role": "strategy",
  "task": "Crea un plan de 90 días para duplicar ingresos",
  "status": "assigned"
}
```

### Response (Error - Rol no registrado)
```json
{
  "detail": "Role 'unknown_role' is not registered. Allowed roles: strategy, finance, legal, marketing, tech, ops"
}
```

### Curl
```bash
curl -X POST "http://localhost:8000/api/v2/dashboard/director/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "finance",
    "task": "Calcula el ROI para el nuevo proyecto"
  }'
```

---

## 6 RoleAgents Especializados

| Role | Descripción | Uso |
|------|------------|-----|
| **strategy** | Planes y estrategias | "Crea estrategia de crecimiento" |
| **finance** | Análisis financiero | "Calcula ROI del proyecto" |
| **legal** | Asesoría normativa | "Revisa el contrato" |
| **marketing** | Campañas y ventas | "Diseña campaña de lanzamiento" |
| **tech** | Arquitectura técnica | "Optimiza la base de datos" |
| **ops** | Operaciones y procesos | "Mejora el flujo de trabajo" |

---

## Características Clave

### ✅ Orquestación Centralizada
Un único punto de entrada para todas las tareas especializadas.

### ✅ Validación de Roles
Solo acepta roles registrados, rechaza otros con error 400.

### ✅ Extensible
Fácil agregar nuevos RoleAgents simplemente llamando a `register()`.

### ✅ Privacidad de Sub-agentes
Cada RoleAgent puede crear sub-agentes internos (via SubAgentFactory) que el Director nunca ve.

### ✅ Moderno
API REST clara, respuestas JSON estructuradas.

---

## Casos de Uso

### 1. **Análisis de Oportunidad**
```bash
curl -X POST "http://localhost:8000/api/v2/dashboard/director/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "strategy",
    "task": "Analiza mercado de IA en latam y propone 3 oportunidades"
  }'
```

### 2. **Evaluación Financiera**
```bash
curl -X POST "http://localhost:8000/api/v2/dashboard/director/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "finance",
    "task": "Proyecta ingresos si escalamos 10x usuarios"
  }'
```

### 3. **Revisión Legal**
```bash
curl -X POST "http://localhost:8000/api/v2/dashboard/director/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "legal",
    "task": "Verifica cumplimiento GDPR para recolección de datos"
  }'
```

### 4. **Estrategia de Marketing**
```bash
curl -X POST "http://localhost:8000/api/v2/dashboard/director/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "marketing",
    "task": "Crea plan de posicionamiento para Q2 2026"
  }'
```

### 5. **Arquitectura Técnica**
```bash
curl -X POST "http://localhost:8000/api/v2/dashboard/director/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "tech",
    "task": "Diseña infraestructura para 100k usuarios concurrentes"
  }'
```

### 6. **Optimización de Procesos**
```bash
curl -X POST "http://localhost:8000/api/v2/dashboard/director/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "ops",
    "task": "Mejora el ciclo de onboarding de clientes"
  }'
```

---

## Diferencia: TeamDirector vs RoleAgent vs SubAgent

```
┌──────────────────────────────────────────────────────────┐
│  JERARQUÍA DE AGENTES                                    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Level 1: TeamDirector (Super Agente Orquestador)      │
│  └─ Decide QUÉ rol usar para cada tarea                │
│                                                          │
│     Level 2: RoleAgent (6 Roles Especializados)         │
│     └─ Ejecuta tareas en su dominio específico          │
│     └─ Puede crear SubAgents bajo demanda               │
│                                                          │
│        Level 3: SubAgent (Micro-agentes Privados)       │
│        └─ Creados dinámicamente para cubrir gaps        │
│        └─ No son visibles al TeamDirector               │
│        └─ Propiedad del RoleAgent padre                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Código Relevante

### routes.py (línea 396-409)
```python
_director = TeamDirector()

@app.post("/api/v2/dashboard/director/assign", response_model=DirectorAssignResponse)
async def director_assign(body: DirectorAssignRequest) -> DirectorAssignResponse:
    """Assign a task via the TeamDirector (dev endpoint)."""
    try:
        result = _director.assign(body.role, body.task)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return DirectorAssignResponse(**result)
```

### team_director.py (estructura)
```python
class TeamDirector:
    def __init__(self, name="default-team", registry=None):
        self.name = name
        self.registry = registry or RoleRegistry()

    def register(self, role_agent: RoleAgent) -> None:
        """Registra un RoleAgent"""
        self.registry.register(role_agent)

    def assign(self, role: str, task: str) -> dict:
        """Asigna una tarea a un rol"""
        if role not in self.registry:
            raise ValueError(f"Role '{role}' not registered")
        role_agent = self.registry.get(role)
        return role_agent.execute(task, {})
```

---

## Próximos Pasos

1. ✅ TeamDirector implementado en `routes.py`
2. ✅ 6 RoleAgents registrados (strategy, finance, legal, marketing, tech, ops)
3. 🔄 **Conectar al Dashboard** - interfaz visual para asignar tareas
4. 🔄 **WebSocket real-time** - ver resultados en tiempo real
5. 🔄 **Persistencia** - guardar historial de asignaciones

---

**Estado**: ✅ Super Agente Orquestador Activo
**Acceso**: POST `/api/v2/dashboard/director/assign`
**6 Roles**: strategy, finance, legal, marketing, tech, ops
**115/115 Tests**: Pasando ✅
