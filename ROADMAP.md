# 🗺️ Roadmap

> De «el paquete está completo» a «el paquete se instaló, se usó y quedó registrado». Cada escalón exige evidencia, no más Markdown.

[Repositorio](README.md) · [Modelo de madurez](docs/MATURITY_MODEL.md) · [Changelog](CHANGELOG.md)

---

## v0.1.0 — base implementada ✅

- [x] Seis plugins con contrato completo y diez agentes por instantánea versionada.
- [x] Cinco targets: OpenAI/Codex, Claude Code, Copilot, Gemini y MCP genérico.
- [x] Veinticuatro evaluaciones deterministas de routing y aprobación.
- [x] Empaquetado reproducible con SHA-256 y exportador que protege lo ajeno.
- [x] Catálogo ARD experimental, declarado como no-conformidad.

## v0.2.0 — coherencia verificable ✅

El salto que convirtió una intención en un mecanismo.

- [x] **Toda la duplicación es ahora una vista generada.** Sesenta y nueve archivos salen del catálogo; el único escrito a mano dentro de un paquete es `evals/cases.jsonl`, y el validador rechaza cualquier otro.
- [x] **El servidor MCP distribuido se genera copiando el código fuente de la política**, con una prueba que compara sus respuestas con las de la CLI acción por acción.
- [x] Panel con guardia de loopback y opt-in explícito.
- [x] Hooks multiplataforma vía console script, verificados en Windows en CI.
- [x] Landing servible desde GitHub Pages, con vista estática generada.
- [x] CI de siete jobs en nueve combinaciones, CodeQL, Pages y Dependabot.
- [x] Documentación completa: índice, referencia de CLI y once documentos temáticos.

## v0.3.0 — uso real y evidencia

El salto que de verdad importa: hoy ningún plugin ha demostrado resolver una misión real.

- [ ] Instalar cada plugin en un host real y registrar la sesión completa.
- [ ] Incorporar casos sanitizados y promover a `OPERATIONAL_LOCAL` **solo** los que cumplan los criterios.
- [ ] Evaluaciones end-to-end por plataforma: instalar, levantar el MCP y disparar el hook dentro del host.
- [ ] Métricas de éxito, duración, intervención humana y retrabajo.
- [ ] Firma criptográfica de los paquetes y SBOM por plugin.

> [!NOTE]
> Este hito no se cierra escribiendo documentación. Se cierra con casos revisados en `evidence/`, uno por plugin promovido.

## v0.4.0 — integraciones

- [ ] Importación versionada de agentes desde el repositorio remoto, en vez de instantánea manual.
- [ ] Registry privado y publicación por canal, no solo por repositorio.
- [ ] A2A Agent Cards por plugin.
- [ ] Políticas OPA/Cedar como backend alternativo al motor propio.
- [ ] MCP Apps UI y sink de evidencia opcional vía OpenTelemetry.

## v1.0.0 — operación observada

- [ ] Contratos estables con migraciones documentadas.
- [ ] Tres o más plugins con uso recurrente y evidencia.
- [ ] Matriz de compatibilidad verificada, no declarada.
- [ ] Auditoría de seguridad externa y prueba de recuperación de extremo a extremo.

## No objetivos

Declarados para que el proyecto no crezca por inercia:

| No objetivo | Por qué |
|---|---|
| Convertirse en un catálogo de agentes | los agentes viven en `operational-ai-agents`; aquí entran por instantánea |
| Convertirse en un catálogo de skills | esos viven en `claude-skills-toolkit` |
| Duplicar los casos de `langgraph-realworld` | ahí viven los procesos sectoriales de referencia |
| Inventar un «formato universal de plugin» | no existe; los manifiestos son adaptadores y se declaran como tales |
| Implementar un motor de agentes | el razonamiento vive en el host, no aquí |
| Incorporar plugins solo para aumentar el catálogo | el tamaño no es una métrica de valor |
| Presentar demos como adopción empresarial | contradice el modelo de madurez |

---

<div align="center"><sub><a href="README.md">Repositorio</a> · <a href="docs/MATURITY_MODEL.md">Madurez</a> · <a href="CONTRIBUTING.md">Contribuir</a></sub></div>
