import sys
from typing import Set

from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QSplitter, QWidget, QVBoxLayout, QStatusBar
from PySide6.QtCore import Qt

from nip.ui.file_tree import FileTree
from nip.ui.preview_panel import PreviewPanel
from nip.ui.toolbar import NipToolBar
from nip.core.worker import DiffWorker
from nip.config import STYLE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NIP-Diff")
        self.resize(1100, 750)

        # ---- central splitter ----------------------------------------
        splitter = QSplitter(Qt.Horizontal)
        self.tree    = FileTree()
        self.preview = PreviewPanel()

        splitter.addWidget(self.tree)
        splitter.addWidget(self.preview)
        splitter.setStretchFactor(1, 2)

        # ---- top toolbar + status bar ---------------------------------
        self.toolbar = NipToolBar(self)
        self.addToolBar(self.toolbar)
        self.setStatusBar(QStatusBar())

        # ---- root widget ----------------------------------------------
        central = QWidget()
        lay = QVBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(splitter)
        self.setCentralWidget(central)

        # ---- wiring signals -------------------------------------------
        self.toolbar.choose_folder.connect(self.tree.set_root)
        self.toolbar.run.connect(self._start_diff)
        self.toolbar.copy.connect(self.preview.copy_all)
        self.toolbar.undo.connect(self.tree.clear_snapshot)
        self.toolbar.export.connect(self.preview.export_to_file)

    # ------------------------------------------------------------------
    def _start_diff(self):
        if not self.tree.root_path:
            QMessageBox.warning(self, "No folder", "Please choose a folder first.")
            return

        include: Set[str] = self.tree.checked_paths()
        self.statusBar().showMessage("Running…", 0)

        worker = DiffWorker(self.tree.root_path, include, self._on_diff_done)
        worker.start()

    def _on_diff_done(self, text: str):
        self.preview.show_text(text)
        self.statusBar().showMessage("Done.", 3000)


# ----------------------------------------------------------------------
def run_app():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
