#!/bin/bash
###############################################################################
# NOME: gen_docs.sh
# DESCRIÇÃO: Automatiza a geração de documentação técnica do projeto usando
#            Doxygen e Graphviz para gerar diagramas de classes.
#
# REQUISITOS: Doxygen instalado.
###############################################################################

if ! command -v doxygen &> /dev/null; then
    echo "Erro: Doxygen não encontrado. Instale com: sudo apt install doxygen"
    exit 1
fi

echo "Gerando documentação técnica..."
if [ ! -f Doxyfile ]; then
    echo "Doxyfile não encontrado. Gerando configuração padrão..."
    doxygen -g
fi

doxygen Doxyfile
echo "Documentação gerada na pasta docs/html."
