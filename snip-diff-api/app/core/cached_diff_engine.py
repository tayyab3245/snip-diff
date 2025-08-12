"""
Cached diff engine for FastAPI backend
Simplified version focused on API operations without Qt dependencies
"""

import hashlib
import json
import os
import time
from dataclasses import dataclass
from typing import Dict, Set, Optional, List, Tuple

from .snapshot import get_all_files, IGNORE_LIST
from .diff_engine import format_output

@dataclass
class FileChange:
    """Represents a single file change"""
    path: str
    change_type: str  # 'added', 'modified', 'deleted', 'unchanged'
    content: str
    old_content: str = ""

@dataclass 
class DiffSection:
    """Represents a visual section in the diff"""
    title: str
    files: List[FileChange]
    collapsed: bool = False

class CachedDiffEngine:
    """Enhanced diff engine with smart caching for API use"""
    
    def __init__(self):
        self._file_cache: Dict[str, dict] = {}
        self._last_snapshot: Dict[str, str] = {}
        self._last_cache_key: Optional[str] = None
        self._scan_results: Dict[str, dict] = {}  # Store scan results by ID
    
    def _compute_cache_key(self, include_paths: Optional[Set[str]], directory: str, 
                          mode: str = 'api_scan') -> str:
        """Compute deterministic cache key for current scan parameters"""
        if include_paths is None:
            selection_tuple = ()
        else:
            selection_tuple = tuple(sorted(include_paths))
        
        cache_data = {
            'files': selection_tuple,
            'directory': os.path.abspath(directory),
            'mode': mode,
            'timestamp': int(time.time() / 300)  # 5-minute buckets for cache stability
        }
        
        raw = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
    
    def get_changed_files_only(
        self, 
        directory: str, 
        include_paths: Optional[Set[str]] = None,
        cache_key: Optional[str] = None
    ) -> Tuple[Dict[str, dict], Set[str]]:
        """
        Scan directory and return only changed files with their content.
        Returns (changed_files, changed_paths)
        """
        if cache_key is None:
            cache_key = self._compute_cache_key(include_paths, directory)
        
        cache_key_changed = self._last_cache_key != cache_key
        changed_files = {}
        changed_paths = set()
        
        # Quick scan for file mtimes
        for root, _, filenames in os.walk(directory):
            if self._should_skip(root.split(os.sep)):
                continue
                
            for filename in filenames:
                abs_path = os.path.join(root, filename)
                rel_path = os.path.relpath(abs_path, directory)
                
                if self._should_skip(rel_path.split(os.sep)):
                    continue
                if include_paths and not any(
                    rel_path == p or rel_path.startswith(f"{p}{os.sep}")
                    for p in include_paths
                ):
                    continue
                
                try:
                    current_mtime = os.path.getmtime(abs_path)
                    cached_info = self._file_cache.get(rel_path, {})
                    last_mtime = cached_info.get('mtime', 0)
                    
                    # Read file content if mtime changed OR cache key changed
                    if current_mtime != last_mtime or cache_key_changed:
                        try:
                            with open(abs_path, "r", encoding="utf-8") as fh:
                                content = fh.read()
                        except UnicodeDecodeError:
                            try:
                                with open(abs_path, "r", encoding="latin-1") as fh:
                                    content = fh.read()
                            except Exception:
                                continue
                        
                        changed_files[rel_path] = {
                            "content": content,
                            "mtime": current_mtime
                        }
                        
                        # Update cache
                        self._file_cache[rel_path] = {
                            "content": content,
                            "mtime": current_mtime
                        }
                        
                        # Mark as changed if content actually changed
                        if current_mtime != last_mtime or cache_key_changed:
                            changed_paths.add(rel_path)
                    else:
                        # Use cached content
                        cached_content = cached_info.get('content', '')
                        changed_files[rel_path] = {
                            "content": cached_content,
                            "mtime": current_mtime
                        }
                        
                except Exception:
                    pass
        
        # Check for deleted files
        if self._last_snapshot:
            old_paths = set(self._last_snapshot.keys())
            current_paths = set(changed_files.keys())
            deleted_paths = old_paths - current_paths
            changed_paths.update(deleted_paths)
        
        # If fresh scan or cache key changed, treat all files as changed
        if not self._last_snapshot or cache_key_changed:
            changed_paths.update(set(changed_files.keys()))
        
        self._last_cache_key = cache_key
        return changed_files, changed_paths
    
    def _should_skip(self, path_parts) -> bool:
        """Check if path should be skipped"""
        return any(part in IGNORE_LIST for part in path_parts)
    
    def create_visual_diff(
        self, 
        old_snapshot: Dict[str, str], 
        new_files: Dict[str, dict],
        changed_paths: Set[str]
    ) -> List[DiffSection]:
        """
        Create visually separated diff sections - one section per file.
        Shows ALL selected files as individual expandable sections.
        """
        sections = []
        
        # Process ALL files from current selection
        all_selected_files = set(new_files.keys()) | (set(old_snapshot.keys()) - set(new_files.keys()))
        
        for path in sorted(all_selected_files):
            old_content = old_snapshot.get(path, "")
            new_entry = new_files.get(path)
            new_content = new_entry.get("content", "") if new_entry is not None else ""
            
            # Determine change type
            if not old_content and new_content:
                change_type = "added"
                status = "Added"
            elif old_content and new_entry is None:
                change_type = "deleted" 
                status = "Deleted"
            elif old_content and not new_content:
                change_type = "deleted" 
                status = "Deleted"
            elif old_content != new_content:
                change_type = "modified"
                status = "Modified"
            else:
                change_type = "unchanged"
                status = "Unchanged"
            
            # Create file change object
            file_change = FileChange(
                path=path,
                change_type=change_type,
                content=new_content,
                old_content=old_content
            )
            
            # Create section title
            filename = os.path.basename(path)
            relative_dir = os.path.dirname(path)
            
            if relative_dir:
                title = f"{filename} ({relative_dir})"
            else:
                title = filename
            
            sections.append(DiffSection(
                title=title,
                files=[file_change],
                collapsed=(change_type == "unchanged")
            ))
        
        return sections
    
    def save_scan_result(self, scan_id: str, result: dict):
        """Save scan result for later retrieval"""
        self._scan_results[scan_id] = result
    
    def get_scan_result(self, scan_id: str) -> Optional[dict]:
        """Get saved scan result"""
        return self._scan_results.get(scan_id)
    
    def save_cache(self, snapshot: Dict[str, str], cache_key: Optional[str] = None):
        """Save snapshot and update internal state"""
        self._last_snapshot = snapshot
        self._last_cache_key = cache_key

# Global instance for API use
cached_diff_engine = CachedDiffEngine()
