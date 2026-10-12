import os
import datetime
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class UsageStats:
    daily: int = 0
    weekly: int = 0
    monthly: int = 0
    yearly: int = 0


class PersistenceService:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/parcel-python")
        os.makedirs(self.config_dir, exist_ok=True)
        self.props_file = os.path.join(self.config_dir, "settings.properties")

    def _encrypt(self, data: str) -> str:
        if not data:
            return ""
        return "".join(f"{ord(c) ^ 0xAF:02x}" for c in data)

    def _decrypt(self, data: str) -> str:
        if not data:
            return ""
        try:
            bytes_list = [int(data[i:i+2], 16) ^ 0xAF for i in range(0, len(data), 2)]
            return "".join(chr(b) for b in bytes_list)
        except Exception:
            return ""

    def load_properties(self) -> Dict[str, str]:
        props = {}
        if os.path.exists(self.props_file):
            with open(self.props_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        props[k.strip()] = v.strip()
        return props

    def save_properties(self, props: Dict[str, str]):
        with open(self.props_file, "w", encoding="utf-8") as f:
            for k, v in props.items():
                f.write(f"{k}={v}\n")

    def save_last_project(self, path: str):
        props = self.load_properties()
        props["last.project.path"] = path
        self.save_properties(props)

    def get_last_project(self) -> str:
        props = self.load_properties()
        return props.get("last.project.path", "")

    def save_open_files(self, file_paths: List[str]):
        props = self.load_properties()
        props["open.files"] = ",".join(file_paths)
        self.save_properties(props)

    def get_open_files(self) -> List[str]:
        props = self.load_properties()
        files = props.get("open.files", "")
        if not files:
            return []
        return [f.strip() for f in files.split(",") if f.strip()]

    def increment_usage(self):
        props = self.load_properties()
        now = datetime.datetime.now()
        d_key = f"usage.d.{now.strftime('%Y-%m-%d')}"
        w_key = f"usage.w.{now.strftime('%Y-%W')}"
        m_key = f"usage.m.{now.strftime('%Y-%m')}"
        y_key = f"usage.y.{now.strftime('%Y')}"

        for key in [d_key, w_key, m_key, y_key]:
            val = int(props.get(key, "0")) + 1
            props[key] = str(val)

        self.save_properties(props)

    def get_usage_stats(self) -> UsageStats:
        props = self.load_properties()
        now = datetime.datetime.now()
        d_key = f"usage.d.{now.strftime('%Y-%m-%d')}"
        w_key = f"usage.w.{now.strftime('%Y-%W')}"
        m_key = f"usage.m.{now.strftime('%Y-%m')}"
        y_key = f"usage.y.{now.strftime('%Y')}"

        return UsageStats(
            daily=int(props.get(d_key, "0")),
            weekly=int(props.get(w_key, "0")),
            monthly=int(props.get(m_key, "0")),
            yearly=int(props.get(y_key, "0"))
        )

    def save_gemini_api_key(self, key: str):
        props = self.load_properties()
        props["gemini.api.key"] = self._encrypt(key)
        self.save_properties(props)

    def get_gemini_api_key(self) -> str:
        props = self.load_properties()
        return self._decrypt(props.get("gemini.api.key", ""))
