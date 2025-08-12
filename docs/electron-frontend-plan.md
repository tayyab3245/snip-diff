# SNIP-DIFF Electron Frontend Implementation Plan

## Project Structure
```
snip-diff-electron/
├── src/
│   ├── main/                   # Electron main process
│   │   ├── main.ts            # Entry point
│   │   ├── preload.ts         # IPC bridge
│   │   └── api-client.ts      # FastAPI communication
│   ├── renderer/              # Frontend app
│   │   ├── components/
│   │   │   ├── FileTree.tsx   # Modern file explorer
│   │   │   ├── DiffView.tsx   # Beautiful diff display
│   │   │   ├── StatusBar.tsx  # Live status updates
│   │   │   └── NeumorphicUI/  # Design system
│   │   ├── hooks/
│   │   │   ├── useApi.ts      # FastAPI integration
│   │   │   ├── useWebSocket.ts # Real-time updates
│   │   │   └── useTheme.ts    # Theme management
│   │   ├── store/             # State management (Redux/Zustand)
│   │   │   ├── fileStore.ts
│   │   │   ├── diffStore.ts
│   │   │   └── uiStore.ts
│   │   ├── styles/
│   │   │   ├── neumorphic.css # Your existing design
│   │   │   └── themes.css     # Dark/Light themes
│   │   └── App.tsx
│   └── shared/
│       ├── types.ts           # TypeScript definitions
│       └── constants.ts
├── package.json
├── electron-builder.yml       # Distribution config
├── vite.config.ts            # Build tool
└── README.md
```

## Technology Stack

### Frontend Framework Options:

**Option A: React + TypeScript (RECOMMENDED)**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0",
    "zustand": "^4.4.0",           // State management
    "react-query": "^3.39.0",     // API state management
    "framer-motion": "^10.16.0",   // Animations
    "styled-components": "^6.0.0"  // CSS-in-JS
  }
}
```

**Option B: Vue 3 + TypeScript**
```json
{
  "dependencies": {
    "vue": "^3.3.0",
    "@vue/typescript": "^5.0.0",
    "pinia": "^2.1.0",            // State management
    "vue-query": "^1.26.0",       // API integration
    "@vueuse/core": "^10.5.0"     // Composition utilities
  }
}
```

## Electron Configuration

```typescript
// src/main/main.ts
import { app, BrowserWindow, ipcMain } from 'electron';
import { spawn } from 'child_process';
import path from 'path';

class SnipDiffApp {
  private mainWindow: BrowserWindow | null = null;
  private apiProcess: any = null;

  async initialize() {
    await app.whenReady();
    
    // Start FastAPI backend
    await this.startApiServer();
    
    // Create main window
    this.createMainWindow();
    
    // Setup IPC handlers
    this.setupIpcHandlers();
  }

  private async startApiServer() {
    // Start Python FastAPI server as subprocess
    this.apiProcess = spawn('python', ['-m', 'uvicorn', 'app.main:app', '--port', '8000'], {
      cwd: path.join(__dirname, '../../api'),
      stdio: 'pipe'
    });
    
    // Wait for server to be ready
    await this.waitForApiServer();
  }

  private createMainWindow() {
    this.mainWindow = new BrowserWindow({
      width: 1200,
      height: 800,
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, 'preload.js')
      },
      titleBarStyle: 'hidden',    // Custom title bar
      frame: false                // Frameless for modern look
    });

    // Load the React app
    if (process.env.NODE_ENV === 'development') {
      this.mainWindow.loadURL('http://localhost:3000');
    } else {
      this.mainWindow.loadFile('dist/index.html');
    }
  }

  private setupIpcHandlers() {
    // Bridge between Electron and React
    ipcMain.handle('api-request', async (event, options) => {
      // Proxy API requests to FastAPI backend
      return await this.makeApiRequest(options);
    });

    ipcMain.handle('select-folder', async () => {
      // Folder selection dialog
      const { dialog } = await import('electron');
      return await dialog.showOpenDialog(this.mainWindow!, {
        properties: ['openDirectory']
      });
    });
  }
}

