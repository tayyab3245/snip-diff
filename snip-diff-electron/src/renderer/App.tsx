/**
 * Main React App Component for SNIP-DIFF
 * Provides the main application layout and routing
 */

import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { FileTree } from './components/FileTree';
import { DiffView } from './components/DiffView';
import { TitleBar } from './components/TitleBar';
import { useApiClient } from './hooks/useApiClient';
import { useAppStore } from './store/appStore';

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #e0e5ec;
  color: #333;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
`;

const MainContent = styled.div`
  display: flex;
  flex: 1;
  overflow: hidden;
`;

const Sidebar = styled.div`
  width: 350px;
  min-width: 250px;
  max-width: 500px;
  background: #e0e5ec;
  border-right: 1px solid #c5c5c5;
  resize: horizontal;
  overflow: auto;
`;

const ContentArea = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
`;

const StatusBar = styled.div`
  height: 30px;
  background: #e0e5ec;
  border-top: 1px solid #c5c5c5;
  display: flex;
  align-items: center;
  padding: 0 16px;
  font-size: 12px;
  color: #666;
  box-shadow: inset 2px 2px 5px #bebebe, inset -2px -2px 5px #ffffff;
`;

const LoadingOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(224, 229, 236, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const LoadingSpinner = styled.div`
  width: 40px;
  height: 40px;
  border: 4px solid #e0e5ec;
  border-top: 4px solid #666;
  border-radius: 50%;
  animation: spin 1s linear infinite;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

export const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [appVersion, setAppVersion] = useState<string>('');
  const { apiRequest } = useApiClient();
  const { selectedPath, scanStatus } = useAppStore();

  useEffect(() => {
    // Initialize app
    const initializeApp = async () => {
      try {
        // Get app version
        const version = await window.electronAPI.getAppVersion();
        setAppVersion(version);

        // Test API connection
        const response = await apiRequest({
          method: 'GET',
          endpoint: '/health'
        });

        if (response.success) {
          console.log('FastAPI backend connected successfully');
        } else {
          console.warn('Failed to connect to FastAPI backend');
        }

      } catch (error) {
        console.error('App initialization error:', error);
      } finally {
        setIsLoading(false);
      }
    };

    initializeApp();
  }, [apiRequest]);

  if (isLoading) {
    return (
      <AppContainer>
        <LoadingOverlay>
          <LoadingSpinner />
        </LoadingOverlay>
      </AppContainer>
    );
  }

  return (
    <AppContainer>
      <TitleBar />
      
      <MainContent>
        <Sidebar>
          <FileTree />
        </Sidebar>
        
        <ContentArea>
          <DiffView />
        </ContentArea>
      </MainContent>
      
      <StatusBar>
        <span>SNIP-DIFF v{appVersion}</span>
        {selectedPath && (
          <>
            <span style={{ margin: '0 16px' }}>|</span>
            <span>📁 {selectedPath}</span>
          </>
        )}
        {scanStatus && (
          <>
            <span style={{ margin: '0 16px' }}>|</span>
            <span>🔍 {scanStatus}</span>
          </>
        )}
        <div style={{ flex: 1 }} />
        <span>Ready</span>
      </StatusBar>
    </AppContainer>
  );
};
