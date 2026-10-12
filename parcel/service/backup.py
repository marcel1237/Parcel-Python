import os
import sqlite3
import datetime
from typing import Optional, List, Dict

class BackupService:
    _instance: Optional["BackupService"] = None

    @classmethod
    def get_instance(cls) -> "BackupService":
        if cls._instance is None:
            cls._instance = BackupService()
        return cls._instance

    def __init__(self):
        self.project_path: str = ""
        self.db_path: str = ""

    def init(self, project_path: str):
        self.project_path = project_path
        self.db_path = os.path.join(project_path, ".parcel_backups.db")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS builds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                description TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS build_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                build_id INTEGER,
                file_path TEXT,
                content BLOB,
                FOREIGN KEY(build_id) REFERENCES builds(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT,
                file_path TEXT,
                timestamp DATETIME,
                change_summary TEXT,
                content BLOB
            )
        """)

        conn.commit()
        conn.close()

    def perform_build_backup(self, manual_desc: str = ""):
        if not self.db_path or not os.path.exists(self.db_path):
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO builds (timestamp, description) VALUES (?, ?)", (timestamp, manual_desc))
        build_id = cursor.lastrowid

        for root, dirs, files in os.walk(self.project_path):
            if "build" in root or ".git" in root or ".parcel_backups.db" in root:
                continue
            for file_name in files:
                if file_name == ".parcel_backups.db":
                    continue
                full_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(full_path, self.project_path)
                try:
                    with open(full_path, "rb") as f:
                        content = f.read()
                    cursor.execute(
                        "INSERT INTO build_files (build_id, file_path, content) VALUES (?, ?, ?)",
                        (build_id, rel_path, content)
                    )
                except Exception:
                    pass

        conn.commit()
        conn.close()

    def save_file_revision(self, file_path: str, content: str, change_summary: str = "Auto-save"):
        if not self.db_path or not os.path.exists(self.db_path):
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = os.path.basename(file_path)
        rel_path = os.path.relpath(file_path, self.project_path) if self.project_path else file_path

        cursor.execute(
            "INSERT INTO saves (file_name, file_path, timestamp, change_summary, content) VALUES (?, ?, ?, ?, ?)",
            (file_name, rel_path, timestamp, change_summary, content.encode("utf-8"))
        )

        conn.commit()
        conn.close()
