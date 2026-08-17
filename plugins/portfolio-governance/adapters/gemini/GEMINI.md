# Portfolio Governance

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

Soporte declarado: **generated-instructions**. Esto es una adaptación
portable, no un manifiesto nativo equivalente: Gemini no instala el
paquete, lo lee.

## Cómo usarlo

1. Carga `skills/portfolio-governance-workflow/SKILL.md` como instrucciones.
2. Selecciona el agente adecuado de `agents/`.
3. Conserva `policies/policy.json` como límite duro de la sesión.
4. Conecta `runtime/mcp_server.py` si el host soporta MCP por stdio.

## Misión

Mantener un catálogo honesto separando aprendizaje, skills, agentes, plugins, casos y productos.

## Límites que no se negocian

Requieren aprobación humana explícita: `profile-edit`, `archive`, `publish`.

Denegado siempre: `hide-limitations`, `claim-production-without-evidence`.
