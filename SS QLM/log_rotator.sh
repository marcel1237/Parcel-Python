#!/bin/bash
###############################################################################
# NOME: log_rotator.sh
# DESCRIÇÃO: Comprime logs antigos e deleta logs com mais de 30 dias para economizar
#            espaço em disco no ambiente de desenvolvimento.
#
# FINALIDADE: Manter a pasta do projeto limpa sem perder o histórico recente.
###############################################################################

LOG_DIR="./logs"
mkdir -p "$LOG_DIR"

echo "Rodando manutenção de logs..."

# Comprime logs de texto que ainda não foram comprimidos
find "$LOG_DIR" -name "*.log" -mtime +1 -exec gzip {} \;

# Deleta logs comprimidos com mais de 30 dias
find "$LOG_DIR" -name "*.gz" -mtime +30 -delete

echo "Manutenção concluída."
