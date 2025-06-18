import os
from typing import Dict, Set

from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QFileSystemModel, QTreeView, QMessageBox


class CheckableFSModel(QFileSystemModel):
    """
    QFileSystemModel where every row has a tri-state checkbox.
    We store state per QModelIndex in self._state.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state: Dict[int, Qt.CheckState] = {}

    # ---------- helpers --------------------------------------------------
    def _index_id(self, idx: QModelIndex) -> int:
        """A stable int key for QModelIndex (can't hash index directly)."""
        return idx.internalId()

    # ---------- Qt overrides ---------------------------------------------
    def flags(self, idx):
        return super().flags(idx) | Qt.ItemIsUserCheckable | Qt.ItemIsTristate

    def data(self, idx, role):
        if role == Qt.CheckStateRole:
            return self._state.get(self._index_id(idx), Qt.Unchecked)
        return super().data(idx, role)

    def setData(self, idx, value, role):
        if role != Qt.CheckStateRole:
            return super().setData(idx, value, role)

        self._set_state_recursive(idx, value)
        self._update_parent_state(idx)
        return True

    # ---------- state propagation helpers --------------------------------
    def _set_state_recursive(self, idx: QModelIndex, state: Qt.CheckState):
        """Apply `state` to idx and all children."""
        self._state[self._index_id(idx)] = state
        for r in range(self.rowCount(idx)):
            child = self.index(r, 0, idx)
            self._set_state_recursive(child, state)
        self.dataChanged.emit(idx, idx)

    def _update_parent_state(self, idx: QModelIndex):
        """Bubble changes upward so parents become Checked / PartiallyChecked."""
        parent = idx.parent()
        if not parent.isValid():
            return

        states = {self._state.get(self._index_id(self.index(r, 0, parent)), Qt.Unchecked)
                  for r in range(self.rowCount(parent))}

        new_state = Qt.Checked if states == {Qt.Checked} else (
            Qt.Unchecked if states == {Qt.Unchecked} else Qt.PartiallyChecked
        )

        self._state[self._index_id(parent)] = new_state
        self.dataChanged.emit(parent, parent)
        self._update_parent_state(parent)

    # ---------- API ------------------------------------------------------
    def checked_paths(self, root_path: str) -> Set[str]:
        """
        Return a set of *relative* paths (files or directories) that are Checked.
        """
        paths: Set[str] = set()
        for idx_id, state in self._state.items():
            if state != Qt.Checked:
                continue
            idx = self.index(idx_id)
            if not idx.isValid():
                continue
            abs_path = self.filePath(idx)
            rel_path = os.path.relpath(abs_path, root_path)
            paths.add(rel_path)
        return paths


class FileTree(QTreeView):
    """
    Wrapper around CheckableFSModel to expose a cleaner API to MainWindow.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = CheckableFSModel()
        self.setModel(self._model)
        self.setHeaderHidden(True)
        self.setSelectionMode(QTreeView.ExtendedSelection)
        # Hide size / type / modified columns
        for col in range(1, 4):
            self.hideColumn(col)

        self._root_path: str | None = None

    # --------------------------------------------------
    @property
    def root_path(self) -> str:
        if not self._root_path:
            raise RuntimeError("Root path not set")
        return self._root_path

    def set_root(self, path: str):
        """Called by toolbar when the user chooses a folder."""
        if not path:
            return
        self._root_path = path
        self._model.setRootPath(path)
        self.setRootIndex(self._model.index(path))

    # --------------------------------------------------
    def checked_paths(self) -> Set[str]:
        """Return selected paths *relative* to root, or empty set if none."""
        if not self._root_path:
            return set()
        return self._model.checked_paths(self._root_path)

    # --------------------------------------------------
    def clear_snapshot(self):
        """Remove .nip_snapshot.json in the selected root folder."""
        from nip.config import SNAPSHOT_FILE
        if not self._root_path:
            return

        target = os.path.join(self._root_path, SNAPSHOT_FILE)
        if os.path.exists(target):
            os.remove(target)
            QMessageBox.information(self, "Undo", "Snapshot removed.")
        else:
            QMessageBox.information(self, "Undo", "No snapshot to remove.")
