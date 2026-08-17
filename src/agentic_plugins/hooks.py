"""Hook `SessionStart` que anuncia los límites del plugin.

Se expone como el console script `agentic-plugins-hook` en vez de invocarse con
`python3 -m …`: `python3` no existe en una instalación estándar de Windows, así
que el hook quedaría muerto justo en una de las plataformas que el repositorio
declara soportadas.

El hook solo imprime. No escribe archivos, no abre red y no modifica el
repositorio: su único efecto es que la sesión empiece sabiendo qué acciones
exigen aprobación humana.
"""

from __future__ import annotations

import argparse
import json
import sys

from .catalog import find_root, load_catalog, plugins_by_id


def build_message(plugin: dict) -> str:
    return (
        f"{plugin['name']} activo. "
        "Gates humanos: " + ", ".join(plugin["policy"]["approval_required"]) + ". "
        "Denegado siempre: " + ", ".join(plugin["policy"]["denied"]) + "."
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="agentic-plugins-hook")
    parser.add_argument("--plugin", required=True)
    parser.add_argument("--event", required=True)
    args = parser.parse_args(argv)
    try:
        plugin = plugins_by_id(load_catalog(find_root()))[args.plugin]
    except (KeyError, ValueError, FileNotFoundError) as exc:
        # Un hook que falla no debe bloquear la sesión del host.
        print(
            json.dumps({"systemMessage": f"Hook inactivo: {exc}", "continue": True}),
            file=sys.stdout,
        )
        return 0
    print(
        json.dumps(
            {"systemMessage": build_message(plugin), "continue": True},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
