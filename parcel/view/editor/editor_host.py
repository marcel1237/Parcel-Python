import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import pyqtSignal
from parcel.view.editor.editor_pane import EditorPane

class EditorHost(QWidget):
    requestAutonomousAI = pyqtSignal(str)
    requestGoogleUrl = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_path = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tab_pane = QTabWidget(self)
        self.tab_pane.setTabsClosable(True)
        self.tab_pane.tabCloseRequested.connect(self.close_tab)

        layout.addWidget(self.tab_pane)

    def set_project_path(self, path: str):
        self.project_path = path

    def open_file(self, file_path: str):
        if not file_path or not os.path.exists(file_path):
            return

        file_name = os.path.basename(file_path)

        for i in range(self.tab_pane.count()):
            if self.tab_pane.tabText(i) == file_name:
                self.tab_pane.setCurrentIndex(i)
                return

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            editor = EditorPane(file_path, content, self)
            idx = self.tab_pane.addTab(editor, file_name)
            self.tab_pane.setCurrentIndex(idx)
        except Exception:
            pass

    def close_tab(self, index: int):
        self.tab_pane.removeTab(index)
