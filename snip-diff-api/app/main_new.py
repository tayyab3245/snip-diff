"""
SNIP-DIFF FastAPI Backend - Simplified startup
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import routes
from app.api.routes import files, diff

# Create FastAPI app
app = FastAPI(
    title="SNIP-DIFF API",
    description="File difference detection API for SNIP-DIFF",
    version="1.0.0"
)

# Configure CORS for Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, be more specific
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(diff.router, prefix="/api/diff", tags=["diff"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "SNIP-DIFF API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "snip-diff-api"}

if __name__ == "__main__":
    import uvicorn
    print("Starting SNIP-DIFF API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
