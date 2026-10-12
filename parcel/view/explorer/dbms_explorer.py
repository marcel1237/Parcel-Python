from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem

class DBMSExplorer(QWidget):
    def __init__(self, project_path: str = "", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Database Connections</b>"))

        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(["Database / Schema", "Type"])

        db_item = QTreeWidgetItem(self.tree, ["local_project.db", "SQLite"])
        QTreeWidgetItem(db_item, ["builds", "Table"])
        QTreeWidgetItem(db_item, ["build_files", "Table"])
        QTreeWidgetItem(db_item, ["saves", "Table"])

        db_item.setExpanded(True)
        layout.addWidget(self.tree)
