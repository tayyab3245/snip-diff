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
 * Git Service for SNIP-DIFF
 * Handles all Git operations directly in main process
 */

import { execFile } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import * as fs from 'fs';
import { normalizePathForCompare, getRelativePath } from '../../shared/path-utils';

const execFileAsync = promisify(execFile);

export interface GitDiffResult {
  success: boolean;
  files: GitFileChange[];
  error?: string;
}

export interface GitFileChange {
  path: string;
  status: 'Modified' | 'Added' | 'Deleted' | 'Untracked';
  diff: string;
}

export interface GitFileStatus {
  path: string;
  status: 'Modified' | 'Added' | 'Deleted' | 'Untracked' | 'Unchanged';
}

export class GitService {
  private watchedRepo: string | null = null;
  private fileStatuses: Map<string, GitFileStatus> = new Map();
  private async execGit(args: string[], cwd: string): Promise<{ stdout: string; stderr: string }> {
    try {
      return await execFileAsync('git', args, { cwd, maxBuffer: 10 * 1024 * 1024 });
    } catch (error: any) {
      if (error.stdout || error.stderr) {
        return { stdout: error.stdout || '', stderr: error.stderr || '' };
      }
      throw error;
    }
  }

  async isGitRepo(directory: string): Promise<boolean> {
    try {
      await this.execGit(['rev-parse', '--git-dir'], directory);
      return true;
    } catch {
      return false;
    }
  }

  async getStatus(directory: string): Promise<{ path: string; status: string }[]> {
    try {
      const { stdout } = await this.execGit(['status', '--porcelain', '--ignored'], directory);
      
      return stdout
        .split('\n')
        .filter(line => line.trim())
        .map(line => {
          const statusCode = line.substring(0, 2);
          const filePath = line.substring(3);
          
          // Git status format: XY where X=index, Y=working tree
          // https://git-scm.com/docs/git-status#_short_format
          const statusMap: Record<string, string> = {
            // Modified
            'M ': 'Modified',      // Modified in index
            ' M': 'Modified',      // Modified in working tree
            'MM': 'Modified',      // Modified in both
            
            // Added
            'A ': 'Added',         // Added to index
            'AM': 'Added',         // Added to index, modified in working tree
            
            // Deleted
            'D ': 'Deleted',       // Deleted from index
            ' D': 'Deleted',       // Deleted from working tree
            'AD': 'Deleted',       // Added to index, deleted in working tree
            
            // Renamed
            'R ': 'Renamed',
            
            // Copied
            'C ': 'Copied',
            
            // Untracked
            '??': 'Untracked',     // Untracked files
            
            // Ignored (if shown)
            '!!': 'Ignored',
          };
          
          return {
            path: filePath,
            status: statusMap[statusCode] || 'Changed'
          };
        });
    } catch (error) {
      return [];
    }
  }

  async getDiff(directory: string, filePaths?: string[], fullContext?: boolean): Promise<GitDiffResult> {
    try {
      const isRepo = await this.isGitRepo(directory);
      if (!isRepo) {
        return {
          success: false,
          files: [],
          error: 'Not a Git repository'
        };
      }

      const status = await this.getStatus(directory);
      let relevantFiles = status;

      // Filter to specified files if provided
      if (filePaths && filePaths.length > 0) {
        const fileSet = new Set(filePaths.map(fp => getRelativePath(directory, fp)));
        relevantFiles = status.filter(f => fileSet.has(normalizePathForCompare(f.path)));
      }

      const files: GitFileChange[] = [];

      for (const file of relevantFiles) {
        let diff = '';

        if (file.status === 'Untracked') {
          // For untracked files, show entire content as additions in unified diff format
          const fullPath = path.join(directory, file.path);
          try {
            const content = await fs.promises.readFile(fullPath, 'utf-8');
            const lines = content.split('\n');
            
            // Create a proper unified diff header
            diff = `diff --git a/${file.path} b/${file.path}\n`;
            diff += `new file mode 100644\n`;
            diff += `--- /dev/null\n`;
            diff += `+++ b/${file.path}\n`;
            diff += `@@ -0,0 +1,${lines.length} @@\n`;
            diff += lines.map(line => `+${line}`).join('\n');
          } catch (error) {
            continue;
          }
        } else {
          // Get diff from Git with unified format
          try {
            const contextLines = fullContext ? '999999' : '3';
            const { stdout } = await this.execGit(
              ['diff', `--unified=${contextLines}`, 'HEAD', '--', file.path],
              directory
            );
            diff = stdout;

            // If no diff with HEAD, try cached (staged)
            if (!diff) {
              const { stdout: cachedDiff } = await this.execGit(
                ['diff', `--unified=${contextLines}`, '--cached', '--', file.path],
                directory
              );
              diff = cachedDiff;
            }
          } catch (error) {
            continue;
          }
        }

        if (diff) {
          files.push({
            path: file.path,
            status: file.status as any,
            diff
          });
        }
      }

      return {
        success: true,
        files
      };
    } catch (error: any) {
      return {
        success: false,
        files: [],
        error: error.message || 'Unknown error'
      };
    }
  }

