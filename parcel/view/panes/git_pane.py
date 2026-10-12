from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton
from parcel.service.git_service import GitService

class GitPane(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_path = ""
        layout = QVBoxLayout(self)

        self.lbl_branch = QLabel("<b>Branch:</b> None", self)
        layout.addWidget(self.lbl_branch)

        btn_refresh = QPushButton("Refresh Status", self)
        btn_refresh.clicked.connect(self.refresh)
        layout.addWidget(btn_refresh)

        self.status_out = QPlainTextEdit(self)
        self.status_out.setReadOnly(True)
        layout.addWidget(self.status_out)

    def set_project_path(self, path: str):
        self.project_path = path
        self.refresh()

    def refresh(self):
        if not self.project_path:
            return
        git = GitService(self.project_path)
        if git.is_repository():
            branch = git.get_current_branch()
            status = git.get_status()
            self.lbl_branch.setText(f"<b>Branch:</b> {branch}")
            self.status_out.setPlainText(status or "Repository is clean.")
        else:
            self.lbl_branch.setText("<b>Branch:</b> Not a Git Repository")
            self.status_out.setPlainText("")
