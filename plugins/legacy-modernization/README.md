# 🏗️ Legacy Modernization

> Planifica y ejecuta modernizaciones incrementales preservando contratos, continuidad y rollback.

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

[Toolkit](https://github.com/vladimiracunadev-create/agentic-plugins-toolkit) · [Contrato](../../docs/PLUGIN_CONTRACT.md) · [Modelo de madurez](../../docs/MATURITY_MODEL.md)

---

## Misión

Reducir deuda y riesgo mediante rebanadas reversibles, pruebas de caracterización y gates de migración.

## Ficha

| Campo | Valor |
|---|---|
| Identificador | `legacy-modernization` |
| Versión | `0.2.0` |
| Estado | `IMPLEMENTED` |
| Categoría | Developer Tools |
| Riesgo | `high` |
| Agentes | 1 |
| Política por defecto | `allow-read-plan` |

## Agentes

### 🏗️ `legacy-modernization-agent`

Diseña y ejecuta modernizaciones incrementales de sistemas legacy preservando continuidad, contratos y rollback.

**Cuándo delegarle trabajo.** Úsalo para migraciones de lenguaje, framework, base de datos, infraestructura o arquitectura con continuidad operativa.

**Se detiene en:** `data_migration`, `contract_break`, `production_cutover`, `dependency_removal`.

## Cuándo se activa

Señales positivas: `legacy`, `modernizar`, `migración`, `php 5`, `php 8`, `strangler`, `compatibilidad`.

Señales negativas: `receta`, `currículum`, `clima`.

```bash
agentic-plugins policy-check legacy-modernization --action "publicar el release"
```

## Límites

- **Requieren aprobación humana:** `data-migration`, `cutover`, `remove-dependency`, `production`, `contract-break`.
- **Denegado siempre, sin excepción:** `big-bang-without-rollback`, `bypass-approval`.
- La aprobación humana **no** se delega en otro agente ni en una tool.

El contrato ejecutable está en `policies/policy.json`; esta ficha es una
lectura del mismo dato, no una promesa aparte.

## Skills opcionales

Funciona sin ellos y mejora si están instalados desde [`claude-skills-toolkit`](https://github.com/vladimiracunadev-create/claude-skills-toolkit):

- `pre-push-guard`
- `python-version-control`
- `repo-coherence-audit`
- `security-audit`
- `yaml-control`

## Madurez

Declara `IMPLEMENTED`: Paquete, contratos, validación y evaluaciones disponibles.

**No afirma** `OPERATIONAL_LOCAL`, `INTEGRATED`, `PRODUCTION_OBSERVED`.

---

<div align="center"><sub><a href="https://github.com/vladimiracunadev-create/agentic-plugins-toolkit">Toolkit</a> · <a href="../../docs/SECURITY_MODEL.md">Modelo de seguridad</a> · <a href="../../docs/MATURITY_MODEL.md">Madurez</a></sub></div>
