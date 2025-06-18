# nip/core/diff_engine.py
import difflib, os
from typing import Dict, List

# ──────────────────────────────────────────────────────────────────────────
def _diff_lines(path: str, old: str, new: str) -> List[str]:
    """
    Return a unified diff for one file where *all* unchanged lines are kept.
    We do this by making the context size equal to the longer file length.
    """
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    ctx = max(len(old_lines), len(new_lines))          # full-file context
    return list(difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=os.path.join("a", path),
        tofile=os.path.join("b", path),
        lineterm="",
        n=ctx
    ))

# ──────────────────────────────────────────────────────────────────────────
def format_output(old_snap: Dict[str, str], new_snap: Dict[str, dict]) -> str:
    """
    Build one big, GPT-friendly unified diff.
      • Deleted files → full body prefixed with “-”
      • Brand-new files → full body prefixed with “+”
      • Modified files → full diff with every line shown
      • Unchanged files → full body prefixed with “ ” (space)
    """
    output: List[str] = []

    all_paths = set(old_snap) | set(new_snap)
    # newest-modified first, then alpha
    sorted_paths = sorted(
        all_paths,
        key=lambda p: (-new_snap.get(p, {}).get("mtime", 0), p)
    )

    for path in sorted_paths:
        old_content = old_snap.get(path, "")
        new_entry   = new_snap.get(path)
        new_content = None if new_entry is None else new_entry["content"]

        # ---------- deleted file --------------------------------------
        if new_content is None:
            output.extend(_diff_lines(path, old_content, ""))
            continue

        # ---------- brand-new file ------------------------------------
        if not old_content:
            hdr  = [f"--- a/{path}", f"+++ b/{path}"]
            body = [f"+{ln}" if ln else "+" for ln in new_content.splitlines()]
            output.extend(hdr + body)
            continue

        # ---------- unchanged file ------------------------------------
        if old_content == new_content:
            hdr  = [f"--- a/{path}", f"+++ b/{path}"]
            body = [f" {ln}" for ln in new_content.splitlines()]
            output.extend(hdr + body)
            continue

        # ---------- modified file -------------------------------------
        output.extend(_diff_lines(path, old_content, new_content))

    return "\n".join(output)
