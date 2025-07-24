# Snip-Diff

```
███████╗███╗   ██╗██╗██████╗       ██████╗ ██╗███████╗███████╗
██╔════╝████╗  ██║██║██╔══██╗      ██╔══██╗██║██╔════╝██╔════╝
███████╗██╔██╗ ██║██║██████╔╝█████╗██║  ██║██║█████╗  █████╗  
╚════██║██║╚██╗██║██║██╔═══╝ ╚════╝██║  ██║██║██╔══╝  ██╔══╝  
███████║██║ ╚████║██║██║           ██████╔╝██║██║     ██║     
╚══════╝╚═╝  ╚═══╝╚═╝╚═╝           ╚═════╝ ╚═╝╚═╝     ╚═╝     
                                                              
    ⚡ Powers AI Workflows - No More Manual File Copying ⚡
```

**AI workflow tool for preparing code context outside agentic environments**

![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)

## Screenshots

### Light Theme
![Light Theme](screenshots/light.png)

### Dark Theme  
![Dark Theme](screenshots/dark.png)

## Mission

Snip-Diff bridges the gap between your codebase and AI language models. It aggregates multiple files into AI-ready formats with visual selection, unified diff generation, and one-click copying. Built for developers who need to efficiently provide code context to GPT, Claude, Gemini, and other LLMs.

## Features

**Core Functionality**
- Multi-file selection with visual tree interface
- Unified diff generation preserving file relationships
- Syntax highlighting optimized for AI consumption
- One-click copy for seamless LLM integration
- Live file watching with automatic updates

**User Experience**
- Neumorphic design with light/dark themes
- Nintendo 3DS-inspired glass transparency
- Keyboard shortcuts for productivity
- Search functionality with wraparound

## Installation

```bash
git clone https://github.com/tayyab3245/snip-diff.git
cd snip-diff
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Requirements:** Python 3.9+, PySide6, Pygments

## Usage

1. Open project folder (Ctrl+O)
2. Select relevant files in tree
3. Generate context (F5)
4. Copy output (Ctrl+C)
5. Paste into your LLM

## Upcoming Updates

**Smart Chunking**
- Platform-specific token limits for GPT-4, Claude, Gemini
- Context size optimization algorithms
- Export presets for different AI providers

**Intelligence Features**
- File relevance scoring and auto-prioritization
- Smart diff algorithms for changed-only contexts
- Integration with popular AI coding assistants

---

MIT License - Built for the AI development community
