import os

class FileSystemService:
    @staticmethod
    def save_file(file_path: str, content: str):
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def save_binary_file(file_path: str, data: bytes):
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(data)
