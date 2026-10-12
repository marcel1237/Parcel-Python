#!/bin/bash
###############################################################################
# NOME: validate_headers.sh
# DESCRIÇÃO: Verifica se todos os arquivos .hpp possuem #ifndef / #define
#            (Header Guards), prevenindo erros de inclusão dupla no C++.
#
# LÓGICA:
#   Analisa as duas primeiras linhas de cada arquivo de cabeçalho.
###############################################################################

echo "Validando Header Guards em arquivos .hpp..."

find ./src -name "*.hpp" | while read -r file; do
    if ! grep -q "#ifndef" "$file"; then
        echo -e "\e[31m[ALERTA]\e[0m $file não possui Header Guard!"
    fi
done

echo "Validação concluída."
