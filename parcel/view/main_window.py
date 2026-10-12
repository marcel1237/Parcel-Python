import os
import os.path
from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
    QToolBar, QLabel, QFileDialog, QMenuBar, QMessageBox
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QTimer
from parcel.core.navigation import NavigationController, NavigationTarget
from parcel.view.dashboard_view import DashboardView
from parcel.view.new_project_view import NewProjectView
from parcel.view.open_project_view import OpenProjectView
from parcel.view.settings_view import SettingsView
from parcel.view.project_workspace import ProjectWorkspace
from parcel.service.persistence import PersistenceService

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1400, 850)
        self.setWindowTitle("Parcel-Python")

        self.setup_menus()
        self.setup_toolbar()

        central_widget = QWidget(self)
        v_layout = QVBoxLayout(central_widget)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)

        self.content_stack = QStackedWidget(self)

        self.dashboard_view = DashboardView(self)
        self.open_project_view = OpenProjectView(self)
        self.new_project_view = NewProjectView(self)
        self.settings_view = SettingsView(self)

        self.content_stack.addWidget(self.dashboard_view)   # 0
        self.content_stack.addWidget(self.open_project_view)# 1
        self.content_stack.addWidget(self.new_project_view) # 2
        self.content_stack.addWidget(self.settings_view)    # 3

        v_layout.addWidget(self.content_stack)

        status_widget = QWidget(self)
        status_widget.setFixedHeight(25)
        status_widget.setStyleSheet("background-color: #222; border-top: 1px solid #333; color: #888;")
        status_layout = QVBoxLayout(status_widget)
        status_layout.setContentsMargins(10, 0, 10, 0)
        status_label = QLabel("Ready | v1.0.0", status_widget)
        status_layout.addWidget(status_label)
        v_layout.addWidget(status_widget)

        self.setCentralWidget(central_widget)
        self.active_workspace = None

        self.setup_navigation()

        QTimer.singleShot(0, self.restore_session)

    def setup_menus(self):
        file_menu = self.menuBar().addMenu("&File")
        exit_action = file_menu.addAction("&Exit")
        exit_action.triggered.connect(self.close)

        help_menu = self.menuBar().addMenu("&Help")
        about_action = help_menu.addAction("&About")
        about_action.triggered.connect(lambda: QMessageBox.about(self, "About Parcel-Python", "Parcel-Python IDE\nAI-Driven Industrial Development Toolkit"))

    def setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(toolbar)

        new_action = toolbar.addAction("New Project")
        open_action = toolbar.addAction("Open")
        toolbar.addSeparator()
        settings_action = toolbar.addAction("Settings")

        new_action.triggered.connect(lambda: NavigationController.get_instance().navigate_to(NavigationTarget.NEW_PROJECT))
        open_action.triggered.connect(lambda: NavigationController.get_instance().navigate_to(NavigationTarget.OPEN_PROJECT))
        settings_action.triggered.connect(lambda: NavigationController.get_instance().navigate_to(NavigationTarget.SETTINGS))

    def setup_navigation(self):
        def on_navigate(target: NavigationTarget, path: str):
            if target == NavigationTarget.HOME:
                self.content_stack.setCurrentWidget(self.dashboard_view)
            elif target == NavigationTarget.NEW_PROJECT:
                self.content_stack.setCurrentWidget(self.new_project_view)
            elif target == NavigationTarget.OPEN_PROJECT:
                self.content_stack.setCurrentWidget(self.open_project_view)
            elif target == NavigationTarget.SETTINGS:
                self.content_stack.setCurrentWidget(self.settings_view)
            elif target == NavigationTarget.WORKSPACE:
                self.load_workspace(path)

        NavigationController.get_instance().set_on_navigate(on_navigate)

    def load_workspace(self, path: str):
        if not path:
            return

        PersistenceService().save_last_project(path)

        if self.active_workspace:
            self.content_stack.removeWidget(self.active_workspace)
            self.active_workspace.deleteLater()

        self.active_workspace = ProjectWorkspace(path, self)
        index = self.content_stack.addWidget(self.active_workspace)
        self.content_stack.setCurrentIndex(index)

    def restore_session(self):
        persistence = PersistenceService()
        last_project = persistence.get_last_project()
        if last_project and os.path.exists(last_project):
            NavigationController.get_instance().navigate_to(NavigationTarget.WORKSPACE, last_project)
