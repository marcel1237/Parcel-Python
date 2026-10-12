#!/bin/bash
###############################################################################
# NOME: valgrind_analyzer.sh
# DESCRIÇÃO: Executa o programa através do Valgrind para detectar vazamentos
#            de memória (Memory Leaks) e erros de perfil de execução.
#
# POR QUE USAR: Garantir que o Parcel C++ seja extremamente estável e não
#              consuma RAM desnecessariamente durante longas sessões de uso.
#
# FERRAMENTAS UTILIZADAS:
#   - Memcheck: Localiza erros de memória (Default).
#   - Massif: Analisa o uso de Heap ao longo do tempo (Opcional).
#
# LÓGICA:
#   O script verifica se o binário existe e o executa com flags de checagem
#   completa, gerando um log detalhado 'valgrind_report.txt'.
###############################################################################

BINARY="./build/Parcel C++/Parcel C++"

if [ ! -f "$BINARY" ]; then
    echo "Erro: Binário não encontrado. Compile o projeto primeiro."
    exit 1
fi

echo "🔍 Iniciando análise profunda com Valgrind (Memcheck)..."

valgrind --leak-check=full \
         --show-leak-kinds=all \
         --track-origins=yes \
         --verbose \
         --log-file=valgrind_report.txt \
         "$BINARY"

echo "✅ Análise concluída. Verifique os resultados em 'valgrind_report.txt'."
