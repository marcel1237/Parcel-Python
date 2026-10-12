import os
import subprocess

class GitService:
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.is_git = os.path.exists(os.path.join(root_path, ".git"))

    def is_repository(self) -> bool:
        return self.is_git

    def get_current_branch(self) -> str:
        if not self.is_git:
            return ""
        try:
            res = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.root_path,
                capture_output=True,
                text=True,
                check=True
            )
            return res.stdout.strip()
        except Exception:
            return ""

    def get_status(self) -> str:
        if not self.is_git:
            return ""
        try:
            res = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.root_path,
                capture_output=True,
                text=True,
                check=True
            )
            return res.stdout
        except Exception:
            return ""
