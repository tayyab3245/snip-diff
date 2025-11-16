/**
 * Layout Component for SNIP-DIFF
 * Defines the entire application layout structure with consistent spacing and sizing
 */

import React from 'react';
import { useTheme } from '../theme';

interface LayoutProps {
  titleBar: React.ReactNode;
  toolbar: React.ReactNode;
  sidebar: React.ReactNode;
  mainContent: React.ReactNode;
  statusBar?: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ titleBar, toolbar, sidebar, mainContent, statusBar }) => {
  const { theme } = useTheme();

  const containerStyle: React.CSSProperties = {
    height: '100vh',
    width: '100vw',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
    background: theme.colors.background.primary,
  };

  const mainAreaStyle: React.CSSProperties = {
    flex: 1,
    display: 'flex',
    overflow: 'hidden',
  };

  const sidebarStyle: React.CSSProperties = {
    width: '280px',
    borderRight: `1px solid ${theme.colors.border.primary}`,
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  };

  const contentStyle: React.CSSProperties = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  };

  return (
    <div style={containerStyle}>
      {/* Title Bar - Fixed at top */}
      {titleBar}

      {/* Toolbar - Fixed below title bar */}
      {toolbar}

      {/* Main Area - Split between sidebar and content */}
      <div style={mainAreaStyle}>
        {/* Sidebar - Fixed width */}
        <div style={sidebarStyle}>
          {sidebar}
        </div>

        {/* Main Content - Flexible, takes remaining space */}
        <div style={contentStyle}>
          {mainContent}
        </div>
      </div>

      {/* Status Bar - Fixed at bottom (optional) */}
      {statusBar}
    </div>
  );
};

interface PanelLayoutProps {
  topBar?: React.ReactNode;
  content: React.ReactNode;
  bottomBar?: React.ReactNode;
}

/**
 * PanelLayout - Three-section vertical layout for panels
 * TOP: Context/status bar
 * MIDDLE: Main content (edge-to-edge, scrollable)
 * BOTTOM: Action buttons
 */
export const PanelLayout: React.FC<PanelLayoutProps> = ({ topBar, content, bottomBar }) => {
  const { theme } = useTheme();

  const containerStyle: React.CSSProperties = {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  };

  const topBarStyle: React.CSSProperties = {
    padding: '16px',
    borderBottom: `1px solid ${theme.colors.border.secondary}`,
    background: theme.colors.background.secondary,
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  };

  const contentStyle: React.CSSProperties = {
    flex: 1,
    overflow: 'auto',
    background: theme.colors.background.primary,
  };

  const bottomBarStyle: React.CSSProperties = {
    padding: '16px',
    borderTop: `1px solid ${theme.colors.border.secondary}`,
    background: theme.colors.background.secondary,
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  };

  return (
    <div style={containerStyle}>
      {topBar && <div style={topBarStyle}>{topBar}</div>}
      <div style={contentStyle}>{content}</div>
      {bottomBar && <div style={bottomBarStyle}>{bottomBar}</div>}
    </div>
  );
};
