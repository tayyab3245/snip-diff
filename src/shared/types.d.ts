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
    files: DiffFile[];
    collapsed: boolean;
}
export interface DiffFile {
    path: string;
    change_type: string;
    content: string;
}
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
export declare enum LineType {
    CONTEXT = "context",
    ADDED = "added",
    DELETED = "deleted",
    MODIFIED = "modified"
}
export declare enum ChangeType {
    ADDED = "added",
    DELETED = "deleted",
    MODIFIED = "modified",
    RENAMED = "renamed",
    UNCHANGED = "unchanged"
}
export declare enum DiffMode {
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
export declare const DEFAULT_RENDER_OPTIONS: RenderOptions;
export declare const DIFF_MODE_LABELS: Record<DiffMode, string>;
export declare const LINE_TYPE_SYMBOLS: Record<LineType, string>;
export interface ElectronAPI {
    getAppVersion: () => Promise<string>;
    windowMinimize: () => Promise<void>;
    windowMaximize: () => Promise<void>;
    windowClose: () => Promise<void>;
    selectFolder: () => Promise<string | null>;
    selectFiles: () => Promise<string[] | null>;
    getGitDiff: (directory: string, filePaths?: string[]) => Promise<GitDiffResult>;
    getGitFileContent: (directory: string, filePath: string, ref?: string) => Promise<{
        success: boolean;
        content?: string;
        error?: string;
    }>;
    isGitRepo: (directory: string) => Promise<{
        success: boolean;
        isRepo: boolean;
    }>;
    startWatch: (filePaths: string[]) => Promise<{
        success: boolean;
        error?: string;
    }>;
    stopWatch: () => Promise<{
        success: boolean;
        error?: string;
    }>;
    onFileChanged: (callback: (filePath: string) => void) => void;
    llmSummarizeFile: (content: string, filePath: string) => Promise<LLMSummarizeResult>;
    llmSummarizeDiff: (diffContent: string, files: string[]) => Promise<LLMSummarizeResult>;
    llmSummarizeMultipleFiles: (files: FileWithContent[]) => Promise<LLMSummarizeResult>;
    llmIsAvailable: () => Promise<{
        available: boolean;
    }>;
    apiRequest: (options: ApiRequestOptions) => Promise<ApiResponse>;
}
declare global {
    interface Window {
        electronAPI: ElectronAPI;
    }
}
//# sourceMappingURL=types.d.ts.map