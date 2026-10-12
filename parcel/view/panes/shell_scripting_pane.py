from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal

class ShellScriptingPane(QWidget):
    requestAIExplanation = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>SSQLM Shell Scripting Tool</b>"))

        self.editor = QTextEdit(self)
        self.editor.setPlainText("""#!/usr/bin/env bash
set -euo pipefail

echo "=== Parcel SSQLM Script Execution ==="
# Safe atomic temp dir creation
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "Temp dir created at $TMP_DIR"
""")
        layout.addWidget(self.editor)

        btn_explain = QPushButton("Request SS AI Explanation", self)
        btn_explain.clicked.connect(self.explain)
        layout.addWidget(btn_explain)

    def explain(self):
        script = self.editor.toPlainText()
        self.requestAIExplanation.emit(script)
