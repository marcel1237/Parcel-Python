#!/bin/bash
###############################################################################
# NOME: api_health_check.sh
# DESCRIÇÃO: Realiza testes de latência e disponibilidade contra endpoints de API
#            que o seu software consome (ex: Gemini, Google, OpenAI).
#
# FINALIDADE: Diagnosticar se lentidões na IDE são causadas pela rede externa.
###############################################################################

ENDPOINTS=("https://generativelanguage.googleapis.com" "https://api.openai.com" "https://google.com")

echo "--- TESTANDO CONECTIVIDADE DE APIS ---"

for url in "${ENDPOINTS[@]}"; do
    start_time=$(date +%s%N)
    status=$(curl -o /dev/null -s -w "%{http_code}" "$url" --max-time 5 || echo "TIMEOUT")
    end_time=$(date +%s%N)
    
    latency=$(( (end_time - start_time) / 1000000 )) # ms

    if [[ "$status" == "200" || "$status" == "401" || "$status" == "404" ]]; then
        echo -e "\e[32m[ALCANÇÁVEL]\e[0m Endpoint: $url | Latência: ${latency}ms"
    else
        echo -e "\e[31m[ERRO]\e[0m Endpoint: $url | Status: $status"
    fi
done
