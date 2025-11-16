/**
 * ActionBar Component for SNIP-DIFF
 * Bottom action bar with Scan, Prompts, and Copy All buttons
 */

import React from 'react';
import { useTheme } from '../theme';

interface ActionBarProps {
  onCopyAll: () => void;
  onSummarize: () => void;
}

export const ActionBar: React.FC<ActionBarProps> = ({ 
  onCopyAll, 
  onSummarize
}) => {
  const { theme } = useTheme();

  const containerStyle: React.CSSProperties = {
    height: '64px',
    backgroundColor: theme.colors.background.secondary,
    borderTop: `1px solid ${theme.colors.border.primary}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 20px',
    gap: '12px',
  };

  const actionButtonStyle: React.CSSProperties = {
    padding: '12px 24px',
    backgroundColor: 'transparent',
    border: `1px solid ${theme.colors.border.secondary}`,
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '15px',
    fontWeight: 500,
    color: theme.colors.text.primary,
    display: 'flex',
    alignItems: 'center',
  };

  return (
    <div style={containerStyle}>
      <button
        style={actionButtonStyle}
        onClick={onCopyAll}
      >
        <span>Copy All</span>
      </button>

      <button
        style={actionButtonStyle}
        onClick={onSummarize}
        title="Summarize selected files from the tree, or open files if none selected"
      >
        <span>Summarize</span>
      </button>
    </div>
  );
};
