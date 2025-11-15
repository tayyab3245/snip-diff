/**
 * Electron Main Process for SNIP-DIFF
 * Handles window management, IPC, and FastAPI backend communication
 */

import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';
import * as os from 'os';
import chokidar, { FSWatcher } from 'chokidar';

class SnipDiffApp {
  private mainWindow: BrowserWindow | null = null;
  private apiProcess: ChildProcess | null = null;
  private fileWatcher: FSWatcher | null = null;
  private watchedFiles: Set<string> = new Set();
  private readonly isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

  constructor() {
    // Enable verbose logging in development
    if (this.isDev) {
      app.commandLine.appendSwitch('enable-logging');
      app.commandLine.appendSwitch('v', '1');
    }
  }

  async initialize() {
    console.log('=== SNIP-DIFF Application Starting ===');
    console.log(`Mode: ${this.isDev ? 'DEVELOPMENT' : 'PRODUCTION'}`);
    console.log(`Platform: ${process.platform}`);
    console.log(`Electron: ${process.versions.electron}`);
    console.log(`Chrome: ${process.versions.chrome}`);
    console.log(`Node: ${process.versions.node}`);
    
    await app.whenReady();
    
    // Start FastAPI backend
    await this.startApiServer();
    
    // Create main window
    this.createMainWindow();
    
    // Setup IPC handlers
    this.setupIpcHandlers();
    
    // Handle app events
    this.setupAppEvents();
  }

  private async startApiServer() {
    if (this.isDev) {
      // Development mode: connect to external API server
      console.log('Development mode: connecting to external API server...');
      try {
        await this.waitForApiServer();
        console.log('Connected to external FastAPI server');
      } catch (error) {
        console.log('Could not connect to external API server, will continue without it');
      }
      return;
    }

    // Production mode: start the API server
    try {
      console.log('Starting FastAPI backend server...');
      const apiPath = path.join(process.resourcesPath, 'api');
      const pythonPath = process.platform === 'win32' ? 'python.exe' : 'python3';

      this.apiProcess = spawn(pythonPath, ['-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000'], {
        cwd: apiPath,
        stdio: 'pipe'
      });

      if (this.apiProcess.stderr) {
        this.apiProcess.stderr.on('data', (data) => {
          console.error('API Error:', data.toString());
        });
      }

      if (this.apiProcess.stdout) {
        this.apiProcess.stdout.on('data', (data) => {
          console.log('API Output:', data.toString());
        });
      }

      this.apiProcess.on('error', (error) => {
        console.error('Failed to start API server:', error);
      });

      // Wait for server to be ready
      await this.waitForApiServer();
      console.log('FastAPI server started successfully');
      
    } catch (error) {
      console.error('Error starting API server:', error);
    }
  }

  private async waitForApiServer(maxRetries: number = 30): Promise<void> {
    for (let i = 0; i < maxRetries; i++) {
      try {
        // Try to connect to the API server
        const response = await fetch('http://127.0.0.1:8000/api/health');
        if (response.ok) {
          return;
        }
      } catch (error) {
        // Server not ready yet, wait and retry
      }
      
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    throw new Error('API server failed to start within timeout period');
  }

  private createMainWindow() {
    console.log('isDev:', this.isDev, 'NODE_ENV:', process.env.NODE_ENV, 'isPackaged:', app.isPackaged);
    
    this.mainWindow = new BrowserWindow({
      width: 1400,
      height: 900,
      minWidth: 1000,
      minHeight: 700,
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, 'preload.js'),
        webSecurity: this.isDev ? false : true // Allow CORS in development
      },
      titleBarStyle: 'hidden',
      frame: false,
      backgroundColor: '#e0e5ec', // Neumorphic background
      show: false, // Don't show until ready
      icon: this.isDev 
        ? path.join(__dirname, '../../../assets/icon.png')
        : path.join(process.resourcesPath, 'icon.png')
    });

    // Load the React app
    if (this.isDev) {
      this.mainWindow.loadURL('http://localhost:5173');
      this.mainWindow.webContents.openDevTools();
    } else {
      this.mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
    }

    // Show window when ready
    this.mainWindow.once('ready-to-show', () => {
      console.log('Window ready to show');
      this.mainWindow?.show();
    });

    // Forward renderer console logs to main process
    this.mainWindow.webContents.on('console-message', (event, level, message, line, sourceId) => {
      const logLevel = ['LOG', 'WARNING', 'ERROR'][level] || 'LOG';
      console.log(`[RENDERER ${logLevel}] ${message} (${sourceId}:${line})`);
    });

    // Log navigation events
    this.mainWindow.webContents.on('did-start-loading', () => {
      console.log('Renderer: Started loading');
    });

    this.mainWindow.webContents.on('did-finish-load', () => {
      console.log('Renderer: Finished loading');
    });

