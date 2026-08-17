"""Carga del catálogo canónico y de la instantánea de agentes.

`catalog/plugins.yaml` es la fuente de verdad del repositorio. El archivo lleva
extensión `.yaml` y contiene **JSON**, que es un subconjunto válido de YAML 1.2:
así la CLI se mantiene sin dependencias de runtime —no necesita `pyyaml`— y el
nombre sigue el estándar de los repositorios relacionados. La consecuencia está
documentada en `docs/PLUGIN_CONTRACT.md`: solo se acepta el subconjunto JSON, no
la sintaxis completa de YAML.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

CATALOG_RELATIVE = Path("catalog") / "plugins.yaml"
SNAPSHOT_RELATIVE = Path("catalog") / "agents.snapshot.json"
ROOT_ENV = "AGENTIC_PLUGINS_ROOT"


def find_root(start: Path | None = None) -> Path:
    configured = os.environ.get(ROOT_ENV)
    if configured:
        root = Path(configured).expanduser().resolve()
        if (root / CATALOG_RELATIVE).is_file():
            return root
        raise FileNotFoundError(f"{ROOT_ENV} inválido: {root}")
    candidates = [start or Path.cwd(), Path(__file__).resolve()]
    for candidate in candidates:
        current = candidate.resolve()
        if current.is_file():
            current = current.parent
        for parent in (current, *current.parents):
            if (parent / CATALOG_RELATIVE).is_file():
                return parent
    raise FileNotFoundError(f"No se encontró {CATALOG_RELATIVE.as_posix()}")


def _read_json(path: Path, label: str) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} inválido: {exc}") from exc
    except OSError as exc:
        raise ValueError(f"No se pudo leer {label}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{label} debe ser un objeto")
    return data


def load_catalog(root: Path | None = None) -> dict:
    data = _read_json((root or find_root()) / CATALOG_RELATIVE, "Catálogo")
    if not isinstance(data.get("plugins"), list) or not data["plugins"]:
        raise ValueError("El catálogo requiere una lista plugins no vacía")
    for key in ("repository_version", "source_of_truth", "mcp_protocol_version", "execution_plan_steps"):
        if key not in data:
            raise ValueError(f"El catálogo requiere la clave {key}")
    return data


def load_agent_snapshot(root: Path | None = None) -> dict:
    data = _read_json((root or find_root()) / SNAPSHOT_RELATIVE, "Snapshot de agentes")
    if not isinstance(data.get("agents"), list) or not data["agents"]:
        raise ValueError("La instantánea requiere una lista agents no vacía")
    return data


def plugins_by_id(catalog: dict) -> dict[str, dict]:
    return {item["id"]: item for item in catalog["plugins"]}
