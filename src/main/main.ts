/**
 * Electron Main Process for SNIP-DIFF
 * Handles window management, IPC, and FastAPI backend communication
 */

// Load environment variables from .env file in project root
import * as dotenv from 'dotenv';
import * as path from 'path';
import { app, BrowserWindow, ipcMain, dialog, IpcMainInvokeEvent, Event } from 'electron';

// Load .env - dotenv will search up from cwd for .env file
const dotenvResult = dotenv.config();

console.log('=== Environment Loading Debug ===');
console.log('CWD:', process.cwd());
console.log('Dotenv result:', dotenvResult.error ? 'ERROR: ' + dotenvResult.error.message : 'Success');
console.log('Dotenv parsed keys:', dotenvResult.parsed ? Object.keys(dotenvResult.parsed).length : 0);
console.log('GEMINI_API_KEY present:', !!process.env.GEMINI_API_KEY);
console.log('GEMINI_API_KEY length:', process.env.GEMINI_API_KEY?.length || 0);
console.log('================================');

import { gitService } from './services/git-service';
import { llmService } from './services/llm-service';
import { FileService } from './services/file-service';

class SnipDiffApp {
  private mainWindow: BrowserWindow | null = null;
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
    
    // Initialize LLM service if API key is provided
    const geminiApiKey = process.env.GEMINI_API_KEY;
    console.log('[LLM Init] API key available:', !!geminiApiKey);
    console.log('[LLM Init] API key length:', geminiApiKey?.length || 0);
    
