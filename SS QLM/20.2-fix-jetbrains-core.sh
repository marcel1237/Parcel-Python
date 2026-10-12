#!/usr/bin/env bash
set -Eeuo pipefail

echo "========================================="
echo " Project Wizard - Etapa 20.2"
echo " Ajuste de Dependências: IntelliJ Core"
echo "========================================="

# 1. Validar ambiente
if [ ! -f pom.xml ]; then
    echo "Erro: Execute na raiz do ProjectWizard."
    exit 1
fi

echo "[1/3] Atualizando pom.xml para usar intellij-core (JAR)..."
python3 <<'PY'
import xml.etree.ElementTree as ET
from pathlib import Path

path = Path("pom.xml")
ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")
tree = ET.parse(path)
root = tree.getroot()
ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

deps = root.find('m:dependencies', ns)

# Remove a dependência ideaIC que falhou
for dep in list(deps):
    art_id = dep.find('m:artifactId', ns).text
    if art_id == 'ideaIC':
        deps.remove(dep)

# Adiciona intellij-core e suporte a Java (PSI)
# Essas versões são JARs nativos compatíveis com compilação Maven direta
dependencies = [
    ('com.jetbrains.intellij.platform', 'core', '241.14494.240'),
    ('com.jetbrains.intellij.java', 'java-psi', '241.14494.240')
]

for g, a, v in dependencies:
    if not any(d.find('m:artifactId', ns).text == a for d in deps.findall('m:dependency', ns)):
        new_dep = ET.SubElement(deps, 'dependency')
        ET.SubElement(new_dep, 'groupId').text = g
        ET.SubElement(new_dep, 'artifactId').text = a
        ET.SubElement(new_dep, 'version').text = v

tree.write(path, encoding='utf-8', xml_declaration=True)
print("✔ pom.xml atualizado com intellij-core e java-psi.")
PY

echo "[2/3] Limpando caches de erro do Maven..."
# Remove metadados de falha local para permitir novas tentativas
rm -rf ~/.m2/repository/com/jetbrains/intellij/idea/ideaIC

echo "[3/3] Recompilando com atualização forçada..."
mvn clean compile -U

echo "========================================="
echo " 🎉 ETAPA 20.2 CONCLUÍDA!"
echo "========================================="
echo "Mudança técnica:"
echo "Substituído o monólito 'ideaIC' por 'intellij-core'."
echo "Isso resolve o erro de 'Artifact Not Found' do JAR."
echo "========================================="
echo "🚀 Tente rodar: mvn javafx:run"