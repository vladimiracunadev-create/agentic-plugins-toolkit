---
name: product-evolution-workflow
description: Convierte productos parciales en incrementos priorizados, compatibles y verificables. Usar cuando la solicitud coincida con la misión de Product Evolution.
license: MIT
compatibility: El servidor MCP local es opcional; no requiere una API de modelo.
metadata:
  author: Vladimir Acuña
  version: "0.2.0"
---

# Product Evolution workflow

1. Confirma objetivo, alcance, destino y autorización.
2. Inspecciona evidencia antes de concluir.
3. Selecciona el agente mínimo para la misión.
4. Produce un plan reversible con criterios de verificación.
5. Detente en todo gate humano.
6. Entrega resultado, pruebas y riesgo residual.

## Agentes

- product-evolution-agent

## Requieren aprobación

- breaking-change
- external-integration
- release
- scope-expansion

## Denegado siempre

- misrepresent-status
- bypass-approval

## Ejemplos

- Diferencia stubs, partes funcionales y roadmap de este producto.
- Construye el siguiente incremento sin romper formatos anteriores.

Si falta una dependencia opcional, continúa con las instrucciones
integradas y declara la limitación. No descargues código silenciosamente.
