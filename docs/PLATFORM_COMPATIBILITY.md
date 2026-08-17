# 🌍 Compatibilidad de plataformas

> Qué recibe cada plataforma, con qué nivel de soporte y por qué el proyecto se niega a llamarlo «formato universal».

[Repositorio](../README.md) · [Documentación](README.md) · [Contrato de plugin](PLUGIN_CONTRACT.md)

---

## No existe un formato universal de plugin agéntico

OpenAI y Claude Code comparten conceptos —manifiesto, skills, hooks, MCP— pero **no un manifiesto idéntico**. Copilot consume perfiles de agente. Gemini no instala paquetes. Un host MCP genérico solo habla el protocolo.

Por eso `plugin.yaml` es canónico y cada plataforma recibe una **proyección**. El nivel de soporte forma parte del contrato, no de una nota al pie:

| Target | Entrega | `support` | Nivel real |
|---|---|---|---|
| OpenAI / Codex | `.codex-plugin/plugin.json`, `skills/`, `hooks/`, `.mcp.json` | `native-package` | paquete nativo |
| Claude Code | `.claude-plugin/plugin.json`, `agents/`, `skills/`, `hooks/`, `.mcp.json` | `native-package` | paquete nativo |
| GitHub Copilot | `adapters/github-copilot/*.agent.md` | `generated-agent-profiles` | **adaptador** |
| Gemini | `adapters/gemini/GEMINI.md` + MCP | `generated-instructions` | **adaptador** |
| Host MCP genérico | `runtime/mcp_server.py` por stdio | `stdio` | protocolo |

## Qué significa cada nivel

**`native-package`** — el host descubre el paquete por su manifiesto y monta agentes, skills, hooks y servidores MCP sin traducción. Es lo más parecido a «instalar».

**`generated-agent-profiles`** — Copilot recibe los mismos agentes que Claude Code, en el formato `.agent.md` que entiende. Los archivos son **idénticos** en contenido: el renderer produce uno solo y lo escribe en las dos rutas. Lo que Copilot no recibe es el hook ni el registro automático del MCP.

**`generated-instructions`** — Gemini recibe un documento portable con la misión, cómo usar el skill, qué agente elegir y los límites duros. Es una adaptación honesta: el host no instala nada, **lee**. Los gates humanos siguen declarados, pero quien los aplica es la persona, no el runtime.

**`stdio`** — cualquier host que hable MCP puede conectar el servidor autocontenido sin instalar el paquete Python. Es el mínimo común denominador y el más portable de todos.

## Lo que es igual en todas partes

Independientemente de la plataforma, todo paquete lleva:

- la misma misión y la misma composición de agentes;
- la misma política: permitido, con gate humano y denegado siempre;
- la misma procedencia en `provenance.json`;
- el mismo servidor MCP, con la misma semántica de política verificada por prueba.

## Lo que cambia

| | OpenAI | Claude Code | Copilot | Gemini | MCP genérico |
|---|:-:|:-:|:-:|:-:|:-:|
| Manifiesto nativo | ✅ | ✅ | ❌ | ❌ | ❌ |
| Agentes | ✅ | ✅ | ✅ | ✅ lectura | ❌ |
| Skill del workflow | ✅ | ✅ | ❌ | ✅ lectura | ❌ |
| Hook `SessionStart` | ✅ | ✅ | ❌ | ❌ | ❌ |
| Servidor MCP | ✅ | ✅ | ❌ | ✅ | ✅ |
| Aplicación automática de la política | del host | del host | ❌ | ❌ manual | ❌ |

> [!IMPORTANT]
> La última fila es la importante. En Copilot y Gemini la política se **declara** pero no la aplica un runtime: es responsabilidad de quien opera. El proyecto lo dice aquí en vez de dejar que se asuma.

## Probar la instalación

```bash
agentic-plugins export repository-engineering --target ~/.claude/plugins
agentic-plugins export repository-engineering --target /ruta/a/tu/host
```

El exportador escribe una marca `.agentic-plugins-managed.json` y se niega a sobrescribir un directorio que no la lleve.

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="../INSTALL.md">Instalación</a> · <a href="MCP.md">MCP</a></sub></div>
