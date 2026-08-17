# OpenAI y Codex

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

Soporte declarado: **native-package**. La raíz del paquete `rootcause-response` contiene todo lo que el host necesita:

| Archivo | Contenido |
|---|---|
| `.codex-plugin/plugin.json` | manifiesto, interfaz y prompts por defecto |
| `skills/` | el workflow del plugin |
| `hooks/hooks.json` | el hook `SessionStart` que anuncia los límites |
| `.mcp.json` | el servidor de control por stdio |

Instala primero el paquete Python para habilitar el ejecutable
`agentic-plugins`, del que dependen el hook y el servidor MCP:

```bash
python -m pip install agentic-plugins-toolkit
agentic-plugins inspect rootcause-response
```

Si prefieres no instalar nada, `runtime/mcp_server.py` es un servidor
autocontenido que solo necesita Python 3.11+ y la biblioteca estándar.
