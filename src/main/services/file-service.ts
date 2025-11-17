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
    /^\./,
    /dist$/,
    /build$/,
    /\.cache/,
    /coverage$/,
    /\.next$/,
    /\.nuxt$/,
    /\.output$/,
  ];

  // Binary and non-text file extensions to exclude from LLM analysis
  private readonly binaryExtensions = new Set([
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.tar', '.gz', '.rar', '.7z',
    '.exe', '.dll', '.so', '.dylib', '.bin',
    '.mp3', '.mp4', '.avi', '.mov', '.wmv',
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    '.db', '.sqlite', '.mdb',
  ]);

  // Additional patterns for gitignored/non-analyzable files
  private readonly llmIgnorePatterns = [
    /node_modules/,
    /\.git/,
    /package-lock\.json$/,
    /yarn\.lock$/,
    /pnpm-lock\.yaml$/,
    /\.min\.(js|css)$/,
    /dist/,
    /build/,
    /coverage/,
    /\.next/,
    /\.nuxt/,
    /\.output/,
    /\.cache/,
    /\.vscode/,
    /\.idea/,
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

  /**
   * Check if file contains binary content by reading a sample
   */
  private isBinaryFile(filePath: string): boolean {
    try {
      const buffer = Buffer.alloc(8192);
      const fd = fs.openSync(filePath, 'r');
      const bytesRead = fs.readSync(fd, buffer, 0, 8192, 0);
      fs.closeSync(fd);

      if (bytesRead === 0) {
        return false;
      }

      // Check for null bytes (strong indicator of binary)
      for (let i = 0; i < bytesRead; i++) {
        if (buffer[i] === 0) {
          return true;
        }
      }

      return false;
    } catch {
      // If we can't read it, assume it's safe to exclude
      return true;
    }
  }

  /**
   * Check if file should be excluded from LLM analysis
   * (binary files, lock files, minified files, etc.)
   */
  public shouldExcludeFromLLM(filePath: string): boolean {
    const ext = path.extname(filePath).toLowerCase();
    
    // Check known binary extensions first (fast path)
    if (this.binaryExtensions.has(ext)) {
      return true;
    }

    // Check gitignore/non-analyzable patterns
    if (this.llmIgnorePatterns.some(pattern => pattern.test(filePath))) {
      return true;
    }

    // For remaining files, check if they contain binary content
    // This catches files without extensions or misidentified files
    if (this.isBinaryFile(filePath)) {
      return true;
    }

    return false;
  }

  /**
   * Filter file paths to exclude binary and gitignored files
   */
  public filterFilesForLLM(filePaths: string[]): string[] {
    return filePaths.filter(filePath => !this.shouldExcludeFromLLM(filePath));
  }
}
