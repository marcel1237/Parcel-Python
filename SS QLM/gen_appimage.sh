#!/bin/bash
###############################################################################
# NOME: gen_appimage.sh
# DESCRIÇÃO: Automatiza a criação de um arquivo AppImage universal para o
#            Parcel C++. O AppImage permite que a IDE rode em praticamente 
#            qualquer distribuição Linux sem instalação.
#
# POR QUE USAR: É o formato de distribuição mais amigável para Linux. Um único
#              arquivo contém todas as bibliotecas e recursos necessários.
#
# REQUISITOS:
#   - appimagetool (baixar em appimage.github.io)
#   - Binário do Parcel C++ já compilado.
#
# LÓGICA:
#   1. Cria a estrutura AppDir (Pasta raiz do AppImage).
#   2. Copia o binário, ícones e arquivo .desktop.
#   3. Resolve dependências (opcionalmente via apprun).
#   4. Empacota tudo em um arquivo .AppImage.
###############################################################################

PROJECT_NAME="Parcel_CPP"
VERSION="1.0.0"
APPDIR="/tmp/${PROJECT_NAME}.AppDir"
BUILD_BIN="./build/Parcel C++/Parcel C++"
ICON_PATH="./resource/parcel-cpp-dark.png"

echo "🚀 Iniciando criação do AppImage..."

# Limpeza e Preparação
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

# 1. Copiar Binário
if [ -f "$BUILD_BIN" ]; then
    cp "$BUILD_BIN" "$APPDIR/usr/bin/parcel-cpp"
else
    echo "Erro: Binário não encontrado em $BUILD_BIN. Compile primeiro!"
    exit 1
fi

# 2. Copiar Ícone
if [ -f "$ICON_PATH" ]; then
    cp "$ICON_PATH" "$APPDIR/parcel-cpp.png"
    cp "$ICON_PATH" "$APPDIR/usr/share/icons/hicolor/256x256/apps/parcel-cpp.png"
else
    echo "Aviso: Ícone não encontrado. Usando ícone genérico."
fi

# 3. Gerar arquivo .desktop necessário para o AppImage
cat << DESKTOP > "$APPDIR/parcel-cpp.desktop"
[Desktop Entry]
Name=Parcel C++
Exec=parcel-cpp
Icon=parcel-cpp
Type=Application
Categories=Development;IDE;
Terminal=false
DESKTOP

# 4. Criar o AppRun (Script de entrada)
cat << 'APPRUN' > "$APPDIR/AppRun"
#!/bin/sh
HERE="$(dirname "$(readlink -f "${0}")")"
export PATH="${HERE}/usr/bin/:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib/:${LD_LIBRARY_PATH}"
exec parcel-cpp "$@"
APPRUN
chmod +x "$APPDIR/AppRun"

# 5. Gerar o arquivo final usando appimagetool
if command -v appimagetool > /dev/null; then
    appimagetool "$APPDIR" "./build/Parcel C++/${PROJECT_NAME}-${VERSION}-x86_64.AppImage"
    echo "✅ Sucesso! AppImage gerado na pasta build."
else
    echo "⚠️ appimagetool não encontrado no PATH."
    echo "A estrutura AppDir foi preparada em $APPDIR, mas o empacotamento falhou."
    echo "Baixe o appimagetool e execute: appimagetool $APPDIR"
fi
