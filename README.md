# Parcel-Python

**Parcel-Python** is a sophisticated, AI-driven Industrial Development Toolkit built on **PyQt6** and **Python 3.10+**. It represents the complete migration of Parcel C++, integrating multi-agent intelligence, real-time code auditing, a SQLite backup/snapshot system, and a visual UI designer to streamline complex software engineering workflows.

---

## 🚀 Key Features

### 🧠 SS AI Agent (Extraordinary Shell & Code Intelligence)
- **Multi-Agent Orchestration:** Seamlessly triages requests between local semantic analysis, real-time web research, and deep reasoning via LLMs (Gemini & OpenAI).
- **SSQLM Standards:** Enforces high-fidelity Shell Script Quality Language Model (SSQLM) standards for safety, atomicity, and industrial resilience.
- **Symbol Indexer & Auto-Healing:** Recursively indexes project classes and functions, performing automated audits and transaction-safe surgical code patching.

### 🎨 Visual UI Designer & Blueprint Engine
- **Hybrid Bridge:** Advanced Python/QML bridge for visual interface development and real-time component design.
- **Cyber-Dark Theme:** Professional, high-contrast dark aesthetic optimized for long-duration industrial development.

### 🛡️ Core Services & Safety
- **Backup Service:** Incremental, SQLite-based project versioning and safe restoration points stored in `.parcel_backups.db`.
- **Script Validator:** Real-time linting for Shell scripts to prevent common pitfalls and security risks.
- **Persistence Layer:** Encrypted storage for API keys and project session management.

---

## 🛠️ Build & Installation

### Prerequisites
- **Python 3.10+**
- **PyQt6 & PyQt6-WebEngine**

### Installation Guide
```bash
# Clone the repository
cd Parcel-Python

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Running the Application
```bash
python3 -m parcel.main
```

---

## 📂 Project Structure

```
parcel/
├── main.py                     # Application entry point
├── core/                       # Navigation and core constants
├── service/                    # Native backend services (Backup, Persistence, Git)
├── ss_ai_agent/                # Autonomous AI Subsystem (QLM, LocalAgent, Patcher)
└── view/                       # PyQt6 GUI Widgets, Workspaces, Panes & Dialogs
```

---

## 📚 Documentation
Comprehensive technical documentation and conversion specifications are available in the [docs/](./docs/) directory:
- [Technical Documentation](./docs/technical_documentation.md)
- [Conversion Specification](./docs/conversion_spec.md)

---

## ⚖️ Licensing

This project is governed by a **Strict Proprietary Software License Agreement**.

- **Proprietary & Confidential:** All rights are reserved by Marcel Aparecido de Andrade.
- **Restrictions:** Redistribution, modification, reverse engineering, and SaaS hosting are strictly prohibited.
- **Trade Secrets:** The core logic, including the SS AI Agent and SSQLM algorithms, are considered trade secrets.

---

## ✍️ Author
**Marcel Aparecido de Andrade**  
*AI-Driven Industrial Development Specialist*
