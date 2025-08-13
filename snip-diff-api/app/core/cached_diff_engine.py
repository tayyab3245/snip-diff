"""
Cached Diff Engine for SNIP-DIFF - Thread-safe implementation for SD-002
"""

import os
import hashlib
import threading
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Iterable
from concurrent.futures import ThreadPoolExecutor

from .diff_engine import DiffEngine


class ScanStatus(Enum):
    """
    Canonical lifecycle for API responses (lowercase values).
    Keep values lowercase to match UI and HTTP payloads.
    """
    PENDING   = "pending"
    RUNNING   = "running"
    COMPLETED = "completed"
    FAILED    = "failed"
    CANCELLED = "cancelled"

def _coerce_status(value: "ScanStatus|str") -> ScanStatus:
    if isinstance(value, ScanStatus):
        return value
    return ScanStatus(str(value).lower())


@dataclass
class ScanResult:
    """Result of a scan operation"""
    scan_id: str
    status: ScanStatus
    directory: str
    include_paths: List[str] = field(default_factory=list)
    started_at: float = field(default_factory=time.time)
    finished_at: Optional[float] = None
    progress: float = 0.0
    sections: Optional[List[Dict[str, Any]]] = None
    unified_diff: Optional[str] = None
    file_count: int = 0
    changed_count: int = 0
    error: Optional[str] = None
    snapshot: Optional[Dict[str, Any]] = None


@dataclass 
class CacheEntry:
    """Cache entry for file snapshots"""
    content_hash: str
    snapshot: Dict[str, Any]
    created_at: float
    last_accessed: float

# ---------- Cache helpers (module-level, no circular imports) ----------
def make_cache_key(base_path: str, include_paths: Optional[Iterable[str]]) -> str:
    norm_base = os.path.abspath(base_path).replace("\\", "/")
    parts = sorted(include_paths) if include_paths else []
    key = f"{norm_base}:{':'.join(parts)}"
    return hashlib.md5(key.encode("utf-8")).hexdigest()

def compute_content_hash(base_path: str, include_paths: Optional[Iterable[str]] = None) -> str:
    """Compute hash of file contents for cache validation with chunked reading."""
    hasher = hashlib.md5()
    chunk_size = 1024 * 1024  # 1MB
    try:
        if include_paths is None:
            if os.path.isfile(base_path):
                with open(base_path, "rb") as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        hasher.update(chunk)
                hasher.update(str(os.path.getmtime(base_path)).encode())
            return hasher.hexdigest()
        for rel in sorted(include_paths):
            fp = os.path.join(base_path, rel)
            if os.path.isfile(fp):
                try:
                    with open(fp, "rb") as f:
                        while True:
                            chunk = f.read(chunk_size)
                            if not chunk:
                                break
                            hasher.update(chunk)
                    hasher.update(str(os.path.getmtime(fp)).encode())
                except (IOError, OSError):
                    hasher.update(b"unreadable")
    except Exception:
        hasher.update(str(time.time()).encode())
    return hasher.hexdigest()


class ScanRegistry:
    """Thread-safe registry for managing scan operations"""
    
    def __init__(self):
        self._scans: Dict[str, ScanResult] = {}
        self._lock = threading.RLock()
        
    def create_scan(self, directory: str, include_paths: List[str]) -> str:
        """Create a new scan and return its ID"""
        scan_id = str(uuid.uuid4())
        with self._lock:
            self._scans[scan_id] = ScanResult(
                scan_id=scan_id,
                status=ScanStatus.PENDING,
                directory=directory,
                include_paths=list(include_paths or []),
            )
        return scan_id
    
    def get_scan(self, scan_id: str) -> Optional[ScanResult]:
        """Get scan by ID (object)"""
        with self._lock:
            return self._scans.get(scan_id)
    
    def update_scan_status(self, scan_id: str, status: ScanStatus, error: str = None):
        """Update scan status"""
        with self._lock:
            if scan_id in self._scans:
                s = _coerce_status(status)
                self._scans[scan_id].status = s
                if s in (ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED):
                    self._scans[scan_id].finished_at = time.time()
                if error:
                    self._scans[scan_id].error = error
    
    def update_scan(self, scan_id: str, **kwargs):
        """Update scan with arbitrary fields"""
        with self._lock:
            if scan_id in self._scans:
                scan = self._scans[scan_id]
                for key, value in kwargs.items():
                    if key == "status":
                        setattr(scan, key, _coerce_status(value))
                    elif hasattr(scan, key):
                        setattr(scan, key, value)
                
                # Auto-set finished_at when status becomes terminal
                if 'status' in kwargs and _coerce_status(kwargs['status']) in (ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED):
                    timestamp = time.time()
                    scan.finished_at = timestamp
    
    def set_scan_result(self, scan_id: str, snapshot: Dict[str, Any]):
        """Set scan result snapshot"""
        with self._lock:
            if scan_id in self._scans:
                self._scans[scan_id].snapshot = snapshot
                self._scans[scan_id].status = ScanStatus.COMPLETED
                self._scans[scan_id].finished_at = time.time()
    
    def list_scans(self, limit: int = 50) -> List[ScanResult]:
        """List all scans with optional limit"""
        with self._lock:
            scans = list(self._scans.values())
            # Sort by started_at descending (newest first)
            scans.sort(key=lambda s: s.started_at, reverse=True)
            return scans[:limit]
    
    def cleanup_old_scans(self, max_age_hours: int = 24):
        """Remove scans older than specified hours"""
        cutoff_time = time.time() - (max_age_hours * 3600)
        
        with self._lock:
            to_remove = [
                scan_id for scan_id, scan in self._scans.items()
                if (scan.finished_at or scan.started_at) < cutoff_time
            ]
            for scan_id in to_remove:
                del self._scans[scan_id]


