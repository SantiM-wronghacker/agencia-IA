"""Root conftest – makes the src/ package importable for all tests."""
import sys
from pathlib import Path

# Add src/ to the front of sys.path so that ``from agencia.agents.…``
# imports resolve without installing the package.
_src = str(Path(__file__).resolve().parent / "src")
if _src not in sys.path:
    sys.path.insert(0, _src)
