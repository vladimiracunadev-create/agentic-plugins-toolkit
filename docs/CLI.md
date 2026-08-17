# 🛠 Referencia de CLI

> Los doce comandos de `agentic-plugins`: qué hacen, qué imprimen y con qué código salen. Todo corre offline, sin clave API y sin costo.

[Repositorio](../README.md) · [Documentación](README.md) · [Instalación](../INSTALL.md)

---

## Invocación

```bash
agentic-plugins [--root RUTA] [--version] <comando> [opciones]
```

Si el ejecutable no está en el PATH, el equivalente siempre funciona:

```bash
python -m agentic_plugins <comando>
```

### Opciones globales

| Opción | Efecto |
|---|---|
| `--root RUTA` | opera sobre otro repositorio en vez de descubrirlo desde el directorio actual |
| `--version` | imprime la versión del paquete y sale |

### Cómo se descubre la raíz

1. La variable de entorno `AGENTIC_PLUGINS_ROOT`, si está definida. Si apunta a un directorio sin `catalog/plugins.yaml`, la CLI **falla** en vez de buscar en otro sitio.
2. `--root`, si se pasa.
3. El primer ancestro del directorio actual que contenga `catalog/plugins.yaml`.
4. El primer ancestro del propio paquete instalado.

### Códigos de retorno

| Código | Significado |
|:-:|---|
| `0` | éxito |
| `1` | el comando funcionó pero el resultado es negativo: hay drift, hay errores de validación o falló alguna evaluación |
| `2` | error de uso o de entorno: plugin desconocido, catálogo inválido, ruta ilegible |
| `130` | interrumpido con Ctrl-C |

La distinción entre `1` y `2` importa en CI: `1` es «el repositorio está mal», `2` es «me invocaste mal».

---

## Inspección

### `list`

Lista el catálogo.

```bash
agentic-plugins list
agentic-plugins list --json
```

```text
repository-engineering       IMPLEMENTED  high   Repository Engineering
legacy-modernization         IMPLEMENTED  high   Legacy Modernization
learning-program-studio      IMPLEMENTED  medium Learning Program Studio
product-evolution            IMPLEMENTED  medium Product Evolution
portfolio-governance         IMPLEMENTED  low    Portfolio Governance
rootcause-response           IMPLEMENTED  high   RootCause Response
```

### `inspect <plugin_id>`

Misión, agentes, acciones con gate humano y acciones denegadas.

```bash
agentic-plugins inspect rootcause-response
agentic-plugins inspect rootcause-response --json    # el contrato completo
```

Sale con `2` si el identificador no existe.

### `doctor`

Diagnóstico del entorno y del catálogo. Útil como primer adjunto de cualquier reporte.

```bash
agentic-plugins doctor
```

```text
agentic-plugins       0.2.0
Python                3.12.9 (OK)
Ejecutable            /usr/local/bin/agentic-plugins
Hook                  /usr/local/bin/agentic-plugins-hook
Raíz                  /home/tu/agentic-plugins-toolkit
Catálogo              6 plugins · 10 agentes
Validación            OK
```

Sale con `1` si la versión de Python no alcanza o si la validación encuentra errores.

---

## Integridad

### `validate`

Comprueba tres familias de propiedades:

- **Contrato** — campos obligatorios, `id` en kebab-case, versión SemVer, agentes presentes en la instantánea, al menos cuatro evaluaciones, gates humanos declarados y `status` coherente con `maturity.declared`.
- **Higiene** — ni secretos ni comandos peligrosos dentro de los paquetes; rutas de manifiesto sin escapes hacia arriba.
- **Ausencia de duplicación no gobernada** — todo archivo del paquete es una vista generada o `evals/cases.jsonl`.

```bash
agentic-plugins validate
agentic-plugins validate --json
```

Sale con `1` si hay algún hallazgo de nivel `error`. Los de nivel `warning` (por ejemplo un directorio en `plugins/` que el catálogo no lista) se informan sin romper la build.

### `sync` / `sync --check`

`sync` regenera las **69 vistas derivadas** del catálogo. `sync --check` no escribe nada y sale con `1` si alguna difiere.

```bash
agentic-plugins sync            # regenera y lista lo que cambió
agentic-plugins sync --check    # lo que ejecuta CI
```

> [!IMPORTANT]
> Si editaste a mano un `README.md` de plugin, un manifiesto o un `runtime/mcp_server.py`, `sync` **descarta** tu edición. El cambio va en `catalog/plugins.yaml` o en `src/agentic_plugins/render.py`.

