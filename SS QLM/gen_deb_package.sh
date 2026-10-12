#!/bin/bash
###############################################################################
# NOME: gen_deb_package.sh
# DESCRIÇÃO: Automatiza a criação de um pacote instalador .deb para sistemas
#            baseados em Debian/Ubuntu.
#
# POR QUE USAR: Facilitar a distribuição da IDE de forma profissional, 
#              permitindo a instalação via 'sudo apt install ./parcel-cpp.deb'.
#
# LÓGICA:
#   1. Cria uma estrutura de diretórios temporária seguindo o padrão Debian.
#   2. Copia o binário compilado e recursos.
#   3. Gera o arquivo 'control' com metadados do pacote.
#   4. Utiliza 'dpkg-deb' para construir o arquivo final.
###############################################################################

PROJECT_NAME="parcel-cpp"
VERSION="1.0.0"
BUILD_DIR="./build/Parcel C++"
DEB_ROOT="/tmp/${PROJECT_NAME}_deb"

echo "📦 Iniciando empacotamento .deb..."

# Limpa e cria estrutura
rm -rf "$DEB_ROOT"
mkdir -p "$DEB_ROOT/usr/bin"
mkdir -p "$DEB_ROOT/usr/share/applications"
mkdir -p "$DEB_ROOT/DEBIAN"

# Copia o binário (assume que o build já foi feito)
if [ -f "$BUILD_DIR/Parcel C++" ]; then
    cp "$BUILD_DIR/Parcel C++" "$DEB_ROOT/usr/bin/parcel-cpp"
else
    echo "Erro: Binário não encontrado em $BUILD_DIR. Compile o projeto primeiro."
    exit 1
fi

# Gera arquivo de controle
cat << CONTROL > "$DEB_ROOT/DEBIAN/control"
Package: $PROJECT_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Seu Nome <voce@exemplo.com>
Description: Parcel C++ IDE - Ambiente de desenvolvimento moderno com IA.
CONTROL

# Constrói o pacote
dpkg-deb --build "$DEB_ROOT" "./build/Parcel C++/${PROJECT_NAME}_${VERSION}.deb"

echo "✅ Sucesso! Instalador gerado em: ./build/Parcel C++/${PROJECT_NAME}_${VERSION}.deb"
