#!/usr/bin/env sh
# Instala la CLI y comprueba que el repositorio está sano.
# No instala plugins en ningún host: eso es `agentic-plugins export`, que es una
# decisión tuya sobre un directorio concreto.
set -eu

python -m pip install -e .
agentic-plugins doctor
agentic-plugins validate
agentic-plugins list

printf '\nPara instalar un plugin en un host:\n'
printf '  agentic-plugins export <plugin-id> --target <directorio>\n'
