#!/bin/bash
###############################################################################
# NOME: project_vacuum.sh
# DESCRIÇÃO: "Limpeza Pesada" do projeto. Remove caches de build, arquivos temporários
#            da IDE, logs gigantes e restaura o projeto ao estado "puro" de código.
#
# POR QUE USAR: Útil antes de grandes refatorações ou para liberar espaço em disco.
#
# AÇÕES:
#   - Deleta pastas build/ e bin/
#   - Remove arquivos .log e arquivos temporários do editor (~).
#   - Limpa o banco de backups locais (Opcional).
###############################################################################

echo "☢️ Iniciando limpeza profunda do projeto..."

# Remove diretórios de compilação
rm -rf ./build/* ./bin/* ./*.o ./*.so

# Remove lixo do editor
find . -name "*~" -delete
find . -name "*.log" -delete

# Remove arquivos de cache do CMake
find . -name "CMakeCache.txt" -delete
find . -name "CMakeFiles" -type d -exec rm -rf {} +

echo "Limpeza concluída. O projeto está limpo para um novo build."
