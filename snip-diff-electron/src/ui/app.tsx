/**
 * Main React App Component for SNIP-DIFF - Themed Version
 * Provides the main application layout with full theme support
 */

import React, { useEffect, useState } from 'react';
import { Layout } from './components/layout';
import { ActionBar } from './components/action-bar';
import { FileTree } from './components/file-tree';
import { DiffView } from './components/diff-view';
import { TitleBar } from './components/title-bar';
import { ContextBar } from './components/context-bar';
import { useApiClient } from './hooks/use-api-client';
import { useAppStore } from './store/app-store';
import { ThemeProvider } from './theme';

// Main App Content Component (wrapped in theme provider)
const AppContent: React.FC = () => {
  const [isWatching, setIsWatching] = useState(false);
  const { apiRequest } = useApiClient();
  const { 
    selectedFiles, 
    selectedPath, 
    setScanStatus, 
    setDiffSections,
    openFiles
  } = useAppStore();
  
  // Test API connection on startup
  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await apiRequest({
          method: 'GET',
          endpoint: '/health'
        });
        console.log('API connection test:', response.success ? 'OK' : 'Failed');
      } catch (error) {
        console.error('Failed to connect to API:', error);
      }
    };
    
    checkConnection();
  }, [apiRequest]);

  // Listen for file changes from Chokidar
  useEffect(() => {
    console.log('[Renderer] Setting up file change listener. isWatching:', isWatching, 'selectedFiles:', Array.from(selectedFiles));
    
    const handleFileChange = async (filePath: string) => {
      console.log('[Renderer] File changed:', filePath);
      console.log('[Renderer] Current state - isWatching:', isWatching, 'selectedPath:', selectedPath);
      
      if (!selectedPath || !isWatching) {
        console.log('[Renderer] Skipping diff - not watching or no path selected');
        return;
      }
      
      // Get Git diff directly from main process (no API needed!)
      try {
        console.log('[Renderer] Getting Git diff...');
        setScanStatus('running');
        
        const selectedFilesArray = Array.from(selectedFiles);
        console.log('[Renderer] Scanning files:', selectedFilesArray);
        
        const diffResult = await window.electronAPI.getGitDiff(selectedPath, selectedFilesArray);
        
        console.log('[Renderer] Git diff result:', diffResult);
        
        if (diffResult.success && diffResult.files) {
          // Convert Git diff format to sections format
          const sections = diffResult.files.map((file: { path: string; status: string; diff: string }) => ({
            title: `${file.status}: ${file.path}`,
            files: [{
              path: file.path,
              change_type: file.status,
              content: file.diff
            }],
            collapsed: false
          }));
          
          console.log('[Renderer] Diff sections:', sections);
          setDiffSections(sections);
          setScanStatus(sections.length > 0 ? 'completed' : null);
        } else {
          console.error('[Renderer] Git diff failed:', diffResult.error);
          setScanStatus('failed');
        }
      } catch (error) {
        console.error('[Renderer] Error fetching diff:', error);
        setScanStatus('failed');
      }
    };

    window.electronAPI.onFileChanged(handleFileChange);
  }, [setScanStatus, selectedPath, selectedFiles, isWatching, setDiffSections]);

  const handleWatch = async () => {
    if (!selectedPath || selectedFiles.size === 0) return;

    if (isWatching) {
      // Stop watching
      try {
        const response = await window.electronAPI.stopWatch();
        if (response.success) {
          console.log('Stopped watching files');
          setIsWatching(false);
          setScanStatus(null);
          setDiffSections([]);
        }
      } catch (error) {
        console.error('Error stopping watch:', error);
      }
      return;
    }

    // Start watching
    setIsWatching(true);
    setScanStatus('running');

    try {
      // Convert Set to Array for watching
      const selectedFilesArray = Array.from(selectedFiles);
      
      const response = await window.electronAPI.startWatch(selectedFilesArray);
      console.log('Watch started:', response);

      if (!response.success) {
        setScanStatus('failed');
        setIsWatching(false);
        console.error('Watch failed:', response);
      }
    } catch (error) {
      console.error('Watch failed:', error);
      setScanStatus('failed');
      setIsWatching(false);
    }
  };

  const handleCopyAll = async () => {
    if (openFiles.length === 0) {
      console.log('No files to copy');
      return;
    }

    try {
      const fileContents: string[] = [];

      // Collect content from all open files
      for (const file of openFiles) {
        fileContents.push(`// File: ${file.path}\n${file.content}`);
      }

      const combinedContent = fileContents.join('\n\n' + '='.repeat(80) + '\n\n');
      
      // Copy to clipboard
      await navigator.clipboard.writeText(combinedContent);
      console.log(`Copied ${openFiles.length} file(s) to clipboard`);
      
      // Optional: Show visual feedback
      // You could add a toast notification here
    } catch (error) {
      console.error('Failed to copy files:', error);
      alert('Failed to copy to clipboard');
    }
  };

  const handlePrompts = () => {
    console.log('Open prompts');
  };

  const handleSummarize = () => {
    console.log('Smart summarize');
  };

  return (
    <Layout
      titleBar={<TitleBar />}
      toolbar={<ContextBar />}
      sidebar={<FileTree />}
      mainContent={<DiffView />}
      statusBar={
        <ActionBar 
          onWatch={handleWatch}
          onCopyAll={handleCopyAll}
          onPrompts={handlePrompts}
          onSummarize={handleSummarize}
          isWatching={isWatching}
          watchDisabled={!selectedPath || selectedFiles.size === 0}
        />
      }
    />
  );
};

// Main App Component with Dark Theme Only
export const App: React.FC = () => {
  return (
    <ThemeProvider defaultTheme="dark">
      <AppContent />
    </ThemeProvider>
  );
};
