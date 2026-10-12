from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from parcel.core.navigation import NavigationController, NavigationTarget
from parcel.service.persistence import PersistenceService

class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        title = QLabel("Configurações", self)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        main_layout.addWidget(title)

        gemini_box = QVBoxLayout()
        gemini_label = QLabel("Gemini API Key (Criptografada localmente):", self)
        gemini_label.setStyleSheet("font-size: 14px; color: #bbb;")
        gemini_box.addWidget(gemini_label)

        self.api_key_field = QLineEdit(self)
        self.api_key_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_field.setPlaceholderText("Insira sua API Key aqui...")
        self.api_key_field.setStyleSheet("background-color: #2b2d30; color: white; border: 1px solid #4e5157; border-radius: 4px; padding: 8px;")

        persistence = PersistenceService()
        current_key = persistence.get_gemini_api_key()
        if current_key:
            self.api_key_field.setText(current_key)

        gemini_box.addWidget(self.api_key_field)
        main_layout.addLayout(gemini_box)

        info_label = QLabel("Nota: Se deixado em branco, a IDE tentará ler do ambiente.", self)
        info_label.setStyleSheet("font-size: 11px; color: #888; font-style: italic;")
        main_layout.addWidget(info_label)

        main_layout.addStretch()

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Salvar Configurações", self)
        save_btn.setStyleSheet("background-color: #34A853; color: white; font-weight: bold; padding: 8px 20px; border-radius: 4px;")

        back_btn = QPushButton("Voltar", self)
        back_btn.setStyleSheet("background-color: #444; color: white; padding: 8px 20px; border-radius: 4px;")

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(back_btn)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        save_btn.clicked.connect(self.handle_save)
        back_btn.clicked.connect(lambda: NavigationController.get_instance().navigate_to(NavigationTarget.HOME))

    def handle_save(self):
        persistence = PersistenceService()
        persistence.save_gemini_api_key(self.api_key_field.text().strip())
        QMessageBox.information(self, "Sucesso", "Configurações salvas com sucesso!")
