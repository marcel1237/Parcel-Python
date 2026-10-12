import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QTabWidget, QProcess, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from parcel.view.project_header import ProjectHeader
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
from parcel.view.panes.browser_pane import BrowserPane
from parcel.view.panes.versions_pane import VersionsPane
from parcel.view.panes.saves_pane import SavesPane
from parcel.service.backup import BackupService

class ProjectWorkspace(QWidget):
    def __init__(self, project_path: str, parent=None):
        super().__init__(parent)
        self.project_path = project_path

        BackupService.get_instance().init(project_path)

        v_layout = QVBoxLayout(self)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)

        # 1. Project Header with Action Buttons
        self.header = ProjectHeader(project_path, self)
        v_layout.addWidget(self.header)

        self.vertical_splitter = QSplitter(Qt.Orientation.Vertical, self)
        self.horizontal_splitter = QSplitter(Qt.Orientation.Horizontal, self)

        # 2. Explorer (Left Tabs)
        self.package_explorer = PackageExplorer(self)
        self.package_explorer.set_root_path(project_path)
        self.package_explorer.fileSelected.connect(self.on_file_selected)

        self.dbms_explorer = DBMSExplorer(project_path, self)

        left_tabs = QTabWidget(self)
        left_tabs.addTab(self.package_explorer, "Files")
        left_tabs.addTab(self.dbms_explorer, "DBMS")
        left_tabs.setStyleSheet("QTabWidget::pane { border: none; }")

        # 3. Editor Host & Designer Pane (Center)
        self.editor_host = EditorHost(self)
        self.editor_host.set_project_path(project_path)

        self.designer_pane = DesignerPane(self)
        self.designer_pane.setVisible(False)

        # 4. East Pane (Right Side Tabs: Gemini, OpenAI, Shell Scripting, Git)
        self.east_tabs = QTabWidget(self)
        self.gemini_pane = GeminiPane(self)
        self.openai_pane = OpenAIPane(self)
        self.shell_scripting_pane = ShellScriptingPane(self)
        self.git_pane = GitPane(self)
        self.git_pane.set_project_path(project_path)

        self.east_tabs.addTab(self.gemini_pane, "Gemini")
        self.east_tabs.addTab(self.openai_pane, "OpenAI")
        self.east_tabs.addTab(self.shell_scripting_pane, "Shell Scripting")
        self.east_tabs.addTab(self.git_pane, "Git")

        self.shell_scripting_pane.requestAIExplanation.connect(lambda script: (
            self.east_tabs.setVisible(True),
            self.east_tabs.setCurrentWidget(self.gemini_pane)
        ))

        self.horizontal_splitter.addWidget(left_tabs)
        self.horizontal_splitter.addWidget(self.editor_host)
        self.horizontal_splitter.addWidget(self.designer_pane)
        self.horizontal_splitter.addWidget(self.east_tabs)

        self.horizontal_splitter.setStretchFactor(0, 0)
        self.horizontal_splitter.setStretchFactor(1, 1)
        self.horizontal_splitter.setStretchFactor(2, 1)
        self.horizontal_splitter.setStretchFactor(3, 0)
        self.horizontal_splitter.setSizes([250, 750, 0, 400])

        # 5. South Pane (Bottom Tabs: Google, Duck.ai, Brave Leo, ChatGPT, ExplainShell, Terminal, SS AI Agent, Problemas, Banco de Dados, Logs, Versões, Saves)
        self.bottom_tabs = QTabWidget(self)
        self.bottom_tabs.setTabPosition(QTabWidget.TabPosition.South)
        self.bottom_tabs.setStyleSheet("QTabWidget::pane { border-top: 1px solid #333; }")

        self.google_pane = BrowserPane("https://www.google.com", self)
        self.duck_ai_pane = BrowserPane("https://duck.ai", self)
        self.brave_leo_pane = BrowserPane("https://search.brave.com/chat", self)
        self.chat_gpt_pane = BrowserPane("https://chatgpt.com", self)
        self.explainshell_pane = BrowserPane("https://explainshell.com", self)
        self.terminal_pane = TerminalPane(self)
        self.ss_ai_pane = SSAIConsolePane(project_path, self)
        self.inspection_pane = InspectionPane(self)
        self.database_pane = DatabasePane(self)
        self.logcat_pane = LogcatPane(self)
        self.versions_pane = VersionsPane(project_path, self)
        self.saves_pane = SavesPane(project_path, self)

        self.bottom_tabs.addTab(self.google_pane, "Google")
        self.bottom_tabs.addTab(self.duck_ai_pane, "Duck.ai")
        self.bottom_tabs.addTab(self.brave_leo_pane, "Brave Leo")
        self.bottom_tabs.addTab(self.chat_gpt_pane, "ChatGPT")
        self.bottom_tabs.addTab(self.explainshell_pane, "ExplainShell")
        self.bottom_tabs.addTab(self.terminal_pane, "Terminal")
        self.bottom_tabs.addTab(self.ss_ai_pane, "SS AI Agent")
        self.bottom_tabs.addTab(self.inspection_pane, "Problemas")
        self.bottom_tabs.addTab(self.database_pane, "Banco de Dados")
        self.bottom_tabs.addTab(self.logcat_pane, "Logs")
        self.bottom_tabs.addTab(self.versions_pane, "Versões")
        self.bottom_tabs.addTab(self.saves_pane, "Saves")

        self.bottom_tabs.setVisible(False)

        self.vertical_splitter.addWidget(self.horizontal_splitter)
        self.vertical_splitter.addWidget(self.bottom_tabs)
        self.vertical_splitter.setStretchFactor(0, 1)
        self.vertical_splitter.setStretchFactor(1, 0)

        v_layout.addWidget(self.vertical_splitter)

        # Header Button Signals & Slots
        self.header.geminiToggled.connect(lambda: self.east_tabs.setVisible(not self.east_tabs.isVisible()))
        self.header.browserToggled.connect(lambda: self.bottom_tabs.setVisible(not self.bottom_tabs.isVisible()))
        self.header.designerToggled.connect(self.toggle_designer)
        self.header.buildRequested.connect(self.run_build)
        self.header.exportRequested.connect(lambda: QMessageBox.information(self, "Export", "Project export and packaging package generated."))

    def on_file_selected(self, file_path: str):
        self.editor_host.open_file(file_path)

    def toggle_designer(self):
        visible = not self.designer_pane.isVisible()
        self.designer_pane.setVisible(visible)
        if visible:
            self.horizontal_splitter.setSizes([250, 0, 1000, 400])
        else:
            self.horizontal_splitter.setSizes([250, 1000, 0, 400])

    def run_build(self):
        self.bottom_tabs.setVisible(True)
        self.bottom_tabs.setCurrentWidget(self.terminal_pane)
        self.terminal_pane.output.appendPlainText("Iniciando Build + Backup do Projeto...")
