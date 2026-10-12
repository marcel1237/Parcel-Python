import re
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression

class ProjectHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # 1. Keywords (Python / C++)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#C678DD"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [
            "class", "def", "fun", "val", "var", "import", "from", "return",
            "if", "else", "for", "while", "in", "try", "except", "catch",
            "include", "namespace", "public", "private", "protected", "void", "int", "bool"
        ]
        for word in keywords:
            pattern = QRegularExpression(rf"\b{word}\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # 2. JSON Keys ("key":)
        json_key_format = QTextCharFormat()
        json_key_format.setForeground(QColor("#E06C75"))
        json_key_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r'"([^"\\]|\\.)*"\s*:'), json_key_format))

        # 3. Strings ("...", '...')
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#98C379"))
        self.highlighting_rules.append((QRegularExpression(r'".*?"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'.*?'"), string_format))

        # 4. JSON Numbers & Booleans/Null
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#D19A66"))
        self.highlighting_rules.append((QRegularExpression(r'\b-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?\b'), number_format))

        bool_null_format = QTextCharFormat()
        bool_null_format.setForeground(QColor("#56B6C2"))
        bool_null_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r'\b(true|false|null)\b'), bool_null_format))

        # 5. Comments (#..., //...)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#5C6370"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r"#.*"), comment_format))
        self.highlighting_rules.append((QRegularExpression(r"//.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
