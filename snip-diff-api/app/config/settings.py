"""
Configuration settings for SNIP-DIFF API
"""

import os
from typing import Set

class Settings:
    """Application settings"""
    
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "SNIP-DIFF API"
    VERSION: str = "1.0.0"
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "file://",
        "*"  # Development only
    ]
    
    # File Processing
    SNAPSHOT_FILE: str = ".nip_snapshot.json"
    IGNORE_LIST: Set[str] = {
        "build", "dist", ".git", ".hg", ".svn",
        "node_modules", "__pycache__", ".idea", ".vscode",
        ".pytest_cache", ".mypy_cache", "venv", "env"
    }
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # File size limits
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    MAX_FILES_PER_SCAN: int = 10000

# Global settings instance
settings = Settings()
