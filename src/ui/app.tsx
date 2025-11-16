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

    // Simulate AI response
    setTimeout(() => {
      addChatMessage({
        type: 'ai',
        content: `I've analyzed the changes in your repository. Here's what I found:\n\n• **${chatMessages.length + 1} files modified** with significant changes\n• Main focus areas: UI components and state management\n• Key improvements: Enhanced Git integration and tabbed interface\n• Potential concerns: None detected\n\nWould you like me to generate a detailed commit message or explain any specific changes?`,
      });
      setIsChatLoading(false);
    }, 1500);
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
