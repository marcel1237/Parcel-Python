from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QSplitter, QListWidget, QLineEdit, QComboBox, QFormLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont

class DesignerCanvas(QWidget):
    elementMoved = pyqtSignal(int, int, int)  # index, x, y
    elementSelected = pyqtSignal(int)         # index

    def __init__(self, parent=None):
        super().__init__(parent)
        self.elements = []
        self.selected_index = -1
        self.dragging = False
        self.drag_offset = QPoint()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("background-color: #161925; border: 1px solid #2b2d30;")

    def set_elements(self, elements, selected_index):
        self.elements = elements
        self.selected_index = selected_index
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            clicked_idx = -1
            for i in range(len(self.elements) - 1, -1, -1):
                e = self.elements[i]
                rect = QRect(e["x"], e["y"], e["width"], e["height"])
                if rect.contains(pos):
                    clicked_idx = i
                    break
            
            if clicked_idx != -1:
                self.selected_index = clicked_idx
                self.dragging = True
                e = self.elements[clicked_idx]
                self.drag_offset = pos - QPoint(e["x"], e["y"])
                self.elementSelected.emit(clicked_idx)
                self.update()
            else:
                self.selected_index = -1
                self.elementSelected.emit(-1)
                self.update()

    def mouseMoveEvent(self, event):
        if self.dragging and 0 <= self.selected_index < len(self.elements):
            new_pos = event.pos() - self.drag_offset
            new_x = max(0, new_pos.x())
            new_y = max(0, new_pos.y())
            self.elements[self.selected_index]["x"] = new_x
            self.elements[self.selected_index]["y"] = new_y
            self.elementMoved.emit(self.selected_index, new_x, new_y)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw grid background
        painter.setPen(QPen(QColor(40, 44, 52), 1, Qt.PenStyle.DotLine))
        for x in range(0, self.width(), 20):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 20):
            painter.drawLine(0, y, self.width(), y)

        # Draw elements
        for i, e in enumerate(self.elements):
            rx, ry, rw, rh = e["x"], e["y"], e["width"], e["height"]
            color = QColor(e.get("color", "#4285F4"))

            painter.setBrush(QBrush(color))
            if i == self.selected_index:
                painter.setPen(QPen(QColor("#FFD43B"), 3))
            else:
                painter.setPen(QPen(QColor("#ffffff"), 1))

            painter.drawRoundedRect(rx, ry, rw, rh, 6, 6)

            painter.setPen(QPen(QColor("#ffffff")))
            painter.setFont(QFont("Sans Serif", 9, QFont.Weight.Bold))
            painter.drawText(QRect(rx + 5, ry + 5, rw - 10, rh - 10), Qt.AlignmentFlag.AlignCenter, f"{e['type']}: {e['id']}")


