# 📎 Referencias

> Las especificaciones oficiales en las que se apoya el diseño, y qué se tomó de cada una.

[Repositorio](../README.md) · [Documentación](README.md) · [Compatibilidad](PLATFORM_COMPATIBILITY.md)

---

## Formatos de plugin

| Fuente | Qué se tomó |
|---|---|
| [OpenAI — build plugins](https://developers.openai.com/plugins/build/plugins) | estructura de `.codex-plugin/plugin.json`, bloque `interface`, `defaultPrompt` y rutas relativas |
| [OpenAI — plugins](https://developers.openai.com/plugins) | modelo de marketplace y política de instalación |
| [Claude Code — plugins reference](https://code.claude.com/docs/en/plugins-reference) | estructura de `.claude-plugin/plugin.json`, descubrimiento de `agents/`, `skills/`, hooks y MCP |
| [Claude Code — plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) | formato de `.claude-plugin/marketplace.json` |

## Skills y agentes

| Fuente | Qué se tomó |
|---|---|
| [Agent Skills — specification](https://agentskills.io/specification) | frontmatter de `SKILL.md`: `name`, `description`, `license`, `compatibility`, `metadata` |
| [Claude Code — subagents](https://code.claude.com/docs/en/sub-agents) | frontmatter de los agentes: `name`, `description`, `tools`, `model: inherit` |

## Protocolo

| Fuente | Qué se tomó |
|---|---|
| [Model Context Protocol](https://modelcontextprotocol.io/) | JSON-RPC por stdio, `initialize`, `tools/list`, `tools/call`, `structuredContent` |
| [MCP — architecture](https://modelcontextprotocol.io/docs/learn/architecture) | separación entre lo que describe el servidor y lo que ejecuta el host |

## Interoperabilidad y descubrimiento

| Fuente | Qué se tomó |
|---|---|
| [A2A Protocol](https://a2a-protocol.org/latest/specification/) | vocabulario de capacidades entre agentes — **no implementado**, está en el roadmap |
| [ARD — agentic resource discovery](https://github.com/ards-project/ard-spec) | idea de catálogo de descubrimiento; ver [ARD_DISCOVERY.md](ARD_DISCOVERY.md) para la declaración explícita de no-conformidad |

## Seguridad

| Fuente | Qué se tomó |
|---|---|
| [OWASP — Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/) | taxonomía de amenazas: goal hijacking, abuso de tools, supply chain, expansión de alcance |
| [OWASP — Top 10 para aplicaciones agénticas](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | priorización de controles en [SECURITY_MODEL.md](SECURITY_MODEL.md) |

## Observabilidad

| Fuente | Qué se tomó |
|---|---|
| [OpenTelemetry — atributos GenAI](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) | vocabulario previsto para el sink de evidencia — **no implementado**, está en el roadmap |

## Convenciones del repositorio

| Fuente | Qué se tomó |
|---|---|
| [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) | formato del [CHANGELOG](../CHANGELOG.md) |
| [Versionado semántico](https://semver.org/lang/es/) | criterio de versión del repositorio y de cada plugin |

> [!NOTE]
> A2A, ARD y OpenTelemetry aparecen aquí como **influencias declaradas**, no como integraciones existentes. Lo que hoy está implementado es MCP por stdio y los dos manifiestos nativos; lo demás está en el [roadmap](../ROADMAP.md) y se presenta como pendiente.

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="PLATFORM_COMPATIBILITY.md">Compatibilidad</a> · <a href="ARD_DISCOVERY.md">Descubrimiento</a></sub></div>
