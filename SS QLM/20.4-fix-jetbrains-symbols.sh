#!/usr/bin/env bash
set -Eeuo pipefail

echo "========================================="
echo " Project Wizard - Etapa 20.4"
echo " Correção de Símbolos JetBrains (PSI)"
echo "========================================="

# 1. Validar ambiente
if [ ! -f pom.xml ]; then
    echo "Erro: Execute na raiz do ProjectWizard."
    exit 1
fi

echo "[1/1] Reconstruindo JetBrainsSyntaxScanner.java com detecção robusta..."
cat > src/main/java/com/projectwizard/service/editor/JetBrainsSyntaxScanner.java <<'EOF'
package com.projectwizard.service.editor;

import com.intellij.lang.java.lexer.JavaLexer;
import com.intellij.pom.java.LanguageLevel;
import com.intellij.psi.JavaTokenType;
import com.intellij.psi.tree.IElementType;

/**
 * JetBrainsSyntaxScanner - Realce de sintaxe profissional usando o Lexer do IntelliJ.
 * Correção: Detecção baseada em tipos individuais para máxima compatibilidade stand-alone.
 */
public class JetBrainsSyntaxScanner {
    private final JavaLexer lexer = new JavaLexer(LanguageLevel.JDK_21);

    public void tokenize(String source, TokenHandler handler) {
        if (source == null || source.isEmpty()) return;
        
        // Inicializa o lexer com o código-fonte
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
        String typeName = type.toString();
        
        // Estratégia de detecção baseada em nomes de tokens do IntelliJ (mais estável no Maven)
        if (typeName.contains("KEYWORD")) return "token-keyword";
        if (typeName.contains("STRING_LITERAL") || typeName.contains("CHAR_LITERAL")) return "token-string";
        if (typeName.contains("COMMENT")) return "token-comment";
        
        // Casos específicos via JavaTokenType para identificadores e literais
        if (type == JavaTokenType.IDENTIFIER) return "token-identifier";
        
        return "token-default";
    }

    public interface TokenHandler {
        void onToken(String type, int start, int end);
    }
}
EOF

echo "========================================="
echo " 🎉 CORREÇÃO APLICADA!"
echo "========================================="
echo "A detecção agora utiliza 'type.toString().contains(\"KEYWORD\")',"
echo "o que evita a dependência de campos inexistentes no JAR da API."
echo "========================================="
echo "🚀 Execute: mvn clean compile"