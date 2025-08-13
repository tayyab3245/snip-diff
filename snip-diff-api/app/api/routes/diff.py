"""
Diff operations API endpoints - Full implementation for SNIP-DIFF
"""

import os
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.cached_diff_engine import (
    scan_registry, cache_store, cached_diff_engine, ScanStatus
)
from app.core.diff_engine import format_output

router = APIRouter()

# Thread pool for background scan operations
scan_executor = ThreadPoolExecutor(max_workers=4)

class ScanRequest(BaseModel):
    """Request model for diff scan operation"""
    directory: str
    include_paths: Optional[List[str]] = None
    scan_mode: str = "fast"  # 'fast', 'complete', 'visual'

class ScanResponse(BaseModel):
    """Response model for scan initiation"""
    success: bool
    scan_id: str
    status: str
    message: Optional[str] = None

class ScanStatusResponse(BaseModel):
    """Response model for scan status check"""
    scan_id: str
    status: str
    progress: Optional[float] = None
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    error: Optional[str] = None

class DiffResultsResponse(BaseModel):
    """Response model for diff results"""
    success: bool
    scan_id: str
    status: str
    sections: Optional[List[Dict[str, Any]]] = None
    unified_diff: Optional[str] = None
    file_count: int = 0
    changed_count: int = 0

class ScanListResponse(BaseModel):
    """Response model for scan list"""
    success: bool
    scans: List[Dict[str, Any]]

class CancelResponse(BaseModel):
    """Response model for scan cancellation"""
    success: bool
    message: str

def process_scan_background(scan_id: str, directory: str, include_paths: Optional[List[str]], scan_mode: str):
    """Background task to process diff scan"""
    try:
        # Update to running
        scan_registry.update_scan(scan_id, status=ScanStatus.RUNNING, progress=0.1)
        
        # Validate directory
        if not os.path.exists(directory) or not os.path.isdir(directory):
            scan_registry.update_scan(
                scan_id,
                status=ScanStatus.FAILED,
                finished_at=time.time(),
                error="Directory not found or not accessible",
                progress=0.0
            )
            return
        
        # Convert to list if it's a set
        if isinstance(include_paths, set):
            include_paths = list(include_paths)
        elif include_paths is None:
            include_paths = []
        
        # Scan files
        scan_registry.update_scan(scan_id, progress=0.3)
        all_files, changed_paths = cached_diff_engine.scan_files(directory, include_paths)
        
        # Get previous snapshot for diff generation
        scan_registry.update_scan(scan_id, progress=0.6)
        old_snapshot = cache_store.get_snapshot(directory, include_paths)
        
        # Create visual sections
        sections = cached_diff_engine.create_visual_diff(old_snapshot, all_files, changed_paths)
        
        # Generate unified diff using preserved format_output function
        scan_registry.update_scan(scan_id, progress=0.8)
        new_snapshot = {k: v["content"] for k, v in all_files.items() if v["content"] is not None}
        unified_diff = format_output(old_snapshot, all_files)
        
        # Save snapshot for next comparison
        cache_store.set_snapshot(directory, include_paths, new_snapshot)
        
        # Complete scan
        scan_registry.update_scan(
            scan_id,
            status=ScanStatus.COMPLETED,
            finished_at=time.time(),
            progress=1.0,
            sections=sections,
            unified_diff=unified_diff,
            file_count=len(all_files),
            changed_count=len(changed_paths)
        )
        
    except Exception as e:
        # Mark scan as failed
        scan_registry.update_scan(
            scan_id,
            status=ScanStatus.FAILED,
            finished_at=time.time(),
            progress=0.0,
            error=str(e)
        )

@router.post("/scan", response_model=ScanResponse)
async def start_diff_scan(request: ScanRequest):
    """
    Start a diff scan operation for the specified directory and files.
    Returns a scan_id that can be used to check status and retrieve results.
    """
    try:
        # Validate directory exists
        if not os.path.exists(request.directory):
            raise HTTPException(status_code=422, detail="Directory not found")
        
        if not os.path.isdir(request.directory):
            raise HTTPException(status_code=422, detail="Path is not a directory")
        
        # Convert include_paths to list
        include_paths = request.include_paths or []

        # Create scan in registry (PENDING by default)
        scan_id = scan_registry.create_scan(request.directory, include_paths)
        
        # Start background processing
        scan_executor.submit(
            process_scan_background,
            scan_id,
            request.directory,
            include_paths,
            request.scan_mode
        )
        
        return ScanResponse(
            success=True,
            scan_id=scan_id,
            status="started",
            message="Scan started successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start scan: {str(e)}")

@router.get("/status/{scan_id}", response_model=ScanStatusResponse)
async def get_scan_status(scan_id: str):
    """Get the current status of a diff scan operation"""
    scan_result = scan_registry.get_scan(scan_id)
    
    if not scan_result:
        raise HTTPException(status_code=404, detail="Scan ID not found")
    
    return ScanStatusResponse(
        scan_id=scan_result.scan_id,
        status=scan_result.status.value,
        progress=scan_result.progress,
        started_at=scan_result.started_at,
        finished_at=scan_result.finished_at,
        error=scan_result.error
    )

@router.get("/results/{scan_id}", response_model=DiffResultsResponse)
async def get_scan_results(scan_id: str):
    """Get the results of a completed diff scan"""
    scan_result = scan_registry.get_scan(scan_id)
    
    if not scan_result:
        raise HTTPException(status_code=404, detail="Scan ID not found")
    
    if scan_result.status != ScanStatus.COMPLETED:
        raise HTTPException(
            status_code=422, 
            detail=f"Scan not completed. Current status: {scan_result.status}"
        )
    
    # Return sections as-is since they're already JSON-serializable dicts
    sections_dict = scan_result.sections or []
    
    return DiffResultsResponse(
        success=True,
        scan_id=scan_result.scan_id,
        status=scan_result.status.value,
        sections=sections_dict,
        unified_diff=scan_result.unified_diff,
        file_count=scan_result.file_count,
        changed_count=scan_result.changed_count
    )

@router.delete("/scan/{scan_id}", response_model=CancelResponse)
async def cancel_scan(scan_id: str):
    """Cancel a running scan operation"""
    scan_result = scan_registry.get_scan(scan_id)
    
    if not scan_result:
        raise HTTPException(status_code=404, detail="Scan ID not found")
    
    if scan_result.status in (ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED):
        raise HTTPException(status_code=422, detail="Scan already finished")
    
    # Mark as cancelled
    scan_registry.update_scan(
        scan_id,
        status=ScanStatus.CANCELLED,
        finished_at=time.time()
    )
    
    return CancelResponse(success=True, message="Scan cancelled")

@router.get("/scans", response_model=ScanListResponse)
async def list_scans(limit: int = 50):
    """List all scan operations and their status"""
    scans = scan_registry.list_scans(limit)
    
    scans_dict = [
        {
            "scan_id": scan.scan_id,
            "status": scan.status.value,
            "started_at": scan.started_at,
            "finished_at": scan.finished_at,
            "directory": scan.directory,
            "file_count": scan.file_count,
            "changed_count": scan.changed_count,
            "error": scan.error
        }
        for scan in scans
    ]
    
    return ScanListResponse(success=True, scans=scans_dict)

@router.get("/health")
async def diff_health():
    """Health check"""
    return {"status": "healthy", "module": "diff", "active_scans": len(scan_registry.list_scans())}
