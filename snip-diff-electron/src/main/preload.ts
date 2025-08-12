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

  // File system operations
  selectFolder: () => Promise<string | null>;
  selectFiles: () => Promise<string[] | null>;

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

  // File dialog operations
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  selectFiles: () => ipcRenderer.invoke('select-files'),

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
