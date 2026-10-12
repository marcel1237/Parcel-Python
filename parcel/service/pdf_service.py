import os
import datetime
import html
from PyQt6.QtGui import QTextDocument, QPageSize
from PyQt6.QtPdf import QPdfWriter

class PdfService:
    @staticmethod
    def update_project_pdf(project_path: str):
        if not project_path or not os.path.exists(project_path):
            return

        output_file_path = os.path.join(project_path, "Project_Knowledge_Base.pdf")
        full_content = "<h1>Project Knowledge Base</h1>"
        full_content += f"<p>Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p><hr>"

        text_extensions = {
            ".java", ".cpp", ".hpp", ".h", ".c", ".cc", ".xml", ".fxml",
            ".json", ".md", ".txt", ".sh", ".bash", ".css", ".pro",
            ".cmake", ".desktop", ".py"
        }

        file_count = 0
        for root, dirs, files in os.walk(project_path):
            if file_count > 200:
                break
            if "build" in root or ".git" in root or ".idea" in root:
                continue
            for file_name in files:
                if file_name == "Project_Knowledge_Base.pdf":
                    continue
                ext = os.path.splitext(file_name)[1].lower()
                if ext in text_extensions or file_name in ("CMakeLists.txt", "Makefile", "requirements.txt"):
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        if len(content) > 50000:
                            content = content[:50000] + "\n... [TRUNCATED]"
                        full_content += f"<h2>File: {file_name}</h2>"
                        full_content += f"<pre style='font-size: 8px;'>{html.escape(content)}</pre><hr>"
                        file_count += 1
                    except Exception:
                        pass

        doc = QTextDocument()
        doc.setHtml(full_content)
        writer = QPdfWriter(output_file_path)
        writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        doc.print(writer)
