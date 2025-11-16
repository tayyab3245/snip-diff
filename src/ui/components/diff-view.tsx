/**
 * DiffView Component for SNIP-DIFF - Themed Version
 * Displays diff results with theme support and Git change indicators
 */

import React from 'react';
import { PanelLayout } from './layout';
import { useAppStore } from '../store/app-store';
import { useTheme } from '../theme';

interface DiffLine {
  type: 'addition' | 'deletion' | 'context' | 'header' | 'file-header' | 'hunk-header';
  content: string;
  lineNumber?: number;
  oldLineNumber?: number;
  newLineNumber?: number;
}

const parseDiff = (diffContent: string): DiffLine[] => {
  const lines = diffContent.split('\n');
  const parsedLines: DiffLine[] = [];
  let oldLineNum = 0;
  let newLineNum = 0;

  for (const line of lines) {
    // Skip "\ No newline at end of file" - it's metadata, not content
    if (line.startsWith('\\ No newline at end of file')) {
      continue;
    }
    
    if (line.startsWith('diff --git')) {
      parsedLines.push({ type: 'file-header', content: line });
    } else if (line.startsWith('+++') || line.startsWith('---')) {
      parsedLines.push({ type: 'header', content: line });
    } else if (line.startsWith('@@')) {
      // Parse hunk header to get line numbers
      const match = line.match(/@@ -(\d+),?\d* \+(\d+),?\d* @@/);
      if (match) {
        oldLineNum = parseInt(match[1], 10);
        newLineNum = parseInt(match[2], 10);
      }
      parsedLines.push({ type: 'hunk-header', content: line });
    } else if (line.startsWith('+')) {
      parsedLines.push({
        type: 'addition',
        content: line.substring(1),
        newLineNumber: newLineNum++,
      });
    } else if (line.startsWith('-')) {
      parsedLines.push({
        type: 'deletion',
        content: line.substring(1),
        oldLineNumber: oldLineNum++,
      });
    } else {
      parsedLines.push({
        type: 'context',
        content: line.startsWith(' ') ? line.substring(1) : line,
        oldLineNumber: oldLineNum++,
        newLineNumber: newLineNum++,
      });
    }
  }

  return parsedLines;
};

