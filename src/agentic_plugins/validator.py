"""Validación estática de la integridad de los paquetes.

Comprueba tres familias de propiedades:

1. **Contrato** — campos obligatorios, kebab-case, SemVer, agentes existentes en
   la instantánea y un mínimo de evaluaciones por plugin.
2. **Higiene** — ni secretos ni comandos peligrosos dentro de los paquetes, y
   rutas de manifiesto sin escapes hacia arriba.
3. **Ausencia de duplicación no gobernada** — todo archivo dentro de un paquete
   es una vista generada del catálogo o está declarado como fuente. Un archivo
   nuevo escrito a mano que repita datos del catálogo se rechaza aquí, que es la
   única forma de que la promesa «una sola fuente de verdad» siga siendo cierta
   dentro de seis meses.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .catalog import load_agent_snapshot, load_catalog
from .render import expected_views

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
SECRET_RE = re.compile(
    r"(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|BEGIN (RSA|OPENSSH) PRIVATE KEY)"
)
DANGEROUS_RE = re.compile(
    r"rm\s+-rf\s+[/~]|git\s+reset\s+--hard|--dangerously-skip-permissions"
)

MINIMUM_EVALS = 4
REQUIRED_FIELDS = {
    "schema_version",
    "id",
    "name",
    "version",
    "status",
    "description",
    "mission",
    "components",
    "targets",
    "policy",
    "activation",
    "examples",
    "maturity",
    "source",
}
# Lo único que un paquete contiene y el catálogo no genera. Se declara aquí para
# que añadir un archivo a mano sea una decisión visible en un diff, no un olvido.
AUTHORED_FILES = {Path("evals") / "cases.jsonl"}
IGNORED_NAMES = {"__pycache__", ".DS_Store", ".agentic-plugins-managed.json"}


def issue(level: str, plugin_id: str, message: str) -> dict:
    return {"level": level, "plugin_id": plugin_id, "message": message}


def _check_contract(plugin: dict, plugin_id: str, known_agents: set[str]) -> list[dict]:
    problems = []
    if not ID_RE.fullmatch(plugin_id):
        problems.append(issue("error", plugin_id, "ID no está en kebab-case"))
    if not SEMVER_RE.fullmatch(plugin["version"]):
        problems.append(issue("error", plugin_id, "Versión no es SemVer"))
    if not plugin["components"]["agents"]:
        problems.append(issue("error", plugin_id, "Debe declarar al menos un agente"))
    if not plugin["components"]["skills"]:
        problems.append(issue("error", plugin_id, "Debe declarar al menos un skill"))
    for agent_id in plugin["components"]["agents"]:
        if agent_id not in known_agents:
            problems.append(
                issue("error", plugin_id, f"Agente fuera de la instantánea: {agent_id}")
            )
    if not plugin["policy"]["approval_required"]:
        problems.append(issue("error", plugin_id, "Debe declarar gates humanos"))
    if not plugin["policy"]["denied"]:
        problems.append(issue("error", plugin_id, "Debe declarar acciones denegadas"))
    if not plugin["policy"].get("human_approval_cannot_be_delegated"):
        problems.append(
            issue("error", plugin_id, "La aprobación humana no puede declararse delegable")
        )
    if plugin["maturity"]["declared"] != plugin["status"]:
        problems.append(issue("error", plugin_id, "status y maturity.declared difieren"))
    return problems


def _check_hygiene(root: Path, base: Path, plugin_id: str) -> list[dict]:
    problems = []
    for path in sorted(base.rglob("*")):
        if not path.is_file() or any(part in IGNORED_NAMES for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        relative = path.relative_to(root).as_posix()
        if SECRET_RE.search(text):
            problems.append(issue("error", plugin_id, f"Posible secreto en {relative}"))
        if DANGEROUS_RE.search(text):
            problems.append(
                issue("error", plugin_id, f"Comando peligroso en {relative}")
            )
    return problems


def _check_no_ungoverned_files(
    base: Path, plugin_id: str, generated: set[Path]
) -> list[dict]:
    problems = []
    for path in sorted(base.rglob("*")):
        if not path.is_file() or any(part in IGNORED_NAMES for part in path.parts):
            continue
        if path in generated or path.relative_to(base) in AUTHORED_FILES:
            continue
        problems.append(
            issue(
                "error",
                plugin_id,
                f"Archivo no gobernado por el catálogo: {path.relative_to(base).as_posix()}",
            )
        )
    return problems


def _check_manifest_paths(base: Path, plugin_id: str) -> list[dict]:
    problems = []
    manifest = base / ".codex-plugin" / "plugin.json"
    if not manifest.is_file():
        return problems
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for key in ("skills", "mcpServers", "hooks"):
        value = data.get(key)
        if value and (not value.startswith("./") or ".." in Path(value).parts):
            problems.append(issue("error", plugin_id, f"Ruta insegura: {key}"))
    return problems


def _check_evals(base: Path, plugin_id: str) -> list[dict]:
    problems = []
    path = base / "evals" / "cases.jsonl"
    if not path.is_file():
        return problems
    identifiers = set()
    count = 0
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError:
            problems.append(issue("error", plugin_id, f"Eval inválida en la línea {number}"))
            continue
        if not {"id", "input", "expected"} <= set(case):
            problems.append(issue("error", plugin_id, f"Eval incompleta en la línea {number}"))
            continue
        if case["id"] in identifiers:
            problems.append(issue("error", plugin_id, f"Eval duplicada: {case['id']}"))
        identifiers.add(case["id"])
        count += 1
    if count < MINIMUM_EVALS:
        problems.append(
            issue("error", plugin_id, f"Se requieren al menos {MINIMUM_EVALS} evals")
        )
    return problems


def validate(root: Path) -> list[dict]:
    catalog = load_catalog(root)
    snapshot = load_agent_snapshot(root)
    known_agents = {item["id"] for item in snapshot["agents"]}
    views = expected_views(root)
    problems: list[dict] = []
    seen: set[str] = set()

    for plugin in catalog["plugins"]:
        plugin_id = plugin.get("id", "<unknown>")
        missing = sorted(REQUIRED_FIELDS - set(plugin))
        if missing:
            problems.append(
                issue("error", plugin_id, "Campos faltantes: " + ", ".join(missing))
            )
            continue
        if plugin_id in seen:
            problems.append(issue("error", plugin_id, "ID duplicado"))
        seen.add(plugin_id)
        problems.extend(_check_contract(plugin, plugin_id, known_agents))

        base = root / "plugins" / plugin_id
        if not base.is_dir():
            problems.append(issue("error", plugin_id, "Falta el directorio del paquete"))
            continue

        generated = {path for path in views if base in path.parents}
        for path in sorted(generated):
            if not path.is_file():
                problems.append(
                    issue(
                        "error",
                        plugin_id,
                        f"Falta la vista generada {path.relative_to(base).as_posix()}",
                    )
                )
        problems.extend(_check_no_ungoverned_files(base, plugin_id, generated))
        problems.extend(_check_hygiene(root, base, plugin_id))
        problems.extend(_check_manifest_paths(base, plugin_id))
        problems.extend(_check_evals(base, plugin_id))

    directories = {path.name for path in (root / "plugins").iterdir() if path.is_dir()}
    for plugin_id in sorted(directories - seen):
        problems.append(issue("warning", plugin_id, "Directorio no catalogado"))
    return problems
