# 🔗 Cadena de suministro

> De dónde viene cada pieza de un paquete, cómo se verifica que no cambió y qué todavía no está firmado.

[Repositorio](../README.md) · [Documentación](README.md) · [Modelo de seguridad](SECURITY_MODEL.md)

---

## Las tres procedencias

Un paquete contiene material de tres orígenes distintos, y los trata de forma distinta:

| Origen | Qué aporta | Cómo entra |
|---|---|---|
| Este repositorio | contrato, políticas, workflow, manifiestos, MCP, adaptadores | generado desde `catalog/plugins.yaml` |
| [`operational-ai-agents`](https://github.com/vladimiracunadev-create/operational-ai-agents) | los diez agentes | **instantánea versionada** en `catalog/agents.snapshot.json` |
| [`claude-skills-toolkit`](https://github.com/vladimiracunadev-create/claude-skills-toolkit) | skills opcionales | **declarados por nombre**, nunca copiados |

### Por qué instantánea y no submódulo

Un paquete distribuible tiene que ser **autocontenido y auditable en el momento en que se construyó**. Un submódulo apuntaría a un repositorio vivo: lo que se validó en CI y lo que llega al usuario podrían no ser lo mismo.

La instantánea declara su versión de origen (`agents_snapshot_version: 0.1.0`) y actualizarla es un acto explícito que pasa por revisión y changelog.

### Por qué los skills se declaran y no se copian

Un plugin **funciona sin sus skills opcionales**. Copiarlos crearía tres problemas: duplicación con un repositorio que evoluciona por su cuenta, licencias arrastradas y un paquete que engorda sin necesidad.

```json
"optional_skills": ["md-lint-fix", "security-audit", "version-bump", "…"]
```

Si falta uno, el workflow continúa con sus instrucciones integradas y **declara la limitación**. Lo que no hace nunca es descargarlo en silencio.

## `provenance.json`

Cada paquete lleva uno, generado:

```json
{
  "plugin": "repository-engineering",
  "version": "0.2.0",
  "generated_from": {
    "plugin_catalog": "catalog/plugins.yaml",
    "agent_snapshot": "catalog/agents.snapshot.json",
    "agent_repository": "operational-ai-agents",
    "agent_repository_version": "0.1.0"
  },
  "optional_skill_source": {
    "repository": "claude-skills-toolkit",
    "mode": "optional-versioned-dependencies",
    "skills": ["…"]
  },
  "generated_files_are_distribution_views": true,
  "production_claim": false,
  "declared_maturity": "IMPLEMENTED",
  "not_claimed": ["OPERATIONAL_LOCAL", "INTEGRATED", "PRODUCTION_OBSERVED"]
}
```

`production_claim: false` viaja **dentro del paquete**: un host que lo inspeccione sabe, sin leer este repositorio, que el plugin no afirma uso productivo.

## Paquetes reproducibles

```bash
agentic-plugins package --all --output dist
cat dist/checksums.json
```

Determinismo garantizado por tres decisiones en el empaquetador:

- los archivos se recorren **ordenados** alfabéticamente;
- la marca temporal se fija en `1980-01-01 00:00:00`;
- los permisos se fijan en `0644` y se excluyen `__pycache__` y `.DS_Store`.

El mismo contenido produce el mismo SHA-256 en cualquier máquina y en cualquier momento. **CI lo comprueba de verdad**: el job `packages` empaqueta dos veces en directorios distintos y hace `diff` de los `checksums.json`. Si el empaquetado dejara de ser determinista, la build cae.

`test_packages_are_reproducible` lo verifica también en las nueve combinaciones de sistema operativo y versión de Python.

## Dependencias del propio toolkit

- **Runtime: cero.** La CLI usa solo la biblioteca estándar. No hay árbol de dependencias que auditar.
- **Desarrollo: una.** `ruff`, opcional, en el extra `dev`.
- **CI:** todas las acciones de GitHub están **fijadas por SHA de commit**, no por etiqueta. Una etiqueta se puede reapuntar; un SHA no.
- **Dependabot** revisa mensualmente pip, GitHub Actions y Docker.
- **CodeQL** analiza el código en cada push y cada lunes.

## Lo que todavía no hay

Se declara para no confundir «verificable» con «firmado»:

- **No hay firma criptográfica** de los paquetes. Hay SHA-256, que detecta alteración si tienes el digest de referencia por un canal confiable, pero no autentica al autor.
- **No hay SBOM** por plugin.
- **No hay registry**: la distribución es por repositorio y por ZIP.

Las tres cosas están en el [roadmap](../ROADMAP.md) como pendientes, no como hechas.

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="SECURITY_MODEL.md">Modelo de seguridad</a> · <a href="../ROADMAP.md">Roadmap</a></sub></div>
