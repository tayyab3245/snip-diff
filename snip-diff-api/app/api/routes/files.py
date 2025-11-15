"""
File operations API endpoints - Complete implementation for SNIP-DIFF
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

class ValidateRequest(BaseModel):
    """Request for file validation"""
    base_path: str
    paths: List[str]

class ValidateResponse(BaseModel):
    """Response for file validation"""
    success: bool
    valid_paths: List[str]
    invalid_paths: List[str]
    readable_files: List[str]

class FileInfoResponse(BaseModel):
    """Response for file info"""
    success: bool
    path: str
    name: str
    is_file: bool
    is_directory: bool
    size: Optional[int] = None
    modified: Optional[float] = None
    is_text: bool = False
    content_preview: Optional[str] = None

def should_ignore_path(path: str) -> bool:
    """Check if path should be ignored"""
    path_parts = path.split(os.sep)
    return any(part in IGNORE_LIST for part in path_parts)

def is_text_file(file_path: str) -> bool:
    """Check if a file is likely a text file"""
    try:
        # Check common text file extensions
        text_extensions = {
            '.txt', '.py', '.js', '.ts', '.html', '.css', '.json', '.xml',
            '.md', '.rst', '.yml', '.yaml', '.ini', '.cfg', '.conf',
            '.sh', '.bat', '.ps1', '.sql', '.c', '.cpp', '.h', '.hpp',
            '.java', '.cs', '.php', '.rb', '.go', '.rs', '.swift',
            '.kt', '.scala', '.clj', '.hs', '.elm', '.vue', '.jsx',
            '.tsx', '.sass', '.scss', '.less', '.styl'
        }
        
        _, ext = os.path.splitext(file_path.lower())
        if ext in text_extensions:
            return True
        
        # Try to read first few bytes to detect binary
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:  # Null bytes indicate binary
                return False
            
        # Try to decode as text
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(100)  # Read small chunk
            return True
            
    except (UnicodeDecodeError, PermissionError, OSError):
        return False

def build_tree_recursive(base_path: str, current_path: str, max_depth: int, current_depth: int, total_counts: dict) -> List[FileNode]:
    """Build file tree recursively with depth limiting"""
    nodes = []
    
    if current_depth >= max_depth:
        return nodes
    
    try:
        items = sorted(os.listdir(current_path))
        
        for item in items:
            if total_counts.get("total", 0) >= total_counts.get("limit", 1000):
                break
                
            item_path = os.path.join(current_path, item)
            rel_path = os.path.relpath(item_path, base_path).replace("\\", "/")
            
            if should_ignore_path(rel_path):
                continue
            
            try:
                stat = os.stat(item_path)
                total_counts["total"] = total_counts.get("total", 0) + 1
                
                if os.path.isdir(item_path):
                    # Build directory node with children
                    children = build_tree_recursive(
                        base_path, 
                        item_path, 
                        max_depth, 
                        current_depth + 1, 
                        total_counts
                    )
                    
                    node = FileNode(
                        path=rel_path,
                        name=item,
                        type='directory',
                        children=children if children else None
                    )
                    nodes.append(node)
                    total_counts["directories"] = total_counts.get("directories", 0) + 1
                    
                else:
                    node = FileNode(
                        path=rel_path,
                        name=item,
                        type='file',
                        size=stat.st_size,
                        modified=stat.st_mtime
                    )
                    nodes.append(node)
                    total_counts["files"] = total_counts.get("files", 0) + 1
                    
            except (PermissionError, OSError):
                continue
                
    except (PermissionError, OSError):
        pass
    
    return nodes

def build_simple_tree(directory: str, max_depth: int = 3) -> List[FileNode]:
    """Simple wrapper for recursive tree building - for testing"""
    total_counts = {"files": 0, "directories": 0, "total": 0, "limit": 1000}
    return build_tree_recursive(directory, directory, max_depth, 0, total_counts)

@router.get("/tree", response_model=FileTreeResponse)
async def get_file_tree(
    path: str = Query(..., description="Directory path to scan"),
    limit: int = Query(500, description="Maximum number of total items to return"),
    max_depth: int = Query(3, description="Maximum depth to traverse")
):
    """Get recursive file tree for directory"""
    try:
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Directory not found")
        
        if not os.path.isdir(path):
            raise HTTPException(status_code=422, detail="Path is not a directory")
        
        # Track counts during traversal
        total_counts = {
            "total": 0,
            "files": 0,
            "directories": 0,
            "limit": limit
        }
        
        # Build recursive tree
        nodes = build_tree_recursive(path, path, max_depth, 0, total_counts)
        
        return FileTreeResponse(
            success=True,
            path=path,
            nodes=nodes,
            total_files=total_counts["files"],
            total_directories=total_counts["directories"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/validate", response_model=ValidateResponse)
async def validate_files(request: ValidateRequest):
    """Validate file paths and check readability"""
    try:
        if not os.path.exists(request.base_path):
            raise HTTPException(status_code=404, detail="Base path not found")
        
        if not os.path.isdir(request.base_path):
            raise HTTPException(status_code=422, detail="Base path is not a directory")
        
        valid_paths = []
        invalid_paths = []
        readable_files = []
        
        for rel_path in request.paths:
            abs_path = os.path.join(request.base_path, rel_path)
            
            # Normalize path to prevent directory traversal
            abs_path = os.path.abspath(abs_path)
            base_abs = os.path.abspath(request.base_path)
            
            if not abs_path.startswith(base_abs):
                invalid_paths.append(rel_path)
                continue
            
            if os.path.exists(abs_path):
                valid_paths.append(rel_path)
                
                # Check if it's a readable file
                if os.path.isfile(abs_path):
                    try:
                        with open(abs_path, 'r', encoding='utf-8') as f:
                            f.read(100)  # Try to read a small chunk
                        readable_files.append(rel_path)
                    except (UnicodeDecodeError, PermissionError, OSError):
                        # Try latin-1 as fallback
                        try:
                            with open(abs_path, 'r', encoding='latin-1') as f:
                                f.read(100)
                            readable_files.append(rel_path)
                        except (PermissionError, OSError):
                            pass  # File exists but not readable
            else:
                invalid_paths.append(rel_path)
        
        return ValidateResponse(
            success=True,
            valid_paths=valid_paths,
            invalid_paths=invalid_paths,
            readable_files=readable_files
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")

@router.get("/info", response_model=FileInfoResponse)
async def get_file_info(
    base_path: str = Query(..., description="Base directory path"),
    path: str = Query(..., description="Relative file/directory path")
):
    """Get detailed information about a file or directory"""
    try:
        abs_path = os.path.join(base_path, path)
        
        # Normalize path to prevent directory traversal
        abs_path = os.path.abspath(abs_path)
        base_abs = os.path.abspath(base_path)
        
        if not abs_path.startswith(base_abs):
            raise HTTPException(status_code=422, detail="Invalid path")
        
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=404, detail="Path not found")
        
        stat = os.stat(abs_path)
        is_file = os.path.isfile(abs_path)
        is_directory = os.path.isdir(abs_path)
        name = os.path.basename(abs_path)
        
        # Initialize response
        response = FileInfoResponse(
            success=True,
            path=path,
            name=name,
            is_file=is_file,
            is_directory=is_directory,
            size=stat.st_size if is_file else None,
            modified=stat.st_mtime,
            is_text=False
        )
        
        # If it's a file, check if it's text and get preview
        if is_file:
            response.is_text = is_text_file(abs_path)
            
            if response.is_text:
                try:
                    with open(abs_path, 'r', encoding='utf-8') as f:
                        content = f.read(500)  # First 500 characters
                        response.content_preview = content
                except (UnicodeDecodeError, PermissionError, OSError):
                    try:
                        with open(abs_path, 'r', encoding='latin-1') as f:
                            content = f.read(500)
                            response.content_preview = content
                    except (PermissionError, OSError):
                        response.content_preview = None
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting file info: {str(e)}")

@router.get("/health")
async def files_health():
    """Health check"""
    return {"status": "healthy", "module": "files"}

class FileContentResponse(BaseModel):
    """Response for file content endpoint"""
    success: bool
    path: str
    content: str
    size: int
    encoding: str

@router.get("/content", response_model=FileContentResponse)
async def get_file_content(
    base_path: str = Query(..., description="Base directory path"),
    path: str = Query(..., description="Relative file path")
):
    """Get full content of a text file"""
    try:
        abs_path = os.path.join(base_path, path)
        
        # Normalize path to prevent directory traversal
        abs_path = os.path.abspath(abs_path)
        base_abs = os.path.abspath(base_path)
        
        if not abs_path.startswith(base_abs):
            raise HTTPException(status_code=422, detail="Invalid path")
        
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        if not os.path.isfile(abs_path):
            raise HTTPException(status_code=422, detail="Path is not a file")
        
        stat = os.stat(abs_path)
        
        # Try to read with UTF-8 first
        encoding = 'utf-8'
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Fallback to latin-1
            encoding = 'latin-1'
            with open(abs_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        return FileContentResponse(
            success=True,
            path=path,
            content=content,
            size=stat.st_size,
            encoding=encoding
        )
        
    except HTTPException:
        raise
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

# Allow forward references
FileNode.model_rebuild()
