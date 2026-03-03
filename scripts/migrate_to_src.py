#!/usr/bin/env python3
"""
Migration script: move Python files from root to src/agencia/agents/[categoria]/.

Scans all *.py files at the repository root, classifies each one into a
category based on its filename prefix, copies it into the corresponding
``src/agencia/agents/<category>/`` directory, and rewrites imports in every
Python file so that ``from <old_module> import X`` becomes
``from src.agencia.agents.<category>.<old_module> import X``.

Usage:
    python scripts/migrate_to_src.py            # dry-run (default)
    python scripts/migrate_to_src.py --execute   # perform the migration

The script is idempotent — running it twice has no additional effect.
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

# ── Category rules ────────────────────────────────────────────────────
# Prefix → category mapping.  Order matters: first match wins.
CATEGORY_RULES = [
    ("agent_router", "core"),
    ("core", "core"),
    ("config", "core"),
    ("llm_router", "core"),
    ("logging_config", "core"),
    ("bus_mensajes", "core"),
    ("root_assistant", "core"),
    ("database", "core"),
    ("rag_", "rag"),
    ("calculadora_", "calculadoras"),
    ("generador_", "generadores"),
    ("analizador_", "analizadores"),
    ("simulador_", "simuladores"),
    ("gestor_", "gestores"),
    ("monitor_", "monitores"),
    ("sistema_", "sistema"),
    ("api", "api"),
    ("app", "api"),
    ("web_bridge", "api"),
    ("celery_app", "herramientas"),
]

# Files that should stay at root (entry-points, configs, etc.)
KEEP_AT_ROOT = {
    "setup.py",
    "conftest.py",
    "__init__.py",
}


def classify(filename: str) -> str:
    """Return the target category for a Python file."""
    for prefix, category in CATEGORY_RULES:
        if filename.startswith(prefix):
            return category
    return "otros"


def collect_root_py_files(repo_root: Path):
    """Yield (Path, category) for every *.py file at the repo root."""
    for p in sorted(repo_root.glob("*.py")):
        if p.name in KEEP_AT_ROOT:
            continue
        yield p, classify(p.stem)


def build_import_map(repo_root: Path):
    """Return a dict  {old_module_name: 'src.agencia.agents.<cat>.<mod>'}."""
    mapping = {}
    for src_file, category in collect_root_py_files(repo_root):
        old = src_file.stem
        mapping[old] = f"src.agencia.agents.{category}.{old}"
    return mapping


def rewrite_imports(file_path: Path, mapping: dict) -> str:
    """Return the rewritten source of *file_path* with updated imports."""
    text = file_path.read_text(encoding="utf-8", errors="replace")
    # Match  from <module> import …  and  import <module>
    for old, new in mapping.items():
        text = re.sub(
            rf"^(from\s+){re.escape(old)}(\s+import\s)",
            rf"\g<1>{new}\2",
            text,
            flags=re.MULTILINE,
        )
        text = re.sub(
            rf"^(import\s+){re.escape(old)}(\s|$|,)",
            rf"\g<1>{new}\2",
            text,
            flags=re.MULTILINE,
        )
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually perform the migration (default is dry-run).",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    src_agents = repo_root / "src" / "agencia" / "agents"

    # ── Collect files ──
    files = list(collect_root_py_files(repo_root))
    mapping = build_import_map(repo_root)

    print(f"Found {len(files)} Python files to migrate.")
    categories = {}
    for _, cat in files:
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} files")

    if not args.execute:
        print("\nDry-run complete.  Re-run with --execute to apply changes.")
        return

    # ── Create directories & copy files ──
    for src_file, category in files:
        dest_dir = src_agents / category
        dest_dir.mkdir(parents=True, exist_ok=True)
        init = dest_dir / "__init__.py"
        if not init.exists():
            init.write_text("", encoding="utf-8")
        dest = dest_dir / src_file.name
        if not dest.exists():
            shutil.copy2(src_file, dest)
            print(f"  Copied {src_file.name} → {dest.relative_to(repo_root)}")

    # ── Rewrite imports in ALL Python files ──
    all_py = list(repo_root.rglob("*.py"))
    for py_file in all_py:
        original = py_file.read_text(encoding="utf-8", errors="replace")
        updated = rewrite_imports(py_file, mapping)
        if updated != original:
            py_file.write_text(updated, encoding="utf-8")
            print(f"  Updated imports in {py_file.relative_to(repo_root)}")

    print(f"\nMigration complete. {len(files)} files moved, imports updated.")


if __name__ == "__main__":
    main()
