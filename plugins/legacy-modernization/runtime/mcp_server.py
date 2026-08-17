"""Servidor MCP autocontenido de Legacy Modernization.

Vista generada desde catalog/plugins.yaml. No la edites a mano.

Solo necesita Python 3.11+ y la biblioteca estándar. La lógica de política de
abajo no es una reimplementación: `render.py` copia el código fuente literal de
`agentic_plugins.policy` al generar este archivo, de modo que este servidor y la
CLI no pueden clasificar la misma acción de forma distinta.
"""

from __future__ import annotations

import json
import sys

PLUGIN = json.loads("{\"schema_version\": \"1.0\", \"id\": \"legacy-modernization\", \"name\": \"Legacy Modernization\", \"version\": \"0.2.0\", \"status\": \"IMPLEMENTED\", \"icon\": \"🏗️\", \"category\": \"Developer Tools\", \"risk\": \"high\", \"description\": \"Planifica y ejecuta modernizaciones incrementales preservando contratos, continuidad y rollback.\", \"mission\": \"Reducir deuda y riesgo mediante rebanadas reversibles, pruebas de caracterización y gates de migración.\", \"source\": {\"agents_repository\": \"operational-ai-agents\", \"agents_snapshot_version\": \"0.1.0\", \"skills_repository\": \"claude-skills-toolkit\", \"skills_mode\": \"optional-versioned-dependencies\"}, \"components\": {\"agents\": [\"legacy-modernization-agent\"], \"skills\": [\"legacy-modernization-workflow\"], \"optional_skills\": [\"pre-push-guard\", \"python-version-control\", \"repo-coherence-audit\", \"security-audit\", \"yaml-control\"], \"mcp_servers\": [\"legacy-modernization-control\"], \"hooks\": [\"SessionStart\"], \"custom_ui\": false}, \"targets\": [{\"id\": \"openai\", \"support\": \"native-package\"}, {\"id\": \"claude-code\", \"support\": \"native-package\"}, {\"id\": \"github-copilot\", \"support\": \"generated-agent-profiles\"}, {\"id\": \"gemini\", \"support\": \"generated-instructions\"}, {\"id\": \"generic-mcp\", \"support\": \"stdio\"}], \"policy\": {\"default\": \"allow-read-plan\", \"approval_required\": [\"data-migration\", \"cutover\", \"remove-dependency\", \"production\", \"contract-break\"], \"denied\": [\"big-bang-without-rollback\", \"bypass-approval\"], \"human_approval_cannot_be_delegated\": true}, \"activation\": {\"keywords\": [\"legacy\", \"modernizar\", \"migración\", \"php 5\", \"php 8\", \"strangler\", \"compatibilidad\"], \"negative_keywords\": [\"receta\", \"currículum\", \"clima\"]}, \"examples\": [\"Diseña la migración incremental de PHP 5.4 a PHP 8.3.\", \"Crea una estrategia Strangler con pruebas y rollback.\"], \"maturity\": {\"declared\": \"IMPLEMENTED\", \"claim\": \"Paquete, contratos, validación y evaluaciones disponibles.\", \"not_claimed\": [\"OPERATIONAL_LOCAL\", \"INTEGRATED\", \"PRODUCTION_OBSERVED\"]}}")

TOOLS = [
    {"name": "plugin_info", "description": "Describe el plugin y sus límites.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "create_execution_plan", "description": "Crea un plan determinista sin ejecutar.", "inputSchema": {"type": "object", "required": ["task"], "properties": {"task": {"type": "string"}, "target": {"type": "string"}}}},
    {"name": "policy_check", "description": "Clasifica una acción.", "inputSchema": {"type": "object", "required": ["action"], "properties": {"action": {"type": "string"}}}},
]

PLAN_STEPS = [
    "confirm-scope",
    "collect-evidence",
    "select-agent",
    "plan",
    "human-gates",
    "execute-if-authorized",
    "verify",
    "handoff"
]


def _matches(text: str, item: str) -> bool:
    normalized_text = text.casefold().replace("_", "-")
    variants = {item.casefold(), item.casefold().replace("-", " ")}
    return any(variant in normalized_text for variant in variants)


def classify_action(plugin: dict, action: str) -> dict:
    denied = next((item for item in plugin["policy"]["denied"] if _matches(action, item)), None)
    approval = next((item for item in plugin["policy"]["approval_required"] if _matches(action, item)), None)
    decision = "denied" if denied else "approval-required" if approval else "allowed"
    return {"action": action, "decision": decision, "matched": denied or approval}


def result(request_id, payload):
    return {"jsonrpc": "2.0", "id": request_id, "result": payload}


def error(request_id, code, message):
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def handle_message(plugin: dict, message: dict) -> dict | None:
    method = message.get("method")
    request_id = message.get("id")
    if method == "initialize":
        return result(
            request_id,
            {
                "protocolVersion": "2025-11-25",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": plugin["id"] + "-control", "version": plugin["version"]},
            },
        )
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return result(request_id, {"tools": TOOLS})
    if method == "tools/call":
        params = message.get("params", {})
        name = params.get("name")
        arguments = params.get("arguments", {})
        if name == "plugin_info":
            data = {
                "id": plugin["id"],
                "name": plugin["name"],
                "status": plugin["status"],
                "agents": plugin["components"]["agents"],
                "policy": plugin["policy"],
            }
        elif name == "create_execution_plan":
            data = {
                "plugin": plugin["id"],
                "task": arguments.get("task", ""),
                "target": arguments.get("target"),
                "steps": PLAN_STEPS,
            }
        elif name == "policy_check":
            data = classify_action(plugin, str(arguments.get("action", "")))
        else:
            return error(request_id, -32601, "Unknown tool")
        return result(
            request_id,
            {
                "content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False)}],
                "structuredContent": data,
            },
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
