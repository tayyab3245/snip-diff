import sys
from typing import Set, Optional

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox,
    QSplitter, QStatusBar
)
from PySide6.QtCore import Qt

from nip.ui.file_tree   import FileTree
from nip.ui.preview_panel import PreviewPanel
from nip.ui.toolbar       import NipToolBar
from nip.core.worker      import DiffWorker
from nip.config           import STYLE


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("NIP-Diff")
        self.resize(1100, 750)

        # ── toolbar / status ──────────────────────────────────────────
        self.toolbar = NipToolBar(self)
        self.addToolBar(self.toolbar)
        self.setStatusBar(QStatusBar(self))

        # ── splitter ──────────────────────────────────────────────────
        splitter = QSplitter(Qt.Horizontal)
        self.tree    = FileTree()
        self.preview = PreviewPanel()
        splitter.addWidget(self.tree)
        splitter.addWidget(self.preview)
        splitter.setStretchFactor(1, 2)
        self.setCentralWidget(splitter)

        # connections
        self.toolbar.choose_folder.connect(self.tree.set_root)
        self.toolbar.run.connect(self._start_diff)
        self.toolbar.copy.connect(self.preview.copy_all)
        self.toolbar.undo.connect(self.tree.clear_snapshot)
        self.toolbar.export.connect(self.preview.export_to_file)

        self._worker: DiffWorker | None = None   # keep reference!

    # ------------------------------------------------------------------
    def _start_diff(self) -> None:
        if self.tree._root_path is None:      # property would raise, test private
            QMessageBox.warning(self, "No folder", "Please choose a folder first.")
            return

        include: Set[str] = self.tree.checked_paths()
        if not include:               # nothing checked → show hint, abort
            QMessageBox.information(
                self, "Nothing selected",
                "Tick one or more check-boxes in the tree first "
                "(left-click on a row to toggle)."
            )
            return
        include_paths: Optional[Set[str]] = include
        self.statusBar().showMessage("Running…", 0)

        # stop previous worker if it’s still alive (rare)
        if self._worker and self._worker.isRunning():
            self._worker.terminate()
            self._worker.wait()

        self._worker = DiffWorker(self.tree.root_path, include_paths, self._on_diff_done)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.finished.connect(lambda _=None: setattr(self, "_worker", None))
        self._worker.start()

    def _on_diff_done(self, text: str) -> None:
        self.preview.show_text(text)
        self.statusBar().showMessage("Done.", 3000)

# ----------------------------------------------------------------------
def run_app() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    win = MainWindow()
    # centre on primary screen
    screen = app.primaryScreen().availableGeometry()
    win.move((screen.width()-win.width())//2, (screen.height()-win.height())//2)

    win.show()
    sys.exit(app.exec())
