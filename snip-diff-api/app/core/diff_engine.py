"""
Core diff engine functionality - extracted from SNIP-DIFF desktop app
Provides unified diff generation with full context for AI consumption
"""

import difflib
import os
from typing import Dict, List

def _diff_lines(path: str, old: str, new: str) -> List[str]:
    """
    Return a unified diff for one file where *all* unchanged lines are kept.
    We do this by making the context size equal to the longer file length.
    For very large files, we limit context to prevent memory issues.
    """
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    max_lines = max(len(old_lines), len(new_lines))
    
    # Limit context for very large files to prevent memory issues
    ctx = min(max_lines, 10000)  # Cap at 10k lines context
    
    return list(difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=os.path.join("a", path),
        tofile=os.path.join("b", path),
        lineterm="",
        n=ctx
    ))

def format_output(old_snap: Dict[str, str], new_snap: Dict[str, dict]) -> str:
    """
    Build one big, GPT-friendly unified diff.
      • Deleted files → full body prefixed with "-"
      • Brand-new files → full body prefixed with "+"
      • Modified files → full diff with every line shown
      • Unchanged files → full body prefixed with " " (space)
    """
    output: List[str] = []

    all_paths = set(old_snap) | set(new_snap)
    # newest-modified first, then alpha
    sorted_paths = sorted(
        all_paths,
        key=lambda p: (-new_snap.get(p, {}).get("mtime", 0), p)
    )

    for path in sorted_paths:
        old_content = old_snap.get(path, "")
        new_entry   = new_snap.get(path)
        new_content = None if new_entry is None else new_entry["content"]

        # ---------- deleted file --------------------------------------
        if new_content is None:
            output.extend(_diff_lines(path, old_content, ""))
            continue

        # ---------- brand-new file ------------------------------------
        if not old_content:
            hdr  = [f"--- a/{path}", f"+++ b/{path}"]
            body = [f"+{ln}" if ln else "+" for ln in new_content.splitlines()]
            output.extend(hdr + body)
            continue

        # ---------- unchanged file ------------------------------------
        if old_content == new_content:
            hdr  = [f"--- a/{path}", f"+++ b/{path}"]
            body = [f" {ln}" for ln in new_content.splitlines()]
            output.extend(hdr + body)
            continue

        # ---------- modified file -------------------------------------
        output.extend(_diff_lines(path, old_content, new_content))

    return "\n".join(output)


class DiffEngine:
    """Simple wrapper class for the diff functionality"""
    
    def format_output(self, base_path: str, include_paths: List[str]) -> Dict[str, any]:
        """
        Format output in the expected snapshot format for the API.
        This method creates a snapshot of files for diff processing.
        """
        import time
        
        snapshot = {
            "files": [],
            "timestamp": time.time(),
            "base_path": base_path,
            "include_paths": include_paths
        }
        
        for rel_path in include_paths:
            file_path = os.path.join(base_path, rel_path)
            
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    file_info = {
                        "path": rel_path,
                        "content": content,
                        "size": len(content),
                        "mtime": os.path.getmtime(file_path),
                        "type": "file"
                    }
                    snapshot["files"].append(file_info)
                    
                except (UnicodeDecodeError, IOError):
                    # Handle binary or unreadable files
                    file_info = {
                        "path": rel_path,
                        "content": None,
                        "size": os.path.getsize(file_path),
                        "mtime": os.path.getmtime(file_path),
                        "type": "binary"
                    }
                    snapshot["files"].append(file_info)
            
            elif os.path.isdir(file_path):
                # Handle directories
                file_info = {
                    "path": rel_path,
                    "content": None,
                    "size": 0,
                    "mtime": os.path.getmtime(file_path),
                    "type": "directory"
                }
                snapshot["files"].append(file_info)
        
        return snapshot
