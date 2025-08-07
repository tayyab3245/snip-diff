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


# neumorphic_scrollbar.py
from PySide6.QtWidgets import QScrollBar, QStyleOptionSlider, QStyle
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Qt

class NeumorphicScrollBar(QScrollBar):
    """Simple custom QScrollBar with good contrast and clean design."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Store theme colors for custom painting
        self.theme_colors = {}
        
    def set_theme(self, theme_colors):
        """Update theme colors and trigger repaint"""
        self.theme_colors = theme_colors
        self.update()  # Trigger a repaint
        
    def paintEvent(self, event):
        """Custom paint event with simple, reliable design."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get theme colors with safe fallbacks - check the actual main_bg color
        main_bg = self.theme_colors.get('main_bg', '#232428')
        is_dark = main_bg == '#232428'  # Dark theme check
        
        # Track background - subtle contrast with main background
        if is_dark:
            track_color = QColor(25, 25, 30)     # Darker than main_bg for inset look
        else:
            track_color = QColor(215, 225, 235)  # Lighter than main_bg for inset look
            
        painter.fillRect(self.rect(), track_color)
        
        # Draw handle - force it to be visible even when no scrollable content
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        
        handle_rect = self.style().subControlRect(QStyle.CC_ScrollBar, opt, 
                                                QStyle.SC_ScrollBarSlider, self)
        
        # If handle rect is empty or invalid, create a visible test handle
        if handle_rect.isEmpty() or not handle_rect.isValid():
            if self.orientation() == Qt.Vertical:
                # Create a test vertical handle
                handle_rect = self.rect().adjusted(2, 10, -2, -50)
            else:
                # Create a test horizontal handle  
                handle_rect = self.rect().adjusted(10, 2, -50, -2)
        
        # Always draw the handle if we have a valid rect
        if handle_rect.isValid() and not handle_rect.isEmpty():
            self._draw_simple_handle(painter, handle_rect, is_dark)
        
        painter.end()
    
    def _draw_simple_handle(self, painter, rect, is_dark):
        """Draw a simple, clean handle with subtle but visible contrast."""
        # Don't adjust the handle rect at all - use full width
        handle_rect = rect  # Use the full rect for maximum visibility
        
        if is_dark:
            # Subtle light gray - visible but not distracting on dark background
            fill_color = QColor(100, 100, 105)    # Subtle light gray
            border_color = QColor(120, 120, 125)  # Slightly lighter border
        else:
            # Subtle dark gray - visible but not distracting on light background
            fill_color = QColor(130, 130, 135)    # Subtle dark gray
            border_color = QColor(110, 110, 115)  # Slightly darker border
        
        # Draw handle with subtle visibility
        painter.setBrush(QBrush(fill_color))
        painter.setPen(QPen(border_color, 1))
        painter.drawRect(handle_rect)
