/**
 * ContextBar Component for SNIP-DIFF
 * Top context bar with view mode toggles
 */

import React from 'react';
import { useTheme } from '../theme';
import { useAppStore } from '../store/app-store';

export const ContextBar: React.FC = () => {
  const { theme } = useTheme();
  const { viewMode, diffMode, setViewMode, setDiffMode, selectChangedFiles, gitStatus } = useAppStore();

  const hasChangedFiles = Array.from(gitStatus.values()).some(status => status !== 'Unchanged');

  const contextBarStyle: React.CSSProperties = {
    height: '56px',
    backgroundColor: theme.colors.background.secondary,
    borderBottom: `1px solid ${theme.colors.border.primary}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 20px',
    gap: '16px',
  };

  const rightSectionStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  };

  const toggleGroupStyle: React.CSSProperties = {
    display: 'flex',
    backgroundColor: theme.colors.background.primary,
    borderRadius: '6px',
    padding: '2px',
    gap: '2px',
  };

  const toggleButtonStyle = (isActive: boolean): React.CSSProperties => ({
    padding: '6px 12px',
    backgroundColor: isActive ? theme.colors.background.secondary : 'transparent',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '12px',
    fontWeight: 500,
    color: isActive ? theme.colors.text.primary : theme.colors.text.tertiary,
  });

  return (
    <div style={contextBarStyle}>
      <div style={rightSectionStyle}>
        {hasChangedFiles && (
          <button
            style={{
              ...toggleButtonStyle(false),
              backgroundColor: theme.colors.primary[500],
              color: '#ffffff',
              padding: '8px 16px',
            }}
            onClick={() => selectChangedFiles()}
          >
            Select Changed Files
          </button>
        )}

        <div style={toggleGroupStyle}>
          <button
            style={toggleButtonStyle(viewMode === 'incremental')}
            onClick={() => setViewMode('incremental')}
          >
            Incremental
          </button>
          <button
            style={toggleButtonStyle(viewMode === 'full')}
            onClick={() => setViewMode('full')}
          >
            Full File
          </button>
        </div>

        <div style={toggleGroupStyle}>
          <button
            style={toggleButtonStyle(diffMode === 'unified')}
            onClick={() => setDiffMode('unified')}
          >
            Unified
          </button>
          <button
            style={toggleButtonStyle(diffMode === 'side-by-side')}
            onClick={() => setDiffMode('side-by-side')}
          >
            Side-by-side
          </button>
        </div>
      </div>
    </div>
  );
};
