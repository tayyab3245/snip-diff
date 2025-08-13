import json
import tempfile
import os
from fastapi.testclient import TestClient

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

class TestFilesAPI:
    def test_files_health(self):
        response = client.get("/api/files/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["module"] == "files"

    def test_file_tree_basic(self):
        """Test basic file tree functionality"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("test content")
            
            test_dir = os.path.join(temp_dir, "subdir")
            os.makedirs(test_dir)
            
            # Test valid directory
            response = client.get(f"/api/files/tree?path={temp_dir}")
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] == True
            assert data["path"] == temp_dir
            assert data["total_files"] >= 1
            assert data["total_directories"] >= 1
            
            # Check nodes
            node_names = [node["name"] for node in data["nodes"]]
            assert "test.txt" in node_names
            assert "subdir" in node_names

    def test_file_tree_with_limit(self):
        """limit applies to total traversed items, root nodes count stays <= limit in flat roots"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create many test files
            for i in range(10):
                test_file = os.path.join(temp_dir, f"test_{i}.txt")
                with open(test_file, "w") as f:
                    f.write(f"test content {i}")
            
            # Test with limit
            response = client.get(f"/api/files/tree?path={temp_dir}&limit=5")
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] == True
            assert len(data["nodes"]) <= 5

    def test_file_tree_invalid_path(self):
        """Test file tree with invalid path"""
        response = client.get("/api/files/tree?path=/nonexistent")
        assert response.status_code == 404

    def test_file_tree_not_directory(self):
        """Test file tree with file instead of directory"""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"test")
            temp_file_path = temp_file.name
        
        try:
            response = client.get(f"/api/files/tree?path={temp_file_path}")
            assert response.status_code == 422
        finally:
            os.unlink(temp_file_path)

    def test_file_validation(self):
        """Test file validation endpoint"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("test content")
            
            binary_file = os.path.join(temp_dir, "binary.bin")
            with open(binary_file, "wb") as f:
                f.write(b'\x00\x01\x02\x03')
            
            payload = {
                "base_path": temp_dir,
                "paths": ["test.txt", "binary.bin", "nonexistent.txt"]
            }
            
            response = client.post("/api/files/validate", json=payload)
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] == True
            assert "test.txt" in data["valid_paths"]
            assert "binary.bin" in data["valid_paths"]
            assert "nonexistent.txt" in data["invalid_paths"]
            assert "test.txt" in data["readable_files"]

    def test_file_validation_invalid_base(self):
        """Test file validation with invalid base path"""
        payload = {
            "base_path": "/nonexistent",
            "paths": ["test.txt"]
        }
        
        response = client.post("/api/files/validate", json=payload)
        assert response.status_code == 404

    def test_file_validation_directory_traversal(self):
        """Test file validation prevents directory traversal"""
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = {
                "base_path": temp_dir,
                "paths": ["../../../etc/passwd"]
            }
            
            response = client.post("/api/files/validate", json=payload)
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] == True
            assert "../../../etc/passwd" in data["invalid_paths"]

    def test_file_info_text_file(self):
        """Test file info for text file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test file
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("test content for preview\nline 2\nline 3")
            
            response = client.get(f"/api/files/info?base_path={temp_dir}&path=test.txt")
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] == True
            assert data["name"] == "test.txt"
            assert data["is_file"] == True
            assert data["is_directory"] == False
            assert data["is_text"] == True
            assert "test content" in data["content_preview"]
            assert data["size"] > 0
            assert data["modified"] is not None

    def test_file_info_directory(self):
        """Test file info for directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = os.path.join(temp_dir, "testdir")
            os.makedirs(test_dir)
            
            response = client.get(f"/api/files/info?base_path={temp_dir}&path=testdir")
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] == True
            assert data["name"] == "testdir"
            assert data["is_file"] == False
            assert data["is_directory"] == True
            assert data["is_text"] == False
            assert data["content_preview"] is None
            assert data["size"] is None

    def test_file_info_binary_file(self):
        """Test file info for binary file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create binary file
            binary_file = os.path.join(temp_dir, "binary.bin")
            with open(binary_file, "wb") as f:
                f.write(b'\x00\x01\x02\x03\x04\x05')
            
            response = client.get(f"/api/files/info?base_path={temp_dir}&path=binary.bin")
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] == True
            assert data["name"] == "binary.bin"
            assert data["is_file"] == True
            assert data["is_text"] == False
            assert data["content_preview"] is None

    def test_file_info_invalid_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            response = client.get(f"/api/files/info?base_path={temp_dir}&path=nonexistent.txt")
            assert response.status_code == 404

    def test_file_info_directory_traversal(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            response = client.get(f"/api/files/info?base_path={temp_dir}&path=../../../etc/passwd")
            assert response.status_code == 422

if __name__ == "__main__":
    # Simple test runner
    test_instance = TestFilesAPI()
    
    test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        try:
            print(f"Running {method_name}...")
            method = getattr(test_instance, method_name)
            method()
            print(f"✓ {method_name} passed")
            passed += 1
        except Exception as e:
            print(f"✗ {method_name} failed: {e}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    if failed > 0:
        exit(1)
    else:
        print("All files tests passed!")
        exit(0)
