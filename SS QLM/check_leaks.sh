#!/bin/bash
###############################################################################
# NOME: check_leaks.sh
# DESCRIÇÃO: Compila o projeto com a flag AddressSanitizer (ASan) habilitada
#            para detectar vazamentos de memória (Memory Leaks) e acessos inválidos.
#
# POR QUE USAR: Fundamental para garantir a estabilidade de aplicações C++.
###############################################################################

echo "Compilando com AddressSanitizer habilitado..."

mkdir -p build_debug && cd build_debug
cmake .. -DCMAKE_CXX_FLAGS="-fsanitize=address -g" -DCMAKE_EXE_LINKER_FLAGS="-fsanitize=address"
make -j$(nproc)

echo "--- EXECUÇÃO COM ANÁLISE DE MEMÓRIA ---"
echo "O programa será encerrado se um vazamento for detectado."
./Parcel\ C++ 
