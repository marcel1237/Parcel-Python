from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel

class OpenAIPane(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>OpenAI GPT-4o Assistant</b>"))

        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)
        self.chat_history.append("🟢 <b>GPT-4o:</b> OpenAI Assistant ready for deep reasoning.")

        layout.addWidget(self.chat_history)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Message GPT-4o...")
        self.input_field.returnPressed.connect(self.send_query)

        btn_send = QPushButton("Send", self)
        btn_send.clicked.connect(self.send_query)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(btn_send)

        layout.addLayout(input_layout)

    def send_query(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self.chat_history.append(f"<br><b>User:</b> {text}")
        self.input_field.clear()
        self.chat_history.append("🟢 <b>GPT-4o:</b> [Processing reasoning via OpenAI API...]")
