import os
from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
    QToolBar, QLabel, QPushButton, QFileDialog
)
from PyQt6.QtGui import QAction
from parcel.view.project_workspace import ProjectWorkspace
from parcel.service.persistence import PersistenceService

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1400, 850)

        self.setup_toolbar()

        central_widget = QWidget(self)
        v_layout = QVBoxLayout(central_widget)
        v_layout.setContentsMargins(0, 0, 0, 0)

        self.content_stack = QStackedWidget(self)

        # Welcome Dashboard View
        dashboard = QWidget(self)
        dash_layout = QVBoxLayout(dashboard)
        dash_layout.addWidget(QLabel("<h2>🚀 Welcome to Parcel-Python</h2><p>AI-Driven Industrial Development Toolkit</p>"))

        btn_open = QPushButton("Open Project Directory", dashboard)
        btn_open.clicked.connect(self.open_project)
        dash_layout.addWidget(btn_open)
        dash_layout.addStretch()

        self.content_stack.addWidget(dashboard)

        v_layout.addWidget(self.content_stack)

        # Statusbar
        status_bar = self.statusBar()
        status_bar.showMessage("Ready")

        self.setCentralWidget(central_widget)

        # Auto-restore last project
        ps = PersistenceService()
        last_proj = ps.get_last_project()
        if last_proj and os.path.exists(last_proj):
            self.load_workspace(last_proj)

    def setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(toolbar)

        act_open = QAction("Open Project", self)
        act_open.triggered.connect(self.open_project)
        toolbar.addAction(act_open)

    def open_project(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Open Project Folder")
        if dir_path:
            PersistenceService().save_last_project(dir_path)
            self.load_workspace(dir_path)

    def load_workspace(self, project_path: str):
        workspace = ProjectWorkspace(project_path, self)
        idx = self.content_stack.addWidget(workspace)
        self.content_stack.setCurrentIndex(idx)
        self.statusBar().showMessage(f"Workspace loaded: {project_path}")
