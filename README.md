# SNIP-Diff

A lightweight desktop application for visually inspecting code diffs with full context. Built using **PySide6**, NIP-Diff emulates a modern Nintendo-style glass UI and delivers VS Code–style syntax highlighting for intuitive review of code changes.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

This project is licensed under the MIT License. You are free to use, modify, and distribute it for personal and commercial purposes.

---

## How It Works

1. **Folder Selection**: Click **Choose Folder** or press `Ctrl+O` to select a project directory.
2. **File Tree**: Browse and check the files/folders you want to include in the diff.
3. **Run Diff**: Click **Run** or press `F5` to generate a unified diff (using Python’s `difflib`).
4. **Preview Panel**: View color-coded diffs with VS Code–style syntax highlighting (via Pygments).
5. **Search & Copy**: Use `Ctrl+F` to search (with wraparound) and `Ctrl+C` or **Copy Output** to copy the entire diff.
6. **Live Reload**: After the initial run, NIP-Diff watches for changes and auto-refreshes the diff (300 ms debounce).

---

## Features

* **Unified Diff**: Full-context diffs for added, removed, and modified lines.
* **Syntax Highlighting**: VS Code–style token coloring with Pygments.
* **Translucent UI**: Nintendo 3DS–inspired glass theme.
* **In-View Search**: `Ctrl+F` search with wraparound.
* **Clipboard Copy**: One-click full-diff copy.
* **Live Filesystem Watcher**: Automatic updates on file changes.

---

## Project Structure

```
nip-diff/              # project root
├── requirements.txt    # dependency list (PySide6, Pygments)
├── LICENSE             # MIT license file
├── config/             # UI theme and defaults
├── nip/                # main package
│   ├── __init__.py
│   ├── ui/             # UI components
│   │   └── main_window.py  # entry point module
│   └── core/           # diff logic & snapshot management
└── README.md           # this file
```

> **Note:** There is no top-level `main.py`.  To launch the app, use the `nip.ui.main_window` module (see below).

## Prerequisites

* **Python** 3.9 or later
* **Git** (for cloning the repository)
* **pip** (package installer for Python)
* **Virtual environment** tool (optional but recommended)

---

## Installation & Running

1. **Clone the repository** (avoids ZIP naming issues):

   ```bash
   git clone https://github.com/your-username/nip-diff.git
   cd nip-diff
   ```

2. **Delete stale directories** (if you previously extracted a ZIP):

   * **Windows (PowerShell)**

     ```powershell
     Remove-Item -Recurse -Force nip-diff-main
     ```
   * **macOS / Linux**

     ```bash
     rm -rf nip-diff-main
     ```

3. **Create and activate** a virtual environment:

   * **macOS / Linux**

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * **Windows (PowerShell)**

     ```powershell
     python -m venv venv
     . .\venv\Scripts\Activate.ps1
     ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Launch NIP-Diff**:

   ```bash
   python -m nip.ui.main_window
   ```

---

## requirements.txt

```text
PySide6>=6.4
Pygments>=2.15
```

To update dependencies, modify `requirements.txt` and run:

```bash
pip install -r requirements.txt
```

---

## Development Notes

* **UI**: `nip/ui/`
* **Diff Engine**: `nip/core/diff_engine.py`
* **Snapshots**: `.nip_snapshot.json`
* **Theme**: `config/theme.py`

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.
