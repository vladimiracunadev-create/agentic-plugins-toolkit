# 🔍 Evidencia

> Qué se registra aquí, cómo se sanitiza y qué no se guarda nunca.

[Repositorio](../README.md) · [Modelo de madurez](../docs/MATURITY_MODEL.md) · [Evaluación](../docs/EVALUATION.md)

---

## Para qué existe este directorio

**Está vacío a propósito.** Es el único mecanismo por el que un plugin puede pasar de `IMPLEMENTED` a `OPERATIONAL_LOCAL`, y hoy ninguno lo ha hecho.

Un plugin con manifiestos válidos, evaluaciones en verde y ZIP reproducibles ha demostrado **integridad del paquete**, no que sirva para algo. Lo segundo se demuestra usándolo y dejando constancia.

## Qué debe contener un caso

Un archivo por ejecución, en `evidence/case-studies/<plugin-id>-<fecha>.md`:

| Sección | Contenido |
|---|---|
| Contexto | plataforma, versión del host, versión del plugin, tipo de repositorio o proyecto |
| Misión | lo que se encargó, literal |
| Recorrido | qué hizo, fase por fase |
| **Gates** | **dónde se detuvo, qué se le autorizó y qué se le denegó** |
| Resultado | qué produjo, con comandos o archivos que lo respalden |
| Verificación | cómo se comprobó que el resultado era correcto |
| Riesgo residual | qué quedó sin resolver o sin comprobar |
| Duración e intervención | tiempo y cuántas veces hubo que corregirlo |

La sección de gates es la que más importa: un caso donde el plugin no se detuvo en ningún momento es tan informativo como uno donde se detuvo cuatro veces, y por razones distintas.

## Qué no se guarda nunca

> [!CAUTION]
> Nada de esto entra aquí: secretos, tokens, credenciales, claves API, prompts privados, datos personales de terceros, rutas locales que identifiquen a alguien, ni contenido de repositorios ajenos sin autorización.

Si un fragmento es necesario para entender el caso pero contiene algo de lo anterior, sustitúyelo por `<redactado: motivo>` en vez de borrarlo en silencio: así el caso sigue siendo legible y se sabe que falta algo.

## Cómo se promueve un plugin

1. Se instala en un host real y se le encarga una misión completa.
2. Se registra la sesión y se sanitiza.
3. Una **persona** revisa el caso y decide si cumple los criterios de [docs/MATURITY_MODEL.md](../docs/MATURITY_MODEL.md).
4. Si cumple, se cambia el `status` en `catalog/plugins.yaml`, se ejecuta `agentic-plugins sync` y se registra en el [CHANGELOG](../CHANGELOG.md).

> [!IMPORTANT]
> Ningún agente puede ejecutar el paso 3. La promoción de madurez es una afirmación pública sobre adopción, y la toma una persona.

## Un cambio de contrato invalida la evidencia

Si cambia la misión, la composición, la política o los gates de un plugin, los casos anteriores dejan de respaldar su estado: describen un paquete que ya no existe. El plugin vuelve a `IMPLEMENTED` hasta que haya evidencia nueva.

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="../docs/MATURITY_MODEL.md">Madurez</a> · <a href="../GOVERNANCE.md">Gobernanza</a></sub></div>
