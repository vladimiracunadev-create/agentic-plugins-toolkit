# 🔒 Seguridad

> Cómo reportar una vulnerabilidad y qué garantiza —y qué no garantiza— este repositorio.

[Repositorio](README.md) · [Modelo de seguridad completo](docs/SECURITY_MODEL.md)

---

## Reportar una vulnerabilidad

> [!CAUTION]
> **No abras un issue público** ni publiques detalles explotables, secretos o trazas reales.

Usa el canal privado de avisos de seguridad de GitHub:

**[Reportar de forma privada →](https://github.com/vladimiracunadev-create/agentic-plugins-toolkit/security/advisories/new)**

Incluye: versión afectada, pasos de reproducción, impacto esperado y, si lo tienes, una propuesta de mitigación. Sanea cualquier dato antes de adjuntarlo.

## Alcance

| Dentro del alcance | Fuera del alcance |
|---|---|
| La CLI y sus doce comandos | El comportamiento del modelo dentro del host |
| El servidor MCP y los seis servidores distribuidos | Vulnerabilidades de Claude Code, Codex, Copilot o Gemini |
| El panel local | Los skills opcionales del toolkit externo |
| El exportador y el empaquetador | Los agentes en su repositorio de origen |
| Los contratos, permisos y gates declarados | Configuraciones que el usuario relaje a propósito |

## Garantías

Todas están cubiertas por pruebas automatizadas que corren en cada push, en Linux, macOS y Windows sobre Python 3.11, 3.12 y 3.13:

- El servidor MCP que viaja **dentro** de cada paquete no puede clasificar una acción de forma distinta a la CLI: su código de política se copia literalmente y una prueba compara ambos servidores acción por acción.
- `BYPASS_APPROVAL`, `bypass approval` y `Bypass-Approval` son la misma acción denegada: la comparación normaliza mayúsculas y separadores.
- Todo plugin declara gates humanos y acciones denegadas, y la aprobación humana **no** es delegable.
- Una palabra negativa no cancela una acción sujeta a aprobación.
- El exportador **nunca** sobrescribe un directorio que no administra, y `uninstall` se niega a borrar uno sin marca.
- El panel escucha en loopback; salir de ahí exige una variable de entorno explícita, y Compose publica el puerto solo en el loopback del host.
- Los hooks no dependen de un binario `python3` que en Windows no existe.
- Ningún archivo distribuido contiene invocación de shell ni banderas que omitan permisos.
- Todo archivo de un paquete es una vista generada del catálogo o una fuente declarada: no hay una tercera categoría donde esconder algo.
- Los paquetes son reproducibles: mismo contenido ⇒ mismo SHA-256, comprobado empaquetando dos veces en CI.
- Ningún plugin declara adopción productiva.

La tabla completa, con el nombre de la prueba que respalda cada garantía, está en [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md).

## Límites conocidos

Se declaran porque omitirlos sería la clase de afirmación que este proyecto existe para evitar:

- **El panel local no tiene autenticación.** Es para loopback, no para exponerlo.
- **La detección de secretos es heurística.** No sustituye la revisión humana ni un scanner dedicado.
- **La política es comparación de subcadenas normalizadas, no semántica.** Un sinónimo que el contrato no enumere no se detecta; el gate del host sigue siendo la última línea.
- **El aislamiento lo aplica el host, no el toolkit.** El paquete declara límites; quien los hace cumplir en ejecución es el runtime.
- **Reproducible no es firmado.** Hay SHA-256 verificable, pero todavía no hay firma criptográfica ni SBOM.

## Dependencias

El paquete no declara dependencias de runtime. Las acciones de GitHub están fijadas por **SHA de commit**, no por etiqueta. Dependabot revisa mensualmente pip, GitHub Actions y Docker. CodeQL analiza el código en cada push y cada lunes.

---

<div align="center"><sub><a href="README.md">Repositorio</a> · <a href="docs/SECURITY_MODEL.md">Modelo de seguridad</a> · <a href="SUPPORT.md">Soporte</a></sub></div>
