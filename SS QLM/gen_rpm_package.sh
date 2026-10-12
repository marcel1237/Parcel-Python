#!/bin/bash
###############################################################################
# NOME: gen_rpm_package.sh
# DESCRIÇÃO: Automatiza a criação de um pacote .rpm para distribuições baseadas
#            em Red Hat (Fedora, RHEL, CentOS).
#
# POR QUE USAR: Expandir a compatibilidade do Parcel C++ para ecossistemas 
#              empresariais além do Ubuntu/Debian.
#
# REQUISITOS: Necessita do pacote 'rpm-build' instalado.
#
# LÓGICA:
#   1. Cria a estrutura de pastas RPM (BUILD, RPMS, SOURCES, SPECS, SRPMS).
#   2. Gera dinamicamente um arquivo .spec com as instruções de instalação.
#   3. Utiliza 'rpmbuild' para gerar o pacote final.
###############################################################################

PROJECT_NAME="parcel-cpp"
VERSION="1.0.0"
RPM_ROOT="$HOME/rpmbuild"

echo "📦 Iniciando construção do pacote .rpm..."

# Garante estrutura do rpmbuild
mkdir -p "$RPM_ROOT"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Gera o arquivo SPEC
cat << SPEC > "$RPM_ROOT/SPECS/${PROJECT_NAME}.spec"
Name:           ${PROJECT_NAME}
Version:        ${VERSION}
Release:        1%{?dist}
Summary:        Parcel C++ IDE - Ambiente de desenvolvimento moderno com IA.
License:        MIT
URL:            https://github.com/voce/parcel-cpp

%description
Uma IDE profissional construída em C++ e Qt 6 com integração nativa de IA e Banco de Dados.

%install
mkdir -p %{buildroot}/usr/bin
cp "$(pwd)/build/Parcel C++/Parcel C++" %{buildroot}/usr/bin/parcel-cpp

%files
/usr/bin/parcel-cpp

%changelog
* $(date +"%a %b %d %Y") Seu Nome <voce@exemplo.com> - 1.0.0
- Versão inicial do pacote RPM.
SPEC

# Constrói o pacote
rpmbuild -ba "$RPM_ROOT/SPECS/${PROJECT_NAME}.spec"

echo "✅ Sucesso! Pacote RPM gerado em: $RPM_ROOT/RPMS/x86_64/"
