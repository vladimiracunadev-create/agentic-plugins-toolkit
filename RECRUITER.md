# 💼 Lectura profesional del proyecto

> Qué demuestra este repositorio sobre ingeniería de sistemas agénticos, y qué deliberadamente no afirma.

[Repositorio](README.md) · [Arquitectura](docs/ARCHITECTURE.md) · [Sitio del proyecto](https://vladimiracunadev-create.github.io/agentic-plugins-toolkit/)

---

## Qué demuestra

| Competencia | Dónde se ve |
|---|---|
| Distinguir skill, agente, plugin y caso de negocio | la tabla del README y [`docs/PLUGIN_CONTRACT.md`](docs/PLUGIN_CONTRACT.md) |
| Diseño por contrato con una sola fuente de verdad | `catalog/plugins.yaml` y las 69 vistas que se generan de él |
| Detección y erradicación de drift real | la divergencia entre el servidor MCP distribuido y la CLI, documentada en [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md#por-qué-esto-no-es-burocracia) |
| Empaquetado reproducible | ZIP deterministas con SHA-256, comprobados construyendo dos veces en CI |
| Interoperabilidad honesta | cinco targets con nivel de soporte declarado, sin fingir un formato universal |
| Modelado de permisos y autorización | política de tres listas, gates humanos no delegables y evaluaciones que los prueban |
| Ingeniería de entrega | CI de siete jobs en nueve combinaciones, CodeQL, wheel con instalación limpia, Docker verificado en vivo y Pages |
| Prevención de drift documental | `sync --check` en CI y un validador que rechaza cualquier archivo no gobernado |
| Honestidad de estado | modelo de madurez de cinco niveles que hoy sitúa todo en `IMPLEMENTED` |

## La decisión de diseño que lo resume

El archivo `runtime/mcp_server.py` —el servidor MCP que viaja **dentro** de cada paquete y llega al host del usuario— se mantenía a mano y reimplementaba la comparación de políticas con `x in action.lower()`. La CLI usaba una comparación que normaliza mayúsculas y separadores.

Consecuencia concreta: para la acción `BYPASS_APPROVAL`, la CLI respondía `denied` y el paquete distribuido respondía `allowed`.

La corrección no fue arreglar el archivo, sino **eliminar la categoría de archivo que podía estar mal**: hoy el servidor se genera copiando el código fuente literal de `policy.py`, el validador rechaza cualquier archivo de un paquete que no sea una vista generada o el `cases.jsonl`, y una prueba levanta ambos servidores como subproceso y compara sus respuestas acción por acción.

Eso convierte una promesa habitual —«el paquete hace lo que el contrato dice»— en una propiedad que el sistema garantiza.

## Lo que este proyecto NO afirma

Esto es parte del trabajo, no una carencia que ocultar:

- **No afirma uso productivo.** Los seis plugins declaran `IMPLEMENTED`: paquete completo y validado. Ninguno ha registrado todavía una misión real con evidencia.
- **No afirma equivalencia entre plataformas.** Copilot y Gemini reciben adaptadores con menos capacidades, y la tabla lo dice explícitamente.
- **No afirma conformidad con ARD**, una especificación que sigue evolucionando.
- **No afirma paquetes firmados.** Hay reproducibilidad y SHA-256; la firma criptográfica y el SBOM están en el roadmap como pendientes.

El mecanismo para incorporar evidencia real sin exagerar está construido y vacío a propósito: [`evidence/README.md`](evidence/README.md) y [`docs/MATURITY_MODEL.md`](docs/MATURITY_MODEL.md).

## Por dónde mirar en cinco minutos

1. **[`catalog/plugins.yaml`](catalog/plugins.yaml)** — el contrato canónico de los seis plugins.
2. **[`src/agentic_plugins/render.py`](src/agentic_plugins/render.py)** — las 69 vistas, y la función que copia el código fuente de la política al servidor distribuido.
3. **[`docs/SECURITY_MODEL.md`](docs/SECURITY_MODEL.md)** — quince amenazas, cada una con el nombre de la prueba que la cubre.
4. **[`tests/test_toolkit.py`](tests/test_toolkit.py)** — las 55 pruebas que convierten esas garantías en propiedades verificadas.

```bash
git clone https://github.com/vladimiracunadev-create/agentic-plugins-toolkit.git
cd agentic-plugins-toolkit && python -m pip install -e .
agentic-plugins doctor && agentic-plugins validate && agentic-plugins eval --all
```

Todo corre offline, sin clave API y sin costo.

---

<div align="center"><sub><a href="README.md">Repositorio</a> · <a href="docs/README.md">Documentación</a> · <a href="ROADMAP.md">Roadmap</a></sub></div>
