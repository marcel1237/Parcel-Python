# Technical Documentation: Parcel-Python

## 1. Executive Summary

**Parcel-Python** is the complete Python migration of the **Parcel C++** (Qt 6 / C++17) Industrial Development Toolkit and IDE. Developed by **Marcel Aparecido de Andrade**, it combines native PyQt6 GUI engineering with an advanced on-device AI agent (**SS AI Agent**) driven by Quality Language Model (QLM/SSQLM) rules, SQLite project backup snapshotting, and multi-pane IDE layout.

---

## 2. Comprehensive Changelog & Migration Record
For a detailed log of all implementations, refactorings, syntax highlighters, interactive designer canvas features, and export services created during this session, please refer to:
- [Complete Changelog](./complete_changelog.md)
- [Conversion Specification](./conversion_spec.md)

---

## 3. Execution & Compilation Guide

### Prerequisites
- Python 3.10+
- PyQt6 & PyQt6-WebEngine

### Setup & Execution
```bash
# Using automated scripts
./build.sh
./run.sh

# Or manually
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m parcel.main
```
