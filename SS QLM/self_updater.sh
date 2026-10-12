#!/bin/bash
###############################################################################
# NOME: self_updater.sh
# DESCRIÇÃO: Script que puxa as últimas alterações do repositório remoto (Git),
#            reinstala dependências se necessário e recompila o projeto.
#
# POR QUE USAR: Manter sua instância de desenvolvimento sempre atualizada com
#              um único comando, garantindo que você não trabalhe em código defasado.
###############################################################################

echo "🔄 Iniciando auto-atualização do projeto..."

# 1. Pull do Git
if git pull; then
    echo "Código atualizado com sucesso."
else
    echo "Erro ao sincronizar com o repositório remoto."
    exit 1
fi

# 2. Re-Build
echo "Iniciando compilação da nova versão..."
./build/build.sh

if [ $? -eq 0 ]; then
    echo "✅ Projeto atualizado e compilado com sucesso!"
else
    echo "❌ Falha na compilação da nova versão."
    exit 1
fi
