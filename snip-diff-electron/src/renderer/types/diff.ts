/**
 * TypeScript interfaces for SNIP-DIFF multi-view diff system
 * Mirrors Python models in snip-diff-api/app/core/models/diff_types.py
 */

export enum LineType {
  CONTEXT = "context",    // Unchanged line (space prefix)
  ADDED = "added",       // Added line (+ prefix)  
  DELETED = "deleted",   // Deleted line (- prefix)
  MODIFIED = "modified"  // Modified line (both add+del)
}

export enum ChangeType {
  ADDED = "added",
  DELETED = "deleted", 
  MODIFIED = "modified",
  RENAMED = "renamed",
  UNCHANGED = "unchanged"
}

export enum DiffMode {
  UNIFIED_FULL = "unified_full",           // All lines with +/- markers
  UNIFIED_CONTEXT = "unified_context",     // Only changed hunks + context
  SIDE_BY_SIDE = "side_by_side",          // Left/right column layout
  INLINE_FULL = "inline_full"             // Full file with change highlights
}

export interface LineToken {
  line_no_old?: number;    // Line number in old file (1-based)
  line_no_new?: number;    // Line number in new file (1-based)
  line_type: LineType;
  text: string;            // Line content (no newline)
}

export interface UnifiedHunk {
  old_start: number;       // Starting line in old file
  old_count: number;       // Number of lines in old file
  new_start: number;       // Starting line in new file  
  new_count: number;       // Number of lines in new file
  header: string;          // @@ -old_start,old_count +new_start,new_count @@
  lines: LineToken[];
}

export interface SideBySideRow {
  left?: LineToken;        // Left side (old file)
  right?: LineToken;       // Right side (new file) 
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
  old_path?: string;       // For renamed files
  change_type: ChangeType;
  file_size_old: number;
  file_size_new: number;
  is_binary: boolean;
  stats: DiffStats;
}

export interface FileDiff {
  meta: FileDiffMeta;
  hunks: UnifiedHunk[];
  modes: Record<string, any>;  // Rendered diff modes
}

export interface RenderOptions {
  context_radius: number;      // Lines of context around changes
  max_lines?: number;         // Limit total output lines
  show_line_numbers: boolean;
  collapse_unchanged: boolean; // For inline_full mode
  char_level: boolean;        // Enable character-level highlighting
}

// UI-specific interfaces
export interface DiffViewerProps {
  fileDiff: FileDiff;
  mode: DiffMode;
  options?: Partial<RenderOptions>;
  onModeChange?: (mode: DiffMode) => void;
}

export interface DiffLineProps {
  line: LineToken;
  showLineNumbers?: boolean;
  charDiff?: CharDiff[];  // Character-level diff spans
}

export interface CharDiff {
  type: 'added' | 'deleted' | 'unchanged';
  text: string;
  start: number;
  end: number;
}

// API Response types (matching backend Pydantic models)
export interface DiffAPIResponse {
  success: boolean;
  file_diffs: FileDiff[];
  total_files: number;
  total_changes: number;
}

export interface BatchDiffRequest {
  paths: string[];
  modes: DiffMode[];
  context: number;
}

export interface FileDiffRequest {
  path: string;
  mode: DiffMode;
  context?: number;
}

// Store interfaces for state management
export interface DiffState {
  fileDiffs: Record<string, FileDiff>;     // path -> FileDiff
  selectedMode: DiffMode;
  renderOptions: RenderOptions;
  isLoading: boolean;
  error?: string;
}

export interface DiffActions {
  setFileDiff: (path: string, diff: FileDiff) => void;
  setSelectedMode: (mode: DiffMode) => void;
  updateRenderOptions: (options: Partial<RenderOptions>) => void;
  clearDiffs: () => void;
}

// Legacy compatibility (for gradual migration)
export interface LegacyDiffSection {
  title: string;
  files: Array<{
    path: string;
    change_type: string;
    content: string;
  }>;
  collapsed: boolean;
}

// Utility types
export type DiffModeRenderer<T = any> = (
  hunks: UnifiedHunk[], 
  options: RenderOptions
) => T;

export type DiffFileFilter = (meta: FileDiffMeta) => boolean;

export type DiffSortFn = (a: FileDiff, b: FileDiff) => number;

// Default values
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
