"""
File operations API endpoints - Simplified version for SNIP-DIFF
"""

import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter()

IGNORE_LIST = {
    "build", "dist", ".git", ".hg", ".svn",
    "node_modules", "__pycache__", ".idea", ".vscode"
}

class FileNode(BaseModel):
    """File or directory node"""
    path: str
    name: str
    type: str  # 'file' or 'directory'
    size: Optional[int] = None
    modified: Optional[float] = None
    children: Optional[List['FileNode']] = None

class FileTreeResponse(BaseModel):
    """Response for file tree endpoint"""
    success: bool
    path: str
    nodes: List[FileNode]
    total_files: int
    total_directories: int

def should_ignore_path(path: str) -> bool:
    """Check if path should be ignored"""
    path_parts = path.split(os.sep)
    return any(part in IGNORE_LIST for part in path_parts)

@router.get("/tree", response_model=FileTreeResponse)
async def get_file_tree(path: str = Query(..., description="Directory path to scan")):
    """Get file tree for directory"""
    try:
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Directory not found")
        
        if not os.path.isdir(path):
            raise HTTPException(status_code=400, detail="Path is not a directory")
        
        nodes = []
        total_files = 0
        total_directories = 0
        
        try:
            items = sorted(os.listdir(path))
            
            for item in items[:50]:  # Limit to 50 items for performance
                item_path = os.path.join(path, item)
                rel_path = os.path.relpath(item_path, path)
                
                if should_ignore_path(rel_path):
                    continue
                
                try:
                    stat = os.stat(item_path)
                    if os.path.isdir(item_path):
                        nodes.append(FileNode(
                            path=rel_path.replace("\\", "/"),
                            name=item,
                            type='directory'
                        ))
                        total_directories += 1
                    else:
                        nodes.append(FileNode(
                            path=rel_path.replace("\\", "/"),
                            name=item,
                            type='file',
                            size=stat.st_size,
                            modified=stat.st_mtime
                        ))
                        total_files += 1
                except (PermissionError, OSError):
                    continue
                    
        except PermissionError:
            raise HTTPException(status_code=403, detail="Permission denied")
        
        return FileTreeResponse(
            success=True,
            path=path,
            nodes=nodes,
            total_files=total_files,
            total_directories=total_directories
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/health")
async def files_health():
    """Health check"""
    return {"status": "healthy", "module": "files"}

# Allow forward references
FileNode.model_rebuild()
