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
        b.setStyleSheet(f"""
            QPushButton {{
                background:{col};
                border:none;
                border-radius:3px;        /* square-ish */
            }}
            QPushButton:hover {{ filter:brightness(115%); }}
            QPushButton:pressed {{ filter:brightness(85%); }}
        """)
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
