from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from parcel.core.navigation import NavigationController, NavigationTarget

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("Bem-vindo ao Parcel-Python", self)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")

        btn_new = QPushButton("New Project", self)
        btn_new.setStyleSheet("background-color: #4285F4; color: white; font-weight: bold; padding: 10px 24px; border-radius: 6px; font-size: 14px;")
        btn_new.clicked.connect(lambda: NavigationController.get_instance().navigate_to(NavigationTarget.NEW_PROJECT))

        btn_open = QPushButton("Open Project", self)
        btn_open.setStyleSheet("background-color: #34A853; color: white; font-weight: bold; padding: 10px 24px; border-radius: 6px; font-size: 14px;")
        btn_open.clicked.connect(lambda: NavigationController.get_instance().navigate_to(NavigationTarget.OPEN_PROJECT))

        layout.addWidget(title, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_new, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_open, 0, Qt.AlignmentFlag.AlignCenter)
