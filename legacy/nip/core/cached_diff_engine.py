"""
================================================================================
SNIP-DIFF - AI workflow tool for preparing code context outside agentic environments
================================================================================

Copyright (c) 2025 Tayyab. All Rights Reserved.

PROPRIETARY AND CONFIDENTIAL

This software and associated documentation files (the "Software") are the 
exclusive property of the copyright holder. This Software contains proprietary 
and confidential information and is protected by copyright laws and 
international treaty provisions.

RESTRICTIONS:
- No part of this Software may be reproduced, distributed, or transmitted 
  in any form or by any means without the prior written permission of the 
  copyright holder.
- This Software is not for sale, license, or distribution to third parties.
- Reverse engineering, decompilation, or disassembly of this Software is 
  strictly prohibited.
- Any unauthorized use, copying, or distribution may result in severe civil 
  and criminal penalties.

This Software is provided "AS IS" without warranty of any kind, express or 
implied, including but not limited to the warranties of merchantability, 
fitness for a particular purpose, and non-infringement.

For licensing inquiries, please contact: tayyab3245@github.com
================================================================================
"""


"""
Enhanced diff engine with caching and visual separation
──────────────────────────────────────────────────────────────────────────
• Intelligent caching based on file modification times
• Visual separation of different file types/folders
• Incremental updates for better performance
"""

import os
import json
import hashlib
from typing import Dict, Set, Optional, List, Tuple
from dataclasses import dataclass
from collections import defaultdict

from nip.config import SNAPSHOT_FILE, IGNORE_LIST


@dataclass
class FileChange:
    """Represents a single file change"""
    path: str
    change_type: str  # 'added', 'modified', 'deleted', 'unchanged'
    content: str = ""
    old_content: str = ""


@dataclass 
class DiffSection:
    """Represents a visual section in the diff"""
    title: str
    files: List[FileChange]
    collapsed: bool = False


