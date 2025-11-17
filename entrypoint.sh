#!/bin/bash
# Script para gerar settings.py a partir do template usando variáveis de ambiente

set -e

SETTINGS_DIR="/app/sistema_academico"
TEMPLATE_FILE="$SETTINGS_DIR/settings.py.template"
SETTINGS_FILE="$SETTINGS_DIR/settings.py"

# Copiar template se settings.py não existir
if [ ! -f "$SETTINGS_FILE" ]; then
    echo "Criando settings.py a partir do template..."
    cp "$TEMPLATE_FILE" "$SETTINGS_FILE"
    echo "✓ settings.py criado com sucesso"
else
    echo "✓ settings.py já existe"
fi

# Executar o comando passado como argumento
exec "$@"
