/**
 * FileTree Component for SNIP-DIFF
 * Renders file tree structure with selection capabilities
 */

import React, { useState } from 'react';
import styled from 'styled-components';
import { useApiClient } from '../hooks/useApiClient';
import { useAppStore } from '../store/appStore';

const FileTreeContainer = styled.div`
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #e0e5ec;
`;

const FileTreeHeader = styled.div`
  padding: 16px;
  border-bottom: 1px solid #c5c5c5;
  box-shadow: inset 2px 2px 5px #bebebe, inset -2px -2px 5px #ffffff;
`;

const HeaderTitle = styled.h3`
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
`;

const SelectFolderButton = styled.button`
  padding: 8px 16px;
  background: #e0e5ec;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
  box-shadow: 2px 2px 5px #bebebe, -2px -2px 5px #ffffff;
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 3px 3px 8px #bebebe, -3px -3px 8px #ffffff;
  }

  &:active {
    transform: translateY(0);
    box-shadow: inset 2px 2px 5px #bebebe, inset -2px -2px 5px #ffffff;
  }
`;

const FileTreeContent = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 8px;
`;

const FileNode = styled.div<{ depth: number; selected: boolean }>`
  padding: 4px 8px;
  margin-left: ${props => props.depth * 16}px;
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #333;
  user-select: none;
  background: ${props => props.selected ? '#d0d7de' : 'transparent'};

  &:hover {
    background: #d5dae1;
  }
`;

const FileIcon = styled.span`
  font-size: 16px;
  width: 16px;
  text-align: center;
`;

const FileName = styled.span`
  flex: 1;
  truncate: true;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const LoadingIndicator = styled.div`
  padding: 16px;
  text-align: center;
  color: #666;
  font-style: italic;
`;

const ErrorMessage = styled.div`
  padding: 16px;
  color: #e74c3c;
  font-size: 14px;
  background: #fdf2f2;
  border-radius: 4px;
  margin: 8px;
`;

interface FileTreeNodeProps {
  node: any;
  depth: number;
  onFileSelect: (path: string) => void;
}

const FileTreeNode: React.FC<FileTreeNodeProps> = ({ node, depth, onFileSelect }) => {
  const [isExpanded, setIsExpanded] = useState(depth < 2);
  const { selectedFiles, toggleFileSelection } = useAppStore();
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

  return (
    <>
      <FileNode depth={depth} selected={isSelected} onClick={handleClick}>
        <FileIcon>{getFileIcon(node.type, node.name)}</FileIcon>
        <FileName>{node.name}</FileName>
        {node.type === 'file' && node.size && (
          <span style={{ fontSize: '12px', color: '#666' }}>
            {formatFileSize(node.size)}
          </span>
        )}
      </FileNode>
      
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
    // Could trigger additional actions when files are selected
    console.log('File selected:', path);
  };

  return (
    <FileTreeContainer>
      <FileTreeHeader>
        <HeaderTitle>Project Files</HeaderTitle>
        <SelectFolderButton onClick={handleSelectFolder}>
          📁 Choose Folder
        </SelectFolderButton>
        {selectedFiles.size > 0 && (
          <div style={{ marginTop: '8px', fontSize: '12px', color: '#666' }}>
            {selectedFiles.size} file{selectedFiles.size !== 1 ? 's' : ''} selected
          </div>
        )}
      </FileTreeHeader>

      <FileTreeContent>
        {isLoading && <LoadingIndicator>Loading files...</LoadingIndicator>}
        
        {error && <ErrorMessage>{error}</ErrorMessage>}
        
        {!isLoading && !error && fileTree.length === 0 && selectedPath && (
          <LoadingIndicator>No files found in selected directory</LoadingIndicator>
        )}
        
        {!isLoading && !error && fileTree.length === 0 && !selectedPath && (
          <LoadingIndicator>Select a folder to browse files</LoadingIndicator>
        )}
        
        {fileTree.map((node) => (
          <FileTreeNode
            key={node.path}
            node={node}
            depth={0}
            onFileSelect={handleFileSelect}
          />
        ))}
      </FileTreeContent>
    </FileTreeContainer>
  );
};
