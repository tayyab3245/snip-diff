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
import { useAppStore } from './store/app-store';
import { ThemeProvider } from './theme';
import { useClipboard } from './hooks/use-clipboard';

// Main App Content Component (wrapped in theme provider)
const AppContent: React.FC = () => {
  const clipboard = useClipboard();
  const { selectedPath } = useAppStore();

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
