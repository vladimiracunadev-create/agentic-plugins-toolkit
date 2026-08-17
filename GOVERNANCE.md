# 🏛️ Gobernanza

> Quién decide qué, y qué decisiones no puede tomar nunca un agente — incluidos los que este repositorio empaqueta.

[Repositorio](README.md) · [Contribuir](CONTRIBUTING.md) · [Modelo de madurez](docs/MATURITY_MODEL.md)

---

## Decisión final

El propietario del repositorio mantiene la decisión final sobre el catálogo, los releases y la promoción de madurez.

## Cambios que exigen revisión explícita

Estos no se aceptan como cambio rutinario, aunque la build quede verde:

| Cambio | Por qué |
|---|---|
| Añadir, quitar o relajar un gate humano | altera la frontera de autorización del plugin |
| Modificar `policy.py` | su código se copia a los seis servidores distribuidos: el cambio llega a todo lo que se instale |
| Ampliar `AUTHORED_FILES` en el validador | abre una vía para introducir archivos a mano en los paquetes |
| Añadir un hook nuevo | intercepta lo que el modelo hace; es otra superficie de seguridad |
| Actualizar la instantánea de agentes | cambia lo que se distribuye sin que el catálogo de plugins lo refleje |
| Promover el estado de madurez de un plugin | es una afirmación pública sobre adopción |
| Retirar una prueba que respalda una garantía | convierte una garantía verificada en una promesa |
| Cambiar el empaquetador | puede romper la reproducibilidad sin que nada más falle |

## Reglas que no dependen de nadie

1. **Ningún plugin puede autopromover su estado de madurez.** El `status` lo cambia una persona con evidencia revisada.
2. **Ningún agente puede aprobar su propia publicación**, ni la de otro.
3. **La aprobación de un agente no sustituye la del usuario.** Un coordinador eleva la decisión; no la resuelve.
4. **Las garantías se retiran con su prueba, no sin ella.** Si una garantía deja de cumplirse, se elimina de la documentación en el mismo cambio.
5. **Todo dato duplicado se genera.** Si un cambio necesita mantener un archivo a mano dentro de un paquete, la decisión correcta casi siempre es cambiar el renderer.

## Versionado

- El repositorio y cada plugin comparten versión: un cambio del contrato de plugin afecta a todo lo que se distribuye.
- Un cambio material del contrato —misión, composición, política o gates— **invalida la evidencia previa** y puede degradar el estado del plugin.
- El formato de changelog y el criterio semántico están en [CHANGELOG.md](CHANGELOG.md).

## Qué se declara y qué no

El proyecto asume un compromiso explícito de no exagerar:

- no se afirma uso productivo sin evidencia sanitizada en `evidence/`;
- no se afirma conformidad con especificaciones que aún se mueven (ver [docs/ARD_DISCOVERY.md](docs/ARD_DISCOVERY.md));
- no se presentan como implementadas las integraciones del roadmap;
- no se llama «portable» a lo que es un adaptador con menos capacidades.

---

<div align="center"><sub><a href="README.md">Repositorio</a> · <a href="CODE_OF_CONDUCT.md">Código de conducta</a> · <a href="ROADMAP.md">Roadmap</a></sub></div>
