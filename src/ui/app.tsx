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
 * Main React App Component for SNIP-DIFF - Themed Version
 * Provides the main application layout with full theme support
 */

import React, { useEffect } from 'react';
import { Layout } from './components/layout';
import { ActionBar } from './components/action-bar';
import { FileTree } from './components/file-tree';
import { DiffView } from './components/diff-view';
import { TitleBar } from './components/title-bar';
import { ContextBar } from './components/context-bar';
import { ChatPanel } from './components/chat-panel';
import { useAppStore } from './store/app-store';
import { ThemeProvider } from './theme';
import { useClipboard } from './hooks/use-clipboard';
import { TokenTracker } from '../shared/token-tracker';

// Main App Content Component (wrapped in theme provider)
const AppContent: React.FC = () => {
  const clipboard = useClipboard();
  const { 
    selectedPath, 
    openFiles,
    activeFilePath,
    selectedFiles,  // Add selectedFiles to get the selected files from tree
    chatMessages, 
    isChatLoading, 
    chatPanelWidth,
    analyzedFilePaths,
    addChatMessage,
    clearChatMessages,
    setIsChatLoading,
    setChatPanelWidth,
    setAnalyzedFilePaths,
  } = useAppStore();

  // Auto-load Git status when folder is selected
  useEffect(() => {
    if (selectedPath) {
      // Git status will be checked when files are opened
      console.log('[App] Folder selected, Git tracking active:', selectedPath);
    }
  }, [selectedPath]);

  const handleCopyAll = async () => {
    const success = await clipboard.copyAllFiles();
    if (!success) {
      alert('Failed to copy to clipboard');
    }
  };

  const handleSummarize = async () => {
    // Clear previous chat messages and token tracking
    clearChatMessages();
    TokenTracker.getInstance().reset();
    setAnalyzedFilePaths([]);
    setIsChatLoading(true);

    try {
      // Check if LLM is available
      const { available } = await window.electronAPI.llmIsAvailable();
      
      if (!available) {
        addChatMessage({
          type: 'error',
          content: 'AI service is not available. Please set GEMINI_API_KEY environment variable.',
        });
        setIsChatLoading(false);
        return;
      }

      // Get current active file or open files
      if (!selectedPath) {
        addChatMessage({
          type: 'error',
          content: 'Please select a folder first.',
        });
        setIsChatLoading(false);
        return;
      }

      // Get files to analyze - prioritize selected files from tree, then fall back to open files
      const selectedFilesArray = Array.from(selectedFiles);
      const filesToAnalyze = selectedFilesArray.length > 0 
        ? selectedFilesArray 
        : (activeFilePath ? [activeFilePath] : openFiles.map(f => f.path));

      if (filesToAnalyze.length === 0) {
        addChatMessage({
          type: 'error',
          content: 'Please select files in the file tree or open a file first.',
        });
        setIsChatLoading(false);
        return;
      }

      // Store analyzed files so they persist
      setAnalyzedFilePaths(filesToAnalyze);

      // Track original file content tokens
      const tokenTracker = TokenTracker.getInstance();
      for (const filePath of filesToAnalyze) {
        const fileData = openFiles.find(f => f.path === filePath);
        if (fileData) {
          tokenTracker.trackOriginalFile(filePath, fileData.content);
        } else {
          // Read file content for tracking if not already open
          try {
            const content = await window.electronAPI.readFile(filePath);
            if (content) {
              tokenTracker.trackOriginalFile(filePath, content);
            }
          } catch (error) {
            console.warn(`Failed to read file for token tracking: ${filePath}`);
          }
        }
      }

      // Call LLM service - main process will handle getting content/diffs
      const result = await window.electronAPI.llmSummarizeDiff(selectedPath, filesToAnalyze);

      if (result.success && result.summary) {
        // Track the summary tokens
        if (filesToAnalyze.length === 1) {
          tokenTracker.trackSummary(filesToAnalyze[0], result.summary);
        } else {
          // For multiple files, track against all files (approximate)
          filesToAnalyze.forEach(filePath => {
            tokenTracker.trackSummary(filePath, result.summary);
          });
        }

        addChatMessage({
          type: 'ai',
          content: result.summary,
          isTyping: true,
        });
      } else {
        addChatMessage({
          type: 'error',
          content: `Failed to generate summary: ${result.error || 'Unknown error'}`,
        });
      }
    } catch (error) {
      console.error('[AI] Summarize error:', error);
      addChatMessage({
        type: 'error',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
      });
    } finally {
      setIsChatLoading(false);
    }
  };

  return (
    <Layout
      titleBar={<TitleBar />}
      toolbar={<ContextBar />}
      sidebar={<FileTree />}
      mainContent={<DiffView />}
      chatPanel={<ChatPanel messages={chatMessages} isLoading={isChatLoading} fileCount={analyzedFilePaths.length} filePaths={analyzedFilePaths} onCopyAll={handleCopyAll} />}
      chatPanelWidth={chatPanelWidth}
      onChatPanelResize={setChatPanelWidth}
      statusBar={
        <ActionBar 
          onSummarize={handleSummarize}
          isDisabled={isChatLoading}
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
