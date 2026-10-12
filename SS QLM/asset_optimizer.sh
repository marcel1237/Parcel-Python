#!/bin/bash
###############################################################################
# NOME: asset_optimizer.sh
# DESCRIÇÃO: Varre a pasta 'resource/' e otimiza imagens PNG/JPG e remove metadados
#            desnecessários para reduzir o tamanho final do binário/instalador.
#
# REQUISITOS: Necessita de 'optipng' ou 'imagemagick' instalados.
#
# LÓGICA:
#   Busca recursivamente por arquivos de imagem e aplica compressão sem perda
#   de qualidade (lossless), garantindo que os ícones do projeto fiquem leves.
###############################################################################

ASSET_DIR="./resource"

if ! command -v optipng &> /dev/null; then
    echo "Erro: 'optipng' não encontrado. Instale-o com: sudo apt install optipng"
    exit 1
fi

echo "Otimizando ativos na pasta $ASSET_DIR..."

find "$ASSET_DIR" -name "*.png" -exec optipng -o2 {} \;

echo "Otimização concluída."
