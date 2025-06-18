import difflib
from typing import Dict, List

def _diff_lines(old: str, new: str) -> List[str]:
    return list(difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        lineterm=""
    ))

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
        output.append("-" * 23)
        output.append(path)

        old_content = old_snap.get(path, "")
        new_entry   = new_snap.get(path)
        new_content = None if new_entry is None else new_entry["content"]

        if new_content is None:
            output.append("(deleted)")
        elif old_content == new_content:      # unchanged
            output.append(new_content)
        elif not old_content:                 # brand-new file
            output.append(new_content)
        else:
            output.extend(_diff_lines(old_content, new_content))

        output.append("-" * 23)

    return "\n".join(output)
