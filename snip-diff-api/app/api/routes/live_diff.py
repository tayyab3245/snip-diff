"""Live watch & token‑aware diff aggregation API.

Endpoints kept intentionally lean for the UI:
  POST /live/start { paths: [] }
  POST /live/stop
  GET  /live/status
  GET  /live/files -> list of watched files + meta
  GET  /live/file?path=... -> full FileDiff
  GET  /live/aggregate?mode=unified|side_by_side&scope=incremental|full
  POST /live/prompt/apply {strategy, text}
  GET  /live/prompt/state
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Optional
import time
import os

from app.core.watch.watch_service import WatchService
from app.core.models.diff_types import (
    FileDiff, FileDiffMetaAPI, FileDiffAPI,
    WatchFileRequest, WatchStatusResponse, LiveDiffResponse, PromptApplyRequest, PromptState
)
from app.core.utils.token_estimator import estimate_tokens, estimate_aggregate

router = APIRouter(prefix="/live", tags=["live"])
_watch = WatchService()
_prompt_state = PromptState()


def _build_api_file_diff(fd: FileDiff) -> FileDiffAPI:
    # Build stats API
    from app.core.models.diff_types import DiffStatsAPI, UnifiedHunkAPI, LineTokenAPI

    stats_api = DiffStatsAPI(
        lines_added=fd.meta.stats.lines_added,
        lines_deleted=fd.meta.stats.lines_deleted,
        lines_modified=fd.meta.stats.lines_modified,
        lines_context=fd.meta.stats.lines_context,
        total_changes=fd.meta.stats.total_changes,
    )
    meta_api = FileDiffMetaAPI(
        path=fd.meta.path,
        old_path=fd.meta.old_path,
        change_type=fd.meta.change_type.value,
        file_size_old=fd.meta.file_size_old,
        file_size_new=fd.meta.file_size_new,
        is_binary=fd.meta.is_binary,
        stats=stats_api,
        est_tokens_unified=fd.meta.est_tokens_unified,
        est_tokens_side_by_side=fd.meta.est_tokens_side_by_side,
        est_tokens_incremental=fd.meta.est_tokens_incremental,
    )
    # Convert hunks
    def _hunk(h):
        return UnifiedHunkAPI(
            old_start=h.old_start,
            old_count=h.old_count,
            new_start=h.new_start,
            new_count=h.new_count,
            header=h.header,
            lines=[LineTokenAPI(
                line_no_old=l.line_no_old,
                line_no_new=l.line_no_new,
                line_type=l.line_type.value,
                text=l.text
            ) for l in h.lines]
        )

    return FileDiffAPI(
        meta=meta_api,
        hunks=[_hunk(h) for h in fd.hunks],
        modes=fd.modes,
    )


@router.post("/start", response_model=LiveDiffResponse)
async def start_watch(request: WatchFileRequest):
    if not _watch.is_running:
        _watch.start()
    _watch.watch_files(request.file_paths)
    return LiveDiffResponse(success=True, message=f"Watching {len(request.file_paths)} file(s)")


@router.post("/stop", response_model=LiveDiffResponse)
async def stop_watch():
    _watch.stop()
    return LiveDiffResponse(success=True, message="Stopped watching")


@router.get("/status", response_model=WatchStatusResponse)
async def status():
    stats = _watch.get_stats()
    watched = list(_watch.watched_paths) if _watch.watched_paths else []
    return WatchStatusResponse(is_watching=_watch.is_running, watched_files=watched, stats=stats)


@router.get("/files")
async def list_files():
    out: List[Dict] = []
    if not _watch.watched_paths:
        return out
    for path in _watch.watched_paths:
        fd = _watch.get_file_diff(path)
        if fd:
            out.append(_build_api_file_diff(fd).dict())
    return out


@router.get("/file", response_model=FileDiffAPI)
async def get_file(path: str = Query(...)):  # noqa: A002
    fd = _watch.get_file_diff(path)
    if not fd:
        raise HTTPException(status_code=404, detail="Diff not available")
    return _build_api_file_diff(fd)


@router.get("/aggregate")
async def aggregate(mode: str = Query("unified"), scope: str = Query("incremental")):
    # Produce a token-aware concatenated diff (with optional prompt)
    if not _watch.watched_paths:
        return {"text": "", "tokens": 0, "files": 0}
    segments: List[str] = []
    for path in _watch.watched_paths:
        fd = _watch.get_file_diff(path)
        if not fd:
            continue
        # Choose view
        view_key = "unified_full" if scope == "full" else "unified_context"
        if mode == "side_by_side":
            view_key = "side_by_side"
        view = fd.modes.get(view_key)
        if not view:
            continue
        header = f"### {path}\n"
        if view_key.startswith("unified"):
            body = "\n".join(
                [f"{l.line_type.value[:1]} {l.text}" for h in fd.hunks for l in h.lines]
            )
        else:  # side_by_side export (simple)
            rows = view
            body = "\n".join(
                [
                    (r.left.text if r.left else "").ljust(40) + " | " + (r.right.text if r.right else "")
                    for r in rows
                ]
            )
        segments.append(header + body)
    prompt = _prompt_state.active_prompt
    if prompt and _prompt_state.strategy == "prepend":
        segments.insert(0, prompt)
    elif prompt and _prompt_state.strategy == "append":
        segments.append(prompt)
    text = "\n\n".join(segments)
    tokens = estimate_tokens(text)
    return {"text": text, "tokens": tokens, "files": len(segments)}


@router.post("/prompt/apply", response_model=PromptState)
async def apply_prompt(req: PromptApplyRequest):
    if req.strategy not in {"prepend", "append", "replace"}:
        raise HTTPException(status_code=400, detail="Invalid strategy")
    if req.strategy == "replace":
        _prompt_state.strategy = "prepend"
        _prompt_state.active_prompt = req.text
    else:
        _prompt_state.strategy = req.strategy
        _prompt_state.active_prompt = req.text
    _prompt_state.total_tokens = estimate_tokens(_prompt_state.active_prompt)
    return _prompt_state


@router.get("/prompt/state", response_model=PromptState)
async def prompt_state():
    return _prompt_state


# Health
@router.get("/health")
async def health():
    return {"status": "ok", "watching": _watch.is_running}
