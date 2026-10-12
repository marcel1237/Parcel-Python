from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QTabWidget, QLabel
from PyQt6.QtCore import Qt
from parcel.view.explorer.package_explorer import PackageExplorer
from parcel.view.explorer.dbms_explorer import DBMSExplorer
from parcel.view.editor.editor_host import EditorHost
from parcel.view.editor.designer_pane import DesignerPane
from parcel.view.panes.gemini_pane import GeminiPane
from parcel.view.panes.openai_pane import OpenAIPane
from parcel.view.panes.database_pane import DatabasePane
from parcel.view.panes.inspection_pane import InspectionPane
from parcel.view.panes.terminal_pane import TerminalPane
from parcel.view.panes.logcat_pane import LogcatPane
from parcel.view.panes.shell_scripting_pane import ShellScriptingPane
from parcel.view.panes.git_pane import GitPane
from parcel.view.panes.ssai_console_pane import SSAIConsolePane
from parcel.service.backup import BackupService

class ProjectWorkspace(QWidget):
    def __init__(self, project_path: str, parent=None):
        super().__init__(parent)
        self.project_path = project_path

        BackupService.get_instance().init(project_path)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header bar
        header = QLabel(f" 📂 Project: <b>{project_path}</b>", self)
        header.setStyleSheet("background-color: #161925; color: #4285f4; padding: 6px; font-size: 13px; border-bottom: 1px solid #1a1d2d;")
        layout.addWidget(header)

        main_splitter = QSplitter(Qt.Orientation.Horizontal, self)

        # Left Explorer Tabs
        left_tabs = QTabWidget(self)
        self.package_explorer = PackageExplorer(self)
        self.package_explorer.set_root_path(project_path)
        self.package_explorer.fileSelected.connect(self.on_file_selected)

        self.dbms_explorer = DBMSExplorer(project_path, self)

        left_tabs.addTab(self.package_explorer, "Files")
        left_tabs.addTab(self.dbms_explorer, "DBMS")

        # Central Editor Host & Designer
        self.editor_host = EditorHost(self)
        self.editor_host.set_project_path(project_path)

        self.designer_pane = DesignerPane(self)

        center_tabs = QTabWidget(self)
        center_tabs.addTab(self.editor_host, "Code Editor")
        center_tabs.addTab(self.designer_pane, "QML Blueprint Designer")

        # Right Assistant Tabs
        right_tabs = QTabWidget(self)
        self.ssai_console = SSAIConsolePane(project_path, self)
        self.gemini_pane = GeminiPane(self)
        self.openai_pane = OpenAIPane(self)
        self.git_pane = GitPane(self)
        self.git_pane.set_project_path(project_path)
        self.shell_pane = ShellScriptingPane(self)
        self.db_pane = DatabasePane(self)
        self.inspection_pane = InspectionPane(self)
        self.terminal_pane = TerminalPane(self)
        self.logcat_pane = LogcatPane(self)

        right_tabs.addTab(self.ssai_console, "SS AI Agent")
        right_tabs.addTab(self.gemini_pane, "Gemini")
        right_tabs.addTab(self.openai_pane, "OpenAI")
        right_tabs.addTab(self.shell_pane, "Shell Scripting")
        right_tabs.addTab(self.git_pane, "Git")
        right_tabs.addTab(self.db_pane, "Database")
        right_tabs.addTab(self.inspection_pane, "Inspection")
        right_tabs.addTab(self.terminal_pane, "Terminal")
        right_tabs.addTab(self.logcat_pane, "Logcat")

        main_splitter.addWidget(left_tabs)
        main_splitter.addWidget(center_tabs)
        main_splitter.addWidget(right_tabs)

        main_splitter.setSizes([250, 700, 350])

        layout.addWidget(main_splitter)

    def on_file_selected(self, file_path: str):
        self.editor_host.open_file(file_path)
