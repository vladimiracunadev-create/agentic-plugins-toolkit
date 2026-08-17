# 🎓 Learning Program Studio

> Diseña programas educativos evolutivos con currículo, clases, laboratorios, evaluaciones y capstones.

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

[Toolkit](https://github.com/vladimiracunadev-create/agentic-plugins-toolkit) · [Contrato](../../docs/PLUGIN_CONTRACT.md) · [Modelo de madurez](../../docs/MATURITY_MODEL.md)

---

## Misión

Transformar un dominio en una experiencia formativa profunda, ejecutable, trazable y mantenible.

## Ficha

| Campo | Valor |
|---|---|
| Identificador | `learning-program-studio` |
| Versión | `0.2.0` |
| Estado | `IMPLEMENTED` |
| Categoría | Education |
| Riesgo | `medium` |
| Agentes | 1 |
| Política por defecto | `allow-read-plan` |

## Agentes

### 🎓 `learning-program-architect`

Diseña y mantiene programas educativos evolutivos con progresión, laboratorios, evaluaciones y trazabilidad curricular.

**Cuándo delegarle trabajo.** Úsalo para crear o ampliar repositorios de aprendizaje desde nivel inicial hasta avanzado.

**Se detiene en:** `scope_or_duration_change`, `licensed_dataset`, `paid_dependency`, `publication`.

## Cuándo se activa

Señales positivas: `curso`, `programa`, `aprendizaje`, `clases`, `laboratorio`, `evaluación`, `capstone`.

Señales negativas: `incidente`, `despliegue`, `clima`.

```bash
agentic-plugins policy-check learning-program-studio --action "publicar el release"
```

## Límites

- **Requieren aprobación humana:** `licensed-dataset`, `paid-service`, `publish`, `scope-expansion`.
- **Denegado siempre, sin excepción:** `copy-without-license`, `fake-completeness`.
- La aprobación humana **no** se delega en otro agente ni en una tool.

El contrato ejecutable está en `policies/policy.json`; esta ficha es una
lectura del mismo dato, no una promesa aparte.

## Skills opcionales

Funciona sin ellos y mejora si están instalados desde [`claude-skills-toolkit`](https://github.com/vladimiracunadev-create/claude-skills-toolkit):

- `md-lint-fix`
- `md-to-doc`
- `repo-coherence-audit`
- `yaml-control`

## Madurez

Declara `IMPLEMENTED`: Paquete, contratos, validación y evaluaciones disponibles.

**No afirma** `OPERATIONAL_LOCAL`, `INTEGRATED`, `PRODUCTION_OBSERVED`.

---

<div align="center"><sub><a href="https://github.com/vladimiracunadev-create/agentic-plugins-toolkit">Toolkit</a> · <a href="../../docs/SECURITY_MODEL.md">Modelo de seguridad</a> · <a href="../../docs/MATURITY_MODEL.md">Madurez</a></sub></div>
