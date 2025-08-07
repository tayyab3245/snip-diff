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
Status overlay widget for showing temporary status messages
──────────────────────────────────────────────────────────────────────────
• Non-intrusive popup overlay for status messages
• Automatic fade-out after timeout
• Different styles for different message types
• Prevents overwriting main content area
"""

from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QLabel, QGraphicsOpacityEffect


class StatusOverlay(QLabel):
    """
    A floating status overlay that shows temporary messages
    without interfering with the main content area.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.hide()
        
        # Setup opacity animation
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(300)  # 300ms fade
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_animation.finished.connect(self._on_fade_finished)
        
        # Auto-hide timer
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.fade_out)
        
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup base styles for the overlay"""
        self.setObjectName("statusOverlay")  # Use CSS class instead of inline style
    
    def show_message(self, message: str, message_type: str = "info", duration: int = 3000):
        """
        Show a status message with auto-hide
        
        Args:
            message: The message text to display
            message_type: Type of message (info, success, warning, error)
            duration: How long to show the message in milliseconds
        """
        self.setText(message)
        self._apply_message_style(message_type)
        
        # Position the overlay
        self._position_overlay()
        
        # Show with fade-in
        self.show()
        self.fade_in()
        
        # Set auto-hide timer
        if duration > 0:
            self.hide_timer.start(duration)
    
    def _apply_message_style(self, message_type: str):
        """Apply styling based on message type"""
        styles = {
            "info": {
                "background": "rgba(45, 45, 48, 220)",
                "border": "#3c3c3c",
                "color": "#ffffff"
            },
            "success": {
                "background": "rgba(30, 58, 30, 220)",
                "border": "#4ec94e",
                "color": "#4ec94e"
            },
            "warning": {
                "background": "rgba(58, 58, 30, 220)",
                "border": "#f1c40f",
                "color": "#f1c40f"
            },
            "error": {
                "background": "rgba(58, 30, 30, 220)",
                "border": "#f14c4c",
                "color": "#f14c4c"
            }
        }
        
        # Apply message type specific styling via CSS classes
        css_classes = {
            "info": "statusOverlayInfo",
            "success": "statusOverlaySuccess", 
            "warning": "statusOverlayWarning",
            "error": "statusOverlayError"
        }
        
        css_class = css_classes.get(message_type, "statusOverlayInfo")
        self.setObjectName(css_class)  # Use CSS class instead of inline styling
    
    def _position_overlay(self):
        """Position the overlay in the parent widget"""
        if not self.parent():
            return
            
        parent = self.parent()
        parent_rect = parent.rect()
        
        # Calculate size
        self.adjustSize()
        overlay_size = self.size()
        
        # Position at top-center
        x = (parent_rect.width() - overlay_size.width()) // 2
        y = 20  # 20px from top
        
        self.move(x, y)
        self.raise_()  # Bring to front
    
    def fade_in(self):
        """Fade in the overlay"""
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
    
    def fade_out(self):
        """Fade out the overlay"""
        self.hide_timer.stop()  # Stop the auto-hide timer
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.start()
    
    def _on_fade_finished(self):
        """Called when fade animation finishes"""
        if self.opacity_effect.opacity() == 0.0:
            self.hide()
    
    def resizeEvent(self, event):
        """Reposition when parent is resized"""
        super().resizeEvent(event)
        if self.isVisible():
            self._position_overlay()


class StatusManager:
    """
    Manager class for coordinating status messages across the application
    """
    
    def __init__(self, overlay: StatusOverlay):
        self.overlay = overlay
    
    def show_info(self, message: str, duration: int = 3000):
        """Show an info message"""
        self.overlay.show_message(message, "info", duration)
    
    def show_success(self, message: str, duration: int = 3000):
        """Show a success message"""
        self.overlay.show_message(message, "success", duration)
    
    def show_warning(self, message: str, duration: int = 4000):
        """Show a warning message"""
        self.overlay.show_message(message, "warning", duration)
    
    def show_error(self, message: str, duration: int = 5000):
        """Show an error message"""
        self.overlay.show_message(message, "error", duration)
    
    def show_no_changes(self, duration: int = 2000):
        """Show the 'no changes' message as a brief info overlay"""
        self.overlay.show_message("No changes detected since last scan", "info", duration)
