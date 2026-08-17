# 🆘 Soporte

> Cómo pedir ayuda de forma que se pueda resolver, y qué no debes adjuntar nunca.

[Repositorio](README.md) · [Instalación](INSTALL.md) · [CLI](docs/CLI.md)

---

## Antes de reportar

Ejecuta el diagnóstico y adjunta su salida:

```bash
agentic-plugins doctor
agentic-plugins validate
python -m unittest discover -s tests -v
```

Muchos problemas de instalación se resuelven con la tabla de [síntomas frecuentes](INSTALL.md#problemas-frecuentes); si estás en Windows, empieza por [docs/WINDOWS.md](docs/WINDOWS.md).

## Dónde escribir

| Situación | Canal |
|---|---|
| Defecto reproducible | [Abrir un issue de bug](https://github.com/vladimiracunadev-create/agentic-plugins-toolkit/issues/new?template=bug.yml) |
| Proponer un plugin nuevo | [Propuesta de plugin](https://github.com/vladimiracunadev-create/agentic-plugins-toolkit/issues/new?template=plugin_proposal.yml) |
| Duda de uso o instalación | [Discussions](https://github.com/vladimiracunadev-create/agentic-plugins-toolkit/discussions) |
| Vulnerabilidad | [Aviso privado](https://github.com/vladimiracunadev-create/agentic-plugins-toolkit/security/advisories/new) — nunca un issue público |

## Qué incluir

- Sistema operativo y versión de Python.
- Comando exacto que ejecutaste y salida completa **sanitizada**.
- Plugin afectado y host donde lo instalaste, si aplica.
- Qué esperabas que ocurriera.

## Qué no incluir

> [!CAUTION]
> Nada de esto debe aparecer en un issue: secretos, tokens, credenciales, prompts privados, datos personales, rutas locales que te identifiquen ni trazas de repositorios de terceros.

Si la evidencia relevante contiene algo de eso, sustitúyelo por `<redactado: motivo>` en vez de borrarlo en silencio, para que el reporte siga siendo legible.

## Autodiagnóstico rápido

| Síntoma | Comprobación |
|---|---|
| «No se encontró catalog/plugins.yaml» | ¿estás dentro del repositorio? ¿`AGENTIC_PLUGINS_ROOT` apunta a otro sitio? |
| `sync --check` falla justo tras clonar | finales de línea: `git add --renormalize .` |
| Una evaluación falla tras editar el catálogo | `agentic-plugins eval <plugin> --json` muestra esperado y obtenido |
| El hook no aparece en la sesión | ¿el paquete está instalado en el intérprete que usa el host? `agentic-plugins doctor` |
| Acentos rotos en Windows | `$env:PYTHONUTF8 = "1"` |
| «Conflicto no administrado» al exportar | ya existe un directorio tuyo con ese nombre; renómbralo o cambia `--target` |
| El panel se niega a arrancar | `serve` solo enlaza loopback salvo opt-in explícito; es intencional |

---

<div align="center"><sub><a href="README.md">Repositorio</a> · <a href="CONTRIBUTING.md">Contribuir</a> · <a href="SECURITY.md">Seguridad</a></sub></div>
