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
    addChatMessage,
    setIsChatLoading,
    setChatPanelWidth,
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

  const handlePrompts = () => {
    addChatMessage({
      type: 'system',
      content: 'Opening prompts library...',
    });
    // TODO: Open prompts modal/sidebar
  };

  const handleSummarize = async () => {
    setIsChatLoading(true);
    addChatMessage({
      type: 'system',
      content: 'Analyzing changes and generating summary...',
    });

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
      
      addChatMessage({
        type: 'system',
        content: `Analyzing ${filesToAnalyze.length} selected file${filesToAnalyze.length > 1 ? 's' : ''}...`,
      });

      // Call LLM service - main process will handle getting content/diffs
      const result = await window.electronAPI.llmSummarizeDiff(selectedPath, filesToAnalyze);

      if (result.success && result.summary) {
        addChatMessage({
          type: 'ai',
          content: result.summary,
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
      chatPanel={<ChatPanel messages={chatMessages} isLoading={isChatLoading} />}
      chatPanelWidth={chatPanelWidth}
      onChatPanelResize={setChatPanelWidth}
      statusBar={
        <ActionBar 
          onCopyAll={handleCopyAll}
          onPrompts={handlePrompts}
          onSummarize={handleSummarize}
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
