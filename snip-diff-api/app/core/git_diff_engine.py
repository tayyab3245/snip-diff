"""
Git-based diff engine for SNIP-DIFF
Uses native Git commands for robust diffing
"""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


class GitDiffEngine:
    """Handles diff operations using Git"""
    
    def __init__(self):
        self.git_available = self._check_git_available()
    
    def _check_git_available(self) -> bool:
        """Check if Git is available on the system"""
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _is_git_repo(self, directory: str) -> bool:
        """Check if directory is inside a Git repository"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=directory,
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_file_content(self, file_path: str, ref: str = 'HEAD') -> Optional[str]:
        """
        Get file content from Git
        
        Args:
            file_path: Path to the file
            ref: Git ref (HEAD, commit hash, etc.)
        
        Returns:
            File content or None if not in Git
        """
        try:
            directory = os.path.dirname(file_path)
            relative_path = os.path.basename(file_path)
            
            result = subprocess.run(
                ['git', 'show', f'{ref}:{relative_path}'],
                cwd=directory,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                return result.stdout
            return None
        except Exception as e:
            print(f"Error getting file content from Git: {e}")
            return None
    
    def get_diff(self, directory: str, file_paths: Optional[List[str]] = None, 
                 context_lines: int = 3, unified: bool = True) -> Dict[str, Any]:
        """
        Get Git diff for specified files or entire directory
        
        Args:
            directory: Repository root or subdirectory
            file_paths: Optional list of specific files to diff
            context_lines: Number of context lines in diff
            unified: Whether to use unified diff format
        
        Returns:
            Dict with diff information
        """
        if not self.git_available:
            return {
                'success': False,
                'error': 'Git is not available on this system'
            }
        
        if not self._is_git_repo(directory):
            return {
                'success': False,
                'error': 'Directory is not a Git repository'
            }
        
        try:
            # Get status to identify changed files
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=directory,
                capture_output=True,
                text=True,
                check=True
            )
            
            changed_files = self._parse_git_status(status_result.stdout, directory)
            
            # Filter by specified paths if provided
            if file_paths:
                abs_paths = {os.path.abspath(fp) for fp in file_paths}
                changed_files = [f for f in changed_files if f['abs_path'] in abs_paths]
            
            # Get diff for each changed file
            sections = []
            for file_info in changed_files:
                diff_text = self._get_file_diff(
                    directory, 
                    file_info['path'], 
                    file_info['status'],
                    context_lines
                )
                
                if diff_text:
                    sections.append({
                        'title': f"{file_info['status']}: {file_info['path']}",
                        'path': file_info['path'],
                        'status': file_info['status'],
                        'diff': diff_text,
                        'collapsed': False
                    })
            
            return {
                'success': True,
                'sections': sections,
                'file_count': len(changed_files),
                'changed_count': len(sections)
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'error': f'Git command failed: {e.stderr if e.stderr else str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error getting diff: {str(e)}'
            }
    
    def _parse_git_status(self, status_output: str, directory: str) -> List[Dict[str, str]]:
        """Parse git status --porcelain output"""
        files = []
        for line in status_output.strip().split('\n'):
            if not line:
                continue
            
            status_code = line[:2]
            file_path = line[3:]
            
            # Map git status codes to readable names
            status_map = {
                'M ': 'Modified',
                ' M': 'Modified',
                'MM': 'Modified',
                'A ': 'Added',
                'D ': 'Deleted',
                ' D': 'Deleted',
                'R ': 'Renamed',
                'C ': 'Copied',
                '??': 'Untracked',
                '!!': 'Ignored'
            }
            
            status = status_map.get(status_code, 'Changed')
            abs_path = os.path.abspath(os.path.join(directory, file_path))
            
            files.append({
                'path': file_path,
                'abs_path': abs_path,
                'status': status,
                'status_code': status_code
            })
        
        return files
    
    def _get_file_diff(self, directory: str, file_path: str, 
                       status: str, context_lines: int) -> Optional[str]:
        """Get diff for a specific file"""
        try:
            if status == 'Untracked':
                # For untracked files, show entire content as added
                full_path = os.path.join(directory, file_path)
                if os.path.exists(full_path):
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    lines = content.split('\n')
                    return '\n'.join(f'+ {line}' for line in lines)
                return None
            
            # For tracked files, use git diff
            result = subprocess.run(
                ['git', 'diff', f'--unified={context_lines}', 'HEAD', '--', file_path],
                cwd=directory,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0 and result.stdout:
                return result.stdout
            
            # If no diff with HEAD, might be staged
            result = subprocess.run(
                ['git', 'diff', f'--unified={context_lines}', '--cached', '--', file_path],
                cwd=directory,
                capture_output=True,
                text=True,
                check=False
            )
            
            return result.stdout if result.returncode == 0 else None
            
        except Exception as e:
            print(f"Error getting diff for {file_path}: {e}")
            return None
    
    def watch_changes(self, directory: str, file_paths: List[str]) -> Dict[str, Any]:
        """
        Get current changes for watched files
        Intended to be called when file changes are detected
        """
        return self.get_diff(directory, file_paths)


# Global instance
git_diff_engine = GitDiffEngine()
