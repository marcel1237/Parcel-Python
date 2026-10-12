from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLabel

class LogcatPane(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Logcat / Application Monitor</b>"))

        self.log_output = QPlainTextEdit(self)
        self.log_output.setReadOnly(True)
        self.log_output.setPlainText("""[INFO] Parcel-Python Initialized.
[INFO] Cyber-Dark Theme Applied successfully.
[INFO] QLM Engine loaded 26 JSON rule files.
[INFO] LocalAgent project symbol indexer ready.
""")
        layout.addWidget(self.log_output)
