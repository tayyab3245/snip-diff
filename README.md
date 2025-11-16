# SNIP-DIFF

```
███████╗███╗   ██╗██╗██████╗       ██████╗ ██╗███████╗███████╗
██╔════╝████╗  ██║██║██╔══██╗      ██╔══██╗██║██╔════╝██╔════╝
███████╗██╔██╗ ██║██║██████╔╝█████╗██║  ██║██║█████╗  █████╗
╚════██║██║╚██╗██║██║██╔═══╝ ╚════╝██║  ██║██║██╔══╝  ██╔══╝
███████║██║ ╚████║██║██║           ██████╔╝██║██║     ██║
╚══════╝╚═╝  ╚═══╝╚═╝╚═╝           ╚═════╝ ╚═╝╚═╝     ╚═╝

    AI-Powered Code Diff & Snippet Tool
```

**Streamline your AI development workflow with intelligent code diffing, context management, and LLM-optimized snippet generation**

![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Electron](https://img.shields.io/badge/Electron-191970?style=flat&logo=Electron&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)

## What SNIP-DIFF Does

SNIP-DIFF is a desktop application that revolutionizes how developers work with AI language models by providing intelligent code diffing, context optimization, and snippet generation tools.

### Smart Code Diffing
- **Git Integration**: Automatically detect and analyze Git repository changes
- **File Comparison**: Compare different versions of files with syntax highlighting
- **Change Detection**: Identify additions, deletions, and modifications with precision
- **Live Diff Updates**: Real-time diff processing as you work

### AI Context Optimization
- **Token Estimation**: Calculate LLM context usage for different AI providers
- **Smart Summarization**: AI-powered change summaries using Google Gemini
- **Context Size Management**: Optimize code snippets for model context limits
- **Provider-Specific Formatting**: Tailored output for GPT, Claude, Gemini, and more

### Snippet Management
- **One-Click Copy**: Copy formatted code snippets to clipboard
- **Syntax Highlighting**: Beautiful code presentation with language detection
- **File Tree Navigation**: Browse and select files from your project structure
- **Export Presets**: Pre-configured formats for different AI workflows

### Modern Desktop Experience
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Neumorphic Design**: Sophisticated UI with smooth animations
- **Dark Theme**: Eye-friendly interface optimized for long coding sessions
- **Responsive Layout**: Adapts to different screen sizes and workflows

## Quick Start

### Prerequisites
- **Python 3.10+** with pip
- **Node.js 18+** with npm
- **Git** for repository operations

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/tayyab3245/snip-diff.git
   cd snip-diff
   ```

2. **Setup Backend (FastAPI)**
   ```bash
   cd snip-diff-api
   pip install -r requirements.txt
   python app/main.py
   ```
   Backend runs on `http://localhost:8000`

3. **Setup Frontend (Electron)**
   ```bash
   cd snip-diff-electron
   npm install
   npm start
   ```

4. **Start Using SNIP-DIFF**
   - Open your Git repository
   - Browse files and view diffs
   - Generate AI-optimized code snippets
   - Copy to clipboard for your LLM conversations

## Use Cases

### **For AI-Assisted Development**
- **Code Review**: Generate concise summaries of code changes for AI review
- **Bug Analysis**: Create focused code snippets for debugging with AI
- **Refactoring**: Share specific code sections with AI for refactoring suggestions
- **Documentation**: Generate code examples with proper context

### **For Technical Communication**
- **Team Collaboration**: Share precise code diffs with colleagues
- **Pull Request Reviews**: Create focused diff snippets for PR discussions
- **Knowledge Sharing**: Export code examples with syntax highlighting

### **For LLM Context Management**
- **Token Optimization**: Ensure your code fits within model context limits
- **Provider Adaptation**: Format snippets for different AI model requirements
- **Context Preservation**: Maintain code relationships and dependencies

## Key Features

### **File Operations**
- ✅ Browse local file systems and Git repositories
- ✅ Real-time file watching and change detection
- ✅ Syntax highlighting for 100+ programming languages
- ✅ Directory tree navigation with search and filtering

### **Diff Processing**
- ✅ Git diff analysis and visualization
- ✅ Side-by-side and unified diff views
- ✅ Change highlighting and line-by-line comparison
- ✅ Live diff updates during development

### **AI Integration**
- ✅ Google Gemini AI for intelligent summarization
- ✅ Token counting for major LLM providers
- ✅ Context-aware snippet generation
- ✅ Export formats optimized for AI consumption

### **User Experience**
- ✅ Native desktop application (no web browser required)
- ✅ Keyboard shortcuts and accessibility features
- ✅ Dark theme optimized for coding
- ✅ Responsive design for different workflows

## Technical Architecture

### **Backend (FastAPI + Python)**
- High-performance async API server
- Git operations and file system access
- AI service integration (Gemini API)
- WebSocket support for real-time updates

### **Frontend (Electron + React + TypeScript)**
- Cross-platform desktop application
- Modern React 18 with hooks
- TypeScript for type safety
- Neumorphic design system

### **Core Components**
- **Diff Engine**: Advanced file comparison algorithms
- **Snapshot System**: Version control and change tracking
- **Token Estimator**: LLM context optimization
- **Watch Service**: Real-time file monitoring

## API Reference

The SNIP-DIFF backend provides a REST API for integrations:

- `GET /api/files/tree` - Browse directory structure
- `POST /api/diff/scan` - Analyze repository changes
- `GET /api/diff/live/{file_path}` - Live diff for specific file
- `POST /api/summarize` - AI-powered change summarization
- `GET /health` - Service health check

Full API documentation available at `http://localhost:8000/docs`

## Contributing

SNIP-DIFF is an open-source project focused on improving AI-assisted development workflows. Contributions are welcome!

### Development Setup
1. Follow the Quick Start guide above
2. Make changes to backend/frontend as needed
3. Test your changes thoroughly
4. Submit a pull request

### Areas for Contribution
- New AI provider integrations
- Additional export formats
- Performance optimizations
- UI/UX improvements
- Bug fixes and feature requests

## License

**Apache License 2.0**

This software is licensed under the Apache License, Version 2.0. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

## Acknowledgments

Built with modern web technologies and powered by AI to enhance developer productivity. Special thanks to the open-source community for the amazing tools that make this possible.

---

**Copyright © 2025 Tayyab. All Rights Reserved.**

*Empowering developers to work smarter with AI through intelligent code diffing and context management.*