class CachedDiffEngine:
    """Enhanced diff engine with smart caching"""
    
    def __init__(self):
        self._file_cache: Dict[str, dict] = {}  # path -> {content, mtime, hash}
        self._last_snapshot: Dict[str, str] = {}
        self._last_selected_paths: Optional[Set[str]] = None  # Track selected files (deprecated)
        self._previous_selection_tuple: Optional[Tuple[str, ...]] = None  # Track previous selection by value
        self._last_cache_key: Optional[str] = None  # Track deterministic cache key
        self._prev_cache_key: Optional[str] = None  # Previous cache key for safety validation
        self.load_cache()
    
    def _compute_cache_key(self, include_paths: Optional[Set[str] | Tuple[str, ...]], directory: str, 
                          mode: str = 'fast_diff', max_depth: int = 100, 
                          include_binary: bool = False) -> str:
        """Compute deterministic cache key for current scan parameters"""
        # Handle both mutable sets and immutable tuples - always convert to tuple
        if include_paths is None:
            selection_tuple = ()
        elif isinstance(include_paths, tuple):
            selection_tuple = include_paths  # Already immutable tuple
        else:
            selection_tuple = tuple(sorted(include_paths))  # Convert set to sorted tuple
        
        # Include all parameters that affect output in the cache key
        cache_data = {
            'files': selection_tuple,  # Use full selection tuple, not just list
            'directory': os.path.abspath(directory),
            'mode': mode,  # single-file vs multi-file vs enhanced
            'max_depth': max_depth,  # directory traversal depth
            'include_binary': include_binary,  # whether to include binary files
            'file_count': len(selection_tuple),  # affects processing approach
            'is_single_file': len(selection_tuple) == 1,  # single vs multi-file mode
        }
        
        # Use SHA-256 for better hash distribution
        raw = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]  # 16 chars for lower collision risk
    
    def load_cache(self):
        """Load previous snapshot and file cache"""
        if os.path.exists(SNAPSHOT_FILE):
            with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and 'snapshot' in data:
                    # New format with metadata
                    self._last_snapshot = data.get('snapshot', {})
                    selected_paths = data.get('selected_paths', None)
                    self._last_selected_paths = set(selected_paths) if selected_paths else None
                    self._last_cache_key = data.get('cache_key', None)
                    # Convert loaded selection to immutable tuple for value comparison
                    self._previous_selection_tuple = tuple(sorted(selected_paths)) if selected_paths else None
                else:
                    # Old format - just the snapshot
                    self._last_snapshot = data
                    self._last_selected_paths = None
                    self._previous_selection_tuple = None
                    self._last_cache_key = None
                    self._prev_cache_key = None
        
        cache_file = SNAPSHOT_FILE.replace('.json', '_cache.json')
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                self._file_cache = json.load(f)
    
    def save_cache(self, snapshot: Dict[str, str], selected_paths: Optional[Set[str]] = None, cache_key: Optional[str] = None):
        """Save snapshot and file cache"""
        # Save with metadata including selected paths and cache key
        data = {
            'snapshot': snapshot,
            'selected_paths': list(selected_paths) if selected_paths else None,
            'cache_key': cache_key
        }
        with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        cache_file = SNAPSHOT_FILE.replace('.json', '_cache.json')
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(self._file_cache, f, indent=2)
        
        # Update last state
        self._last_selected_paths = selected_paths
        self._last_cache_key = cache_key
    
    def clear_cache(self):
        """Clear all cached data - useful when switching to a new folder"""
        self._file_cache.clear()
        self._last_snapshot.clear()
        self._last_selected_paths = None
        self._previous_selection_tuple = None  # Clear immutable selection tracking
        self._last_cache_key = None
        self._prev_cache_key = None
        
        # Remove cache files
        if os.path.exists(SNAPSHOT_FILE):
            os.remove(SNAPSHOT_FILE)
        
        cache_file = SNAPSHOT_FILE.replace('.json', '_cache.json')
        if os.path.exists(cache_file):
            os.remove(cache_file)
    
    def get_changed_files_only(
        self, 
        directory: str, 
        include_paths: Optional[Set[str] | Tuple[str, ...]] = None,
        cache_key: Optional[str] = None
    ) -> Tuple[Dict[str, dict], Set[str]]:
        """
        Get only files that have changed since last run.
        Returns: (new_files_dict, changed_paths_set)
        """
        changed_files = {}
        changed_paths = set()
        
        # Use provided cache key or compute one
        if cache_key is None:
            current_cache_key = self._compute_cache_key(include_paths, directory)
        else:
            current_cache_key = cache_key
            
        cache_key_changed = self._last_cache_key != current_cache_key
        
        # CRITICAL: Convert selection to immutable tuple for value comparison
        if include_paths is None:
            current_selection_tuple = None
        elif isinstance(include_paths, tuple):
            current_selection_tuple = include_paths  # Already immutable
        else:
            current_selection_tuple = tuple(sorted(include_paths))  # Make immutable
        
        # Detect change via VALUE comparison, not identity
        selection_changed = self._previous_selection_tuple != current_selection_tuple
        
        # SAFETY CHECK: Invalidate on selection change even if cache key somehow didn't change
        # This guards against accidental reuse of old results
        invalidate_safety = False
        if self._prev_cache_key is not None and self._prev_cache_key != current_cache_key:
            # Selection definitely changed, ensure we don't reuse old snapshot/cache
            if self._last_snapshot:
                print("DEBUG: SAFETY INVALIDATION - Previous cache key differs, clearing snapshot")
                self._last_snapshot = {}
                invalidate_safety = True
        
        print(f"DEBUG: Cache key: {self._last_cache_key} -> {current_cache_key} (changed: {cache_key_changed})")
        print(f"DEBUG: Selection: {self._previous_selection_tuple} -> {current_selection_tuple} (changed: {selection_changed})")
        print(f"DEBUG: Safety invalidation: {invalidate_safety}")
        
        # Store current key as previous for next run
        self._prev_cache_key = current_cache_key
        
        # Quick scan for file mtimes only (much faster than reading content)
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
                    
                    # Read file content if mtime changed OR cache key changed (different selection)
                    if current_mtime != last_mtime or cache_key_changed:
                        try:
                            with open(abs_path, "r", encoding="utf-8") as fh:
                                content = fh.read()
                        except UnicodeDecodeError:
                            # Try with latin-1 as fallback, or skip binary files
                            try:
                                with open(abs_path, "r", encoding="latin-1") as fh:
                                    content = fh.read()
                            except Exception:
                                # Skip binary or unreadable files
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
                        
                        # Mark as changed if file content actually changed OR cache key changed
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
                    # Binary or unreadable file
                    pass
        
        # Check for deleted files
        old_paths = set(self._last_snapshot.keys())
        current_paths = set(changed_files.keys())
        deleted_paths = old_paths - current_paths
        changed_paths.update(deleted_paths)
        
        # If this is a fresh scan (no previous snapshot) OR cache key changed OR safety invalidation, treat all files as new
        if not self._last_snapshot or cache_key_changed or invalidate_safety:
            changed_paths.update(current_paths)
        
        # Update last cache key to track for next scan
        self._last_cache_key = current_cache_key
        
        # CRITICAL: Always update previous selection even if "no changed paths"
        # This must happen before return to ensure proper change detection next time
        self._previous_selection_tuple = current_selection_tuple
        print(f"DEBUG: Updated previous_selection_tuple to: {self._previous_selection_tuple}")
        
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
        Shows ALL selected files (changed and unchanged) as individual expandable sections.
        """
        sections = []
        
        # Process ALL files from current selection AND previously selected files that might be deleted
        # Include files that existed in old snapshot but are deleted in new selection
        all_selected_files = set(new_files.keys()) | (set(old_snapshot.keys()) - set(new_files.keys()))
        
        for path in sorted(all_selected_files):
            old_content = old_snapshot.get(path, "")
            new_entry = new_files.get(path)  # Use get() without default to detect None
            new_content = new_entry.get("content", "") if new_entry is not None else ""
            
            # Determine change type for each file
            if not old_content and new_content:
                change_type = "added"
                icon = "[+]"
                status = "Added"
            elif old_content and new_entry is None:  # File was deleted
                change_type = "deleted" 
                icon = "[D]"
                status = "Deleted"
            elif old_content and not new_content:
                change_type = "deleted" 
                icon = "[D]"
                status = "Deleted"
            elif old_content != new_content:
                change_type = "modified"
                icon = "[M]"
                status = "Modified"
            else:
                change_type = "unchanged"
                icon = "[U]"
                status = "Unchanged"
            
            # Create individual section for each file
            file_change = FileChange(
                path=path,
                change_type=change_type,
                content=new_content,
                old_content=old_content
            )
            
            # File name with simplified format
            filename = os.path.basename(path)
            relative_dir = os.path.dirname(path)
            
            # Simplified title format
            if relative_dir:
                title = f"{filename} ({relative_dir})"
            else:
                title = filename
            
            sections.append(DiffSection(
                title=title,
                files=[file_change],  # One file per section
                collapsed=(change_type == "unchanged")  # Auto-collapse unchanged files
            ))
        
        return sections


# Global instance
cached_diff_engine = CachedDiffEngine()
