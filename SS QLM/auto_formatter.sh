#!/bin/bash
###############################################################################
# NOME: auto_formatter.sh
# DESCRIÇÃO: Aplica o 'clang-format' em massa em todos os arquivos de código
#            C++ do projeto para garantir um estilo visual consistente.
#
# REQUISITOS: clang-format instalado.
#
# LÓGICA:
#   Localiza todos os arquivos .cpp, .hpp e .h e aplica a formatação 'in-place' (-i).
###############################################################################

if ! command -v clang-format &> /dev/null; then
    echo "Erro: clang-format não instalado. Use: sudo apt install clang-format"
    exit 1
fi

echo "Formatando código fonte C++ recursivamente..."

find ./src ./include ./tests -type f \( -name "*.cpp" -o -name "*.hpp" -o -name "*.h" \) | while read -r file; do
    echo "Formatando: $file"
    clang-format -i "$file"
done

echo "Tudo pronto! Código formatado com sucesso."