new SnipDiffApp().initialize();
```

## Modern UI Components

### File Tree Component (React)
```tsx
// src/renderer/components/FileTree.tsx
import React, { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import { NeumorphicContainer } from './NeumorphicUI';

interface FileNode {
  path: string;
  name: string;
  type: 'file' | 'directory';
  children?: FileNode[];
  selected?: boolean;
}

export const FileTree: React.FC = () => {
  const [fileTree, setFileTree] = useState<FileNode[]>([]);
  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set());
  const { get, isLoading } = useApi();

  const loadFileTree = async (projectPath: string) => {
    const response = await get(`/api/files/tree?path=${projectPath}`);
    setFileTree(response.data);
  };

  const toggleFileSelection = (filePath: string) => {
    const newSelection = new Set(selectedFiles);
    if (newSelection.has(filePath)) {
      newSelection.delete(filePath);
    } else {
      newSelection.add(filePath);
    }
    setSelectedFiles(newSelection);
  };

  return (
    <NeumorphicContainer className="file-tree">
      <div className="file-tree-header">
        <h3>Project Files</h3>
        <button onClick={() => window.electronAPI.selectFolder()}>
          Choose Folder
        </button>
      </div>
      
      <div className="file-tree-content">
        {fileTree.map(node => (
          <FileTreeNode 
            key={node.path}
            node={node}
            selectedFiles={selectedFiles}
            onToggle={toggleFileSelection}
          />
        ))}
      </div>
    </NeumorphicContainer>
  );
};
```

### Beautiful Diff Display
```tsx
// src/renderer/components/DiffView.tsx
import React from 'react';
import { motion } from 'framer-motion';
import { useDiffStore } from '../store/diffStore';

export const DiffView: React.FC = () => {
  const { sections, isLoading } = useDiffStore();

  return (
    <div className="diff-view">
      <div className="instructions-panel">
        <textarea 
          placeholder="Add AI instructions..."
          className="neumorphic-textarea"
        />
        <div className="controls">
          <select className="position-control">
            <option value="prepend">Prepend</option>
            <option value="append">Append</option>
          </select>
          <button className="copy-button neumorphic-button">
            Copy All
          </button>
        </div>
      </div>

      <div className="diff-sections">
        {sections.map((section, index) => (
          <motion.div
            key={section.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="diff-section neumorphic-card"
          >
            <div className="section-header">
              <h4>{section.title}</h4>
              <span className={`status-badge ${section.changeType}`}>
                {section.changeType}
              </span>
            </div>
            <pre className="section-content">
              <code>{section.content}</code>
            </pre>
          </motion.div>
        ))}
      </div>
    </div>
  );
};
```

## Real-time Communication

```typescript
// src/renderer/hooks/useWebSocket.ts
import { useEffect, useRef } from 'react';
import { useDiffStore } from '../store/diffStore';

export const useWebSocket = (url: string) => {
  const ws = useRef<WebSocket | null>(null);
  const { updateDiffResults } = useDiffStore();

  useEffect(() => {
    ws.current = new WebSocket(url);
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'file_changed':
          // Trigger automatic diff update
          updateDiffResults(data.scanResults);
          break;
        case 'scan_complete':
          // Update UI with new results
          updateDiffResults(data.sections);
          break;
      }
    };

    return () => {
      ws.current?.close();
    };
  }, [url]);

  const sendMessage = (message: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  };

  return { sendMessage };
};
```

## Distribution Strategy

```yaml
# electron-builder.yml
appId: com.tayyab.snip-diff
productName: SNIP-DIFF
directories:
  output: dist
  buildResources: build
files:
  - "dist/**/*"
  - "api/**/*"            # Include Python API
  - "!**/node_modules/*"
extraResources:
  - "python-runtime/"     # Bundled Python runtime
win:
  target: nsis
  icon: assets/icon.ico
mac:
  target: dmg
  icon: assets/icon.icns
linux:
  target: AppImage
  icon: assets/icon.png
```
