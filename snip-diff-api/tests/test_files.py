"""
Tests for file operations API endpoints
"""

import pytest
import tempfile
import os
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_file_tree_endpoint():
    """Test the file tree endpoint with a temporary directory"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some test files
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")
        
        # Create subdirectory
        sub_dir = os.path.join(temp_dir, "subdir")
        os.makedirs(sub_dir)
        
        sub_file = os.path.join(sub_dir, "sub.txt")
        with open(sub_file, "w") as f:
            f.write("sub content")
        
        # Test the endpoint
        response = client.get(f"/api/files/tree?path={temp_dir}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["path"] == temp_dir
        assert len(data["nodes"]) >= 2  # test.txt and subdir
        assert data["total_files"] >= 2
        assert data["total_directories"] >= 1

def test_file_tree_invalid_path():
    """Test file tree endpoint with invalid path"""
    response = client.get("/api/files/tree?path=/nonexistent/path")
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()

def test_file_validation_endpoint():
    """Test file validation endpoint"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        test_file = os.path.join(temp_dir, "valid.txt")
        with open(test_file, "w") as f:
            f.write("valid content")
        
        # Test validation
        request_data = {
            "paths": ["valid.txt", "nonexistent.txt"],
            "base_path": temp_dir
        }
        
        response = client.post("/api/files/validate", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "valid.txt" in data["valid_paths"]
        assert "nonexistent.txt" in data["invalid_paths"]
        assert len(data["readable_files"]) >= 1

def test_file_info_endpoint():
    """Test file info endpoint"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test file
        test_file = os.path.join(temp_dir, "info.txt")
        test_content = "test file content"
        with open(test_file, "w") as f:
            f.write(test_content)
        
        # Test file info
        response = client.get(f"/api/files/info?path=info.txt&base_path={temp_dir}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["path"] == "info.txt"
        assert data["name"] == "info.txt"
        assert data["is_file"] is True
        assert data["is_directory"] is False
        assert data["is_text"] is True
        assert test_content in data["content_preview"]
