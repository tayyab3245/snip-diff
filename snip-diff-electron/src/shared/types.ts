/**
 * Shared types for SNIP-DIFF Electron app
 */

// ===== File System Types =====

export interface FileNode {
  path: string;
  name: string;
  type: 'file' | 'directory';
  size?: number;
  modified?: number;
  children?: FileNode[];
}

// ===== Diff Types =====

export interface DiffSection {
  title: string;
  files: DiffFile[];
  collapsed: boolean;
}

export interface DiffFile {
  path: string;
  change_type: string;
  content: string;
}

// ===== Git Types =====

export type GitStatus = 'Modified' | 'Added' | 'Deleted' | 'Untracked' | 'Unchanged';

export interface GitFileChange {
  path: string;
  status: GitStatus;
  diff: string;
}

export interface GitDiffResult {
  success: boolean;
  files: GitFileChange[];
  error?: string;
}

// ===== LLM Types =====

export interface LLMSummarizeResult {
  success: boolean;
  summary?: string;
  tokensUsed?: number;
  error?: string;
}

export interface FileWithContent {
  path: string;
  content: string;
}

// ===== API Types =====

export interface ApiResponse<T = any> {
  success: boolean;
  status?: number;
  data?: T;
  error?: string;
}

export interface ApiRequestOptions {
  method: string;
  endpoint: string;
  data?: any;
  params?: Record<string, string>;
}

// ===== Electron API Types =====

export interface ElectronAPI {
  // App info
  getAppVersion: () => Promise<string>;
  
  // Window controls
  windowMinimize: () => Promise<void>;
  windowMaximize: () => Promise<void>;
  windowClose: () => Promise<void>;
  
  // File system operations
  selectFolder: () => Promise<string | null>;
  selectFiles: () => Promise<string[] | null>;
  
  // Git operations
  getGitDiff: (directory: string, filePaths?: string[]) => Promise<GitDiffResult>;
  getGitFileContent: (directory: string, filePath: string, ref?: string) => Promise<{
    success: boolean;
    content?: string;
    error?: string;
  }>;
  isGitRepo: (directory: string) => Promise<{ success: boolean; isRepo: boolean }>;
  
  // File watching
  startWatch: (filePaths: string[]) => Promise<{ success: boolean; error?: string }>;
  stopWatch: () => Promise<{ success: boolean; error?: string }>;
  onFileChanged: (callback: (filePath: string) => void) => void;
  
  // LLM operations
  llmSummarizeFile: (content: string, filePath: string) => Promise<LLMSummarizeResult>;
  llmSummarizeDiff: (diffContent: string, files: string[]) => Promise<LLMSummarizeResult>;
  llmSummarizeMultipleFiles: (files: FileWithContent[]) => Promise<LLMSummarizeResult>;
  llmIsAvailable: () => Promise<{ available: boolean }>;
  
  // Legacy API request (for backward compatibility)
  apiRequest: (options: ApiRequestOptions) => Promise<ApiResponse>;
}

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
