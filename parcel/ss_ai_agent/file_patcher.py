import os
from enum import Enum, auto

class PatchStatus(Enum):
    Success = auto()
    FileNotFound = auto()
    FileAlreadyExists = auto()
    MarkersNotFound = auto()
    DuplicateFound = auto()
    WriteError = auto()


class FilePatcher:
    @staticmethod
    def atomic_write(file_path: str, content: str) -> bool:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            tmp_path = file_path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(content)
            os.replace(tmp_path, file_path)
            return True
        except Exception:
            return False

    @classmethod
    def reconstruct(cls, file_path: str, content: str) -> PatchStatus:
        if cls.atomic_write(file_path, content):
            return PatchStatus.Success
        return PatchStatus.WriteError

    @classmethod
    def safe_create(cls, file_path: str, content: str) -> PatchStatus:
        if os.path.exists(file_path):
            return PatchStatus.FileAlreadyExists
        if cls.atomic_write(file_path, content):
            return PatchStatus.Success
        return PatchStatus.WriteError

    @classmethod
    def patch(cls, file_path: str, start_marker: str, end_marker: str, new_content: str) -> PatchStatus:
        if not os.path.exists(file_path):
            return PatchStatus.FileNotFound

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return PatchStatus.FileNotFound

        start_index = content.find(start_marker)
        end_index = content.find(end_marker)

        if start_index == -1 or end_index == -1 or end_index <= start_index:
            return PatchStatus.MarkersNotFound

        end_of_start_line = content.find("\n", start_index)
        if end_of_start_line == -1:
            end_of_start_line = start_index + len(start_marker)

        prefix = content[:end_of_start_line + 1]
        suffix = content[end_index:]

        patched_content = prefix + new_content + ("" if new_content.endswith("\n") else "\n") + suffix

        if cls.atomic_write(file_path, patched_content):
            return PatchStatus.Success
        return PatchStatus.WriteError

    @classmethod
    def smart_append(cls, file_path: str, content: str, duplicate_check_marker: str) -> PatchStatus:
        existing_content = ""
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    existing_content = f.read()
                if duplicate_check_marker in existing_content:
                    return PatchStatus.DuplicateFound
            except Exception:
                return PatchStatus.FileNotFound

        final_content = existing_content
        if final_content and not final_content.endswith("\n"):
            final_content += "\n"
        final_content += content

        if cls.atomic_write(file_path, final_content):
            return PatchStatus.Success
        return PatchStatus.WriteError