### `eval`

Evaluaciones deterministas de routing y aprobación. No consumen API.

```bash
agentic-plugins eval --all
agentic-plugins eval repository-engineering
agentic-plugins eval --all --json
```

```text
repository-engineering: 4/4
legacy-modernization: 4/4
...
TOTAL: 24/24
```

Cuando un caso falla, imprime el identificador, la línea del `cases.jsonl`, lo esperado y lo obtenido. Sale con `1` si algún caso falla y con `2` si no se indicó ni `plugin_id` ni `--all`.

---

## Distribución

### `package`

Construye ZIP **reproducibles** y escribe `checksums.json`.

```bash
agentic-plugins package --all --output dist
agentic-plugins package rootcause-response --output /tmp/salida
```

```text
repository-engineering-0.2.0.zip  sha256:…
```

Los archivos se ordenan alfabéticamente, la marca temporal se fija en `1980-01-01` y los permisos en `0644`, de modo que el mismo contenido produce el mismo digest en cualquier máquina. CI lo comprueba empaquetando dos veces y comparando los `checksums.json`.

### `export`

Instala un plugin en un directorio destino.

```bash
agentic-plugins export repository-engineering --target ~/.claude/plugins
agentic-plugins export repository-engineering --target ~/.claude/plugins --force
```

Escribe una marca `.agentic-plugins-managed.json` en el destino. Si el directorio ya existe **sin** esa marca, la operación falla con `2` y tus archivos quedan intactos; `--force` es la única forma de sobrescribir, y es una decisión explícita.

### `uninstall`

```bash
agentic-plugins uninstall repository-engineering --target ~/.claude/plugins
```

Elimina **solo** lo que lleva la marca. Sobre un directorio ajeno falla en vez de borrar.

---

## Ejecución

### `policy-check`

Clasifica una acción contra la política del plugin. Es la forma barata de saber dónde se detendría antes de instalarlo.

```bash
agentic-plugins policy-check repository-engineering --action "publicar el release"
```

```json
{
  "action": "publicar el release",
  "decision": "approval-required",
  "matched": "release"
}
```

`decision` es `allowed`, `approval-required` o `denied`. La comparación normaliza mayúsculas y trata `_` y `-` como equivalentes, de modo que `BYPASS_APPROVAL`, `bypass approval` y `Bypass-Approval` son la misma acción denegada.

### `mcp`

Servidor MCP por stdio. No escribe archivos, no abre red y no invoca modelos.

```bash
agentic-plugins mcp --plugin repository-engineering
```

Detalle de las tres tools en [MCP.md](MCP.md).

### `serve`

Panel local de inspección del catálogo.

```bash
agentic-plugins serve --host 127.0.0.1 --port 8787
```

| Ruta | Contenido |
|---|---|
| `/` | la landing, servida desde `site/` |
| `/api/plugins` | el catálogo completo en JSON |
| `/healthz` | `{"status":"ok"}` para healthchecks |

> [!CAUTION]
> El panel **no implementa autenticación**. `serve` se niega a enlazar fuera de loopback y sale con `2`, salvo que declares `AGENTIC_PLUGINS_ALLOW_REMOTE_BIND=1`. El `Dockerfile` lo declara porque dentro de un contenedor `0.0.0.0` es la única dirección alcanzable, y `compose.yaml` publica el puerto solo en el loopback del host.

---

## El hook

`agentic-plugins-hook` es un ejecutable aparte, el que invocan los `hooks/hooks.json` de cada paquete.

```bash
agentic-plugins-hook --plugin repository-engineering --event SessionStart
```

```json
{"systemMessage": "Repository Engineering activo. Gates humanos: publish, push, release, delete, deploy, credential, paid. Denegado siempre: bypass-approval, exfiltrate-secret.", "continue": true}
```

Solo imprime. Si el catálogo no se encuentra, devuelve `continue: true` con un mensaje de hook inactivo en vez de bloquear la sesión del host.

---

## Variables de entorno

| Variable | Efecto |
|---|---|
| `AGENTIC_PLUGINS_ROOT` | fija la raíz del repositorio; si es inválida, la CLI falla en vez de buscar en otro sitio |
| `AGENTIC_PLUGINS_ALLOW_REMOTE_BIND` | con valor `1`, permite que `serve` enlace fuera de loopback |
| `PYTHONUTF8` | recomendable en Windows para que los acentos y emoji del catálogo salgan bien en consola |

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="README.md">Documentación</a> · <a href="../INSTALL.md">Instalación</a></sub></div>
