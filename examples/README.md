# 🧪 Ejemplos

> Todo lo de aquí corre offline, sin clave API y sin costo. Copia, pega y observa.

[Repositorio](../README.md) · [CLI](../docs/CLI.md) · [MCP](../docs/MCP.md)

---

## 1 · Ver qué hay y qué límites tiene

```bash
agentic-plugins list
agentic-plugins inspect rootcause-response
```

```text
RootCause Response (rootcause-response)
Estado: IMPLEMENTED | Riesgo: high
Misión: Reducir incertidumbre, preservar evidencia y remediar sin introducir un segundo incidente.
Agentes: incident-root-cause-agent, security-remediation-agent
Aprobación humana: publish, deploy, delete, credential, production, paid
Denegado: bypass-approval, exfiltrate-secret
```

## 2 · Preguntar dónde se detendría, antes de instalarlo

```bash
agentic-plugins policy-check rootcause-response --action "leer los logs del incidente"
agentic-plugins policy-check rootcause-response --action "desplegar el parche a producción"
agentic-plugins policy-check rootcause-response --action "BYPASS_APPROVAL"
```

```json
{"action": "leer los logs del incidente",        "decision": "allowed",           "matched": null}
{"action": "desplegar el parche a producción",   "decision": "approval-required", "matched": "deploy"}
{"action": "BYPASS_APPROVAL",                    "decision": "denied",            "matched": "bypass-approval"}
```

El tercero es interesante: la comparación normaliza mayúsculas y trata `_` y `-` como equivalentes, así que escribirlo de otra forma no lo convierte en permitido.

## 3 · Hablar con el servidor MCP sin instalar nada

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"create_execution_plan","arguments":{"task":"auditar el repositorio"}}}' \
  | python plugins/repository-engineering/runtime/mcp_server.py
```

El plan que devuelve tiene ocho pasos y uno de ellos es `human-gates`. Es un plan: no ejecuta nada.

## 4 · Comprobar que el paquete distribuido y la CLI dicen lo mismo

```bash
ACTION='{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"policy_check","arguments":{"action":"BYPASS_APPROVAL now"}}}'

echo "$ACTION" | python plugins/repository-engineering/runtime/mcp_server.py
echo "$ACTION" | agentic-plugins mcp --plugin repository-engineering
```

Las dos salidas son idénticas. En la versión 0.1.0 no lo eran: la primera decía `allowed` y la segunda `denied`.

## 5 · Verificar que los paquetes son reproducibles

```bash
agentic-plugins package --all --output /tmp/a
agentic-plugins package --all --output /tmp/b
diff /tmp/a/checksums.json /tmp/b/checksums.json && echo "idénticos"
```

## 6 · Comprobar que el exportador respeta lo que no administra

```bash
mkdir -p /tmp/host/portfolio-governance
echo "esto es mío" > /tmp/host/portfolio-governance/mio.txt

agentic-plugins export portfolio-governance --target /tmp/host
# ERROR: Conflicto no administrado: /tmp/host/portfolio-governance

cat /tmp/host/portfolio-governance/mio.txt   # sigue ahí
```

## 7 · Ver el drift en acción

```bash
echo "una línea a mano" >> plugins/product-evolution/README.md
agentic-plugins sync --check
# Drift en 1 archivos:
#   plugins/product-evolution/README.md

agentic-plugins sync    # lo regenera y descarta la edición
```

Es exactamente lo que hace CI en cada push.

## 8 · Levantar el panel

```bash
agentic-plugins serve --host 127.0.0.1 --port 8787
curl -s http://127.0.0.1:8787/healthz
curl -s http://127.0.0.1:8787/api/plugins | head -c 200
```

Y comprobar que se niega a exponerse:

```bash
agentic-plugins serve --host 0.0.0.0
# ERROR: El panel no tiene autenticación: use loopback o declare
#        AGENTIC_PLUGINS_ALLOW_REMOTE_BIND=1 si de verdad quiere exponer 0.0.0.0.
```

---

<div align="center"><sub><a href="../README.md">Repositorio</a> · <a href="../docs/CLI.md">CLI</a> · <a href="../INSTALL.md">Instalación</a></sub></div>
