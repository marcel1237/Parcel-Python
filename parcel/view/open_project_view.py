import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit
from parcel.core.navigation import NavigationController, NavigationTarget
from parcel.service.git_service import GitService

class OpenProjectView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        title = QLabel("Open Project", self)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        layout.addWidget(title)

        path_layout = QHBoxLayout()
        self.path_field = QLineEdit(self)
        self.path_field.setPlaceholderText("Choose a project folder...")
        self.path_field.setReadOnly(True)

        browse_btn = QPushButton("Browse...", self)
        path_layout.addWidget(self.path_field)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        self.info_area = QTextEdit(self)
        self.info_area.setReadOnly(True)
        self.info_area.setPlaceholderText("Choose a folder to continue.")
        layout.addWidget(self.info_area)

        button_layout = QHBoxLayout()
        self.open_btn = QPushButton("Open", self)
        self.open_btn.setEnabled(False)
        self.open_btn.setStyleSheet("background-color: #34A853; color: white; font-weight: bold; padding: 6px 15px; border-radius: 4px;")

        cancel_btn = QPushButton("Cancel", self)

        button_layout.addWidget(self.open_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        browse_btn.clicked.connect(self.handle_browse)
        self.open_btn.clicked.connect(self.handle_open)
        cancel_btn.clicked.connect(self.handle_cancel)

    def handle_browse(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Open Project Folder", "")
        if dir_path:
            self.selected_path = dir_path
            self.path_field.setText(dir_path)
            self.analyze_project(dir_path)
            self.open_btn.setEnabled(True)

    def analyze_project(self, path: str):
        report = f"<b>🔍 Análise do Projeto</b><br><br><b>Caminho:</b> {path}<br>"
        git = GitService(path)
        if git.is_repository():
            report += f"<b>🌿 Repositório Git:</b> Ativo<br><b>🔀 Branch Atual:</b> {git.get_current_branch()}<br>"
        else:
            report += "<b>🌿 Repositório Git:</b> Não detectado<br>"

        file_count = 0
        total_size = 0
        for root, dirs, files in os.walk(path):
            if "build" in root or ".git" in root or "__pycache__" in root:
                continue
            for f in files:
                file_count += 1
                try:
                    total_size += os.path.getsize(os.path.join(root, f))
                except Exception:
                    pass

        report += f"<b>📂 Estatísticas:</b> {file_count} arquivos ({total_size / 1024:.2f} KB)<br>"
        report += "<br>🚀 <i>Clique em 'Open' para carregar o Workspace.</i>"
        self.info_area.setHtml(report)

    def handle_open(self):
        if hasattr(self, "selected_path") and self.selected_path:
            NavigationController.get_instance().navigate_to(NavigationTarget.WORKSPACE, self.selected_path)

    def handle_cancel(self):
        self.path_field.clear()
        self.selected_path = ""
        self.info_area.clear()
        self.open_btn.setEnabled(False)
