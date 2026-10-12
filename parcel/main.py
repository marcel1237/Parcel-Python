import os
import sys
# CRITICAL: QWebEngineView must be imported before QApplication is created
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QDir, QRect
from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QLinearGradient, QColor, QFont

def create_application_icon() -> QIcon:
    size = 512
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

    gradient = QLinearGradient(0, 0, size, size)
    gradient.setColorAt(0, QColor("#1a1a1a"))
    gradient.setColorAt(0.5, QColor("#050505"))
    gradient.setColorAt(1, QColor("#1a1a1a"))

    painter.setBrush(gradient)
    painter.setPen(QColor("#4285F4"))
    painter.drawRoundedRect(10, 10, size - 20, size - 20, int(size / 5), int(size / 5))

    font = QFont("Sans Serif", int(size / 3), QFont.Weight.Bold)
    painter.setFont(font)
    painter.setPen(QColor(66, 133, 244, 100))
    painter.drawText(QRect(4, 4, size, size), Qt.AlignmentFlag.AlignCenter, "PC")
    painter.setPen(QColor("#ffffff"))
    painter.drawText(QRect(0, 0, size, size), Qt.AlignmentFlag.AlignCenter, "PC")

    glass = QLinearGradient(0, 0, 0, int(size / 3))
    glass.setColorAt(0, QColor(66, 133, 244, 40))
    glass.setColorAt(1, QColor(66, 133, 244, 0))
    painter.setBrush(glass)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(15, 15, size - 30, int(size / 3), int(size / 5), int(size / 5))
    painter.end()

    home_icon_dir = os.path.expanduser("~/.local/share/icons")
    os.makedirs(home_icon_dir, exist_ok=True)
    pixmap.save(os.path.join(home_icon_dir, "parcel-cpp-dark.png"), "PNG")

    return QIcon(pixmap)


def main():
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--log-level=3 --enable-logging=none"

    if not os.environ.get("QT_QPA_PLATFORM"):
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    app.setApplicationName("Parcel-Python")
    app.setApplicationDisplayName("Parcel-Python")
    app.setOrganizationName("Parcel")
    app.setDesktopFileName("Parcel-Python")

    app_icon = create_application_icon()
    app.setWindowIcon(app_icon)

    from parcel.view.theme import Theme
    Theme.apply_extraordinary_skin(app)

    from parcel.view.main_window import MainWindow
    main_window = MainWindow()
    main_window.setWindowTitle("Parcel-Python")
    main_window.setWindowIcon(app_icon)
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
