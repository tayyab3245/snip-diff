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
  chatPanel?: React.ReactNode;
  chatPanelWidth?: number;
  onChatPanelResize?: (width: number) => void;
  statusBar?: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ 
  titleBar, 
  toolbar, 
  sidebar, 
  mainContent, 
  chatPanel,
  chatPanelWidth = 400,
  onChatPanelResize,
  statusBar 
}) => {
  const { theme } = useTheme();
  const [isDragging, setIsDragging] = React.useState(false);
  const [dragStartX, setDragStartX] = React.useState(0);
  const [dragStartWidth, setDragStartWidth] = React.useState(chatPanelWidth);

  React.useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isDragging && onChatPanelResize) {
        const deltaX = dragStartX - e.clientX;
        const newWidth = Math.max(300, Math.min(800, dragStartWidth + deltaX));
        onChatPanelResize(newWidth);
      }
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragStartX, dragStartWidth, onChatPanelResize]);

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
    flexDirection: 'row',
    overflow: 'hidden',
  };

  const contentAreaStyle: React.CSSProperties = {
    flex: 1,
    overflow: 'hidden',
    minWidth: 0,
    display: 'flex',
    flexDirection: 'column',
  };

  const chatPanelContainerStyle: React.CSSProperties = {
    width: `${chatPanelWidth}px`,
    borderLeft: `1px solid ${theme.colors.border.primary}`,
    overflow: 'hidden',
    position: 'relative',
    flexShrink: 0,
  };

  const resizerStyle: React.CSSProperties = {
    position: 'absolute',
    top: 0,
    left: 0,
    bottom: 0,
    width: '4px',
    cursor: 'ew-resize',
    backgroundColor: 'transparent',
    zIndex: 10,
  };

  const resizerActiveStyle: React.CSSProperties = {
    ...resizerStyle,
    backgroundColor: theme.colors.primary[500],
  };

  const handleResizerMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsDragging(true);
    setDragStartX(e.clientX);
    setDragStartWidth(chatPanelWidth);
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
          <div style={contentAreaStyle}>
            {mainContent}
          </div>

          {/* Chat Panel - Resizable on right */}
          {chatPanel && (
            <div style={chatPanelContainerStyle}>
              <div
                style={isDragging ? resizerActiveStyle : resizerStyle}
                onMouseDown={handleResizerMouseDown}
              />
              {chatPanel}
            </div>
          )}
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
