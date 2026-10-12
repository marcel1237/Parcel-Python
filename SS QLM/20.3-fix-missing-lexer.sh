#!/usr/bin/env bash
set -Eeuo pipefail

echo "========================================="
echo " Project Wizard - Etapa 20.3"
echo " Correção de Dependências: Java Lexer Impl"
echo "========================================="

# 1. Validar ambiente
if [ ! -f pom.xml ]; then
    echo "Erro: Execute na raiz do ProjectWizard."
    exit 1
fi

echo "[1/2] Adicionando implementações PSI e Analysis no pom.xml..."
python3 <<'PY'
import xml.etree.ElementTree as ET
from pathlib import Path

path = Path("pom.xml")
ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")
tree = ET.parse(path)
root = tree.getroot()
ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

deps = root.find('m:dependencies', ns)

# Lista de dependências necessárias para o Lexer e PSI Java funcionar standalone
# Versão baseada no build 241 (IntelliJ 2024.1)
build_ver = '241.14494.240'
required_deps = [
    ('com.jetbrains.intellij.java', 'java-psi-impl', build_ver),
    ('com.jetbrains.intellij.java', 'java-analysis-impl', build_ver),
    ('com.jetbrains.intellij.platform', 'analysis-impl', build_ver),
    ('com.jetbrains.intellij.platform', 'core-impl', build_ver)
]

for g, a, v in required_deps:
    if not any(d.find('m:artifactId', ns).text == a for d in deps.findall('m:dependency', ns)):
        new_dep = ET.SubElement(deps, 'dependency')
        ET.SubElement(new_dep, 'groupId').text = g
        ET.SubElement(new_dep, 'artifactId').text = a
        ET.SubElement(new_dep, 'version').text = v
        print(f"✔ Adicionado: {a}")

tree.write(path, encoding='utf-8', xml_declaration=True)
PY

echo "[2/2] Recompilando com atualização de dependências..."
# -U garante que o Maven busque as novas implementações sem usar cache de erro
mvn clean compile -U

echo "========================================="
echo " 🎉 ETAPA 20.3 CONCLUÍDA!"
echo "========================================="
echo "Correções:"
echo "✔ Adicionado 'java-psi-impl' (Contém o JavaLexer)."
echo "✔ Adicionado 'core-impl' e 'analysis-impl'."
echo "========================================="
echo "🚀 Execute: mvn javafx:run"