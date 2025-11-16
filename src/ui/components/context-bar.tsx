/**
 * ContextBar Component for SNIP-DIFF
 * Top context bar with view mode toggles
 */

import React from 'react';
import { useTheme } from '../theme';
import { useAppStore } from '../store/app-store';

// Inject gradient animation styles
const styleSheet = document.createElement('style');
styleSheet.textContent = `
  @keyframes aiGradient {
    0%, 100% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
  }
  
  @keyframes aiPulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.85;
    }
  }
`;
if (!document.head.querySelector('[data-ai-gradient]')) {
  styleSheet.setAttribute('data-ai-gradient', 'true');
  document.head.appendChild(styleSheet);
}

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
    ...(selectedCount > 0 ? {
      background: 'linear-gradient(90deg, #06b6d4, #3b82f6, #8b5cf6, #3b82f6, #06b6d4)',
      backgroundSize: '200% 100%',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      backgroundClip: 'text',
      animation: 'aiGradient 3s ease infinite, aiPulse 2s ease-in-out infinite',
      fontWeight: 600,
    } : {
      color: theme.colors.text.secondary,
      fontWeight: 400,
    }),
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
