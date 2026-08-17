# 🔐 Modelo de seguridad

> Qué amenazas se consideran, qué control cubre cada una, qué prueba respalda ese control y qué límites se declaran en vez de ocultarse.

[Repositorio](../README.md) · [Documentación](README.md) · [Política de reporte](../SECURITY.md)

---

## Superficie

Un plugin agéntico es un vector poco habitual: se instala en un host que ya tiene permisos sobre el equipo del usuario, y lo que trae dentro —instrucciones, políticas, hooks, un servidor MCP— **influye en el comportamiento del modelo**. No hay sandbox que lo contenga si el propio paquete miente sobre sus límites.

Por eso el objetivo de este modelo no es «que el código no tenga bugs», sino que **lo que el paquete declara sea lo que el paquete hace**.

## Amenazas y controles

| # | Amenaza | Control | Prueba |
|:-:|---|---|---|
| 1 | **Divergencia entre lo declarado y lo distribuido** — el manifiesto dice una cosa y el archivo que llega al host hace otra | todo archivo del paquete se genera desde el catálogo; el servidor MCP distribuido copia el código fuente literal de la política | `test_distributed_server_agrees_with_the_cli` · `test_every_duplicated_file_is_generated` |
| 2 | **Evasión de política por normalización** — `BYPASS_APPROVAL` no coincide con `bypass-approval` y pasa como permitida | comparación que hace casefold y trata `_` y `-` como equivalentes, en una única implementación | `test_denial_survives_case_and_separator_changes` |
| 3 | **Expansión silenciosa de alcance** — el plugin acaba haciendo más de lo que se autorizó | `default: allow-read-plan`; publicar, desplegar, borrar, credenciales y servicios de pago tienen gate humano declarado | `test_every_plugin_declares_human_gates` |
| 4 | **Delegación de la aprobación** — un agente aprueba en lugar del usuario | `human_approval_cannot_be_delegated` es obligatorio y el validador lo exige | `test_every_plugin_declares_human_gates` |
| 5 | **Goal hijacking por routing** — una frase manipulada desactiva el gate | una palabra negativa no cancela una acción sujeta a aprobación | `test_a_negative_word_does_not_cancel_a_human_gate` |
| 6 | **Supply chain del paquete** — no se sabe de dónde vino cada pieza | `provenance.json` generado por plugin, instantánea versionada de agentes, skills externos declarados como opcionales | `test_no_drift` |
| 7 | **Paquete alterado en tránsito** | ZIP deterministas y `checksums.json` con SHA-256; CI empaqueta dos veces y compara | `test_packages_are_reproducible` |
| 8 | **Exposición de secretos** | búsqueda de patrones de clave privada y token en todo archivo del paquete | `validate` · `test_no_dangerous_command_is_shipped` |
| 9 | **Comandos destructivos embebidos** | rechazo de `rm -rf /`, `git reset --hard` y banderas que omiten permisos | `validate` · `test_no_dangerous_command_is_shipped` |
| 10 | **Instalación destructiva** — el exportador pisa un plugin del usuario | marca `.agentic-plugins-managed.json`; sin ella, la operación falla | `test_export_preserves_an_unmanaged_directory` |
| 11 | **Desinstalación destructiva** | `uninstall` se niega sobre un directorio sin marca | `test_uninstall_refuses_an_unmanaged_directory` |
| 12 | **Panel expuesto a la red** | `serve` solo enlaza loopback; salir exige `AGENTIC_PLUGINS_ALLOW_REMOTE_BIND=1` | `test_panel_refuses_a_non_loopback_bind_without_optin` |
| 13 | **Hook que falla o no existe en la plataforma** | ejecutable propio en vez de `python3`; si el catálogo no se encuentra devuelve `continue: true` | `test_hooks_do_not_depend_on_a_python3_binary` |
| 14 | **Path traversal en manifiestos** | las rutas deben empezar por `./` y no contener `..` | `validate` |
| 15 | **Afirmación de madurez no respaldada** | `status` acotado, `not_claimed` explícito, promoción manual | `test_status_is_honest` |

## Lo que el servidor MCP **no** puede hacer

Las tres tools son `plugin_info`, `create_execution_plan` y `policy_check`. Ninguna:

- escribe archivos;
- abre conexiones de red;
- ejecuta comandos;
- invoca un modelo.

`create_execution_plan` devuelve una lista de pasos, no los ejecuta. Las acciones reales viven en las tools del host y quedan sujetas a sus permisos, que el usuario ya conoce.

## Permisos por defecto

| Situación | Comportamiento |
|---|---|
| Leer el repositorio, inventariar, planificar | permitido |
| Escribir archivos | dentro del alcance autorizado por el host |
| Publicar, empujar, liberar, borrar, desplegar | **gate humano** |
| Credenciales o servicios de pago | **gate humano** |
| Omitir una aprobación, exfiltrar un secreto | **denegado siempre** |

## Límites conocidos

Se declaran porque omitirlos sería exactamente la clase de afirmación que este proyecto existe para evitar.

- **El panel local no tiene autenticación.** Es para loopback. El opt-in existe para contenedores, no para exponerlo.
- **La detección de secretos es heurística.** Cubre patrones frecuentes (`sk-…`, `ghp_…`, claves privadas PEM). No sustituye una revisión humana ni un scanner dedicado antes de publicar.
- **La política es comparación de subcadenas normalizadas, no semántica.** Un sinónimo que el contrato no enumere no se detecta: `«sube esto a producción»` coincide por `deploy` solo si esa palabra aparece. Por eso el gate del host sigue siendo la última línea, no la única.
- **El aislamiento es del host, no del toolkit.** El paquete declara límites; quien los aplica en tiempo de ejecución es el runtime.
- **La instantánea de agentes es una foto.** Refleja `operational-ai-agents` en la versión declarada, no su estado actual. Actualizarla es un acto explícito y versionado.
- **Reproducible no es firmado.** Los ZIP tienen SHA-256 verificable, pero todavía no hay firma criptográfica ni SBOM: está en el roadmap y no se presenta como hecho.

## Dependencias

El paquete **no declara dependencias de runtime**. Las acciones de GitHub están fijadas por SHA de commit, Dependabot revisa mensualmente pip, GitHub Actions y Docker, y CodeQL analiza el código en cada push y cada lunes.

## Reporte

Vulnerabilidades por el canal privado, nunca en un issue público: ver **[SECURITY.md](../SECURITY.md)**.

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="../SECURITY.md">Política de seguridad</a> · <a href="SUPPLY_CHAIN.md">Cadena de suministro</a></sub></div>
