"""
Checkable file-system tree view
-------------------------------

• No longer relies on Qt.ItemIsTristate (removed in Qt 6.6+    # toggle helper ----------------------------------------------------
    def _toggle_check(self, idx: QModelIndex):
        # Ignore clicks in columns > 0 (they're hidden anyway)
        if idx.column() != 0:
            return
        current = self._model.data(idx, Qt.CheckStateRole)
        new_state = Qt.Unchecked if current == Qt.Checked else Qt.Checked
        self._model.setData(idx, new_state, Qt.CheckStateRole)
        
        # CRITICAL: Log selection change immediately and trigger UI update
        new_selection = self.checked_paths()
        print(f"DEBUG: UI selection changed to {new_selection}")
        
        # Emit selection change signal for immediate UI updates
        self.selection_changed.emit(new_selection)
        
        # fire the click flash
        self._flash.stop()
        self._flash.start()i-state is handled in Python so it works on all PySide6 builds.
"""

from __future__ import annotations

import os
from typing import Dict, Set

from PySide6.QtCore import Qt, QModelIndex, Signal
from PySide6.QtWidgets import QFileSystemModel, QTreeView, QMessageBox


# ----------------------------------------------------------------------
class CheckableFSModel(QFileSystemModel):
    """QFileSystemModel where every index is user-checkable."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # key = absolute path, value = Qt.CheckState
        self._state: Dict[str, Qt.CheckState] = {}
    # public helper – wipe old selections --------------------------------
    def clear_states(self):
        """Remove **all** remembered check-boxes (called when root changes)."""
        self._state.clear()

    # ---------- helpers -------------------------------------------------
    def _path(self, idx: QModelIndex) -> str:
        return self.filePath(idx)

    # ---------- Qt overrides -------------------------------------------
    def flags(self, idx: QModelIndex):
        # Leave out ItemIsTristate; we simulate tri-state ourselves.
        return super().flags(idx) | Qt.ItemIsUserCheckable

    def data(self, idx: QModelIndex, role):
        if role == Qt.CheckStateRole:
            return self._state.get(self._path(idx), Qt.Unchecked)
        return super().data(idx, role)

    def setData(self, idx: QModelIndex, value, role):
        if role != Qt.CheckStateRole:
            return super().setData(idx, value, role)

        # 1) apply to this index & all children
        self._set_state_recursive(idx, value)

        # 2) update ancestors so parents show Checked / PartiallyChecked / Unchecked
        self._refresh_ancestors(idx.parent())

        self.dataChanged.emit(idx, idx.siblingAtColumn(0))
        return True

    # ---------- state propagation --------------------------------------
    def _set_state_recursive(self, idx: QModelIndex, state: Qt.CheckState):
        """Apply `state` to idx and all its children."""
        self._state[self._path(idx)] = state
        for row in range(self.rowCount(idx)):
            child = self.index(row, 0, idx)
            self._set_state_recursive(child, state)

    def _refresh_ancestors(self, parent: QModelIndex):
        """Bubble changes upward so ancestors get correct mixed state."""
        while parent.isValid():
            states = {
                self._state.get(self._path(self.index(r, 0, parent)), Qt.Unchecked)
                for r in range(self.rowCount(parent))
            }
            if states == {Qt.Checked}:          # all checked
                new_state = Qt.Checked
            elif states == {Qt.Unchecked}:      # none checked
                new_state = Qt.Unchecked
            else:                               # mixture
                new_state = Qt.PartiallyChecked
            self._state[self._path(parent)] = new_state
            parent = parent.parent()

    # ---------- public API ---------------------------------------------
    def checked_paths(self, root_path: str) -> Set[str]:
        """
        Return a set of *relative* paths that are fully Checked.
        Directories marked PartiallyChecked are ignored (their children
        decide individually).
        """
        rel: Set[str] = set()
        for abs_path, state in self._state.items():
            if state != Qt.Checked:
                continue
            rel.add(os.path.relpath(abs_path, root_path))
        return rel


# ----------------------------------------------------------------------
class FileTree(QTreeView):
    """
    Thin wrapper around CheckableFSModel to expose
    `set_root()`, `checked_paths()`, and `clear_snapshot()`.
    """
    # Signal emitted when file selection changes
    selection_changed = Signal(set)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = CheckableFSModel()
        self.setModel(self._model)
        self.setHeaderHidden(True)
        self.setSelectionMode(QTreeView.SingleSelection)
        # A plain left-click now toggles the check mark for that row
        self.clicked.connect(self._toggle_check)
        # subtle opacity flash on click (safe; uses Qt property)
        from PySide6.QtWidgets import QGraphicsOpacityEffect
        from PySide6.QtCore    import QPropertyAnimation, QEasingCurve

        eff = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(eff)

        self._flash = QPropertyAnimation(eff, b"opacity", self)
        self._flash.setDuration(120)
        self._flash.setStartValue(0.6)
        self._flash.setEndValue(1.0)
        self._flash.setEasingCurve(QEasingCurve.InOutQuad)

        # Hide columns Size | Type | Date Modified  ← was lost
        for col in range(1, 4):
            self.hideColumn(col)

        self._root_path: str | None = None        

    # toggle helper ----------------------------------------------------
    def _toggle_check(self, idx: QModelIndex):
        # Ignore clicks in columns > 0 (they’re hidden anyway)
        if idx.column() != 0:
            return
        current = self._model.data(idx, Qt.CheckStateRole)
        new_state = Qt.Unchecked if current == Qt.Checked else Qt.Checked
        self._model.setData(idx, new_state, Qt.CheckStateRole)
        # fire the click flash
        self._flash.stop()
        self._flash.start()

    # ---- basic actions -------------------------------------------------
    def set_root(self, path: str):
        if not path:
            return
        self._root_path = path
        self._model.clear_states()          # ← forget previous selections
        self._model.setRootPath(path)
        self.setRootIndex(self._model.index(path))

    @property
    def root_path(self) -> str:
        if not self._root_path:
            raise RuntimeError("Root path not set")
        return self._root_path

    def checked_paths(self) -> Set[str]:
        if not self._root_path:
            return set()
        return self._model.checked_paths(self._root_path)

    # ---- undo snapshot helper -----------------------------------------
    def clear_snapshot(self):
        from nip.config import SNAPSHOT_FILE  # local import avoids cycle
        if not self._root_path:
            return
        snap = os.path.join(self._root_path, SNAPSHOT_FILE)
        if os.path.exists(snap):
            os.remove(snap)
            QMessageBox.information(self, "Undo", "Snapshot removed.")
        else:
            QMessageBox.information(self, "Undo", "No snapshot to remove.")
