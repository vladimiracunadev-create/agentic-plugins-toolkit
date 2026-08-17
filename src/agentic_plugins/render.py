"""Renderizadores de las vistas derivadas del catálogo.

`expected_views` devuelve el contenido exacto que debe tener cada archivo
generado. `syncer.sync` lo escribe y `sync --check` falla si algo difiere, así
que ningún archivo de esta lista puede editarse a mano sin romper la build.

La regla de diseño es explícita: **todo dato que aparezca en dos sitios se
genera desde el catálogo**. Un README de plugin, un `provenance.json` o un
servidor MCP autocontenido son copias de información que ya vive en
`catalog/plugins.yaml`; mantenerlos a mano es exactamente el drift que este
repositorio dice evitar.
"""

from __future__ import annotations

import inspect
import json
from pathlib import Path

from . import policy
from .catalog import load_agent_snapshot, load_catalog

REPOSITORY_URL = "https://github.com/vladimiracunadev-create/agentic-plugins-toolkit"
AUTHOR = "Vladimir Acuña"
AUTHOR_URL = "https://github.com/vladimiracunadev-create"
BRAND_COLOR = "#6D5CE7"
GENERATED_NOTICE = "Vista generada desde catalog/plugins.yaml. No la edites a mano."


def as_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# Agentes y skills
# ─────────────────────────────────────────────────────────────────────────────


def render_agent(agent: dict, plugin: dict) -> str:
    lines = [
        "---",
        f"name: {agent['id']}",
        f"description: {agent['description']}",
        "tools: " + ", ".join(agent["tools"]),
        "model: inherit",
        "---",
        "",
        f"# {agent['name']}",
        "",
        f"Plugin propietario: {plugin['id']}",
        "",
        "## Misión",
        "",
        agent["mission"],
        "",
        "## Flujo",
        "",
    ]
    lines.extend(
        f"{index}. {phase}"
        for index, phase in enumerate(agent["phases"], start=1)
    )
    lines.extend(["", "## Verificaciones", ""])
    lines.extend(f"- {item}" for item in agent["checks"])
    lines.extend(["", "## Gates humanos", ""])
    lines.extend(f"- {item}" for item in agent["approval_points"])
    lines.extend(
        [
            "",
            "Ningún agente, subagente o tool sustituye la aprobación humana.",
            "Distingue siempre observado, inferido y pendiente.",
            "",
        ]
    )
    return "\n".join(lines)


def render_skill(plugin: dict) -> str:
    lines = [
        "---",
        f"name: {plugin['id']}-workflow",
        (
            f"description: {plugin['description']} Usar cuando la solicitud "
            f"coincida con la misión de {plugin['name']}."
        ),
        "license: MIT",
        (
            "compatibility: El servidor MCP local es opcional; "
            "no requiere una API de modelo."
        ),
        "metadata:",
        f"  author: {AUTHOR}",
        f'  version: "{plugin["version"]}"',
        "---",
        "",
        f"# {plugin['name']} workflow",
        "",
        "1. Confirma objetivo, alcance, destino y autorización.",
        "2. Inspecciona evidencia antes de concluir.",
        "3. Selecciona el agente mínimo para la misión.",
        "4. Produce un plan reversible con criterios de verificación.",
        "5. Detente en todo gate humano.",
        "6. Entrega resultado, pruebas y riesgo residual.",
        "",
        "## Agentes",
        "",
    ]
    lines.extend(f"- {item}" for item in plugin["components"]["agents"])
    lines.extend(["", "## Requieren aprobación", ""])
    lines.extend(f"- {item}" for item in plugin["policy"]["approval_required"])
    lines.extend(["", "## Denegado siempre", ""])
    lines.extend(f"- {item}" for item in plugin["policy"]["denied"])
    lines.extend(["", "## Ejemplos", ""])
    lines.extend(f"- {item}" for item in plugin["examples"])
    lines.extend(
        [
            "",
            "Si falta una dependencia opcional, continúa con las instrucciones",
            "integradas y declara la limitación. No descargues código silenciosamente.",
            "",
        ]
    )
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Manifiestos por plataforma
# ─────────────────────────────────────────────────────────────────────────────


