from typing import Set

from PySide6.QtCore import QThread, Signal

from nip.core.snapshot import load_snapshot, save_snapshot, get_all_files
from nip.core.diff_engine import format_output
from nip.config import IGNORE_LIST


class DiffWorker(QThread):
    """
    Runs the heavyweight file-system walk and diff in the background.
    """
    finished = Signal(str)  # emits full diff text

    def __init__(self, root_path: str, include_paths: Set[str], callback):
        super().__init__()
        self._root   = root_path
        self._paths  = include_paths
        self.finished.connect(callback)

    # ----------------------------------------- #
    def run(self) -> None:
        old = load_snapshot()
        new = get_all_files(self._root, IGNORE_LIST, self._paths)
        diff = format_output(old, new)
        save_snapshot(new)
        self.finished.emit(diff)
