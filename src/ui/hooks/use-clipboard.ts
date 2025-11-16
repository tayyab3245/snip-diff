/**
 * Clipboard Hook
 * Handles clipboard operations for copying file content
 */

import { useCallback } from 'react';
import { useAppStore } from '../store/app-store';

export const useClipboard = () => {
  const { openFiles } = useAppStore();

  /**
   * Copy all open files to clipboard
   */
  const copyAllFiles = useCallback(async (): Promise<boolean> => {
    if (openFiles.length === 0) {
      console.warn('No files to copy');
      return false;
    }

    try {
      const fileContents = openFiles.map(file => 
        `// File: ${file.path}\n${file.content}`
      );

      const combinedContent = fileContents.join('\n\n' + '='.repeat(80) + '\n\n');
      
      await navigator.clipboard.writeText(combinedContent);
      console.log(`Copied ${openFiles.length} file(s) to clipboard`);
      return true;
    } catch (error) {
      console.error('Failed to copy files:', error);
      return false;
    }
  }, [openFiles]);

  /**
   * Copy specific text to clipboard
   */
  const copyText = useCallback(async (text: string): Promise<boolean> => {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (error) {
      console.error('Failed to copy text:', error);
      return false;
    }
  }, []);

  return {
    copyAllFiles,
    copyText
  };
};
