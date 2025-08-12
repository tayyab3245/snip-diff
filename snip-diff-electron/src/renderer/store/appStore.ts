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

interface AppState {
  // File tree state
  selectedPath: string | null;
  fileTree: FileNode[];
  selectedFiles: Set<string>;
  
  // Diff state
  currentScanId: string | null;
  scanStatus: string | null;
  diffSections: DiffSection[];
  unifiedDiff: string | null;
  
  // UI state
  isLoading: boolean;
  sidebarWidth: number;
  isDarkMode: boolean;
  
  // Actions
  setSelectedPath: (path: string | null) => void;
  setFileTree: (tree: FileNode[]) => void;
  toggleFileSelection: (filePath: string) => void;
  clearFileSelection: () => void;
  setScanStatus: (status: string | null) => void;
  setCurrentScanId: (scanId: string | null) => void;
  setDiffSections: (sections: DiffSection[]) => void;
  setUnifiedDiff: (diff: string | null) => void;
  setIsLoading: (loading: boolean) => void;
  setSidebarWidth: (width: number) => void;
  toggleDarkMode: () => void;
}

export const useAppStore = create<AppState>((set, get) => ({
  // Initial state
  selectedPath: null,
  fileTree: [],
  selectedFiles: new Set(),
  currentScanId: null,
  scanStatus: null,
  diffSections: [],
  unifiedDiff: null,
  isLoading: false,
  sidebarWidth: 350,
  isDarkMode: false,

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
  
  setScanStatus: (status) => set({ scanStatus: status }),
  
  setCurrentScanId: (scanId) => set({ currentScanId: scanId }),
  
  setDiffSections: (sections) => set({ diffSections: sections }),
  
  setUnifiedDiff: (diff) => set({ unifiedDiff: diff }),
  
  setIsLoading: (loading) => set({ isLoading: loading }),
  
  setSidebarWidth: (width) => set({ sidebarWidth: Math.max(250, Math.min(500, width)) }),
  
  toggleDarkMode: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
}));
