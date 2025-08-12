"""
Tests for diff operations API endpoints
"""

import pytest
import tempfile
import os
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_diff_scan_endpoint():
    """Test the diff scan endpoint with a temporary directory"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        test_file = os.path.join(temp_dir, "test.py")
        with open(test_file, "w") as f:
            f.write("print('hello world')")
        
        # Test scan request
        request_data = {
            "directory": temp_dir,
            "include_paths": ["test.py"],
            "scan_mode": "fast"
        }
        
        response = client.post("/api/diff/scan", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "scan_id" in data
        assert data["status"] == "started"
        
        return data["scan_id"]

def test_scan_status_endpoint():
    """Test scan status endpoint"""
    # First start a scan
    scan_id = test_diff_scan_endpoint()
    
    # Check status
    response = client.get(f"/api/diff/status/{scan_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["scan_id"] == scan_id
    assert data["status"] in ["started", "running", "completed"]

def test_scan_invalid_directory():
    """Test scan with invalid directory"""
    request_data = {
        "directory": "/nonexistent/path",
        "scan_mode": "fast"
    }
    
    response = client.post("/api/diff/scan", json=request_data)
    
    assert response.status_code == 404

def test_scan_status_invalid_id():
    """Test status check with invalid scan ID"""
    response = client.get("/api/diff/status/invalid-scan-id")
    
    assert response.status_code == 404

def test_list_scans_endpoint():
    """Test list scans endpoint"""
    response = client.get("/api/diff/scans")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "scans" in data
    assert isinstance(data["scans"], list)
