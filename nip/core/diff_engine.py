import difflib, os
from typing import Dict, List

def _diff_lines(path: str, old: str, new: str) -> List[str]:
    """Return canonical unified-diff for *one* file (old → new)."""
    return list(
        difflib.unified_diff(
            old.splitlines(),
            new.splitlines(),
            fromfile=os.path.join("a", path),
            tofile=os.path.join("b", path),
            lineterm=""
        )
    )

def format_output(old_snap: Dict[str, str], new_snap: Dict[str, dict]) -> str:
    """
    Build one big, GPT-friendly unified diff.
    Deleted files show '(deleted)'.
    Unchanged files show untouched content for context.
    """
    output: List[str] = []
    all_paths = set(old_snap) | set(new_snap)
    # sort by newest mtime first, then name
    sorted_paths = sorted(
        all_paths,
        key=lambda p: (-new_snap.get(p, {}).get("mtime", 0), p)
    )

    for path in sorted_paths:

        old_content = old_snap.get(path, "")
        new_entry   = new_snap.get(path)
        new_content = None if new_entry is None else new_entry["content"]

        # Deleted file -------------------------------------------------
        if new_content is None:
            output.extend(_diff_lines(path, old_content, ""))
            continue

        # Brand-new or unchanged file → dump full body ----------------
        if not old_content or old_content == new_content:
            hdr = [f"--- a/{path}", f"+++ b/{path}"]
            body = [f" {ln}" for ln in new_content.splitlines()]
            output.extend(hdr + body)
            continue

        # Modified file -----------------------------------------------
        output.extend(_diff_lines(path, old_content, new_content))
    return "\n".join(output)
