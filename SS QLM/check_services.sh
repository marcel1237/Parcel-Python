#!/bin/bash
###############################################################################
# NOME: check_services.sh
# DESCRIÇÃO: Verifica se os serviços de infraestrutura (Banco de Dados, Redis,
#            Servidores Web) estão rodando localmente antes de iniciar a IDE.
#
# FINALIDADE: Evitar erros de conexão no "Database Inspector" ou "WebEngine"
#             devido a serviços offline.
#
# LÓGICA:
#   Utiliza 'systemctl' para serviços do sistema e 'nc' (netcat) para checar
#   portas abertas em serviços Docker ou remotos.
###############################################################################

SERVICES=("sqlite" "mongodb" "redis-server" "docker")
PORTS=(8080 6379 27017 5432)

echo "--- RELATÓRIO DE STATUS DE INFRAESTRUTURA ---"

for svc in "${SERVICES[@]}"; do
    if systemctl is-active --quiet "$svc"; then
        echo -e "\e[32m[ATIVO]\e[0m Serviço: $svc"
    else
        echo -e "\e[31m[OFFLINE]\e[0m Serviço: $svc"
    fi
done

echo "--- CHECAGEM DE PORTAS ---"
for port in "${PORTS[@]}"; do
    if timeout 0.1 bash -c "true < /dev/tcp/127.0.0.1/$port" &> /dev/null; then
        echo -e "\e[32m[OUVINDO]\e[0m Porta: $port"
    else
        echo -e "\e[33m[FECHADA]\e[0m Porta: $port"
    fi
done
