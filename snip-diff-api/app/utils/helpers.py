"""
Utility functions for SNIP-DIFF API
"""

import os
import hashlib
from typing import List, Set

def normalize_path(path: str) -> str:
    """Normalize file path for cross-platform compatibility"""
    return os.path.normpath(path).replace("\\", "/")

def generate_file_hash(content: str) -> str:
    """Generate SHA-256 hash for file content"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove or replace dangerous characters
    dangerous_chars = '<>:"/\\|?*'
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    return filename

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def validate_paths(paths: List[str], base_path: str) -> List[str]:
    """Validate that paths are within the base directory"""
    valid_paths = []
    base_abs = os.path.abspath(base_path)
    
    for path in paths:
        if os.path.isabs(path):
            abs_path = path
        else:
            abs_path = os.path.abspath(os.path.join(base_path, path))
        
        # Check if path is within base directory
        if abs_path.startswith(base_abs):
            valid_paths.append(path)
    
    return valid_paths