class CacheStore:
    """Thread-safe cache store for file snapshots"""
    
    def __init__(self, max_entries: int = 1000):
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self._max_entries = max_entries
    
    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached snapshot"""
        with self._lock:
            entry = self._cache.get(cache_key)
            if entry:
                entry.last_accessed = time.time()
                return entry.snapshot
            return None
    
    def put(self, cache_key: str, content_hash: str, snapshot: Dict[str, Any]):
        """Store snapshot in cache"""
        with self._lock:
            # Evict if cache is full
            if len(self._cache) >= self._max_entries:
                self._evict_oldest()
            
            self._cache[cache_key] = CacheEntry(
                content_hash=content_hash,
                snapshot=snapshot,
                created_at=time.time(),
                last_accessed=time.time()
            )
    
    def invalidate(self, cache_key: str):
        """Remove cache entry"""
        with self._lock:
            self._cache.pop(cache_key, None)
    
    def clear(self):
        """Clear all cache entries"""
        with self._lock:
            self._cache.clear()
    
    def is_valid(self, cache_key: str, content_hash: str) -> bool:
        """Check if an entry exists and matches the given content hash."""
        with self._lock:
            entry = self._cache.get(cache_key)
            if not entry:
                return False
            return entry.content_hash == content_hash
    
    def _evict_oldest(self):
        """Evict least recently used entry"""
        if not self._cache:
            return
        
        oldest_key = min(
            self._cache.keys(),
            key=lambda k: self._cache[k].last_accessed
        )
        del self._cache[oldest_key]
    
    def cleanup_expired(self, max_age_hours: int = 6):
        """Remove entries older than specified hours"""
        cutoff_time = time.time() - (max_age_hours * 3600)
        
        with self._lock:
            to_remove = [
                key for key, entry in self._cache.items()
                if entry.created_at < cutoff_time
            ]
            for key in to_remove:
                del self._cache[key]
    
    def get_snapshot(self, directory: str, include_paths: List[str]) -> Dict[str, str]:
        """Get cached snapshot as dict[path, content]"""
        cache_key = make_cache_key(directory, include_paths)
        cached_data = self.get(cache_key)
        
        if cached_data and 'files' in cached_data:
            # Convert from snapshot format to path->content dict
            result = {}
            for file_info in cached_data['files']:
                if file_info.get('content') is not None:
                    result[file_info['path']] = file_info['content']
            return result
        
        return {}
    
    def set_snapshot(self, directory: str, include_paths: List[str], snapshot: Dict[str, str]):
        """Set cached snapshot from dict[path, content]"""
        cache_key = make_cache_key(directory, include_paths)
        content_hash = compute_content_hash(directory, include_paths)
        
        # Convert from path->content dict to snapshot format
        files = []
        for path, content in snapshot.items():
            file_path = os.path.join(directory, path)
            if os.path.exists(file_path):
                files.append({
                    'path': path,
                    'content': content,
                    'size': len(content) if content else 0,
                    'mtime': os.path.getmtime(file_path) if os.path.exists(file_path) else time.time(),
                    'type': 'file'
                })
        
        snapshot_data = {
            'files': files,
            'timestamp': time.time(),
            'base_path': directory,
            'include_paths': include_paths
        }
        
        self.put(cache_key, content_hash, snapshot_data)


class CachedDiffEngine:
    """Thread-safe cached diff engine with separated concerns"""
    
    def __init__(self, max_cache_entries: int = 1000):
        self.scan_registry = ScanRegistry()
        self.cache_store = CacheStore(max_cache_entries)
        self.diff_engine = DiffEngine()
        self._executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="diff-scan")
        self._lock = threading.RLock()
    
    def start_scan_async(self, base_path: str, include_paths: List[str]) -> str:
        """Start asynchronous scan and return scan ID"""
        scan_id = self.scan_registry.create_scan(base_path, include_paths)
        
        # Submit scan task to thread pool
        self._executor.submit(self._execute_scan, scan_id, base_path, include_paths)
        
        return scan_id
    
    def _execute_scan(self, scan_id: str, base_path: str, include_paths: List[str]):
        """Execute scan in background thread"""
        try:
            # Update status to running
            self.scan_registry.update_scan_status(scan_id, ScanStatus.RUNNING)
            
            # Check cache first
            cache_key = make_cache_key(base_path, include_paths)
            content_hash = compute_content_hash(base_path, include_paths)
            if self.cache_store.is_valid(cache_key, content_hash):
                cached_snapshot = self.cache_store.get(cache_key)
                if cached_snapshot:
                    self.scan_registry.set_scan_result(scan_id, cached_snapshot)
                    return
            
            # Perform fresh scan
            snapshot = self._perform_scan(base_path, include_paths)
            
            # Cache the result
            self.cache_store.put(cache_key, content_hash, snapshot)
            
            # Store result
            self.scan_registry.set_scan_result(scan_id, snapshot)
            
        except Exception as e:
            self.scan_registry.update_scan_status(scan_id, ScanStatus.FAILED, str(e))
    
    def _perform_scan(self, base_path: str, include_paths: List[str]) -> Dict[str, Any]:
        """Perform the actual diff scan using the original format_output function"""
        try:
            # Use the original diff engine format_output method
            snapshot = self.diff_engine.format_output(base_path, include_paths)
            return snapshot
            
        except Exception as e:
            raise Exception(f"Scan failed: {str(e)}")
    
    def get_scan_status(self, scan_id: str) -> Optional[ScanResult]:
        """Get scan status and result"""
        return self.scan_registry.get_scan(scan_id)
    
    def get_scan_result(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Get scan result snapshot"""
        scan = self.scan_registry.get_scan(scan_id)
        if scan and scan.status == ScanStatus.COMPLETED:
            return scan.snapshot
        return None
    
    def list_scans(self) -> List[ScanResult]:
        """List all scans"""
        return self.scan_registry.list_scans()
    
    def scan_files(self, directory: str, include_paths: List[str]) -> Tuple[Dict[str, Dict[str, Any]], set]:
        """
        Scan files and return (all_files, changed_paths).
        all_files: dict[path -> {"content": str, "mtime": float}]
        changed_paths: set of paths that changed since last scan
        """
        all_files = {}
        changed_paths = set()
        
        try:
            # Get cached snapshot for comparison
            old_snapshot = self.cache_store.get_snapshot(directory, include_paths)
            
            for path in include_paths:
                file_path = os.path.join(directory, path)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        all_files[path] = {
                            "content": content,
                            "mtime": os.path.getmtime(file_path)
                        }
                        
                        # Check if changed since last scan
                        if path not in old_snapshot or old_snapshot[path] != content:
                            changed_paths.add(path)
                            
                    except (UnicodeDecodeError, IOError, OSError):
                        # Handle binary or unreadable files
                        all_files[path] = {
                            "content": None,
                            "mtime": os.path.getmtime(file_path) if os.path.exists(file_path) else 0
                        }
                        if path not in old_snapshot:
                            changed_paths.add(path)
            
            return all_files, changed_paths
            
        except Exception as e:
            # Fallback: treat all files as changed
            return all_files, set(include_paths)
    
    def create_visual_diff(self, old_snapshot: Dict[str, str], all_files: Dict[str, Dict[str, Any]], changed_paths: set) -> List[Dict[str, Any]]:
        """
        Create visual diff sections for the UI.
        Returns list of sections: [{"title": str, "files": [...], "collapsed": bool}]
        """
        sections = []
        
        if not changed_paths:
            return sections
        
        # Group files by change type
        new_files = []
        modified_files = []
        deleted_files = []
        
        # Check for new and modified files
        for path in changed_paths:
            if path in all_files:
                if path not in old_snapshot:
                    new_files.append({
                        "path": path,
                        "change_type": "added",
                        "content": all_files[path].get("content", "")
                    })
                else:
                    modified_files.append({
                        "path": path,
                        "change_type": "modified", 
                        "content": all_files[path].get("content", "")
                    })
        
        # Check for deleted files
        for path in old_snapshot:
            if path not in all_files:
                deleted_files.append({
                    "path": path,
                    "change_type": "deleted",
                    "content": ""
                })
        
        # Create sections
        if new_files:
            sections.append({
                "title": f"New Files ({len(new_files)})",
                "files": new_files,
                "collapsed": False
            })
        
        if modified_files:
            sections.append({
                "title": f"Modified Files ({len(modified_files)})",
                "files": modified_files,
                "collapsed": False
            })
        
        if deleted_files:
            sections.append({
                "title": f"Deleted Files ({len(deleted_files)})",
                "files": deleted_files,
                "collapsed": True
            })
        
        return sections
    
    def cleanup(self):
        """Cleanup old scans and cache entries"""
        self.scan_registry.cleanup_old_scans()
        self.cache_store.cleanup_expired()
    
    def shutdown(self):
        """Shutdown the engine and cleanup resources"""
        self._executor.shutdown(wait=True)
        self.cache_store.clear()


# Global instance for the application
cached_diff_engine = CachedDiffEngine()

scan_registry = cached_diff_engine.scan_registry
cache_store = cached_diff_engine.cache_store

__all__ = [
    "CachedDiffEngine",
    "cached_diff_engine",
    "scan_registry",
    "cache_store",
    "ScanStatus",
    "make_cache_key",
    "compute_content_hash",
]
