# 🔌 MCP

> Las tres tools que expone cada plugin, las dos formas de levantar el servidor y por qué ambas responden exactamente lo mismo.

[Repositorio](../README.md) · [Documentación](README.md) · [CLI](CLI.md)

---

## Dos servidores, una semántica

Cada plugin se puede servir de dos maneras:

```bash
# 1 · a través de la CLI instalada
agentic-plugins mcp --plugin repository-engineering

# 2 · directamente el archivo que viaja dentro del paquete
python plugins/repository-engineering/runtime/mcp_server.py
```

La segunda existe para hosts que prefieren ejecutar un archivo sin instalar nada: solo necesita Python 3.11+ y la biblioteca estándar.

> [!IMPORTANT]
> `runtime/mcp_server.py` es una **vista generada**. `render.py` lo produce copiando el **código fuente literal** de `policy._matches` y `policy.classify_action`, de modo que no puede reimplementar la semántica ni derivar de ella. `test_distributed_server_agrees_with_the_cli` levanta ambos servidores y compara sus respuestas acción por acción.
>
> No es una precaución teórica: en la versión anterior ese archivo se mantenía a mano, comparaba con `x in action.lower()` y devolvía `allowed` para `BYPASS_APPROVAL` mientras la CLI devolvía `denied`.

### Registro en un host

Cada paquete trae su `.mcp.json`:

```json
{
  "mcpServers": {
    "repository-engineering-control": {
      "command": "agentic-plugins",
      "args": ["mcp", "--plugin", "repository-engineering"]
    }
  }
}
```

## Las tres tools

### `plugin_info`

Sin argumentos. Devuelve identidad, estado, agentes y política completa.

```json
{
  "id": "repository-engineering",
  "name": "Repository Engineering",
  "status": "IMPLEMENTED",
  "agents": ["repository-evolution-agent", "…"],
  "policy": {
    "default": "allow-read-plan",
    "approval_required": ["publish", "push", "release", "…"],
    "denied": ["bypass-approval", "exfiltrate-secret"],
    "human_approval_cannot_be_delegated": true
  }
}
```

### `create_execution_plan`

Requiere `task`, acepta `target`. Devuelve un plan determinista de ocho pasos, **sin ejecutar ninguno**:

```text
confirm-scope → collect-evidence → select-agent → plan
→ human-gates → execute-if-authorized → verify → handoff
```

Los pasos salen de `execution_plan_steps` en el catálogo, no de una constante local, para que la CLI y los seis servidores distribuidos no puedan declarar planes distintos.

### `policy_check`

Requiere `action`. Clasifica en `allowed`, `approval-required` o `denied`.

```json
{"action": "publicar el release", "decision": "approval-required", "matched": "release"}
```

La comparación normaliza mayúsculas y trata `_` y `-` como equivalentes.

## Qué no hace ninguna tool

- No escribe archivos.
- No abre conexiones de red.
- No ejecuta comandos.
- No invoca un modelo.

Las acciones reales viven en las tools del host y quedan sujetas a sus permisos. El servidor describe, planifica y clasifica; ahí termina su alcance.

## Protocolo

`protocolVersion` sale de `mcp_protocol_version` en el catálogo: hoy `2025-11-25`. Métodos soportados:

| Método | Respuesta |
|---|---|
| `initialize` | versión de protocolo, capacidades y `serverInfo` con la versión del plugin |
| `notifications/initialized` | ninguna, por diseño |
| `tools/list` | las tres tools con su `inputSchema` |
| `tools/call` | `content` textual + `structuredContent` |
| cualquier otro | error `-32601` |

Un mensaje malformado responde `-32603` y **la sesión continúa**: un JSON roto no debe tumbar el servidor.

## Probarlo a mano

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"policy_check","arguments":{"action":"desplegar a producción"}}}' \
  | python plugins/repository-engineering/runtime/mcp_server.py
```

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="CLI.md">CLI</a> · <a href="SECURITY_MODEL.md">Modelo de seguridad</a></sub></div>
