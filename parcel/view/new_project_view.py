from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from parcel.core.navigation import NavigationController, NavigationTarget

class NewProjectView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)

        # Left Steps Panel
        steps_panel = QVBoxLayout()
        steps_panel.setSpacing(15)
        steps = ["① Project", "② Language", "③ Framework", "④ Dependencies", "⑤ Git", "⑥ Summary"]
        for step in steps:
            lbl = QLabel(step, self)
            lbl.setStyleSheet("font-size: 15px; padding: 8px; color: #bbb;")
            steps_panel.addWidget(lbl)
        steps_panel.addStretch()
        main_layout.addLayout(steps_panel, 1)

        # Center Form Panel
        center_layout = QVBoxLayout()
        title = QLabel("Create New Project", self)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 20px; color: white;")
        center_layout.addWidget(title)

        form_grid = QGridLayout()
        form_grid.setVerticalSpacing(15)
        form_grid.setHorizontalSpacing(10)

        form_grid.addWidget(QLabel("Project Name:", self), 0, 0)
        form_grid.addWidget(QLineEdit(self), 0, 1)

        form_grid.addWidget(QLabel("Group:", self), 1, 0)
        form_grid.addWidget(QLineEdit("com.example", self), 1, 1)

        form_grid.addWidget(QLabel("Artifact:", self), 2, 0)
        form_grid.addWidget(QLineEdit(self), 2, 1)

        form_grid.addWidget(QLabel("Language:", self), 3, 0)
        lang_combo = QComboBox(self)
        lang_combo.addItems(["Python", "C++", "Java", "Kotlin", "Groovy"])
        form_grid.addWidget(lang_combo, 3, 1)

        form_grid.addWidget(QLabel("Build Tool:", self), 4, 0)
        build_combo = QComboBox(self)
        build_combo.addItems(["CMake", "Gradle", "Maven", "Setup.py"])
        form_grid.addWidget(build_combo, 4, 1)

        center_layout.addLayout(form_grid)
        center_layout.addSpacing(30)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        center_layout.addWidget(separator)

        # Action Buttons
        btn_layout = QHBoxLayout()
        back_btn = QPushButton("◀ Back", self)
        next_btn = QPushButton("Next ▶", self)
        finish_btn = QPushButton("Finish", self)
        finish_btn.setStyleSheet("background-color: #0078d4; color: white; font-weight: bold; padding: 6px 15px; border-radius: 4px;")

        btn_layout.addStretch()
        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(next_btn)
        btn_layout.addWidget(finish_btn)
        center_layout.addLayout(btn_layout)
        center_layout.addStretch()

        main_layout.addLayout(center_layout, 3)

        back_btn.clicked.connect(lambda: NavigationController.get_instance().navigate_to(NavigationTarget.HOME))
        finish_btn.clicked.connect(lambda: NavigationController.get_instance().navigate_to(NavigationTarget.HOME))
