#!/bin/bash
###############################################################################
# NOME: env_diff_checker.sh
# DESCRIÇÃO: Compara seu arquivo .env local com o .env.example do projeto para
#            garantir que você não esqueceu de configurar nenhuma variável nova.
#
# FINALIDADE: Evitar erros de "Undefined Variable" em produção após atualizações.
###############################################################################

if [ ! -f .env ] || [ ! -f .env.example ]; then
    echo "Erro: Arquivos .env ou .env.example não encontrados na raiz."
    exit 1
fi

echo "--- COMPARANDO VARIÁVEIS DE AMBIENTE ---"

# Extrai chaves e compara
awk -F'=' '{print $1}' .env.example | sort > /tmp/env_keys_example
awk -F'=' '{print $1}' .env | sort > /tmp/env_keys_local

missing=$(comm -23 /tmp/env_keys_example /tmp/env_keys_local)

if [ -n "$missing" ]; then
    echo -e "\e[31m[ATENÇÃO]\e[0m As seguintes chaves estão faltando no seu .env:"
    echo "$missing"
else
    echo -e "\e[32m[OK]\e[0m Seu arquivo .env está sincronizado com o exemplo."
fi
