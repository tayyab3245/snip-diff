"""
File watching service for SNIP-DIFF live updates
Monitors selected files/directories and triggers diff recomputation on changes
"""

import os
import time
import hashlib
import threading
from typing import Dict, Set, List, Optional, Callable, Any
from dataclasses import dataclass, field
from pathlib import Path
from queue import Queue, Empty
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent

from app.core.algorithms.diff_core import HybridDiffEngine
from app.core.transformers.render_views import DiffRenderer
from app.core.models.diff_types import FileDiff, FileDiffMeta, ChangeType, RenderOptions


@dataclass
class FileSnapshot:
    """Snapshot of a file's content and metadata"""
    path: str
    content: str
    content_hash: str
    mtime: float
    size: int
    
    @classmethod
    def from_file(cls, path: str) -> Optional['FileSnapshot']:
        """Create snapshot from file path"""
        try:
            if not os.path.isfile(path):
                return None
                
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            mtime = os.path.getmtime(path)
            size = len(content)
            
            return cls(path=path, content=content, content_hash=content_hash, 
                      mtime=mtime, size=size)
        except (IOError, OSError, UnicodeDecodeError):
            return None


@dataclass
class DiffEvent:
    """Event representing a file diff change"""
    file_path: str
    change_type: ChangeType
    file_diff: Optional[FileDiff] = None
    error: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


class DiffWatchHandler(FileSystemEventHandler):
    """File system event handler for diff watching"""
    
    def __init__(self, watch_service: 'WatchService'):
        self.watch_service = watch_service
        self.debounce_delay = 0.25  # 250ms debounce
        self.pending_events: Dict[str, float] = {}
        self.debounce_timer: Optional[threading.Timer] = None
        
    def on_modified(self, event):
        if event.is_directory:
            return
        self._schedule_diff_update(event.src_path)
    
    def on_created(self, event):
        if event.is_directory:
            return
        self._schedule_diff_update(event.src_path)
    
    def on_deleted(self, event):
        if event.is_directory:
            return
        self._schedule_diff_update(event.src_path)
    
    def _schedule_diff_update(self, file_path: str):
        """Schedule diff update with debouncing"""
        # Normalize path
        file_path = os.path.abspath(file_path)
        
        # Check if file is being watched
        if not self.watch_service.is_file_watched(file_path):
            return
        
        # Update pending events
        self.pending_events[file_path] = time.time()
        
        # Reset debounce timer
        if self.debounce_timer:
            self.debounce_timer.cancel()
        
        self.debounce_timer = threading.Timer(
            self.debounce_delay, 
            self._process_pending_events
        )
        self.debounce_timer.start()
    
    def _process_pending_events(self):
        """Process all pending file change events"""
        current_time = time.time()
        events_to_process = []
        
        for file_path, event_time in self.pending_events.items():
            if current_time - event_time >= self.debounce_delay:
                events_to_process.append(file_path)
        
        # Clear processed events
        for file_path in events_to_process:
            del self.pending_events[file_path]
        
        # Batch process files
        if events_to_process:
            self.watch_service._process_file_changes(events_to_process)


