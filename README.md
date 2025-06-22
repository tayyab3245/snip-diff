# NIP-Diff

A lightweight desktop application for visually inspecting code diffs with full context. Built using **PySide6**, NIP-Diff emulates a modern Nintendo-style glass UI and delivers VS Code-like syntax highlighting for easy, intuitive review of code changes.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

This project is licensed under the MIT License. You are free to use, modify, and distribute it for personal and commercial purposes.

---

## Screenshots

### Diff Viewer UI

<img src="./assets/screens/diff-viewer-ui.png" alt="Diff Viewer UI Screenshot" height="480"/>

---

## Features

* Unified diff viewer with full context for every file
* Contextual syntax highlighting using Pygments
* Beautiful translucent UI inspired by Nintendo 3DS
* Ctrl+F in-view search with wraparound
* Copy entire diff output to clipboard
* Auto-refresh support with live filesystem watcher

---

## Tech Stack

* Python 3.9+
* PySide6 (Qt 6)
* Pygments (for syntax highlighting)
* Built-in `difflib` for generating unified diffs

---

## Getting Started

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/nip-diff.git
cd nip-diff
pip install -r requirements.txt
```

---

## Running the App

To launch NIP-Diff:

```bash
python -Xfaulthandler main.py
```

Once launched:

* Choose a folder
* Check the files you'd like to diff
* Press **Run** (or `F5`) to view full diffs with syntax highlighting

---

## Development Notes

* UI logic is in `nip/ui/`
* Diff logic is handled by `nip/core/diff_engine.py`
* Filesystem snapshots stored as `.nip_snapshot.json`
* Custom theme in `config/theme.py`

---

## Requirements

* Python 3.9+
* pip
* Compatible with Windows, macOS, and Linux (Qt support required)

---

## License

This project is licensed under the MIT License.

> See [LICENSE](./LICENSE) for full terms.
