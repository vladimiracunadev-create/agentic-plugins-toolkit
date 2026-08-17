# 🗂️ Portfolio Governance

> Clasifica repositorios, detecta solapamientos y produce una narrativa profesional basada en evidencia.

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

[Toolkit](https://github.com/vladimiracunadev-create/agentic-plugins-toolkit) · [Contrato](../../docs/PLUGIN_CONTRACT.md) · [Modelo de madurez](../../docs/MATURITY_MODEL.md)

---

## Misión

Mantener un catálogo honesto separando aprendizaje, skills, agentes, plugins, casos y productos.

## Ficha

| Campo | Valor |
|---|---|
| Identificador | `portfolio-governance` |
| Versión | `0.2.0` |
| Estado | `IMPLEMENTED` |
| Categoría | Productivity |
| Riesgo | `low` |
| Agentes | 1 |
| Política por defecto | `allow-read-plan` |

## Agentes

### 🗂️ `portfolio-curator-agent`

Clasifica y audita un portafolio de repositorios, detecta solapamientos y produce una narrativa profesional respaldada por evidencia.

**Cuándo delegarle trabajo.** Úsalo para revisar varios repositorios, ordenar el portafolio o preparar evidencia para reclutadores y colaboradores.

**Se detiene en:** `profile_edit`, `repository_archive`, `external_publication`.

## Cuándo se activa

Señales positivas: `portafolio`, `portfolio`, `repositorios`, `github`, `clasificar`, `reclutador`, `catálogo`.

Señales negativas: `borrar`, `producción`, `clima`.

```bash
agentic-plugins policy-check portfolio-governance --action "publicar el release"
```

## Límites

- **Requieren aprobación humana:** `profile-edit`, `archive`, `publish`.
- **Denegado siempre, sin excepción:** `hide-limitations`, `claim-production-without-evidence`.
- La aprobación humana **no** se delega en otro agente ni en una tool.

El contrato ejecutable está en `policies/policy.json`; esta ficha es una
lectura del mismo dato, no una promesa aparte.

## Skills opcionales

Funciona sin ellos y mejora si están instalados desde [`claude-skills-toolkit`](https://github.com/vladimiracunadev-create/claude-skills-toolkit):

- `repo-coherence-audit`
- `web-snap`

## Madurez

Declara `IMPLEMENTED`: Paquete, contratos, validación y evaluaciones disponibles.

**No afirma** `OPERATIONAL_LOCAL`, `INTEGRATED`, `PRODUCTION_OBSERVED`.

---

<div align="center"><sub><a href="https://github.com/vladimiracunadev-create/agentic-plugins-toolkit">Toolkit</a> · <a href="../../docs/SECURITY_MODEL.md">Modelo de seguridad</a> · <a href="../../docs/MATURITY_MODEL.md">Madurez</a></sub></div>
