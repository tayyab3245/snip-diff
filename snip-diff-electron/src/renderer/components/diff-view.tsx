/**
 * DiffView Component for SNIP-DIFF - Themed Version
 * Displays diff results with theme support
 */

import React from 'react';
import { PanelLayout } from './layout';
import { useAppStore } from '../store/app-store';
import { useTheme } from '../theme';

export const DiffView: React.FC = () => {
  const { theme } = useTheme();

  const { 
    openFiles,
    activeFilePath,
  } = useAppStore();

  const activeFile = openFiles.find(f => f.path === activeFilePath);

  const emptyStateStyle: React.CSSProperties = {
    textAlign: 'center',
    color: theme.colors.text.secondary,
    fontSize: '14px',
    padding: '60px 40px',
  };

  const filePathStyle: React.CSSProperties = {
    fontSize: '13px',
    fontWeight: 500,
    color: theme.colors.text.secondary,
    marginBottom: '12px',
    padding: '20px',
    paddingBottom: '0',
  };

  const contentStyle: React.CSSProperties = {
    fontFamily: 'Monaco, Menlo, "Courier New", monospace',
    fontSize: '13px',
    lineHeight: '1.6',
    whiteSpace: 'pre-wrap',
    wordBreak: 'break-word',
    color: theme.colors.text.primary,
    padding: '20px',
  };

  const diffLineStyle = (line: string): React.CSSProperties => {
    if (line.startsWith('+')) {
      return {
        background: 'rgba(46, 160, 67, 0.15)',
        color: '#2ea043',
        display: 'block',
      };
    }
    if (line.startsWith('-')) {
      return {
        background: 'rgba(248, 81, 73, 0.15)',
        color: '#f85149',
        display: 'block',
      };
    }
    if (line.startsWith('@@')) {
      return {
        background: 'rgba(56, 139, 253, 0.15)',
        color: '#388bfd',
        fontWeight: 600,
        display: 'block',
      };
    }
    return { display: 'block' };
  };

  // CONTENT: Open file content
  const content = (
    <>
      {!activeFile && (
        <div style={emptyStateStyle}>
          Click on a file to open it in the editor
        </div>
      )}

      {activeFile && (
        <div>
          <div style={filePathStyle}>
            {activeFile.path}
          </div>
          
          <div style={contentStyle}>
            {activeFile.content.split('\n').map((line: string, lineIndex: number) => (
              <div key={lineIndex} style={diffLineStyle(line)}>
                {line || ' '}
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );

  return (
    <PanelLayout 
      content={content}
    />
  );
};
