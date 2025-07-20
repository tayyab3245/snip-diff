"""
Enhanced worker with intelligent caching for faster diff updates
"""

from __future__ import annotations
from typing import Set, Callable, Optional, Dict, List, Tuple
import os
import time

from PySide6.QtCore import QThread, Signal

from nip.core.cached_diff_engine import cached_diff_engine
from nip.core.diff_engine import format_output


def snapshot_selection(sel_set: Optional[Set[str]]) -> Optional[Tuple[str, ...]]:
    """Create immutable snapshot of selection to prevent mutation during scans"""
    if sel_set is None:
        return None
    return tuple(sorted(sel_set))


class FastDiffWorker(QThread):
    """Enhanced diff worker with smart caching"""
    
    finished = Signal(str)  # emits formatted diff text
    progress = Signal(str)  # emits progress updates
    sections_ready = Signal(list)  # emits list of (title, content, collapsed) tuples
    status_message = Signal(str, str)  # emits (message, type) for status overlay
    scan_completed = Signal(int, list, str)  # emits (scan_id, sections_data, cache_key) for race condition checking

    def __init__(self, root: str, include_paths: Optional[Set[str]], 
                 callback: Callable[[str], None], scan_id: int = 0):
        super().__init__()
        self._root = root
        # CRITICAL: Create immutable snapshot to prevent selection mutations during scan
        self._include_snapshot = snapshot_selection(include_paths)
        self._include = set(self._include_snapshot) if self._include_snapshot else None  # Convert back for compatibility
        self._scan_id = scan_id  # Track scan ID for race condition prevention
        print(f"DEBUG: FastDiffWorker created with immutable selection: {self._include_snapshot}")
        self.finished.connect(callback)

    def run(self):
        try:
            self.progress.emit("Scanning for changes...")
            
            # CRITICAL: Compute cache key BEFORE any cache operations
            # Include mode parameters that affect output - use immutable selection tuple
            is_single_file = self._include_snapshot and len(self._include_snapshot) == 1
            mode = 'single_file' if is_single_file else 'multi_file'
            
            # ENSURE: Pass the immutable selection tuple, not the mutable set
            cache_key = cached_diff_engine._compute_cache_key(
                self._include_snapshot,  # Use immutable tuple, not mutable set
                self._root, 
                mode=mode, 
                max_depth=100,  # Could be configurable
                include_binary=False  # Could be configurable
            )
            
            print(f"DEBUG: Cache key computed from selection_tuple: {self._include_snapshot} -> {cache_key}")
            
            # Use cached diff engine for smart scanning with precomputed cache key
            start_time = time.time()
            new_files, changed_paths = cached_diff_engine.get_changed_files_only(
                self._root, self._include, cache_key
            )
            scan_time = time.time() - start_time
            
            # TEMPORARILY COMMENTED OUT: Remove early return to test if logic is blocking updates
            # if not changed_paths:
            #     print("DEBUG: No changed paths detected, returning early")
            #     self.progress.emit("No changes detected")
            #     # Emit status message instead of calling finished callback
            #     self.status_message.emit("No changes detected since last scan", "info")
            #     return

            print(f"DEBUG: Found {len(changed_paths)} changed paths: {changed_paths}")
            if not changed_paths:
                print("DEBUG: No changed paths - but continuing processing to test logic")
            self.progress.emit(f"Found {len(changed_paths)} changed files in {scan_time:.1f}s")            # Load old snapshot for comparison, but filter it to current selection
            old_snapshot = cached_diff_engine._last_snapshot
            
            # CRITICAL FIX: Filter old snapshot to only include currently selected files
            # This prevents showing diffs from previously selected files
            filtered_old_snapshot = {}
            if old_snapshot and self._include:
                current_file_paths = set(new_files.keys())
                for path in current_file_paths:
                    if path in old_snapshot:
                        filtered_old_snapshot[path] = old_snapshot[path]
                        
                print(f"DEBUG: Snapshot filtering:")
                print(f"  - Original old_snapshot keys: {set(old_snapshot.keys())}")
                print(f"  - Current file paths: {current_file_paths}")
                print(f"  - Filtered old_snapshot keys: {set(filtered_old_snapshot.keys())}")
            
            # Create visual sections with filtered snapshot
            sections = cached_diff_engine.create_visual_diff(
                filtered_old_snapshot, new_files, changed_paths
            )
            
            # Generate traditional unified diff for copy functionality with filtered snapshot
            new_snapshot = {k: v["content"] for k, v in new_files.items()}
            unified_diff = format_output(filtered_old_snapshot, {k: v for k, v in new_files.items()})
            
            # Save ONLY the currently selected files to the snapshot  
            # This prevents mixing old and new file data in the cache
            cached_diff_engine.save_cache(new_snapshot, self._include, cache_key)
            cached_diff_engine._last_snapshot = new_snapshot
            
            # Emit sections for visual display
            sections_data = []
            for section in sections:
                # Create content for this section
                section_content = []
                for file_change in section.files:
                    if file_change.change_type == "added":
                        section_content.append(f"+ {file_change.path}")
                        section_content.append(file_change.content)
                    elif file_change.change_type == "deleted":
                        section_content.append(f"- {file_change.path}")
                        section_content.append(file_change.old_content)
                    elif file_change.change_type == "modified":
                        section_content.append(f"~ {file_change.path}")
                        # Simple before/after for now
                        section_content.append("--- OLD ---")
                        section_content.append(file_change.old_content[:500] + "..." if len(file_change.old_content) > 500 else file_change.old_content)
                        section_content.append("--- NEW ---")
                        section_content.append(file_change.content[:500] + "..." if len(file_change.content) > 500 else file_change.content)
                
                sections_data.append((
                    section.title,
                    "\n".join(section_content),
                    section.collapsed
                ))

            print(f"DEBUG: Emitting {len(sections_data)} sections for scan_id {self._scan_id}")
            for i, (title, content_preview, collapsed) in enumerate(sections_data):
                print(f"  Section {i}: {title} (collapsed={collapsed}, content_length={len(content_preview)})")
            
            # Emit with scan ID and cache key for race condition checking and forced re-renders
            self.scan_completed.emit(self._scan_id, sections_data, cache_key)
            
            # Also emit traditional diff for compatibility
            self.finished.emit(unified_diff)
            
            elapsed = time.time() - start_time
            self.progress.emit(f"Diff completed in {elapsed:.1f}s")
            self.status_message.emit(f"Diff completed in {elapsed:.1f}s", "success")
            
        except Exception as e:
            self.progress.emit(f"Error: {str(e)}")
            self.status_message.emit(f"Error during diff: {str(e)}", "error")
            # Don't emit to finished for errors to prevent overwriting content
            return
