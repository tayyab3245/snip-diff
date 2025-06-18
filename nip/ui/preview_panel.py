# nip/ui/preview_panel.py
"""
Preview panel that shows a full unified diff, colour-codes it à-la VS Code,
and supports Ctrl+F searching.

Hard-deps:  pip install pygments
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QGuiApplication, QTextCharFormat, QColor, QFont, QTextCursor,
    QSyntaxHighlighter,
)
from PySide6.QtWidgets import (
    QPlainTextEdit, QWidget, QVBoxLayout, QInputDialog
)

from pygments import lex
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.token import Token


# ────────────────────────────────────────────────────────────────────────
def _fmt(col: str) -> QTextCharFormat:
    f = QTextCharFormat()
    f.setForeground(QColor(col))
    f.setFont(QFont("Menlo, Consolas, monospace"))
    return f


class _DiffHighlighter(QSyntaxHighlighter):
    """
    Highlights a unified diff:

      • green  “+”  added lines
      • red    “-”  removed lines
      • grey   “ ”  context
      • amber  headers (--- / +++ / @@)
      • inside each line: VS-Code-like syntax colours via *pygments*
    """
    fmt_add = _fmt("#00E676")
    fmt_del = _fmt("#FF5370")
    fmt_hdr = _fmt("#FFD740")
    fmt_ctx = _fmt("#AAAAAA")

    # VS-Code-ish token palette
    token_map = {
        Token.Keyword:         _fmt("#C792EA"),
        Token.Name:            _fmt("#FFFFFF"),
        Token.Comment:         _fmt("#546E7A"),
        Token.String:          _fmt("#C3E88D"),
        Token.Number:          _fmt("#F78C6C"),
        Token.Operator:        _fmt("#89DDFF"),
        Token.Punctuation:     _fmt("#89DDFF"),
        Token.Name.Function:   _fmt("#82AAFF"),
        Token.Name.Class:      _fmt("#FFCB6B"),
        Token.Name.Decorator:  _fmt("#82AAFF"),
    }

    def __init__(self, doc):
        super().__init__(doc)
        self._current_path = ""      # updated on every --- a/foo.py header

    # called from PreviewPanel when a new file block starts -------------
    def set_current_file(self, path: str) -> None:
        self._current_path = path

    # ------------------------------------------------------------------
    def highlightBlock(self, text: str) -> None:
        if not text:                   # blank line
            return

        # colour the whole line by diff prefix
        if text.startswith("+"):
            self.setFormat(0, len(text), self.fmt_add)
        elif text.startswith("-"):
            self.setFormat(0, len(text), self.fmt_del)
        elif text.startswith("@@") or text.startswith("---") or text.startswith("+++"):
            self.setFormat(0, len(text), self.fmt_hdr)
        else:
            self.setFormat(0, len(text), self.fmt_ctx)

        # only lex code for context / added / removed lines
        prefix, body = text[0], text[1:]
        if prefix not in " +-":
            return

        try:
            lexer = get_lexer_for_filename(self._current_path, stripnl=False)
        except Exception:
            lexer = TextLexer()

        col = 1  # skip diff prefix
        for ttype, value in lex(body, lexer):
            length = len(value)
            if fmt := self.token_map.get(ttype):
                self.setFormat(col, length, fmt)
            col += length


# ────────────────────────────────────────────────────────────────────────
class PreviewPanel(QWidget):
    """Read-only diff viewer with Copy All and Ctrl+F search."""
    def __init__(self, parent=None):
        super().__init__(parent)

        self._view = QPlainTextEdit(readOnly=True)
        self.highlighter = _DiffHighlighter(self._view.document())

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._view)

        self._last_find: str = ""

    # ----- search ------------------------------------------------------
    def start_search(self) -> None:
        term, ok = QInputDialog.getText(self, "Find", "Text:")
        if ok and term:
            self._last_find = term
            self._find_next()

    def _find_next(self) -> None:
        if not self._view.find(self._last_find):
            cursor = self._view.textCursor()
            cursor.movePosition(QTextCursor.Start)
            self._view.setTextCursor(cursor)
            self._view.find(self._last_find)

    # ----- public API --------------------------------------------------
    def show_text(self, text: str) -> None:
        """
        Feed a *full* unified diff string.  We split on file headers so the
        highlighter can choose an appropriate lexer for each block.
        """
        self._view.clear()

        for block in text.split("\n--- a/"):
            if not block.strip():
                continue
            header, *rest = block.splitlines()
            path = header.split(" ", 1)[0]           # “a/foo/bar.py”
            self.highlighter.set_current_file(path[2:])  # drop leading “a/”

            self._view.appendPlainText(f"--- a/{block}")

        self._view.moveCursor(QTextCursor.Start)

    # convenience
    def copy_all(self) -> None:
        QGuiApplication.clipboard().setText(self._view.toPlainText())
