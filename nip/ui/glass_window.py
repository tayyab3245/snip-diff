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
