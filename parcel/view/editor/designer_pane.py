from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QSplitter
)
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, QVariant

class DesignerElement:
    def __init__(self, element_id: str, element_type: str, text: str = "Component"):
        self.id = element_id
        self.type = element_type
        self.x = 50
        self.y = 50
        self.width = 160
        self.height = 40
        self.text = text


class DesignerPane(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Horizontal, self)

        # Left Palette
        palette_widget = QWidget(self)
        p_layout = QVBoxLayout(palette_widget)
        p_layout.addWidget(QLabel("<b>QML Blueprint Elements</b>"))

        btn_button = QPushButton("+ Add Button", palette_widget)
        btn_label = QPushButton("+ Add Label", palette_widget)
        btn_text = QPushButton("+ Add TextField", palette_widget)

        p_layout.addWidget(btn_button)
        p_layout.addWidget(btn_label)
        p_layout.addWidget(btn_text)
        p_layout.addStretch()

        # Center Code Preview / Generated QML
        preview_widget = QWidget(self)
        c_layout = QVBoxLayout(preview_widget)
        c_layout.addWidget(QLabel("<b>Generated QML Code</b>"))

        self.qml_code_edit = QTextEdit(preview_widget)
        self.qml_code_edit.setPlainText("""import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    width: 600
    height: 400
    color: "#161925"

    Button {
        x: 50; y: 50
        text: "Parcel Cyber Button"
    }
}""")
        c_layout.addWidget(self.qml_code_edit)

        splitter.addWidget(palette_widget)
        splitter.addWidget(preview_widget)

        layout.addWidget(splitter)
