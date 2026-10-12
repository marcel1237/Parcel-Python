import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, QLabel

class TerminalPane(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Integrated Terminal</b>"))

        self.output = QPlainTextEdit(self)
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Enter shell command...")
        self.input.returnPressed.connect(self.execute_cmd)
        layout.addWidget(self.input)

    def execute_cmd(self):
        cmd = self.input.text().strip()
        if not cmd:
            return

        self.output.appendPlainText(f"$ {cmd}")
        self.input.clear()

        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            if res.stdout:
                self.output.appendPlainText(res.stdout)
            if res.stderr:
                self.output.appendPlainText(res.stderr)
        except Exception as e:
            self.output.appendPlainText(f"Error: {str(e)}")
