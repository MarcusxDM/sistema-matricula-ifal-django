#!/bin/bash
# Script para gerar settings.py a partir do template usando variáveis de ambiente

set -e

SETTINGS_DIR="/app/sistema_academico"
TEMPLATE_FILE="/app/sistema_academico/settings.py.template"
SETTINGS_FILE="$SETTINGS_DIR/settings.py"

echo "Verificando estrutura de diretórios..."
ls -la /app/

echo "Procurando template em: $TEMPLATE_FILE"
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "⚠ Template não encontrado em $TEMPLATE_FILE"
    echo "Procurando em diretórios alternativos..."
    find /app -name "settings.py.template" 2>/dev/null || echo "Nenhum template encontrado"
else
    echo "✓ Template encontrado!"
    # Copiar template se settings.py não existir
    if [ ! -f "$SETTINGS_FILE" ]; then
        echo "Criando settings.py a partir do template..."
        cp "$TEMPLATE_FILE" "$SETTINGS_FILE"
        echo "✓ settings.py criado com sucesso"
    else
        echo "✓ settings.py já existe"
    fi
fi

# Executar o comando passado como argumento
exec "$@"
