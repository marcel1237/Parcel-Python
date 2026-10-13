# Complete Changelog & Migration Record: Parcel-Python

This document records all architectural implementations, migrations, features, and refinements performed during the creation of **Parcel-Python**, converted from the original C++ (Qt 6) codebase.

---

## 1. Migration Overview (C++ to Python)
- **Framework Stack**: Migrated from C++17 / Qt 6 Widgets / QML to **Python 3.10+ / PyQt6 / PyQt6-WebEngine**.
- **Modular Package Structure**: Organized inside the `parcel/` package with dedicated submodules for core, services, AI agents, and views.

---

## 2. Core Layer & Navigation (`parcel/core/`)
- **`NavigationController`**: Thread-safe singleton managing view transitions via `NavigationTarget` enums (`HOME`, `NEW_PROJECT`, `OPEN_PROJECT`, `SETTINGS`, `WORKSPACE`).
- **Constants & Version**: Global application constants and versioning (`1.0.0`).

---

## 3. Native Service & Backup Layer (`parcel/service/`)
- **`PersistenceService`**: Settings manager with XOR-based encryption (`0xAF`) for LLM API keys (Gemini/OpenAI) and usage telemetry tracking.
- **`BackupService`**: SQLite database snapshotter (`.parcel_backups.db`) managing recursive build backups and individual file revision saves.
- **`ExportService`**: Native Python export engine capable of generating Debian packages (`.deb`), release tarballs (`.tar.gz`), and AppImage directory structures inside the `build/` folder.
- **`GitService` & Desktop Managers**: Subprocess Git repository detector, branch tracker, and environment bridges for KDE, GTK (2/3/4), .NET, PHP, and Node.js.

---

## 4. SS AI Agent Subsystem (`parcel/ss_ai_agent/`)
- **`QLMEngine`**: Evaluates natural language instructions against JSON rule files (`QLM/` and `SS QLM/`).
- **`LocalAgent` & `ProjectKnowledge`**: Recursively indexes project symbols (classes and functions), manages short-term memory, and tracks technical debt.
- **`FilePatcher`**: Transactional code patcher ensuring safe, atomic file modifications (`reconstruct`, `safe_create`, `patch`, `smart_append`).
- **`ScriptValidator`**: Shell script linter enforcing SSQLM safety standards (`set -uo pipefail`, error traps, unquoted variable checks).
- **`MLService` & `WebSearch`**: Python ML context predictor and Trafilatura web research agent.

---

## 5. View Layer & UI Components (`parcel/view/`)
- **Cyber-Dark Theme (`theme.py`)**: Deep space color palette applied via custom `QPalette` and stylesheets.
- **Navigation Views**:
  - `DashboardView`: Welcome dashboard with New Project and Open Project buttons.
  - `NewProjectView`: Multi-step project creation wizard.
  - `OpenProjectView`: Folder picker and static project analysis report viewer.
  - `SettingsView`: API key configuration and framework integrations view.
- **Project Header & Workspace (`project_header.py`, `project_workspace.py`)**:
  - Compact header with Git branch badge and action buttons: **East Pane**, **South Pane**, **Designer**, **Build + Backup** (triggers SQLite backup and live terminal build logging), and **Export** (menu with `.deb`, `.tar.gz`, `.AppDir` options).
- **Advanced Syntax Highlighter (`highlighter.py`)**:
  - Supports **Python, C/C++, Java, C#, VB.NET, F#, Go, Rust, JavaScript, TypeScript, PHP, Ruby, Perl, Raku, ASP, JSP, Assembly, Shell Script, SQL, JSON, YAML, HTML/XML/QML, and Markdown**.
- **Interactive QML Designer (`designer_pane.py`, `DesignerCanvas`)**:
  - Component palette with 30+ QML & Kirigami elements, interactive mouse-draggable canvas for precise X/Y positioning, Properties Inspector, and live QML Code Generator.
- **Assistant & Tool Panes**:
  - Gemini, OpenAI, Terminal, Logcat, Browser, Databases, Inspection, Versions, and Saves panes.

---

## 6. Automation, Packaging & Execution
- **`build.sh` & `run.sh`**: Automated environment setup and execution scripts (available at project root and inside `build/`).
- **Dynamic Application Icon**: Automatically generates and saves the "PP" monogram icon with Python branding colors (`resources/parcel-python-dark.png` and `~/.local/share/icons/`).
- **`.gitignore`**: Configured to exclude virtual environments, build artifacts, and large SQLite backup files (`.parcel_backups.db`).