    if (geminiApiKey) {
      try {
        console.log('[LLM Init] Attempting to initialize LLM service...');
        await llmService.initialize(geminiApiKey);
        console.log('[LLM Init] ✓ Initialized with Gemini');
      } catch (error) {
        console.error('[LLM Init] ✗ Failed to initialize:', error);
      }
    } else {
      console.log('[LLM Init] Skipped - no GEMINI_API_KEY in environment');
    }
    
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
    this.mainWindow.webContents.on('console-message', (_event: Event, level: number, message: string, line: number, sourceId: string) => {
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

    this.mainWindow.webContents.on('did-fail-load', (_event: Event, errorCode: number, errorDescription: string) => {
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
    ipcMain.handle('get-git-diff', async (_event: IpcMainInvokeEvent, directory: string, filePaths?: string[], fullContext?: boolean) => {
      try {
        const result = await gitService.getDiff(directory, filePaths, fullContext);
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
    ipcMain.handle('get-git-file-content', async (_event: IpcMainInvokeEvent, directory: string, filePath: string, ref?: string) => {
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
    ipcMain.handle('is-git-repo', async (_event: IpcMainInvokeEvent, directory: string) => {
      try {
        const isRepo = await gitService.isGitRepo(directory);
        return { success: true, isRepo };
      } catch (error) {
        return { success: false, isRepo: false };
      }
    });

    // Get Git status for all files in directory
    ipcMain.handle('get-git-status', async (_event: IpcMainInvokeEvent, directory: string) => {
      try {
        const statuses = await gitService.getStatus(directory);
        return { success: true, statuses };
      } catch (error) {
        console.error('[Git] Error getting status:', error);
        return {
          success: false,
          statuses: [],
          error: error instanceof Error ? error.message : 'Unknown error'
        };
      }
    });

    // File tree handler
    ipcMain.handle('get-file-tree', async (_event: IpcMainInvokeEvent, dirPath: string) => {
      return this.fileService.getFileTree(dirPath);
    });

    // File read handler - single file
    ipcMain.handle('read-file', async (_event: IpcMainInvokeEvent, filePath: string) => {
      return this.fileService.readFile(filePath);
    });

    // File read handler - multiple files (for batch operations and LLM)
    ipcMain.handle('read-multiple-files', async (_event: IpcMainInvokeEvent, filePaths: string[]) => {
      return this.fileService.readMultipleFiles(filePaths);
    });

    // LLM Summarization handlers
    ipcMain.handle('llm-summarize-diff', async (_event: IpcMainInvokeEvent, repoPath: string, files: string[]) => {
      try {
        // Filter out binary and gitignored files
        const filteredFiles = this.fileService.filterFilesForLLM(files);
        console.log('[LLM] Summarizing files:', filteredFiles.length, '(filtered from', files.length, ')');
        
        if (filteredFiles.length === 0) {
          return {
            success: false,
            error: 'No valid files to analyze (all files are binary or ignored)'
          };
        }
        
        // Try to get git diff first
        const diffResult = await gitService.getDiff(repoPath, filteredFiles, false);
        
        let diffContent = '';
        const gitStatus = new Map<string, string>();
        const fileContents = new Map<string, string>();
        
        // If we have diff content, use it
        if (diffResult.success && diffResult.files.length > 0) {
          diffContent = diffResult.files.map(f => f.diff).join('\n\n');
          diffResult.files.forEach(f => gitStatus.set(f.path, f.status));
        } else {
          // No diffs - read full file contents instead
          console.log('[LLM] No diffs found, reading full file contents');
          const fileReadResult = await this.fileService.readMultipleFiles(filteredFiles);
          
          if (fileReadResult.success && fileReadResult.data) {
            fileReadResult.data.forEach((f) => {
              if (f.content) {
                fileContents.set(f.path, f.content);
                // Mark as unchanged in git
                gitStatus.set(f.path, 'Unchanged');
              }
            });
            
            // Create a "diff" representation of the full files
            diffContent = Array.from(fileContents.entries())
              .map(([path, content]) => `=== ${path} ===\n${content}`)
              .join('\n\n');
          }
        }

        if (!diffContent && fileContents.size === 0) {
          return {
            success: false,
            error: 'No content to summarize'
          };
        }

        // Build context for AI
        const context = {
          repoPath,
          selectedFiles: filteredFiles,
          gitStatus,
          diffContent,
          fileContents: fileContents.size > 0 ? fileContents : undefined,
        };

        const result = await llmService.summarizeDiff(context);
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

    ipcMain.handle('llm-generate-commit', async (_event: IpcMainInvokeEvent, repoPath: string, files: string[]) => {
      try {
        console.log('[LLM] Generating commit message for files:', files);
        
        // Get diff content from git service
        const diffResult = await gitService.getDiff(repoPath, files, false);
        if (!diffResult.success || diffResult.files.length === 0) {
          return {
            success: false,
            error: 'No changes to commit'
          };
        }

        // Combine all diffs
        const diffContent = diffResult.files.map(f => f.diff).join('\n\n');
        
        // Build git status map
        const gitStatus = new Map(diffResult.files.map(f => [f.path, f.status]));

        // Build context for AI
        const context = {
          repoPath,
          selectedFiles: files,
          gitStatus,
          diffContent,
        };

        // DEPRECATED - generateCommitMessage removed
        // const result = await llmService.generateCommitMessage(context);
        console.log('[LLM] Commit message generation deprecated - feature removed');
        return {
          success: false,
          error: 'Commit message generation is no longer supported'
        };
      } catch (error) {
        console.error('[LLM] Error:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error'
        };
      }
    });

    ipcMain.handle('llm-initialize', async (_event: IpcMainInvokeEvent, apiKey: string) => {
      try {
        console.log('[LLM] Initializing with API key');
        await llmService.initialize(apiKey);
        return { success: true };
      } catch (error) {
        console.error('[LLM] Initialization error:', error);
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
    ipcMain.handle('start-watch', async (_event: IpcMainInvokeEvent, filePaths: string[]) => {
      // This handler is now deprecated - Git tracking is automatic
      // Keeping for backward compatibility but returning success immediately
      console.log('[Watch] Deprecated: Git tracking is automatic, no manual watch needed');
      return { success: true };
    });
    
    // Stop watching files
    ipcMain.handle('stop-watch', async () => {
      // This handler is now deprecated - Git tracking is automatic
      console.log('[Watch] Deprecated: Git tracking is automatic, no manual watch needed');
      return { success: true };
    });

    // API request handler - proxy requests to FastAPI backend
    ipcMain.handle('api-request', async (_event: IpcMainInvokeEvent, options: {
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
    // No cleanup needed - Git tracking is automatic
    console.log('Cleaning up...');
  }
}

// Initialize the app
const snipDiffApp = new SnipDiffApp();
snipDiffApp.initialize().catch((error) => {
  console.error('Fatal error during initialization:', error);
  app.quit();
});
