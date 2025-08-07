"""
================================================================================
SNIP-DIFF - AI workflow tool for preparing code context outside agentic environments
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


"""
Runs the diff in a background thread   +   optional live filesystem watcher
───────────────────────────────────────────────────────────────────────────
• DiffWorker  – QThread that performs one diff run and emits the diff text.
• LiveWatcher – QObject wrapper around QFileSystemWatcher that emits a
                callback every time *anything* under the chosen root updates.
"""

from __future__ import annotations
from typing import Set, Callable, List, Optional
import os

from PySide6.QtCore import QThread, Signal, QObject, QFileSystemWatcher

from nip.core.snapshot     import load_snapshot, save_snapshot, get_all_files
from nip.core.diff_engine  import format_output
from nip.config            import IGNORE_LIST


# ──────────────────────────────────────────────────────────────────────────
class DiffWorker(QThread):
    finished = Signal(str)            # emits full diff text when done

    def __init__(self, root: str, include_paths: Optional[Set[str]],
                 callback: Callable[[str], None]):
        super().__init__()
        self._root   = root
        self._include: Optional[Set[str]] = include_paths
        self.finished.connect(callback)

    # ------------------------------------------------------------------ #
    def run(self):
        # 1) load previous snapshot and KEEP ONLY paths still included
        old_full = load_snapshot()
        if self._include is not None:
            keep = tuple(self._include)        # faster lookup inside loop
            old = {
                p: v for p, v in old_full.items()
                if any(p == inc or p.startswith(f"{inc}{os.sep}") for inc in keep)
            }
        else:
            old = {}

        # 2) make fresh scan (already limited by include_paths)
        new = get_all_files(self._root, IGNORE_LIST, self._include)
        diff = format_output(old, new)
        save_snapshot(new)
        self.finished.emit(diff)


# ──────────────────────────────────────────────────────────────────────────
class LiveWatcher(QObject):
    """
    Watches *all* directories under `root` and invokes `on_change`
    whenever any file or sub-directory changes.
    """
    def __init__(self, root: str, on_change: Callable[[], None]):
        super().__init__()
        self._watcher = QFileSystemWatcher(self._all_dirs(root))
        self._watcher.directoryChanged.connect(on_change)
        self._watcher.fileChanged.connect(on_change)

    # gather every directory so QFileSystemWatcher is recursive -------- #
    @staticmethod
    def _all_dirs(root: str) -> List[str]:
        dirs: List[str] = []
        for dir_path, subdirs, _ in os.walk(root):
            # exclude ignored dirs so we don’t overflow the watch limit
            if any(part in IGNORE_LIST for part in dir_path.split(os.sep)):
                subdirs[:] = []      # prune walk
                continue
            dirs.append(dir_path)
        return dirs
