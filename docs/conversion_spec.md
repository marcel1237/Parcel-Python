# Parcel-Python Conversion Specification

This document details the conversion specification for migrating **Parcel C++** (Qt 6 / C++17) to **Parcel-Python** (PyQt6 / Python 3.10+).

## Architecture Mapping

| Component | Parcel C++ (C++17 / Qt 6) | Parcel-Python (Python 3.10+ / PyQt6) |
| :--- | :--- | :--- |
| **Main Window & Views** | `src/main.cpp`, `MainWindow.hpp`, `DashboardView.hpp` | `parcel/main.py`, `parcel/view/main_window.py`, `dashboard_view.py` |
| **Navigation & Wizards** | `NavigationController.hpp`, `NewProjectView.hpp`, `OpenProjectView.hpp` | `parcel/core/navigation.py`, `new_project_view.py`, `open_project_view.py` |
| **Settings & Config** | `SettingsView.hpp`, `PersistenceService.cpp` | `parcel/view/settings_view.py`, `parcel/service/persistence.py` |
| **Project Header & Buttons** | `ProjectHeader.hpp` | `parcel/view/project_header.py` |
| **Backups & Database** | `BackupService.hpp` (SQLite) | `parcel/service/backup.py` (SQLite `sqlite3`) |
| **SS AI Agent** | `SSAIModule.cpp`, `LocalAgent.cpp` | `parcel/ss_ai_agent/ssai_module.py`, `local_agent.py` |
| **QLM Engine** | `QLMEngine.cpp` | `parcel/ss_ai_agent/qlm_engine.py` |
| **Code Editor & Designer** | `EditorPane.cpp`, `DesignerPane.hpp` | `parcel/view/editor/editor_pane.py`, `designer_pane.py` |
| **Workspace Host** | `ProjectWorkspace.hpp` | `parcel/view/project_workspace.py` |

## Detailed Documentation
See [technical_documentation.md](./technical_documentation.md) for complete architecture and execution details.
