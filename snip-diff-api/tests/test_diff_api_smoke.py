# snip-diff-api/tests/test_diff_api_smoke.py
import os
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure "app" package is importable when running pytest from repo root
import sys
THIS_DIR = Path(__file__).resolve().parent
API_ROOT = THIS_DIR.parent  # snip-diff-api/
if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from app.main import app  # noqa: E402

# Create TestClient instance
client = TestClient(app)


def wait_for_status(scan_id: str, *, timeout_s: float = 15.0):
    """
    Poll the status endpoint until it returns a terminal state or timeout.
    Returns (status_string, status_payload_dict).
    """
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        r = client.get(f"/api/diff/status/{scan_id}")
        assert r.status_code == 200, f"status endpoint failed: {r.text}"
        payload = r.json()
        last = payload
        status = (payload.get("status") or "").lower()
        if status in {"completed", "failed", "cancelled"}:
            return status, payload
        time.sleep(0.2)
    pytest.fail(f"Timed out waiting for terminal status. Last payload: {last}")


def make_files(tmp_path: Path):
    a = tmp_path / "a.txt"
    b = tmp_path / "sub" / "b.txt"
    b.parent.mkdir(parents=True, exist_ok=True)
    a.write_text("hello\nworld\n", encoding="utf-8")
    b.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")
    return [str(a.relative_to(tmp_path)).replace("\\", "/"),
            str(b.relative_to(tmp_path)).replace("\\", "/")]


def test_health_endpoint():
    r = client.get("/api/health")
    assert r.status_code == 200
    j = r.json()
    assert j.get("status") == "healthy"
    assert j.get("service") == "snip-diff-api"


def test_scan_lifecycle_success(tmp_path: Path):
    include_paths = make_files(tmp_path)

    # kick off scan
    r = client.post("/api/diff/scan", json={
        "directory": str(tmp_path),
        "include_paths": include_paths,
        "scan_mode": "visual"
    })
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["success"] is True
    assert body["status"] == "started"
    scan_id = body["scan_id"]
    assert isinstance(scan_id, str) and len(scan_id) > 0

    # before completion, results should 422
    early = client.get(f"/api/diff/results/{scan_id}")
    assert early.status_code in (200, 422)  # tolerate very fast machines
    if early.status_code == 422:
        err = early.json()
        assert "Scan not completed" in err.get("detail", "")

    # poll for completion
    status, status_payload = wait_for_status(scan_id)
    assert status == "completed"
    assert status_payload["scan_id"] == scan_id
    assert status_payload["progress"] is None or 0.0 <= status_payload["progress"] <= 1.0

    # fetch results
    res = client.get(f"/api/diff/results/{scan_id}")
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["success"] is True
    assert data["scan_id"] == scan_id
    assert data["status"] == "completed"
    # sections should reflect new/modified files
    assert isinstance(data.get("sections"), list)
    # unified diff should exist (non-empty string, at least includes headers)
    udiff = data.get("unified_diff") or ""
    assert isinstance(udiff, str)
    assert "+++ b/" in udiff or "--- a/" in udiff


def test_cancel_finished_scan_rejected(tmp_path: Path):
    include_paths = make_files(tmp_path)
    r = client.post("/api/diff/scan", json={
        "directory": str(tmp_path),
        "include_paths": include_paths
    })
    scan_id = r.json()["scan_id"]
    wait_for_status(scan_id)

    # trying to cancel after finishing should 422
    cancel = client.delete(f"/api/diff/scan/{scan_id}")
    assert cancel.status_code == 422
    assert "already finished" in cancel.json().get("detail", "")


def test_invalid_directory_422(tmp_path: Path):
    bogus = tmp_path / "nope"
    r = client.post("/api/diff/scan", json={
        "directory": str(bogus),
        "include_paths": ["a.txt"]
    })
    assert r.status_code == 422
    assert "Directory not found" in r.json().get("detail", "")


def test_list_scans_has_entries(tmp_path: Path):
    include_paths = make_files(tmp_path)
    client.post("/api/diff/scan", json={
        "directory": str(tmp_path),
        "include_paths": include_paths
    })
    # don't care if it's finished yet; list should contain at least one
    r = client.get("/api/diff/scans?limit=50")
    assert r.status_code == 200
    j = r.json()
    assert j["success"] is True
    assert isinstance(j["scans"], list)
    assert len(j["scans"]) >= 1
    # status values should be lowercase per contract
    assert all(isinstance(s.get("status"), str) and s["status"] == s["status"].lower()
               for s in j["scans"])
