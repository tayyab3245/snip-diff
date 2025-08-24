/**
 * Main React App Component for SNIP-DIFF - Themed Version
 * Provides the main application layout with full theme support
 */

import React, { useEffect, useState } from 'react';
import { FileTree } from './components/FileTree';
import { DiffView } from './components/DiffView';
import { TitleBar } from './components/TitleBar';
import { useApiClient } from './hooks/useApiClient';
import { ThemeProvider, useTheme } from './theme';

// Main App Content Component (wrapped in theme provider)
const AppContent: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const { theme, toggleTheme, isDark } = useTheme();
  const { apiRequest } = useApiClient();
  
  // Test API connection on startup
  useEffect(() => {
    const checkConnection = async () => {
      setIsLoading(true);
      try {
        const response = await apiRequest({
          method: 'GET',
          endpoint: '/health'
        });
        console.log('API connection test:', response.success ? 'OK' : 'Failed');
      } catch (error) {
        console.error('Failed to connect to API:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    checkConnection();
  }, [apiRequest]);

  const appContainerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    backgroundColor: theme.colors.background.primary,
    color: theme.colors.text.primary,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif',
    WebkitFontSmoothing: 'antialiased',
    MozOsxFontSmoothing: 'grayscale',
    transition: 'background-color 0.3s ease, color 0.3s ease',
  };

  const mainContentStyle: React.CSSProperties = {
    display: 'flex',
    flex: 1,
    overflow: 'hidden',
  };

  const sidebarStyle: React.CSSProperties = {
    width: '350px',
    minWidth: '300px',
    backgroundColor: theme.colors.background.secondary,
    borderRight: `1px solid ${theme.colors.border.primary}`,
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  };

  const contentAreaStyle: React.CSSProperties = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  };

  const statusBarStyle: React.CSSProperties = {
    height: '24px',
    backgroundColor: theme.colors.background.secondary,
    borderTop: `1px solid ${theme.colors.border.primary}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0 12px',
    fontSize: '12px',
    color: theme.colors.text.secondary,
  };

  const loadingOverlayStyle: React.CSSProperties = {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: theme.colors.background.primary + 'ee',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
  };

  const loadingSpinnerStyle: React.CSSProperties = {
    width: '32px',
    height: '32px',
    border: `4px solid ${theme.colors.surface.base}`,
    borderTop: `4px solid ${theme.colors.primary[500]}`,
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  };

  const themeToggleButtonStyle: React.CSSProperties = {
    padding: '4px 8px',
    backgroundColor: 'transparent',
    border: `1px solid ${theme.colors.border.secondary}`,
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '12px',
    color: theme.colors.text.secondary,
    transition: 'all 0.2s ease',
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
  };

  return (
    <>
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>
      <div style={appContainerStyle}>
        <TitleBar />
        
        <div style={mainContentStyle}>
          <div style={sidebarStyle}>
            <FileTree />
          </div>
          
          <div style={contentAreaStyle}>
            <DiffView />
          </div>
        </div>
        
        <div style={statusBarStyle}>
          <span>Ready</span>
          <button
            style={themeToggleButtonStyle}
            onClick={toggleTheme}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = theme.colors.surface.hover;
              e.currentTarget.style.borderColor = theme.colors.border.focus;
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'transparent';
              e.currentTarget.style.borderColor = theme.colors.border.secondary;
            }}
            title={`Switch to ${isDark ? 'light' : 'dark'} theme`}
          >
            {isDark ? '☀️' : '🌙'} {isDark ? 'Light' : 'Dark'}
          </button>
        </div>
        
        {isLoading && (
          <div style={loadingOverlayStyle}>
            <div style={loadingSpinnerStyle} />
          </div>
        )}
      </div>
    </>
  );
};

// Main App Component with Theme Provider
export const App: React.FC = () => {
  return (
    <ThemeProvider defaultTheme="light">
      <AppContent />
    </ThemeProvider>
  );
};
