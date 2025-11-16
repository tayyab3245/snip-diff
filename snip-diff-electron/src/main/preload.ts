/**
 * Preload script for SNIP-DIFF Electron app
 * Provides secure IPC bridge between renderer and main processes
 */

import { contextBridge, ipcRenderer } from 'electron';

// Define the API interface
interface ElectronAPI {
  // API communication
  apiRequest: (options: {
    method: string;
    endpoint: string;
    data?: any;
    params?: Record<string, string>;
  }) => Promise<{
    success: boolean;
    status?: number;
    data?: any;
    error?: string;
  }>;

  // Git operations
  getGitDiff: (directory: string, filePaths?: string[]) => Promise<{
    success: boolean;
    files: Array<{ path: string; status: string; diff: string }>;
    error?: string;
  }>;
  getGitFileContent: (directory: string, filePath: string, ref?: string) => Promise<{
    success: boolean;
    content?: string;
    error?: string;
  }>;
  isGitRepo: (directory: string) => Promise<{ success: boolean; isRepo: boolean }>;

  // File system operations
  selectFolder: () => Promise<string | null>;
  selectFiles: () => Promise<string[] | null>;

  // File watching
  startWatch: (filePaths: string[]) => Promise<{ success: boolean; error?: string }>;
  stopWatch: () => Promise<{ success: boolean; error?: string }>;
  onFileChanged: (callback: (filePath: string) => void) => void;

  // Window controls
  windowMinimize: () => Promise<void>;
  windowMaximize: () => Promise<void>;
  windowClose: () => Promise<void>;

  // App info
  getAppVersion: () => Promise<string>;
}

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // API communication with FastAPI backend
  apiRequest: (options: {
    method: string;
    endpoint: string;
    data?: any;
    params?: Record<string, string>;
  }) => ipcRenderer.invoke('api-request', options),

  // Git operations
  getGitDiff: (directory: string, filePaths?: string[]) => 
    ipcRenderer.invoke('get-git-diff', directory, filePaths),
  getGitFileContent: (directory: string, filePath: string, ref?: string) => 
    ipcRenderer.invoke('get-git-file-content', directory, filePath, ref),
  isGitRepo: (directory: string) => 
    ipcRenderer.invoke('is-git-repo', directory),

  // File dialog operations
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  selectFiles: () => ipcRenderer.invoke('select-files'),

  // File watching
  startWatch: (filePaths: string[]) => ipcRenderer.invoke('start-watch', filePaths),
  stopWatch: () => ipcRenderer.invoke('stop-watch'),
  onFileChanged: (callback: (filePath: string) => void) => {
    ipcRenderer.on('file-changed', (_, filePath) => callback(filePath));
  },

  // Window controls for frameless window
  windowMinimize: () => ipcRenderer.invoke('window-minimize'),
  windowMaximize: () => ipcRenderer.invoke('window-maximize'),
  windowClose: () => ipcRenderer.invoke('window-close'),

  // App information
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
} as ElectronAPI);

// Type declaration for the global electronAPI
declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
