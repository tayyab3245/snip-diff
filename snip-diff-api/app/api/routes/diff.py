"""
Diff operations API endpoints - Git-based implementation
"""

import os
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.git_diff_engine import git_diff_engine

router = APIRouter()

class ScanRequest(BaseModel):
    """Request model for diff scan operation"""
    directory: str
    include_paths: Optional[List[str]] = None
    context_lines: Optional[int] = 3

class ScanResponse(BaseModel):
    """Response model for scan results"""
    success: bool
    sections: Optional[List[Dict[str, Any]]] = None
    file_count: int = 0
    changed_count: int = 0
    error: Optional[str] = None

@router.post("/scan", response_model=ScanResponse)
async def get_diff(request: ScanRequest):
    """
    Get Git diff for the specified directory and files.
    Returns diff sections immediately using Git.
    """
    try:
        # Validate directory exists
        if not os.path.exists(request.directory):
            raise HTTPException(status_code=422, detail="Directory not found")
        
        if not os.path.isdir(request.directory):
            raise HTTPException(status_code=422, detail="Path is not a directory")
        
        # Get diff from Git
        result = git_diff_engine.get_diff(
            directory=request.directory,
            file_paths=request.include_paths,
            context_lines=request.context_lines or 3
        )
        
        if not result.get('success'):
            return ScanResponse(
                success=False,
                error=result.get('error', 'Unknown error'),
                file_count=0,
                changed_count=0
            )
        
        return ScanResponse(
            success=True,
            sections=result.get('sections', []),
            file_count=result.get('file_count', 0),
            changed_count=result.get('changed_count', 0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get diff: {str(e)}")

@router.get("/health")
async def diff_health():
    """Health check"""
    return {
        "status": "healthy", 
        "module": "diff", 
        "git_available": git_diff_engine.git_available
    }
