---
name: repository-engineering-workflow
description: Audita, evoluciona, documenta y prepara releases de repositorios con evidencia y aprobación humana. Usar cuando la solicitud coincida con la misión de Repository Engineering.
license: MIT
compatibility: El servidor MCP local es opcional; no requiere una API de modelo.
metadata:
  author: Vladimir Acuña
  version: "0.2.0"
---

# Repository Engineering workflow

1. Confirma objetivo, alcance, destino y autorización.
2. Inspecciona evidencia antes de concluir.
3. Selecciona el agente mínimo para la misión.
4. Produce un plan reversible con criterios de verificación.
5. Detente en todo gate humano.
6. Entrega resultado, pruebas y riesgo residual.

## Agentes

- repository-evolution-agent
- documentation-coherence-agent
- release-governance-agent
- repository-maintenance-coordinator

## Requieren aprobación

- publish
- push
- release
- delete
- deploy
- credential
- paid

## Denegado siempre

- bypass-approval
- exfiltrate-secret

## Ejemplos

- Examina este repositorio y separa lo implementado de lo prometido.
- Prepara una evolución verificable y detente antes de publicar.

Si falta una dependencia opcional, continúa con las instrucciones
integradas y declara la limitación. No descargues código silenciosamente.
