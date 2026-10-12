from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit
from PyQt6.QtCore import pyqtSignal
from parcel.view.editor.highlighter import ProjectHighlighter

class EditorPane(QWidget):
    requestBrowserUrl = pyqtSignal(str)
    requestGoogleUrl = pyqtSignal(str)

    def __init__(self, file_path: str = "", content: str = "", parent=None):
        super().__init__(parent)
        self.file_path = file_path

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setPlainText(content)

        self.highlighter = ProjectHighlighter(self.text_edit.document())
        layout.addWidget(self.text_edit)

    def get_content(self) -> str:
        return self.text_edit.toPlainText()

    def set_content(self, content: str):
        self.text_edit.setPlainText(content)
