from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import pyqtSignal, QDir

class PackageExplorer(QWidget):
    fileSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tree = QTreeView(self)
        self.model = QFileSystemModel(self)
        self.model.setFilter(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot)

        self.tree.setModel(self.model)
        self.tree.doubleClicked.connect(self.on_double_click)

        layout.addWidget(self.tree)

    def set_root_path(self, path: str):
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))

    def on_double_click(self, index):
        file_path = self.model.filePath(index)
        if not self.model.isDir(index):
            self.fileSelected.emit(file_path)
