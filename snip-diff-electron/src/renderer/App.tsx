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
  const [isScanning, setIsScanning] = useState(false);
  const { apiRequest, startScan, getScanResults } = useApiClient();
  const { 
    selectedFiles, 
    selectedPath, 
    setScanStatus, 
    setScanProgress,
    setDiffSections 
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

  const handleScan = async () => {
    if (!selectedPath || selectedFiles.size === 0) return;

    setIsScanning(true);
    setScanStatus('running');
    setScanProgress(0);

    try {
      // Convert Set to Array for API
      const selectedFilesArray = Array.from(selectedFiles);
      
      const response = await startScan(selectedPath, selectedFilesArray);
      console.log('Scan response:', response);

      if (response.success && response.data?.scan_id) {
        const scanId = response.data.scan_id;
        setDiffSections([]); // Clear previous results
        
        // Poll for results
        let attempts = 0;
        const maxAttempts = 30;
        
        const pollInterval = setInterval(async () => {
          attempts++;
          const progress = (attempts / maxAttempts) * 100;
          setScanProgress(Math.min(progress, 95));
          
          try {
            const resultsResponse = await getScanResults(scanId);
            console.log('Results response:', resultsResponse);
            
            if (resultsResponse.success && resultsResponse.data) {
              clearInterval(pollInterval);
              setScanStatus('completed');
              setIsScanning(false);
              setScanProgress(100);
              
              // Set the diff sections
              const sections = resultsResponse.data.sections || [];
              console.log('Setting diff sections:', sections);
              setDiffSections(sections);
            }
          } catch (error) {
            console.log('Polling for results, attempt:', attempts);
            // Continue polling
          }
          
          if (attempts >= maxAttempts) {
            clearInterval(pollInterval);
            setScanStatus('failed');
            setIsScanning(false);
            console.error('Scan timeout - results not available');
          }
        }, 1000);
      } else {
        setScanStatus('failed');
        setIsScanning(false);
        console.error('Scan failed:', response);
      }
    } catch (error) {
      console.error('Diff scan failed:', error);
      setScanStatus('failed');
      setIsScanning(false);
    }
  };

  const handleCopyAll = () => {
    console.log('Copy all to clipboard');
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
          onScan={handleScan}
          onCopyAll={handleCopyAll}
          onPrompts={handlePrompts}
          onSummarize={handleSummarize}
          isScanning={isScanning}
          scanDisabled={!selectedPath || selectedFiles.size === 0}
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
