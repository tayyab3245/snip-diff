# neumorphic_scrollbar.py
from PySide6.QtCore    import Qt, QRect, QSize, QPoint
from PySide6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QApplication
from PySide6.QtGui     import QColor
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Neumorphism.Neumorphism import BoxShadowWrapper            # your cloned file

# ---------- colour tokens reused from the palette --------------------
LIGHT_BG          = QColor("#EAE7DF")               # track concave
LIGHT_HANDLE_BG   = QColor("#F7F5F1")               # handle raised
LIGHT_SHADOW_OUT  = QColor(0, 0, 0, 25)
LIGHT_HLIGHT_OUT  = QColor(255, 255, 255, 200)
LIGHT_SHADOW_IN   = QColor(0, 0, 0, 45)
LIGHT_HLIGHT_IN   = QColor(255, 255, 255, 230)

# Dark theme colors
DARK_BG           = QColor("#232428")               # track concave
DARK_HANDLE_BG    = QColor("#2a2a2e")               # handle raised
DARK_SHADOW_OUT   = QColor(0, 0, 0, 128)
DARK_HLIGHT_OUT   = QColor(255, 255, 255, 25)
DARK_SHADOW_IN    = QColor(0, 0, 0, 180)
DARK_HLIGHT_IN    = QColor(255, 255, 255, 40)


def raised_shadow(radius=8, dark_theme=False):
    if dark_theme:
        return [
            {"outside": True,  "offset": [radius,  radius],
             "blur": radius*1.5, "color": DARK_SHADOW_OUT},
            {"outside": True,  "offset": [-radius, -radius],
             "blur": radius*1.5, "color": DARK_HLIGHT_OUT},
        ]
    else:
        return [
            {"outside": True,  "offset": [radius,  radius],
             "blur": radius*1.5, "color": LIGHT_SHADOW_OUT},
            {"outside": True,  "offset": [-radius, -radius],
             "blur": radius*1.5, "color": LIGHT_HLIGHT_OUT},
        ]


def sunken_shadow(radius=8, dark_theme=False):
    if dark_theme:
        return [
            {"inside": True,   "offset": [radius,  radius],
             "blur": radius, "color": DARK_SHADOW_IN},
            {"inside": True,   "offset": [-radius, -radius],
             "blur": radius, "color": DARK_HLIGHT_IN},
        ]
    else:
        return [
            {"inside": True,   "offset": [radius,  radius],
             "blur": radius, "color": LIGHT_SHADOW_IN},
            {"inside": True,   "offset": [-radius, -radius],
             "blur": radius, "color": LIGHT_HLIGHT_IN},
        ]


class Handle(QWidget):
    """Draggable thumb."""
    def __init__(self, parent=None, dark_theme=False):
        super().__init__(parent)
        self.dark_theme = dark_theme
        self.setMinimumWidth(14)
        self.setMinimumHeight(40)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # logic in bar
        
        # Set background color based on theme
        bg_color = DARK_HANDLE_BG if dark_theme else LIGHT_HANDLE_BG
        self.setStyleSheet(f"background-color: {bg_color.name()};")
        
        # wrap the handle in a shadow to get soft edges
        self.shadow_wrapper = BoxShadowWrapper(self, raised_shadow(dark_theme=dark_theme), border=1, disable_margins=True)
    
    def set_theme(self, dark_theme):
        """Update theme"""
        self.dark_theme = dark_theme
        bg_color = DARK_HANDLE_BG if dark_theme else LIGHT_HANDLE_BG
        self.setStyleSheet(f"background-color: {bg_color.name()};")
        if hasattr(self, 'shadow_wrapper'):
            self.shadow_wrapper.setShadowList(raised_shadow(dark_theme=dark_theme))


