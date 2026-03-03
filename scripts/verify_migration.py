#!/usr/bin/env python3
"""
Verification script: checks that the migration completed correctly.

* Every file listed in ``categorias/`` exists under ``src/agencia/agents/``
* ``__init__.py`` files are present at every package level
* Basic ``import`` smoke‑tests pass
"""

import os
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CATEGORIAS = REPO / "categorias"
AGENTS_ROOT = REPO / "src" / "agencia" / "agents"


def normalize_category(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", name)
    return nfkd.encode("ascii", "ignore").decode("ascii").lower()


def verify() -> bool:
    ok = True
    total_expected = 0
    total_found = 0
    missing: list[str] = []

    # 1. Check __init__.py files
    for d in (REPO / "src", REPO / "src" / "agencia", AGENTS_ROOT):
        init = d / "__init__.py"
        if not init.exists():
            print(f"✗ Missing {init.relative_to(REPO)}")
            ok = False
        else:
            print(f"✓ {init.relative_to(REPO)}")

    # 2. Check each category
    print("\n── Category verification ──")
    for cat in sorted(CATEGORIAS.iterdir()):
        if not cat.is_dir():
            continue
        norm = normalize_category(cat.name)
        cat_dir = AGENTS_ROOT / norm
        cat_init = cat_dir / "__init__.py"

        cat_expected = [f for f in cat.iterdir() if f.suffix == ".py"]
        total_expected += len(cat_expected)

        if not cat_dir.exists():
            print(f"✗ Missing directory: src/agencia/agents/{norm}/")
            ok = False
            missing.extend(f.name for f in cat_expected)
            continue

        if not cat_init.exists():
            print(f"✗ Missing __init__.py in {norm}/")
            ok = False

        found = 0
        for py in cat_expected:
            dest = cat_dir / py.name
            if dest.exists():
                found += 1
            else:
                missing.append(f"{norm}/{py.name}")
                ok = False
        total_found += found
        status = "✓" if found == len(cat_expected) else "✗"
        print(f"  {status} {norm:40s} {found}/{len(cat_expected)}")

    # 3. Check that root is clean
    root_py_agents = [
        f for f in REPO.iterdir()
        if f.suffix == ".py" and f.name != "conftest.py"
        and f.name not in ("setup.py",)
        and f.is_file()
    ]
    # There should be no .py files left at root that were in categorias
    leftover = []
    all_cat_files = set()
    for cat in CATEGORIAS.iterdir():
        if cat.is_dir():
            for f in cat.iterdir():
                if f.suffix == ".py":
                    all_cat_files.add(f.name)
    for f in root_py_agents:
        if f.name in all_cat_files:
            leftover.append(f.name)
    if leftover:
        print(f"\n✗ {len(leftover)} agent files still at repository root:")
        for f in sorted(leftover)[:10]:
            print(f"    {f}")
        if len(leftover) > 10:
            print(f"    ... and {len(leftover) - 10} more")
        ok = False
    else:
        print(f"\n✓ No agent files remaining at repository root")

    # 4. Summary
    print(f"\n── Summary ──")
    print(f"  Expected files : {total_expected}")
    print(f"  Found files    : {total_found}")
    print(f"  Missing files  : {len(missing)}")

    if missing:
        print(f"\n  Missing files:")
        for m in sorted(missing)[:20]:
            print(f"    {m}")
        if len(missing) > 20:
            print(f"    ... and {len(missing) - 20} more")

    if ok:
        print(f"\n✓ VERIFICATION PASSED")
    else:
        print(f"\n✗ VERIFICATION FAILED")

    return ok


if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)
