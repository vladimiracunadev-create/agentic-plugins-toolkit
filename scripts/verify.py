"""Ejecuta localmente la misma secuencia que verifica CI.

Equivale a `make check` para quien no tenga `make` (típicamente en Windows).
Cada paso se ejecuta como proceso separado para que el código de salida sea el
del paso que falló y no el del último comando.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

STEPS = [
    ("Drift respecto del catálogo", [sys.executable, "-m", "agentic_plugins", "sync", "--check"]),
    ("Integridad de los paquetes", [sys.executable, "-m", "agentic_plugins", "validate"]),
    ("Evaluaciones deterministas", [sys.executable, "-m", "agentic_plugins", "eval", "--all"]),
    ("Pruebas unitarias", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
]


def main() -> int:
    for label, command in STEPS:
        print(f"\n=== {label} ===", flush=True)
        result = subprocess.run(command, check=False, cwd=ROOT)
        if result.returncode:
            print(f"\nFALLÓ: {label}", file=sys.stderr)
            return result.returncode
    print("\nTodo en verde.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
