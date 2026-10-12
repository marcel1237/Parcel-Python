#!/bin/bash
###############################################################################
# NOME: check_hardcoded_keys.sh
# DESCRIÇÃO: Scanner de segurança preventivo que procura por segredos expostos
#            (Hardcoded Secrets) no código fonte.
#
# O QUE PROCURA:
#   - Chaves de API do Google (Cloud/Maps).
#   - Chaves da OpenAI (ChatGPT).
#   - Padrões comuns de senhas e tokens.
###############################################################################

echo "🔎 Iniciando varredura de segurança em busca de segredos..."

# Regex para chaves comuns
patterns=(
    "AIza[0-9A-Za-z-_]{35}"     # Google API Keys
    "sk-[a-zA-Z0-9]{48}"         # OpenAI Keys
    "api_key\s*[:=]\s*['\"].*['\"]" # Chaves genéricas
    "password\s*[:=]\s*['\"].*['\"]" # Senhas genéricas
)

found=0
for p in "${patterns[@]}"; do
    if grep -rnE "$p" . --exclude-dir={build,.git,templates} --exclude="*.db" --color=always; then
        found=1
    fi
done

if [ $found -eq 1 ]; then
    echo -e "\e[31m[PERIGO]\e[0m Foram encontrados possíveis segredos no código! Remova-os antes de dar commit."
else
    echo -e "\e[32m[SEGURO]\e[0m Nenhum segredo óbvio foi detectado."
fi