export const DiffView: React.FC = () => {
  const { theme } = useTheme();
  const [lastUpdate, setLastUpdate] = React.useState<Date | null>(null);
  const [diffContent, setDiffContent] = React.useState<string | null>(null);

  const { 
    openFiles,
    activeFilePath,
    diffMode,
    gitStatus,
    selectedPath,
    viewMode,
    setActiveFile,
    closeFile,
  } = useAppStore();

  const activeFile = openFiles.find(f => f.path === activeFilePath);

  // Fetch diff content based on view mode (context amount)
  React.useEffect(() => {
    if (!activeFile || !selectedPath || activeFile.language !== 'diff') {
      setDiffContent(null);
      return;
    }

    const fetchDiff = async () => {
      // Determine if we need full context or limited context
      const fullContext = viewMode === 'full';
      
      const diffResult = await window.electronAPI.getGitDiff(
        selectedPath, 
        [activeFile.path], 
        fullContext
      );
      
      if (diffResult.success && diffResult.files && diffResult.files.length > 0) {
        const fileData = diffResult.files[0];
        if (fileData && fileData.diff) {
          setDiffContent(fileData.diff);
          setLastUpdate(new Date());
        }
      }
    };

    fetchDiff();
  }, [activeFile?.path, viewMode, selectedPath, gitStatus]);

  // Update timestamp when active file content changes
  React.useEffect(() => {
    if (activeFile) {
      setLastUpdate(new Date());
    }
  }, [activeFile?.content]);

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
    marginBottom: '4px',
    padding: '20px',
    paddingBottom: '0',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  };

  const statusBadgeStyle = (status?: string): React.CSSProperties => {
    let bgColor = '#4b5563';
    let textColor = '#ffffff';

    switch (status) {
      case 'Modified':
        bgColor = 'rgba(224, 159, 62, 0.2)';
        textColor = '#E09F3E';
        break;
      case 'Added':
      case 'Untracked':
        bgColor = 'rgba(115, 201, 145, 0.2)';
        textColor = '#73C991';
        break;
      case 'Deleted':
        bgColor = 'rgba(244, 135, 113, 0.2)';
        textColor = '#F48771';
        break;
      case 'Renamed':
        bgColor = 'rgba(139, 92, 246, 0.2)';
        textColor = '#a78bfa';
        break;
    }

    return {
      fontSize: '11px',
      fontWeight: 600,
      textTransform: 'uppercase',
      padding: '2px 8px',
      borderRadius: '4px',
      backgroundColor: bgColor,
      color: textColor,
    };
  };

  const timestampStyle: React.CSSProperties = {
    fontSize: '11px',
    color: theme.colors.text.secondary,
    opacity: 0.7,
    padding: '0 20px 12px 20px',
    fontStyle: 'italic',
  };

  const tabBarStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    background: theme.colors.background.secondary,
    borderBottom: `1px solid ${theme.colors.border.primary}`,
    overflowX: 'hidden',
    overflowY: 'visible',
    height: '35px',
    flexShrink: 0,
  };

  const tabStyle = (isActive: boolean): React.CSSProperties => ({
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '8px 12px',
    background: isActive ? theme.colors.background.primary : 'transparent',
    borderRight: `1px solid ${theme.colors.border.secondary}`,
    cursor: 'pointer',
    fontSize: '13px',
    color: isActive ? theme.colors.text.primary : theme.colors.text.secondary,
    whiteSpace: 'nowrap',
    minWidth: '120px',
    maxWidth: '200px',
    position: 'relative',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  });

  const tabLabelStyle: React.CSSProperties = {
    flex: 1,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  };

  const closeTabStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '16px',
    height: '16px',
    borderRadius: '3px',
    fontSize: '14px',
    color: theme.colors.text.secondary,
    background: 'transparent',
    border: 'none',
    cursor: 'pointer',
    padding: 0,
  };

  const getFileName = (path: string) => {
    return path.split(/[/\\]/).pop() || path;
  };

  const handleCloseTab = (e: React.MouseEvent, path: string) => {
    e.stopPropagation();
    closeFile(path);
  };

  const contentStyle: React.CSSProperties = {
    fontFamily: 'Monaco, Menlo, "Courier New", monospace',
    fontSize: '13px',
    lineHeight: '1.6',
    whiteSpace: 'pre-wrap',
    wordBreak: 'break-word',
    color: theme.colors.text.primary,
    padding: '20px',
    overflowX: 'auto',
  };

  const lineNumberStyle: React.CSSProperties = {
    display: 'inline-block',
    width: '50px',
    textAlign: 'right',
    paddingRight: '12px',
    color: theme.colors.text.secondary,
    opacity: 0.5,
    userSelect: 'none',
    fontSize: '12px',
  };

  const sideBySideContainerStyle: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '1px',
    backgroundColor: theme.colors.components.diffViewer.border,
    fontFamily: 'Monaco, Menlo, "Courier New", monospace',
    fontSize: '13px',
    lineHeight: '1.6',
  };

  const sideBySidePaneStyle: React.CSSProperties = {
    backgroundColor: theme.colors.background.primary,
    padding: '20px',
    overflowX: 'auto',
  };

  const sideBySideHeaderStyle: React.CSSProperties = {
    fontSize: '12px',
    fontWeight: 600,
    color: theme.colors.text.secondary,
    marginBottom: '12px',
    paddingBottom: '8px',
    borderBottom: `1px solid ${theme.colors.components.diffViewer.border}`,
  };

  const diffLineStyle = (lineType: DiffLine['type']): React.CSSProperties => {
    const baseStyle: React.CSSProperties = {
      display: 'block',
      padding: '0 8px',
      margin: 0,
    };

    switch (lineType) {
      case 'header':
        return {
          ...baseStyle,
          background: 'rgba(56, 139, 253, 0.1)',
          color: '#388bfd',
          fontWeight: 600,
        };
      case 'addition':
        return {
          ...baseStyle,
          background: 'rgba(46, 160, 67, 0.2)',
          color: '#3fb950',
          borderLeft: '3px solid #3fb950',
        };
      case 'deletion':
        return {
          ...baseStyle,
          background: 'rgba(248, 81, 73, 0.2)',
          color: '#ff7b72',
          borderLeft: '3px solid #ff7b72',
        };
      case 'hunk-header':
        return {
          ...baseStyle,
          background: 'rgba(56, 139, 253, 0.15)',
          color: '#58a6ff',
          fontWeight: 600,
        };
      case 'file-header':
        return {
          ...baseStyle,
          background: 'rgba(110, 118, 129, 0.1)',
          color: theme.colors.text.secondary,
          fontWeight: 600,
          marginTop: '16px',
        };
      case 'context':
      default:
        return {
          ...baseStyle,
          color: theme.colors.text.primary,
        };
    }
  };

  const renderUnifiedDiff = (diffLines: DiffLine[]) => (
    <div style={contentStyle}>
      {diffLines.map((line, index) => (
        <div key={index} style={diffLineStyle(line.type)}>
          {(line.type === 'addition' || line.type === 'deletion' || line.type === 'context') && (
            <>
              <span style={lineNumberStyle}>
                {line.oldLineNumber || ' '}
              </span>
              <span style={lineNumberStyle}>
                {line.newLineNumber || ' '}
              </span>
            </>
          )}
          {line.type === 'addition' && <span style={{ color: '#3fb950', marginRight: '8px' }}>+</span>}
          {line.type === 'deletion' && <span style={{ color: '#ff7b72', marginRight: '8px' }}>-</span>}
          {line.type === 'context' && <span style={{ marginRight: '8px', opacity: 0.5 }}> </span>}
          <span>{line.content || ' '}</span>
        </div>
      ))}
    </div>
  );

  const renderSideBySideDiff = (diffLines: DiffLine[]) => {
    const leftLines: DiffLine[] = [];
    const rightLines: DiffLine[] = [];

    // Separate additions and deletions for side-by-side view
    diffLines.forEach((line) => {
      if (line.type === 'deletion' || line.type === 'context') {
        leftLines.push(line);
      }
      if (line.type === 'addition' || line.type === 'context') {
        rightLines.push(line);
      }
      // Skip headers in side-by-side view (or show in both)
      if (line.type === 'header' || line.type === 'file-header' || line.type === 'hunk-header') {
        leftLines.push(line);
        rightLines.push(line);
      }
    });

    return (
      <div style={sideBySideContainerStyle}>
        <div style={sideBySidePaneStyle}>
          <div style={sideBySideHeaderStyle}>Original</div>
          {leftLines.map((line, index) => (
            <div key={`left-${index}`} style={diffLineStyle(line.type)}>
              {(line.type === 'deletion' || line.type === 'context') && (
                <span style={lineNumberStyle}>{line.oldLineNumber || ' '}</span>
              )}
              <span>{line.content || ' '}</span>
            </div>
          ))}
        </div>
        <div style={sideBySidePaneStyle}>
          <div style={sideBySideHeaderStyle}>Modified</div>
          {rightLines.map((line, index) => (
            <div key={`right-${index}`} style={diffLineStyle(line.type)}>
              {(line.type === 'addition' || line.type === 'context') && (
                <span style={lineNumberStyle}>{line.newLineNumber || ' '}</span>
              )}
              <span>{line.content || ' '}</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // CONTENT: Open file content
  const content = (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
      {openFiles.length > 0 && (
        <div style={tabBarStyle}>
          {openFiles.map((file) => (
            <div
              key={file.path}
              style={tabStyle(file.path === activeFilePath)}
              onClick={() => setActiveFile(file.path)}
            >
              <span style={tabLabelStyle} title={file.path}>
                {getFileName(file.path)}
              </span>
              {file.gitStatus && (
                <span style={{ fontSize: '10px', opacity: 0.7 }}>
                  {file.gitStatus === 'Modified' && 'M'}
                  {file.gitStatus === 'Added' && 'A'}
                  {file.gitStatus === 'Deleted' && 'D'}
                  {file.gitStatus === 'Untracked' && 'U'}
                </span>
              )}
              <button
                style={closeTabStyle}
                onClick={(e) => handleCloseTab(e, file.path)}
                onMouseEnter={(e) => e.currentTarget.style.background = theme.colors.background.tertiary}
                onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                title="Close"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}

      <div style={{ flex: 1, overflow: 'auto' }}>
        {!activeFile && (
          <div style={emptyStateStyle}>
            Click on a file to open it in the editor
          </div>
        )}

        {activeFile && (
          <div>
            <div style={filePathStyle}>
              <span>{activeFile.path}</span>
              {activeFile.gitStatus && (
                <span style={statusBadgeStyle(activeFile.gitStatus)}>
                  {activeFile.gitStatus}
                </span>
              )}
            </div>
            
            {lastUpdate && (
              <div style={timestampStyle}>
                Last updated: {lastUpdate.toLocaleTimeString()}
              </div>
            )}
            
            {activeFile.language === 'diff' ? (
              // Render Git diff - viewMode controls context, diffMode controls format
              diffMode === 'side-by-side'
                ? renderSideBySideDiff(parseDiff(diffContent || activeFile.content))
                : renderUnifiedDiff(parseDiff(diffContent || activeFile.content))
            ) : (
              // Render regular file content
              <div style={contentStyle}>
                {activeFile.content.split('\n').map((line: string, lineIndex: number) => (
                  <div key={lineIndex}>
                    <span style={lineNumberStyle}>{lineIndex + 1}</span>
                    <span>{line || ' '}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );

  return (
    <PanelLayout 
      content={content}
    />
  );
};
