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


# nip/ui/glass_window.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QBrush, QColor


class GlassWindow(QWidget):
    """
    Mix-in that gives any QWidget:
      • Frameless     • Rounded corners     • Blur-behind (on Win-10/11 & macOS)
    """
    def __init__(self, radius: int = 8, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._radius = radius

        # make window translucent + frameless
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # enable native blur where available (Qt 6.5+)
        try:
            from PySide6.QtGui import QGraphicsBlurEffect
            self.setGraphicsEffect(QGraphicsBlurEffect(blurRadius=30))
        except Exception:
            pass  # older Qt – still translucent

    # paint rounded rectangle so children inherit the alpha mask
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QBrush(QColor(30, 30, 30, 180)))   # semi-transparent charcoal
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(self.rect(), self._radius, self._radius)
