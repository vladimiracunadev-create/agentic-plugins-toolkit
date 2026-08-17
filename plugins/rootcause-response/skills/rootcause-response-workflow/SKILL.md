---
name: rootcause-response-workflow
description: Investiga incidentes y convierte hallazgos técnicos o de seguridad en remediaciones verificables. Usar cuando la solicitud coincida con la misión de RootCause Response.
license: MIT
compatibility: El servidor MCP local es opcional; no requiere una API de modelo.
metadata:
  author: Vladimir Acuña
  version: "0.2.0"
---

# RootCause Response workflow

1. Confirma objetivo, alcance, destino y autorización.
2. Inspecciona evidencia antes de concluir.
3. Selecciona el agente mínimo para la misión.
4. Produce un plan reversible con criterios de verificación.
5. Detente en todo gate humano.
6. Entrega resultado, pruebas y riesgo residual.

## Agentes

- incident-root-cause-agent
- security-remediation-agent

## Requieren aprobación

- production-command
- service-restart
- configuration-change
- credential
- deploy

## Denegado siempre

- destroy-evidence
- exploit-third-party
- bypass-approval

## Ejemplos

- Construye la línea temporal y prueba hipótesis para este incidente.
- Prioriza remediaciones sin ejecutar cambios productivos.

Si falta una dependencia opcional, continúa con las instrucciones
integradas y declara la limitación. No descargues código silenciosamente.
