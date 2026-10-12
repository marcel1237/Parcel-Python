#!/bin/bash
###############################################################################
# NOME: todo_scanner.sh
# DESCRIÇÃO: Varre o código fonte em busca de marcações técnicas (TODO, FIXME, HACK)
#            que indicam dívidas técnicas ou tarefas pendentes.
#
# FINALIDADE: Ajuda o desenvolvedor a não esquecer partes do código que precisam
#             de refatoração ou finalização.
#
# LÓGICA:
#   Utiliza 'grep' recursivo ignorando pastas irrelevantes como .git e build.
###############################################################################

echo "--- BUSCANDO TAREFAS PENDENTES (TODO/FIXME) ---"

# Procura por padrões de comentários técnicos
grep -rnE "TODO|FIXME|HACK" . \
    --exclude-dir={build,.git,templates,resource} \
    --color=always || echo "Nenhuma tarefa pendente encontrada. Bom trabalho!"

echo "----------------------------------------------"
