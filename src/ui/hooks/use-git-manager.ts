/**
 * Git Manager Hook
 * Handles Git operations and diff generation - separates business logic from UI
 */

import { useCallback, useRef } from 'react';
import { useAppStore } from '../store/app-store';

export const useGitManager = () => {
  const { 
    selectedPath,
    selectedFiles,
    openFile,
    setActiveFile,
    setScanStatus,
    markFileModified
  } = useAppStore();

  /**
   * Generate and display unified diff for selected files
   */
  const generateDiff = useCallback(async (): Promise<boolean> => {
    if (!selectedPath || selectedFiles.size === 0) {
      console.warn('[GitManager] Cannot generate diff: no path or files selected');
      return false;
    }

    try {
      console.log('[GitManager] Generating diff...');
      setScanStatus('running');
      
      const selectedFilesArray = Array.from(selectedFiles);
      const diffResult = await window.electronAPI.getGitDiff(selectedPath, selectedFilesArray);
      
      if (diffResult.success && diffResult.files) {
        // Update/create open files with fresh diff content
        diffResult.files.forEach((file) => {
          const diffContent = file.diff || '(No changes)';
          
          openFile({
            path: file.path,
            content: diffContent,
            language: 'diff'
          });
          
          // Set as active file to show the diff
          setActiveFile(file.path);
        });
        
        setScanStatus(diffResult.files.length > 0 ? 'completed' : null);
        console.log('[GitManager] Diff generated successfully');
        return true;
      } else {
        console.error('[GitManager] Git diff failed:', diffResult.error);
        setScanStatus('failed');
        return false;
      }
    } catch (error) {
      console.error('[GitManager] Error generating diff:', error);
      setScanStatus('failed');
      return false;
    }
  }, [selectedPath, selectedFiles, setScanStatus, openFile, setActiveFile]);

  /**
   * Poll Git status and refresh diffs for selected files
   */
  const pollGitStatus = useCallback(async () => {
    if (!selectedPath || selectedFiles.size === 0) {
      return;
    }

    try {
      const selectedFilesArray = Array.from(selectedFiles);
      const diffResult = await window.electronAPI.getGitDiff(selectedPath, selectedFilesArray);
      
      if (diffResult.success && diffResult.files) {
        // Normalize paths for comparison
        const normalizePathForCompare = (p: string) => p.replace(/\\/g, '/').toLowerCase();
        
        diffResult.files.forEach((file) => {
          const diffContent = file.diff || '(No changes)';
          
          // Find the matching selected file
          const normalizedGitPath = normalizePathForCompare(file.path);
          const matchingFile = selectedFilesArray.find(sf => {
            const normalizedSelected = normalizePathForCompare(sf);
            const fullGitPath = normalizePathForCompare(selectedPath + '/' + file.path);
            
            return normalizedSelected === fullGitPath || 
                   normalizedSelected.endsWith('/' + normalizedGitPath);
          });
          
          if (matchingFile) {
            // Mark as modified
            markFileModified(matchingFile);
            
            // Update the diff view
            openFile({
              path: matchingFile,
              content: diffContent,
              language: 'diff'
            });
            setActiveFile(matchingFile);
          }
        });
      }
    } catch (error) {
      console.error('[GitManager] Error polling Git status:', error);
    }
  }, [selectedPath, selectedFiles, markFileModified, openFile, setActiveFile]);

  /**
   * Start polling Git status (like VS Code's Git integration)
   */
  const pollIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  
  const startWatch = useCallback(async (): Promise<{ success: boolean; error?: string }> => {
    if (!selectedPath || selectedFiles.size === 0) {
      return { success: false, error: 'No files selected' };
    }

    try {
      setScanStatus('running');
      
      // Poll Git status every 2 seconds
      pollIntervalRef.current = setInterval(() => {
        pollGitStatus();
      }, 2000);
      
      // Initial poll
      await pollGitStatus();
      
      return { success: true };
    } catch (error) {
      console.error('[GitManager] Watch failed:', error);
      setScanStatus('failed');
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }, [selectedPath, selectedFiles, setScanStatus, pollGitStatus]);

  /**
   * Stop polling Git status
   */
  const stopWatch = useCallback(async (): Promise<boolean> => {
    try {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
      setScanStatus(null);
      return true;
    } catch (error) {
      console.error('[GitManager] Error stopping watch:', error);
      return false;
    }
  }, [setScanStatus]);

  return {
    generateDiff,
    startWatch,
    stopWatch
  };
};
