from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from parcel.ss_ai_agent.ssai_module import SSAIModule

class SSAIConsolePane(QWidget):
    def __init__(self, project_path: str = "", parent=None):
        super().__init__(parent)
        self.ssai = SSAIModule(project_path)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>SS AI Agent Console</b>"))

        self.console = QTextEdit(self)
        self.console.setReadOnly(True)
        self.console.append("🤖 <b>SS AI Agent:</b> On-Device Intelligence Console initialized.")

        layout.addWidget(self.console)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Comando para o agente SS AI (ex: onde está MainWindow?)...")
        self.input_field.returnPressed.connect(self.send_command)

        btn_send = QPushButton("Executar", self)
        btn_send.clicked.connect(self.send_command)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(btn_send)

        layout.addLayout(input_layout)

    def send_command(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self.console.append(f"<br><b>&gt;</b> {text}")
        self.input_field.clear()

        res = self.ssai.process_instruction(text)
        self.console.append(f"{res.message}")
