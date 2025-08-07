"""
================================================================================
NIP-DIFF - Advanced File Difference Visualization Tool
================================================================================

Copyright (c) 2025 Tayyab. All Rights Reserved.

PROPRIETARY AND CONFIDENTIAL

This software and associated documentation files (the "Software") are the 
exclusive property of the copyright holder. This Software contains proprietary 
and confidential information and is protected by copyright laws and 
international treaty provisions.

RESTRICTIONS:
- No part of this Software may be reproduced, distributed, or transmitted 
  in any form or by any means without the prior written permission of the 
  copyright holder.
- This Software is not for sale, license, or distribution to third parties.
- Reverse engineering, decompilation, or disassembly of this Software is 
  strictly prohibited.
- Any unauthorized use, copying, or distribution may result in severe civil 
  and criminal penalties.

This Software is provided "AS IS" without warranty of any kind, express or 
implied, including but not limited to the warranties of merchantability, 
fitness for a particular purpose, and non-infringement.

For licensing inquiries, please contact: tayyab3245@github.com
================================================================================
"""


# nip/core/diff_engine.py
import difflib, os
from typing import Dict, List

# ──────────────────────────────────────────────────────────────────────────
def _diff_lines(path: str, old: str, new: str) -> List[str]:
    """
    Return a unified diff for one file where *all* unchanged lines are kept.
    We do this by making the context size equal to the longer file length.
    For very large files, we limit context to prevent memory issues.
    """
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    max_lines = max(len(old_lines), len(new_lines))
    
    # Limit context for very large files to prevent memory issues
    ctx = min(max_lines, 10000)  # Cap at 10k lines context
    
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
