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


from PySide6.QtCore    import Signal, Qt, QTimer
from PySide6.QtGui     import QAction, QColor
from PySide6.QtWidgets import QToolBar, QFileDialog, QPushButton, QWidget, QHBoxLayout, QSizePolicy
from .neumorphism.Neumorphism import BoxShadow, BoxShadowWrapper


class NipToolBar(QToolBar):
    """
    Emits high-level signals consumed by MainWindow.
    The toolbar shows plain text buttons so it’s visible even without icons.
    """
    choose_folder = Signal(str)
    run           = Signal()
    copy          = Signal()
    undo          = Signal()
    export        = Signal()
    theme_changed = Signal(str)  # Emit theme mode when changed

    def __init__(self, parent=None):
        super().__init__("Actions", parent)
        self.setObjectName("toolbar")

        # Make sure text is always visible (no icons supplied)
        self.setToolButtonStyle(Qt.ToolButtonTextOnly)

        # Choose Folder ────────────────────────────────────────────────
        act_choose = QAction("Choose Folder", self)
        act_choose.setShortcut("Ctrl+O")
        act_choose.setToolTip("Select a root folder to diff (Ctrl+O)")
        act_choose.triggered.connect(self._on_choose)
        self.addAction(act_choose)

        # Run / Refresh diff ───────────────────────────────────────────
        act_run = QAction("Run", self)
        act_run.setShortcut("F5")
        act_run.setToolTip("Scan and build diff (F5)")
        act_run.triggered.connect(self.run)
        self.addAction(act_run)

        # Copy Output ─────────────────────────────────────────────────
        act_copy = QAction("Copy Output", self)
        act_copy.setShortcut("Ctrl+C")
        act_copy.setToolTip("Copy diff text to clipboard (Ctrl+C)")
        act_copy.triggered.connect(self.copy)
        self.addAction(act_copy)

        # Live Watch Toggle ────────────────────────────────────────────
        self.act_live = QAction("Live Watch: ON", self)
        self.act_live.setCheckable(True)
        self.act_live.setChecked(True)  # Default to ON
        self.act_live.setToolTip("Toggle automatic file watching")
        self.act_live.triggered.connect(self._toggle_live_watch)
        self.addAction(self.act_live)

        # Theme Toggle ─────────────────────────────────────────────────
        self.act_theme = QAction("Dark", self)
        self.act_theme.setToolTip("Toggle between light and dark theme")
        self.act_theme.triggered.connect(self._toggle_theme)
        self.addAction(self.act_theme)
        
        # Track current theme mode
        self._current_theme = 'dark'
    # ─────────────────────────────────────────────────────────────────
    def _on_choose(self):
        folder = QFileDialog.getExistingDirectory(self.parent(), "Select folder")
        if folder:
            self.choose_folder.emit(folder)
    
    def _toggle_live_watch(self):
        """Toggle live file watching on/off"""
        is_enabled = self.act_live.isChecked()
        if is_enabled:
            self.act_live.setText("Live Watch: ON")
            # Re-enable the watcher if it exists
            if hasattr(self.parent(), '_watcher') and self.parent()._watcher:
                print("Live watch enabled")
        else:
            self.act_live.setText("Live Watch: OFF")
            # Disable the watcher
            if hasattr(self.parent(), '_watcher') and self.parent()._watcher:
                self.parent()._watcher.deleteLater()
                self.parent()._watcher = None
                print("Live watch disabled")

    def _toggle_theme(self):
        """Toggle between light and dark themes"""
        if self._current_theme == 'dark':
            self._current_theme = 'light'
            self.act_theme.setText("Light")
        else:
            self._current_theme = 'dark'
            self.act_theme.setText("Dark")
        
        # Emit the theme change signal
        self.theme_changed.emit(self._current_theme)