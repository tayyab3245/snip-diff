/**
 * Shared types for SNIP-DIFF Electron app
 */

export interface FileNode {
  path: string;
  name: string;
  type: 'file' | 'directory';
  size?: number;
  modified?: number;
  children?: FileNode[];
}

export interface DiffSection {
  title: string;
  files: Array<{
    path: string;
    change_type: string;
    content: string;
  }>;
  collapsed: boolean;
}

export interface ScanRequest {
  directory: string;
  include_paths?: string[];
  scan_mode?: string;
}

export interface ScanResponse {
  success: boolean;
  scan_id: string;
  status: string;
  message: string;
}

export interface ApiResponse<T = any> {
  success: boolean;
  status?: number;
  data?: T;
  error?: string;
}

export interface ElectronAPI {
  getAppVersion: () => Promise<string>;
  selectFolder: () => Promise<string | null>;
  windowMinimize: () => Promise<void>;
  windowMaximize: () => Promise<void>;
  windowClose: () => Promise<void>;
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
  startWatch: (filePaths: string[]) => Promise<{ success: boolean; error?: string }>;
  stopWatch: () => Promise<{ success: boolean; error?: string }>;
  onFileChanged: (callback: (filePath: string) => void) => void;
}

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
