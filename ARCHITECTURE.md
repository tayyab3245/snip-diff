# SNIP-DIFF Architecture

## 🏗️ Project Structure

```
snip-diff-electron/
├── src/
│   ├── main/              # 🔧 BACKEND (Node.js - Electron Main Process)
│   │   ├── services/      # Business logic
│   │   │   ├── git-service.ts      # Git operations (diff, status, content)
│   │   │   └── llm-service.ts      # Gemini AI summarization
│   │   ├── main.ts        # Entry point: window creation, IPC handlers
│   │   ├── preload.ts     # Security bridge: exposes safe APIs to frontend
│   │   └── tsconfig.json  # Backend TypeScript config (CommonJS, Node.js)
│   │
│   ├── renderer/          # 🎨 FRONTEND (React + Vite)
│   │   ├── components/    # React UI components
│   │   │   ├── action-bar.tsx      # Top action buttons
│   │   │   ├── context-bar.tsx     # Context controls
│   │   │   ├── diff-view.tsx       # Diff display
│   │   │   ├── file-tree.tsx       # File browser
│   │   │   ├── layout.tsx          # Layout container
│   │   │   ├── title-bar.tsx       # Custom window title bar
│   │   │   └── tool-bar.tsx        # Bottom toolbar
│   │   ├── hooks/         # Custom React hooks
│   │   │   ├── use-api-client.ts   # API communication
│   │   │   └── use-live-diff.ts    # File watching & diff updates
│   │   ├── store/         # State management (Zustand)
│   │   │   └── app-store.ts        # Global app state
│   │   ├── theme/         # Design system
│   │   │   ├── dark-theme.ts       # Dark theme colors
│   │   │   ├── tokens.ts           # Design tokens
│   │   │   └── theme-provider.tsx  # Theme context
│   │   ├── app.tsx        # Root React component
│   │   ├── main.tsx       # React entry point (ReactDOM.render)
│   │   └── index.html     # HTML shell
│   │
│   └── shared/            # 🔗 SHARED (Types & Constants)
│       ├── types.ts       # TypeScript interfaces (Git, LLM, Electron API)
│       └── constants.ts   # App constants (config, window settings)
│
├── dist/                  # 📦 Build output
│   ├── main/             # Compiled backend
│   └── renderer/         # Compiled frontend
│
├── package.json          # Dependencies & scripts
├── tsconfig.json         # Frontend TypeScript config (ESNext, React)
├── tsconfig.node.json    # Vite config TypeScript settings
├── vite.config.ts        # Vite bundler configuration
└── .env                  # Environment variables (GEMINI_API_KEY)
```

---

## 🔄 Architecture Overview

### Electron Multi-Process Model

**IMPORTANT:** Electron applications MUST have separate processes for security and performance:

```
┌─────────────────────────────────────────────────────────┐
│                    Electron App                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐      ┌──────────────┐     ┌─────────┐ │
│  │ Main Process │────▶│   Preload    │────▶│Renderer │ │
│  │  (Backend)   │     │   (Bridge)   │     │(Frontend)│ │
│  │   Node.js    │     │   Security   │     │  React  │ │
│  │              │     │              │     │ Chromium│ │
│  └──────────────┘     └──────────────┘     └─────────┘ │
│   • Git Service         • IPC Bridge         • UI      │
│   • LLM Service         • Type Safety        • State   │
│   • File Watch          • Context Bridge     • Hooks   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Why Multiple TypeScript Configs?

### 1. **Root `tsconfig.json`** - Frontend Configuration
- **Target:** React renderer process
- **Module System:** ESNext (for Vite)
- **JSX:** React JSX support
- **Includes:** `src/renderer`, `src/shared`
- **Used by:** Vite bundler for frontend

### 2. **`src/main/tsconfig.json`** - Backend Configuration
- **Target:** Node.js main process
- **Module System:** CommonJS (Electron compatibility)
- **No JSX:** Pure TypeScript/Node.js
- **Output:** `dist/main`
- **Used by:** TypeScript compiler for backend

### 3. **`tsconfig.node.json`** - Build Tools Configuration
- **Target:** Vite config file
- **Module System:** ESNext
- **Used by:** `vite.config.ts` compilation

**Why separate?** Backend (Node.js) and frontend (browser) need different compilation settings.

---

## 🔐 Security Model: Why Preload?

**Problem:** Renderer (Chromium) shouldn't have direct Node.js access (security risk)

**Solution:** Preload script acts as a secure bridge:

```typescript
// ❌ UNSAFE: Renderer directly using Node.js
import fs from 'fs'; // NO! Security vulnerability

