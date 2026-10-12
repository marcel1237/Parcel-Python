#!/usr/bin/env bash
###############################################################################
# NOME: build.sh
# DESCRIÇÃO: Script de build e configuração do ambiente para o Parcel-Python.
###############################################################################
set -euo pipefail

echo "=== Parcel-Python Build & Environment Setup ==="

# Garante python3 e venv
if ! command -v python3 &> /dev/null; then
    echo "Erro: python3 não encontrado."
    exit 1
fi

python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

mkdir -p build

echo "✅ Build concluído com sucesso! Para executar, rode ./run.sh ou bash build/run.sh"
