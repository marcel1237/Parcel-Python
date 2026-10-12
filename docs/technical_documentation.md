# Technical Documentation: Parcel-Python

## 1. Executive Summary

**Parcel-Python** is the complete Python migration of the **Parcel C++** (Qt 6 / C++17) Industrial Development Toolkit and IDE. Developed by **Marcel Aparecido de Andrade**, it combines native PyQt6 GUI engineering with an advanced on-device AI agent (**SS AI Agent**) driven by Quality Language Model (QLM/SSQLM) rules, SQLite project backup snapshotting, and multi-pane IDE layout.

---

## 2. Project Structure (`parcel/`)

```
parcel/
├── __init__.py                 # Package initializer
├── main.py                     # Application entry point (WebEngine config, icon painter, theme loader)
├── core/                       # Core navigation and constants
│   ├── constants.py            # Global app constants
│   ├── version.py              # Version info ("1.0.0")
│   └── navigation.py           # Singleton NavigationController & NavigationTarget enum
├── service/                    # Native backend services
│   ├── persistence.py          # Encrypted settings (XOR), LLM keys, and usage telemetry
│   ├── backup.py               # SQLite-backed build backups and file saves (.parcel_backups.db)
│   ├── git_service.py          # Git repository detector, branch & status checker
│   ├── file_system.py          # File I/O helpers
│   ├── pdf_service.py          # PDF knowledge base exporter
│   └── desktop_managers.py     # KDE, GTK, .NET, PHP, and Node.js environment bridges
├── ss_ai_agent/                # Autonomous AI Subsystem
│   ├── qlm_engine.py           # JSON-driven QLM/SSQLM rule matcher
│   ├── project_knowledge.py    # Symbol table, location index, and task queue
│   ├── file_patcher.py         # Transactional surgical code patcher (reconstruct, safe_create, patch, smart_append)
│   ├── script_validator.py     # Shell script safety linter (SSQLM rules)
│   ├── ml_service.py           # scikit-learn / numpy bridge for bug risk & style analysis
│   ├── web_search.py           # Trafilatura / requests web research agent
│   ├── local_agent.py          # On-device intelligence coordinator
│   └── ssai_module.py          # Central multi-agent orchestrator
└── view/                       # PyQt6 GUI Widgets & Layouts
    ├── theme.py                # Cyber-Dark custom palette & stylesheet
    ├── main_window.py          # Main window hosting menu bar, toolbar, status bar, and view stack
    ├── dashboard_view.py       # Welcome dashboard with New Project and Open Project buttons
    ├── new_project_view.py     # Multi-step project creation wizard
    ├── open_project_view.py    # Project folder selector and static analysis report viewer
    ├── settings_view.py        # Gemini API key configuration and framework integrations view
    ├── project_header.py       # Compact project header with Git badge and action buttons
    ├── project_workspace.py    # Multi-pane workspace (Explorer, Editor, Designer, East/South panes)
    ├── editor/                 # Code Editor, QML Blueprint Designer, Hex, and PDF Viewers
    ├── explorer/               # Package Explorer and DBMS Explorer
    └── panes/                  # Assistant and tool panes (Gemini, OpenAI, Terminal, Logcat, Browser, etc.)
```

---

## 3. Core Layer & Navigation (`parcel/core/`)

- **`NavigationController` (`navigation.py`):** Implements a thread-safe singleton pattern routing views across the application via `NavigationTarget` enums (`HOME`, `NEW_PROJECT`, `OPEN_PROJECT`, `SETTINGS`, `WORKSPACE`).

---

## 4. Service & Backup Layer (`parcel/service/`)

- **`PersistenceService` (`persistence.py`):** Stores application state and encrypts sensitive API keys using XOR transformation (`0xAF`). Tracks daily, weekly, and monthly usage metrics.
- **`BackupService` (`backup.py`):** Initializes `.parcel_backups.db` SQLite database inside target projects, capturing recursive build backups and individual file revision saves.
- **`GitService` & Desktop Managers (`git_service.py`, `desktop_managers.py`):** Provides subprocess wrappers for Git commands and environment bridges for KDE, GTK, .NET, PHP, and Node.js.

---

## 5. SS AI Agent Subsystem (`parcel/ss_ai_agent/`)

- **`QLMEngine` (`qlm_engine.py`):** Scans and matches natural language instructions against JSON rule files located in `QLM/` and `SS QLM/`.
- **`FilePatcher` (`file_patcher.py`):** Guarantees atomic file updates using `QSaveFile`-like temporary file replacement and precise block patching.
- **`LocalAgent` (`local_agent.py`):** Recursively indexes project symbols (classes and functions) and provides local intelligence.

---

## 6. View Layer, Navigation Views & Button Layout (`parcel/view/`)

### Navigation Views
1. **`DashboardView`**: Displays welcome title and primary buttons: **New Project** and **Open Project**.
2. **`NewProjectView`**: Multi-step wizard with fields for Project Name, Group, Artifact, Language combo, Build Tool combo, and action buttons (**Back**, **Next**, **Finish**).
3. **`OpenProjectView`**: Folder picker with automated project analysis (Git status, file counts, sizes) and action buttons (**Browse...**, **Open**, **Cancel**).
4. **`SettingsView`**: Configuration panel for Gemini API key, framework info, and action buttons (**Salvar Configurações**, **Voltar**).

### Project Workspace Header Buttons
Located in `ProjectHeader` (`project_header.py`):
- **✨ East Pane** (`#4285F4`): Toggles the right-side AI assistant panel (Gemini, OpenAI, Shell Scripting, Git).
- **🌐 South Pane** (`#34A853`): Toggles the bottom tool panel (Web browsers, Terminal, SS AI Agent, Problems, Database, Logs, Versions, Saves).
- **🎨 Designer** (`#E67E22`): Toggles the QML Visual Component Designer pane.
- **🔨 Build + Backup** (`#27ae60`): Triggers SQLite backup generation and runs build logging in the terminal.
- **📦 Export** (`#8E44AD`): Triggers project export packaging.

---

## 7. Execution & Compilation Guide

### Prerequisites
- Python 3.10+
- PyQt6 & PyQt6-WebEngine

### Setup & Execution
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m parcel.main
```
