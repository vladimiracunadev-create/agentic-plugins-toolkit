# Legacy Modernization

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

Soporte declarado: **generated-instructions**. Esto es una adaptación
portable, no un manifiesto nativo equivalente: Gemini no instala el
paquete, lo lee.

## Cómo usarlo

1. Carga `skills/legacy-modernization-workflow/SKILL.md` como instrucciones.
2. Selecciona el agente adecuado de `agents/`.
3. Conserva `policies/policy.json` como límite duro de la sesión.
4. Conecta `runtime/mcp_server.py` si el host soporta MCP por stdio.

## Misión

Reducir deuda y riesgo mediante rebanadas reversibles, pruebas de caracterización y gates de migración.

## Límites que no se negocian

Requieren aprobación humana explícita: `data-migration`, `cutover`, `remove-dependency`, `production`, `contract-break`.

Denegado siempre: `big-bang-without-rollback`, `bypass-approval`.
