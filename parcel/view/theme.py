from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class Theme:
    @staticmethod
    def apply_extraordinary_skin(app: QApplication):
        p = QPalette()
        dark_bg = QColor(15, 17, 26)
        surface_bg = QColor(22, 25, 37)
        accent_blue = QColor(66, 133, 244)
        neon_cyan = QColor(0, 191, 255)
        text_main = QColor(224, 224, 224)
        text_dim = QColor(136, 136, 136)

        p.setColor(QPalette.ColorRole.Window, dark_bg)
        p.setColor(QPalette.ColorRole.WindowText, text_main)
        p.setColor(QPalette.ColorRole.Base, surface_bg)
        p.setColor(QPalette.ColorRole.AlternateBase, dark_bg)
        p.setColor(QPalette.ColorRole.ToolTipBase, dark_bg)
        p.setColor(QPalette.ColorRole.ToolTipText, text_main)
        p.setColor(QPalette.ColorRole.Text, text_main)
        p.setColor(QPalette.ColorRole.Button, surface_bg)
        p.setColor(QPalette.ColorRole.ButtonText, text_main)
        p.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
        p.setColor(QPalette.ColorRole.Link, neon_cyan)
        p.setColor(QPalette.ColorRole.Highlight, accent_blue)
        p.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

        app.setPalette(p)

        # Apply fallback styling
        app.setStyleSheet("""
            QWidget {
                background-color: #0f111a;
                color: #e0e0e0;
                font-family: 'Segoe UI', 'Sans-Serif', sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #1a1d2d;
                background-color: #161925;
            }
            QTabBar::tab {
                background-color: #0f111a;
                color: #888888;
                padding: 8px 16px;
                border: 1px solid #1a1d2d;
            }
            QTabBar::tab:selected {
                background-color: #161925;
                color: #4285f4;
                border-bottom: 2px solid #4285f4;
            }
            QPushButton {
                background-color: #161925;
                border: 1px solid #4285f4;
                border-radius: 4px;
                padding: 6px 12px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #1e2238;
            }
            QTextEdit, QPlainTextEdit, QLineEdit {
                background-color: #161925;
                border: 1px solid #1a1d2d;
                color: #e0e0e0;
            }
        """)
