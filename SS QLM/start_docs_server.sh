#!/bin/bash
###############################################################################
# NOME: start_docs_server.sh
# DESCRIÇÃO: Inicia um servidor HTTP local super leve para visualizar a
#            documentação gerada ou o manual do projeto no navegador.
#
# POR QUE USAR: Visualizar diagramas do Doxygen ou arquivos HTML do projeto
#              sem precisar abrir os arquivos manualmente no navegador.
###############################################################################

PORT=8000
DOCS_DIR="./docs/html"

if [ ! -d "$DOCS_DIR" ]; then
    echo "Erro: Pasta de documentação não encontrada. Execute 'gen_docs.sh' primeiro."
    exit 1
fi

echo "Iniciando servidor de documentação em http://localhost:$PORT"
cd "$DOCS_DIR" && python3 -m http.server $PORT
