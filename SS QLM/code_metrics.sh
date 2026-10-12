#!/bin/bash
###############################################################################
# NOME: code_metrics.sh
# DESCRIÇÃO: Gera estatísticas sobre o volume de código do projeto, contando
#            linhas de código, comentários e espaços em branco.
#
# FINALIDADE: Útil para relatórios de progresso e para identificar arquivos
#             que estão ficando grandes demais (monolíticos).
#
# LÓGICA:
#   Filtra arquivos por extensões (.cpp, .hpp, .sh) e utiliza 'cloc' (se disponível)
#   ou um contador manual via 'wc -l'.
###############################################################################

echo "--- MÉTRICAS DE CÓDIGO DO PROJETO ---"

# Contagem simplificada usando ferramentas nativas
total_lines=$(find . -type f \( -name "*.cpp" -o -name "*.hpp" -o -name "*.sh" \) | xargs wc -l | tail -n 1)

echo "Resumo (Arquivos C++ e Shell):"
echo "$total_lines"

echo "Top 5 maiores arquivos do projeto:"
find . -type f \( -name "*.cpp" -o -name "*.hpp" \) -exec wc -l {} + | sort -rn | head -n 5
