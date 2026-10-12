#!/bin/bash
###############################################################################
# NOME: env_guard.sh
# DESCRIÇÃO: Garante que variáveis de ambiente críticas (como GEMINI_API_KEY ou
#            DB_PASSWORD) estejam definidas antes de iniciar a IDE ou o build.
#
# FINALIDADE: Evitar falhas em tempo de execução causadas por chaves ausentes.
#
# COMO USAR: Execute este script antes de iniciar seu ambiente de desenvolvimento.
###############################################################################

CRITICAL_VARS=("GEMINI_API_KEY" "QT_QPA_PLATFORM" "PROJECT_ROOT")

echo "Verificando variáveis de ambiente críticas..."

missing=0
for var in "${CRITICAL_VARS[@]}"; do
    if [ -z "${!var+x}" ]; then
        echo -e "\e[33m[AVISO]\e[0m A variável $var não está definida no seu shell."
        missing=$((missing + 1))
    else
        echo -e "\e[32m[DEFINIDA]\e[0m $var está configurada."
    fi
done

if [ $missing -gt 0 ]; then
    echo "Total de $missing variáveis ausentes. Verifique seu arquivo .bashrc ou .env."
fi
