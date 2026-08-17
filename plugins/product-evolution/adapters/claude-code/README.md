# Claude Code

<!-- Vista generada desde catalog/plugins.yaml. No la edites a mano. -->

Soporte declarado: **native-package**. Claude Code descubre agentes,
skills, hooks y servidores MCP desde la raíz del paquete.

```bash
agentic-plugins export product-evolution --target ~/.claude/plugins
```

El exportador escribe una marca `.agentic-plugins-managed.json` y se
niega a sobrescribir un directorio que no lleve esa marca: un plugin
tuyo con el mismo nombre queda intacto y la operación falla.

> [!IMPORTANT]
> Revisa `hooks/hooks.json` **antes** de confiar en el paquete. El hook
> `SessionStart` solo imprime los límites del plugin, no escribe archivos
> ni accede a la red, pero esa comprobación es tuya y no debería basarse
> en esta frase.

Los agentes de `product-evolution` declaran `model: inherit`: el paquete no
impone modelo ni consume una API por su cuenta.
