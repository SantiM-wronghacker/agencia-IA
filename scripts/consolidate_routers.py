#!/usr/bin/env python3
"""
Consolidation script: merge the four agent-router files into one.

Source files:
  - agent_router.py
  - agent_router_memory.py
  - agent_router_memory_pro.py
  - agent_router_state_pro.py

Target:
  - src/agencia/core/router.py   (DynamicRouter class already scaffolded)

The script reads the source files, extracts unique helper functions and
constants that are NOT yet present in the target, and appends them under a
clearly marked section.  Duplicate definitions are skipped.

Usage:
    python scripts/consolidate_routers.py            # dry-run
    python scripts/consolidate_routers.py --execute   # apply
"""

import argparse
import ast
import sys
from pathlib import Path


def extract_top_level_names(source: str):
    """Return a set of top-level function/class/assignment names."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    names = set()
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
        elif isinstance(node, ast.ClassDef):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
    return names


SOURCE_FILES = [
    "agent_router.py",
    "agent_router_memory.py",
    "agent_router_memory_pro.py",
    "agent_router_state_pro.py",
]

TARGET_FILE = Path("src") / "agencia" / "core" / "router.py"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually perform the consolidation (default is dry-run).",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    target = repo_root / TARGET_FILE

    if not target.exists():
        print(f"ERROR: Target {TARGET_FILE} does not exist. "
              "Run this after creating the src/ package structure.")
        sys.exit(1)

    target_source = target.read_text(encoding="utf-8")
    existing_names = extract_top_level_names(target_source)
    print(f"Target already defines {len(existing_names)} symbols:")
    for n in sorted(existing_names):
        print(f"  - {n}")

    extras = []  # (source_file, name, code_block)
    for fname in SOURCE_FILES:
        src_path = repo_root / fname
        if not src_path.exists():
            print(f"  SKIP (not found): {fname}")
            continue

        source = src_path.read_text(encoding="utf-8", errors="replace")
        names = extract_top_level_names(source)
        new_names = names - existing_names

        if new_names:
            print(f"\n  {fname} has {len(new_names)} NEW symbols:")
            for n in sorted(new_names):
                print(f"    + {n}")
                extras.append((fname, n))
                existing_names.add(n)
        else:
            print(f"\n  {fname}: all symbols already consolidated.")

    if not extras:
        print("\nNo new symbols to consolidate. Target is up to date.")
        return

    if not args.execute:
        print(f"\nDry-run: {len(extras)} new symbols found. "
              "Re-run with --execute to apply.")
        return

    # Append a consolidation marker
    lines = [
        "\n\n# ── Consolidated from legacy routers ─────────────────────────────\n",
        "# The following symbols were automatically extracted during\n",
        "# consolidation and may require manual review.\n",
    ]

    for fname in SOURCE_FILES:
        src_path = repo_root / fname
        if not src_path.exists():
            continue
        source = src_path.read_text(encoding="utf-8", errors="replace")
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue

        source_lines = source.splitlines(keepends=True)
        for node in ast.iter_child_nodes(tree):
            name = getattr(node, "name", None)
            if name is None and isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        name = t.id
                        break
            if name and any(n == name for (_, n) in extras):
                start = node.lineno - 1
                end = getattr(node, "end_lineno", node.lineno)
                block = "".join(source_lines[start:end])
                lines.append(f"\n# From {fname}\n")
                lines.append(block)
                if not block.endswith("\n"):
                    lines.append("\n")

    with open(target, "a", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"\nConsolidation complete. {len(extras)} symbols appended to {TARGET_FILE}.")


if __name__ == "__main__":
    main()
