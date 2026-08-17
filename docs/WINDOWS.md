# 🪟 Windows

> Lo que cambia en Windows, PowerShell y WSL — y las tres cosas que rompían antes y ahora están cubiertas por CI.

[Repositorio](../README.md) · [Documentación](README.md) · [Instalación](../INSTALL.md)

---

## Instalación

```powershell
python -m pip install -e .
agentic-plugins doctor
agentic-plugins validate
agentic-plugins eval --all
```

O con el script:

```powershell
.\scripts\install.ps1
```

Sin `make`, la verificación completa es:

```powershell
python scripts\verify.py
```

## Codificación

El catálogo lleva acentos y emoji. La consola de Windows usa `cp1252` por defecto y eso produce `UnicodeEncodeError` al imprimir.

```powershell
$env:PYTHONUTF8 = "1"
```

Para dejarlo permanente:

```powershell
setx PYTHONUTF8 1
```

CI define `PYTHONUTF8=1` y `PYTHONIOENCODING=utf-8` en los tres sistemas operativos por la misma razón.

## Lo que estaba roto y ahora se verifica

### 1 · El hook invocaba `python3`

Los `hooks.json` llamaban a `python3 -m agentic_plugins.hooks`. **En una instalación estándar de Windows no hay binario `python3`**, así que el hook moría en silencio.

Hoy invocan el console script `agentic-plugins-hook`, que `pip` instala como `.exe` en `Scripts\`. El job `test` de CI lo ejecuta de verdad en Windows, y `test_hooks_do_not_depend_on_a_python3_binary` falla si alguien vuelve a introducir la dependencia.

### 2 · Los saltos de línea

`.gitattributes` normaliza todo a LF salvo los `.ps1`, que se mantienen en CRLF. Sin eso, un `sync` en Windows reescribiría 69 archivos con CRLF y `sync --check` fallaría en Linux. El escritor de vistas fuerza `newline="\n"` explícitamente.

### 3 · Los pasos multilínea en CI

En `windows-latest` un `run:` multilínea usa PowerShell, que solo propaga el código de salida del **último** comando. Los cuatro gates del job `test` están escritos como pasos separados a propósito: si `validate` falla y `eval` pasa, la build tiene que caer igualmente.

## Rutas

La CLI usa `pathlib` en todo. Los ZIP normalizan los separadores a `/` dentro del archivo, de modo que un paquete construido en Windows y otro construido en Linux tienen **el mismo SHA-256**. `test_packages_are_reproducible` corre en las nueve combinaciones de sistema operativo y versión de Python.

## WSL

Si tu host ejecuta el servidor MCP desde WSL, instala el paquete **dentro** de WSL y usa rutas del mismo entorno:

```bash
python -m pip install -e .
agentic-plugins mcp --plugin repository-engineering
```

Mezclar un `agentic-plugins` de Windows con rutas de WSL —o al revés— produce un `No se encontró catalog/plugins.yaml` que confunde. Si lo necesitas, fija la raíz explícitamente:

```bash
export AGENTIC_PLUGINS_ROOT=/mnt/c/dev/agentic-plugins-toolkit
```

## Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `UnicodeEncodeError` al imprimir el catálogo | consola en cp1252 | `$env:PYTHONUTF8 = "1"` |
| `agentic-plugins` no se reconoce | `Scripts\` fuera del PATH | usa `python -m agentic_plugins` o añade el directorio |
| El hook no aparece en la sesión | el paquete no está instalado en el intérprete que usa el host | instala ahí, o revisa `agentic-plugins doctor` |
| `sync --check` falla justo tras clonar | finales de línea | comprueba que `.gitattributes` se aplicó: `git add --renormalize .` |
| Rutas con espacios | comillas | `agentic-plugins export mi-plugin --target "C:\Mis Cosas\plugins"` |

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="../INSTALL.md">Instalación</a> · <a href="../SUPPORT.md">Soporte</a></sub></div>
