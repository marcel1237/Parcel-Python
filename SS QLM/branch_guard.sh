#!/bin/bash
###############################################################################
# NOME: branch_guard.sh
# DESCRIÇÃO: Protege branches críticas (como main ou master) contra ações
#            destrutivas ou comandos acidentais realizados no ambiente de dev.
#
# LÓGICA: Verifica o nome da branch atual via Git antes de prosseguir.
###############################################################################

PROTECTED_BRANCHES=("main" "master" "production")
current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "not-git")

for branch in "${PROTECTED_BRANCHES[@]}"; do
    if [ "$current_branch" == "$branch" ]; then
        echo -e "\e[41m ATENÇÃO: VOCÊ ESTÁ NA BRANCH PROTEGIDA: $current_branch \e[0m"
        echo "Cuidado com comandos de deleção, force-push ou alteração de banco!"
        exit 0
    fi
done

echo "Ambiente seguro. Branch atual: $current_branch"
