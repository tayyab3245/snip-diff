"""
File snapshot utilities - extracted from SNIP-DIFF desktop app
Handles file scanning, loading, and saving snapshots for diff comparison
"""

import json
import os
from typing import Dict, Set, Optional

# Default ignore patterns
IGNORE_LIST = {
    "build", "dist", ".git", ".hg", ".svn",
    "node_modules", "__pycache__", ".idea", ".vscode",
    ".pytest_cache", ".mypy_cache", "venv", "env"
}

def _should_skip(path_parts, ignore_set: Set[str]) -> bool:
    """Check if path should be skipped based on ignore patterns"""
    return any(part in ignore_set for part in path_parts)

def get_all_files(
    directory: str,
    ignore_set: Set[str] = IGNORE_LIST,
    include_paths: Optional[Set[str]] = None,
) -> Dict[str, dict]:
    """
    Walk `directory`, return {relative_path: {"content": str, "mtime": float}}
    Only files whose *relative* path starts with a value in `include_paths`
    are kept when that set is provided.
    """
    files: Dict[str, dict] = {}

    for root, _, filenames in os.walk(directory):
        if _should_skip(root.split(os.sep), ignore_set):
            continue

        for filename in filenames:
            abs_path = os.path.join(root, filename)
            rel_path = os.path.relpath(abs_path, directory)

            if _should_skip(rel_path.split(os.sep), ignore_set):
                continue
            if include_paths is not None and not any(
                rel_path == p or rel_path.startswith(f"{p}{os.sep}")
                for p in include_paths
            ):
                continue

            try:
                with open(abs_path, "r", encoding="utf-8") as fh:
                    files[rel_path] = {
                        "content": fh.read(),
                        "mtime": os.path.getmtime(abs_path),
                    }
            except Exception:
                # Binary file or unreadable – skip
                pass
    return files

def load_snapshot(snapshot_file: str = ".nip_snapshot.json") -> Dict[str, str]:
    """Load snapshot from JSON file"""
    if not os.path.exists(snapshot_file):
        return {}
    try:
        with open(snapshot_file, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            # Handle both old and new snapshot formats
            if isinstance(data, dict) and 'snapshot' in data:
                return data['snapshot']
            return data
    except Exception:
        return {}

def save_snapshot(snapshot: Dict[str, dict], snapshot_file: str = ".nip_snapshot.json") -> None:
    """
    Persist snapshot in a minimal form: {path: content}.
    Modification time is only used during the current run.
    """
    cleaned = {k: v["content"] if isinstance(v, dict) else v for k, v in snapshot.items()}
    try:
        with open(snapshot_file, "w", encoding="utf-8") as fh:
            json.dump(cleaned, fh, indent=2)
    except Exception:
        pass  # Fail silently for API context
