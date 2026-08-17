"""Interfaz de línea de comandos del toolkit.

Doce comandos, ninguna dependencia de runtime y ninguna clave API: validar,
sincronizar, evaluar, empaquetar, exportar e inspeccionar funcionan offline. La
referencia completa está en `docs/CLI.md`.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from . import __version__
from .catalog import find_root, load_catalog, plugins_by_id
from .evaluation import evaluate_plugin
from .exporter import export_plugin, uninstall_plugin
from .mcp_server import serve as serve_mcp
from .packager import package_plugin, write_checksums
from .policy import classify_action
from .server import serve
from .syncer import sync
from .validator import validate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentic-plugins", description="Toolkit de plugins agénticos"
    )
    parser.add_argument("--root", type=Path, help="Raíz del repositorio a operar")
    parser.add_argument("--version", action="version", version=f"agentic-plugins {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    listing = sub.add_parser("list", help="Lista el catálogo")
    listing.add_argument("--json", action="store_true")

    inspect = sub.add_parser("inspect", help="Muestra el contrato de un plugin")
    inspect.add_argument("plugin_id")
    inspect.add_argument("--json", action="store_true")

    check = sub.add_parser("validate", help="Valida la integridad de los paquetes")
    check.add_argument("--json", action="store_true")

    synchronize = sub.add_parser("sync", help="Regenera las vistas derivadas")
    synchronize.add_argument("--check", action="store_true", help="Falla si hay drift")

    evaluate = sub.add_parser("eval", help="Ejecuta las evaluaciones deterministas")
    evaluate.add_argument("plugin_id", nargs="?")
    evaluate.add_argument("--all", action="store_true")
    evaluate.add_argument("--json", action="store_true")

    package = sub.add_parser("package", help="Construye ZIP reproducibles")
    package.add_argument("plugin_id", nargs="?")
    package.add_argument("--all", action="store_true")
    package.add_argument("--output", type=Path, default=Path("dist"))

    export = sub.add_parser("export", help="Instala un plugin en un directorio destino")
    export.add_argument("plugin_id")
    export.add_argument("--target", type=Path, required=True)
    export.add_argument("--force", action="store_true")

    uninstall = sub.add_parser("uninstall", help="Elimina un plugin administrado")
    uninstall.add_argument("plugin_id")
    uninstall.add_argument("--target", type=Path, required=True)

    policy = sub.add_parser("policy-check", help="Clasifica una acción")
    policy.add_argument("plugin_id")
    policy.add_argument("--action", required=True)

    mcp = sub.add_parser("mcp", help="Servidor MCP por stdio")
    mcp.add_argument("--plugin", required=True)

    web = sub.add_parser("serve", help="Panel local de inspección")
    web.add_argument("--host", default="127.0.0.1")
    web.add_argument("--port", type=int, default=8787)

    sub.add_parser("doctor", help="Diagnóstico del entorno")
    return parser


def _selected(catalog: dict, plugins: dict, args) -> list[dict]:
    if args.all:
        return catalog["plugins"]
    if args.plugin_id:
        return [plugins[args.plugin_id]]
    raise ValueError("Indique plugin_id o --all")


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = args.root.resolve() if args.root else find_root()
        catalog = load_catalog(root)
        plugins = plugins_by_id(catalog)

        if args.command == "list":
            rows = [
                {key: item[key] for key in ("id", "name", "status", "category", "risk")}
                for item in catalog["plugins"]
            ]
            if args.json:
                print(json.dumps(rows, ensure_ascii=False, indent=2))
            else:
                for row in rows:
                    print(f"{row['id']:<28} {row['status']:<12} {row['risk']:<6} {row['name']}")
            return 0

        if args.command == "inspect":
            item = plugins[args.plugin_id]
            if args.json:
                print(json.dumps(item, ensure_ascii=False, indent=2))
            else:
                print(
                    f"{item['name']} ({item['id']})\n"
                    f"Estado: {item['status']} | Riesgo: {item['risk']}\n"
                    f"Misión: {item['mission']}\n"
                    "Agentes: " + ", ".join(item["components"]["agents"]) + "\n"
                    "Aprobación humana: " + ", ".join(item["policy"]["approval_required"]) + "\n"
                    "Denegado: " + ", ".join(item["policy"]["denied"])
                )
            return 0

        if args.command == "validate":
            issues = validate(root)
            if args.json:
                print(json.dumps(issues, ensure_ascii=False, indent=2))
            elif issues:
                for item in issues:
                    print(f"{item['level'].upper():<7} {item['plugin_id']}: {item['message']}")
            else:
                print(f"OK: {len(catalog['plugins'])} plugins válidos")
            return 1 if any(item["level"] == "error" for item in issues) else 0

        if args.command == "sync":
            drift = sync(root, check=args.check)
            if not drift:
                print("OK: no hay drift")
            elif args.check:
                print(f"Drift en {len(drift)} archivos:")
                for item in drift:
                    print(f"  {item}")
            else:
                print(f"Sincronizados {len(drift)} archivos:")
                for item in drift:
                    print(f"  {item}")
            return 1 if args.check and drift else 0

        if args.command == "eval":
            output = [
                {"plugin_id": item["id"], "cases": evaluate_plugin(root, item)}
                for item in _selected(catalog, plugins, args)
            ]
            passed = sum(case["passed"] for item in output for case in item["cases"])
            total = sum(len(item["cases"]) for item in output)
            if args.json:
                print(json.dumps(output, ensure_ascii=False, indent=2))
            else:
                for item in output:
                    ok = sum(case["passed"] for case in item["cases"])
                    print(f"{item['plugin_id']}: {ok}/{len(item['cases'])}")
                    for case in item["cases"]:
                        if not case["passed"]:
                            print(
                                f"  FALLA {case['id']} (línea {case['line']}): "
                                f"esperado {case['expected']} · obtenido "
                                f"activate={case['actual']['activate']} "
                                f"approval={case['actual']['approval']}"
                            )
                print(f"TOTAL: {passed}/{total}")
            return 0 if passed == total else 1

        if args.command == "package":
            selected = _selected(catalog, plugins, args)
            output = args.output if args.output.is_absolute() else root / args.output
            values = [package_plugin(root, item, output) for item in selected]
            write_checksums(output, values)
            for path, digest in values:
                print(f"{path.name}  sha256:{digest}")
            return 0

        if args.command == "export":
            print(export_plugin(root, plugins[args.plugin_id], args.target, args.force))
            return 0

        if args.command == "uninstall":
            removed = uninstall_plugin(plugins[args.plugin_id], args.target)
            print("Eliminado" if removed else "No estaba instalado")
            return 0

        if args.command == "policy-check":
            print(
                json.dumps(
                    classify_action(plugins[args.plugin_id], args.action),
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        if args.command == "mcp":
            return serve_mcp(args.plugin)

        if args.command == "serve":
            serve(root, args.host, args.port)
            return 0

        if args.command == "doctor":
            supported = sys.version_info >= (3, 11)
            agents = {
                agent
                for plugin in catalog["plugins"]
                for agent in plugin["components"]["agents"]
            }
            print(f"agentic-plugins       {__version__}")
            print(f"Python                {sys.version.split()[0]} " f"({'OK' if supported else 'requiere 3.11+'})")
            print(f"Ejecutable            {shutil.which('agentic-plugins') or 'ejecución por módulo'}")
            print(f"Hook                  {shutil.which('agentic-plugins-hook') or 'no instalado'}")
            print(f"Raíz                  {root}")
            print(f"Catálogo              {len(catalog['plugins'])} plugins · {len(agents)} agentes")
            issues = validate(root)
            errors = sum(1 for item in issues if item["level"] == "error")
            print(f"Validación            {'OK' if not errors else f'{errors} errores'}")
            return 0 if supported and not errors else 1

    except KeyError as exc:
        print(f"ERROR: plugin desconocido: {exc.args[0]}", file=sys.stderr)
        return 2
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