class Track(QWidget):
    """Concave track that hosts the handle."""
    def __init__(self, vertical=True, parent=None, dark_theme=False):
        super().__init__(parent)
        self.vertical = vertical
        self.dark_theme = dark_theme
        
        # Set background color based on theme
        bg_color = DARK_BG if dark_theme else LIGHT_BG
        self.setStyleSheet(f"background-color: {bg_color.name()};")
        
        # inner (concave) shadow
        self.shadow_wrapper = BoxShadowWrapper(self, sunken_shadow(dark_theme=dark_theme), border=2, disable_margins=True)
        # handle
        self.handle = Handle(self, dark_theme)

    def set_theme(self, dark_theme):
        """Update theme"""
        self.dark_theme = dark_theme
        bg_color = DARK_BG if dark_theme else LIGHT_BG
        self.setStyleSheet(f"background-color: {bg_color.name()};")
        if hasattr(self, 'shadow_wrapper'):
            self.shadow_wrapper.setShadowList(sunken_shadow(dark_theme=dark_theme))
        self.handle.set_theme(dark_theme)

    # Update handle geometry when the bar value changes ----------------
    def update_position(self, value, maximum):
        bar_len  = self.height() if self.vertical else self.width()
        handle_len = self.handle.height() if self.vertical else self.handle.width()
        span = bar_len - handle_len
        pos  = int(value / maximum * span) if maximum else 0
        if self.vertical:
            self.handle.move(0, pos)
        else:
            self.handle.move(pos, 0)

    # let the parent QScrollArea size‑hint drive dimensions
    def sizeHint(self):
        return QSize(14, 200) if self.vertical else QSize(200, 14)


class NeoScrollBar(QWidget):
    """Scrollbar made of real widgets, so BoxShadow works."""
    def __init__(self, orientation=Qt.Vertical, parent=None, dark_theme=False):
        super().__init__(parent)
        self.vertical = orientation == Qt.Vertical
        self.dark_theme = dark_theme
        layout_cls = QVBoxLayout if self.vertical else QHBoxLayout
        lay = layout_cls(self)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(0)

        self.track = Track(self.vertical, dark_theme=dark_theme)
        lay.addWidget(self.track, 1)

        self._maximum = 1
        self._value   = 0

    def set_theme(self, dark_theme):
        """Update theme"""
        self.dark_theme = dark_theme
        self.track.set_theme(dark_theme)

    # API compatible with QScrollBar subset ----------------------------
    def set_range(self, maximum):
        self._maximum = max(1, maximum)
        self.track.update_position(self._value, self._maximum)

    def set_value(self, value):
        self._value = max(0, min(value, self._maximum))
        self.track.update_position(self._value, self._maximum)

    def sizeHint(self):
        return self.track.sizeHint()


class NeumorphicScrollArea(QScrollArea):
    """Drop‑in replacement that wires its own NeoScrollBars."""
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.dark_theme = True  # Default to dark theme
        self.vbar = NeoScrollBar(Qt.Vertical, self, dark_theme=self.dark_theme)
        self.hbar = NeoScrollBar(Qt.Horizontal, self, dark_theme=self.dark_theme)
        self.setViewportMargins(0, 0, 22, 22)  # room for bars
        self.vbar.move(self.width() - 22, 0)
        self.hbar.move(0, self.height() - 22)
        self.vbar.resize(22, self.height() - 22)
        self.hbar.resize(self.width() - 22, 22)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.viewport().installEventFilter(self)

        # sync positions ------------------------------------------------
        self.verticalScrollBar().valueChanged.connect(
            lambda v: self.vbar.set_value(v))
        self.horizontalScrollBar().valueChanged.connect(
            lambda v: self.hbar.set_value(v))
        self.verticalScrollBar().rangeChanged.connect(
            lambda _, m: self.vbar.set_range(m))
        self.horizontalScrollBar().rangeChanged.connect(
            lambda _, m: self.hbar.set_range(m))

    def set_theme(self, theme_mode):
        """Update the theme for the scroll area and scroll bars"""
        dark_theme = theme_mode == 'dark'
        self.dark_theme = dark_theme
        self.vbar.set_theme(dark_theme)
        self.hbar.set_theme(dark_theme)

    # keep bars stuck to the edges after resize ------------------------
    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self.vbar.move(self.width() - 22, 0)
        self.hbar.move(0, self.height() - 22)
        self.vbar.resize(22, self.height() - 22)
        self.hbar.resize(self.width() - 22, 22)


# ----------------------------- demo -----------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    from PySide6.QtWidgets import QLabel

    lorem = QLabel("\n".join("Lorem ipsum " * 20 for _ in range(100)))
    lorem.setWordWrap(True)

    area = NeumorphicScrollArea()
    area.setWidget(lorem)
    area.resize(420, 260)
    area.show()

    sys.exit(app.exec())
