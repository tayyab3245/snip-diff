/**
 * FileTree Component for SNIP-DIFF
 * Renders file tree structure with selection capabilities
 */

import React, { useState } from 'react';
import { PanelLayout } from './layout';
import { useApiClient } from '../hooks/use-api-client';
import { useAppStore } from '../store/app-store';
import { useTheme } from '../theme';

interface FileTreeNodeProps {
  node: any;
  depth: number;
  onFileSelect: (path: string) => void;
  isSelected: boolean;
}

// Lucide-style SVG Icons
const FolderIcon: React.FC<{ isOpen?: boolean }> = ({ isOpen }) => (
  <svg 
    width="16" 
    height="16" 
    viewBox="0 0 24 24" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
    stroke={isOpen ? "#dcb67a" : "#8f8f8f"}
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {isOpen ? (
      <>
        <path d="M2 11v8a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-8" />
        <path d="M2 11V9a2 2 0 0 1 2-2h5.293a2 2 0 0 1 1.414.586l1.586 1.586A2 2 0 0 0 13.707 10H20a2 2 0 0 1 2 2v1" />
      </>
    ) : (
      <>
        <path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z" />
      </>
    )}
  </svg>
);

const FileIcon: React.FC<{ ext?: string }> = ({ ext }) => {
  const getFileColor = (extension?: string) => {
    if (!extension) return '#8f8f8f';
    
    const ext = extension.toLowerCase();
    switch (ext) {
      case 'ts':
      case 'tsx':
        return '#3178c6';
      case 'js':
      case 'jsx':
        return '#f7df1e';
      case 'py':
        return '#3776ab';
      case 'json':
        return '#5a5a5a';
      case 'html':
        return '#e34c26';
      case 'css':
      case 'scss':
        return '#264de4';
      case 'md':
        return '#ffffff';
      default:
        return '#8f8f8f';
    }
  };

  return (
    <svg 
      width="16" 
      height="16" 
      viewBox="0 0 24 24" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      stroke={getFileColor(ext)}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>
  );
};

const ChevronIcon: React.FC<{ isOpen: boolean }> = ({ isOpen }) => (
  <svg 
    width="12" 
    height="12" 
    viewBox="0 0 12 12" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
    style={{ transform: isOpen ? 'rotate(90deg)' : 'none', transition: 'transform 0.15s' }}
  >
    <path
      d="M4.5 2L8.5 6L4.5 10"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

const FileTreeNode: React.FC<FileTreeNodeProps> = ({ node, depth, onFileSelect, isSelected }) => {
  const [isExpanded, setIsExpanded] = useState(depth < 2);
  const { activeFilePath, selectedFiles, openFile, closeFile } = useAppStore();
  const { theme } = useTheme();
  const isActive = activeFilePath === node.path;

  const handleClick = async () => {
    if (node.type === 'file') {
      // Check if file is currently selected (before toggle)
      const wasSelected = selectedFiles.has(node.path);
      
      // Toggle selection
      onFileSelect(node.path);
      
      if (!wasSelected) {
        // File is being selected - open it
        try {
          console.log('Opening file:', node.path);
          const response = await window.electronAPI.readFile(node.path);
          
          if (response.success && response.data) {
            openFile({
              path: node.path,
              content: response.data.content,
              language: getFileExtension(node.name)
            });
            console.log('File opened successfully:', node.path);
          } else {
            const errorMsg = response.error || 'Failed to open file';
            console.error('Failed to get file content:', errorMsg);
          }
        } catch (error) {
          console.error('Exception opening file:', error);
        }
      } else {
        // File is being deselected - close it
        closeFile(node.path);
        console.log('File closed:', node.path);
      }
    } else {
      setIsExpanded(!isExpanded);
    }
  };

  const getFileExtension = (name: string) => {
    return name.split('.').pop();
  };

  const nodeStyle: React.CSSProperties = {
    padding: '6px 12px',
    paddingLeft: `${12 + depth * 16}px`,
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    fontSize: '13px',
    color: theme.colors.components.fileTree.text,
    userSelect: 'none',
    background: isSelected ? 'rgba(56, 189, 248, 0.15)' : (isActive ? 'rgba(255, 255, 255, 0.08)' : 'transparent'),
    borderLeft: isSelected ? '3px solid #38bdf8' : '3px solid transparent',
    transition: 'background 0.15s, border-left 0.15s',
  };

  const iconContainerStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    width: '16px',
    height: '16px',
    flexShrink: 0,
  };

  const nameStyle: React.CSSProperties = {
    fontSize: '13px',
    fontWeight: 400,
    flex: 1,
  };

  return (
    <>
      <div 
        style={nodeStyle} 
        onClick={handleClick}
        onMouseEnter={(e) => {
          if (!isSelected) {
            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.04)';
          }
        }}
        onMouseLeave={(e) => {
          if (!isSelected) {
            e.currentTarget.style.background = 'transparent';
          }
        }}
      >
        {node.type === 'directory' && (
          <div style={{ width: '12px', color: theme.colors.text.tertiary }}>
            <ChevronIcon isOpen={isExpanded} />
          </div>
        )}
        {node.type === 'file' && <div style={{ width: '12px' }} />}
        
        <div style={iconContainerStyle}>
          {node.type === 'directory' ? (
            <FolderIcon isOpen={isExpanded} />
          ) : (
            <FileIcon ext={getFileExtension(node.name)} />
          )}
        </div>
        
        <span style={nameStyle}>{node.name}</span>
      </div>
      
      {node.type === 'directory' && isExpanded && node.children && (
        <div>
          {node.children.map((child: any) => (
            <FileTreeNode
              key={child.path}
              node={child}
              depth={depth + 1}
              onFileSelect={onFileSelect}
              isSelected={selectedFiles.has(child.path)}
            />
          ))}
        </div>
      )}
    </>
  );
};

