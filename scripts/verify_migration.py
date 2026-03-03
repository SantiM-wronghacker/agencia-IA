#!/usr/bin/env python3
"""
Verification script: validate that all imports work, no broken references,
and all tests pass after migration.

Checks performed:
  1. All Python files under ``src/`` can be imported without errors.
  2. The six updated core files (api.py, api_agencia.py, app.py,
     app_dashboard.py, celery_app.py, sistema_maestro.py) parse without
     syntax errors and their imports resolve.
  3. No Python file references a module that doesn't exist.
  4. pytest suite passes.

Usage:
    python scripts/verify_migration.py
"""

import ast
import importlib
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

CORE_FILES = [
    "api.py",
    "api_agencia.py",
    "app.py",
    "app_dashboard.py",
    "celery_app.py",
    "sistema_maestro.py",
]


def check_syntax(py_file: Path) -> bool:
    """Return True if *py_file* has valid Python syntax."""
    try:
        ast.parse(py_file.read_text(encoding="utf-8", errors="replace"))
        return True
    except SyntaxError as exc:
        print(f"  SYNTAX ERROR in {py_file.relative_to(REPO_ROOT)}: {exc}")
        return False


def check_imports(py_file: Path) -> list:
    """Return list of import targets that appear to reference local modules."""
    source = py_file.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split(".")[0])
    return imports


def verify_src_importable():
    """Try to import every module under src/."""
    src_dir = REPO_ROOT / "src"
    if not src_dir.exists():
        print("  WARNING: src/ directory not found. Migration may not have run yet.")
        return False

    ok = True
    for py in sorted(src_dir.rglob("*.py")):
        if py.name == "__init__.py":
            continue
        rel = py.relative_to(REPO_ROOT)
        module_path = ".".join(rel.with_suffix("").parts)
        try:
            importlib.import_module(module_path)
        except Exception as exc:
            print(f"  IMPORT ERROR: {module_path} → {exc}")
            ok = False
    return ok


def verify_core_syntax():
    """Parse the six core files for syntax errors."""
    ok = True
    for fname in CORE_FILES:
        fpath = REPO_ROOT / fname
        if fpath.exists():
            if not check_syntax(fpath):
                ok = False
        else:
            print(f"  WARNING: {fname} not found.")
    return ok


def verify_no_broken_refs():
    """Check that imported local modules exist as files or packages."""
    stdlib_top = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else set()
    ok = True
    for py in sorted(REPO_ROOT.rglob("*.py")):
        if ".venv" in py.parts or "venv" in py.parts or "__pycache__" in py.parts:
            continue
        for mod in check_imports(py):
            if mod in stdlib_top:
                continue
            # Check if it exists as a file or package at repo root
            as_file = REPO_ROOT / f"{mod}.py"
            as_pkg = REPO_ROOT / mod / "__init__.py"
            as_src = REPO_ROOT / "src" / mod
            if not (as_file.exists() or as_pkg.exists() or as_src.exists()):
                # Could be a third-party package, skip if installable
                try:
                    importlib.import_module(mod)
                except ImportError:
                    print(f"  BROKEN REF: {py.relative_to(REPO_ROOT)} imports '{mod}' — not found")
                    ok = False
    return ok


def run_tests():
    """Run pytest and return True if all tests pass."""
    print("\nRunning pytest...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return False
    return True


def main():
    print("=" * 60)
    print("  Migration Verification")
    print("=" * 60)

    results = {}

    print("\n1. Checking core file syntax...")
    results["syntax"] = verify_core_syntax()

    print("\n2. Checking src/ importability...")
    results["src_imports"] = verify_src_importable()

    print("\n3. Checking for broken references...")
    results["refs"] = verify_no_broken_refs()

    print("\n4. Running tests...")
    results["tests"] = run_tests()

    print("\n" + "=" * 60)
    print("  Results")
    print("=" * 60)
    all_ok = True
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}  {check}")
        if not passed:
            all_ok = False

    if all_ok:
        print("\n  All checks passed! Migration is valid.")
    else:
        print("\n  Some checks failed. Review the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
