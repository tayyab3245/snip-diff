/**
 * Git Service for SNIP-DIFF
 * Handles all Git operations directly in main process
 */

import { execFile } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import * as fs from 'fs';

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

export class GitService {
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
      const { stdout } = await this.execGit(['status', '--porcelain'], directory);
      
      return stdout
        .split('\n')
        .filter(line => line.trim())
        .map(line => {
          const statusCode = line.substring(0, 2);
          const filePath = line.substring(3);
          
          const statusMap: Record<string, string> = {
            'M ': 'Modified',
            ' M': 'Modified',
            'MM': 'Modified',
            'A ': 'Added',
            'D ': 'Deleted',
            ' D': 'Deleted',
            '??': 'Untracked',
          };
          
          return {
            path: filePath,
            status: statusMap[statusCode] || 'Changed'
          };
        });
    } catch (error) {
      console.error('Error getting Git status:', error);
      return [];
    }
  }

  async getDiff(directory: string, filePaths?: string[]): Promise<GitDiffResult> {
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
        const fileSet = new Set(filePaths.map(fp => path.relative(directory, fp)));
        relevantFiles = status.filter(f => fileSet.has(f.path) || filePaths.includes(f.path));
      }

      const files: GitFileChange[] = [];

      for (const file of relevantFiles) {
        let diff = '';

        if (file.status === 'Untracked') {
          // For untracked files, show entire content as additions
          const fullPath = path.join(directory, file.path);
          try {
            const content = await fs.promises.readFile(fullPath, 'utf-8');
            const lines = content.split('\n');
            diff = lines.map(line => `+ ${line}`).join('\n');
          } catch (error) {
            console.error(`Error reading untracked file ${file.path}:`, error);
            continue;
          }
        } else {
          // Get diff from Git
          try {
            const { stdout } = await this.execGit(
              ['diff', 'HEAD', '--', file.path],
              directory
            );
            diff = stdout;

            // If no diff with HEAD, try cached (staged)
            if (!diff) {
              const { stdout: cachedDiff } = await this.execGit(
                ['diff', '--cached', '--', file.path],
                directory
              );
              diff = cachedDiff;
            }
          } catch (error) {
            console.error(`Error getting diff for ${file.path}:`, error);
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
      console.error('Error getting Git diff:', error);
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
}

export const gitService = new GitService();
