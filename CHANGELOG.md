# 📋 Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y [versionado semántico](https://semver.org/lang/es/).

El repositorio y los plugins comparten versión: un cambio del contrato de plugin afecta a todo lo que se distribuye.

---

## [0.2.0] — 2026-08-17

Versión de **coherencia verificable**. La 0.1.0 afirmaba que `catalog/plugins.yaml` controlaba los contratos; en realidad seis archivos por plugin se mantenían a mano y los seis habían derivado. Esta versión no arregla esos archivos: elimina la categoría de archivo que podía estar mal.

### Corregido

- **El servidor MCP distribuido clasificaba las políticas de forma distinta a la CLI.** `plugins/*/runtime/mcp_server.py` se mantenía a mano y comparaba con `x in action.lower()`, mientras `policy.py` normaliza mayúsculas y trata `_` y `-` como equivalentes. Para la acción `BYPASS_APPROVAL` la CLI respondía `denied` y el archivo que efectivamente viaja dentro del paquete respondía `allowed`. Hoy ese servidor es una vista generada que **copia el código fuente literal** de `policy._matches` y `policy.classify_action`, y `test_distributed_server_agrees_with_the_cli` levanta ambos servidores como subproceso y compara sus respuestas acción por acción.
- **Los hooks invocaban `python3`**, un binario que no existe en una instalación estándar de Windows: el hook moría en silencio justo en una de las tres plataformas declaradas como soportadas. Ahora invocan el console script `agentic-plugins-hook`, que el job `test` de CI ejecuta de verdad en Windows.
- **La landing habría quedado vacía en GitHub Pages.** `site/app.js` leía `/api/plugins`, un endpoint que solo existe con el panel local levantado, y `index.html` referenciaba `/styles.css` y `/app.js` con rutas absolutas que rompen en un Pages de proyecto. Ahora hay una vista estática `site/catalog.json`, la API local se usa como fuente preferente cuando existe, y todas las rutas son relativas.
- **Las pruebas no se podían ejecutar sin instalar el paquete.** `python -m unittest discover -s tests` fallaba con `ModuleNotFoundError` en un clon limpio; ahora el módulo de pruebas hace bootstrap de `sys.path`.
- **`catalog/ai-catalog.json` se mantenía a mano** y sus URNs conservaban la versión anterior tras cada bump. Es una vista generada.
- **El validador podía lanzar `IndexError`** ante un plugin sin skills declarados, en vez de reportar el problema.

### Añadido

