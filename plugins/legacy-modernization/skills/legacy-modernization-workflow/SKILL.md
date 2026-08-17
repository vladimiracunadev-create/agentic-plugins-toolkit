---
name: legacy-modernization-workflow
description: Planifica y ejecuta modernizaciones incrementales preservando contratos, continuidad y rollback. Usar cuando la solicitud coincida con la misión de Legacy Modernization.
license: MIT
compatibility: El servidor MCP local es opcional; no requiere una API de modelo.
metadata:
  author: Vladimir Acuña
  version: "0.2.0"
---

# Legacy Modernization workflow

1. Confirma objetivo, alcance, destino y autorización.
2. Inspecciona evidencia antes de concluir.
3. Selecciona el agente mínimo para la misión.
4. Produce un plan reversible con criterios de verificación.
5. Detente en todo gate humano.
6. Entrega resultado, pruebas y riesgo residual.

## Agentes

- legacy-modernization-agent

## Requieren aprobación

- data-migration
- cutover
- remove-dependency
- production
- contract-break

## Denegado siempre

- big-bang-without-rollback
- bypass-approval

## Ejemplos

- Diseña la migración incremental de PHP 5.4 a PHP 8.3.
- Crea una estrategia Strangler con pruebas y rollback.

Si falta una dependencia opcional, continúa con las instrucciones
integradas y declara la limitación. No descargues código silenciosamente.
