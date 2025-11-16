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

export interface FileChangeEvent {
  path: string;
  status: GitStatus;
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

// ===== Diff View Types =====

export enum LineType {
  CONTEXT = "context",
  ADDED = "added",
  DELETED = "deleted",
  MODIFIED = "modified"
}

export enum ChangeType {
  ADDED = "added",
  DELETED = "deleted",
  MODIFIED = "modified",
  RENAMED = "renamed",
  UNCHANGED = "unchanged"
}

export enum DiffMode {
  UNIFIED_FULL = "unified_full",
  UNIFIED_CONTEXT = "unified_context",
  SIDE_BY_SIDE = "side_by_side",
  INLINE_FULL = "inline_full"
}

export interface LineToken {
  line_no_old?: number;
  line_no_new?: number;
  line_type: LineType;
  text: string;
}

export interface UnifiedHunk {
  old_start: number;
  old_count: number;
  new_start: number;
  new_count: number;
  header: string;
  lines: LineToken[];
}

export interface SideBySideRow {
  left?: LineToken;
  right?: LineToken;
  row_type: LineType;
}

export interface DiffStats {
  lines_added: number;
  lines_deleted: number;
  lines_modified: number;
  lines_context: number;
  total_changes: number;
}

export interface FileDiffMeta {
  path: string;
  old_path?: string;
  change_type: ChangeType;
  file_size_old: number;
  file_size_new: number;
  is_binary: boolean;
  stats: DiffStats;
}

export interface FileDiff {
  meta: FileDiffMeta;
  hunks: UnifiedHunk[];
  modes: Record<string, any>;
}

export interface RenderOptions {
  context_radius: number;
  max_lines?: number;
  show_line_numbers: boolean;
  collapse_unchanged: boolean;
  char_level: boolean;
}

export interface CharDiff {
  type: 'added' | 'deleted' | 'unchanged';
  text: string;
  start: number;
  end: number;
}

export const DEFAULT_RENDER_OPTIONS: RenderOptions = {
  context_radius: 3,
  show_line_numbers: true,
  collapse_unchanged: false,
  char_level: false
};

export const DIFF_MODE_LABELS: Record<DiffMode, string> = {
  [DiffMode.UNIFIED_FULL]: "Unified (Full)",
  [DiffMode.UNIFIED_CONTEXT]: "Unified (Context)",
  [DiffMode.SIDE_BY_SIDE]: "Side by Side",
  [DiffMode.INLINE_FULL]: "Inline (Full)"
};

export const LINE_TYPE_SYMBOLS: Record<LineType, string> = {
  [LineType.CONTEXT]: " ",
  [LineType.ADDED]: "+",
  [LineType.DELETED]: "-",
  [LineType.MODIFIED]: "~"
};

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
  getFileTree: (dirPath: string) => Promise<ApiResponse<{ nodes: FileNode[] }>>;
  readFile: (filePath: string) => Promise<ApiResponse<{ content: string; filePath: string }>>;
  readMultipleFiles: (filePaths: string[]) => Promise<ApiResponse<Array<{ path: string; content: string }>>>;
  
  // Git operations
  getGitDiff: (directory: string, filePaths?: string[], fullContext?: boolean) => Promise<GitDiffResult>;
  getGitFileContent: (directory: string, filePath: string, ref?: string) => Promise<{
    success: boolean;
    content?: string;
    error?: string;
  }>;
  isGitRepo: (directory: string) => Promise<{ success: boolean; isRepo: boolean }>;
  
  // File watching
  startWatch: (filePaths: string[]) => Promise<{ success: boolean; fileStatuses?: Record<string, string>; error?: string }>;
  stopWatch: () => Promise<{ success: boolean; error?: string }>;
  onFileChanged: (callback: (event: FileChangeEvent) => void) => void;
  
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
