# NIP-Diff

A lightweight desktop application for visually inspecting code diffs with full context. Built using **PySide6**, NIP-Diff emulates a modern Nintendo-style glass UI and delivers VS Code–style syntax highlighting for intuitive review of code changes.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

This project is licensed under the MIT License. You are free to use, modify, and distribute it for personal and commercial purposes.

---

## How It Works

1. **Folder Selection**: Click **Choose Folder** or use `Ctrl+O` to pick a project directory.
2. **File Tree**: A checkable tree displays all files and folders; select items to include in the diff.
3. **Run Diff**: Click **Run** or press `F5` to generate a full unified diff using Python’s `difflib`.
4. **Preview Panel**: View color-coded diffs with syntax highlighting (via Pygments) in a read-only panel.
5. **Search & Copy**:

   * Press `Ctrl+F` to search within the diff (with wraparound).
   * Click **Copy Output** or press `Ctrl+C` to copy the entire diff to the clipboard.
6. **Live Reload**: After the first run, NIP-Diff watches for file changes and auto-refreshes the diff (300 ms debounce).

---

## Features

* **Unified Diff**: Complete context for added, removed, and modified lines.
* **Syntax Highlighting**: VS Code–style token coloring.
* **Translucent UI**: Nintendo 3DS–inspired glass theme.
* **In-View Search**: `Ctrl+F` with wraparound.
* **Clipboard Copy**: One-click full-diff copy.
* **Live Filesystem Watcher**: Automatic updates on file changes.

---

## Prerequisites

* **Python** 3.9 or later
* **Git** (for cloning the repository)
* **pip** (Python package installer)
* **Virtual environment** tool (optional)

---

## Installation & Running

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/nip-diff.git
cd nip-diff
```

### 2. Create & Activate Virtual Environment (Recommended)

* **macOS / Linux**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

* **Windows (PowerShell)**

  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch NIP-Diff

```bash
python -Xfaulthandler main.py
```

Use the toolbar or keyboard shortcuts (`Ctrl+O`, `F5`, `Ctrl+C`, `Ctrl+F`) to interact.

---

## requirements.txt

```text
PySide6>=6.4
Pygments>=2.15
```

To update dependencies, edit `requirements.txt` and re-run:

```bash
pip install -r requirements.txt
```

---

## Development Notes

* **UI components**: `nip/ui/`
* **Diff engine**: `nip/core/diff_engine.py`
* **Snapshot storage**: `.nip_snapshot.json` (undo functionality)
* **Theme**: `config/theme.py`

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.
