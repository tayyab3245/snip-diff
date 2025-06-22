# NIP-Diff

A lightweight desktop application for visually inspecting code diffs with full context. Built using **PySide6**, NIP-Diff emulates a modern Nintendo-style glass UI and delivers VS Code-like syntax highlighting for intuitive review of code changes.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

This project is licensed under the MIT License. You are free to use, modify, and distribute it for personal and commercial purposes.

---

## Screenshots

### Diff Viewer UI

<img src="./assets/screens/diff-viewer-ui.png" alt="Diff Viewer UI Screenshot" width="640"/>

---

## Features

* **Unified Diff**: View full-context diffs for added, removed, and modified files.
* **Syntax Highlighting**: VS Code–style coloring using Pygments.
* **Translucent UI**: Nintendo 3DS–inspired glass theme via Qt styles.
* **Search**: In-view `Ctrl+F` search with wraparound.
* **Clipboard**: Copy entire diff output with one click.
* **Live Reload**: Auto-refresh on filesystem changes.

---

## Prerequisites

* **Python** 3.9 or later
* **Git** (for cloning the repository)
* **Virtual environment** tool (optional but recommended)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/nip-diff.git
   cd nip-diff
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

> The `requirements.txt` file lists:
>
> ```
> PySide6>=6.4
> Pygments>=2.15
> ```

---

## Running the App

From the project root, run:

```bash
python -Xfaulthandler main.py
```

* **Choose** a folder to diff
* **Check** files you want to include
* Press **Run** (or `F5`) to generate and view syntax‑highlighted diffs

---

## Development Notes

* **UI components**: `nip/ui/`
* **Diff engine**: `nip/core/diff_engine.py`
* **Snapshot storage**: `.nip_snapshot.json`
* **Theme file**: `config/theme.py`

---

## Requirements File

Ensure `requirements.txt` is present at the project root with the dependencies listed above. To update dependencies, modify `requirements.txt` and reinstall:

```bash
pip install -r requirements.txt
```

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.
