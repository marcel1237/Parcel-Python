from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel

class GeminiPane(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Gemini 1.5 Pro AI Assistant</b>"))

        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)
        self.chat_history.append("✨ <b>Gemini AI:</b> Olá! Como posso ajudar na desenvolvimento do projeto hoje?")

        layout.addWidget(self.chat_history)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Pergunte ao Gemini AI...")
        self.input_field.returnPressed.connect(self.send_query)

        btn_send = QPushButton("Enviar", self)
        btn_send.clicked.connect(self.send_query)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(btn_send)

        layout.addLayout(input_layout)

    def send_query(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self.chat_history.append(f"<br><b>Você:</b> {text}")
        self.input_field.clear()
        self.chat_history.append("✨ <b>Gemini AI:</b> [Processando requisição no modelo Gemini 1.5 Pro...]")
