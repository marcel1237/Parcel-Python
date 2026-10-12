#!/usr/bin/env bash
set -Eeuo pipefail

echo "========================================="
echo " Project Wizard - Etapa 20.0"
echo " Migração: Eclipse JDT ➡ JetBrains (PSI)"
echo "========================================="

# 1. Validar ambiente
if [ ! -f pom.xml ]; then
    echo "Erro: Execute na raiz do ProjectWizard."
    exit 1
fi

echo "[1/4] Removendo Eclipse JDT e configurando JetBrains no pom.xml..."
python3 <<'PY'
import xml.etree.ElementTree as ET
from pathlib import Path

path = Path("pom.xml")
ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")
tree = ET.parse(path)
root = tree.getroot()
ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

# 1. Adicionar Repositório JetBrains
repositories = root.find('m:repositories', ns)
if repositories is None:
    repositories = ET.SubElement(root, 'repositories')

jb_repo_id = "jetbrains-repository"
if not any(r.find('m:id', ns).text == jb_repo_id for r in repositories.findall('m:repository', ns)):
    repo = ET.SubElement(repositories, 'repository')
    ET.SubElement(repo, 'id').text = jb_repo_id
    ET.SubElement(repo, 'url').text = "https://www.jetbrains.com/intellij-repository/releases"
    print("✔ Repositório JetBrains adicionado.")

# 2. Gerenciar Dependências
deps = root.find('m:dependencies', ns)
for dep in list(deps):
    art_id = dep.find('m:artifactId', ns).text
    # Remove Eclipse JDT Core
    if art_id == 'org.eclipse.jdt.core':
        deps.remove(dep)
        print("✔ Dependência Eclipse JDT removida.")

# Adiciona o Monólito do IntelliJ (ideaIC) para análise PSI [2, 4]
if not any(d.find('m:artifactId', ns).text == 'ideaIC' for d in deps.findall('m:dependency', ns)):
    new_dep = ET.SubElement(deps, 'dependency')
    ET.SubElement(new_dep, 'groupId').text = 'com.jetbrains.intellij.idea'
    ET.SubElement(new_dep, 'artifactId').text = 'ideaIC'
    ET.SubElement(new_dep, 'version').text = '2024.1.6'
    ET.SubElement(new_dep, 'scope').text = 'compile'
    print("✔ Dependência ideaIC (JetBrains) adicionada.")

tree.write(path, encoding='utf-8', xml_declaration=True)
PY

echo "[2/4] Removendo scanner antigo do Eclipse..."
rm -f src/main/java/com/projectwizard/service/editor/JavaTokenScanner.java

echo "[3/4] Criando novo JetBrainsSyntaxScanner.java..."
# Utiliza o Lexer do IntelliJ para uma tokenização mais precisa que a do JDT [1]
cat > src/main/java/com/projectwizard/service/editor/JetBrainsSyntaxScanner.java <<'EOF'
package com.projectwizard.service.editor;

import com.intellij.lang.java.lexer.JavaLexer;
import com.intellij.pom.java.LanguageLevel;
import com.intellij.psi.JavaTokenType;
import com.intellij.psi.tree.IElementType;

public class JetBrainsSyntaxScanner {
    private final JavaLexer lexer = new JavaLexer(LanguageLevel.JDK_21);

    public void tokenize(String source, TokenHandler handler) {
        if (source == null || source.isEmpty()) return;
        
        lexer.start(source);
        
        while (lexer.getTokenType() != null) {
            IElementType type = lexer.getTokenType();
            int start = lexer.getTokenStart();
            int end = lexer.getTokenEnd();
            
            String styleClass = mapTypeToStyle(type);
            handler.onToken(styleClass, start, end);
            
            lexer.advance();
        }
    }

    private String mapTypeToStyle(IElementType type) {
        if (JavaTokenType.KEYWORD_SET.contains(type)) return "token-keyword";
        if (type == JavaTokenType.STRING_LITERAL) return "token-string";
        if (JavaTokenType.COMMENT_SET.contains(type)) return "token-comment";
        if (type == JavaTokenType.IDENTIFIER) return "token-identifier";
        return "token-default";
    }

    public interface TokenHandler {
        void onToken(String type, int start, int end);
    }
}
EOF

echo "[4/4] Atualizando EditorPane para usar JetBrains..."
python3 <<'PY'
from pathlib import Path
p = Path("src/main/java/com/projectwizard/view/editor/EditorPane.java")
if p.exists():
    txt = p.read_text()
    # Substitui a classe do scanner
    txt = txt.replace("JavaTokenScanner", "JetBrainsSyntaxScanner")
    txt = txt.replace("new JavaTokenScanner()", "new JetBrainsSyntaxScanner()")
    p.write_text(txt)
    print("✔ EditorPane atualizado para o motor JetBrains.")
PY

echo "========================================="
echo " 🎉 ETAPA 20.0 CONCLUÍDA!"
echo "========================================="
echo "Alterações:"
echo "✔ Eclipse JDT removido do projeto."
echo "✔ IntelliJ ideaIC integrado via Maven [4]."
echo "✔ Novo Scanner baseado em JavaLexer (JetBrains)."
echo "========================================="
echo "🚀 Execute: mvn clean compile"