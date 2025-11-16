/**
 * Preload script for SNIP-DIFF Electron app
 * Provides secure IPC bridge between renderer and main processes
 */

import { contextBridge, ipcRenderer } from 'electron';
import type { ElectronAPI } from '../shared/types';

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // App information
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),

  // Window controls for frameless window
  windowMinimize: () => ipcRenderer.invoke('window-minimize'),
  windowMaximize: () => ipcRenderer.invoke('window-maximize'),
  windowClose: () => ipcRenderer.invoke('window-close'),

  // File dialog operations
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  selectFiles: () => ipcRenderer.invoke('select-files'),

  // Git operations
  getGitDiff: (directory: string, filePaths?: string[]) => 
    ipcRenderer.invoke('get-git-diff', directory, filePaths),
  getGitFileContent: (directory: string, filePath: string, ref?: string) => 
    ipcRenderer.invoke('get-git-file-content', directory, filePath, ref),
  isGitRepo: (directory: string) => 
    ipcRenderer.invoke('is-git-repo', directory),

  // File watching
  startWatch: (filePaths: string[]) => ipcRenderer.invoke('start-watch', filePaths),
  stopWatch: () => ipcRenderer.invoke('stop-watch'),
  onFileChanged: (callback: (_filePath: string) => void) => {
    ipcRenderer.on('file-changed', (_: Electron.IpcRendererEvent, filePath: string) => callback(filePath));
  },

  // LLM operations
  llmSummarizeFile: (content: string, filePath: string) =>
    ipcRenderer.invoke('llm-summarize-file', content, filePath),
  llmSummarizeDiff: (diffContent: string, files: string[]) =>
    ipcRenderer.invoke('llm-summarize-diff', diffContent, files),
  llmSummarizeMultipleFiles: (files: Array<{ path: string; content: string }>) =>
    ipcRenderer.invoke('llm-summarize-multiple-files', files),
  llmIsAvailable: () =>
    ipcRenderer.invoke('llm-is-available'),

  // Legacy API communication (for backward compatibility)
  apiRequest: (options: {
    method: string;
    endpoint: string;
    data?: any;
    params?: Record<string, string>;
  }) => ipcRenderer.invoke('api-request', options),
} as ElectronAPI);
