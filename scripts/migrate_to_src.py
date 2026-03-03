#!/usr/bin/env python3
"""
Migration script: moves all Python agent files from the repository root
into the ``src/agencia/agents/<category>/`` package structure.

The mapping of *file → category* is read from the existing ``categorias/``
directory that was prepared in a previous step.

After moving, every internal ``from <module> import …`` / ``import <module>``
statement is rewritten to use the fully‑qualified package path.
"""

import os
import re
import shutil
import unicodedata
from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parent.parent
CATEGORIAS = REPO / "categorias"
SRC_ROOT = REPO / "src"
PKG_ROOT = SRC_ROOT / "agencia"
AGENTS_ROOT = PKG_ROOT / "agents"

# ── helpers ────────────────────────────────────────────────────────────────

def normalize_category(name: str) -> str:
    """BIENES_RAÍCES_COMERCIALES → bienes_raices_comerciales"""
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_name = nfkd.encode("ascii", "ignore").decode("ascii")
    return ascii_name.lower()


def build_module_to_category() -> dict[str, str]:
    """Return {module_name: normalized_category} from categorias/."""
    mapping: dict[str, str] = {}
    for cat in sorted(CATEGORIAS.iterdir()):
        if not cat.is_dir():
            continue
        norm = normalize_category(cat.name)
        for py in cat.glob("*.py"):
            mod = py.stem
            mapping[mod] = norm
    return mapping


def create_package_dirs(categories: set[str]) -> None:
    """Create __init__.py at every level of the package tree."""
    for d in (SRC_ROOT, PKG_ROOT, AGENTS_ROOT):
        d.mkdir(parents=True, exist_ok=True)
        init = d / "__init__.py"
        if not init.exists():
            init.write_text("")

    for cat in sorted(categories):
        cat_dir = AGENTS_ROOT / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        init = cat_dir / "__init__.py"
        if not init.exists():
            init.write_text("")


def move_files(mapping: dict[str, str]) -> list[tuple[str, str, str]]:
    """Move each .py from repo root → src/agencia/agents/<cat>/
    Returns list of (module, category, dest_path) tuples."""
    moved: list[tuple[str, str, str]] = []
    for mod, cat in sorted(mapping.items()):
        src = REPO / f"{mod}.py"
        if not src.exists():
            continue
        dest_dir = AGENTS_ROOT / cat
        dest = dest_dir / f"{mod}.py"
        shutil.move(str(src), str(dest))
        moved.append((mod, cat, str(dest)))
    return moved


# ── import rewriting ───────────────────────────────────────────────────────

# Patterns we rewrite:
#   from <mod> import …
#   import <mod>
#   import <mod> as …
# We intentionally skip relative imports (from . import …) and stdlib/third-party.

_FROM_RE = re.compile(
    r"^(\s*from\s+)([A-Za-z_]\w*)(\s+import\s+.*)$"
)
_IMPORT_RE = re.compile(
    r"^(\s*import\s+)([A-Za-z_]\w*)(\s*(?:as\s+\w+)?\s*)$"
)


def rewrite_imports_in_file(filepath: Path, mapping: dict[str, str]) -> int:
    """Rewrite internal imports in *filepath*.  Returns count of changes."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return 0

    lines = text.splitlines(keepends=True)
    changes = 0
    new_lines: list[str] = []

    for line in lines:
        m = _FROM_RE.match(line)
        if m:
            mod = m.group(2)
            if mod in mapping:
                cat = mapping[mod]
                new_line = f"{m.group(1)}agencia.agents.{cat}.{mod}{m.group(3)}"
                if not new_line.endswith("\n") and line.endswith("\n"):
                    new_line += "\n"
                new_lines.append(new_line)
                changes += 1
                continue

        m = _IMPORT_RE.match(line)
        if m:
            mod = m.group(2)
            if mod in mapping:
                cat = mapping[mod]
                new_line = f"{m.group(1)}agencia.agents.{cat}.{mod}{m.group(3)}"
                if not new_line.endswith("\n") and line.endswith("\n"):
                    new_line += "\n"
                new_lines.append(new_line)
                changes += 1
                continue

        new_lines.append(line)

    if changes:
        filepath.write_text("".join(new_lines), encoding="utf-8")

    return changes


def rewrite_all_imports(mapping: dict[str, str]) -> int:
    """Walk every .py under src/agencia/ and rewrite imports."""
    total = 0
    for py in sorted(AGENTS_ROOT.rglob("*.py")):
        total += rewrite_imports_in_file(py, mapping)
    # Also rewrite tests
    tests_dir = REPO / "tests"
    if tests_dir.exists():
        for py in sorted(tests_dir.rglob("*.py")):
            total += rewrite_imports_in_file(py, mapping)
    return total


# ── main ───────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print("  Migration: root → src/agencia/agents/<category>/")
    print("=" * 60)

    # 1. Build mapping
    mapping = build_module_to_category()
    categories = set(mapping.values())
    print(f"\n✓ Built mapping: {len(mapping)} modules → {len(categories)} categories")

    # 2. Create package directories
    create_package_dirs(categories)
    print("✓ Created package directory structure under src/agencia/agents/")

    # 3. Move files
    moved = move_files(mapping)
    print(f"✓ Moved {len(moved)} files")

    # 4. Rewrite imports
    import_changes = rewrite_all_imports(mapping)
    print(f"✓ Rewrote {import_changes} import statements")

    # 5. Summary by category
    print("\n── Files by category ──")
    cat_counts: dict[str, int] = {}
    for _, cat, _ in moved:
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    for cat in sorted(cat_counts):
        print(f"  {cat:40s} {cat_counts[cat]:>4d}")
    print(f"  {'TOTAL':40s} {len(moved):>4d}")

    print(f"\n✓ Migration complete.  Run scripts/verify_migration.py to verify.")


if __name__ == "__main__":
    main()