class WatchService:
    """
    File watching service with live diff computation
    """
    
    def __init__(self):
        self.observer = Observer()
        self.diff_engine = HybridDiffEngine()
        self.diff_renderer = DiffRenderer()
        
        # File tracking
        self.watched_paths: Set[str] = set()
        self.baseline_snapshots: Dict[str, FileSnapshot] = {}
        self.current_snapshots: Dict[str, FileSnapshot] = {}
        
        # Event system
        self.event_queue: Queue[DiffEvent] = Queue()
        self.event_listeners: List[Callable[[DiffEvent], None]] = []
        
        # Threading
        self.lock = threading.RLock()
        self.is_running = False
        
        # Stats
        self.stats = {
            'events_processed': 0,
            'diffs_computed': 0,
            'errors': 0,
            'last_activity': None
        }
    
    def start(self):
        """Start the file watching service"""
        with self.lock:
            if self.is_running:
                return
            
            self.observer.start()
            self.is_running = True
            print("File watch service started")
    
    def stop(self):
        """Stop the file watching service"""
        with self.lock:
            if not self.is_running:
                return
            
            self.observer.stop()
            self.observer.join()
            self.is_running = False
            print("File watch service stopped")
    
    def watch_directory(self, directory: str, include_patterns: Optional[List[str]] = None):
        """
        Start watching a directory for changes
        
        Args:
            directory: Directory path to watch
            include_patterns: List of file patterns to include (e.g., ['*.py', '*.js'])
        """
        directory = os.path.abspath(directory)
        
        if not os.path.isdir(directory):
            raise ValueError(f"Directory does not exist: {directory}")
        
        with self.lock:
            # Create handler
            handler = DiffWatchHandler(self)
            
            # Start watching
            watch = self.observer.schedule(handler, directory, recursive=True)
            
            self.watched_paths.add(directory)
            print(f"Watching directory: {directory}")
            
            return watch
    
    def watch_files(self, file_paths: List[str]):
        """
        Start watching specific files for changes
        
        Args:
            file_paths: List of file paths to watch
        """
        with self.lock:
            for file_path in file_paths:
                file_path = os.path.abspath(file_path)
                
                if not os.path.isfile(file_path):
                    print(f"Warning: File does not exist: {file_path}")
                    continue
                
                # Create baseline snapshot
                snapshot = FileSnapshot.from_file(file_path)
                if snapshot:
                    self.baseline_snapshots[file_path] = snapshot
                    self.current_snapshots[file_path] = snapshot
                    self.watched_paths.add(file_path)
                    print(f"Watching file: {file_path}")
                
                # Watch parent directory if not already watched
                parent_dir = os.path.dirname(file_path)
                if parent_dir not in self.watched_paths:
                    self.watch_directory(parent_dir)
    
    def is_file_watched(self, file_path: str) -> bool:
        """Check if a file is being watched"""
        file_path = os.path.abspath(file_path)
        return file_path in self.watched_paths or any(
            file_path.startswith(watched_path) 
            for watched_path in self.watched_paths 
            if os.path.isdir(watched_path)
        )
    
    def set_baseline(self, file_path: str):
        """Set current file state as baseline for future diffs"""
        file_path = os.path.abspath(file_path)
        
        with self.lock:
            current = self.current_snapshots.get(file_path)
            if current:
                self.baseline_snapshots[file_path] = current
                print(f"Updated baseline for: {file_path}")
    
    def get_file_diff(self, file_path: str) -> Optional[FileDiff]:
        """Get current diff for a file vs its baseline"""
        file_path = os.path.abspath(file_path)
        
        with self.lock:
            baseline = self.baseline_snapshots.get(file_path)
            current = self.current_snapshots.get(file_path)
            
            if not baseline:
                return None
            
            if not current:
                # File was deleted
                meta = FileDiffMeta(
                    path=file_path,
                    change_type=ChangeType.DELETED,
                    file_size_old=baseline.size,
                    file_size_new=0
                )
                return FileDiff(meta=meta, hunks=[])
            
            if baseline.content_hash == current.content_hash:
                # No changes
                meta = FileDiffMeta(
                    path=file_path,
                    change_type=ChangeType.UNCHANGED,
                    file_size_old=baseline.size,
                    file_size_new=current.size
                )
                return FileDiff(meta=meta, hunks=[])
            
            # Compute diff
            return self._compute_file_diff(baseline, current)
    
    def add_event_listener(self, listener: Callable[[DiffEvent], None]):
        """Add event listener for diff changes"""
        self.event_listeners.append(listener)
    
    def remove_event_listener(self, listener: Callable[[DiffEvent], None]):
        """Remove event listener"""
        if listener in self.event_listeners:
            self.event_listeners.remove(listener)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        with self.lock:
            return {
                **self.stats,
                'watched_files': len(self.watched_paths),
                'baseline_snapshots': len(self.baseline_snapshots),
                'current_snapshots': len(self.current_snapshots),
                'event_queue_size': self.event_queue.qsize(),
                'is_running': self.is_running
            }
    
    def _process_file_changes(self, file_paths: List[str]):
        """Process batched file changes"""
        with self.lock:
            for file_path in file_paths:
                try:
                    self._process_single_file_change(file_path)
                except Exception as e:
                    self.stats['errors'] += 1
                    print(f"Error processing file change {file_path}: {e}")
            
            self.stats['last_activity'] = time.time()
    
    def _process_single_file_change(self, file_path: str):
        """Process change for a single file"""
        # Create new snapshot
        new_snapshot = FileSnapshot.from_file(file_path)
        old_snapshot = self.current_snapshots.get(file_path)
        
        # Update current snapshot
        if new_snapshot:
            self.current_snapshots[file_path] = new_snapshot
        elif file_path in self.current_snapshots:
            del self.current_snapshots[file_path]
        
        # Check if content actually changed
        if old_snapshot and new_snapshot:
            if old_snapshot.content_hash == new_snapshot.content_hash:
                return  # No actual content change
        
        # Compute diff vs baseline
        file_diff = self.get_file_diff(file_path)
        if not file_diff:
            return
        
        # Generate all render modes
        options = RenderOptions(context_radius=3)
        if file_diff.hunks:
            rendered_modes = self.diff_renderer.render_all_modes(file_diff.hunks, options)
            for mode_name, mode_data in rendered_modes.items():
                file_diff.add_mode(mode_name, mode_data)
        
        # Create and broadcast event
        change_type = file_diff.meta.change_type
        event = DiffEvent(
            file_path=file_path,
            change_type=change_type,
            file_diff=file_diff
        )
        
        self._broadcast_event(event)
        self.stats['events_processed'] += 1
        self.stats['diffs_computed'] += 1
    
    def _compute_file_diff(self, baseline: FileSnapshot, current: FileSnapshot) -> FileDiff:
        """Compute diff between baseline and current snapshots"""
        hunks, stats = self.diff_engine.generate_unified(baseline.content, current.content)
        
        # Determine change type
        if stats.total_changes == 0:
            change_type = ChangeType.UNCHANGED
        else:
            change_type = ChangeType.MODIFIED
        
        meta = FileDiffMeta(
            path=current.path,
            change_type=change_type,
            file_size_old=baseline.size,
            file_size_new=current.size,
            stats=stats
        )
        
        return FileDiff(meta=meta, hunks=hunks)
    
    def get_recent_events(self, limit: int = 50) -> List[DiffEvent]:
        """Get recent events from the queue"""
        events = []
        temp_events = []
        
        # Extract events from queue without losing them
        try:
            while not self.event_queue.empty() and len(events) < limit:
                event = self.event_queue.get_nowait()
                events.append(event)
                temp_events.append(event)
        except:
            pass
        
        # Put events back in queue
        for event in temp_events:
            self.event_queue.put(event)
        
        return events[-limit:] if events else []
    
    def clear_all(self):
        """Clear all watched files and events"""
        self.stop()
        self.watched_files.clear()
        self.baseline_snapshots.clear()
        self.current_snapshots.clear()
        
        # Clear event queue
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except:
                break
    
    def unwatch_file(self, file_path: str) -> bool:
        """Remove a file from the watch list"""
        if file_path in self.watched_files:
            del self.watched_files[file_path]
            self.baseline_snapshots.pop(file_path, None)
            self.current_snapshots.pop(file_path, None)
            return True
        return False
    
    def _broadcast_event(self, event: DiffEvent):
        """Broadcast event to all listeners"""
        self.event_queue.put(event)
        
        for listener in self.event_listeners:
            try:
                listener(event)
            except Exception as e:
                print(f"Error in event listener: {e}")


# Global instance
watch_service = WatchService()

__all__ = ['WatchService', 'watch_service', 'DiffEvent', 'FileSnapshot']
