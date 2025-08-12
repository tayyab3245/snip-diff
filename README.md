# SNIP-DIFF

```
███████╗███╗   ██╗██╗██████╗       ██████╗ ██╗███████╗███████╗
██╔════╝████╗  ██║██║██╔══██╗      ██╔══██╗██║██╔════╝██╔════╝
███████╗██╔██╗ ██║██║██████╔╝█████╗██║  ██║██║█████╗  █████╗  
╚════██║██║╚██╗██║██║██╔═══╝ ╚════╝██║  ██║██║██╔══╝  ██╔══╝  
███████║██║ ╚████║██║██║           ██████╔╝██║██║     ██║     
╚══════╝╚═╝  ╚═══╝╚═╝╚═╝           ╚═════╝ ╚═╝╚═╝     ╚═╝     
                                                              
    ⚡ Modern Full-Stack AI Workflow Tool ⚡
```

**Next-generation full-stack application for AI-assisted development workflows**

![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Electron](https://img.shields.io/badge/Electron-191970?style=flat&logo=Electron&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)

## 🚀 Architecture Overview

SNIP-DIFF has been completely transformed into a modern full-stack application:

### **🔧 Backend: FastAPI API Server**
- **Modern Python API**: High-performance async FastAPI backend
- **RESTful Endpoints**: Clean API design for file operations and diff processing
- **Extracted Core Logic**: Reusable business logic decoupled from UI
- **CORS Enabled**: Ready for cross-origin requests from Electron frontend

### **💻 Frontend: Electron + React + TypeScript**
- **Cross-Platform Desktop**: Native desktop experience with web technologies
- **Modern React 18**: Component-based UI with hooks and functional components
- **TypeScript**: Full type safety and enhanced developer experience
- **Neumorphic Design**: Sophisticated UI with custom styling and animations

### **📁 Project Structure**
```
snip-diff/
├── snip-diff-api/          # FastAPI Backend
│   ├── app/
│   │   ├── api/routes/     # API endpoints
│   │   ├── core/           # Business logic
│   │   └── main.py         # FastAPI application
│   └── requirements.txt
├── snip-diff-electron/     # Electron Frontend
│   ├── src/
│   │   ├── main/           # Electron main process
│   │   ├── preload/        # IPC bridge
│   │   └── renderer/       # React UI components
│   ├── package.json
│   └── tsconfig.json
├── legacy/                 # Original PySide6 implementation
└── docs/                   # Documentation and planning
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** with pip
- **Node.js 18+** with npm
- **Git** for version control

### 🔧 Backend Setup (FastAPI)
```bash
cd snip-diff-api
pip install -r requirements.txt
python app/main.py
```
Server runs on `http://localhost:8000` with API docs at `/docs`

### 💻 Frontend Setup (Electron)
```bash
cd snip-diff-electron
npm install
npm start
```

### 🎯 Development Workflow
1. Start FastAPI backend server
2. Launch Electron frontend in development mode
3. Both services auto-reload on file changes
4. Access API documentation for endpoint testing

## 🌟 Current Features

### **Core Functionality** ✅
- **File Tree Browsing**: Interactive directory navigation via API
- **Diff Processing**: Advanced file comparison and change detection
- **REST API**: Clean endpoints for file operations and diff processing
- **Cross-Platform Desktop**: Native desktop experience with Electron

### **Modern Architecture** ✅
- **Async FastAPI Backend**: High-performance Python API server
- **React + TypeScript Frontend**: Type-safe component-based UI
- **IPC Communication**: Seamless frontend-backend integration
- **Modular Design**: Separated concerns for maintainability

## 🗺️ Development Roadmap

### **Phase 1: Foundation** ✅ *COMPLETED*
- [x] FastAPI backend with core file operations
- [x] Electron + React frontend scaffold
- [x] Basic API endpoints (`/api/files/tree`, `/api/diff/scan`)
- [x] Project structure and development environment

### **Phase 2: Core Features** 🔄 *IN PROGRESS*
- [ ] File selection and management UI
- [ ] Real-time diff processing and display
- [ ] Copy-to-clipboard functionality
- [ ] Theme system (light/dark mode)
- [ ] Basic error handling and user feedback

### **Phase 3: Enhanced UX** 📋 *PLANNED*
- [ ] Neumorphic design system implementation
- [ ] Advanced file filtering and search
- [ ] Keyboard shortcuts and accessibility
- [ ] Performance optimizations
- [ ] User preferences and settings

### **Phase 4: AI Integration** 🎯 *PLANNED*
- [ ] Token counting and LLM optimization
- [ ] Context size management
- [ ] AI provider-specific formatting
- [ ] Smart file relevance scoring
- [ ] Export presets for different AI models

## 🧪 API Documentation

The FastAPI backend provides comprehensive API documentation:
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc (Alternative documentation)
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Key Endpoints
- `GET /api/files/tree?path={directory}` - Browse file system
- `POST /api/diff/scan` - Process directory for changes
- `GET /health` - Service health check

## 🏗️ Legacy Support

The original PySide6 implementation has been preserved in the `legacy/` directory for reference and fallback purposes. The new full-stack architecture provides:

- **Better Performance**: Async backend with optimized API calls
- **Enhanced Maintainability**: Separated frontend and backend concerns
- **Modern Development**: React ecosystem and TypeScript safety
- **Future Scalability**: API-first design for potential web version

---

**Copyright © 2025 Tayyab. All Rights Reserved.**

*This software is proprietary and confidential. Built for the AI development community with professional-grade features and design.*
