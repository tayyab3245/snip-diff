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


"""
Checkable file-system tree view
-------------------------------

• No longer relies on Qt.ItemIsTristate (removed in Qt 6.6+)
• The check-state is handled in Python so it works on all PySide6 builds.
"""

from __future__ import annotations

import os
from typing import Dict, Set

from PySide6.QtCore import Qt, QModelIndex, Signal
from PySide6.QtWidgets import QFileSystemModel, QTreeView, QMessageBox

# Import neumorphic scroll bar
from .neumorphic_scrollbar import NeumorphicScrollBar


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

    def _refresh_ancestors(self, parent_idx: QModelIndex):
        """Walk up the tree & set each ancestor to Checked/PartiallyChecked/Unchecked."""
        if not parent_idx.isValid():
            return  # reached root

        all_checked = True
        any_checked = False
        for row in range(self.rowCount(parent_idx)):
            child_idx = self.index(row, 0, parent_idx)
            child_state = self.data(child_idx, Qt.CheckStateRole)
            if child_state == Qt.Checked:
                any_checked = True
            elif child_state == Qt.PartiallyChecked:
                any_checked = True
                all_checked = False
            else:  # Unchecked
                all_checked = False

        if all_checked:
            new_state = Qt.Checked
        elif any_checked:
            new_state = Qt.PartiallyChecked
        else:
            new_state = Qt.Unchecked

        old_state = self._state.get(self._path(parent_idx), Qt.Unchecked)
        if old_state != new_state:
            self._state[self._path(parent_idx)] = new_state
            self.dataChanged.emit(parent_idx, parent_idx)
            self._refresh_ancestors(parent_idx.parent())

    def checked_paths(self, root_path: str) -> Set[str]:
        """Return absolute paths of all fully-checked items (not partial)."""
        checked = set()
        self._collect_checked(self.index(root_path), checked)
        return checked

    def _collect_checked(self, idx: QModelIndex, out_set: Set[str]):
        if not idx.isValid():
            return
        state = self.data(idx, Qt.CheckStateRole)
        if state == Qt.Checked:
            out_set.add(self._path(idx))
        # recurse children
        for row in range(self.rowCount(idx)):
            child_idx = self.index(row, 0, idx)
            self._collect_checked(child_idx, out_set)


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
        
        # Set custom neumorphic scrollbars
        self.setVerticalScrollBar(NeumorphicScrollBar(self))
        self.setHorizontalScrollBar(NeumorphicScrollBar(self))
        
        # Apply neumorphic styling
        self._setup_theme_styling()
        
        # A plain left-click now toggles the check mark for that row
        self.clicked.connect(self._toggle_check)
        # ALSO connect to model data changes for when checkboxes are clicked directly
        self._model.dataChanged.connect(self._on_data_changed)
        print("DEBUG: FileTree initialized, clicked signal connected to _toggle_check")
        print("DEBUG: Also connected model.dataChanged to _on_data_changed")
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
    
    def _setup_theme_styling(self):
        """Apply neumorphic theme styling to the file tree"""
        # Dark theme neumorphic styling (matching theme file)
        dark_style = """
            QTreeView {
                background-color: #232428;
                color: rgb(4, 236, 180);
                border: 1px solid #0a0a0a;
                margin: 8px;
                border-radius: 4px;
                font-size: 16px;
                outline: none;
                selection-background-color: transparent;
            }
            
            QTreeView::item {
                border: none;
                padding: 4px 8px;
                background: transparent;
                border-radius: 2px;
                margin: 1px;
                outline: none;
            }
            
            QTreeView::item:hover {
                background: rgba(255, 255, 255, 0.06);
            }
            
            QTreeView::item:selected {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 0, 0, 0.8), stop: 1 #232428);
                border-top: 1px solid rgba(0, 0, 0, 0.8);
                border-left: 1px solid rgba(0, 0, 0, 0.8);
                border-bottom: 1px solid rgba(58, 58, 58, 1.0);
                border-right: 1px solid rgba(58, 58, 58, 1.0);
                color: rgb(4, 236, 180);
                outline: none;
            }
            
            QTreeView::item:selected:focus {
                outline: none;
                border: none;
            }
            
            QTreeView:focus {
                outline: none;
                border: 1px solid #0a0a0a;
            }
        """
        
        self.setStyleSheet(dark_style)
        
        # Remove focus policy to prevent dotted borders
        self.setFocusPolicy(Qt.NoFocus)
        
        # Store current theme
        self._current_theme = 'dark'
    
    def set_theme(self, theme_colors):
        """Update the theme for the file tree"""
        # Determine theme mode from colors
        bg_color = theme_colors.get('main_bg', '#232428')
        self._current_theme = 'dark' if bg_color.startswith('#2') else 'light'
        
        # Set theme for custom scrollbars
        v_scrollbar = self.verticalScrollBar()
        h_scrollbar = self.horizontalScrollBar()
        if hasattr(v_scrollbar, 'set_theme'):
            v_scrollbar.set_theme(theme_colors)
        if hasattr(h_scrollbar, 'set_theme'):
            h_scrollbar.set_theme(theme_colors)
        
        if self._current_theme == 'dark':
            style = """
                QTreeView {
                    background-color: #232428;
                    color: rgb(4, 236, 180);
                    border: 1px solid #0a0a0a;
                    margin: 8px;
                    border-radius: 4px;
                    font-size: 16px;
                    outline: none;
                    selection-background-color: transparent;
                }
                
                QTreeView::item {
                    border: none;
                    padding: 4px 8px;
                    background: transparent;
                    border-radius: 2px;
                    margin: 1px;
                    outline: none;
                }
                
                QTreeView::item:hover {
                    background: rgba(255, 255, 255, 0.06);
                }
                
                QTreeView::item:selected {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 rgba(0, 0, 0, 0.8), stop: 1 #232428);
                    border-top: 1px solid rgba(0, 0, 0, 0.8);
                    border-left: 1px solid rgba(0, 0, 0, 0.8);
                    border-bottom: 1px solid rgba(58, 58, 58, 1.0);
                    border-right: 1px solid rgba(58, 58, 58, 1.0);
                    color: rgb(4, 236, 180);
                    outline: none;
                }
                
                QTreeView::item:selected:focus {
                    outline: none;
                    border: none;
                }
                
                QTreeView:focus {
                    outline: none;
                    border: 1px solid #0a0a0a;
                }
            """
        else:  # light theme
            style = """
                QTreeView {
                    background-color: #E3EDF7;
                    color: #979797;
                    border: 1px solid #d0d0d0;
                    margin: 8px;
                    border-radius: 4px;
                    font-size: 16px;
                    outline: none;
                    selection-background-color: transparent;
                }
                
                QTreeView::item {
                    border: none;
                    padding: 4px 8px;
                    background: transparent;
                    border-radius: 2px;
                    margin: 1px;
                    outline: none;
                }
                
                QTreeView::item:hover {
                    background: rgba(0, 0, 0, 0.06);
                }
                
                QTreeView::item:selected {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 rgba(111, 140, 176, 0.4), stop: 1 #E3EDF7);
                    border-top: 1px solid rgba(111, 140, 176, 0.4);
                    border-left: 1px solid rgba(111, 140, 176, 0.4);
                    border-bottom: 1px solid #FFFFFF;
                    border-right: 1px solid #FFFFFF;
                    color: #979797;
                    outline: none;
                }
                
                QTreeView::item:selected:focus {
                    outline: none;
                    border: none;
                }
                
                QTreeView:focus {
                    outline: none;
                    border: 1px solid #d0d0d0;
                }
            """
        
        self.setStyleSheet(style)        

    # toggle helper ----------------------------------------------------
    def _toggle_check(self, idx: QModelIndex):
        print(f"DEBUG: _toggle_check called for index {idx.row()}")
        # Ignore clicks in columns > 0 (they're hidden anyway)
        if idx.column() != 0:
            print("DEBUG: Ignoring click on column > 0")
            return
        current = self._model.data(idx, Qt.CheckStateRole)
        new_state = Qt.Unchecked if current == Qt.Checked else Qt.Checked
        print(f"DEBUG: Changing state from {current} to {new_state}")
        self._model.setData(idx, new_state, Qt.CheckStateRole)
        # fire the click flash
        self._flash.stop()
        self._flash.start()
        
        # Emit selection changed signal for auto-scan functionality
        new_selection = self.checked_paths()
        print(f"DEBUG: Emitting selection_changed signal with {len(new_selection)} files: {new_selection}")
        self.selection_changed.emit(new_selection)

    def _on_data_changed(self, topLeft, bottomRight, roles):
        """Handle model data changes (when checkboxes are clicked directly)"""
        if Qt.CheckStateRole in roles:
            print("DEBUG: Model data changed - checkbox was clicked")
            new_selection = self.checked_paths()
            print(f"DEBUG: Emitting selection_changed signal with {len(new_selection)} files: {new_selection}")
            self.selection_changed.emit(new_selection)

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
