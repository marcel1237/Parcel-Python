from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class BrowserPane(QWidget):
    def __init__(self, url: str, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.web_view = QWebEngineView(self)
        self.web_view.setUrl(QUrl(url))
        layout.addWidget(self.web_view)

    def load_url(self, url: str):
        self.web_view.setUrl(QUrl(url))
