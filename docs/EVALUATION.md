# ✅ Evaluación

> Qué demuestran las 24 evaluaciones deterministas, qué explícitamente **no** demuestran y qué haría falta para poder afirmar más.

[Repositorio](../README.md) · [Documentación](README.md) · [Modelo de madurez](MATURITY_MODEL.md)

---

## Las dos capas que existen hoy

### Capa 1 · Evaluaciones de contrato — 24 casos

Cuatro por plugin, en `plugins/<id>/evals/cases.jsonl`. Cada caso declara una entrada en lenguaje natural y el resultado esperado del router:

```json
{"id": "human-gate", "input": "Ejecuta publish inmediatamente.", "expected": {"activate": true, "approval": true}}
```

Cada plugin cubre cuatro propiedades **distintas**:

| Caso | Qué prueba |
|---|---|
| `direct-activation` | una petición típica activa el plugin |
| `indirect-activation` | una formulación oblicua también lo activa |
| `negative-routing` | una petición ajena **no** lo activa |
| `human-gate` | una acción irreversible activa **y** exige aprobación |

El validador exige al menos cuatro casos con identificadores únicos, y una prueba exige que entre ellos haya siempre uno de no-activación y uno de gate humano: cuatro copias del mismo caso pasan la cuenta pero no aportan garantía.

```bash
agentic-plugins eval --all
agentic-plugins eval repository-engineering --json
```

### Capa 2 · Pruebas de propiedad — 55 pruebas

`tests/test_toolkit.py` verifica lo que un `cases.jsonl` no puede: coherencia de versión entre marcadores, ausencia de drift, ausencia de duplicación no gobernada, reproducibilidad de los paquetes, protección del exportador, guardia de loopback del panel, y la equivalencia entre el servidor MCP de la CLI y el que viaja dentro del paquete.

```bash
python -m unittest discover -s tests -v
```

## Qué demuestra esto

- Que el **routing** distingue lo que le compete de lo que no.
- Que los **gates humanos** existen y se disparan donde deben.
- Que la **política** clasifica igual en la CLI y en el paquete distribuido, ante mayúsculas y separadores distintos.
- Que la **documentación no puede contradecir al contrato**, porque se genera de él.
- Que los **paquetes son reproducibles** byte a byte.

Todo eso son propiedades del **contrato**. Son verificables, deterministas y corren sin consumir un solo token.

## Qué NO demuestra

Esto no es una carencia oculta; es la razón por la que los seis plugins declaran `IMPLEMENTED` y no más:

- **No demuestra que un host instale y ejecute el paquete correctamente.** Nadie ha registrado todavía una sesión real completa con cada plugin en cada plataforma declarada.
- **No demuestra que el modelo obedezca la política.** El contrato la declara y el host debería aplicarla; que un LLM concreto lo respete en un caso adversarial es otra pregunta.
- **No demuestra calidad del resultado.** Que el plugin correcto se active no dice nada sobre si el trabajo que produce sirve.
- **No hay evaluaciones model-graded.** No hay juicio de un modelo sobre salidas reales, versionado por runtime y por modelo.
- **No hay métricas de uso**, costo, duración ni retrabajo, porque todavía no existen ejecuciones que medir.

## Qué haría falta para afirmar más

| Para promover a | Hace falta |
|---|---|
| `OPERATIONAL_LOCAL` | instalar el plugin en un host real, ejecutar una misión completa y guardar la sesión sanitizada en `evidence/` |
| `INTEGRATED` | pruebas end-to-end por plataforma que instalen el paquete, levanten el MCP y comprueben el hook dentro del host |
| `PRODUCTION_OBSERVED` | uso recurrente con trazas, métricas y revisión humana de los resultados |

Criterios completos en [MATURITY_MODEL.md](MATURITY_MODEL.md); formato de la evidencia en [`evidence/README.md`](../evidence/README.md).

## Añadir una evaluación

`evals/cases.jsonl` es el **único** archivo de un paquete que se escribe a mano. Una línea por caso:

```json
{"id": "identificador-unico", "input": "la frase del usuario", "expected": {"activate": true, "approval": false}}
```

Luego:

```bash
agentic-plugins eval <plugin-id>
agentic-plugins validate
```

> [!TIP]
> Un caso que falla no significa necesariamente que el caso esté mal. Si la frase es razonable y el router no la enruta, lo que hay que ajustar son las `activation.keywords` del catálogo — y entonces conviene comprobar que el cambio no activa el plugin en las peticiones ajenas.

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="MATURITY_MODEL.md">Madurez</a> · <a href="PLUGIN_CONTRACT.md">Contrato</a></sub></div>