export const FileTree: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { theme } = useTheme();
  
  const { 
    selectedPath, 
    fileTree, 
    setSelectedPath, 
    setFileTree,
    selectedFiles,
    toggleFileSelection,
    clearFileSelection
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

  const loadFileTree = async (_path: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await window.electronAPI.getFileTree(_path);
      
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
    console.log('File clicked:', path);
    toggleFileSelection(path);
  };

  const handleClearSelection = () => {
    clearFileSelection();
  };

  // Button styles (non-layout)
  const selectButtonStyle: React.CSSProperties = {
    width: '100%',
    padding: '10px 16px',
    background: 'transparent',
    border: `1px solid ${theme.colors.border.secondary}`,
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '13px',
    fontWeight: 500,
    color: theme.colors.text.primary,
    textAlign: 'center',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
  };

  const clearButtonStyle: React.CSSProperties = {
    width: '100%',
    padding: '8px 16px',
    background: 'transparent',
    border: `1px solid ${theme.colors.border.secondary}`,
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '12px',
    fontWeight: 500,
    color: theme.colors.text.secondary,
    textAlign: 'center',
  };

  const loadingStyle: React.CSSProperties = {
    padding: '16px',
    textAlign: 'center',
    color: theme.colors.text.secondary,
    fontSize: '13px',
  };

  const errorStyle: React.CSSProperties = {
    padding: '16px',
    textAlign: 'center',
    color: theme.colors.semantic.error,
    fontSize: '13px',
    background: theme.colors.background.tertiary,
    borderRadius: '4px',
    margin: '8px',
  };

  // TOP BAR: Folder selection and clear button
  const topBar = (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      <button 
        style={selectButtonStyle}
        onClick={handleSelectFolder}
      >
        Choose Folder
      </button>
      
      <div style={{ minHeight: '36px' }}>
        {selectedFiles.size > 0 && (
          <button 
            style={clearButtonStyle}
            onClick={handleClearSelection}
          >
            Clear Selection
          </button>
        )}
      </div>
    </div>
  );

  // CONTENT: File tree (edge-to-edge with padding)
  const content = (
    <div style={{ padding: '8px', background: theme.colors.components.fileTree.background }}>
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
          isSelected={selectedFiles.has(node.path)}
        />
      ))}
    </div>
  );

  return (
    <PanelLayout 
      topBar={topBar}
      content={content}
    />
  );
};
