/**
 * Electron Main Process for SNIP-DIFF
 * Handles window management, IPC, and FastAPI backend communication
 */

/// <reference types="node" />

import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import * as path from 'path';
import chokidar, { FSWatcher } from 'chokidar';
import { gitService } from './services/git-service';
import { llmService } from './services/llm-service';
import { FileService } from './services/file-service';

class SnipDiffApp {
  private mainWindow: BrowserWindow | null = null;
  private fileWatcher: FSWatcher | null = null;
  private watchedFiles: Set<string> = new Set();
  private readonly isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;
  private fileService = new FileService();

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
    console.log(`LLM Service: ${llmService.isAvailable() ? 'Available' : 'Not configured'}`);
    
    await app.whenReady();
    
    // Create main window
    this.createMainWindow();
    
    // Setup IPC handlers
    this.setupIpcHandlers();
    
    // Handle app events
    this.setupAppEvents();
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
        : path.join((process as any).resourcesPath, 'icon.png')
    });

    // Load the React app
    if (this.isDev) {
      this.mainWindow.loadURL('http://localhost:5173');
      this.mainWindow.webContents.openDevTools();
    } else {
      this.mainWindow.loadFile(path.join(__dirname, '../ui/index.html'));
    }

    // Show window when ready
    this.mainWindow.once('ready-to-show', () => {
      console.log('Window ready to show');
      this.mainWindow?.show();
    });

    // Forward renderer console logs to main process
    this.mainWindow.webContents.on('console-message', (_event: Electron.Event, level: number, message: string, line: number, sourceId: string) => {
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

    this.mainWindow.webContents.on('did-fail-load', (_event: Electron.Event, errorCode: number, errorDescription: string) => {
      console.error(`Renderer: Failed to load - ${errorCode}: ${errorDescription}`);
    });

    // Handle window closed
    this.mainWindow.on('closed', () => {
      console.log('Main window closed');
      this.mainWindow = null;
    });
  }

  private setupIpcHandlers() {
    // Get Git diff for files
    ipcMain.handle('get-git-diff', async (_event: Electron.IpcMainInvokeEvent, directory: string, filePaths?: string[]) => {
      try {
        console.log('[Git] Getting diff for:', directory, filePaths);
        const result = await gitService.getDiff(directory, filePaths);
        console.log('[Git] Diff result:', result);
        return result;
      } catch (error) {
        console.error('[Git] Error getting diff:', error);
        return {
          success: false,
          files: [],
          error: error instanceof Error ? error.message : 'Unknown error'
        };
      }
    });

    // Get file content from Git
    ipcMain.handle('get-git-file-content', async (_event: Electron.IpcMainInvokeEvent, directory: string, filePath: string, ref?: string) => {
      try {
        const content = await gitService.getFileContent(directory, filePath, ref);
        return { success: true, content };
      } catch (error) {
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error'
        };
      }
    });

    // Check if directory is a Git repo
    ipcMain.handle('is-git-repo', async (_event: Electron.IpcMainInvokeEvent, directory: string) => {
      try {
        const isRepo = await gitService.isGitRepo(directory);
        return { success: true, isRepo };
      } catch (error) {
        return { success: false, isRepo: false };
      }
    });

    // File tree handler
    ipcMain.handle('get-file-tree', async (_event: Electron.IpcMainInvokeEvent, dirPath: string) => {
      console.log('[FileService] Getting file tree for:', dirPath);
      return this.fileService.getFileTree(dirPath);
    });

    // File read handler - single file
    ipcMain.handle('read-file', async (_event: Electron.IpcMainInvokeEvent, filePath: string) => {
      console.log('[FileService] Reading file:', filePath);
      return this.fileService.readFile(filePath);
    });

    // File read handler - multiple files (for batch operations and LLM)
    ipcMain.handle('read-multiple-files', async (_event: Electron.IpcMainInvokeEvent, filePaths: string[]) => {
      console.log('[FileService] Reading multiple files:', filePaths.length, 'files');
      return this.fileService.readMultipleFiles(filePaths);
    });

    // LLM Summarization handlers
    ipcMain.handle('llm-summarize-file', async (_event: Electron.IpcMainInvokeEvent, content: string, filePath: string) => {
      try {
        console.log('[LLM] Summarizing file:', filePath);
        const result = await llmService.summarizeFile(content, filePath);
        console.log('[LLM] Summary result:', result.success ? 'success' : result.error);
        return result;
      } catch (error) {
        console.error('[LLM] Error:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error'
        };
      }
    });

    ipcMain.handle('llm-summarize-diff', async (_event: Electron.IpcMainInvokeEvent, diffContent: string, files: string[]) => {
      try {
        console.log('[LLM] Summarizing diff for files:', files);
        const result = await llmService.summarizeDiff(diffContent, files);
        console.log('[LLM] Diff summary result:', result.success ? 'success' : result.error);
        return result;
      } catch (error) {
        console.error('[LLM] Error:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error'
        };
      }
    });

    ipcMain.handle('llm-summarize-multiple-files', async (_event: Electron.IpcMainInvokeEvent, files: Array<{ path: string; content: string }>) => {
      try {
        console.log('[LLM] Summarizing multiple files:', files.length);
        const result = await llmService.summarizeMultipleFiles(files);
        console.log('[LLM] Multi-file summary result:', result.success ? 'success' : result.error);
        return result;
      } catch (error) {
        console.error('[LLM] Error:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error'
        };
      }
    });

    ipcMain.handle('llm-is-available', async () => {
      return { available: llmService.isAvailable() };
    });

    // Start watching files
    ipcMain.handle('start-watch', async (_event: Electron.IpcMainInvokeEvent, filePaths: string[]) => {
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
    ipcMain.handle('api-request', async (_event: Electron.IpcMainInvokeEvent, options: {
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
  }
}

// Initialize the app
const snipDiffApp = new SnipDiffApp();
snipDiffApp.initialize().catch((error) => {
  console.error('Fatal error during initialization:', error);
  app.quit();
});
