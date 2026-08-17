# 🩺 RootCause Response

> Investiga incidentes y convierte hallazgos técnicos o de seguridad en remediaciones verificables.

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

[Toolkit](https://github.com/vladimiracunadev-create/agentic-plugins-toolkit) · [Contrato](../../docs/PLUGIN_CONTRACT.md) · [Modelo de madurez](../../docs/MATURITY_MODEL.md)

---

## Misión

Reducir incertidumbre, preservar evidencia y remediar sin introducir un segundo incidente.

## Ficha

| Campo | Valor |
|---|---|
| Identificador | `rootcause-response` |
| Versión | `0.2.0` |
| Estado | `IMPLEMENTED` |
| Categoría | Security |
| Riesgo | `high` |
| Agentes | 2 |
| Política por defecto | `allow-read-plan` |

## Agentes

### 🩺 `incident-root-cause-agent`

Investiga incidentes técnicos con línea temporal, hipótesis falsables, evidencia y acciones correctivas sin culpar personas.

**Cuándo delegarle trabajo.** Úsalo para errores intermitentes, degradaciones, fallas de CI, incidentes de producción o causas desconocidas.

**Se detiene en:** `production_command`, `data_export`, `service_restart`, `configuration_change`.

### 🛡️ `security-remediation-agent`

Convierte hallazgos de seguridad en remediaciones priorizadas, compatibles y verificadas, con cobertura y riesgo residual explícitos.

**Cuándo delegarle trabajo.** Úsalo después de un audit, alerta de dependencia, secreto expuesto o hallazgo SAST que requiere análisis y corrección.

**Se detiene en:** `credential_rotation`, `breaking_dependency_upgrade`, `security_control_disable`, `production_change`.

## Cuándo se activa

Señales positivas: `incidente`, `root cause`, `causa raíz`, `vulnerabilidad`, `seguridad`, `remediación`, `falla`.

Señales negativas: `curso`, `portafolio`, `clima`.

```bash
agentic-plugins policy-check rootcause-response --action "publicar el release"
```

## Límites

- **Requieren aprobación humana:** `production-command`, `service-restart`, `configuration-change`, `credential`, `deploy`.
- **Denegado siempre, sin excepción:** `destroy-evidence`, `exploit-third-party`, `bypass-approval`.
- La aprobación humana **no** se delega en otro agente ni en una tool.

El contrato ejecutable está en `policies/policy.json`; esta ficha es una
lectura del mismo dato, no una promesa aparte.

## Skills opcionales

Funciona sin ellos y mejora si están instalados desde [`claude-skills-toolkit`](https://github.com/vladimiracunadev-create/claude-skills-toolkit):

- `docker-compose-doctor`
- `pre-push-guard`
- `python-deps-pinning`
- `repo-coherence-audit`
- `security-audit`
- `yaml-control`

## Madurez

Declara `IMPLEMENTED`: Paquete, contratos, validación y evaluaciones disponibles.

**No afirma** `OPERATIONAL_LOCAL`, `INTEGRATED`, `PRODUCTION_OBSERVED`.

---

<div align="center"><sub><a href="https://github.com/vladimiracunadev-create/agentic-plugins-toolkit">Toolkit</a> · <a href="../../docs/SECURITY_MODEL.md">Modelo de seguridad</a> · <a href="../../docs/MATURITY_MODEL.md">Madurez</a></sub></div>