def openai_manifest(plugin: dict) -> dict:
    return {
        "name": plugin["id"],
        "version": plugin["version"],
        "description": plugin["description"],
        "author": {"name": AUTHOR, "url": AUTHOR_URL},
        "repository": REPOSITORY_URL,
        "license": "MIT",
        "keywords": ["agents", "skills", "mcp", "plugin", plugin["id"]],
        "skills": "./skills/",
        "mcpServers": "./.mcp.json",
        "hooks": "./hooks/hooks.json",
        "interface": {
            "displayName": plugin["name"],
            "shortDescription": plugin["description"][:100],
            "longDescription": plugin["description"],
            "developerName": AUTHOR,
            "category": plugin["category"],
            "capabilities": ["Read", "Plan", "Write with approval"],
            "defaultPrompt": plugin["examples"],
            "brandColor": BRAND_COLOR,
        },
    }


def claude_manifest(plugin: dict) -> dict:
    return {
        "name": plugin["id"],
        "version": plugin["version"],
        "description": plugin["description"],
        "author": {"name": AUTHOR},
        "homepage": REPOSITORY_URL,
        "license": "MIT",
    }


def mcp_manifest(plugin: dict) -> dict:
    return {
        "mcpServers": {
            f"{plugin['id']}-control": {
                "command": "agentic-plugins",
                "args": ["mcp", "--plugin", plugin["id"]],
            }
        }
    }


def hooks_manifest(plugin: dict) -> dict:
    # `agentic-plugins-hook` es un console script del propio paquete. Se usa en
    # lugar de `python3 -m …` porque `python3` no existe en una instalación
    # estándar de Windows y el hook quedaría muerto justo en la plataforma que
    # docs/WINDOWS.md declara soportada.
    return {
        "hooks": {
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": (
                                f"agentic-plugins-hook --plugin {plugin['id']} "
                                "--event SessionStart"
                            ),
                            "statusMessage": f"Cargando límites de {plugin['name']}",
                        }
                    ]
                }
            ]
        }
    }


