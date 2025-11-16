/**
 * TitleBar Component for SNIP-DIFF
 * Provides custom title bar with window controls for frameless window
 */

import React from 'react';
import { useTheme } from '../theme';
import { useWindowControls } from '../hooks/use-window-controls';
import { useFileManager } from '../hooks/use-file-manager';

const Logo: React.FC<{ style?: React.CSSProperties }> = ({ style }) => (
  <svg 
    version="1.2" 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 470 638" 
    style={style}
  >
    <image 
      width="470" 
      height="638" 
      href="/snip-diff.svg"
    />
  </svg>
);

export const TitleBar: React.FC = () => {
  const { theme } = useTheme();
  const windowControls = useWindowControls();
  const fileManager = useFileManager();
  const [fileMenuOpen, setFileMenuOpen] = React.useState(false);
  const menuRef = React.useRef<HTMLDivElement>(null);

  // Close menu when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setFileMenuOpen(false);
      }
    };

    if (fileMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [fileMenuOpen]);

  const titleBarStyle: React.CSSProperties = {
    height: '32px',
    background: theme.colors.background.secondary,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0 16px 0 8px',
    borderBottom: `1px solid ${theme.colors.border.secondary}`,
    userSelect: 'none',
    boxShadow: theme.colors.shadows.neumorphic.raised,
    // @ts-ignore - Electron specific property
    WebkitAppRegion: 'drag',
  };

  const titleSectionStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  };

  const appTitleStyle: React.CSSProperties = {
    fontSize: '13px',
    fontWeight: 600,
    color: theme.colors.text.primary,
    letterSpacing: '0.3px',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  };

  const logoStyle: React.CSSProperties = {
    height: '18px',
    width: 'auto',
  };

  const menuBarStyle: React.CSSProperties = {
    display: 'flex',
    gap: '2px',
    // @ts-ignore - Electron specific property
    WebkitAppRegion: 'no-drag',
  };

  const menuButtonStyle: React.CSSProperties = {
    padding: '5px 10px',
    border: 'none',
    borderRadius: '0',
    cursor: 'pointer',
    fontSize: '13px',
    fontWeight: 400,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif',
    background: fileMenuOpen ? theme.colors.background.tertiary : 'transparent',
    color: theme.colors.text.primary,
    transition: 'background 0.1s',
  };

  const windowControlsStyle: React.CSSProperties = {
    display: 'flex',
    gap: '0',
    // @ts-ignore - Electron specific property
    WebkitAppRegion: 'no-drag',
  };

  const controlButtonBaseStyle: React.CSSProperties = {
    width: '46px',
    height: '32px',
    border: 'none',
    borderRadius: '0',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '16px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif',
    background: 'transparent',
    color: theme.colors.text.secondary,
    transition: 'background 0.1s',
  };

  const minimizeButtonStyle: React.CSSProperties = {
    ...controlButtonBaseStyle,
  };

  const maximizeButtonStyle: React.CSSProperties = {
    ...controlButtonBaseStyle,
  };

  const closeButtonStyle: React.CSSProperties = {
    ...controlButtonBaseStyle,
  };

  const dropdownStyle: React.CSSProperties = {
    position: 'absolute',
    top: '32px',
    left: '8px',
    minWidth: '220px',
    background: theme.colors.background.secondary,
    border: `1px solid ${theme.colors.border.light}`,
    borderRadius: '0',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.5)',
    zIndex: 1000,
    overflow: 'hidden',
  };

  const dropdownItemStyle: React.CSSProperties = {
    padding: '6px 32px 6px 16px',
    cursor: 'pointer',
    fontSize: '13px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif',
    fontWeight: 400,
    color: theme.colors.text.primary,
    background: 'transparent',
    border: 'none',
    width: '100%',
    textAlign: 'left',
    display: 'block',
    transition: 'background 0.1s',
  };

  const handleOpenFolder = async () => {
    setFileMenuOpen(false);
    await fileManager.selectFolder();
  };

  const handleOpenFile = async () => {
    setFileMenuOpen(false);
    const filePaths = await window.electronAPI.selectFiles();
    if (filePaths && filePaths.length > 0) {
      for (const filePath of filePaths) {
        await fileManager.openFileWithContent(filePath);
      }
    }
  };

  return (
    <div style={titleBarStyle}>
      <div style={titleSectionStyle}>
        <div style={appTitleStyle}>
          <Logo style={logoStyle} />
        </div>
        <div style={menuBarStyle} ref={menuRef}>
          <button 
            style={menuButtonStyle}
            onClick={() => setFileMenuOpen(!fileMenuOpen)}
            onMouseEnter={(e) => !fileMenuOpen && (e.currentTarget.style.background = theme.colors.background.tertiary)}
            onMouseLeave={(e) => !fileMenuOpen && (e.currentTarget.style.background = 'transparent')}
          >
            File
          </button>
          <button 
            style={menuButtonStyle}
            onMouseEnter={(e) => e.currentTarget.style.background = theme.colors.background.tertiary}
            onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
          >
            Edit
          </button>
          <button 
            style={menuButtonStyle}
            onMouseEnter={(e) => e.currentTarget.style.background = theme.colors.background.tertiary}
            onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
          >
            View
          </button>
          <button 
            style={menuButtonStyle}
            onMouseEnter={(e) => e.currentTarget.style.background = theme.colors.background.tertiary}
            onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
          >
            Help
          </button>
          {fileMenuOpen && (
            <div style={dropdownStyle}>
              <button 
                style={dropdownItemStyle}
                onClick={handleOpenFile}
                onMouseEnter={(e) => e.currentTarget.style.background = theme.colors.background.primary}
                onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
              >
                Open File...
              </button>
              <button 
                style={dropdownItemStyle}
                onClick={handleOpenFolder}
                onMouseEnter={(e) => e.currentTarget.style.background = theme.colors.background.primary}
                onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
              >
                Open Folder...
              </button>
            </div>
          )}
        </div>
      </div>

      <div style={windowControlsStyle}>
        <button 
          style={minimizeButtonStyle} 
          onClick={windowControls.minimize} 
          title="Minimize"
          onMouseEnter={(e) => e.currentTarget.style.background = theme.colors.background.tertiary}
          onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
        >
          −
        </button>
        <button 
          style={maximizeButtonStyle} 
          onClick={windowControls.maximize} 
          title="Maximize"
          onMouseEnter={(e) => e.currentTarget.style.background = theme.colors.background.tertiary}
          onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
        >
          □
        </button>
        <button 
          style={closeButtonStyle} 
          onClick={windowControls.close} 
          title="Close"
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#e81123';
            e.currentTarget.style.color = '#ffffff';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'transparent';
            e.currentTarget.style.color = theme.colors.text.secondary;
          }}
        >
          ×
        </button>
      </div>
    </div>
  );
};
