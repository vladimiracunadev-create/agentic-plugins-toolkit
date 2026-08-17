# Product Evolution

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

Soporte declarado: **generated-instructions**. Esto es una adaptación
portable, no un manifiesto nativo equivalente: Gemini no instala el
paquete, lo lee.

## Cómo usarlo

1. Carga `skills/product-evolution-workflow/SKILL.md` como instrucciones.
2. Selecciona el agente adecuado de `agents/`.
3. Conserva `policies/policy.json` como límite duro de la sesión.
4. Conecta `runtime/mcp_server.py` si el host soporta MCP por stdio.

## Misión

Alinear intención, experiencia de usuario, arquitectura y evidencia para entregar el siguiente incremento útil.

## Límites que no se negocian

Requieren aprobación humana explícita: `breaking-change`, `external-integration`, `release`, `scope-expansion`.

Denegado siempre: `misrepresent-status`, `bypass-approval`.