def provenance(catalog: dict, plugin: dict) -> dict:
    return {
        "plugin": plugin["id"],
        "version": plugin["version"],
        "generated_from": {
            "plugin_catalog": catalog["source_of_truth"],
            "agent_snapshot": "catalog/agents.snapshot.json",
            "agent_repository": plugin["source"]["agents_repository"],
            "agent_repository_version": plugin["source"]["agents_snapshot_version"],
        },
        "optional_skill_source": {
            "repository": plugin["source"]["skills_repository"],
            "mode": plugin["source"]["skills_mode"],
            "skills": plugin["components"]["optional_skills"],
        },
        "generated_files_are_distribution_views": True,
        "production_claim": False,
        "declared_maturity": plugin["maturity"]["declared"],
        "not_claimed": plugin["maturity"]["not_claimed"],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Fichas humanas y adaptadores
# ─────────────────────────────────────────────────────────────────────────────


def render_plugin_readme(plugin: dict, agents: dict) -> str:
    approvals = ", ".join(f"`{item}`" for item in plugin["policy"]["approval_required"])
    denied = ", ".join(f"`{item}`" for item in plugin["policy"]["denied"])
    lines = [
        f"# {plugin['icon']} {plugin['name']}",
        "",
        f"> {plugin['description']}",
        "",
        f"<!-- {GENERATED_NOTICE} -->",
        "",
        f"[Toolkit]({REPOSITORY_URL}) · "
        "[Contrato](../../docs/PLUGIN_CONTRACT.md) · "
        "[Modelo de madurez](../../docs/MATURITY_MODEL.md)",
        "",
        "---",
        "",
        "## Misión",
        "",
        plugin["mission"],
        "",
        "## Ficha",
        "",
        "| Campo | Valor |",
        "|---|---|",
        f"| Identificador | `{plugin['id']}` |",
        f"| Versión | `{plugin['version']}` |",
        f"| Estado | `{plugin['status']}` |",
        f"| Categoría | {plugin['category']} |",
        f"| Riesgo | `{plugin['risk']}` |",
        f"| Agentes | {len(plugin['components']['agents'])} |",
        f"| Política por defecto | `{plugin['policy']['default']}` |",
        "",
        "## Agentes",
        "",
    ]
    for agent_id in plugin["components"]["agents"]:
        agent = agents[agent_id]
        lines.append(f"### {agent['icon']} `{agent_id}`")
        lines.append("")
        lines.append(agent["description"])
        lines.append("")
        lines.append(f"**Cuándo delegarle trabajo.** {agent['delegate_when']}")
        lines.append("")
        lines.append(
            "**Se detiene en:** "
            + ", ".join(f"`{item}`" for item in agent["approval_points"])
            + "."
        )
        lines.append("")
    lines.extend(
        [
            "## Cuándo se activa",
            "",
            "Señales positivas: "
            + ", ".join(f"`{item}`" for item in plugin["activation"]["keywords"])
            + ".",
            "",
            "Señales negativas: "
            + ", ".join(f"`{item}`" for item in plugin["activation"]["negative_keywords"])
            + ".",
            "",
            "```bash",
            f"agentic-plugins policy-check {plugin['id']} --action \"publicar el release\"",
            "```",
            "",
            "## Límites",
            "",
            f"- **Requieren aprobación humana:** {approvals}.",
            f"- **Denegado siempre, sin excepción:** {denied}.",
            "- La aprobación humana **no** se delega en otro agente ni en una tool.",
            "",
            "El contrato ejecutable está en `policies/policy.json`; esta ficha es una",
            "lectura del mismo dato, no una promesa aparte.",
            "",
            "## Skills opcionales",
            "",
            "Funciona sin ellos y mejora si están instalados desde "
            f"[`{plugin['source']['skills_repository']}`]"
            f"(https://github.com/vladimiracunadev-create/{plugin['source']['skills_repository']}):",
            "",
        ]
    )
    lines.extend(f"- `{item}`" for item in plugin["components"]["optional_skills"])
    lines.extend(
        [
            "",
            "## Madurez",
            "",
            f"Declara `{plugin['maturity']['declared']}`: {plugin['maturity']['claim']}",
            "",
            "**No afirma** "
            + ", ".join(f"`{item}`" for item in plugin["maturity"]["not_claimed"])
            + ".",
            "",
            "---",
            "",
            '<div align="center"><sub>'
            f'<a href="{REPOSITORY_URL}">Toolkit</a> · '
            '<a href="../../docs/SECURITY_MODEL.md">Modelo de seguridad</a> · '
            '<a href="../../docs/MATURITY_MODEL.md">Madurez</a></sub></div>',
            "",
        ]
    )
    return "\n".join(lines)


def render_openai_adapter(plugin: dict) -> str:
    return "\n".join(
        [
            "# OpenAI y Codex",
            "",
            f"<!-- {GENERATED_NOTICE} -->",
            "",
            f"Soporte declarado: **native-package**. La raíz del paquete "
            f"`{plugin['id']}` contiene todo lo que el host necesita:",
            "",
            "| Archivo | Contenido |",
            "|---|---|",
            "| `.codex-plugin/plugin.json` | manifiesto, interfaz y prompts por defecto |",
            "| `skills/` | el workflow del plugin |",
            "| `hooks/hooks.json` | el hook `SessionStart` que anuncia los límites |",
            "| `.mcp.json` | el servidor de control por stdio |",
            "",
            "Instala primero el paquete Python para habilitar el ejecutable",
            "`agentic-plugins`, del que dependen el hook y el servidor MCP:",
            "",
            "```bash",
            "python -m pip install agentic-plugins-toolkit",
            f"agentic-plugins inspect {plugin['id']}",
            "```",
            "",
            "Si prefieres no instalar nada, `runtime/mcp_server.py` es un servidor",
            "autocontenido que solo necesita Python 3.11+ y la biblioteca estándar.",
            "",
        ]
    )


def render_claude_adapter(plugin: dict) -> str:
    return "\n".join(
        [
            "# Claude Code",
            "",
            f"<!-- {GENERATED_NOTICE} -->",
            "",
            "Soporte declarado: **native-package**. Claude Code descubre agentes,",
            "skills, hooks y servidores MCP desde la raíz del paquete.",
            "",
            "```bash",
            f"agentic-plugins export {plugin['id']} --target ~/.claude/plugins",
            "```",
            "",
            "El exportador escribe una marca `.agentic-plugins-managed.json` y se",
            "niega a sobrescribir un directorio que no lleve esa marca: un plugin",
            "tuyo con el mismo nombre queda intacto y la operación falla.",
            "",
            "> [!IMPORTANT]",
            "> Revisa `hooks/hooks.json` **antes** de confiar en el paquete. El hook",
            "> `SessionStart` solo imprime los límites del plugin, no escribe archivos",
            "> ni accede a la red, pero esa comprobación es tuya y no debería basarse",
            "> en esta frase.",
            "",
            f"Los agentes de `{plugin['id']}` declaran `model: inherit`: el paquete no",
            "impone modelo ni consume una API por su cuenta.",
            "",
        ]
    )


def render_gemini_adapter(plugin: dict) -> str:
    return "\n".join(
        [
            f"# {plugin['name']}",
            "",
            f"<!-- {GENERATED_NOTICE} -->",
            "",
            "Soporte declarado: **generated-instructions**. Esto es una adaptación",
            "portable, no un manifiesto nativo equivalente: Gemini no instala el",
            "paquete, lo lee.",
            "",
            "## Cómo usarlo",
            "",
            f"1. Carga `skills/{plugin['components']['skills'][0]}/SKILL.md` como instrucciones.",
            "2. Selecciona el agente adecuado de `agents/`.",
            "3. Conserva `policies/policy.json` como límite duro de la sesión.",
            "4. Conecta `runtime/mcp_server.py` si el host soporta MCP por stdio.",
            "",
            "## Misión",
            "",
            plugin["mission"],
            "",
            "## Límites que no se negocian",
            "",
            "Requieren aprobación humana explícita: "
            + ", ".join(f"`{item}`" for item in plugin["policy"]["approval_required"])
            + ".",
            "",
            "Denegado siempre: "
            + ", ".join(f"`{item}`" for item in plugin["policy"]["denied"])
            + ".",
            "",
        ]
    )


def render_icon(plugin: dict) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" role="img" '
        f'aria-label="{plugin["name"]}">'
        '<rect width="128" height="128" rx="24" fill="#18152d"/>'
        f'<circle cx="64" cy="64" r="42" fill="{BRAND_COLOR.lower()}"/>'
        f'<text x="64" y="79" text-anchor="middle" font-size="48">{plugin["icon"]}</text>'
        "</svg>\n"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Servidor MCP autocontenido
# ─────────────────────────────────────────────────────────────────────────────

RUNTIME_TEMPLATE = '''\
"""Servidor MCP autocontenido de {name}.

{notice}

Solo necesita Python 3.11+ y la biblioteca estándar. La lógica de política de
abajo no es una reimplementación: `render.py` copia el código fuente literal de
`agentic_plugins.policy` al generar este archivo, de modo que este servidor y la
CLI no pueden clasificar la misma acción de forma distinta.
"""

from __future__ import annotations

import json
import sys

PLUGIN = json.loads({payload})

TOOLS = [
    {{"name": "plugin_info", "description": "Describe el plugin y sus límites.", "inputSchema": {{"type": "object", "properties": {{}}}}}},
    {{"name": "create_execution_plan", "description": "Crea un plan determinista sin ejecutar.", "inputSchema": {{"type": "object", "required": ["task"], "properties": {{"task": {{"type": "string"}}, "target": {{"type": "string"}}}}}}}},
    {{"name": "policy_check", "description": "Clasifica una acción.", "inputSchema": {{"type": "object", "required": ["action"], "properties": {{"action": {{"type": "string"}}}}}}}},
]

PLAN_STEPS = {steps}


{policy_source}

def result(request_id, payload):
    return {{"jsonrpc": "2.0", "id": request_id, "result": payload}}


def error(request_id, code, message):
    return {{"jsonrpc": "2.0", "id": request_id, "error": {{"code": code, "message": message}}}}


def handle_message(plugin: dict, message: dict) -> dict | None:
    method = message.get("method")
    request_id = message.get("id")
    if method == "initialize":
        return result(
            request_id,
            {{
                "protocolVersion": "{protocol}",
                "capabilities": {{"tools": {{}}}},
                "serverInfo": {{"name": plugin["id"] + "-control", "version": plugin["version"]}},
            }},
        )
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return result(request_id, {{"tools": TOOLS}})
    if method == "tools/call":
        params = message.get("params", {{}})
        name = params.get("name")
        arguments = params.get("arguments", {{}})
        if name == "plugin_info":
            data = {{
                "id": plugin["id"],
                "name": plugin["name"],
                "status": plugin["status"],
                "agents": plugin["components"]["agents"],
                "policy": plugin["policy"],
            }}
        elif name == "create_execution_plan":
            data = {{
                "plugin": plugin["id"],
                "task": arguments.get("task", ""),
                "target": arguments.get("target"),
                "steps": PLAN_STEPS,
            }}
        elif name == "policy_check":
            data = classify_action(plugin, str(arguments.get("action", "")))
        else:
            return error(request_id, -32601, "Unknown tool")
        return result(
            request_id,
            {{
                "content": [{{"type": "text", "text": json.dumps(data, ensure_ascii=False)}}],
                "structuredContent": data,
            }},
        )
    return error(request_id, -32601, "Method not found")


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            answer = handle_message(PLUGIN, json.loads(line))
            if answer is not None:
                print(json.dumps(answer, ensure_ascii=False), flush=True)
        except (ValueError, KeyError, TypeError) as exc:
            print(json.dumps(error(None, -32603, str(exc))), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def policy_source() -> str:
    """Devuelve el código fuente literal de la semántica de política.

    Copiar el código en vez de reescribirlo es lo que hace imposible que el
    paquete distribuido y la CLI diverjan: si alguien cambia `policy.py` sin
    regenerar, `sync --check` falla en CI.
    """
    return (
        inspect.getsource(policy._matches).rstrip()
        + "\n\n\n"
        + inspect.getsource(policy.classify_action).rstrip()
        + "\n"
    )


def render_runtime(plugin: dict, protocol: str, steps: list[str]) -> str:
    payload = json.dumps(json.dumps(plugin, ensure_ascii=False), ensure_ascii=False)
    return RUNTIME_TEMPLATE.format(
        name=plugin["name"],
        notice=GENERATED_NOTICE,
        payload=payload,
        protocol=protocol,
        steps=json.dumps(steps, ensure_ascii=False, indent=4),
        policy_source=policy_source(),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Vistas del repositorio
# ─────────────────────────────────────────────────────────────────────────────


def count_eval_cases(root: Path, plugin_id: str) -> int:
    path = root / "plugins" / plugin_id / "evals" / "cases.jsonl"
    if not path.is_file():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def ai_catalog(catalog: dict) -> dict:
    return {
        "schema_version": "experimental-2026",
        "status": "ARD_READY_NOT_CONFORMANCE_CLAIM",
        "publisher": {"name": AUTHOR, "url": AUTHOR_URL},
        "resources": [
            {
                "id": f"urn:agentic-plugin:{plugin['id']}:{plugin['version']}",
                "type": "plugin",
                "name": plugin["name"],
                "description": plugin["description"],
                "version": plugin["version"],
                "interfaces": [
                    {"protocol": "mcp", "transport": "stdio"},
                    {
                        "protocol": "plugin-package",
                        "targets": [item["id"] for item in plugin["targets"]],
                    },
                ],
                "path": f"../plugins/{plugin['id']}",
            }
            for plugin in catalog["plugins"]
        ],
    }


def site_catalog(catalog: dict, eval_counts: dict[str, int]) -> dict:
    """Vista estática que consume la landing.

    GitHub Pages sirve archivos, no la API del panel: sin este archivo la página
    publicada quedaría vacía. Al ser una vista generada, tampoco puede afirmar
    algo distinto de lo que dice el catálogo — incluido el número de
    evaluaciones, que se cuenta sobre los archivos reales y no se escribe a mano.
    """
    return {
        "repository_version": catalog["repository_version"],
        "generated_from": catalog["source_of_truth"],
        "totals": {
            "plugins": len(catalog["plugins"]),
            "agents": len(
                {
                    agent
                    for plugin in catalog["plugins"]
                    for agent in plugin["components"]["agents"]
                }
            ),
            "evals": sum(eval_counts.values()),
        },
        "plugins": [
            {
                "id": plugin["id"],
                "icon": plugin["icon"],
                "name": plugin["name"],
                "description": plugin["description"],
                "mission": plugin["mission"],
                "status": plugin["status"],
                "category": plugin["category"],
                "risk": plugin["risk"],
                "evals": eval_counts[plugin["id"]],
                "agents": plugin["components"]["agents"],
                "approval_required": plugin["policy"]["approval_required"],
                "denied": plugin["policy"]["denied"],
                "examples": plugin["examples"],
            }
            for plugin in catalog["plugins"]
        ],
    }


def marketplace_openai(catalog: dict) -> dict:
    return {
        "name": "vladimir-agentic-plugins",
        "interface": {"displayName": "Vladimir Agentic Plugins"},
        "plugins": [
            {
                "name": plugin["id"],
                "source": {"source": "local", "path": f"./plugins/{plugin['id']}"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": plugin["category"],
                "interface": {"displayName": plugin["name"]},
            }
            for plugin in catalog["plugins"]
        ],
    }


def marketplace_claude(catalog: dict) -> dict:
    return {
        "name": "vladimir-agentic-plugins",
        "owner": {"name": AUTHOR},
        "plugins": [
            {
                "name": plugin["id"],
                "source": f"./plugins/{plugin['id']}",
                "description": plugin["description"],
                "version": plugin["version"],
            }
            for plugin in catalog["plugins"]
        ],
    }


def expected_views(root: Path) -> dict[Path, str]:
    catalog = load_catalog(root)
    snapshot = load_agent_snapshot(root)
    agents = {item["id"]: item for item in snapshot["agents"]}
    protocol = catalog["mcp_protocol_version"]
    steps = catalog["execution_plan_steps"]
    views: dict[Path, str] = {}
    for plugin in catalog["plugins"]:
        base = root / "plugins" / plugin["id"]
        views[base / "plugin.yaml"] = as_json(plugin)
        views[base / ".codex-plugin" / "plugin.json"] = as_json(openai_manifest(plugin))
        views[base / ".claude-plugin" / "plugin.json"] = as_json(claude_manifest(plugin))
        views[base / ".mcp.json"] = as_json(mcp_manifest(plugin))
        views[base / "hooks" / "hooks.json"] = as_json(hooks_manifest(plugin))
        views[base / "policies" / "policy.json"] = as_json(plugin["policy"])
        views[base / "provenance.json"] = as_json(provenance(catalog, plugin))
        views[base / "README.md"] = render_plugin_readme(plugin, agents)
        views[base / "assets" / "icon.svg"] = render_icon(plugin)
        views[base / "runtime" / "mcp_server.py"] = render_runtime(plugin, protocol, steps)
        views[base / "adapters" / "openai" / "README.md"] = render_openai_adapter(plugin)
        views[base / "adapters" / "claude-code" / "README.md"] = render_claude_adapter(plugin)
        views[base / "adapters" / "gemini" / "GEMINI.md"] = render_gemini_adapter(plugin)
        skill_id = plugin["components"]["skills"][0]
        views[base / "skills" / skill_id / "SKILL.md"] = render_skill(plugin)
        for agent_id in plugin["components"]["agents"]:
            rendered = render_agent(agents[agent_id], plugin)
            views[base / "agents" / f"{agent_id}.md"] = rendered
            views[base / "adapters" / "github-copilot" / f"{agent_id}.agent.md"] = rendered
    eval_counts = {
        plugin["id"]: count_eval_cases(root, plugin["id"])
        for plugin in catalog["plugins"]
    }
    views[root / "catalog" / "ai-catalog.json"] = as_json(ai_catalog(catalog))
    views[root / "site" / "catalog.json"] = as_json(site_catalog(catalog, eval_counts))
    views[root / ".agents" / "plugins" / "marketplace.json"] = as_json(
        marketplace_openai(catalog)
    )
    views[root / ".claude-plugin" / "marketplace.json"] = as_json(
        marketplace_claude(catalog)
    )
    return views