class DesignerPane(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.elements = [
            {"id": "btn1", "type": "Button", "text": "Parcel Cyber Button", "x": 50, "y": 50, "width": 160, "height": 40, "color": "#4285F4"},
            {"id": "lbl1", "type": "Label", "text": "Industrial Blueprint", "x": 50, "y": 120, "width": 200, "height": 30, "color": "#ffffff"}
        ]
        self.selected_index = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        splitter = QSplitter(Qt.Orientation.Horizontal, self)

        # 1. Component Palette (Left)
        palette_widget = QWidget(self)
        p_layout = QVBoxLayout(palette_widget)
        p_layout.setContentsMargins(2, 2, 2, 2)
        p_layout.setSpacing(4)
        p_layout.addWidget(QLabel("<b>🎨 QML Palette</b>"))

        components = [
            "Button", "Label", "TextField", "TextEdit", "TextArea",
            "CheckBox", "RadioButton", "Switch", "Slider", "ProgressBar", "Dial",
            "Rectangle", "Item", "RowLayout", "ColumnLayout", "GridLayout",
            "ScrollView", "Pane", "GroupBox", "TabBar",
            "ListView", "GridView", "TableView", "ComboBox", "SpinBox", "Tumbler",
            "ToolButton", "RoundButton", "StackView", "Drawer", "Dialog",
            "Popup", "BusyIndicator", "DelayButton", "SwipeView"
        ]
        self.palette_list = QListWidget(self)
        self.palette_list.addItems(components)
        p_layout.addWidget(self.palette_list)

        btn_add = QPushButton("➕ Add", self)
        btn_add.setStyleSheet("background-color: #34A853; color: white; font-weight: bold;")
        btn_add.clicked.connect(self.add_component)
        p_layout.addWidget(btn_add)

        # 2. Interactive Canvas (Center)
        center_widget = QWidget(self)
        c_layout = QVBoxLayout(center_widget)
        c_layout.setContentsMargins(2, 2, 2, 2)
        c_layout.setSpacing(4)
        
        lbl_canvas = QLabel("📐 Canvas (Drag to move X, Y)")
        lbl_canvas.setStyleSheet("font-size: 11px; color: #888;")
        c_layout.addWidget(lbl_canvas)

        self.canvas = DesignerCanvas(self)
        self.canvas.elementMoved.connect(self.on_element_moved)
        self.canvas.elementSelected.connect(self.on_canvas_selected)
        c_layout.addWidget(self.canvas)

        btn_del = QPushButton("🗑️ Remove Selected", self)
        btn_del.setStyleSheet("background-color: #EA4335; color: white;")
        btn_del.clicked.connect(self.remove_component)
        c_layout.addWidget(btn_del)

        # 3. Inspector & QML Code Generator (Right)
        right_widget = QWidget(self)
        r_layout = QVBoxLayout(right_widget)
        r_layout.setContentsMargins(2, 2, 2, 2)
        r_layout.setSpacing(4)

        r_layout.addWidget(QLabel("<b>⚙️ Inspector</b>"))
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setVerticalSpacing(4)
        
        self.txt_id = QLineEdit(self)
        self.txt_text = QLineEdit(self)
        self.txt_color = QLineEdit(self)
        self.txt_width = QLineEdit(self)
        self.txt_height = QLineEdit(self)
        self.txt_x = QLineEdit(self)
        self.txt_y = QLineEdit(self)

        self.txt_id.textChanged.connect(self.update_property)
        self.txt_text.textChanged.connect(self.update_property)
        self.txt_color.textChanged.connect(self.update_property)
        self.txt_width.textChanged.connect(self.update_property)
        self.txt_height.textChanged.connect(self.update_property)
        self.txt_x.textChanged.connect(self.update_property)
        self.txt_y.textChanged.connect(self.update_property)

        self.form_layout.addRow("ID:", self.txt_id)
        self.form_layout.addRow("Text:", self.txt_text)
        self.form_layout.addRow("Color:", self.txt_color)
        self.form_layout.addRow("X:", self.txt_x)
        self.form_layout.addRow("Y:", self.txt_y)
        self.form_layout.addRow("Width:", self.txt_width)
        self.form_layout.addRow("Height:", self.txt_height)

        r_layout.addLayout(self.form_layout)

        r_layout.addWidget(QLabel("<b>💻 QML Code</b>"))
        self.qml_code_edit = QTextEdit(self)
        r_layout.addWidget(self.qml_code_edit)

        splitter.addWidget(palette_widget)
        splitter.addWidget(center_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([180, 560, 320])

        layout.addWidget(splitter)
        self.refresh_ui()

    def refresh_ui(self):
        self.canvas.set_elements(self.elements, self.selected_index)

        if 0 <= self.selected_index < len(self.elements):
            e = self.elements[self.selected_index]
            for widget in [self.txt_id, self.txt_text, self.txt_color, self.txt_width, self.txt_height, self.txt_x, self.txt_y]:
                widget.blockSignals(True)

            self.txt_id.setText(e["id"])
            self.txt_text.setText(e["text"])
            self.txt_color.setText(e["color"])
            self.txt_width.setText(str(e["width"]))
            self.txt_height.setText(str(e["height"]))
            self.txt_x.setText(str(e["x"]))
            self.txt_y.setText(str(e["y"]))

            for widget in [self.txt_id, self.txt_text, self.txt_color, self.txt_width, self.txt_height, self.txt_x, self.txt_y]:
                widget.blockSignals(False)

        self.generate_qml()

    def on_canvas_selected(self, index: int):
        self.selected_index = index
        self.refresh_ui()

    def on_element_moved(self, index: int, x: int, y: int):
        self.selected_index = index
        self.txt_x.blockSignals(True)
        self.txt_y.blockSignals(True)
        self.txt_x.setText(str(x))
        self.txt_y.setText(str(y))
        self.txt_x.blockSignals(False)
        self.txt_y.blockSignals(False)
        self.generate_qml()

    def add_component(self):
        item = self.palette_list.currentItem()
        comp_type = item.text() if item else "Button"
        idx = len(self.elements) + 1
        new_elem = {
            "id": f"comp{idx}",
            "type": comp_type,
            "text": f"New {comp_type}",
            "x": 50 + (idx * 20),
            "y": 50 + (idx * 30),
            "width": 160,
            "height": 40,
            "color": "#4285F4"
        }
        self.elements.append(new_elem)
        self.selected_index = len(self.elements) - 1
        self.refresh_ui()

    def remove_component(self):
        if 0 <= self.selected_index < len(self.elements):
            self.elements.pop(self.selected_index)
            self.selected_index = max(0, self.selected_index - 1)
            self.refresh_ui()

    def update_property(self):
        if 0 <= self.selected_index < len(self.elements):
            e = self.elements[self.selected_index]
            e["id"] = self.txt_id.text()
            e["text"] = self.txt_text.text()
            e["color"] = self.txt_color.text()
            try:
                e["x"] = int(self.txt_x.text())
            except Exception:
                pass
            try:
                e["y"] = int(self.txt_y.text())
            except Exception:
                pass
            try:
                e["width"] = int(self.txt_width.text())
            except Exception:
                pass
            try:
                e["height"] = int(self.txt_height.text())
            except Exception:
                pass
            self.canvas.update()
            self.generate_qml()

    def generate_qml(self):
        code = "import QtQuick 2.15\nimport QtQuick.Controls 2.15\nimport org.kde.kirigami 2.20 as Kirigami\n\nRectangle {\n    width: 800\n    height: 600\n    color: \"#161925\"\n\n"
        for e in self.elements:
            t = e["type"]
            code += f"    {t} {{\n        id: {e['id']}\n        x: {e['x']}; y: {e['y']}\n        width: {e['width']}; height: {e['height']}\n"
            if "text" in e and t in ["Button", "Label", "TextField", "TextEdit", "TextArea", "CheckBox", "RadioButton", "Switch", "GroupBox", "ToolButton", "RoundButton", "Dialog", "Popup", "DelayButton"]:
                code += f"        text: \"{e['text']}\"\n"
            if "color" in e:
                code += f"        color: \"{e['color']}\"\n"
            code += "    }\n\n"
        code += "}\n"
        self.qml_code_edit.setPlainText(code)
