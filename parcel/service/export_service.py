import os
import shutil
import tarfile
import subprocess

class ExportService:
    @staticmethod
    def export_tarball(project_path: str) -> str:
        build_dir = os.path.join(project_path, "build")
        os.makedirs(build_dir, exist_ok=True)
        out_name = os.path.join(build_dir, "Parcel_Python_v1.0.0_linux_x64.tar.gz")
        
        with tarfile.open(out_name, "w:gz") as tar:
            for root, dirs, files in os.walk(project_path):
                if "build" in root or ".git" in root or "venv" in root or ".parcel_backups.db" in root:
                    continue
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, project_path)
                    tar.add(full_path, arcname=rel_path)
        return out_name

    @staticmethod
    def export_deb(project_path: str) -> str:
        build_dir = os.path.join(project_path, "build")
        os.makedirs(build_dir, exist_ok=True)
        deb_root = os.path.join(build_dir, "parcel_python_deb")
        if os.path.exists(deb_root):
            shutil.rmtree(deb_root)

        os.makedirs(os.path.join(deb_root, "usr", "bin"), exist_ok=True)
        os.makedirs(os.path.join(deb_root, "DEBIAN"), exist_ok=True)

        control_content = """Package: parcel-python
Version: 1.0.0
Section: utils
Priority: optional
Architecture: all
Maintainer: Marcel Aparecido de Andrade <marcel@parcel.com>
Description: Parcel-Python IDE - AI-Driven Industrial Development Toolkit.
"""
        with open(os.path.join(deb_root, "DEBIAN", "control"), "w", encoding="utf-8") as f:
            f.write(control_content)

        out_deb = os.path.join(build_dir, "parcel-python_1.0.0.deb")
        try:
            subprocess.run(["dpkg-deb", "--build", deb_root, out_deb], check=True, capture_output=True)
            return out_deb
        except Exception:
            return ExportService.export_tarball(project_path)

    @staticmethod
    def export_appimage(project_path: str) -> str:
        build_dir = os.path.join(project_path, "build")
        os.makedirs(build_dir, exist_ok=True)
        
        out_binary = os.path.join(build_dir, "parcel-python")

        try:
            pyinstaller_bin = os.path.join(project_path, "venv", "bin", "pyinstaller")
            if not os.path.exists(pyinstaller_bin):
                pyinstaller_bin = "pyinstaller"

            cmd = [
                pyinstaller_bin,
                "--onefile",
                "--name=parcel-python",
                "--clean",
                "--noconfirm",
                f"--add-data=QLM{os.pathsep}QLM",
                f"--add-data=SS QLM{os.pathsep}SS QLM",
                f"--add-data=resources{os.pathsep}resources",
                os.path.join(project_path, "parcel", "main.py")
            ]
            subprocess.run(cmd, cwd=project_path, capture_output=True, text=True, check=True)

            dist_bin = os.path.join(project_path, "dist", "parcel-python")
            if os.path.exists(dist_bin):
                if os.path.exists(out_binary):
                    os.remove(out_binary)
                shutil.copy2(dist_bin, out_binary)
                os.chmod(out_binary, 0o755)
                return out_binary
        except Exception:
            pass

        # Fallback executable binary wrapper script if PyInstaller binary compilation fails
        with open(out_binary, "w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env bash\n")
            f.write(f"cd \"{project_path}\"\n")
            f.write("exec ./venv/bin/python -m parcel.main \"$@\"\n")
        os.chmod(out_binary, 0o755)
        return out_binary
