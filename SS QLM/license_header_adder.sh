#!/bin/bash
###############################################################################
# NOME: license_header_adder.sh
# DESCRIÇÃO: Adiciona automaticamente um cabeçalho de licença ou copyright em 
#            todos os arquivos .cpp, .hpp e .sh do projeto.
#
# POR QUE USAR: Manter a conformidade legal e profissional do código fonte
#              sem precisar editar arquivo por arquivo manualmente.
#
# COMO USAR: Edite a variável 'LICENSE' abaixo com seu texto.
###############################################################################

LICENSE="/* (C) $(date +%Y) Seu Nome/Empresa. Todos os direitos reservados. */"

echo "Aplicando cabeçalho de licença nos arquivos fonte..."

find ./src ./include -type f \( -name "*.cpp" -o -name "*.hpp" -o -name "*.h" \) | while read -r file; do
    if ! grep -q "Todos os direitos reservados" "$file"; then
        echo -e "$LICENSE\n$(cat "$file")" > "$file"
        echo "Atualizado: $file"
    fi
done

echo "Processo concluído."