- **Nueve vistas generadas más por plugin**: `README.md`, `provenance.json`, `assets/icon.svg`, `runtime/mcp_server.py` y los tres adaptadores de OpenAI, Claude Code y Gemini, además de `catalog/ai-catalog.json` y `site/catalog.json`. Total: **69 archivos** derivados del catálogo.
- **`test_every_duplicated_file_is_generated` y la comprobación equivalente en el validador**: todo archivo dentro de un paquete es una vista generada o `evals/cases.jsonl`. No hay una tercera categoría, y `AUTHORED_FILES` declara la única excepción en una constante visible en el diff.
- **Guardia de loopback en el panel.** `serve` se niega a enlazar fuera de loopback salvo `AGENTIC_PLUGINS_ALLOW_REMOTE_BIND=1`. El `Dockerfile` lo declara porque dentro de un contenedor `0.0.0.0` es la única dirección alcanzable, y `compose.yaml` publica el puerto solo en el loopback del host.
- **Endpoint `/healthz`** en el panel, y `HEALTHCHECK` en la imagen.
- **`mcp_protocol_version` y `execution_plan_steps` en el catálogo**: la versión de protocolo y los pasos del plan dejan de estar duplicados entre la CLI y los seis servidores distribuidos.
- **Console script `agentic-plugins-hook`** y bandera `--version` en la CLI.
- **`doctor` ampliado**: versión, intérprete, ejecutables, raíz, conteos y resultado de la validación.
- **`eval` explica los fallos**: identificador, línea del `cases.jsonl`, esperado y obtenido.
- **Validaciones nuevas**: agentes que deben existir en la instantánea, políticas no vacías, aprobación humana no delegable, `status` coherente con `maturity.declared`, evaluaciones con identificadores únicos y campos completos.
- **21 pruebas nuevas** (34 → **55**), organizadas por familia: catálogo, vistas generadas, política, evaluación, MCP, seguridad, empaquetado, formato y CLI. Incluyen coherencia de versión entre marcadores y resolución de los enlaces a `docs/` del README.
- **Workflow `codeql.yml`** y **workflow `pages.yml`**, ambos con acciones fijadas por SHA.
- **Job `packages` en CI**: empaqueta dos veces en directorios distintos y hace `diff` de los `checksums.json`. Si el empaquetado dejara de ser determinista, la build cae.
- **`.github/`** completo: plantillas de issue de bug y de propuesta de plugin, `config.yml`, plantilla de PR y Dependabot para pip, GitHub Actions y Docker.
- **Documentación completa** según el estándar de los repositorios relacionados: `docs/README.md` como índice, `docs/CLI.md` nuevo, y los once documentos temáticos existentes reescritos con tablas de garantías, diagramas y límites declarados. `INSTALL.md`, `CONTRIBUTING.md`, `SECURITY.md`, `GOVERNANCE.md`, `SUPPORT.md`, `CODE_OF_CONDUCT.md`, `ROADMAP.md` y `RECRUITER.md` pasan de nota breve a documento operativo.
- **`.gitattributes`** que normaliza a LF salvo los `.ps1`, para que `sync` en Windows no produzca drift en Linux.

### Cambiado

- **CI pasa de un job a siete**: `lint` con ruff, `contracts`, `test` en nueve combinaciones (Linux, macOS y Windows × Python 3.11, 3.12 y 3.13), `packages`, `build` con instalación del wheel en entorno limpio, `docker` con healthcheck en vivo y `ci` como check agregado para proteger la rama. Todas las acciones fijadas por SHA de commit, con `concurrency` y `workflow_dispatch`.
- **`Makefile` con `help` autodocumentado** y objetivo `check` que ejecuta exactamente lo mismo que CI.
- **Configuración de `ruff`** en `pyproject.toml`, con las mismas reglas que el resto de los repositorios.
- **`scripts/verify.py`** informa qué paso falló en vez de salir en silencio.
- **`packager` excluye `__pycache__` y `.DS_Store`** de forma explícita y el ZIP normaliza separadores a `/`, de modo que un paquete construido en Windows y otro en Linux tienen el mismo SHA-256.
- **El mensaje del hook** enumera también las acciones denegadas, no solo las que exigen aprobación.
- **`SKILL.md` generado** incluye la sección de acciones denegadas.
- **Metadatos del paquete**: `project.urls`, `keywords`, clasificadores de Python 3.13 y extra `dev`.

### Seguridad

- La semántica de política tiene ahora una **única implementación**; los seis servidores distribuidos la copian y una prueba verifica la equivalencia.
- El panel exige opt-in explícito para salir de loopback.
- El contenedor descarta todas las capacidades y no permite escalada de privilegios.
- Dependabot vigila pip, GitHub Actions y Docker; CodeQL analiza en cada push y cada lunes.

---

## [0.1.0] — 2026-08-15

### Añadido

- Entrega inicial con seis plugins, diez agentes por instantánea versionada, veinticuatro evaluaciones deterministas, servidor MCP, adaptadores para cinco plataformas y control center local.
- Empaquetado reproducible con `checksums.json` y exportador que preserva directorios no administrados.
- Catálogo ARD experimental declarado como `ARD_READY_NOT_CONFORMANCE_CLAIM`.

[0.2.0]: https://github.com/vladimiracunadev-create/agentic-plugins-toolkit/releases/tag/v0.2.0
[0.1.0]: https://github.com/vladimiracunadev-create/agentic-plugins-toolkit/releases/tag/v0.1.0
