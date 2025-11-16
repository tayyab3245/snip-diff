/**
 * File Service for SNIP-DIFF
 * Handles all file system operations including reading, tree building, and content management
 */

import * as fs from 'fs';
import * as path from 'path';

export interface FileNode {
  path: string;
  name: string;
  type: 'file' | 'directory';
  children?: FileNode[];
}

export interface FileServiceResult<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export class FileService {
  private readonly maxDepth = 10;
  private readonly ignorePatterns = [
    /node_modules/,
    /\.git$/,
    /^\./, // Hidden files
    /dist$/,
    /build$/,
    /\.cache/,
    /coverage$/,
    /\.next$/,
    /\.nuxt$/,
    /\.output$/,
  ];

  /**
   * Build directory tree structure
   */
  public getFileTree(dirPath: string): FileServiceResult<{ nodes: FileNode[] }> {
    try {
      const nodes = this.buildTree(dirPath);
      return { success: true, data: { nodes } };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to read directory'
      };
    }
  }

  /**
   * Read file content
   */
  public readFile(filePath: string): FileServiceResult<{ content: string; filePath: string }> {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      return { 
        success: true, 
        data: { content, filePath } 
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to read file'
      };
    }
  }

  /**
   * Read multiple files at once (useful for batch operations and LLM summarization)
   */
  public readMultipleFiles(filePaths: string[]): FileServiceResult<Array<{ path: string; content: string }>> {
    try {
      const files = filePaths.map(filePath => {
        const content = fs.readFileSync(filePath, 'utf-8');
        return { path: filePath, content };
      });
      return { success: true, data: files };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to read files'
      };
    }
  }

  /**
   * Check if path exists
   */
  public exists(filePath: string): boolean {
    return fs.existsSync(filePath);
  }

  /**
   * Check if path is a directory
   */
  public isDirectory(filePath: string): boolean {
    try {
      return fs.statSync(filePath).isDirectory();
    } catch {
      return false;
    }
  }

  /**
   * Build tree structure recursively
   */
  private buildTree(dirPath: string, depth: number = 0): FileNode[] {
    if (depth >= this.maxDepth) {
      return [];
    }

    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    const nodes: FileNode[] = [];

    for (const entry of entries) {
      // Skip ignored patterns
      if (this.shouldIgnore(entry.name)) {
        continue;
      }

      const fullPath = path.join(dirPath, entry.name);
      
      if (entry.isDirectory()) {
        const children = this.buildTree(fullPath, depth + 1);
        nodes.push({
          path: fullPath,
          name: entry.name,
          type: 'directory',
          children
        });
      } else if (entry.isFile()) {
        nodes.push({
          path: fullPath,
          name: entry.name,
          type: 'file'
        });
      }
    }

    // Sort: directories first, then alphabetically
    return nodes.sort((a, b) => {
      if (a.type !== b.type) {
        return a.type === 'directory' ? -1 : 1;
      }
      return a.name.localeCompare(b.name);
    });
  }

  /**
   * Check if file/directory should be ignored
   */
  private shouldIgnore(name: string): boolean {
    return this.ignorePatterns.some(pattern => pattern.test(name));
  }
}