// ✅ SAFE: Renderer uses preload-exposed API
window.electronAPI.selectFolder(); // Safe IPC call
```

**Flow:**
1. Renderer calls `window.electronAPI.getGitDiff()`
2. Preload forwards via IPC to main process
3. Main process executes Git command (has Node.js access)
4. Result sent back through IPC to renderer

---

## 🧩 Separation of Concerns

### Backend (`src/main/`)
**Responsibility:** Business logic, system operations, security
- Git operations (exec git commands)
- LLM API calls (Gemini)
- File system watching (Chokidar)
- IPC handlers (receive requests from frontend)

### Frontend (`src/renderer/`)
**Responsibility:** User interface, user interactions
- React components (UI rendering)
- State management (Zustand)
- User events (clicks, selections)
- Display logic only (no system access)

### Shared (`src/shared/`)
**Responsibility:** Common types and constants
- TypeScript interfaces (contract between frontend/backend)
- App constants
- No business logic

---

## 🚀 Development Flow

### Starting the App
```bash
npm run dev
```
1. Vite starts → React dev server on `localhost:5173`
2. TypeScript compiles `src/main/` → `dist/main/`
3. Electron launches → loads React from Vite

### Build for Production
```bash
npm run build
```
1. Vite bundles React → `dist/renderer/`
2. TypeScript compiles backend → `dist/main/`
3. Electron Builder packages → executable

---

## 📦 Key Technologies

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Desktop Shell** | Electron 28 | Cross-platform desktop app |
| **Frontend** | React 18 + TypeScript | UI framework |
| **Backend** | Node.js + TypeScript | Business logic |
| **Bundler** | Vite 5 | Fast dev server & build |
| **State** | Zustand | Lightweight state management |
| **Styling** | Framer Motion | Animations & theme |
| **Git** | Native `git` CLI | Diff operations |
| **AI** | Google Gemini 1.5 Flash | Code summarization |
| **Watch** | Chokidar | File system monitoring |

---

## 🎯 Use Cases

1. **Copy Files to LLM** - Select files → Copy All → paste to ChatGPT
2. **Summarize Files** - Select files → Summarize → Copy → paste to LLM (less tokens)
3. **Git Change Detection** - Auto-detect modified files → select → view diff → copy
4. **Summarize Diffs** - View diff → Summarize Diff → Copy (optimized for LLM context)

---

## 🔑 Environment Setup

Create `.env` file in `snip-diff-electron/`:
```env
GEMINI_API_KEY=your_google_ai_studio_api_key
```

Get API key: https://aistudio.google.com/app/apikey

---

## 📚 File Naming Conventions

- **Components:** `kebab-case.tsx` (e.g., `file-tree.tsx`)
- **Hooks:** `use-*.ts` (e.g., `use-live-diff.ts`)
- **Services:** `*-service.ts` (e.g., `git-service.ts`)
- **Types:** `types.ts` (centralized)
- **Constants:** `constants.ts` (centralized)

---

## 🛠️ Common Tasks

### Add New Backend Service
1. Create `src/main/services/my-service.ts`
2. Export service instance
3. Import in `main.ts`
4. Add IPC handler in `main.ts`
5. Expose in `preload.ts`
6. Add type to `shared/types.ts` → `ElectronAPI` interface

### Add New React Component
1. Create `src/renderer/components/my-component.tsx`
2. Import in parent component or `app.tsx`
3. Use Zustand store for state if needed

### Add New Type
1. Edit `src/shared/types.ts`
2. Both frontend and backend can import
3. Keep types organized by category

---

## ✅ This Structure is CORRECT

The current organization follows **Electron best practices**:
- ✅ Clear frontend/backend separation
- ✅ Secure IPC communication
- ✅ Proper TypeScript configuration for each target
- ✅ Logical folder grouping (components, services, shared)
- ✅ No unnecessary nesting

**The "multiple configs" and "subfolders" are NOT messy - they're required for Electron architecture!**
