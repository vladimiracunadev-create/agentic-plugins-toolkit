# 🔧 Instrucciones para mantener este repositorio

> Para agentes y para personas. Lo que hay que saber antes de tocar nada, y las trampas que ya costaron una versión.

[Repositorio](README.md) · [Contribuir](CONTRIBUTING.md) · [Guía de autoría](docs/AUTHORING_GUIDE.md)

---

## La regla que lo domina todo

**`catalog/plugins.yaml` es la fuente de verdad.** De él se generan **69 archivos**. El único archivo escrito a mano dentro de un paquete es `plugins/<id>/evals/cases.jsonl`.

Si editas una vista generada, `sync` la sobrescribe y CI falla con drift. El cambio va siempre en uno de estos tres sitios:

| Quieres cambiar | Edita |
|---|---|
| Un dato del plugin (misión, política, agentes, keywords) | `catalog/plugins.yaml` |
| El **formato** de una vista (ficha, adaptador, manifiesto) | `src/agentic_plugins/render.py` |
| La **semántica** de política o routing | `src/agentic_plugins/policy.py` |

## Trampas conocidas

### 1 · `policy.py` se copia dentro de los paquetes

`render.py` usa `inspect.getsource` para copiar el código fuente literal de `policy._matches` y `policy.classify_action` a los seis `runtime/mcp_server.py`. Es deliberado: así el servidor que viaja dentro del paquete no puede clasificar una acción de forma distinta a la CLI.

**Consecuencia:** cualquier cambio en esas dos funciones exige `agentic-plugins sync` **en el mismo commit**. Si no, CI falla con drift en seis archivos y el motivo no es evidente a primera vista.

Esta trampa existe porque su ausencia costó un bug real: la versión 0.1.0 mantenía esos archivos a mano y devolvían `allowed` para `BYPASS_APPROVAL` mientras la CLI devolvía `denied`.

### 2 · Añadir un archivo a un paquete rompe la validación

El validador rechaza cualquier archivo dentro de `plugins/<id>/` que no sea una vista generada o el `cases.jsonl`. **Eso es intencional.** Si de verdad necesitas uno nuevo:

- lo correcto casi siempre es generarlo desde `render.py`;
- si no puede generarse, hay que añadirlo a `AUTHORED_FILES` en `validator.py`, y eso pasa por [GOVERNANCE.md](GOVERNANCE.md).

### 3 · No promociones madurez sin evidencia

Los seis plugins declaran `IMPLEMENTED`. Cambiar ese `status` requiere un caso real sanitizado en `evidence/`, revisado por una persona. Un agente **no** puede promoverlo. Criterios en [docs/MATURITY_MODEL.md](docs/MATURITY_MODEL.md).

### 4 · No toques los gates humanos como cambio rutinario

Añadir, quitar o relajar una entrada de `approval_required` o de `denied` altera la frontera de autorización de todo lo que se instale. Exige revisión explícita.

### 5 · Finales de línea

`.gitattributes` normaliza a LF salvo los `.ps1`. El escritor de vistas fuerza `newline="\n"`. Si `sync --check` falla justo tras clonar en Windows: `git add --renormalize .`.

### 6 · Codificación en Windows

El catálogo lleva acentos y emoji. Sin `PYTHONUTF8=1` la consola de Windows lanza `UnicodeEncodeError`. CI lo define en los tres sistemas operativos.

## Antes de cerrar un cambio

```bash
make check
```

O paso a paso:

```bash
ruff check .
agentic-plugins sync --check
agentic-plugins validate
agentic-plugins eval --all
python -m unittest discover -s tests -v
```

Sin `make` ni CLI instalada:

```bash
python scripts/verify.py
```

## Coherencia de versión

La versión aparece en cuatro sitios y **todos deben coincidir**:

| Marcador | Archivo |
|---|---|
| `__version__` | `src/agentic_plugins/__init__.py` |
| `version` | `pyproject.toml` |
| `repository_version` | `catalog/plugins.yaml` |
| `version` de cada plugin | `catalog/plugins.yaml` |

`test_version_is_coherent_across_every_marker` lo verifica. El badge del README y los conteos de plugins, agentes y evaluaciones también están cubiertos por `test_readme_badges_match_the_catalog`: si cambias el catálogo, actualiza el README o la prueba te lo recuerda.

## Qué no hacer nunca

- No agregues secretos, tokens, rutas locales ni datos personales: el catálogo es público y hay una prueba.
- No elimines una prueba que respalda una garantía sin eliminar también la garantía de la documentación, en el mismo cambio.
- No presentes como implementado lo que está en el roadmap.
- No llames «portable» a un adaptador con menos capacidades: la tabla de [docs/PLATFORM_COMPATIBILITY.md](docs/PLATFORM_COMPATIBILITY.md) dice exactamente qué recibe cada plataforma.

---

<div align="center"><sub><a href="README.md">Repositorio</a> · <a href="CONTRIBUTING.md">Contribuir</a> · <a href="GOVERNANCE.md">Gobernanza</a></sub></div>
