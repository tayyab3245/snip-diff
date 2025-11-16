/**
 * TitleBar Component for SNIP-DIFF
 * Provides custom title bar with window controls for frameless window
 */

import React from 'react';
import { useTheme } from '../theme';

export const TitleBar: React.FC = () => {
  const { theme } = useTheme();

  const handleMinimize = async () => {
    try {
      await window.electronAPI.windowMinimize();
    } catch (error) {
      console.error('Failed to minimize window:', error);
    }
  };

  const handleMaximize = async () => {
    try {
      await window.electronAPI.windowMaximize();
    } catch (error) {
      console.error('Failed to maximize window:', error);
    }
  };

  const handleClose = async () => {
    try {
      await window.electronAPI.windowClose();
    } catch (error) {
      console.error('Failed to close window:', error);
    }
  };

  const titleBarStyle: React.CSSProperties = {
    height: '32px',
    background: theme.colors.background.secondary,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0 16px',
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
  };

  const windowControlsStyle: React.CSSProperties = {
    display: 'flex',
    gap: '8px',
    // @ts-ignore - Electron specific property
    WebkitAppRegion: 'no-drag',
  };

  const controlButtonBaseStyle: React.CSSProperties = {
    width: '32px',
    height: '24px',
    border: 'none',
    borderRadius: '0',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '14px',
    background: 'transparent',
    color: theme.colors.text.secondary,
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

  return (
    <div style={titleBarStyle}>
      <div style={titleSectionStyle}>
        <span style={appTitleStyle}>SNIP-DIFF</span>
      </div>

      <div style={windowControlsStyle}>
        <button 
          style={minimizeButtonStyle} 
          onClick={handleMinimize} 
          title="Minimize"
        >
          −
        </button>
        <button 
          style={maximizeButtonStyle} 
          onClick={handleMaximize} 
          title="Maximize"
        >
          □
        </button>
        <button 
          style={closeButtonStyle} 
          onClick={handleClose} 
          title="Close"
        >
          ×
        </button>
      </div>
    </div>
  );
};
