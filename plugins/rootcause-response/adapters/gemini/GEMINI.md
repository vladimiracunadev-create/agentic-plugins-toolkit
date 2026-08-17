# RootCause Response

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

Soporte declarado: **generated-instructions**. Esto es una adaptación
portable, no un manifiesto nativo equivalente: Gemini no instala el
paquete, lo lee.

## Cómo usarlo

1. Carga `skills/rootcause-response-workflow/SKILL.md` como instrucciones.
2. Selecciona el agente adecuado de `agents/`.
3. Conserva `policies/policy.json` como límite duro de la sesión.
4. Conecta `runtime/mcp_server.py` si el host soporta MCP por stdio.

## Misión

Reducir incertidumbre, preservar evidencia y remediar sin introducir un segundo incidente.

## Límites que no se negocian

Requieren aprobación humana explícita: `production-command`, `service-restart`, `configuration-change`, `credential`, `deploy`.

Denegado siempre: `destroy-evidence`, `exploit-third-party`, `bypass-approval`.
