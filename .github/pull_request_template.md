## Objetivo

## Plugins o contratos afectados

## Riesgo y aprobaciones

¿Añade, quita o relaja algún gate humano? ¿Amplía lo que un plugin puede tocar?

## Evidencia

- [ ] `ruff check .`
- [ ] `agentic-plugins sync --check` — sin drift respecto del catálogo
- [ ] `agentic-plugins validate` — integridad de los paquetes
- [ ] `agentic-plugins eval --all` — evaluaciones deterministas
- [ ] `python -m unittest discover -s tests -v`
- [ ] No edité ninguna vista generada a mano
- [ ] No contiene secretos ni afirma una madurez no demostrada
