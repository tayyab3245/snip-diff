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


# nip/ui/title_bar.py
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication


class TitleBar(QWidget):
    """Mac-style traffic lights (square) + drag-to-move."""
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(28)

        # ----- buttons -------------------------------------------------
        self.btn_close = self._circle("#FF5F57")
        self.btn_min   = self._circle("#FFBD2E")
        self.btn_max   = self._circle("#28C840")

        self.btn_close.clicked.connect(QApplication.instance().quit)
        self.btn_min.clicked.connect(self.window().showMinimized)
        self.btn_max.clicked.connect(self._toggle_max)

        lay = QHBoxLayout(self, spacing=6, contentsMargins=(10, 0, 0, 0))
        lay.addWidget(self.btn_close)
        lay.addWidget(self.btn_min)
        lay.addWidget(self.btn_max)
        lay.addStretch()

    # ------------------------------------------------------------------
    @staticmethod
    def _circle(col: str) -> QPushButton:
        b = QPushButton()
        b.setFixedSize(14, 14)
        # Use CSS classes instead of inline styling
        if col == "#F75E5E":
            b.setObjectName("titleBarCloseButton")
        elif col == "#F5BF4F":
            b.setObjectName("titleBarMinimizeButton")
        elif col == "#5EC947":
            b.setObjectName("titleBarMaximizeButton")
        else:
            b.setObjectName("titleBarButton")
        return b

    # toggle helper ----------------------------------------------------
    def _toggle_max(self):
        win = self.window()
        if win.isMaximized():
            win.showNormal()
        else:
            win.showMaximized()

    # ----- drag window -----------------------------------------------
    _mouse_pos: QPoint | None = None

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._mouse_pos = e.globalPosition().toPoint() - self.window().frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._mouse_pos and e.buttons() & Qt.LeftButton:
            self.window().move(e.globalPosition().toPoint() - self._mouse_pos)

    def mouseReleaseEvent(self, _):
        self._mouse_pos = None
