#!/bin/bash
###############################################################################
# NOME: resource_integrity.sh
# DESCRIÇÃO: Gera e valida somas de verificação (Checksums) para todos os arquivos
#            na pasta resource/.
#
# POR QUE USAR: Garantir que nenhum banco de dados ou ícone foi corrompido durante
#              o download ou transferência do projeto.
###############################################################################

CHECKSUM_FILE="resource/integrity.sha256"

if [[ "$1" == "--verify" ]]; then
    echo "Verificando integridade dos recursos..."
    sha256sum -c "$CHECKSUM_FILE"
else
    echo "Gerando mapa de integridade para resource/..."
    find resource/ -type f ! -name "integrity.sha256" -exec sha256sum {} + > "$CHECKSUM_FILE"
    echo "Mapa gerado em $CHECKSUM_FILE"
fi
