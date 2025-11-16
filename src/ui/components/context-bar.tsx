/**
 * ContextBar Component for SNIP-DIFF
 * Top context bar with view mode toggles
 */

import React from 'react';
import { useTheme } from '../theme';
import { useAppStore } from '../store/app-store';

export const ContextBar: React.FC = () => {
  const { theme } = useTheme();
  const { viewMode, diffMode, setViewMode, setDiffMode, selectedFiles } = useAppStore();

  const selectedCount = selectedFiles.size;

  const contextBarStyle: React.CSSProperties = {
    height: '64px',
    backgroundColor: theme.colors.background.secondary,
    borderBottom: `1px solid ${theme.colors.border.primary}`,
    display: 'grid',
    gridTemplateColumns: '1fr auto 1fr',
    alignItems: 'center',
    padding: '0 20px',
    gap: '16px',
  };

  const leftSectionStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    color: theme.colors.text.secondary,
    fontSize: '15px',
  };

  const selectedCountStyle: React.CSSProperties = {
    color: selectedCount > 0 ? '#38bdf8' : theme.colors.text.secondary,
    fontWeight: selectedCount > 0 ? 600 : 400,
  };

  const centerSectionStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
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
    padding: '10px 16px',
    backgroundColor: isActive ? theme.colors.background.secondary : 'transparent',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 500,
    color: isActive ? theme.colors.text.primary : theme.colors.text.tertiary,
  });

  return (
    <div style={contextBarStyle}>
      <div style={leftSectionStyle}>
        <span style={selectedCountStyle}>
          {selectedCount > 0 
            ? `${selectedCount} file${selectedCount > 1 ? 's' : ''} selected for AI` 
            : 'Select files in tree for AI summarization'
          }
        </span>
      </div>

      <div style={centerSectionStyle}>
        <div style={toggleGroupStyle}>
          <button
            style={toggleButtonStyle(viewMode === 'incremental')}
            onClick={() => setViewMode('incremental')}
          >
            Changes Only
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

      <div />
    </div>
  );
};
