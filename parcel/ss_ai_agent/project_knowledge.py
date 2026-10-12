import datetime
from typing import Dict, List, Optional

class ProjectKnowledge:
    _instance: Optional["ProjectKnowledge"] = None

    @classmethod
    def get_instance(cls) -> "ProjectKnowledge":
        if cls._instance is None:
            cls._instance = ProjectKnowledge()
        return cls._instance

    def __init__(self):
        self.project_root: str = ""
        self.recent_files: List[str] = []
        self.pending_tasks: List[str] = []
        self.symbol_map: Dict[str, str] = {}
        self.symbol_type_map: Dict[str, str] = {}
        self.last_seen: Dict[str, datetime.datetime] = {}

    def record_modified_file(self, path: str):
        if path in self.recent_files:
            self.recent_files.remove(path)
        self.recent_files.insert(0, path)

    def register_symbol(self, name: str, file_path: str, symbol_type: str = "class"):
        self.symbol_map[name] = file_path
        self.symbol_type_map[name] = symbol_type
        self.last_seen[name] = datetime.datetime.now()

    def find_symbol_location(self, name: str) -> str:
        return self.symbol_map.get(name, "")

    def get_symbol_type(self, name: str) -> str:
        return self.symbol_type_map.get(name, "")

    def add_task(self, description: str):
        self.pending_tasks.append(description)

    def complete_task(self, index: int):
        if 0 <= index < len(self.pending_tasks):
            self.pending_tasks.pop(index)

    def clear_tasks(self):
        self.pending_tasks.clear()
