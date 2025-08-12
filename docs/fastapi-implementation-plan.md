# SNIP-DIFF FastAPI Backend Implementation Plan

## Project Structure
```
snip-diff-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry
│   ├── core/                   # Existing logic (copied)
│   │   ├── cached_diff_engine.py
│   │   ├── fast_diff_worker.py
│   │   ├── diff_engine.py
│   │   └── snapshot.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── diff.py         # /api/diff endpoints
│   │   │   ├── files.py        # /api/files endpoints
│   │   │   └── websocket.py    # /ws for real-time
│   │   └── models.py           # Pydantic models
│   ├── config/
│   │   ├── settings.py         # App configuration
│   │   └── theme.py            # Theme management
│   └── utils/
│       ├── file_watcher.py     # File system monitoring
│       └── background_tasks.py # Async task management
├── requirements.txt
├── Dockerfile                  # For easy deployment
└── README.md
```

## Key API Endpoints Design

### 1. File Management
```python
# GET /api/files/tree?path=/project/path
# POST /api/files/select
# GET /api/files/content?path=file.py
```

### 2. Diff Operations  
```python
# POST /api/diff/scan
# GET /api/diff/results/{scan_id}
# POST /api/diff/copy  # Copy with instructions
```

### 3. Real-time Updates
```python
# WebSocket /ws/live-updates
# WebSocket /ws/file-changes
```

### 4. Configuration
```python
# GET /api/config/themes
# POST /api/config/settings
# GET /api/config/preferences
```

## Sample FastAPI Implementation

```python
# app/main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import diff, files
from app.core.cached_diff_engine import CachedDiffEngine

app = FastAPI(
    title="SNIP-DIFF API",
    description="AI workflow tool for preparing code context",
    version="2.0.0"
)

# Enable CORS for Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Electron dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core engine
diff_engine = CachedDiffEngine()

# Include API routes
app.include_router(diff.router, prefix="/api/diff", tags=["diff"])
app.include_router(files.router, prefix="/api/files", tags=["files"])

@app.websocket("/ws/live-updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Real-time file change notifications
    # Reuse existing LiveWatcher logic
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

```python
# app/api/routes/diff.py
from fastapi import APIRouter, BackgroundTasks
from app.core.fast_diff_worker import FastDiffWorker
from app.api.models import DiffRequest, DiffResponse

router = APIRouter()

@router.post("/scan", response_model=DiffResponse)
async def scan_differences(
    request: DiffRequest,
    background_tasks: BackgroundTasks
):
    """Trigger diff scan - reuses existing FastDiffWorker logic"""
    # Convert your existing worker to async FastAPI background task
    worker = FastDiffWorker(
        root=request.project_path,
        include_paths=request.selected_files,
        callback=lambda result: None,  # Handle via background tasks
        scan_id=request.scan_id,
        is_user_action=True
    )
    
    background_tasks.add_task(run_diff_scan, worker)
    
    return DiffResponse(
        scan_id=request.scan_id,
        status="started",
        message="Diff scan initiated"
    )

@router.get("/results/{scan_id}")
async def get_diff_results(scan_id: int):
    """Get diff results - reuses existing caching"""
    # Use your existing cached_diff_engine
    pass
```
