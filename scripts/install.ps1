# Instala la CLI y comprueba que el repositorio esta sano.
# No instala plugins en ningun host: eso es `agentic-plugins export`, que es una
# decision tuya sobre un directorio concreto.
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"

python -m pip install -e .
agentic-plugins doctor
agentic-plugins validate
agentic-plugins list

Write-Host ""
Write-Host "Para instalar un plugin en un host:"
Write-Host "  agentic-plugins export <plugin-id> --target <directorio>"
