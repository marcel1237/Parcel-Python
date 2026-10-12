#!/bin/bash
###############################################################################
# NOME: project_scaffold.sh
# DESCRIÇÃO: Cria automaticamente a estrutura de diretórios padrão para um 
#            novo projeto C++ moderno seguindo as convenções da comunidade.
#
# POR QUE USAR: Poupa tempo de configuração manual e garante que todos os seus
#              projetos tenham a mesma organização lógica.
#
# ESTRUTURA CRIADA:
#   - src/ (Implementação .cpp)
#   - include/ (Cabeçalhos .hpp)
#   - tests/ (Testes Unitários)
#   - build/ (Arquivos de compilação)
#   - resource/ (Ativos como ícones e bancos de dados)
#   - docs/ (Documentação Markdown/Doxygen)
###############################################################################

PROJECT_NAME=${1:-"NewProject"}

echo "Iniciando Scaffold para o projeto: $PROJECT_NAME"

mkdir -p "$PROJECT_NAME"/{src,include,tests,build,resource,docs}
touch "$PROJECT_NAME"/README.md

# Gera um CMakeLists.txt básico
cat << 'CMAKE' > "$PROJECT_NAME"/CMakeLists.txt
cmake_minimum_required(VERSION 3.16)
project($PROJECT_NAME LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)
add_executable(${PROJECT_NAME} src/main.cpp)
CMAKE

echo "Sucesso! Estrutura de pastas e CMakeLists.txt criados em ./$PROJECT_NAME"
