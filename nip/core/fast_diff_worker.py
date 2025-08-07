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
    progress = Signal(str, bool)  # emits (progress message, is_user_action)
    sections_ready = Signal(list)  # emits list of (title, content, collapsed) tuples
    status_message = Signal(str, str, bool)  # emits (message, type, is_user_action) for status overlay
    operational_log = Signal(str, str)  # emits (message, level) for operational logging
    scan_completed = Signal(int, list, str)  # emits (scan_id, sections_data, cache_key) for race condition checking

    def __init__(self, root: str, include_paths: Optional[Set[str]], 
                 callback: Callable[[str], None], scan_id: int = 0, is_user_action: bool = True):
        super().__init__()
        self._root = root
        # CRITICAL: Create immutable snapshot to prevent selection mutations during scan
        self._include_snapshot = snapshot_selection(include_paths)
        self._include = set(self._include_snapshot) if self._include_snapshot else None  # Convert back for compatibility
        self._scan_id = scan_id  # Track scan ID for race condition prevention
        self._is_user_action = is_user_action  # Track if this is an explicit user action or background scan
        self._cancelled = False  # Cooperative cancellation flag
        self.operational_log.emit(f"FastDiffWorker created with immutable selection: {self._include_snapshot}", "debug")
        self.finished.connect(callback)

    def cancel(self):
        """Cancel the worker thread safely"""
        self._cancelled = True

    def run(self):
        try:
            # Early cancellation check
            if self._cancelled:
                return
                
            if self._is_user_action:
                self.progress.emit("Scanning for changes...", True)
            
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
            
            self.operational_log.emit(f"Cache key computed from selection_tuple: {self._include_snapshot} -> {cache_key}", "debug")
            
            # Use cached diff engine for smart scanning with precomputed cache key
            start_time = time.time()
            
            # CRITICAL FIX: Convert absolute paths to relative paths for get_changed_files_only
            # The cached diff engine expects relative paths but _include_snapshot contains absolute paths
            if self._include:
                relative_include = set()
                for abs_path in self._include:
                    try:
                        rel_path = os.path.relpath(abs_path, self._root)
                        relative_include.add(rel_path)
                    except Exception as e:
                        self.operational_log.emit(f"Path conversion error for {abs_path}: {e}", "error")
                
                new_files, changed_paths = cached_diff_engine.get_changed_files_only(
                    self._root, relative_include, cache_key
                )
            else:
                new_files, changed_paths = cached_diff_engine.get_changed_files_only(
                    self._root, self._include, cache_key
                )
            scan_time = time.time() - start_time
            
            # Check for cancellation after potentially long scanning operation
            if self._cancelled:
                return
            
            # TEMPORARILY COMMENTED OUT: Remove early return to test if logic is blocking updates
            # if not changed_paths:
            #     print("DEBUG: No changed paths detected, returning early")
            #     self.progress.emit("No changes detected", self._is_user_action)
            #     # Emit status message instead of calling finished callback
            #     self.status_message.emit("No changes detected since last scan", "info", self._is_user_action)
            #     return

            self.operational_log.emit(f"Found {len(changed_paths)} changed paths: {changed_paths}", "debug")
            if not changed_paths:
                self.operational_log.emit("No changed paths - but continuing processing to test logic", "debug")
            
            # Optimization: Avoid full rescan on mere deselection (no content changes)
            # If selection shrank and no files inside the remaining selection changed, 
            # we can skip expensive operations and just rebuild UI (which is now cheap with per-file sections)
            if not changed_paths and not self._is_user_action:
                self.operational_log.emit("Deselection detected with no content changes - using fast path", "debug")
            
            # Only show progress for user actions to reduce log noise in live mode
            if self._is_user_action:
                self.progress.emit(f"Found {len(changed_paths)} changed files in {scan_time:.1f}s", self._is_user_action)            # Load old snapshot for comparison, but filter it to current selection
            old_snapshot = cached_diff_engine._last_snapshot
            
            # CRITICAL FIX: Filter old snapshot to only include currently selected files
            # This prevents showing diffs from previously selected files
            filtered_old_snapshot = {}
            if old_snapshot and self._include_snapshot:
                # Use explicit selection snapshot instead of deriving from new_files.keys()
                current_file_paths = set(self._include_snapshot)
                for path in current_file_paths:
                    if path in old_snapshot:
                        filtered_old_snapshot[path] = old_snapshot[path]
                        
                self.operational_log.emit(f"Snapshot filtering:", "debug")
                self.operational_log.emit(f"  - Original old_snapshot keys: {set(old_snapshot.keys())}", "debug")
                self.operational_log.emit(f"  - Current selection paths: {current_file_paths}", "debug")
                self.operational_log.emit(f"  - Filtered old_snapshot keys: {set(filtered_old_snapshot.keys())}", "debug")
            
            # Create visual sections with filtered snapshot
            sections = cached_diff_engine.create_visual_diff(
                filtered_old_snapshot, new_files, changed_paths
            )
            
            # Generate traditional unified diff for copy functionality with filtered snapshot
            allowed = set(self._include_snapshot or [])
            new_snapshot = {k: v["content"] for k, v in new_files.items() if not allowed or k in allowed}
            unified_diff = format_output(filtered_old_snapshot, {k: v for k, v in new_files.items()})
            
            # Save ONLY the currently selected files to the snapshot  
            # This prevents mixing old and new file data in the cache
            cached_diff_engine.save_cache(new_snapshot, self._include, cache_key)
            cached_diff_engine._last_snapshot = new_snapshot
            
            # Emit sections for visual display - now one file per section
            sections_data = []
            for section in sections:
                # Each section now has exactly one file (per the new create_visual_diff implementation)
                fc = section.files[0]
                lines = []
                
                # Use simple markers for change types
                marker = {
                    "added": "+",
                    "deleted": "-", 
                    "modified": "~",
                    "unchanged": " "
                }.get(fc.change_type, " ")
                
                lines.append(f"{marker} {fc.path}")
                
                if fc.change_type == "modified":
                    lines.append("--- OLD ---")
                    lines.append(fc.old_content)
                    lines.append("--- NEW ---")
                    lines.append(fc.content)
                elif fc.change_type == "added":
                    lines.append(fc.content)
                elif fc.change_type == "deleted":
                    lines.append(fc.old_content)
                else:  # unchanged
                    # Show full content for unchanged files (no truncation)
                    lines.append(fc.content)
                
                sections_data.append((section.title, "\n".join(lines), section.collapsed))

            self.operational_log.emit(f"Emitting {len(sections_data)} sections for scan_id {self._scan_id}", "debug")
            for i, (title, content_preview, collapsed) in enumerate(sections_data):
                self.operational_log.emit(f"  Section {i}: {title} (collapsed={collapsed}, content_length={len(content_preview)})", "debug")
            
            # Emit with scan ID and cache key for race condition checking and forced re-renders
            self.scan_completed.emit(self._scan_id, sections_data, cache_key)
            
            # Also emit traditional diff for compatibility
            self.finished.emit(unified_diff)
            
            elapsed = time.time() - start_time
            
            # Only show progress completion for user actions to reduce log noise
            if self._is_user_action:
                self.progress.emit(f"Diff completed in {elapsed:.1f}s", self._is_user_action)
                self.status_message.emit(f"Diff completed in {elapsed:.1f}s", "success", self._is_user_action)
            else:
                # For background scans, just log operationally
                self.operational_log.emit(f"Background diff completed in {elapsed:.1f}s", "debug")
            
        except Exception as e:
            # Only show error progress for user actions to reduce log noise
            if self._is_user_action:
                self.progress.emit(f"Error: {str(e)}", self._is_user_action)
                self.status_message.emit(f"Error during diff: {str(e)}", "error", self._is_user_action)
            else:
                # For background scans, just log operationally
                self.operational_log.emit(f"Background scan error: {str(e)}", "error")
            # Don't emit to finished for errors to prevent overwriting content
            return