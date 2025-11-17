/*
 * Copyright 2025 Tayyab
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * Preload script for SNIP-DIFF Electron app
 * Provides secure IPC bridge between renderer and main processes
 */

import { contextBridge, ipcRenderer } from 'electron';
import type { ElectronAPI, FileChangeEvent } from '../shared/types';

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
  getGitDiff: (directory: string, filePaths?: string[], fullContext?: boolean) => 
    ipcRenderer.invoke('get-git-diff', directory, filePaths, fullContext),
  getGitStatus: (directory: string) =>
    ipcRenderer.invoke('get-git-status', directory),
  getGitFileContent: (directory: string, filePath: string, ref?: string) => 
    ipcRenderer.invoke('get-git-file-content', directory, filePath, ref),
  isGitRepo: (directory: string) => 
    ipcRenderer.invoke('is-git-repo', directory),
  
  // File operations
  getFileTree: (dirPath: string) =>
    ipcRenderer.invoke('get-file-tree', dirPath),
  readFile: (filePath: string) =>
    ipcRenderer.invoke('read-file', filePath),
  readMultipleFiles: (filePaths: string[]) =>
    ipcRenderer.invoke('read-multiple-files', filePaths),

  // File watching
  startWatch: (filePaths: string[]) => ipcRenderer.invoke('start-watch', filePaths),
  stopWatch: () => ipcRenderer.invoke('stop-watch'),
  onFileChanged: (callback: (event: FileChangeEvent) => void) => {
    const listener = (_: Electron.IpcRendererEvent, event: FileChangeEvent) => callback(event);
    ipcRenderer.on('file-changed', listener);
    
    // Return cleanup function
    return () => {
      ipcRenderer.removeListener('file-changed', listener);
    };
  },

  // LLM operations
  llmInitialize: (apiKey: string) =>
    ipcRenderer.invoke('llm-initialize', apiKey),
  llmSummarizeDiff: (repoPath: string, files: string[]) =>
    ipcRenderer.invoke('llm-summarize-diff', repoPath, files),
  llmGenerateCommit: (repoPath: string, files: string[]) =>
    ipcRenderer.invoke('llm-generate-commit', repoPath, files),
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
