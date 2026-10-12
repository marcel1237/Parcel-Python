#!/bin/bash
###############################################################################
# NOME: dependency_checker.sh
# DESCRIÇÃO: Valida se o ambiente de desenvolvimento possui todas as ferramentas
#            necessárias instaladas no PATH do sistema.
#
# POR QUE USAR: Fundamental para scripts de CI/CD ou para garantir que um novo
#              desenvolvedor consiga compilar o projeto sem erros de "command not found".
#
# LÓGICA:
#   Utiliza o comando 'command -v' que é o padrão POSIX mais eficiente para
#   verificar a existência de binários sem disparar execuções acidentais.
###############################################################################

REQUIRED_TOOLS=("git" "curl" "g++" "make" "cmake" "shellcheck")

echo "--- VERIFICANDO DEPENDÊNCIAS DO SISTEMA ---"

for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        echo -e "\e[31m[ERRO]\e[0m $tool não está instalado. Por favor, instale-o para prosseguir."
        exit 1
    else
        echo -e "\e[32m[OK]\e[0m $tool encontrado em: $(which $tool)"
    fi
done

echo "Sucesso: Todas as dependências foram atendidas."
