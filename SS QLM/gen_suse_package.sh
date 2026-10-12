#!/bin/bash
###############################################################################
# NOME: gen_suse_package.sh
# DESCRIÇÃO: Versão customizada do gerador RPM focada em padrões do OpenSUSE.
#
# POR QUE USAR: O OpenSUSE possui padrões rígidos de Build Service e metadados.
#              Este script prepara o ambiente para o OBS (Open Build Service).
#
# LÓGICA:
#   Semelhante ao RPM padrão, mas utiliza macros e categorias de desktop
#   específicas que o YaST e o Zypper preferem para indexação.
###############################################################################

PROJECT_NAME="parcel-cpp-suse"
VERSION="1.0.0"
SPEC_FILE="/tmp/${PROJECT_NAME}.spec"

echo "🦎 Preparando pacote especializado para OpenSUSE..."

cat << SPEC > "$SPEC_FILE"
# Documentação SUSE: https://en.opensuse.org/openSUSE:Packaging_guidelines
Name:           ${PROJECT_NAME}
Version:        ${VERSION}
Release:        0
Summary:        Parcel C++ IDE para openSUSE
License:        GPL-3.0-or-later
Group:          Development/Tools/IDE
BuildRequires:  cmake, gcc-c++, qt6-widgets-devel

%description
IDE Parcel C++ otimizada para o ecossistema openSUSE Tumbleweed/Leap.

%prep
# Preparação do fonte aqui

%build
# Macros do SUSE para CMake
%cmake
%cmake_build

%install
%cmake_install

%files
%{_bindir}/parcel-cpp
%doc README.md

%changelog
SPEC

echo "✅ Spec para SUSE gerada em: $SPEC_FILE"
echo "Para finalizar, envie este arquivo para o seu projeto no OBS (osc build)."
