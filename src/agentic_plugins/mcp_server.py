"""Servidor MCP de control, por stdio y sin dependencias.

Expone tres tools deterministas —`plugin_info`, `create_execution_plan` y
`policy_check`— que describen, planifican y clasifican, pero **no ejecutan**: no
escriben archivos, no abren red y no invocan modelos. Las acciones reales viven
en las tools del host y quedan sujetas a sus permisos.

La versión del protocolo y los pasos del plan salen del catálogo, no de una
constante local, para que este servidor y los seis servidores autocontenidos que
se distribuyen dentro de los paquetes no puedan declarar cosas distintas.
"""

from __future__ import annotations

import json
import sys

from .catalog import find_root, load_catalog, plugins_by_id
from .policy import classify_action


def result(request_id, payload):
    return {"jsonrpc": "2.0", "id": request_id, "result": payload}


def error(request_id, code, message):
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }


TOOLS = [
    {
        "name": "plugin_info",
        "description": "Describe el plugin y sus límites.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "create_execution_plan",
        "description": "Crea un plan determinista sin ejecutar.",
        "inputSchema": {
            "type": "object",
            "required": ["task"],
            "properties": {"task": {"type": "string"}, "target": {"type": "string"}},
        },
    },
    {
        "name": "policy_check",
        "description": "Clasifica una acción.",
        "inputSchema": {
            "type": "object",
            "required": ["action"],
            "properties": {"action": {"type": "string"}},
        },
    },
]


def handle_message(
    plugin: dict,
    message: dict,
    protocol: str = "2025-11-25",
    steps: list[str] | None = None,
) -> dict | None:
    method = message.get("method")
    request_id = message.get("id")
    if method == "initialize":
        return result(
            request_id,
            {
                "protocolVersion": protocol,
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": plugin["id"] + "-control",
                    "version": plugin["version"],
                },
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
                "steps": list(steps or []),
            }
        elif name == "policy_check":
            data = classify_action(plugin, str(arguments.get("action", "")))
        else:
            return error(request_id, -32601, "Unknown tool")
        return result(
            request_id,
            {
                "content": [
                    {"type": "text", "text": json.dumps(data, ensure_ascii=False)}
                ],
                "structuredContent": data,
            },
        )
    return error(request_id, -32601, "Method not found")


def serve(plugin_id: str) -> int:
    catalog = load_catalog(find_root())
    plugin = plugins_by_id(catalog).get(plugin_id)
    if plugin is None:
        print(f"Plugin desconocido: {plugin_id}", file=sys.stderr)
        return 2
    protocol = catalog["mcp_protocol_version"]
    steps = catalog["execution_plan_steps"]
    for line in sys.stdin:
        if not line.strip():
            continue
        # Un mensaje malformado no debe tumbar el servidor: se responde con un
        # error JSON-RPC y la sesión continúa, que es lo que espera el host.
        try:
            answer = handle_message(plugin, json.loads(line), protocol, steps)
            if answer is not None:
                print(json.dumps(answer, ensure_ascii=False), flush=True)
        except (ValueError, KeyError, TypeError) as exc:
            print(json.dumps(error(None, -32603, str(exc))), flush=True)
    return 0
