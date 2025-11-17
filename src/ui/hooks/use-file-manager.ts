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
 * File Manager Hook
 * Handles file operations and state management - separates business logic from UI
 */

import { useCallback } from 'react';
import { useAppStore } from '../store/app-store';

export const useFileManager = () => {
  const { 
    setSelectedPath, 
    selectedPath,
    setFileTree,
    openFile,
    closeFile,
    setActiveFile,
    selectedFiles
  } = useAppStore();

  /**
   * Select a folder via dialog
   */
  const selectFolder = useCallback(async (): Promise<boolean> => {
    try {
      const folderPath = await window.electronAPI.selectFolder();
      if (folderPath) {
        setSelectedPath(folderPath);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Failed to select folder:', error);
      return false;
    }
  }, [setSelectedPath]);

  /**
   * Load file tree for a directory
   */
  const loadFileTree = useCallback(async (path: string): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await window.electronAPI.getFileTree(path);
      
      if (response.success && response.data) {
        setFileTree(response.data.nodes || []);
        return { success: true };
      } else {
        return { success: false, error: response.error || 'Failed to load file tree' };
      }
    } catch (error) {
      console.error('Error loading file tree:', error);
      return { success: false, error: 'Error loading file tree' };
    }
  }, [setFileTree]);

  /**
   * Open a file and read its content (or diff if available)
   */
  const openFileWithContent = useCallback(async (filePath: string): Promise<boolean> => {
    if (!selectedPath) return false;
    
    try {
      // Get Git diff for THIS specific file (check its actual Git status)
      const diffResult = await window.electronAPI.getGitDiff(selectedPath, [filePath]);
      
      if (diffResult.success && diffResult.files && diffResult.files.length > 0) {
        // Git found changes for this file
        const fileData = diffResult.files[0];
        
        if (fileData && fileData.diff) {
          // File has changes - show diff
          openFile({
            path: filePath,
            content: fileData.diff || '(No changes)',
            language: 'diff',
            gitStatus: fileData.status
          });
          setActiveFile(filePath);
          return true;
        }
      }
      
      // No Git changes found - file is unchanged, show raw content
      const response = await window.electronAPI.readFile(filePath);
      
      if (response.success && response.data) {
        const fileName = filePath.split(/[\\/]/).pop() || filePath;
        const extension = fileName.split('.').pop();
        
        openFile({
          path: filePath,
          content: response.data.content,
          language: extension
        });
        setActiveFile(filePath);
        return true;
      } else {
        console.error('[FileManager] Failed to read file:', response.error);
        return false;
      }
      
    } catch (error) {
      console.error('Exception opening file:', error);
      return false;
    }
  }, [selectedPath, selectedFiles, openFile, setActiveFile]);

  /**
   * Toggle file selection (select/deselect)
   */
  const toggleFile = useCallback(async (filePath: string, wasSelected: boolean) => {
    // File is already toggled in parent, no need to toggle here
    
    if (!wasSelected) {
      // File just got selected - show its diff
      await openFileWithContent(filePath);
    } else {
      // File just got deselected - close it
      closeFile(filePath);
    }
  }, [openFileWithContent, closeFile]);

  return {
    selectFolder,
    loadFileTree,
    openFileWithContent,
    toggleFile,
  };
};
