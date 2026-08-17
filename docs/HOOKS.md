# 🪝 Hooks

> Por qué solo hay un hook, qué hace exactamente, qué no hace y qué haría falta para añadir otro.

[Repositorio](../README.md) · [Documentación](README.md) · [Modelo de seguridad](SECURITY_MODEL.md)

---

## El único hook

Cada paquete declara **un** hook, `SessionStart`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "agentic-plugins-hook --plugin repository-engineering --event SessionStart",
            "statusMessage": "Cargando límites de Repository Engineering"
          }
        ]
      }
    ]
  }
}
```

Lo que imprime:

```json
{"systemMessage": "Repository Engineering activo. Gates humanos: publish, push, release, delete, deploy, credential, paid. Denegado siempre: bypass-approval, exfiltrate-secret.", "continue": true}
```

Su único efecto es que la sesión empiece sabiendo dónde se va a detener el plugin.

## Qué no hace

- No escribe archivos.
- No abre conexiones de red.
- No modifica el repositorio.
- No lee nada fuera del catálogo del propio toolkit.
- No bloquea la sesión: si el catálogo no se encuentra, devuelve `continue: true` con un mensaje de hook inactivo.

## Por qué un ejecutable propio y no `python3 -m …`

La versión anterior invocaba `python3 -m agentic_plugins.hooks`. En una instalación estándar de Windows **no existe un binario `python3`**, así que el hook moría en silencio justo en una de las tres plataformas que el repositorio declara soportadas.

Hoy el paquete expone el console script `agentic-plugins-hook`, que `pip` instala con el nombre correcto en cada sistema. `test_hooks_do_not_depend_on_a_python3_binary` recorre todos los `hooks.json` del repositorio y falla si alguno vuelve a mencionarlo, y el job `test` de CI lo ejecuta de verdad en Linux, macOS y Windows.

## Confianza

> [!IMPORTANT]
> Un hook es código que tu host ejecuta por ti. El anfitrión debería mostrártelo y pedirte confianza **antes** de habilitarlo, y tú deberías leerlo. Que este documento afirme que el hook solo imprime no es una razón suficiente para creerlo: el archivo son doce líneas y está en [`src/agentic_plugins/hooks.py`](../src/agentic_plugins/hooks.py).

## Añadir otro hook

No se acepta como cambio rutinario. Un `PreToolUse` o un `PostToolUse` interceptan lo que el modelo hace y son una superficie de seguridad distinta. Para incorporar uno hace falta:

1. una amenaza concreta que el hook mitigue, escrita en [SECURITY_MODEL.md](SECURITY_MODEL.md);
2. la garantía de que sigue sin escribir, sin red y sin ejecutar comandos ajenos;
3. una prueba que verifique su salida;
4. documentación de qué ve y qué puede bloquear;
5. revisión explícita según [GOVERNANCE.md](../GOVERNANCE.md).

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="SECURITY_MODEL.md">Modelo de seguridad</a> · <a href="CLI.md">CLI</a></sub></div>
