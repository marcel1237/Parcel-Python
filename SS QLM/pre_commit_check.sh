#!/bin/bash
###############################################################################
# NOME: pre_commit_check.sh
# DESCRIÇÃO: Um script de guarda que roda os testes fundamentais antes de você
#            poder dar um commit.
#
# LÓGICA:
#   1. Roda o linter (ShellCheck ou Clang-Tidy).
#   2. Roda a inspeção de sintaxe local.
#   3. Verifica se o projeto compila.
###############################################################################

echo "🏃 Iniciando verificações pré-commit..."

# 1. Checa Syntax Bash
./templates/shell/todo_scanner.sh

# 2. Checa Secret Keys
./templates/shell/check_hardcoded_keys.sh

# 3. Tenta compilar (Syntax-only)
g++ -fsyntax-only ./src/main.cpp -I./src 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "\e[32m[PASSOU]\e[0m O projeto está estável."
else
    echo -e "\e[31m[FALHOU]\e[0m Corrija os erros de compilação antes do commit."
    exit 1
fi
