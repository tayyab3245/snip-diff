/**
 * FileTree Component for SNIP-DIFF
 * Renders file tree structure with selection capabilities
 */

import React, { useState } from 'react';
import { useApiClient } from '../hooks/useApiClient';
import { useAppStore } from '../store/appStore';
import { useTheme } from '../theme';

interface FileTreeNodeProps {
  node: any;
  depth: number;
  onFileSelect: (path: string) => void;
}

const FileTreeNode: React.FC<FileTreeNodeProps> = ({ node, depth, onFileSelect }) => {
  const [isExpanded, setIsExpanded] = useState(depth < 2);
  const { selectedFiles, toggleFileSelection } = useAppStore();
  const { theme } = useTheme();
  const isSelected = selectedFiles.has(node.path);

  const handleClick = () => {
    if (node.type === 'file') {
      toggleFileSelection(node.path);
    } else {
      setIsExpanded(!isExpanded);
    }
    onFileSelect(node.path);
  };

  const getFileIcon = (type: string, name: string) => {
    if (type === 'directory') {
      return isExpanded ? '📁' : '📂';
    }
    
    const ext = name.split('.').pop()?.toLowerCase();
    switch (ext) {
      case 'js':
      case 'ts':
      case 'jsx':
      case 'tsx':
        return '📜';
      case 'py':
        return '🐍';
      case 'html':
        return '🌐';
      case 'css':
        return '🎨';
      case 'json':
        return '📋';
      case 'md':
        return '📝';
      default:
        return '📄';
    }
  };

  const nodeStyle: React.CSSProperties = {
    padding: '4px 8px',
    marginLeft: `${depth * 16}px`,
    cursor: 'pointer',
    borderRadius: '4px',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    fontSize: '14px',
    color: theme.colors.components.fileTree.text,
    userSelect: 'none',
    background: isSelected ? theme.colors.components.fileTree.selected : 'transparent',
    transition: 'background-color 0.2s ease',
  };

  const iconStyle: React.CSSProperties = {
    fontSize: '16px',
    width: '16px',
    textAlign: 'center',
  };

  const nameStyle: React.CSSProperties = {
    fontSize: '14px',
    fontWeight: node.type === 'directory' ? 500 : 400,
  };

  return (
    <>
      <div 
        style={nodeStyle} 
        onClick={handleClick}
        onMouseEnter={(e) => {
          if (!isSelected) {
            e.currentTarget.style.background = theme.colors.components.fileTree.hover;
          }
        }}
        onMouseLeave={(e) => {
          if (!isSelected) {
            e.currentTarget.style.background = 'transparent';
          }
        }}
      >
        <span style={iconStyle}>{getFileIcon(node.type, node.name)}</span>
        <span style={nameStyle}>{node.name}</span>
        {node.type === 'file' && node.size && (
          <span style={{ fontSize: '12px', color: theme.colors.text.tertiary, marginLeft: 'auto' }}>
            {formatFileSize(node.size)}
          </span>
        )}
      </div>
      
      {node.type === 'directory' && isExpanded && node.children && (
        <div>
          {node.children.map((child: any) => (
            <FileTreeNode
              key={child.path}
              node={child}
              depth={depth + 1}
              onFileSelect={onFileSelect}
            />
          ))}
        </div>
      )}
    </>
  );
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
};

export const FileTree: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { theme } = useTheme();
  
  const { getFileTree } = useApiClient();
  const { 
    selectedPath, 
    fileTree, 
    setSelectedPath, 
    setFileTree,
    selectedFiles 
  } = useAppStore();

  const handleSelectFolder = async () => {
    try {
      const folderPath = await window.electronAPI.selectFolder();
      if (folderPath) {
        setSelectedPath(folderPath);
        await loadFileTree(folderPath);
      }
    } catch (error) {
      console.error('Failed to select folder:', error);
      setError('Failed to select folder');
    }
  };

  const loadFileTree = async (path: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await getFileTree(path);
      
      if (response.success && response.data) {
        setFileTree(response.data.nodes || []);
      } else {
        setError(response.error || 'Failed to load file tree');
      }
    } catch (error) {
      console.error('Error loading file tree:', error);
      setError('Error loading file tree');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileSelect = (path: string) => {
    console.log('File selected:', path);
  };

  const containerStyle: React.CSSProperties = {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    background: theme.colors.components.fileTree.background,
  };

  const headerStyle: React.CSSProperties = {
    padding: '16px',
    borderBottom: `1px solid ${theme.colors.border.secondary}`,
    boxShadow: theme.colors.shadows.neumorphic.pressed,
  };

  const titleStyle: React.CSSProperties = {
    margin: '0 0 12px 0',
    fontSize: '16px',
    fontWeight: 600,
    color: theme.colors.text.primary,
  };

  const selectButtonStyle: React.CSSProperties = {
    padding: '8px 16px',
    background: theme.colors.components.toolbar.button,
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    color: theme.colors.text.primary,
    boxShadow: theme.colors.shadows.neumorphic.raised,
    transition: 'all 0.2s ease',
  };

  const contentStyle: React.CSSProperties = {
    flex: 1,
    overflowY: 'auto',
    padding: '8px',
  };

  const loadingStyle: React.CSSProperties = {
    padding: '16px',
    textAlign: 'center',
    color: theme.colors.text.secondary,
    fontSize: '14px',
  };

  const errorStyle: React.CSSProperties = {
    padding: '16px',
    textAlign: 'center',
    color: theme.colors.semantic.error,
    fontSize: '14px',
    background: theme.colors.background.tertiary,
    borderRadius: '4px',
    margin: '8px',
  };

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <h3 style={titleStyle}>Project Files</h3>
        <button 
          style={selectButtonStyle}
          onClick={handleSelectFolder}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-1px)';
            e.currentTarget.style.boxShadow = theme.colors.shadows.neumorphic.float;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = theme.colors.shadows.neumorphic.raised;
          }}
        >
          📁 Choose Folder
        </button>
        {selectedFiles.size > 0 && (
          <div style={{ marginTop: '8px', fontSize: '12px', color: theme.colors.text.tertiary }}>
            {selectedFiles.size} file{selectedFiles.size !== 1 ? 's' : ''} selected
          </div>
        )}
      </div>

      <div style={contentStyle}>
        {isLoading && <div style={loadingStyle}>Loading files...</div>}
        
        {error && <div style={errorStyle}>{error}</div>}
        
        {!isLoading && !error && fileTree.length === 0 && selectedPath && (
          <div style={loadingStyle}>No files found in selected directory</div>
        )}
        
        {!isLoading && !error && fileTree.length === 0 && !selectedPath && (
          <div style={loadingStyle}>Select a folder to browse files</div>
        )}
        
        {fileTree.map((node) => (
          <FileTreeNode
            key={node.path}
            node={node}
            depth={0}
            onFileSelect={handleFileSelect}
          />
        ))}
      </div>
    </div>
  );
};
