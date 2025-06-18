from PySide6.QtWidgets import QToolBar, QFileDialog
from PySide6.QtGui     import QAction
from PySide6.QtCore    import Signal      # ← add this

class NipToolBar(QToolBar):
    """
    Emits high-level signals; MainWindow wires them up.
    """
    choose_folder = Signal(str)
    run   = Signal()
    copy  = Signal()
    undo  = Signal()
    export = Signal()

    def __init__(self, parent=None):
        super().__init__("Actions", parent)

        # ---- Choose Folder ---------------------------------------------
        act_choose = QAction("Choose Folder")
        act_choose.setShortcut("Ctrl+O")
        act_choose.triggered.connect(self._on_choose)
        self.addAction(act_choose)

        # ---- Run --------------------------------------------------------
        act_run = QAction("Run")
        act_run.setShortcut("F5")
        act_run.triggered.connect(self.run)
        self.addAction(act_run)

        # ---- Copy Output -----------------------------------------------
        act_copy = QAction("Copy Output")
        act_copy.setShortcut("Ctrl+C")
        act_copy.triggered.connect(self.copy)
        self.addAction(act_copy)

        # ---- Undo Snapshot ---------------------------------------------
        act_undo = QAction("Undo Snapshot")
        act_undo.triggered.connect(self.undo)
        self.addAction(act_undo)

        # ---- Export diff -----------------------------------------------
        act_export = QAction("Export")
        act_export.setShortcut("Ctrl+S")
        act_export.triggered.connect(self.export)
        self.addAction(act_export)

    # ------------------------------------------------------------------
    def _on_choose(self):
        folder = QFileDialog.getExistingDirectory(self.parent(), "Select folder")
        if folder:
            self.choose_folder.emit(folder)
