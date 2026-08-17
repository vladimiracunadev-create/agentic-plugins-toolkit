# Repository Engineering

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

Soporte declarado: **generated-instructions**. Esto es una adaptación
portable, no un manifiesto nativo equivalente: Gemini no instala el
paquete, lo lee.

## Cómo usarlo

1. Carga `skills/repository-engineering-workflow/SKILL.md` como instrucciones.
2. Selecciona el agente adecuado de `agents/`.
3. Conserva `policies/policy.json` como límite duro de la sesión.
4. Conecta `runtime/mcp_server.py` si el host soporta MCP por stdio.

## Misión

Convertir mantenimiento amplio en cambios verificables sin confundir documentación, implementación y adopción.

## Límites que no se negocian

Requieren aprobación humana explícita: `publish`, `push`, `release`, `delete`, `deploy`, `credential`, `paid`.

Denegado siempre: `bypass-approval`, `exfiltrate-secret`.
