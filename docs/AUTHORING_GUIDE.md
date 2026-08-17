# ✍️ Guía de autoría

> Cómo se escribe un plugin nuevo, en orden, y qué comprobar antes de abrir el PR.

[Repositorio](../README.md) · [Documentación](README.md) · [Contribuir](../CONTRIBUTING.md)

---

## Antes de escribir nada

Comprueba que ningún plugin del catálogo cubra ya la misión:

```bash
agentic-plugins list
agentic-plugins inspect <plugin-id>
```

Un solapamiento parcial no descalifica la propuesta, pero el PR debe explicar **qué compone el plugin nuevo que ninguno de los seis existentes compone**. Ampliar el catálogo por ampliarlo es un no-objetivo declarado.

> [!TIP]
> Prueba rápida de nivel: si lo que propones es **una capacidad**, es un skill y su hogar es `claude-skills-toolkit`. Si es **alguien que se encarga de una misión y responde por ella**, es un agente y su hogar es `operational-ai-agents`. Si es **el paquete que reúne varios de ellos alrededor de una misión e instala en cinco plataformas**, entonces sí es un plugin y va aquí.

## Los siete pasos

### 1 · Define una misión reconocible

No una lista de tareas. La misión es el resultado integral del que el paquete responde: «convertir mantenimiento amplio en cambios verificables», no «hacer cosas con repositorios».

### 2 · Reutiliza el mínimo de agentes y skills

Los agentes salen de `catalog/agents.snapshot.json`. El validador rechaza cualquier identificador que no esté ahí: si tu plugin necesita un agente que no existe, el trabajo empieza en `operational-ai-agents`, no aquí.

### 3 · Registra la entrada canónica

Añade el objeto en [`catalog/plugins.yaml`](../catalog/plugins.yaml). Todos los campos son obligatorios; la referencia está en [PLUGIN_CONTRACT.md](PLUGIN_CONTRACT.md).

```json
{
  "schema_version": "1.0",
  "id": "mi-plugin",
  "name": "Mi Plugin",
  "version": "0.2.0",
  "status": "IMPLEMENTED",
  "icon": "🧪",
  "category": "Developer Tools",
  "risk": "medium",
  "description": "…",
  "mission": "…",
  "source": { "…" },
  "components": { "…" },
  "targets": [ "…" ],
  "policy": { "…" },
  "activation": { "…" },
  "examples": [ "…" ],
  "maturity": { "declared": "IMPLEMENTED", "…" }
}
```

### 4 · Declara la política con honestidad

Tres listas, ninguna vacía:

- `approval_required` — todo lo irreversible o que sale del equipo: publicar, empujar, liberar, borrar, desplegar, credenciales, servicios de pago.
- `denied` — lo que no se autoriza nunca, con o sin aprobación.
- `human_approval_cannot_be_delegated: true` — no es opcional.

Si dudas de si algo va en `approval_required`, pregúntate si te molestaría descubrir que ocurrió sin avisarte.

### 5 · Escribe las evaluaciones

`plugins/<id>/evals/cases.jsonl` es el **único** archivo que creas a mano. Mínimo cuatro casos que prueben propiedades distintas:

```json
{"id": "direct-activation",   "input": "…", "expected": {"activate": true,  "approval": false}}
{"id": "indirect-activation", "input": "…", "expected": {"activate": true,  "approval": false}}
{"id": "negative-routing",    "input": "…", "expected": {"activate": false, "approval": false}}
{"id": "human-gate",          "input": "…", "expected": {"activate": true,  "approval": true}}
```

Una prueba exige que haya siempre un caso de no-activación y uno de gate humano.

### 6 · Genera

```bash
agentic-plugins sync
```

Esto crea el paquete completo: manifiestos, agentes, skill, hooks, políticas, `provenance.json`, README, icono, servidor MCP autocontenido y los cuatro adaptadores.

> [!IMPORTANT]
> **No edites nada de lo que `sync` produce.** Si el resultado no te gusta, el cambio va en `catalog/plugins.yaml` o en `src/agentic_plugins/render.py`. El validador rechaza cualquier archivo del paquete que no sea una vista generada o el `cases.jsonl`, y CI rechaza el drift.

### 7 · Verifica

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

Sin `make`:

```bash
python scripts/verify.py
```

## Cambiar cómo se ven los paquetes

Si lo que quieres es cambiar el **formato** de una vista —la ficha de un plugin, el adaptador de Gemini, el servidor MCP— el archivo es [`src/agentic_plugins/render.py`](../src/agentic_plugins/render.py). Modifica el renderer, ejecuta `sync` y los seis paquetes cambian a la vez.

Si lo que cambias es la **semántica de política**, el archivo es [`src/agentic_plugins/policy.py`](../src/agentic_plugins/policy.py) — y `sync` regenerará los seis servidores MCP distribuidos, porque su código se copia literalmente de ahí. Si no ejecutas `sync`, CI te lo dirá.

## Errores frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `Agente fuera de la instantánea` | referenciaste un agente que no existe | añádelo primero a `operational-ai-agents` y actualiza la instantánea |
| `Archivo no gobernado por el catálogo` | creaste un archivo a mano dentro del paquete | genéralo desde el renderer, o justifica la excepción en `AUTHORED_FILES` |
| `plugin.yaml tiene drift` | editaste una vista en vez del catálogo | `agentic-plugins sync` y edita `catalog/plugins.yaml` |
| Una evaluación falla | el routing no cubre esa formulación | ajusta `activation.keywords` y comprueba que no activa peticiones ajenas |
| `Se requieren al menos cuatro evals` | faltan casos | añádelos con identificadores únicos |

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="PLUGIN_CONTRACT.md">Contrato</a> · <a href="../CONTRIBUTING.md">Contribuir</a></sub></div>
