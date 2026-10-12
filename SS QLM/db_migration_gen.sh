#!/bin/bash
###############################################################################
# NOME: db_migration_gen.sh
# DESCRIÇÃO: Gera um arquivo SQL de migração com timestamp para controle de
#            versão do esquema do banco de dados.
#
# FINALIDADE: Manter o histórico de mudanças no banco de dados sincronizado
#             entre todos os desenvolvedores do projeto.
###############################################################################

MIGRATION_NAME=${1:-"new_migration"}
TIMESTAMP=$(date +%Y%m%d%H%M%S)
FILE_NAME="resource/migrations/${TIMESTAMP}_${MIGRATION_NAME}.sql"

mkdir -p resource/migrations

cat << SQL > "$FILE_NAME"
-- MIGRATION: $MIGRATION_NAME
-- DATE: $(date)

-- UP: (Ações para aplicar a mudança)
-- CREATE TABLE ...

-- DOWN: (Ações para reverter a mudança)
-- DROP TABLE ...
SQL

echo "📝 Migração criada: $FILE_NAME"
