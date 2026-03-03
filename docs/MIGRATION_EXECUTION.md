# Migration Execution Guide

Step-by-step guide to execute the Agencia Santi modernisation migration.

## Prerequisites

- Python 3.10+
- All dependencies installed: `pip install -r requirements.txt`
- Repository cloned and on the migration branch

## Step 1 — Consolidate Routers

Merge the four router implementations into `src/agencia/core/router.py`:

```bash
# Dry-run (shows what would change, no files touched)
python scripts/consolidate_routers.py

# Execute
python scripts/consolidate_routers.py --execute
```

## Step 2 — Migrate Files to src/

Move 300+ Python files from the root into `src/agencia/agents/<category>/`
and rewrite every import automatically:

```bash
# Dry-run
python scripts/migrate_to_src.py

# Execute
python scripts/migrate_to_src.py --execute
```

## Step 3 — Verify Migration

Run the automated verification script that checks syntax, imports,
references, and the full test suite:

```bash
python scripts/verify_migration.py
```

## Step 4 — Run Tests

```bash
python -m pytest tests/ -v
```

Expected: all tests pass (core, router, escalation, API).

## Step 5 — Start Services with Docker

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for full Docker instructions.

```bash
cp .env.example .env        # configure API keys
docker-compose up -d         # start all services
docker-compose ps            # verify containers are running
```

## Step 6 — Post-Migration Cleanup

After verifying everything works:

1. Remove the original flat files that were copied into `src/`:
   ```bash
   # Only after confirming tests pass with the new structure
   git rm calculadora_*.py generador_*.py analizador_*.py  # etc.
   ```
2. Commit the cleanup.

## Rollback

If anything goes wrong, revert to the pre-migration commit:

```bash
git log --oneline -5          # find the commit before migration
git revert <commit_sha>       # create a revert commit
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` after migration | Run `python scripts/verify_migration.py` to find broken refs |
| Tests fail with import errors | Ensure `src/` is on `PYTHONPATH`: `export PYTHONPATH=.` |
| Docker services won't start | Check `.env` has valid API keys; see `docker-compose logs` |
