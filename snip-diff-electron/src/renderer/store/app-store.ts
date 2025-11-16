/**
 * App State Store using Zustand
 * Manages global application state for SNIP-DIFF
 */

import { create } from 'zustand';

interface FileNode {
  path: string;
  name: string;
  type: 'file' | 'directory';
  size?: number;
  modified?: number;
  children?: FileNode[];
}

interface DiffSection {
  title: string;
  files: Array<{
    path: string;
    change_type: string;
    content: string;
  }>;
  collapsed: boolean;
}

interface OpenFile {
  path: string;
  content: string;
  language?: string;
}

interface AppState {
  // File tree state
  selectedPath: string | null;
  fileTree: FileNode[];
  selectedFiles: Set<string>;
  gitStatus: Map<string, string>; // path -> status (Modified, Untracked, etc.)
  
  // Diff state
  currentScanId: string | null;
  scanStatus: string | null;
  scanProgress: number | null;
  diffSections: DiffSection[];
  unifiedDiff: string | null;
  
  // Open files state (editor mode)
  openFiles: OpenFile[];
  activeFilePath: string | null;
  
  // UI state
  isLoading: boolean;
  sidebarWidth: number;
  isDarkMode: boolean;
  viewMode: 'incremental' | 'full';
  diffMode: 'unified' | 'side-by-side';
  
  // Actions
  setSelectedPath: (path: string | null) => void;
  setFileTree: (tree: FileNode[]) => void;
  toggleFileSelection: (filePath: string) => void;
  clearFileSelection: () => void;
  selectChangedFiles: () => void;
  setGitStatus: (status: Map<string, string>) => void;
  clearDiffResults: () => void;
  setScanStatus: (status: string | null) => void;
  setScanProgress: (progress: number | null) => void;
  setCurrentScanId: (scanId: string | null) => void;
  setDiffSections: (sections: DiffSection[]) => void;
  setUnifiedDiff: (diff: string | null) => void;
  openFile: (file: OpenFile) => void;
  closeFile: (path: string) => void;
  setActiveFile: (path: string) => void;
  setIsLoading: (loading: boolean) => void;
  setSidebarWidth: (width: number) => void;
  toggleDarkMode: () => void;
  setViewMode: (mode: 'incremental' | 'full') => void;
  setDiffMode: (mode: 'unified' | 'side-by-side') => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  selectedPath: null,
  fileTree: [],
  selectedFiles: new Set(),
  gitStatus: new Map(),
  currentScanId: null,
  scanStatus: null,
  scanProgress: null,
  diffSections: [],
  unifiedDiff: null,
  openFiles: [],
  activeFilePath: null,
  isLoading: false,
  sidebarWidth: 350,
  isDarkMode: false,
  viewMode: 'full',
  diffMode: 'side-by-side',

  // Actions
  setSelectedPath: (path) => set({ selectedPath: path }),
  
  setFileTree: (tree) => set({ fileTree: tree }),
  
  toggleFileSelection: (filePath) => set((state) => {
    const newSelection = new Set(state.selectedFiles);
    if (newSelection.has(filePath)) {
      newSelection.delete(filePath);
    } else {
      newSelection.add(filePath);
    }
    return { selectedFiles: newSelection };
  }),
  
  clearFileSelection: () => set({ selectedFiles: new Set() }),
  
  selectChangedFiles: () => set((state) => {
    const changedFiles = new Set<string>();
    state.gitStatus.forEach((status, path) => {
      if (status !== 'Unchanged') {
        changedFiles.add(path);
      }
    });
    return { selectedFiles: changedFiles };
  }),
  
  setGitStatus: (status) => set({ gitStatus: status }),
  
  clearDiffResults: () => set({ 
    diffSections: [], 
    scanStatus: null, 
    scanProgress: null,
    currentScanId: null 
  }),
  
  setScanStatus: (status) => set({ scanStatus: status }),
  
  setScanProgress: (progress) => set({ scanProgress: progress }),
  
  setCurrentScanId: (scanId) => set({ currentScanId: scanId }),
  
  setDiffSections: (sections) => set({ diffSections: sections }),
  
  setUnifiedDiff: (diff) => set({ unifiedDiff: diff }),
  
  openFile: (file) => set((state) => {
    const exists = state.openFiles.some(f => f.path === file.path);
    if (exists) {
      return { activeFilePath: file.path };
    }
    return { 
      openFiles: [...state.openFiles, file],
      activeFilePath: file.path 
    };
  }),
  
  closeFile: (path) => set((state) => {
    const newFiles = state.openFiles.filter(f => f.path !== path);
    const newActive = state.activeFilePath === path 
      ? (newFiles.length > 0 ? newFiles[newFiles.length - 1].path : null)
      : state.activeFilePath;
    return { openFiles: newFiles, activeFilePath: newActive };
  }),
  
  setActiveFile: (path) => set({ activeFilePath: path }),
  
  setIsLoading: (loading) => set({ isLoading: loading }),
  
  setSidebarWidth: (width) => set({ sidebarWidth: Math.max(250, Math.min(500, width)) }),
  
  toggleDarkMode: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
  
  setViewMode: (mode) => set({ viewMode: mode }),
  
  setDiffMode: (mode) => set({ diffMode: mode }),
}));
