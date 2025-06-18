"""
Preview panel with syntax-highlighted unified diff.
"""

from PySide6.QtGui     import QGuiApplication, QTextCharFormat, QColor, QFont, QSyntaxHighlighter
from PySide6.QtWidgets import (
    QPlainTextEdit, QWidget, QVBoxLayout, QFileDialog
)


# ──────────────────────────────────────────────────────────────────────────
class _DiffHighlighter(QSyntaxHighlighter):
    """
    Colourises unified-diff in real time.
    +  green  – added lines
    +  red    – removed lines
    +  grey   – context
    +  yellow – headers / separator lines
    """
    def __init__(self, doc):
        super().__init__(doc)
        self.fmt_add    = self._fmt("#00E676")   # bright green
        self.fmt_del    = self._fmt("#FF5370")   # coral red
        self.fmt_hdr    = self._fmt("#FFD740")   # amber
        self.fmt_ctx    = self._fmt("#9E9E9E")   # mid grey

    @staticmethod
    def _fmt(col: str) -> QTextCharFormat:
        f = QTextCharFormat()
        f.setForeground(QColor(col))
        f.setFont(QFont("Menlo, Consolas, monospace"))
        return f

    # -------------------------------------------------------------- #
    def highlightBlock(self, text: str):
        if text.startswith("+"):
            self.setFormat(0, len(text), self.fmt_add)
        elif text.startswith("-"):
            self.setFormat(0, len(text), self.fmt_del)
        elif text.startswith("@@") or text.startswith("---") or text.startswith("+++"):
            self.setFormat(0, len(text), self.fmt_hdr)
        else:
            self.setFormat(0, len(text), self.fmt_ctx)


# ──────────────────────────────────────────────────────────────────────────
class PreviewPanel(QWidget):
    """Read-only diff viewer with Copy / Export actions."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._view = QPlainTextEdit()
        self._view.setReadOnly(True)
        _DiffHighlighter(self._view.document())   # attach highlighter

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._view)

    # public helpers -------------------------------------------------- #
    def show_text(self, text: str):
        self._view.setPlainText(text)

    def copy_all(self):
        QGuiApplication.clipboard().setText(self._view.toPlainText())

    def export_to_file(self):
        name, _ = QFileDialog.getSaveFileName(self, "Export diff", "diff.txt", "Text (*.txt)")
        if name:
            with open(name, "w", encoding="utf-8") as fh:
                fh.write(self._view.toPlainText())
