#!/bin/bash
###############################################################################
# NOME: find_duplicates.sh
# DESCRIÇÃO: Localiza blocos de código idênticos ou muito parecidos em arquivos
#            diferentes do projeto.
#
# POR QUE USAR: Identificar código que deve ser refatorado para uma função
#              comum ou classe base, reduzindo a complexidade do projeto.
#
# REQUISITOS: Utiliza uma técnica de 'fuzzy grep' ou 'md5sum' simplificado.
###############################################################################

echo "--- BUSCANDO POSSÍVEIS DUPLICAÇÕES DE CÓDIGO ---"

# Gera hashes de arquivos pequenos para comparar duplicidade total
find ./src -type f -name "*.cpp" -exec md5sum {} + | sort | uniq -w32 -dD

echo "Dica: Use a ferramenta 'cloc' ou 'cppcheck' para uma análise mais profunda."
