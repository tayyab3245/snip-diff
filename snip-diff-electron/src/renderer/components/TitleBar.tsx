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

  const appIconStyle: React.CSSProperties = {
    width: '20px',
    height: '20px',
    background: theme.colors.gradients.primary,
    borderRadius: '4px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: 'white',
    fontWeight: 'bold',
    fontSize: '12px',
    boxShadow: theme.colors.shadows.neumorphic.raised,
  };

  const appTitleStyle: React.CSSProperties = {
    fontSize: '14px',
    fontWeight: 500,
    color: theme.colors.text.primary,
  };

  const windowControlsStyle: React.CSSProperties = {
    display: 'flex',
    gap: '8px',
    // @ts-ignore - Electron specific property
    WebkitAppRegion: 'no-drag',
  };

  const controlButtonBaseStyle: React.CSSProperties = {
    width: '20px',
    height: '20px',
    border: 'none',
    borderRadius: '50%',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '12px',
    transition: 'all 0.2s ease',
    background: theme.colors.background.secondary,
    boxShadow: theme.colors.shadows.neumorphic.raised,
  };

  const minimizeButtonStyle: React.CSSProperties = {
    ...controlButtonBaseStyle,
    color: theme.colors.semantic.warning,
  };

  const maximizeButtonStyle: React.CSSProperties = {
    ...controlButtonBaseStyle,
    color: theme.colors.semantic.success,
  };

  const closeButtonStyle: React.CSSProperties = {
    ...controlButtonBaseStyle,
    color: theme.colors.semantic.error,
  };

  return (
    <div style={titleBarStyle}>
      <div style={titleSectionStyle}>
        <div style={appIconStyle}>S</div>
        <span style={appTitleStyle}>SNIP-DIFF</span>
      </div>

      <div style={windowControlsStyle}>
        <button style={minimizeButtonStyle} onClick={handleMinimize} title="Minimize">
          −
        </button>
        <button style={maximizeButtonStyle} onClick={handleMaximize} title="Maximize">
          □
        </button>
        <button style={closeButtonStyle} onClick={handleClose} title="Close">
          ×
        </button>
      </div>
    </div>
  );
};
