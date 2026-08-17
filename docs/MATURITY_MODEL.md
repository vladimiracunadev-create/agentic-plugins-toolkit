# 📈 Modelo de madurez

> Cinco estados, qué evidencia exige cada promoción y por qué hoy los seis plugins están en el segundo.

[Repositorio](../README.md) · [Documentación](README.md) · [Evaluación](EVALUATION.md)

---

## Los cinco estados

| Estado | Significa | Evidencia mínima | Hoy |
|---|---|---|:-:|
| `DRAFT` | diseño incompleto | — no se distribuye | 0 |
| `IMPLEMENTED` | el paquete está completo y validado | manifiestos, políticas, MCP, adaptadores y evaluaciones que pasan | **6** |
| `OPERATIONAL_LOCAL` | alguien lo usó de verdad | una sesión real registrada y sanitizada por plugin | 0 |
| `INTEGRATED` | funciona dentro de un host | prueba end-to-end por plataforma: instalar, levantar MCP, disparar el hook | 0 |
| `PRODUCTION_OBSERVED` | se usa de forma recurrente | trazas, métricas de éxito y retrabajo, revisión humana | 0 |

## La distinción que sostiene todo

> **Integridad de archivos ≠ adopción.**

Un paquete puede tener manifiestos válidos, políticas coherentes, evaluaciones en verde y ZIP reproducibles, y aun así **no haber resuelto nunca un problema real**. Ese es exactamente el estado de este repositorio hoy, y declararlo es parte del diseño.

`IMPLEMENTED` afirma: *el contrato está completo y verificado*. No afirma: *esto funciona en producción*.

## Reglas de promoción

1. **Ningún plugin se autopromueve.** El `status` lo cambia una persona con evidencia revisada.
2. **La evidencia se sanitiza antes de entrar.** Sin secretos, sin datos personales, sin rutas del autor, sin prompts privados de terceros.
3. **Un cambio material del contrato invalida la evidencia previa.** Si cambia la misión, la composición o los gates, el plugin vuelve a `IMPLEMENTED`.
4. **La promoción es por plugin, no por repositorio.** Que uno alcance `OPERATIONAL_LOCAL` no arrastra a los otros cinco.
5. **Una garantía se retira con su prueba, no sin ella.** Si deja de cumplirse, se elimina de la documentación en el mismo cambio.

## Qué se necesita para el siguiente escalón

Para que un plugin pase a `OPERATIONAL_LOCAL` hace falta un caso en `evidence/` con:

- la plataforma y la versión del host;
- la misión encargada, literal;
- qué hizo el plugin, fase por fase;
- **dónde se detuvo** y qué se aprobó;
- el resultado verificable y el riesgo residual;
- todo saneado.

El mecanismo está construido y vacío a propósito: [`evidence/README.md`](../evidence/README.md).

## Cómo se declara en el contrato

```json
"maturity": {
  "declared": "IMPLEMENTED",
  "claim": "Paquete, contratos, validación y evaluaciones disponibles.",
  "not_claimed": ["OPERATIONAL_LOCAL", "INTEGRATED", "PRODUCTION_OBSERVED"]
}
```

`declared` debe coincidir con `status` —el validador lo exige— y `not_claimed` enumera explícitamente lo que **no** se está afirmando. `test_status_is_honest` verifica que ningún plugin omita `PRODUCTION_OBSERVED` de esa lista.

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="EVALUATION.md">Evaluación</a> · <a href="../ROADMAP.md">Roadmap</a></sub></div>
