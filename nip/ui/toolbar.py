from PySide6.QtCore    import Signal, Qt
from PySide6.QtGui     import QAction
from PySide6.QtWidgets import QToolBar, QFileDialog


class NipToolBar(QToolBar):
    """
    Emits high-level signals consumed by MainWindow.
    The toolbar shows plain text buttons so it’s visible even without icons.
    """
    choose_folder = Signal(str)
    run           = Signal()
    copy          = Signal()
    undo          = Signal()
    export        = Signal()

    def __init__(self, parent=None):
        super().__init__("Actions", parent)

        # Make sure text is always visible (no icons supplied)
        self.setToolButtonStyle(Qt.ToolButtonTextOnly)

        # Choose Folder ────────────────────────────────────────────────
        act_choose = QAction("Choose Folder", self)
        act_choose.setShortcut("Ctrl+O")
        act_choose.setToolTip("Select a root folder to diff (Ctrl+O)")
        act_choose.triggered.connect(self._on_choose)
        self.addAction(act_choose)

        # Run / Refresh diff ───────────────────────────────────────────
        act_run = QAction("Run", self)
        act_run.setShortcut("F5")
        act_run.setToolTip("Scan and build diff (F5)")
        act_run.triggered.connect(self.run)
        self.addAction(act_run)

        # Copy Output ─────────────────────────────────────────────────
        act_copy = QAction("Copy Output", self)
        act_copy.setShortcut("Ctrl+C")
        act_copy.setToolTip("Copy diff text to clipboard (Ctrl+C)")
        act_copy.triggered.connect(self.copy)
        self.addAction(act_copy)

        # Undo Snapshot ───────────────────────────────────────────────
        act_undo = QAction("Undo Snapshot", self)
        act_undo.setToolTip("Delete .nip_snapshot.json in the root folder")
        act_undo.triggered.connect(self.undo)
        self.addAction(act_undo)

        # Export diff ────────────────────────────────────────────────
        act_export = QAction("Export", self)
        act_export.setShortcut("Ctrl+S")
        act_export.setToolTip("Save diff to a text file (Ctrl+S)")
        act_export.triggered.connect(self.export)
        self.addAction(act_export)

    # ─────────────────────────────────────────────────────────────────
    def _on_choose(self):
        folder = QFileDialog.getExistingDirectory(self.parent(), "Select folder")
        if folder:
            self.choose_folder.emit(folder)