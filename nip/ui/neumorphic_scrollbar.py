# neumorphic_scrollbar.py
import sys
from PySide6.QtCore    import Qt, QRect, QSize, QPoint
from PySide6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QApplication
from PySide6.QtGui     import QColor
from .neumorphism.Neumorphism import BoxShadowWrapper            # your cloned file

# Minimum handle height to ensure usability
MIN_HANDLE_HEIGHT = 40


def raised_shadow(radius=8, shadow_color=None, highlight_color=None):
    """Create raised shadow effect using provided colors"""
    shadow_color = shadow_color or QColor(0, 0, 0, 128)
    highlight_color = highlight_color or QColor(255, 255, 255, 25)
    
    return [
        {"outside": True,  "offset": [radius,  radius],
         "blur": radius*1.5, "color": shadow_color},
        {"outside": True,  "offset": [-radius, -radius],
         "blur": radius*1.5, "color": highlight_color},
    ]


def sunken_shadow(radius=8, shadow_color=None, highlight_color=None):
    """Create sunken shadow effect using provided colors"""
    shadow_color = shadow_color or QColor(0, 0, 0, 180)
    highlight_color = highlight_color or QColor(255, 255, 255, 40)
    
    return [
        {"inside": True,   "offset": [radius,  radius],
         "blur": radius, "color": shadow_color},
        {"inside": True,   "offset": [-radius, -radius],
         "blur": radius, "color": highlight_color},
    ]


class Handle(QWidget):
    """Draggable thumb."""
    def __init__(self, parent=None, theme_colors=None):
        super().__init__(parent)
        self.theme_colors = theme_colors or {}
        self.setMinimumWidth(14)
        self.setMinimumHeight(40)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # logic in bar
        
        # Set background color from theme
        bg_color = QColor(self.theme_colors.get('scrollbar_handle_bg', '#2a2a2e'))
        self.setStyleSheet(f"background-color: {bg_color.name()};")
        
        # wrap the handle in a shadow to get soft edges
        shadow_color = QColor(self.theme_colors.get('scrollbar_shadow_out', 'rgba(0, 0, 0, 0.5)'))
        highlight_color = QColor(self.theme_colors.get('scrollbar_highlight_out', 'rgba(255, 255, 255, 0.1)'))
        self.shadow_wrapper = BoxShadowWrapper(self, raised_shadow(shadow_color=shadow_color, highlight_color=highlight_color), border=1, disable_margins=True)
    
    def set_theme(self, theme_colors):
        """Update theme"""
        self.theme_colors = theme_colors
        bg_color = QColor(theme_colors.get('scrollbar_handle_bg', '#2a2a2e'))
        self.setStyleSheet(f"background-color: {bg_color.name()};")
        if hasattr(self, 'shadow_wrapper'):
            shadow_color = QColor(theme_colors.get('scrollbar_shadow_out', 'rgba(0, 0, 0, 0.5)'))
            highlight_color = QColor(theme_colors.get('scrollbar_highlight_out', 'rgba(255, 255, 255, 0.1)'))
            self.shadow_wrapper.setShadowList(raised_shadow(shadow_color=shadow_color, highlight_color=highlight_color))


