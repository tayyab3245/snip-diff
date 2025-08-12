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
