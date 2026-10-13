import re
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression

class ProjectHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # ----------------------------------------------------
        # 1. Python & C/C++ (.py, .cpp, .hpp, .c, .h, .cc)
        # ----------------------------------------------------
        cpp_py_format = QTextCharFormat()
        cpp_py_format.setForeground(QColor("#C678DD"))
        cpp_py_format.setFontWeight(QFont.Weight.Bold)
        cpp_py_keywords = [
            "class", "def", "fun", "val", "var", "import", "from", "return",
            "if", "else", "for", "while", "in", "try", "except", "catch",
            "include", "namespace", "public", "private", "protected", "void", "int", "bool",
            "true", "false", "None", "nullptr", "this", "self"
        ]
        for word in cpp_py_keywords:
            self.highlighting_rules.append((QRegularExpression(rf"\b{word}\b"), cpp_py_format))

        # ----------------------------------------------------
        # 2. JavaScript / TypeScript (.js, .ts, .jsx, .tsx, .mjs, .cjs)
        # ----------------------------------------------------
        js_ts_format = QTextCharFormat()
        js_ts_format.setForeground(QColor("#E5C07B"))
        js_ts_format.setFontWeight(QFont.Weight.Bold)
        js_ts_keywords = [
            "const", "let", "var", "function", "return", "import", "export",
            "default", "class", "extends", "constructor", "if", "else", "switch",
            "case", "for", "while", "do", "try", "catch", "finally", "async",
            "await", "new", "typeof", "instanceof", "interface", "type", "enum",
            "implements", "public", "private", "protected", "readonly", "undefined"
        ]
        for word in js_ts_keywords:
            self.highlighting_rules.append((QRegularExpression(rf"\b{word}\b"), js_ts_format))

        # ----------------------------------------------------
        # 3. Golang (.go)
        # ----------------------------------------------------
        go_format = QTextCharFormat()
        go_format.setForeground(QColor("#56B6C2"))
        go_format.setFontWeight(QFont.Weight.Bold)
        go_keywords = [
            "package", "import", "func", "return", "var", "const", "type",
            "struct", "interface", "map", "chan", "go", "select", "switch",
            "case", "default", "if", "else", "for", "range", "break",
            "continue", "fallthrough", "defer", "error", "nil"
        ]
        for word in go_keywords:
            self.highlighting_rules.append((QRegularExpression(rf"\b{word}\b"), go_format))

        # ----------------------------------------------------
        # 4. Rust (.rs)
        # ----------------------------------------------------
        rust_format = QTextCharFormat()
        rust_format.setForeground(QColor("#D19A66"))
        rust_format.setFontWeight(QFont.Weight.Bold)
        rust_keywords = [
            "fn", "let", "mut", "pub", "use", "mod", "struct", "enum",
            "impl", "trait", "match", "if", "else", "for", "while", "loop",
            "return", "where", "async", "await", "move", "ref", "self",
            "super", "crate", "Option", "Result", "String", "i32", "u32", "f64"
        ]
        for word in rust_keywords:
            self.highlighting_rules.append((QRegularExpression(rf"\b{word}\b"), rust_format))

        # ----------------------------------------------------
        # 5. PHP (.php)
        # ----------------------------------------------------
        php_format = QTextCharFormat()
        php_format.setForeground(QColor("#C678DD"))
        php_format.setFontWeight(QFont.Weight.Bold)
        php_keywords = [
            "php", "echo", "function", "class", "public", "private", "protected",
            "static", "namespace", "use", "return", "if", "else", "foreach",
            "as", "array", "new", "abstract", "interface", "trait", "extends", "implements"
        ]
        for word in php_keywords:
            self.highlighting_rules.append((QRegularExpression(rf"\b{word}\b", QRegularExpression.PatternOption.CaseInsensitiveOption), php_format))

        # PHP Variables ($variable)
        php_var_format = QTextCharFormat()
        php_var_format.setForeground(QColor("#E06C75"))
        self.highlighting_rules.append((QRegularExpression(r"\$[a-zA-Z_][a-zA-Z0-9_]*"), php_var_format))

        # ----------------------------------------------------
        # 6. Java & Kotlin / Groovy (.java, .groovy, .kt)
        # ----------------------------------------------------
        java_format = QTextCharFormat()
        java_format.setForeground(QColor("#E5C07B"))
        java_format.setFontWeight(QFont.Weight.Bold)
        java_keywords = [
            "package", "interface", "enum", "extends", "implements", "override",
            "static", "final", "throws", "finally", "new", "String", "Boolean",
            "Integer", "Double", "Float", "Long", "synchronized", "volatile",
            "transient", "native", "strictfp", "abstract", "default"
        ]
        for word in java_keywords:
            self.highlighting_rules.append((QRegularExpression(rf"\b{word}\b"), java_format))

        # ----------------------------------------------------
        # 7. Microsoft .NET Framework Languages (.cs, .vb, .fs)
        # ----------------------------------------------------
        dotnet_format = QTextCharFormat()
        dotnet_format.setForeground(QColor("#61AFEF"))
        dotnet_format.setFontWeight(QFont.Weight.Bold)
        dotnet_keywords = [
            "using", "namespace", "struct", "internal", "readonly", "async", "await",
            "foreach", "decimal", "object", "dynamic", "event", "delegate", "get", "set",
            "add", "remove", "where", "yield", "partial", "extern",
            "Module", "Sub", "Function", "Dim", "As", "Inherits", "End",
            "let", "rec", "open", "type", "member", "match", "with", "mutable"
        ]
        for word in dotnet_keywords:
            self.highlighting_rules.append((QRegularExpression(rf"\b{word}\b"), dotnet_format))

        # ----------------------------------------------------
        # 8. Ruby, Swift, Dart (.rb, .swift, .dart)
        # ----------------------------------------------------
        other_lang_format = QTextCharFormat()
        other_lang_format.setForeground(QColor("#98C379"))
        other_lang_format.setFontWeight(QFont.Weight.Bold)
        other_keywords = [
            "module", "require", "include", "attr_accessor", "elsif", "end", "yield",
            "guard", "protocol", "extension", "external", "dynamic",
            "final", "late", "required", "covariant", "factory", "get", "set"
        ]
        for word in other_keywords:
            self.highlighting_rules.append((QRegularExpression(rf"\b{word}\b"), other_lang_format))

        # ----------------------------------------------------
        # 9. Shell Script (.sh, .bash, .zsh)
        # ----------------------------------------------------
        shell_format = QTextCharFormat()
        shell_format.setForeground(QColor("#98C379"))
        shell_format.setFontWeight(QFont.Weight.Bold)
        shell_keywords = ["fi", "then", "elif", "do", "done", "case", "esac", "until", "echo", "export", "local", "readonly"]
        for word in shell_keywords:
            self.highlighting_rules.append((QRegularExpression(rf"\b{word}\b"), shell_format))

        # Shell Variables ($VAR, ${VAR})
        var_format = QTextCharFormat()
        var_format.setForeground(QColor("#E06C75"))
        self.highlighting_rules.append((QRegularExpression(r"\$[a-zA-Z_][a-zA-Z0-9_]*|\$\{[^\}]+\}"), var_format))

        # ----------------------------------------------------
        # 10. SQL (.sql)
        # ----------------------------------------------------
        sql_format = QTextCharFormat()
        sql_format.setForeground(QColor("#61AFEF"))
        sql_format.setFontWeight(QFont.Weight.Bold)
        sql_keywords = [
            "SELECT", "FROM", "WHERE", "INSERT", "INTO", "UPDATE", "DELETE",
            "CREATE", "TABLE", "DROP", "ALTER", "JOIN", "LEFT", "RIGHT", "INNER",
            "ON", "AND", "OR", "AS", "ORDER", "BY", "GROUP", "LIMIT", "OFFSET", "VALUES", "SET"
        ]
        for word in sql_keywords:
            self.highlighting_rules.append((QRegularExpression(rf"\b{word}\b", QRegularExpression.PatternOption.CaseInsensitiveOption), sql_format))

        # ----------------------------------------------------
        # 11. JSON Keys ("key":) (.json)
        # ----------------------------------------------------
        json_key_format = QTextCharFormat()
        json_key_format.setForeground(QColor("#E06C75"))
        json_key_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r'"([^"\\]|\\.)*"\s*:'), json_key_format))

        # ----------------------------------------------------
        # 12. YAML Keys (key:) (.yml, .yaml)
        # ----------------------------------------------------
        yaml_key_format = QTextCharFormat()
        yaml_key_format.setForeground(QColor("#E06C75"))
        yaml_key_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r"^[ \t]*[a-zA-Z0-9_-]+\s*:", QRegularExpression.PatternOption.MultilineOption), yaml_key_format))

        # ----------------------------------------------------
        # 13. HTML / XML / XAML / QML Tags & Attributes (.html, .xml, .xaml, .qml, .ui)
        # ----------------------------------------------------
        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor("#E06C75"))
        tag_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r"</?[a-zA-Z_:][-a-zA-Z0-9_:.]*"), tag_format))

        attr_format = QTextCharFormat()
        attr_format.setForeground(QColor("#D19A66"))
        self.highlighting_rules.append((QRegularExpression(r"\b[a-zA-Z_:][-a-zA-Z0-9_:.]*(?=\s*=\s*[\"'])"), attr_format))

        # ----------------------------------------------------
        # 14. Markdown Headers & Formatting (.md)
        # ----------------------------------------------------
        md_header_format = QTextCharFormat()
        md_header_format.setForeground(QColor("#61AFEF"))
        md_header_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r"^#{1,6}\s+.*$"), md_header_format))

        md_bold_format = QTextCharFormat()
        md_bold_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r"\*\*.*?\*\*"), md_bold_format))

        # ----------------------------------------------------
        # 15. Strings & Literals ("...", '...')
        # ----------------------------------------------------
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#98C379"))
        self.highlighting_rules.append((QRegularExpression(r'".*?"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'.*?'"), string_format))

        # ----------------------------------------------------
        # 16. Numbers & Booleans/Null
        # ----------------------------------------------------
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#D19A66"))
        self.highlighting_rules.append((QRegularExpression(r'\b-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?\b'), number_format))

        bool_null_format = QTextCharFormat()
        bool_null_format.setForeground(QColor("#56B6C2"))
        bool_null_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r'\b(true|false|null|nil|TRUE|FALSE|NULL|NIL)\b'), bool_null_format))

        # ----------------------------------------------------
        # 17. Comments (#..., //..., /*...*/, <!--...-->)
        # ----------------------------------------------------
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#5C6370"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r"#.*"), comment_format))
        self.highlighting_rules.append((QRegularExpression(r"//.*"), comment_format))
        self.highlighting_rules.append((QRegularExpression(r"/\*.*?\*/", QRegularExpression.PatternOption.DotMatchesEverythingOption), comment_format))
        self.highlighting_rules.append((QRegularExpression(r"<!--.*?-->", QRegularExpression.PatternOption.DotMatchesEverythingOption), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
