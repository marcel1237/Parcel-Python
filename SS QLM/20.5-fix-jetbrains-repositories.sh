#!/usr/bin/env bash
set -Eeuo pipefail

echo "========================================="
echo " Project Wizard - Etapa 20.5"
echo " Resolvendo Dependências Transitivas JetBrains"
echo "========================================="

# 1. Validar ambiente
if [ ! -f pom.xml ]; then
    echo "Erro: Execute na raiz do ProjectWizard."
    exit 1
fi

echo "[1/2] Adicionando Repositórios Auxiliares (Thirdparty) no pom.xml..."
python3 <<'PY'
import xml.etree.ElementTree as ET
from pathlib import Path

path = Path("pom.xml")
ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")
tree = ET.parse(path)
root = tree.getroot()
ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

repositories = root.find('m:repositories', ns)
if repositories is None:
    repositories = ET.SubElement(root, 'repositories')

# Lista de repositórios vitais da JetBrains para o PSI Standalone
jb_repos = [
    ("jetbrains-releases", "https://cache-redirector.jetbrains.com/intellij-repository/releases"),
    ("jetbrains-thirdparty", "https://cache-redirector.jetbrains.com/intellij-repository/thirdparty"),
    ("jetbrains-dependencies", "https://cache-redirector.jetbrains.com/intellij-dependencies")
]

for repo_id, repo_url in jb_repos:
    if not any(r.find('m:id', ns).text == repo_id for r in repositories.findall('m:repository', ns)):
        repo = ET.SubElement(repositories, 'repository')
        ET.SubElement(repo, 'id').text = repo_id
        ET.SubElement(repo, 'url').text = repo_url
        print(f"✔ Repositório {repo_id} adicionado.")

tree.write(path, encoding='utf-8', xml_declaration=True)
PY

echo "[2/2] Limpando metadados de erro e forçando download..."
# Remove as pastas de erro do cache local para que o Maven tente os novos repositórios
rm -rf ~/.m2/repository/org/jetbrains/intellij/deps
rm -rf ~/.m2/repository/com/jetbrains/rd

# O sinalizador -U é fundamental aqui para ignorar falhas armazenadas em cache
mvn clean compile -U

echo "========================================="
echo " 🎉 ETAPA 20.5 CONCLUÍDA!"
echo "========================================="
echo "Novidades:"
echo "✔ Adicionado repositório 'thirdparty' (Onde reside o asm-all:9.5.3)."
echo "✔ Adicionado repositório 'dependencies' (Para componentes rd-core e rd-text)."
echo "✔ Cache local de erros limpo com sucesso."
echo "========================================="
echo "🚀 Execute: mvn javafx:run"