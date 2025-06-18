from PySide6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QFileDialog
from PySide6.QtGui import QGuiApplication


class PreviewPanel(QWidget):
    """
    Read-only text viewer + helper actions (copy/export).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = QPlainTextEdit(readOnly=True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._text)

    # --------------------------------------------------
    def show_text(self, text: str):
        self._text.setPlainText(text)

    def copy_all(self):
        QGuiApplication.clipboard().setText(self._text.toPlainText())

    def export_to_file(self):
        name, _ = QFileDialog.getSaveFileName(self, "Export diff", "diff.txt", "Text (*.txt)")
        if not name:
            return
        with open(name, "w", encoding="utf-8") as fh:
            fh.write(self._text.toPlainText())