    this.mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
      console.error(`Renderer: Failed to load - ${errorCode}: ${errorDescription}`);
    });

    // Handle window closed
    this.mainWindow.on('closed', () => {
      console.log('Main window closed');
      this.mainWindow = null;
    });
  }

  private setupIpcHandlers() {
    // Start watching files
    ipcMain.handle('start-watch', async (event, filePaths: string[]) => {
      try {
        console.log('[Watch] Starting watch for files:', filePaths);
        
        // Stop existing watcher if any
        if (this.fileWatcher) {
          await this.fileWatcher.close();
          this.fileWatcher = null;
        }
        
        // Clear watched files
        this.watchedFiles.clear();
        filePaths.forEach(fp => this.watchedFiles.add(fp));
        
        // Create new watcher
        this.fileWatcher = chokidar.watch(filePaths, {
          persistent: true,
          ignoreInitial: true,
          awaitWriteFinish: {
            stabilityThreshold: 100,
            pollInterval: 50
          }
        });
        
        // Handle file changes
        this.fileWatcher.on('change', async (filePath: string) => {
          console.log('[Watch] File changed:', filePath);
          
          // Notify renderer about the change
          if (this.mainWindow && !this.mainWindow.isDestroyed()) {
            this.mainWindow.webContents.send('file-changed', filePath);
          }
        });
        
        this.fileWatcher.on('error', (error) => {
          console.error('[Watch] Error:', error);
        });
        
        console.log('[Watch] Started successfully');
        return { success: true };
        
      } catch (error) {
        console.error('[Watch] Failed to start:', error);
        return { 
          success: false, 
          error: error instanceof Error ? error.message : 'Unknown error' 
        };
      }
    });
    
    // Stop watching files
    ipcMain.handle('stop-watch', async () => {
      try {
        console.log('[Watch] Stopping watch');
        
        if (this.fileWatcher) {
          await this.fileWatcher.close();
          this.fileWatcher = null;
        }
        
        this.watchedFiles.clear();
        
        console.log('[Watch] Stopped successfully');
        return { success: true };
        
      } catch (error) {
        console.error('[Watch] Failed to stop:', error);
        return { 
          success: false, 
          error: error instanceof Error ? error.message : 'Unknown error' 
        };
      }
    });

    // API request handler - proxy requests to FastAPI backend
    ipcMain.handle('api-request', async (event, options: {
      method: string;
      endpoint: string;
      data?: any;
      params?: Record<string, string>;
    }) => {
      try {
        const { method, endpoint, data, params } = options;
        
        // Build URL with params
        const url = new URL(`http://127.0.0.1:8000${endpoint}`);
        if (params) {
          Object.entries(params).forEach(([key, value]) => {
            url.searchParams.append(key, value);
          });
        }

        console.log(`[API Request] ${method} ${url.toString()}`);
        if (params) {
          console.log('[API Request] Params:', params);
        }

        const fetchOptions: RequestInit = {
          method: method.toUpperCase(),
          headers: {
            'Content-Type': 'application/json',
          },
        };

        if (data && ['POST', 'PUT', 'PATCH'].includes(method.toUpperCase())) {
          fetchOptions.body = JSON.stringify(data);
        }

        const response = await fetch(url.toString(), fetchOptions);
        const responseData = await response.json();

        console.log(`[API Response] Status: ${response.status}, OK: ${response.ok}`);
        console.log('[API Response] Data:', responseData);

        return {
          success: response.ok,
          status: response.status,
          data: responseData
        };

      } catch (error) {
        console.error('API request error:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error'
        };
      }
    });

    // Folder selection dialog
    ipcMain.handle('select-folder', async () => {
      if (!this.mainWindow) return null;

      const result = await dialog.showOpenDialog(this.mainWindow, {
        properties: ['openDirectory'],
        title: 'Select Project Folder'
      });

      return result.canceled ? null : result.filePaths[0];
    });

    // File selection dialog
    ipcMain.handle('select-files', async () => {
      if (!this.mainWindow) return null;

      const result = await dialog.showOpenDialog(this.mainWindow, {
        properties: ['openFile', 'multiSelections'],
        title: 'Select Files',
        filters: [
          { name: 'All Files', extensions: ['*'] },
          { name: 'Text Files', extensions: ['txt', 'md', 'json', 'js', 'ts', 'py', 'html', 'css'] }
        ]
      });

      return result.canceled ? null : result.filePaths;
    });

    // Window controls for frameless window
    ipcMain.handle('window-minimize', () => {
      this.mainWindow?.minimize();
    });

    ipcMain.handle('window-maximize', () => {
      if (this.mainWindow?.isMaximized()) {
        this.mainWindow.unmaximize();
      } else {
        this.mainWindow?.maximize();
      }
    });

    ipcMain.handle('window-close', () => {
      this.mainWindow?.close();
    });

    // Get app version
    ipcMain.handle('get-app-version', () => {
      return app.getVersion();
    });
  }

  private setupAppEvents() {
    app.on('window-all-closed', () => {
      if (process.platform !== 'darwin') {
        this.cleanup();
        app.quit();
      }
    });

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        this.createMainWindow();
      }
    });

    app.on('before-quit', () => {
      this.cleanup();
    });
  }

  private cleanup() {
    // Close file watcher
    if (this.fileWatcher) {
      console.log('Closing file watcher...');
      this.fileWatcher.close();
      this.fileWatcher = null;
    }
    
    // Terminate API server
    if (this.apiProcess) {
      console.log('Terminating API server...');
      this.apiProcess.kill();
      this.apiProcess = null;
    }
  }
}

// Initialize the app
const snipDiffApp = new SnipDiffApp();
snipDiffApp.initialize().catch((error) => {
  console.error('Fatal error during initialization:', error);
  app.quit();
});
