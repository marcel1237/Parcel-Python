import sqlite3
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton

class SavesPane(QWidget):
    def __init__(self, project_path: str = "", parent=None):
        super().__init__(parent)
        self.project_path = project_path
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Individual File Saves & Revisions</b>"))

        btn_refresh = QPushButton("Refresh Saves", self)
        btn_refresh.clicked.connect(self.load_saves)
        layout.addWidget(btn_refresh)

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "File Name", "Timestamp", "Summary"])
        layout.addWidget(self.table)

    def load_saves(self):
        if not self.project_path:
            return
        db_path = os.path.join(self.project_path, ".parcel_backups.db")
        if not os.path.exists(db_path):
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, file_name, timestamp, change_summary FROM saves ORDER BY id DESC")
            rows = cursor.fetchall()
            conn.close()

            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
                self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
                self.table.setItem(i, 2, QTableWidgetItem(str(row[2])))
                self.table.setItem(i, 3, QTableWidgetItem(str(row[3])))
        except Exception:
            pass
