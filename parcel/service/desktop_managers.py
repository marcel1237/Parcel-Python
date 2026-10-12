import os
import subprocess
from typing import Dict, List

class KDEManager:
    def __init__(self):
        pass

    def get_plasma_version(self) -> str:
        try:
            res = subprocess.run(["plasmashell", "--version"], capture_output=True, text=True)
            return res.stdout.strip()
        except Exception:
            return "KDE Plasma Not Detected"


class GTKManager:
    def __init__(self, version: int = 4):
        self.version = version

    def get_theme_name(self) -> str:
        try:
            res = subprocess.run(["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"], capture_output=True, text=True)
            return res.stdout.strip().replace("'", "")
        except Exception:
            return "Adwaita-dark"


class DotNetManager:
    def __init__(self):
        pass

    def get_sdk_versions(self) -> List[str]:
        try:
            res = subprocess.run(["dotnet", "--list-sdks"], capture_output=True, text=True)
            return [line.strip() for line in res.stdout.splitlines() if line.strip()]
        except Exception:
            return []


class PhpWebManager:
    def __init__(self):
        pass

    def get_php_version(self) -> str:
        try:
            res = subprocess.run(["php", "-v"], capture_output=True, text=True)
            return res.stdout.splitlines()[0] if res.stdout else "PHP Not Found"
        except Exception:
            return "PHP Not Found"


class JavaScriptWebManager:
    def __init__(self):
        pass

    def get_node_version(self) -> str:
        try:
            res = subprocess.run(["node", "-v"], capture_output=True, text=True)
            return res.stdout.strip()
        except Exception:
            return "Node.js Not Found"
