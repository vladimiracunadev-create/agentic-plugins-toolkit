# 📜 Contrato de plugin

> Qué declara un plugin campo a campo, qué invariantes cumple siempre y qué rechaza el validador.

[Repositorio](../README.md) · [Documentación](README.md) · [Arquitectura](ARCHITECTURE.md)

---

## Dónde vive

La entrada canónica de cada plugin está en [`catalog/plugins.yaml`](../catalog/plugins.yaml). El schema formal está en [`schemas/plugin.schema.json`](../schemas/plugin.schema.json).

> [!NOTE]
> El archivo lleva extensión `.yaml` y contiene **JSON**, que es un subconjunto válido de YAML 1.2. La razón es concreta: la CLI no declara dependencias de runtime, y parsear YAML completo exigiría `pyyaml`. El nombre sigue el estándar de los repositorios relacionados; la consecuencia —solo se acepta el subconjunto JSON— se declara aquí en vez de descubrirse al primer `#` de comentario.

## Campos del contrato

### Identidad

| Campo | Tipo | Regla |
|---|---|---|
| `schema_version` | string | versión del contrato |
| `id` | string | **kebab-case**, único en el catálogo |
| `name` | string | nombre legible |
| `version` | string | **SemVer** `X.Y.Z` |
| `icon` | string | un emoji; se proyecta al `assets/icon.svg` generado |
| `category` | string | categoría del host (`Developer Tools`, `Security`, …) |
| `risk` | enum | `low` · `medium` · `high` |
| `status` | enum | estado de madurez actual |

### Propósito

| Campo | Regla |
|---|---|
| `description` | qué hace, en una frase; se proyecta a los cinco manifiestos |
| `mission` | el resultado integral del que el plugin responde |
| `examples` | frases literales que un usuario escribiría; alimentan el `defaultPrompt` de OpenAI |

### Composición

```json
"components": {
  "agents": ["repository-evolution-agent", "…"],
  "skills": ["repository-engineering-workflow"],
  "optional_skills": ["md-lint-fix", "security-audit", "…"],
  "mcp_servers": ["repository-engineering-control"],
  "hooks": ["SessionStart"],
  "custom_ui": false
}
```

- `agents` — identificadores que **deben existir** en `catalog/agents.snapshot.json`. El validador lo comprueba: un agente inventado rompe la build.
- `skills` — el workflow propio del plugin; al menos uno.
- `optional_skills` — mejoras que vienen de `claude-skills-toolkit`. El plugin **funciona sin ellas** y lo declara.
- `mcp_servers` / `hooks` — lo que el paquete expone al host.

### Procedencia

```json
"source": {
  "agents_repository": "operational-ai-agents",
  "agents_snapshot_version": "0.1.0",
  "skills_repository": "claude-skills-toolkit",
  "skills_mode": "optional-versioned-dependencies"
}
```

Se proyecta al `provenance.json` generado de cada paquete. Distingue lo que se **incorpora** (agentes, por instantánea versionada) de lo que se **declara** (skills, como dependencia opcional).

### Targets

```json
"targets": [
  {"id": "openai",         "support": "native-package"},
  {"id": "claude-code",    "support": "native-package"},
  {"id": "github-copilot", "support": "generated-agent-profiles"},
  {"id": "gemini",         "support": "generated-instructions"},
  {"id": "generic-mcp",    "support": "stdio"}
]
```

El nivel de soporte es parte del contrato precisamente para no insinuar equivalencia entre plataformas. Ver [PLATFORM_COMPATIBILITY.md](PLATFORM_COMPATIBILITY.md).

### Política

```json
"policy": {
  "default": "allow-read-plan",
  "approval_required": ["publish", "push", "release", "delete", "deploy", "credential", "paid"],
  "denied": ["bypass-approval", "exfiltrate-secret"],
  "human_approval_cannot_be_delegated": true
}
```

| Clave | Significado |
|---|---|
| `default` | qué puede hacer el plugin sin preguntar: leer y planificar |
| `approval_required` | acciones que **se detienen** y esperan una decisión humana |
| `denied` | acciones que no se autorizan nunca, con o sin aprobación |
| `human_approval_cannot_be_delegated` | ni otro agente ni una tool aprueban en tu lugar |

Las tres listas se proyectan a `policies/policy.json`, al mensaje del hook, a la ficha del plugin, al adaptador de Gemini y al servidor MCP. El validador exige que ninguna esté vacía y que la última sea verdadera.

### Activación

```json
"activation": {
  "keywords": ["repositorio", "readme", "release", "…"],
  "negative_keywords": ["clima", "receta", "película"]
}
```

El router activa el plugin cuando hay una señal positiva **o** una acción sujeta a aprobación. Una palabra negativa desactiva **solo** si no hay ninguna de las dos: «publica el release aunque haga mal clima» sigue siendo una publicación y debe detenerse en su gate. Hay una prueba para eso.

### Madurez

```json
"maturity": {
  "declared": "IMPLEMENTED",
  "claim": "Paquete, contratos, validación y evaluaciones disponibles.",
  "not_claimed": ["OPERATIONAL_LOCAL", "INTEGRATED", "PRODUCTION_OBSERVED"]
}
```

`declared` debe coincidir con `status`, y lo que **no** se afirma se enumera explícitamente. Ver [MATURITY_MODEL.md](MATURITY_MODEL.md).

---

## Las invariantes

Cada una tiene una comprobación en `validator.py`, una prueba en `tests/test_toolkit.py` o ambas.

1. **El `id` es kebab-case y único.** Es la clave de directorio, de manifiesto y de URN.
2. **La versión es SemVer** y coincide con la del paquete Python y la del repositorio.
3. **Todo agente declarado existe en la instantánea.** No se referencian agentes que no viajan dentro del paquete.
4. **Todo plugin declara al menos un agente y un skill.**
5. **Toda política declara aprobaciones y denegaciones no vacías**, y la aprobación humana no es delegable.
6. **`status` y `maturity.declared` coinciden.** No se puede prometer un estado en un campo y otro en el vecino.
7. **Al menos cuatro evaluaciones, con identificadores únicos**, y entre ellas un caso de no-activación y un caso de gate humano.
8. **Ningún archivo del paquete contiene secretos ni comandos peligrosos.**
9. **Las rutas de los manifiestos son relativas y no escapan hacia arriba.**
10. **Todo archivo del paquete es una vista generada o `evals/cases.jsonl`.** No hay una tercera categoría.

## Qué rechaza el validador

```bash
agentic-plugins validate
```

| Hallazgo | Nivel |
|---|---|
| Campo obligatorio ausente | `error` |
| `id` fuera de kebab-case o versión no SemVer | `error` |
| Agente que no está en la instantánea | `error` |
| Política vacía o aprobación declarada delegable | `error` |
| `status` distinto de `maturity.declared` | `error` |
| Menos de cuatro evaluaciones o identificadores repetidos | `error` |
| Vista generada ausente | `error` |
| Archivo no gobernado por el catálogo | `error` |
| Posible secreto o comando peligroso | `error` |
| Directorio en `plugins/` que el catálogo no lista | `warning` |

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="ARCHITECTURE.md">Arquitectura</a> · <a href="AUTHORING_GUIDE.md">Guía de autoría</a></sub></div>
