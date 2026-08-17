# 📦 Instalación

> Instalar, exportar a un host, actualizar y desinstalar. Nada de esto necesita clave API: validar contratos, evaluar, empaquetar, servir MCP y usar el panel funcionan offline.

[Repositorio](README.md) · [Referencia de CLI](docs/CLI.md) · [Compatibilidad](docs/PLATFORM_COMPATIBILITY.md)

---

## Requisitos

| Requisito | Para qué | ¿Obligatorio? |
|---|---|:-:|
| Python 3.11+ | CLI, validación, evaluaciones, MCP y panel | ✅ |
| Git | clonar y actualizar | ✅ |
| Un host agéntico | ejecutar los plugins de verdad | ❌ solo para ejecución real |
| Docker | levantar el panel en contenedor | ❌ opcional |
| `make` | atajo de los gates locales | ❌ hay alternativa |

No hay dependencias de runtime: la CLI usa únicamente la biblioteca estándar.

## 1 · CLI local

```bash
git clone https://github.com/vladimiracunadev-create/agentic-plugins-toolkit.git
cd agentic-plugins-toolkit
python -m pip install -e .
agentic-plugins doctor
agentic-plugins list
```

Si `agentic-plugins` no aparece en el PATH, el equivalente siempre funciona:

```bash
python -m agentic_plugins list
```

O con el script, que además valida:

```bash
./scripts/install.sh        # Linux, macOS, Git Bash
```

```powershell
.\scripts\install.ps1       # Windows PowerShell
```

## 2 · Instalar un plugin en un host

```bash
agentic-plugins export repository-engineering --target ~/.claude/plugins
```

> [!IMPORTANT]
> El exportador escribe una marca `.agentic-plugins-managed.json` y **nunca sobrescribe un directorio que no la lleve**. Si ya tienes un plugin con el mismo nombre, la operación falla y tus archivos quedan intactos. `--force` es la única forma de sobrescribir, y es una decisión explícita.

### Qué recibe cada plataforma

| Plataforma | Ruta habitual | Qué monta |
|---|---|---|
| Claude Code | `~/.claude/plugins/<id>` | manifiesto, agentes, skill, hooks y MCP |
| OpenAI / Codex | el directorio de plugins del host | manifiesto, skill, hooks y MCP |
| GitHub Copilot | `.github/` del proyecto | perfiles `adapters/github-copilot/*.agent.md` |
| Gemini | donde lo cargues | `adapters/gemini/GEMINI.md` |
| Host MCP genérico | ninguna instalación | `runtime/mcp_server.py` por stdio |

Detalle y niveles de soporte en [docs/PLATFORM_COMPATIBILITY.md](docs/PLATFORM_COMPATIBILITY.md).

### Marketplaces locales

Los dos archivos de marketplace están en el repositorio:

- `.claude-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`

Ambos son **vistas generadas** del catálogo. El toolkit no publica ni registra plugins automáticamente en ningún servicio.

> [!CAUTION]
> Revisa `hooks/hooks.json` de cada plugin **antes** de habilitarlo. Un hook es código que tu host ejecuta por ti. El de este repositorio solo imprime los límites del plugin —son doce líneas en [`src/agentic_plugins/hooks.py`](src/agentic_plugins/hooks.py)— pero esa comprobación es tuya.

## 3 · Comprobar que funciona

```bash
agentic-plugins doctor
agentic-plugins policy-check repository-engineering --action "publicar el release"
```

Y el servidor MCP, sin instalar nada:

```bash
python plugins/repository-engineering/runtime/mcp_server.py
```

## 4 · Panel local (opcional)

```bash
agentic-plugins serve --host 127.0.0.1 --port 8787
```

O en contenedor:

```bash
docker compose up --build
```

> [!CAUTION]
> El panel **no implementa autenticación**. Escucha en loopback por defecto y salir de ahí exige declarar `AGENTIC_PLUGINS_ALLOW_REMOTE_BIND=1`. No lo expongas a Internet.

## Actualizar

```bash
git pull
python -m pip install -e .
agentic-plugins sync
agentic-plugins export <plugin-id> --target <ruta> --force
```

`sync` regenera las vistas derivadas del catálogo; el `export` con `--force` refresca una instalación que ya administras.

## Desinstalar

```bash
agentic-plugins uninstall repository-engineering --target ~/.claude/plugins
```

Solo se elimina lo que lleva la marca `.agentic-plugins-managed.json`. Un directorio ajeno hace fallar la operación en vez de borrarse. Para quitar la CLI:

```bash
python -m pip uninstall agentic-plugins-toolkit
```

## Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `agentic-plugins: command not found` | el directorio de scripts no está en el PATH | usa `python -m agentic_plugins` o añade el directorio |
| `No se encontró catalog/plugins.yaml` | estás fuera del repositorio | `cd` al repositorio, usa `--root` o define `AGENTIC_PLUGINS_ROOT` |
| `AGENTIC_PLUGINS_ROOT inválido` | la variable apunta a un directorio sin catálogo | corrígela o quítala; la CLI falla a propósito en vez de adivinar |
| `Conflicto no administrado` | ya existe un plugin tuyo con ese nombre | renómbralo, elige otro `--target` o usa `--force` a sabiendas |
| `No se eliminará un directorio no administrado` | `uninstall` sobre algo que no instaló el toolkit | bórralo tú, con conocimiento de causa |
| `El panel no tiene autenticación: use loopback…` | intentaste enlazar fuera de loopback | declara la variable de opt-in solo si sabes lo que haces |
| Acentos rotos en la salida de Windows | consola en cp1252 | `$env:PYTHONUTF8 = "1"` · ver [docs/WINDOWS.md](docs/WINDOWS.md) |
| `sync --check` falla justo tras clonar | finales de línea | `git add --renormalize .` |

Más diagnóstico en [SUPPORT.md](SUPPORT.md).

---

<div align="center"><sub><a href="README.md">Repositorio</a> · <a href="docs/CLI.md">CLI</a> · <a href="SUPPORT.md">Soporte</a></sub></div>
