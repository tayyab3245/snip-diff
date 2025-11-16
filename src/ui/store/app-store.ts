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
  gitStatus?: string; // Git status: Modified, Added, Deleted, Untracked, etc.
}

interface ChatMessage {
  id: string;
  type: 'ai' | 'system' | 'error';
  content: string;
  timestamp?: Date;
  isTyping?: boolean;
}

interface AppState {
  // File tree state
  selectedPath: string | null;
  fileTree: FileNode[];
  selectedFiles: Set<string>;
  gitStatus: Map<string, string>; // path -> status (Modified, Untracked, etc.)
  modifiedFiles: Set<string>; // Files that have been modified while watching
  
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
  
  // AI Chat state
  chatMessages: ChatMessage[];
  isChatLoading: boolean;
  chatPanelWidth: number;
  analyzedFilePaths: string[]; // Persist analyzed files even when selection changes
  
  // Actions
  setSelectedPath: (path: string | null) => void;
  setFileTree: (tree: FileNode[]) => void;
  toggleFileSelection: (filePath: string) => void;
  setGitStatus: (status: Map<string, string>) => void;
  markFileModified: (path: string) => void;
  clearModifiedFiles: () => void;
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
  addChatMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void;
  clearChatMessages: () => void;
  setIsChatLoading: (loading: boolean) => void;
  setChatPanelWidth: (width: number) => void;
  setAnalyzedFilePaths: (paths: string[]) => void;
}

export type { ChatMessage };

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  selectedPath: null,
  fileTree: [],
  selectedFiles: new Set(),
  gitStatus: new Map(),
  modifiedFiles: new Set(),
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
  viewMode: 'incremental',
  diffMode: 'unified',
  chatMessages: [],
  isChatLoading: false,
  chatPanelWidth: 400,
  analyzedFilePaths: [],

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
  
  setGitStatus: (status) => set({ gitStatus: status }),
  
  markFileModified: (path) => set((state) => {
    const newModified = new Set(state.modifiedFiles);
    newModified.add(path);
    return { modifiedFiles: newModified };
  }),
  
  clearModifiedFiles: () => set({ modifiedFiles: new Set() }),
  
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
    const existingIndex = state.openFiles.findIndex(f => f.path === file.path);
    if (existingIndex !== -1) {
      // File already open - update its content and make it active
      const newOpenFiles = [...state.openFiles];
      newOpenFiles[existingIndex] = file;
      return { 
        openFiles: newOpenFiles,
        activeFilePath: file.path 
      };
    }
    // File not open yet - add it
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
    // Also remove from selectedFiles to clear the selection indicator
    const newSelection = new Set(state.selectedFiles);
    newSelection.delete(path);
    return { openFiles: newFiles, activeFilePath: newActive, selectedFiles: newSelection };
  }),
  
  setActiveFile: (path) => set({ activeFilePath: path }),
  
  setIsLoading: (loading) => set({ isLoading: loading }),
  
  setSidebarWidth: (width) => set({ sidebarWidth: Math.max(250, Math.min(500, width)) }),
  
  toggleDarkMode: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
  
  setViewMode: (mode) => set({ viewMode: mode }),
  
  setDiffMode: (mode) => set({ diffMode: mode }),
  
  addChatMessage: (message) => set((state) => ({
    chatMessages: [
      ...state.chatMessages,
      {
        ...message,
        id: `msg-${Date.now()}-${Math.random()}`,
        timestamp: message.type === 'error' ? undefined : new Date(),
      },
    ],
  })),
  
  clearChatMessages: () => set({ chatMessages: [] }),
  
  setIsChatLoading: (loading) => set({ isChatLoading: loading }),
  
  setChatPanelWidth: (width) => set({ chatPanelWidth: Math.max(300, Math.min(800, width)) }),
  
  setAnalyzedFilePaths: (paths) => set({ analyzedFilePaths: paths }),
}));
