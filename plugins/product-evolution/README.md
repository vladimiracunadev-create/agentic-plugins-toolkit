# 🚀 Product Evolution

> Convierte productos parciales en incrementos priorizados, compatibles y verificables.

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

[Toolkit](https://github.com/vladimiracunadev-create/agentic-plugins-toolkit) · [Contrato](../../docs/PLUGIN_CONTRACT.md) · [Modelo de madurez](../../docs/MATURITY_MODEL.md)

---

## Misión

Alinear intención, experiencia de usuario, arquitectura y evidencia para entregar el siguiente incremento útil.

## Ficha

| Campo | Valor |
|---|---|
| Identificador | `product-evolution` |
| Versión | `0.2.0` |
| Estado | `IMPLEMENTED` |
| Categoría | Productivity |
| Riesgo | `medium` |
| Agentes | 1 |
| Política por defecto | `allow-read-plan` |

## Agentes

### 🚀 `product-evolution-agent`

Evalúa productos parciales, alinea producto y arquitectura y convierte brechas en entregas evolutivas verificables.

**Cuándo delegarle trabajo.** Úsalo cuando un producto ya existe parcialmente y necesita prioridades, fases y mejoras sin perder compatibilidad.

**Se detiene en:** `scope_expansion`, `breaking_change`, `external_integration`, `release`.

## Cuándo se activa

Señales positivas: `producto`, `roadmap`, `mvp`, `incremento`, `funcionalidad`, `product`, `backlog`.

Señales negativas: `incidente`, `receta`, `clima`.

```bash
agentic-plugins policy-check product-evolution --action "publicar el release"
```

## Límites

- **Requieren aprobación humana:** `breaking-change`, `external-integration`, `release`, `scope-expansion`.
- **Denegado siempre, sin excepción:** `misrepresent-status`, `bypass-approval`.
- La aprobación humana **no** se delega en otro agente ni en una tool.

El contrato ejecutable está en `policies/policy.json`; esta ficha es una
lectura del mismo dato, no una promesa aparte.

## Skills opcionales

Funciona sin ellos y mejora si están instalados desde [`claude-skills-toolkit`](https://github.com/vladimiracunadev-create/claude-skills-toolkit):

- `md-lint-fix`
- `pre-push-guard`
- `repo-coherence-audit`
- `security-audit`

## Madurez

Declara `IMPLEMENTED`: Paquete, contratos, validación y evaluaciones disponibles.

**No afirma** `OPERATIONAL_LOCAL`, `INTEGRATED`, `PRODUCTION_OBSERVED`.

---

<div align="center"><sub><a href="https://github.com/vladimiracunadev-create/agentic-plugins-toolkit">Toolkit</a> · <a href="../../docs/SECURITY_MODEL.md">Modelo de seguridad</a> · <a href="../../docs/MATURITY_MODEL.md">Madurez</a></sub></div>
