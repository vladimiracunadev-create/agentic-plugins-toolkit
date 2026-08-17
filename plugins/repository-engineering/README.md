# 🧭 Repository Engineering

> Audita, evoluciona, documenta y prepara releases de repositorios con evidencia y aprobación humana.

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

[Toolkit](https://github.com/vladimiracunadev-create/agentic-plugins-toolkit) · [Contrato](../../docs/PLUGIN_CONTRACT.md) · [Modelo de madurez](../../docs/MATURITY_MODEL.md)

---

## Misión

Convertir mantenimiento amplio en cambios verificables sin confundir documentación, implementación y adopción.

## Ficha

| Campo | Valor |
|---|---|
| Identificador | `repository-engineering` |
| Versión | `0.2.0` |
| Estado | `IMPLEMENTED` |
| Categoría | Developer Tools |
| Riesgo | `high` |
| Agentes | 4 |
| Política por defecto | `allow-read-plan` |

## Agentes

### 🧭 `repository-evolution-agent`

Analiza un repositorio real, separa hechos de promesas y conduce su evolución incremental con pruebas y evidencia.

**Cuándo delegarle trabajo.** Úsalo para examinar, completar, mejorar o evolucionar un repositorio sin romper lo que ya funciona.

**Se detiene en:** `scope_expansion`, `destructive_change`, `external_publish`, `credential_or_paid_service`.

### 📚 `documentation-coherence-agent`

Reconcilia documentación, arquitectura, ejemplos y métricas con las fuentes de verdad del repositorio.

**Cuándo delegarle trabajo.** Úsalo cuando README, docs, conteos, diagramas o ejemplos pueden haberse desalineado del código.

**Se detiene en:** `historical_rewrite`, `public_claim_change`, `generated_docs_overwrite`.

### 🏷️ `release-governance-agent`

Prepara releases coherentes y auditables, valida versiones, pruebas, seguridad, artefactos y rollback antes de publicar.

**Cuándo delegarle trabajo.** Úsalo para preparar una versión, revisar readiness o coordinar un release sin publicar automáticamente.

**Se detiene en:** `version_change`, `tag_or_release_publish`, `registry_upload`, `production_deploy`.

### 🎛️ `repository-maintenance-coordinator`

Coordina especialistas para una misión de mantenimiento amplia, conserva decisiones humanas y consolida una entrega verificable.

**Cuándo delegarle trabajo.** Úsalo cuando una tarea cruza coherencia documental, seguridad, evolución, modernización o release y necesita varios especialistas.

**Se detiene en:** `specialist_scope_expansion`, `mutation_start`, `external_publish`, `release_or_deploy`.

## Cuándo se activa

Señales positivas: `repositorio`, `repository`, `readme`, `documentación`, `release`, `mantenimiento`, `coherencia`.

Señales negativas: `clima`, `receta`, `película`.

```bash
agentic-plugins policy-check repository-engineering --action "publicar el release"
```

## Límites

- **Requieren aprobación humana:** `publish`, `push`, `release`, `delete`, `deploy`, `credential`, `paid`.
- **Denegado siempre, sin excepción:** `bypass-approval`, `exfiltrate-secret`.
- La aprobación humana **no** se delega en otro agente ni en una tool.

El contrato ejecutable está en `policies/policy.json`; esta ficha es una
lectura del mismo dato, no una promesa aparte.

## Skills opcionales

Funciona sin ellos y mejora si están instalados desde [`claude-skills-toolkit`](https://github.com/vladimiracunadev-create/claude-skills-toolkit):

- `md-lint-fix`
- `md-to-doc`
- `pre-push-guard`
- `python-deps-pinning`
- `repo-coherence-audit`
- `security-audit`
- `version-bump`
- `yaml-control`

## Madurez

Declara `IMPLEMENTED`: Paquete, contratos, validación y evaluaciones disponibles.

**No afirma** `OPERATIONAL_LOCAL`, `INTEGRATED`, `PRODUCTION_OBSERVED`.

---

<div align="center"><sub><a href="https://github.com/vladimiracunadev-create/agentic-plugins-toolkit">Toolkit</a> · <a href="../../docs/SECURITY_MODEL.md">Modelo de seguridad</a> · <a href="../../docs/MATURITY_MODEL.md">Madurez</a></sub></div>
