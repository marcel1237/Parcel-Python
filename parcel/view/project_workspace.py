import os
import sys
import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QTabWidget, QMessageBox, QMenu
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QIcon, QCursor
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
from parcel.service.export_service import ExportService

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
        self.header.exportRequested.connect(self.run_export)

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
        self.terminal_pane.output.appendPlainText("🔨 [Build + Backup] Iniciando backup incremental e build do projeto...")

        try:
            # 1. Perform SQLite Backup
            BackupService.get_instance().init(self.project_path)
            BackupService.get_instance().perform_build_backup("Automated build backup")
            self.terminal_pane.output.appendPlainText("✅ [Backup] Snapshot SQLite (.parcel_backups.db) realizado com sucesso.")

            # 2. Run Python Syntax Compilation Build Check
            self.terminal_pane.output.appendPlainText("⚙️ [Build] Verificando sintaxe e compilando arquivos do projeto...")
            
            py_files = []
            for root, dirs, files in os.walk(self.project_path):
                if "build" in root or ".git" in root or "venv" in root:
                    continue
                for f in files:
                    if f.endswith(".py"):
                        py_files.append(os.path.join(root, f))

            success = True
            for pf in py_files:
                res = subprocess.run([sys.executable, "-m", "py_compile", pf], capture_output=True, text=True)
                if res.returncode != 0:
                    success = False
                    self.terminal_pane.output.appendPlainText(f"❌ Erro de compilação em {pf}:\n{res.stderr}")
                else:
                    self.terminal_pane.output.appendPlainText(f"   ✓ Compilado: {os.path.basename(pf)}")

            if success:
                self.terminal_pane.output.appendPlainText("🎉 [Build + Backup] Build concluído com sucesso! 0 erros.")
                QMessageBox.information(self, "Build + Backup", "Build e Backup realizados com sucesso!")
            else:
                self.terminal_pane.output.appendPlainText("⚠️ [Build + Backup] Build concluído com avisos/erros.")
        except Exception as e:
            self.terminal_pane.output.appendPlainText(f"❌ Erro crítico no Build + Backup: {str(e)}")
            QMessageBox.critical(self, "Erro no Build", str(e))

    def run_export(self):
        export_menu = QMenu(self)
        export_menu.setStyleSheet("QMenu { background-color: #2b2d30; color: #bcbec4; } QMenu::item:selected { background-color: #8E44AD; }")

        deb_act = export_menu.addAction("📦 Debian Package (.deb)")
        tar_act = export_menu.addAction("📦 Release Archive (.tar.gz)")
        appimage_act = export_menu.addAction("📦 AppImage Structure (.AppDir)")

        selected = export_menu.exec(QCursor.pos())
        if not selected:
            return

        self.bottom_tabs.setVisible(True)
        self.bottom_tabs.setCurrentWidget(self.terminal_pane)
        self.terminal_pane.output.appendPlainText("Iniciando Exportação nativa em Python...")

        try:
            if selected == deb_act:
                out_path = ExportService.export_deb(self.project_path)
                self.terminal_pane.output.appendPlainText(f"✅ Pacote Debian gerado com sucesso em:\n{out_path}")
                QMessageBox.information(self, "Export Concluído", f"Pacote gerado em:\n{out_path}")
            elif selected == tar_act:
                out_path = ExportService.export_tarball(self.project_path)
                self.terminal_pane.output.appendPlainText(f"✅ Release Archive gerado com sucesso em:\n{out_path}")
                QMessageBox.information(self, "Export Concluído", f"Release gerada em:\n{out_path}")
            elif selected == appimage_act:
                out_path = ExportService.export_appimage(self.project_path)
                self.terminal_pane.output.appendPlainText(f"✅ AppImage Dir estruturado com sucesso em:\n{out_path}")
                QMessageBox.information(self, "Export Concluído", f"AppDir estruturado em:\n{out_path}")
        except Exception as e:
            self.terminal_pane.output.appendPlainText(f"❌ Erro na exportação: {str(e)}")
            QMessageBox.critical(self, "Erro na Exportação", str(e))
