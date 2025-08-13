#!/usr/bin/env python3
"""
SD-003 Validation Test Suite
Tests for "Align API/Engine Contracts, Unify Prefixes, Recursive File Tree, and Hardening"
"""

import os
import sys
import asyncio
import tempfile
import shutil
import time
from pathlib import Path

# Add project paths for testing
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'snip-diff-api'))

def test_unified_api_imports():
    """Ensure critical imports succeed (pytest-style)."""
    from fastapi import FastAPI  # noqa: F401
    from fastapi.middleware.cors import CORSMiddleware  # noqa: F401
    from app.main import cleanup_resources  # noqa: F401
    from app.api.routes import files, diff  # noqa: F401

def test_api_base_paths():
    """All router paths should be relative; main.py adds the /api prefix."""
    from app.api.routes.files import router as files_router
    from app.api.routes.diff import router as diff_router
    files_routes = [route.path for route in files_router.routes if hasattr(route, "path")]
    diff_routes  = [route.path for route in diff_router.routes  if hasattr(route, "path")]
    assert all(not p.startswith("/api") for p in files_routes + diff_routes), (
        f"Found absolute paths: {files_routes + diff_routes}"
    )

def test_scan_status_enum():
    """Enum must include the canonical lowercase lifecycle values."""
    from app.core.cached_diff_engine import ScanStatus
    required = {"pending", "running", "completed", "failed", "cancelled"}
    actual   = {s.value for s in ScanStatus}
    assert required <= actual, f"Missing: {required - actual}"

def test_scan_result_fields():
    """ScanResult must expose the agreed fields; progress uses 0..1 semantics."""
    from app.core.cached_diff_engine import ScanResult, ScanStatus
    result = ScanResult(
        scan_id="test-123",
        status=ScanStatus.COMPLETED,
        directory="./test",
        include_paths=["file1.py"],
        started_at=1234567890.0,
        finished_at=1234567890.0,
        progress=0.5,
        sections=[],
        unified_diff="",
    )
    for f in ("scan_id","status","directory","include_paths","started_at","finished_at","progress","sections","unified_diff"):
        assert hasattr(result, f), f"Missing field {f}"
    assert 0.0 <= result.progress <= 1.0

def test_recursive_file_tree(tmp_path):
    """Depth limiting must be monotonic (deeper depth ⇒ >= nodes)."""
    (tmp_path/"level1"/"level2"/"level3").mkdir(parents=True)
    (tmp_path/"root.txt").write_text("root")
    (tmp_path/"level1"/"file1.txt").write_text("l1")
    (tmp_path/"level1"/"level2"/"file2.txt").write_text("l2")
    (tmp_path/"level1"/"level2"/"level3"/"file3.txt").write_text("l3")
    from app.api.routes.files import build_simple_tree
    d1 = build_simple_tree(str(tmp_path), max_depth=1)
    d2 = build_simple_tree(str(tmp_path), max_depth=2)
    d3 = build_simple_tree(str(tmp_path), max_depth=3)
    assert len(d3) >= len(d2) >= len(d1)


def _flatten_count(nodes):
    """
    Count all nodes recursively (files and directories).
    Works with Pydantic FileNode objects that may have `children=None`.
    """
    total = 0
    stack = list(nodes)
    while stack:
        n = stack.pop()
        total += 1
        kids = getattr(n, "children", None) or []
        stack.extend(kids)
    return total


def _contains_path(nodes, target: str) -> bool:
    """Return True if any node (at any depth) has path == target."""
    stack = list(nodes)
    while stack:
        n = stack.pop()
        if getattr(n, "path", None) == target:
            return True
        kids = getattr(n, "children", None) or []
        stack.extend(kids)
    return False


def test_recursive_file_tree_strict(tmp_path):
    """
    Depth limiting must control visibility of deeper descendants:
      - depth=2 shows level2 dir but not its contents
      - depth=3 includes file2.txt but not level3 contents
      - depth=4 includes file3.txt
    Also, total node counts should be monotonic as depth increases.
    """
    (tmp_path / "level1" / "level2" / "level3").mkdir(parents=True)
    (tmp_path / "root.txt").write_text("root", encoding="utf-8")
    (tmp_path / "level1" / "file1.txt").write_text("l1", encoding="utf-8")
    (tmp_path / "level1" / "level2" / "file2.txt").write_text("l2", encoding="utf-8")
    (tmp_path / "level1" / "level2" / "level3" / "file3.txt").write_text("l3", encoding="utf-8")

    from app.api.routes.files import build_simple_tree

    d2 = build_simple_tree(str(tmp_path), max_depth=2)
    d3 = build_simple_tree(str(tmp_path), max_depth=3)
    d4 = build_simple_tree(str(tmp_path), max_depth=4)

    assert _flatten_count(d4) >= _flatten_count(d3) >= _flatten_count(d2)
    # At depth=2, we see level2 dir but not its contents
    assert _contains_path(d2, "level1/level2")
    assert not _contains_path(d2, "level1/level2/file2.txt")  
    # At depth=3, we see file2.txt but not level3 contents
    assert _contains_path(d3, "level1/level2/file2.txt")
    assert _contains_path(d3, "level1/level2/level3")      # dir becomes visible
    assert not _contains_path(d3, "level1/level2/level3/file3.txt")
    # At depth=4, we finally see file3.txt
    assert _contains_path(d4, "level1/level2/level3/file3.txt")

def test_chunked_hashing(tmp_path):
    """Hashing must be deterministic and content-sensitive."""
    from app.core.cached_diff_engine import compute_content_hash
    p = tmp_path/"h.txt"
    p.write_text("A\n"*1000, encoding="utf-8")
    hash1 = compute_content_hash(str(p))
    hash2 = compute_content_hash(str(p))
    assert hash1 == hash2, "Hashing must be deterministic"
    p.write_text("A\n"*1000 + "CHANGED\n", encoding="utf-8")
    hash3 = compute_content_hash(str(p))
    assert hash3 != hash2, "Hash must change when file contents change"


def test_registry_concurrency_updates():
    """
    Stress ScanRegistry with many concurrent updates to one scan.
    We don't assert on ordering—only that the lock protects state
    (no exceptions, valid status, and final progress is one of the
    written values and inside [0,1]).
    """
    from concurrent.futures import ThreadPoolExecutor
    from app.core.cached_diff_engine import ScanRegistry, ScanStatus

    reg = ScanRegistry()
    scan_id = reg.create_scan("/tmp/some", ["a.txt"])

    # 64 distinct progress values in [0,1]
    values = [i / 63.0 for i in range(64)]

    def worker(v):
        reg.update_scan(scan_id, status=ScanStatus.RUNNING, progress=v)

    with ThreadPoolExecutor(max_workers=16) as ex:
        list(ex.map(worker, values))

    scan = reg.get_scan(scan_id)
    assert scan is not None
    assert scan.status == ScanStatus.RUNNING
    assert 0.0 <= float(scan.progress) <= 1.0
    assert float(scan.progress) in set(values)

def test_thread_safety():
    """ScanRegistry updates must be thread-safe and reflect final state."""
    from app.core.cached_diff_engine import ScanRegistry, ScanStatus
    reg = ScanRegistry()
    scan_id = reg.create_scan("/test/dir", ["file1.py"])
    reg.update_scan(scan_id, status=ScanStatus.RUNNING, progress=0.5)
    scan = reg.get_scan(scan_id)
    assert scan is not None
    assert scan.status == ScanStatus.RUNNING
    assert scan.progress == 0.5

if __name__ == "__main__":  # optional: allow running as script
    import pytest, sys
    sys.exit(pytest.main([__file__]))
