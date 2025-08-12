"""
Diff operations API endpoints - Simplified version for SNIP-DIFF
"""

import os
import time
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter()

class ScanRequest(BaseModel):
    """Request model for diff scan operation"""
    directory: str
    scan_mode: str = "fast"  # 'fast', 'complete'

class ScanResponse(BaseModel):
    """Response model for scan operation"""
    success: bool
    directory: str
    file_count: int
    message: str

@router.post("/scan", response_model=ScanResponse)
async def scan_directory(request: ScanRequest):
    """
    Scan directory for files - simplified version
    """
    try:
        # Validate directory exists
        if not os.path.exists(request.directory):
            raise HTTPException(status_code=404, detail="Directory not found")
        
        if not os.path.isdir(request.directory):
            raise HTTPException(status_code=400, detail="Path is not a directory")
        
        # Simple file count
        file_count = 0
        for root, dirs, files in os.walk(request.directory):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            file_count += len(files)
            
            # Limit for performance
            if file_count > 1000:
                break
        
        return ScanResponse(
            success=True,
            directory=request.directory,
            file_count=file_count,
            message=f"Scanned {file_count} files in directory"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scan: {str(e)}")

@router.get("/health")
async def diff_health():
    """Health check"""
    return {"status": "healthy", "module": "diff"}
