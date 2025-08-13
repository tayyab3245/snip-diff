"""
SNIP-DIFF FastAPI Backend - Unified entrypoint for SD-003
"""

import sys
import os
import atexit
from contextlib import asynccontextmanager

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import routes
from app.api.routes import files, diff

# Cleanup function for thread pools
def cleanup_resources():
    """Cleanup thread pools and other resources on shutdown"""
    try:
        from app.api.routes.diff import scan_executor
        if scan_executor:
            scan_executor.shutdown(wait=True)
            print("Thread pool executor shutdown complete")
    except Exception as e:
        print(f"Error during cleanup: {e}")

# Register cleanup function
atexit.register(cleanup_resources)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan management for resource cleanup"""
    # Startup
    yield
    # Shutdown
    cleanup_resources()

# Create FastAPI app with lifespan management
app = FastAPI(
    title="SNIP-DIFF API",
    description="File difference detection API for SNIP-DIFF with thread-safe scanning",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS for development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:3001",  # React alternative port
        "http://localhost:5173",  # Vite dev server for Electron renderer
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001", 
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers with /api prefix for unified base path
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(diff.router, prefix="/api/diff", tags=["diff"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "SNIP-DIFF API is running", "version": "2.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "snip-diff-api"}

@app.get("/api/health")
async def api_health_check():
    """API health check endpoint"""
    return {"status": "healthy", "service": "snip-diff-api", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    print("Starting SNIP-DIFF API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