class Track(QWidget):
    """Concave track that hosts the handle."""
    def __init__(self, vertical=True, parent=None, theme_colors=None):
        super().__init__(parent)
        self.vertical = vertical
        self.theme_colors = theme_colors or {}
        
        # Set background color from theme
        bg_color = QColor(self.theme_colors.get('scrollbar_track_bg', '#232428'))
        self.setStyleSheet(f"background-color: {bg_color.name()};")
        
        # inner (concave) shadow
        shadow_color = QColor(self.theme_colors.get('scrollbar_shadow_in', 'rgba(0, 0, 0, 0.7)'))
        highlight_color = QColor(self.theme_colors.get('scrollbar_highlight_in', 'rgba(58, 58, 58, 0.8)'))
        self.shadow_wrapper = BoxShadowWrapper(self, sunken_shadow(shadow_color=shadow_color, highlight_color=highlight_color), border=2, disable_margins=True)
        # handle
        self.handle = Handle(self, theme_colors)

    def set_theme(self, theme_colors):
        """Update theme"""
        self.theme_colors = theme_colors
        bg_color = QColor(theme_colors.get('scrollbar_track_bg', '#232428'))
        self.setStyleSheet(f"background-color: {bg_color.name()};")
        if hasattr(self, 'shadow_wrapper'):
            shadow_color = QColor(theme_colors.get('scrollbar_shadow_in', 'rgba(0, 0, 0, 0.7)'))
            highlight_color = QColor(theme_colors.get('scrollbar_highlight_in', 'rgba(58, 58, 58, 0.8)'))
            self.shadow_wrapper.setShadowList(sunken_shadow(shadow_color=shadow_color, highlight_color=highlight_color))
        self.handle.set_theme(theme_colors)

    # Update handle geometry when the bar value changes ----------------
    def update_position(self, value, maximum, page_step=10):
        bar_height = self.height() if self.vertical else self.width()
        
        # --- START NEW LOGIC ---
        
        # Calculate the total content height (maximum is content_height - viewport_height)
        total_content_height = maximum + page_step
        
        # Calculate the ideal proportional handle height
        if total_content_height > 0:
            ideal_handle_height = int(bar_height * (page_step / total_content_height))
        else:
            # If there's no content, the handle should fill the bar
            ideal_handle_height = bar_height
        
        # Enforce the minimum height constant defined at the top of the file
        final_handle_size = max(MIN_HANDLE_HEIGHT, ideal_handle_height)
        
        # --- END NEW LOGIC ---
        
        # Apply the size
        if self.vertical:
            self.handle.setFixedHeight(final_handle_size)
        else:
            self.handle.setFixedWidth(final_handle_size)

        # Calculate position using the final handle size
        available_space = bar_height - final_handle_size
        if maximum > 0:
            pos = int((value / maximum) * available_space)
        else:
            pos = 0
        
        # Clamp position to valid range
        pos = max(0, min(pos, available_space))
        
        if self.vertical:
            self.handle.move(0, pos)
        else:
            self.handle.move(pos, 0)

    # let the parent QScrollArea size‑hint drive dimensions
    def sizeHint(self):
        return QSize(14, 200) if self.vertical else QSize(200, 14)


class NeoScrollBar(QWidget):
    """Scrollbar made of real widgets, so BoxShadow works."""
    def __init__(self, orientation=Qt.Vertical, parent=None, theme_colors=None):
        super().__init__(parent)
        self.vertical = orientation == Qt.Vertical
        self.theme_colors = theme_colors or {}
        layout_cls = QVBoxLayout if self.vertical else QHBoxLayout
        lay = layout_cls(self)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(0)

        self.track = Track(self.vertical, theme_colors=theme_colors)
        lay.addWidget(self.track, 1)

        self._maximum = 1
        self._value   = 0
        self._page_step = 10  # Default page step

    def set_theme(self, theme_colors):
        """Update theme"""
        self.theme_colors = theme_colors
        self.track.set_theme(theme_colors)

    # API compatible with QScrollBar subset ----------------------------
    def set_range(self, maximum):
        self._maximum = max(1, maximum)
        self.track.update_position(self._value, self._maximum, self._page_step)

    def set_value(self, value):
        self._value = max(0, min(value, self._maximum))
        self.track.update_position(self._value, self._maximum, self._page_step)
    
    def set_page_step(self, page_step):
        self._page_step = max(1, page_step)
        self.track.update_position(self._value, self._maximum, self._page_step)

    def sizeHint(self):
        return self.track.sizeHint()


class NeumorphicScrollArea(QScrollArea):
    """Drop‑in replacement that wires its own NeoScrollBars."""
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.theme_colors = {}  # Default empty theme colors
        self.vbar = NeoScrollBar(Qt.Vertical, self, theme_colors=self.theme_colors)
        self.hbar = NeoScrollBar(Qt.Horizontal, self, theme_colors=self.theme_colors)
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
        
        # sync page step for proper handle sizing
        def update_v_page_step():
            page_step = self.verticalScrollBar().pageStep()
            self.vbar.set_page_step(page_step)
        
        def update_h_page_step():
            page_step = self.horizontalScrollBar().pageStep()
            self.hbar.set_page_step(page_step)
        
        # Update page step whenever scrollbar properties change
        self.verticalScrollBar().rangeChanged.connect(lambda _, __: update_v_page_step())
        self.horizontalScrollBar().rangeChanged.connect(lambda _, __: update_h_page_step())
        
        # Initial page step sync
        update_v_page_step()
        update_h_page_step()

    def set_theme(self, theme_colors):
        """Update the theme for the scroll area and scroll bars"""
        self.theme_colors = theme_colors
        self.vbar.set_theme(theme_colors)
        self.hbar.set_theme(theme_colors)

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
