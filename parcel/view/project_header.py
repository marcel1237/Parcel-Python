import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal
from parcel.service.git_service import GitService
from parcel.service.backup import BackupService

class ProjectHeader(QWidget):
    geminiToggled = pyqtSignal()
    browserToggled = pyqtSignal()
    designerToggled = pyqtSignal()
    buildRequested = pyqtSignal()
    exportRequested = pyqtSignal()

    def __init__(self, project_path: str, parent=None):
        super().__init__(parent)
        self.project_path = project_path
        self.git_service = GitService(project_path)

        base_name = os.path.basename(project_path)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 2, 15, 2)
        main_layout.setSpacing(15)
        self.setFixedHeight(45)
        self.setStyleSheet("background-color: #252525; border-bottom: 1px solid #333;")

        project_label = QLabel(f"📁 <b>{base_name}</b>", self)
        project_label.setStyleSheet("color: white; font-size: 13px;")
        main_layout.addWidget(project_label)

        if self.git_service.is_repository():
            branch = self.git_service.get_current_branch()
            git_badge = QLabel(f"🌿 Git: {branch}", self)
            git_badge.setStyleSheet("color: #4caf50; font-weight: bold; font-size: 11px;")
            main_layout.addWidget(git_badge)

        path_label = QLabel(f"📍 <small>{project_path}</small>", self)
        path_label.setStyleSheet("color: #666;")
        main_layout.addWidget(path_label)

        main_layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        button_layout.setContentsMargins(0, 0, 0, 0)

        gemini_btn = QPushButton("✨ East Pane", self)
        gemini_btn.setStyleSheet("background-color: #4285F4; color: white; border-radius: 4px; padding: 5px 12px; font-weight: bold; font-size: 11px;")
        button_layout.addWidget(gemini_btn)

        browser_btn = QPushButton("🌐 South Pane", self)
        browser_btn.setStyleSheet("background-color: #34A853; color: white; border-radius: 4px; padding: 5px 12px; font-weight: bold; font-size: 11px;")
        button_layout.addWidget(browser_btn)

        designer_btn = QPushButton("🎨 Designer", self)
        designer_btn.setStyleSheet("background-color: #E67E22; color: white; border-radius: 4px; padding: 5px 12px; font-weight: bold; font-size: 11px;")
        button_layout.addWidget(designer_btn)

        build_btn = QPushButton("🔨 Build + Backup", self)
        build_btn.setStyleSheet("background-color: #27ae60; color: white; border-radius: 4px; padding: 5px 12px; font-weight: bold; font-size: 11px;")
        button_layout.addWidget(build_btn)

        export_btn = QPushButton("📦 Export", self)
        export_btn.setStyleSheet("background-color: #8E44AD; color: white; border-radius: 4px; padding: 5px 12px; font-weight: bold; font-size: 11px;")
        button_layout.addWidget(export_btn)

        main_layout.addLayout(button_layout)

        gemini_btn.clicked.connect(self.geminiToggled)
        browser_btn.clicked.connect(self.browserToggled)
        designer_btn.clicked.connect(self.designerToggled)
        export_btn.clicked.connect(self.exportRequested)
        build_btn.clicked.connect(self.on_build_clicked)

    def on_build_clicked(self):
        BackupService.get_instance().init(self.project_path)
        BackupService.get_instance().perform_build_backup("Automated build backup")
        self.buildRequested.emit()
