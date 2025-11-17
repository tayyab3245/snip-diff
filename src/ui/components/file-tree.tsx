/*
 * Copyright 2025 Tayyab
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * FileTree Component for SNIP-DIFF
 * Renders file tree structure with selection capabilities
 */

import React, { useState, useEffect } from 'react';
import { PanelLayout } from './layout';
import { useAppStore } from '../store/app-store';
import { useTheme } from '../theme';
import { useFileManager } from '../hooks/use-file-manager';
import { normalizePathForCompare, getRelativePath } from '../../shared/path-utils';

interface FileTreeNodeProps {
  node: any;
  depth: number;
  onFileSelect: (path: string) => void;
  isSelected: boolean;
}

// Lucide-style SVG Icons
const FolderIcon: React.FC<{ isOpen: boolean; color?: string }> = ({ isOpen, color = '#ffffff' }) => (
  <svg 
    width="16" 
    height="16" 
    viewBox="0 0 24 24" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
    stroke={color}
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

const FileIcon: React.FC<{ ext?: string; color?: string }> = ({ ext, color }) => {
  const defaultColor = color || '#ffffff';

  return (
    <svg 
      width="16" 
      height="16" 
      viewBox="0 0 24 24" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      stroke={defaultColor}
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
  const { activeFilePath, selectedFiles, gitStatus } = useAppStore();
  const { toggleFile } = useFileManager();
  const { theme } = useTheme();
  const isActive = activeFilePath === node.path;
  const fileStatus = gitStatus.get(node.path);
  const isModified = fileStatus && fileStatus !== 'Unchanged';

  // Get status color for text (desaturated to match diff view)
  const getStatusColor = () => {
    if (!fileStatus || fileStatus === 'Unchanged') return null;
    
    switch (fileStatus) {
      case 'Untracked':
        return '#5a9d6a'; // Desaturated green for untracked
      case 'Modified':
        return '#c08a3a'; // Desaturated orange for modified
      case 'Added':
        return '#5a9d6a'; // Desaturated green for added
      case 'Deleted':
        return '#d87070'; // Desaturated red for deleted
      case 'Renamed':
        return '#5a9d6a'; // Desaturated green for renamed
      case 'Copied':
        return '#5a9d6a'; // Desaturated green for copied
      case 'Ignored':
        return null; // No color for ignored
      default:
        return '#c08a3a'; // Desaturated orange for other changes
    }
  };

  const statusColor = getStatusColor();

  // Get icon color: use status color if available, gray for ignored, white otherwise
  const getIconColor = () => {
    if (statusColor) {
      return statusColor; // Use Git status color (green/orange/red)
    }
    if (fileStatus === 'Ignored') {
      return '#6b7280'; // Gray for ignored files
    }
    return '#ffffff'; // White for all other files
  };

  const iconColor = getIconColor();

  const handleClick = async () => {
    if (node.type === 'file') {
      // Check if file is currently selected (before toggle)
      const wasSelected = selectedFiles.has(node.path);
      
      // Toggle selection and open/close file
      onFileSelect(node.path);
      await toggleFile(node.path, wasSelected);
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
    color: statusColor || (fileStatus === 'Ignored' ? '#6b7280' : theme.colors.components.fileTree.text),
    userSelect: 'none',
    background: isSelected ? 'rgba(56, 189, 248, 0.15)' : (isActive ? 'rgba(255, 255, 255, 0.08)' : 'transparent'),
    transition: 'background 0.15s, color 0.15s',
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
            <FolderIcon isOpen={isExpanded} color={iconColor} />
          ) : (
            <FileIcon ext={getFileExtension(node.name)} color={iconColor} />
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
  const fileManager = useFileManager();
  
  const { 
    selectedPath, 
    fileTree, 
    selectedFiles,
    toggleFileSelection,
    setGitStatus,
    modifiedFiles
  } = useAppStore();

  // Poll Git status every 2 seconds to detect changes
  useEffect(() => {
    if (!selectedPath) return;

    const pollGitStatus = async () => {
      try {
        const isRepo = await window.electronAPI.isGitRepo(selectedPath);
        if (!isRepo.isRepo) return;

        // Get Git status for all files in the repository
        const statusResult = await window.electronAPI.getGitStatus(selectedPath);
        if (!statusResult.success || !statusResult.statuses) return;

        const statusMap = new Map<string, string>();
        
        // Get all files from the tree
        const getAllFiles = (nodes: any[]): string[] => {
          const files: string[] = [];
          nodes.forEach(node => {
            if (node.type === 'file') {
              files.push(node.path);
            } else if (node.type === 'directory' && node.children) {
              files.push(...getAllFiles(node.children));
            }
          });
          return files;
        };

        const allFiles = getAllFiles(fileTree);
        
        // Get all folders from the tree
        const getAllFolders = (nodes: any[]): string[] => {
          const folders: string[] = [];
          nodes.forEach(node => {
            if (node.type === 'directory') {
              folders.push(node.path);
              if (node.children) {
                folders.push(...getAllFolders(node.children));
              }
            }
          });
          return folders;
        };

        const allFolders = getAllFolders(fileTree);
        
        // Map Git status to file paths in tree
        statusResult.statuses.forEach((fileStatus: { path: string; status: string }) => {
          const normalizedGitPath = normalizePathForCompare(fileStatus.path);
          
          // Handle folder status (Git returns folders with trailing /)
          if (normalizedGitPath.endsWith('/')) {
            // This is a folder - mark the folder itself and all files inside it
            const folderPath = normalizedGitPath.slice(0, -1);
            
            // Mark the folder node itself
            allFolders.forEach(treePath => {
              const normalizedTreePath = normalizePathForCompare(treePath);
              const relativeToRepo = normalizedTreePath.replace(normalizePathForCompare(selectedPath) + '/', '');
              
              if (relativeToRepo === folderPath || relativeToRepo.startsWith(folderPath + '/')) {
                statusMap.set(treePath, fileStatus.status);
              }
            });
            
            // Mark all files inside it
            allFiles.forEach(treePath => {
              const normalizedTreePath = normalizePathForCompare(treePath);
              const relativeToRepo = normalizedTreePath.replace(normalizePathForCompare(selectedPath) + '/', '');
              
              if (relativeToRepo.startsWith(folderPath + '/')) {
                statusMap.set(treePath, fileStatus.status);
              }
            });
          } else {
            // This is a file - find matching file in tree
            allFiles.forEach(treePath => {
              const normalizedTreePath = normalizePathForCompare(treePath);
              const fullGitPath = normalizePathForCompare(selectedPath + '/' + fileStatus.path);
              
              if (normalizedTreePath === fullGitPath || normalizedTreePath.endsWith('/' + normalizedGitPath)) {
                statusMap.set(treePath, fileStatus.status);
                
                // Mark all parent folders to indicate they contain changed files
                allFolders.forEach(folderPath => {
                  const normalizedFolderPath = normalizePathForCompare(folderPath);
                  if (normalizedTreePath.startsWith(normalizedFolderPath + '/') || 
                      normalizedTreePath.startsWith(normalizedFolderPath + '\\')) {
                    // Only set if folder doesn't already have a status (preserve specific folder status)
                    if (!statusMap.has(folderPath)) {
                      statusMap.set(folderPath, fileStatus.status);
                    }
                  }
                });
              }
            });
          }
        });
        
        setGitStatus(statusMap);
      } catch (error) {
        console.error('[FileTree] Error polling Git status:', error);
      }
    };

    // Initial poll
    pollGitStatus();

    // Poll every 2 seconds
    const interval = setInterval(pollGitStatus, 2000);

    return () => clearInterval(interval);
  }, [selectedPath, fileTree, setGitStatus]);

  // Auto-load file tree when path changes
  useEffect(() => {
    if (selectedPath) {
      setIsLoading(true);
      setError(null);
      
      fileManager.loadFileTree(selectedPath).then(result => {
        if (!result.success) {
          setError(result.error || 'Failed to load file tree');
        }
        setIsLoading(false);
      });
    }
  }, [selectedPath]);

  const handleFileSelect = (path: string) => {
    toggleFileSelection(path);
  };

  const loadingStyle: React.CSSProperties = {
    padding: '16px',
    textAlign: 'center',
    color: theme.colors.text.secondary,
    fontSize: '15px',
  };

  const errorStyle: React.CSSProperties = {
    padding: '16px',
    textAlign: 'center',
    color: theme.colors.semantic.error,
    fontSize: '15px',
    background: theme.colors.background.tertiary,
    borderRadius: '4px',
    margin: '8px',
  };

  const handleOpenFolder = async () => {
    await fileManager.selectFolder();
  };

  const chooseFolderButtonStyle: React.CSSProperties = {
    width: '100%',
    padding: '10px 16px',
    margin: '8px 0',
    backgroundColor: theme.colors.background.secondary,
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 500,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif',
    color: theme.colors.text.primary,
    transition: 'background 0.15s',
    textAlign: 'center',
  };

  // CONTENT: File tree (edge-to-edge with padding)
  const content = (
    <div style={{ padding: '8px', background: theme.colors.components.fileTree.background }}>
      <button
        style={chooseFolderButtonStyle}
        onClick={handleOpenFolder}
        onMouseEnter={(e) => e.currentTarget.style.background = theme.colors.background.tertiary}
        onMouseLeave={(e) => e.currentTarget.style.background = theme.colors.background.secondary}
      >
        Choose Folder
      </button>
      
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
      content={content}
    />
  );
};
