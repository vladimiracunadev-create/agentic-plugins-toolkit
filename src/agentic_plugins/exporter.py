from __future__ import annotations

import json
import shutil
from pathlib import Path

MARKER = ".agentic-plugins-managed.json"


def export_plugin(root: Path, plugin: dict, target: Path, force: bool = False) -> Path:
    destination = target.expanduser().resolve() / plugin["id"]
    source = root / "plugins" / plugin["id"]
    if destination.exists():
        marker = destination / MARKER
        if not force and not marker.is_file():
            raise ValueError(f"Conflicto no administrado: {destination}")
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    (destination / MARKER).write_text(
        json.dumps({"id": plugin["id"], "version": plugin["version"]}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return destination


def uninstall_plugin(plugin: dict, target: Path) -> bool:
    destination = target.expanduser().resolve() / plugin["id"]
    marker = destination / MARKER
    if not destination.exists():
        return False
    if not marker.is_file():
        raise ValueError(f"No se eliminará un directorio no administrado: {destination}")
    shutil.rmtree(destination)
    return True
