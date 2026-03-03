# Guía de Migración - Agencia IA

## De Monolítico a Microservicios

Esta guía explica cómo migrar del sistema monolítico actual a la nueva arquitectura con Docker y microservicios.

## Cambios Principales

### 1. Nueva Estructura de Directorios

**Antes:**
```
agencia-IA/
├── calculadora_roi.py          # ~300 scripts en raíz
├── generador_contrato.py
├── analizador_flujo_caja.py
└── ...
```

**Después:**
```
agencia-IA/
├── src/agencia/agents/         # Agentes organizados por categoría
│   ├── finanzas/
│   │   ├── calculators/
│   │   └── analyzers/
│   ├── legal/
│   └── ...
├── src/agencia/core/           # Módulos centrales
│   ├── base_agent.py
│   ├── agent_registry.py
│   ├── router.py
│   └── ...
├── docker-compose.yml
└── database/schema.sql
```

### 2. BaseAgent

Todos los agentes ahora heredan de `BaseAgent`, que proporciona:
- Logging automático
- Métricas automáticas
- Caching de resultados
- Error handling estándar

### 3. AgentRegistry

Sistema centralizado para registrar y descubrir agentes:
- Registro por nombre, categoría y capacidades
- Búsqueda semántica
- Tracking de ejecuciones
- Health checks

### 4. Docker Compose

Todo se ejecuta con un solo comando:
```bash
docker-compose up -d
```

### 5. Base de Datos

Migración de SQLite a PostgreSQL:
- Schema en `database/schema.sql`
- Ejecutado automáticamente al iniciar PostgreSQL

## Pasos de Migración

1. **Configurar entorno**: `cp .env.example .env`
2. **Levantar infraestructura**: `docker-compose up -d postgres redis rabbitmq`
3. **Ejecutar migraciones**: Schema se aplica automáticamente
4. **Levantar servicios**: `docker-compose up -d`
5. **Verificar**: `docker-compose ps`

## Compatibilidad

Los scripts existentes en la raíz siguen funcionando. La nueva estructura en `src/agencia/` es una adición, no un reemplazo.
