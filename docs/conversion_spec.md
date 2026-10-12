# Parcel-Python Conversion Specification

This document details the conversion specification for migrating **Parcel C++** (Qt 6 / C++17) to **Parcel-Python** (PyQt6 / Python 3.10+).

## Architecture Mapping

| Component | Parcel C++ (C++17 / Qt 6) | Parcel-Python (Python 3.10+ / PyQt6) |
| :--- | :--- | :--- |
| **Main Window** | `src/main.cpp`, `src/view/MainWindow.hpp` | `parcel/main.py`, `parcel/view/main_window.py` |
| **Core Router** | `src/core/navigation/NavigationController.hpp` | `parcel/core/navigation.py` |
| **Persistence & Auth** | `src/service/PersistenceService.cpp` | `parcel/service/persistence.py` |
| **Backups** | `src/service/BackupService.hpp` (SQLite) | `parcel/service/backup.py` (SQLite `sqlite3`) |
| **SS AI Agent** | `src/SS AI Agent/SSAIModule.cpp`, `LocalAgent.cpp` | `parcel/ss_ai_agent/ssai_module.py`, `local_agent.py` |
| **QLM Engine** | `src/SS AI Agent/QLMEngine.cpp` | `parcel/ss_ai_agent/qlm_engine.py` |
| **Code Editor** | `src/view/editor/EditorPane.cpp` | `parcel/view/editor/editor_pane.py` |
| **QML Designer** | `src/view/editor/DesignerPane.hpp` | `parcel/view/editor/designer_pane.py` |
| **File Explorer** | `src/view/explorer/PackageExplorer.cpp` | `parcel/view/explorer/package_explorer.py` |
| **Workspace Host** | `src/view/ProjectWorkspace.hpp` | `parcel/view/project_workspace.py` |

## Dependencies

- **`PyQt6`**: Core GUI, Widgets, QML/QuickWidgets, Sql, Charts, Network
- **`PyQt6-WebEngine`**: WebEngineView for Gemini/OpenAI/Browser panes
- **`scikit-learn` & `numpy`**: Machine Learning predictions & style analysis
- **`trafilatura` & `requests`**: Web scraping and research agent
- **`google-genai` & `openai`**: LLM API integrations
