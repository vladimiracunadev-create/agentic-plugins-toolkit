# 📖 Documentación

> Todo el proyecto es inspeccionable sin ejecutar nada y sin clave API. Esta carpeta explica cómo está construido y por qué toma las decisiones que toma.

[← Volver al repositorio](../README.md)

---

## Por dónde empezar

| Si quieres… | Lee |
|---|---|
| instalar y usar los plugins | [INSTALL.md](../INSTALL.md) y luego [CLI.md](CLI.md) |
| entender qué es un plugin aquí | [PLUGIN_CONTRACT.md](PLUGIN_CONTRACT.md) |
| saber cómo encaja todo | [ARCHITECTURE.md](ARCHITECTURE.md) |
| conocer los límites de seguridad | [SECURITY_MODEL.md](SECURITY_MODEL.md) |
| escribir un plugin nuevo | [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md) y [CONTRIBUTING.md](../CONTRIBUTING.md) |
| mantener el repositorio con un agente | [AGENTS.md](../AGENTS.md) |

## Referencia completa

### Fundamentos

| Documento | Contenido |
|---|---|
| [PLUGIN_CONTRACT.md](PLUGIN_CONTRACT.md) | qué campos declara un plugin, qué invariantes cumple y por qué |
| [ARCHITECTURE.md](ARCHITECTURE.md) | límites del sistema, componentes, fuente de verdad y flujo de generación |
| [MATURITY_MODEL.md](MATURITY_MODEL.md) | los cinco estados y qué evidencia exige cada promoción |

### Operación

| Documento | Contenido |
|---|---|
| [CLI.md](CLI.md) | los doce comandos, sus flags, salidas y códigos de retorno |
| [MCP.md](MCP.md) | las tres tools, el servidor de la CLI y el servidor distribuido |
| [HOOKS.md](HOOKS.md) | qué hace el único hook, qué no hace y por qué no hay más |
| [PLATFORM_COMPATIBILITY.md](PLATFORM_COMPATIBILITY.md) | qué recibe cada plataforma y con qué nivel de soporte |
| [WINDOWS.md](WINDOWS.md) | PowerShell, codificación, enlaces simbólicos y WSL |

### Garantías

| Documento | Contenido |
|---|---|
| [SECURITY_MODEL.md](SECURITY_MODEL.md) | amenazas, controles, permisos y gates humanos |
| [EVALUATION.md](EVALUATION.md) | qué demuestran las evaluaciones y qué explícitamente no |
| [SUPPLY_CHAIN.md](SUPPLY_CHAIN.md) | procedencia, reproducibilidad y dependencias opcionales |

### Extensión

| Documento | Contenido |
|---|---|
| [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md) | cómo se escribe un plugin nuevo, paso a paso |
| [ARD_DISCOVERY.md](ARD_DISCOVERY.md) | catálogo de descubrimiento experimental y qué no se certifica |
| [REFERENCES.md](REFERENCES.md) | especificaciones oficiales en las que se apoya el diseño |

---

## Tres ideas que atraviesan todo el proyecto

**Todo dato duplicado es una vista.** Un README de plugin, un manifiesto de plataforma, un `provenance.json` o un servidor MCP autocontenido repiten información que ya vive en `catalog/plugins.yaml`. Ninguno se escribe a mano: los sesenta y nueve se generan, y `sync --check` falla en CI si alguno difiere. La versión anterior mantenía seis de ellos a mano y los seis habían derivado.

**Acceso no es autorización.** Que un plugin pueda leer un repositorio no le permite publicar, desplegar, borrar ni rotar credenciales. Cada una de esas acciones tiene un gate humano explícito, declarado en el contrato y verificado por una evaluación.

**Los manifiestos son adaptadores.** No existe un formato universal de plugin agéntico. OpenAI y Claude Code comparten conceptos pero no un manifiesto idéntico, y Copilot y Gemini reciben proyecciones, no paquetes equivalentes. El proyecto lo declara en vez de fingir portabilidad total.

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="../CONTRIBUTING.md">Contribuir</a> · <a href="../CHANGELOG.md">Changelog</a></sub></div>
