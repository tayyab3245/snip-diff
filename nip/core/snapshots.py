import json
import os
from typing import Dict, Set, Optional

from nip.config import SNAPSHOT_FILE, IGNORE_LIST

def _should_skip(path_parts, ignore_set: Set[str]) -> bool:
    return any(part in ignore_set for part in path_parts)

def get_all_files(
    directory: str,
    ignore_set: Set[str] = IGNORE_LIST,
    include_paths: Optional[Set[str]] = None,
) -> Dict[str, dict]:
    """
    Walk `directory`, return {relative_path: {"content": str, "mtime": float}}
    Only files whose *relative* path starts with a value in `include_paths`
    are kept when that set is provided.
    """
    files: Dict[str, dict] = {}

    for root, _, filenames in os.walk(directory):
        if _should_skip(root.split(os.sep), ignore_set):
            continue

        for filename in filenames:
            abs_path = os.path.join(root, filename)
            rel_path = os.path.relpath(abs_path, directory)

            if _should_skip(rel_path.split(os.sep), ignore_set):
                continue
            if include_paths and not any(
                rel_path == p or rel_path.startswith(f"{p}{os.sep}")
                for p in include_paths
            ):
                continue

            try:
                with open(abs_path, "r", encoding="utf-8") as fh:
                    files[rel_path] = {
                        "content": fh.read(),
                        "mtime": os.path.getmtime(abs_path),
                    }
            except Exception:
                # Binary file or unreadable – skip
                pass
    return files


def load_snapshot() -> Dict[str, str]:
    if not os.path.exists(SNAPSHOT_FILE):
        return {}
    with open(SNAPSHOT_FILE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_snapshot(snapshot: Dict[str, dict]) -> None:
    """
    Persist snapshot in a minimal form: {path: content}.
    Modification time is only used during the current run.
    """
    cleaned = {k: v["content"] if isinstance(v, dict) else v for k, v in snapshot.items()}
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as fh:
        json.dump(cleaned, fh, indent=2)
