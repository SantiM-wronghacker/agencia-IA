# Validation Checklist

Use this checklist to confirm that the migration was successful.

## Pre-Migration

- [ ] Repository cloned and on the correct branch
- [ ] Python 3.10+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` configured with valid API keys

## File Migration

- [ ] `scripts/migrate_to_src.py --execute` completed without errors
- [ ] Files moved to `src/agencia/agents/<category>/`
- [ ] `__init__.py` created in every new package directory
- [ ] No Python files left orphaned at root (except entry-points)

## Router Consolidation

- [ ] `scripts/consolidate_routers.py --execute` completed without errors
- [ ] `src/agencia/core/router.py` contains `DynamicRouter` class
- [ ] `DynamicRouter` exposes: `route_intent`, `dispatch`, `load_state`, `save_state`
- [ ] No duplicate function definitions across router files

## Imports Updated

- [ ] `api.py` — imports from `src.agencia.core.router`
- [ ] `api_agencia.py` — imports from `src.agencia.core.router`
- [ ] `app.py` — imports from `src.agencia.core.router`
- [ ] `app_dashboard.py` — imports from `src.agencia.core.router`
- [ ] `celery_app.py` — imports from `src.agencia.core.router`
- [ ] `sistema_maestro.py` — imports from `src.agencia.core.router`

## Tests Pass

- [ ] `pytest tests/test_core.py` — all pass
- [ ] `pytest tests/test_router.py` — all pass
- [ ] `pytest tests/test_escalation.py` — all pass
- [ ] `pytest tests/test_api.py` — all pass (or known pre-existing failures documented)
- [ ] `python scripts/verify_migration.py` — all checks pass

## Docker Running

- [ ] `.env.example` copied to `.env` and configured
- [ ] `docker-compose up -d` starts all services
- [ ] `curl http://localhost:8000/health` returns `{"status": "ok", ...}`
- [ ] Dashboard accessible at `http://localhost:5000`
- [ ] Redis reachable at `localhost:6379`

## No Duplicates

- [ ] No duplicate function names across `src/agencia/core/router.py`
- [ ] No duplicate system-prompt constants
- [ ] No orphaned import aliases pointing to removed files

## Final Verification

- [ ] `python scripts/verify_migration.py` passes all 4 checks:
  - Syntax ✓
  - src/ importability ✓
  - No broken references ✓
  - Tests ✓
