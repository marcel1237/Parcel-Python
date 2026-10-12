#!/usr/bin/env bash
set -Eeuo pipefail

echo "========================================="
echo " Project Wizard - Etapa 20.1"
echo " Corrigindo Resolução de Dependência JetBrains"
echo "========================================="

# 1. Validar ambiente
if [ ! -f pom.xml ]; then
    echo "Erro: Execute na raiz do ProjectWizard."
    exit 1
fi

echo "[1/2] Atualizando URL do repositório para o Redirector Oficial..."
# O redirecionador 'cache-redirector' é mais resiliente para downloads massivos como o ideaIC [1]
sed -i 's|https://www.jetbrains.com/intellij-repository/releases|https://cache-redirector.jetbrains.com/intellij-repository/releases|g' pom.xml

echo "[2/2] Forçando atualização de dependências e recompilando..."
# O sinalizador -U (force-update) limpa o cache de erro mencionado no log [Help 1]
mvn clean compile -U

echo "========================================="
echo " 🎉 CORREÇÃO APLICADA!"
echo "========================================="
echo "O comando 'mvn clean compile -U' forçou o Maven a"
echo "ignorar o erro em cache e tentar baixar o SDK novamente."
echo "========================================="
echo "🚀 Se o download for concluído, execute: mvn javafx:run"
