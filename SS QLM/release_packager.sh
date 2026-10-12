#!/bin/bash
###############################################################################
# NOME: release_packager.sh
# DESCRIÇÃO: Automatiza o processo de compilação em modo Release e empacotamento
#            do projeto para distribuição final.
#
# FUNCIONAMENTO:
#   1. Limpa a pasta build.
#   2. Roda o CMake com otimizações de Release.
#   3. Compila usando todos os núcleos do processador (nproc).
#   4. Gera um arquivo .tar.gz contendo apenas o essencial.
###############################################################################

VERSION=${1:-"v1.0.0"}
PROJECT_NAME="ParcelCPP"
OUT_NAME="${PROJECT_NAME}_${VERSION}_linux_x64.tar.gz"

echo "Preparando Release $VERSION..."

# Compilação limpa
rm -rf build/*
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
cd ..

# Empacotamento
echo "Empacotando binários e recursos..."
tar -czf "$OUT_NAME" \
    --exclude="build" \
    --exclude=".git" \
    --exclude=".parcel_backups.db" \
    --exclude="templates" \
    .

echo "--- RELEASE CONCLUÍDA ---"
echo "Arquivo gerado: $OUT_NAME"
