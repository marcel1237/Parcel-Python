#!/usr/bin/env bash
###############################################################################
# NOME: run.sh
# DESCRIÇÃO: Script para iniciar o Parcel-Python na raiz do projeto.
###############################################################################
set -euo pipefail

if [ ! -d "venv" ]; then
    echo "Ambiente virtual não encontrado. Rodando build.sh..."
    ./build.sh
fi

echo "🚀 Iniciando Parcel-Python..."
exec ./venv/bin/python -m parcel.main "$@"
