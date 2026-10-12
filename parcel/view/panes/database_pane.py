from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QTableWidget, QTableWidgetItem, QPushButton, QLabel

class DatabasePane(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Database SQL Runner</b>"))

        self.sql_edit = QTextEdit(self)
        self.sql_edit.setPlainText("SELECT * FROM builds LIMIT 10;")
        self.sql_edit.setMaximumHeight(100)
        layout.addWidget(self.sql_edit)

        btn_run = QPushButton("Execute SQL", self)
        btn_run.clicked.connect(self.run_sql)
        layout.addWidget(btn_run)

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Timestamp", "Description"])
        layout.addWidget(self.table)

    def run_sql(self):
        self.table.setRowCount(2)
        self.table.setItem(0, 0, QTableWidgetItem("1"))
        self.table.setItem(0, 1, QTableWidgetItem("2026-02-18 10:00:00"))
        self.table.setItem(0, 2, QTableWidgetItem("Initial Build Snapshot"))

        self.table.setItem(1, 0, QTableWidgetItem("2"))
        self.table.setItem(1, 1, QTableWidgetItem("2026-02-18 10:30:00"))
        self.table.setItem(1, 2, QTableWidgetItem("SSQLM Auto-Save Revision"))
