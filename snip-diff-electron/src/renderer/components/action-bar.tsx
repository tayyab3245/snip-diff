/**
 * ActionBar Component for SNIP-DIFF
 * Bottom action bar with Scan, Prompts, and Copy All buttons
 */

import React from 'react';
import { useTheme } from '../theme';

interface ActionBarProps {
  onScan: () => void;
  onPrompts: () => void;
  onCopyAll: () => void;
  onSummarize: () => void;
  isScanning: boolean;
  scanDisabled: boolean;
}

export const ActionBar: React.FC<ActionBarProps> = ({ 
  onScan, 
  onPrompts, 
  onCopyAll, 
  onSummarize,
  isScanning, 
  scanDisabled 
}) => {
  const { theme } = useTheme();

  const containerStyle: React.CSSProperties = {
    height: '60px',
    backgroundColor: theme.colors.background.secondary,
    borderTop: `1px solid ${theme.colors.border.primary}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '0 20px',
    gap: '12px',
  };

  const actionButtonStyle: React.CSSProperties = {
    padding: '8px 16px',
    backgroundColor: 'transparent',
    border: `1px solid ${theme.colors.border.secondary}`,
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '13px',
    fontWeight: 500,
    color: theme.colors.text.primary,
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
  };

  const primaryButtonStyle: React.CSSProperties = {
    ...actionButtonStyle,
    backgroundColor: scanDisabled ? theme.colors.background.tertiary : 'transparent',
    cursor: scanDisabled ? 'not-allowed' : 'pointer',
    opacity: scanDisabled ? 0.5 : 1,
  };

  return (
    <div style={containerStyle}>
      <button
        style={primaryButtonStyle}
        onClick={onScan}
        disabled={scanDisabled}
      >
        <span>▶</span>
        <span>{isScanning ? 'Scanning...' : 'Scan'}</span>
      </button>

      <button
        style={actionButtonStyle}
        onClick={onPrompts}
      >
        <span>⊕</span>
        <span>Prompts</span>
      </button>

      <button
        style={actionButtonStyle}
        onClick={onCopyAll}
      >
        <span>⎘</span>
        <span>Copy All</span>
      </button>

      <button
        style={actionButtonStyle}
        onClick={onSummarize}
      >
        <span>✦</span>
        <span>Smart Summarize</span>
      </button>
    </div>
  );
};