  async getFileContent(directory: string, filePath: string, ref: string = 'HEAD'): Promise<string | null> {
    try {
      const relativePath = path.relative(directory, filePath);
      const { stdout } = await this.execGit(['show', `${ref}:${relativePath}`], directory);
      return stdout;
    } catch (error) {
      // File might not exist in Git, read from filesystem
      try {
        return await fs.promises.readFile(filePath, 'utf-8');
      } catch {
        return null;
      }
    }
  }

  /**
   * Initialize tracking for a repository
   * Scans the repo and builds initial file status map
   */
  async initTracking(directory: string): Promise<{ success: boolean; error?: string }> {
    try {
      const isRepo = await this.isGitRepo(directory);
      if (!isRepo) {
        return { success: false, error: 'Not a Git repository' };
      }

      this.watchedRepo = directory;
      await this.refreshFileStatuses();
      
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.message || 'Failed to initialize tracking' };
    }
  }

  /**
   * Refresh file statuses from Git
   */
  async refreshFileStatuses(): Promise<void> {
    if (!this.watchedRepo) return;

    const statuses = await this.getStatus(this.watchedRepo);
    this.fileStatuses.clear();

    for (const status of statuses) {
      this.fileStatuses.set(status.path, {
        path: status.path,
        status: status.status as any
      });
    }
  }

  /**
   * Get status for specific files
   */
  getFileStatuses(filePaths: string[]): Map<string, GitFileStatus> {
    const result = new Map<string, GitFileStatus>();
    
    for (const filePath of filePaths) {
      const relativePath = this.watchedRepo 
        ? path.relative(this.watchedRepo, filePath)
        : filePath;
      
      const status = this.fileStatuses.get(relativePath);
      if (status) {
        result.set(filePath, status);
      } else {
        result.set(filePath, { path: filePath, status: 'Unchanged' });
      }
    }
    
    return result;
  }

  /**
   * Mark a file as modified (called when file watcher detects change)
   */
  async markFileChanged(filePath: string): Promise<GitFileStatus> {
    if (!this.watchedRepo) {
      return { path: filePath, status: 'Modified' };
    }

    const relativePath = path.relative(this.watchedRepo, filePath);
    
    // Refresh status for this specific file
    const statuses = await this.getStatus(this.watchedRepo);
    const fileStatus = statuses.find(s => s.path === relativePath);
    
    const status: GitFileStatus = {
      path: relativePath,
      status: fileStatus ? (fileStatus.status as any) : 'Modified'
    };
    
    this.fileStatuses.set(relativePath, status);
    return status;
  }

  /**
   * Generate unified diff for specific files
   */
  async generateUnifiedDiff(directory: string, filePaths: string[]): Promise<GitDiffResult> {
    return await this.getDiff(directory, filePaths);
  }

  /**
   * Stop tracking
   */
  stopTracking(): void {
    this.watchedRepo = null;
    this.fileStatuses.clear();
  }
}

export const gitService = new GitService();

