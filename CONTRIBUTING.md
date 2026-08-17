# 🤝 Contribuir

> Cómo se propone un plugin nuevo, qué criterios debe cumplir y qué se verifica antes de aceptarlo.

[Repositorio](README.md) · [Documentación](docs/README.md) · [Contrato de plugin](docs/PLUGIN_CONTRACT.md)

---

## Regla principal

Un elemento nuevo debe ser un **plugin**: la unidad de composición, instalación y distribución alrededor de una misión reconocible.

No es un plugin un prompt largo, un script, ni una capacidad suelta. Tampoco lo es un agente: los agentes viven en [`operational-ai-agents`](https://github.com/vladimiracunadev-create/operational-ai-agents) y aquí entran por instantánea versionada.

> [!TIP]
> Prueba de nivel en tres preguntas:
> - ¿Es **una capacidad** que el modelo carga en su contexto? → es un skill: [`claude-skills-toolkit`](https://github.com/vladimiracunadev-create/claude-skills-toolkit).
> - ¿Es **alguien que se encarga de una misión** y responde por el resultado? → es un agente: [`operational-ai-agents`](https://github.com/vladimiracunadev-create/operational-ai-agents).
> - ¿Es **el paquete** que reúne varios de ellos, declara sus límites conjuntos y los deja instalables en cinco plataformas? → es un plugin, y va aquí.

## Antes de escribir nada

```bash
agentic-plugins list
agentic-plugins inspect <plugin-id>
```

Un solapamiento parcial no descalifica la propuesta, pero el PR debe explicar **qué compone el plugin nuevo que ninguno de los seis existentes compone**. Ampliar el catálogo por ampliarlo es un no-objetivo declarado.

## Flujo

1. **Registrar** — añade la entrada canónica en [`catalog/plugins.yaml`](catalog/plugins.yaml).
2. **Escribir a mano** lo único que no se genera: `plugins/<id>/evals/cases.jsonl`, con al menos cuatro casos.
3. **Generar** — `agentic-plugins sync` produce el paquete completo.
4. **Verificar** — `make check`, o la secuencia completa de abajo.

Guía paso a paso en [docs/AUTHORING_GUIDE.md](docs/AUTHORING_GUIDE.md).

> [!IMPORTANT]
> Los manifiestos, los agentes, el skill, los hooks, las políticas, el `provenance.json`, el `README.md`, el icono, el servidor MCP autocontenido y los cuatro adaptadores son **vistas generadas**. No los edites: cambia el catálogo o el renderer en `src/agentic_plugins/render.py` y vuelve a ejecutar `sync`. El validador rechaza cualquier archivo del paquete que no sea una vista o el `cases.jsonl`, y CI rechaza el drift.

## Criterios de aceptación

### Identidad y alcance

- `id` único en kebab-case y versión SemVer alineada con la del repositorio.
- Misión reconocible, no una lista de tareas.
- `description` y `examples` que permitan a un host decidir cuándo el plugin aplica.

### Composición

- Los agentes **deben existir** en `catalog/agents.snapshot.json`. Si el que necesitas no está, el trabajo empieza en `operational-ai-agents`.
- Reutiliza el mínimo: un plugin que compone diez agentes probablemente sean dos plugins.
- Los skills externos se declaran como `optional_skills`. **El plugin tiene que funcionar sin ellos** y declarar la limitación si faltan.

### Permisos

- `default: allow-read-plan`. Las fases iniciales inspeccionan; las mutaciones llegan tras alcance y plan.
- `approval_required` cubre todo lo irreversible o que sale del equipo: publicar, empujar, liberar, borrar, desplegar, credenciales y servicios de pago.
- `denied` no puede estar vacío.
- `human_approval_cannot_be_delegated: true`, sin excepciones.

### Honestidad

- Estado inicial `IMPLEMENTED`, coherente con `maturity.declared`.
- `not_claimed` enumera explícitamente lo que **no** se afirma.
- Nunca declares una madurez que no puedas respaldar con evidencia revisada.

### Evaluaciones

- Al menos cuatro casos con identificadores únicos que prueben **propiedades distintas**.
- Entre ellos, obligatoriamente, uno de no-activación y uno de gate humano.
- Cuatro copias del mismo caso pasan la cuenta pero no aportan garantía, y una prueba lo detecta.

### Contenido

- **Sin secretos, sin datos personales, sin rutas del autor.** El catálogo es público y una prueba lo verifica.
- **Genérico, no personal.** Un plugin atado a tus repositorios o a tu nombre no es reutilizable: parametrízalo por patrón.
- Documentación en español; identificadores y contratos técnicos en inglés estable.

## Calidad

Antes de abrir un PR, ejecuta lo mismo que ejecuta CI:

```bash
make check
```

O paso a paso:

```bash
ruff check .
agentic-plugins sync --check
agentic-plugins validate
agentic-plugins eval --all
python -m unittest discover -s tests -v
```

Sin `make`, típicamente en Windows:

```bash
python scripts/verify.py
```

CI además construye el wheel con instalación limpia, empaqueta dos veces y compara los SHA-256, levanta la imagen Docker y comprueba el panel en vivo, analiza el código con CodeQL y despliega la landing. Referencia completa de comandos en [docs/CLI.md](docs/CLI.md).

## Qué revisa un mantenedor

| Pregunta | Dónde se ve |
|---|---|
| ¿Es un plugin y no un agente o un skill disfrazado? | `mission` y `components` |
| ¿Se solapa con el catálogo? | comparación con `agentic-plugins list` |
| ¿Los agentes existen de verdad? | `catalog/agents.snapshot.json` |
| ¿Los gates cubren lo irreversible? | `policy.approval_required` frente a lo que la misión implica |
| ¿Las evaluaciones prueban cosas distintas? | los cuatro `expected` del `cases.jsonl` |
| ¿Alguien editó una vista a mano? | `agentic-plugins sync --check` |
| ¿Afirma algo que no puede demostrar? | `status`, `maturity` y la ausencia de evidencia |

## Cambiar el núcleo

Si tu PR toca `src/agentic_plugins/policy.py`, recuerda que ese código se **copia literalmente** a los seis servidores MCP distribuidos. Ejecuta `agentic-plugins sync` en el mismo commit: si no, CI fallará con drift en seis archivos y el motivo no será evidente a primera vista.

---

<div align="center"><sub><a href="README.md">Repositorio</a> · <a href="docs/AUTHORING_GUIDE.md">Guía de autoría</a> · <a href="CODE_OF_CONDUCT.md">Código de conducta</a></sub></div>
