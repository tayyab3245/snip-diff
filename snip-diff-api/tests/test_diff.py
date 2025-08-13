import os
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

client = TestClient(app)

def wait_for_terminal(scan_id: str, timeout_s: float = 10.0) -> str:
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        r = client.get(f"/api/diff/status/{scan_id}")
        assert r.status_code == 200, r.text
        last = r.json()
        st = (last.get("status") or "").lower()
        if st in {"completed", "failed", "cancelled"}:
            return st
        time.sleep(0.1)
    raise AssertionError(f"timeout waiting for terminal status; last={last}")

class TestDiffAPI:
    def test_diff_health(self):
        r = client.get("/api/diff/health")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "healthy"
        assert data["module"] == "diff"

    def test_scan_workflow_complete(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files for diff
            file1 = os.path.join(temp_dir, "file1.txt")
            file2 = os.path.join(temp_dir, "file2.txt")
            with open(file1, "w", encoding="utf-8") as f:
                f.write("line 1\nline 2\nline 3\n")
            with open(file2, "w", encoding="utf-8") as f:
                f.write("line 1\nline 2 modified\nline 3\nline 4\n")

            payload = {"directory": temp_dir, "include_paths": ["file1.txt", "file2.txt"], "scan_mode": "visual"}
            response = client.post("/api/diff/scan", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            scan_id = data["scan_id"]
            assert scan_id is not None

            # Status should be pending/running until completion
            response = client.get(f"/api/diff/status/{scan_id}")
            assert response.status_code == 200
            assert response.json()["scan_id"] == scan_id

            assert wait_for_terminal(scan_id) == "completed"

            # Get results (sections + unified_diff)
            response = client.get(f"/api/diff/results/{scan_id}")
            assert response.status_code == 200
            results_data = response.json()
            assert results_data["success"] == True
            assert results_data["status"] == "completed"
            assert isinstance(results_data.get("sections"), list)
            assert isinstance(results_data.get("unified_diff"), str)
            assert results_data.get("file_count", 0) >= 0

            # Check scan list (prefixed under /api)
            response = client.get("/api/diff/scans")
            assert response.status_code == 200
            scans_data = response.json()
            assert scans_data["success"] == True
            assert len(scans_data["scans"]) > 0
            scan_ids = [scan["scan_id"] for scan in scans_data["scans"]]
            assert scan_id in scan_ids
            # status strings are lowercase
            assert all(isinstance(s.get("status"), str) and s["status"] == s["status"].lower() for s in scans_data["scans"])

    def test_scan_invalid_base_path(self):
        payload = {"directory": "/nonexistent", "include_paths": ["file1.txt"]}
        response = client.post("/api/diff/scan", json=payload)
        assert response.status_code == 422

    def test_scan_empty_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = {"directory": temp_dir, "include_paths": []}
            r = client.post("/api/diff/scan", json=payload)
            assert r.status_code == 200
            scan_id = r.json()["scan_id"]
            assert wait_for_terminal(scan_id) == "completed"
            res = client.get(f"/api/diff/results/{scan_id}")
            assert res.status_code == 200
            data = res.json()
            assert data.get("file_count", 0) == 0

    def test_status_invalid_id(self):
        response = client.get("/api/diff/status/invalid-id")
        assert response.status_code == 404

    def test_results_invalid_id(self):
        response = client.get("/api/diff/results/invalid-id")
        assert response.status_code == 404

    def test_concurrent_scans(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            for i in range(5):
                test_file = os.path.join(temp_dir, f"test_{i}.txt")
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write(f"content {i}\nline 2\nline 3\n")
            
            def run_scan(index):
                payload = {"directory": temp_dir, "include_paths": [f"test_{index}.txt"]}
                response = client.post("/api/diff/scan", json=payload)
                assert response.status_code == 200
                data = response.json()
                assert data["success"] == True
                return data["scan_id"]
            
            # Run multiple scans concurrently
            scan_ids = []
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(run_scan, i) for i in range(3)]
                for future in futures:
                    scan_id = future.result()
                    scan_ids.append(scan_id)
            
            # Verify all scans have unique IDs
            assert len(scan_ids) == len(set(scan_ids))
            
            # Wait for all scans to complete
            for scan_id in scan_ids:
                st = wait_for_terminal(scan_id, timeout_s=10)
                assert st in {"completed", "failed"}
                response = client.get(f"/api/diff/status/{scan_id}")
                status_data = response.json()
                assert status_data["status"] in ["completed", "failed"]

    def test_cache_deterministic(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test file
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("test content\n")

            payload = {"directory": temp_dir, "include_paths": ["test.txt"]}
            response1 = client.post("/api/diff/scan", json=payload)
            assert response1.status_code == 200
            scan_id1 = response1.json()["scan_id"]

            assert wait_for_terminal(scan_id1, timeout_s=5) == "completed"

            # Second scan should hit cache and also complete
            response2 = client.post("/api/diff/scan", json=payload)
            assert response2.status_code == 200
            scan_id2 = response2.json()["scan_id"]

            assert wait_for_terminal(scan_id2, timeout_s=5) == "completed"

            response1 = client.get(f"/api/diff/results/{scan_id1}")
            response2 = client.get(f"/api/diff/results/{scan_id2}")
            assert response1.status_code == 200
            assert response2.status_code == 200
            data1 = response1.json()
            data2 = response2.json()
            assert data1.get("file_count") == data2.get("file_count")

if __name__ == "__main__":
    # Simple test runner
    test_instance = TestDiffAPI()
    
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
        print("All diff tests passed!")
        exit(0)
