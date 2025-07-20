import sys
import os
import time
import logging
from typing import Set, Optional, Tuple
from PySide6.QtCore import Qt, QTimer                 # +QTimer

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox,
    QSplitter, QStatusBar, QProgressBar
)
from PySide6.QtCore import Qt

from nip.ui.file_tree   import FileTree
from nip.ui.enhanced_preview_panel import EnhancedPreviewPanel
from nip.ui.toolbar       import NipToolBar
from nip.ui.status_overlay import StatusOverlay, StatusManager
from nip.core.worker      import DiffWorker
from nip.core.fast_diff_worker import FastDiffWorker
from nip.config           import theme_manager, get_theme, apply_theme_to_widget


def snapshot_selection(sel_set: Set[str]) -> Tuple[str, ...]:
    """Create immutable snapshot of selection to prevent mutation during scans"""
    return tuple(sorted(sel_set))


# Configure operational logger for debug messages
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("NIP-Diff")
        self.resize(1100, 750)

        # ── toolbar / status ──────────────────────────────────────────
        self.toolbar = NipToolBar(self)
        self.addToolBar(self.toolbar)
        
        # Enhanced status bar with progress
        status_bar = QStatusBar(self)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_bar.addPermanentWidget(self.progress_bar)
        self.setStatusBar(status_bar)

        # ── splitter ──────────────────────────────────────────────────
        splitter = QSplitter(Qt.Horizontal)
        self.tree    = FileTree()
        self.preview = EnhancedPreviewPanel()
        
        # Status overlay for non-intrusive messages
        self.status_overlay = StatusOverlay(self)
        self.status_manager = StatusManager(self.status_overlay)
        
        splitter.addWidget(self.tree)
        splitter.addWidget(self.preview)
        splitter.setStretchFactor(1, 2)
        self.setCentralWidget(splitter)

        # connections
        self.toolbar.choose_folder.connect(self._on_folder_selected)
        self.toolbar.run.connect(lambda: self._start_fast_diff(is_user_action=True))  # Explicit user action
        self.toolbar.copy.connect(self.preview.copy_all)
        self.toolbar.theme_changed.connect(self._on_theme_changed)  # Connect theme toggle
        # Connect file tree selection changes to immediate scan triggering
        self.tree.selection_changed.connect(self._on_selection_changed)
        # Undo / Export buttons were removed

        self._worker: FastDiffWorker | None = None   # Use fast worker
        self._watcher = None               # LiveWatcher after first Run
        self._latest_scan_id = 0           # Race condition guard - track latest scan request
        self._live_scan_in_progress = False  # Track background live scans separately
        self._debounce = QTimer(singleShot=True)
        self._debounce.setInterval(300)    # ms – lump rapid saves together
        self._debounce.timeout.connect(lambda: self._start_fast_diff(is_user_action=False))  # Live watch = background

    # ------------------------------------------------------------------
    def _on_folder_selected(self, folder_path: str):
        """Handle new folder selection - clear cache and set root"""
        # Clear the cache when switching folders
        from nip.core.cached_diff_engine import cached_diff_engine
        cached_diff_engine.clear_cache()
        
        # Set the new root
        self.tree.set_root(folder_path)
        
        # Clear previous results and show helpful message
        self.preview.clear_sections()
        self.preview.show_text("Folder selected. Click 'Run' (F5) to scan for changes.")
        
        # Show status
        self.status_manager.show_info(f"Selected folder: {os.path.basename(folder_path)}")

    def _on_selection_changed(self, new_selection):
        """Handle immediate file selection changes - trigger scan automatically"""
        logger.debug(f"Selection changed to: {new_selection}")
        
        # Only auto-scan if we have a folder and the selection isn't empty
        if hasattr(self.tree, '_root_path') and self.tree._root_path and new_selection:
            logger.debug("Auto-triggering background scan for new selection")
            self._start_fast_diff(is_user_action=False)  # Background scan, no spinner
        else:
            logger.debug("Skipping auto-scan - no folder or empty selection")

    def _on_theme_changed(self, theme_mode: str):
        """Handle theme change - apply new theme to entire application"""
        logger.debug(f"Theme changed to: {theme_mode}")
        
        # Update theme manager
        theme_manager.set_mode(theme_mode)
        
        # Get new theme
        theme = get_theme(theme_mode)
        
        # Apply to the entire application
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            app.setStyleSheet(theme['qss'])
            
        # Show status message
        self.status_manager.show_info(f"Theme changed to {theme['name']}")
        
        logger.debug(f"Applied {theme['name']} successfully")

    def _start_fast_diff(self, is_user_action: bool = True) -> None:
        """Start fast diff with intelligent caching - allows concurrent requests, discards stale results
        
        Args:
            is_user_action: True for explicit user scans (show spinner), False for background scans (no spinner)
        """
        # Stop any pending debounced scan
        if self._debounce.isActive():
            logger.debug("Stopping pending debounced scan")
            self._debounce.stop()
            
        if self.tree._root_path is None:      # property would raise, test private
            QMessageBox.warning(self, "No folder", "Please choose a folder first.")
            return

        include: Set[str] = self.tree.checked_paths()
        logger.debug(f"Scan triggered - selection: {include}, user_action: {is_user_action}")
        
        if not include:               # nothing checked → show hint, abort
            QMessageBox.information(
                self, "Nothing selected",
                "Tick one or more check-boxes in the tree first "
                "(left-click on a row to toggle)."
            )
            return
            
        # CRITICAL: Create immutable snapshot of selection to prevent mutation during scan
        current_selection = snapshot_selection(include)
        logger.debug(f"Immutable selection snapshot: {current_selection}")
        
        # Convert back to set for compatibility (but this is now a snapshot at this point in time)
        include_paths: Optional[Set[str]] = set(current_selection)
        
        # Show progress only for explicit user actions
        if is_user_action:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.statusBar().showMessage("Scanning changes…", 0)
        else:
            # For background scans, track internally but don't show spinner
            self._live_scan_in_progress = True

        # Increment scan ID to guard against race conditions (instead of blocking)
        self._latest_scan_id += 1
        current_scan_id = self._latest_scan_id
        logger.debug(f"Starting scan with ID {current_scan_id} (user_action: {is_user_action})")

        # stop previous worker if it's still alive (rare)
        if self._worker and self._worker.isRunning():
            self._worker._cancelled = True
            self._worker.wait()

        self._worker = FastDiffWorker(self.tree.root_path, include_paths, self._on_diff_done, current_scan_id, is_user_action)
        self._worker.progress.connect(self._on_progress)
        self._worker.status_message.connect(self._on_status_message)
        self._worker.operational_log.connect(self._on_operational_log)
        
        # Connect to scan_completed with race condition guard
        self._worker.scan_completed.connect(self._on_scan_completed)
        
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.finished.connect(lambda _=None: setattr(self, "_worker", None))
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.start()

        # one-time setup – start filesystem watcher after first Run OK
        if self._watcher is None and self.toolbar.act_live.isChecked():
            from nip.core.worker import LiveWatcher
            self._watcher = LiveWatcher(
                self.tree.root_path,
                lambda: self._debounce.start()      # debounce rapid events
            )

    def _on_scan_completed(self, scan_id: int, sections_data: list, cache_key: str):
        """Handle scan completion with race condition guard"""
        logger.debug(f"Scan {scan_id} completed, latest is {self._latest_scan_id}")
        
        # Guard against race conditions - ignore stale responses
        if scan_id != self._latest_scan_id:
            logger.debug(f"IGNORING stale scan {scan_id} (latest: {self._latest_scan_id})")
            return
            
        # This is the latest scan, update the UI with cache key for forced re-render
        logger.debug(f"ACCEPTING current scan {scan_id}, updating UI with cache key {cache_key}")
        
        # ASSERTION: Ensure cache key is not empty
        assert cache_key, f"Cache key must not be empty here. Scan ID: {scan_id}"
        
        if hasattr(self.preview, 'show_sections'):
            self.preview.show_sections(sections_data, cache_key)

    def _on_worker_finished(self):
        """Clean up after worker finishes"""
        self.progress_bar.setVisible(False)
        self._live_scan_in_progress = False

    def _on_status_message(self, message: str, message_type: str, is_user_action: bool):
        """Handle user-facing status messages via overlay (only for user actions)"""
        if is_user_action:  # Only show status overlay for explicit user actions
            if message_type == "info":
                self.status_manager.show_info(message)
            elif message_type == "success":
                self.status_manager.show_success(message)
            elif message_type == "warning":
                self.status_manager.show_warning(message)
            elif message_type == "error":
                self.status_manager.show_error(message)
        else:
            # For background scans, just log operationally
            logger.debug(f"Background scan {message_type}: {message}")

    def _on_operational_log(self, message: str, level: str):
        """Handle operational debug messages - always go to logger"""
        if level == "debug":
            logger.debug(message)
        elif level == "info":
            logger.info(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)

    def _on_progress(self, message: str, is_user_action: bool):
        """Handle progress updates - only show for user actions"""
        if is_user_action:
            self.statusBar().showMessage(message, 0)
        else:
            logger.debug(f"Background progress: {message}")

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

        # one-time setup – start filesystem watcher after first Run OK
        if self._watcher is None:
            from nip.core.worker import LiveWatcher
            self._watcher = LiveWatcher(
                self.tree.root_path,
                lambda: self._debounce.start()      # debounce rapid events
            )

    def _on_diff_done(self, text: str) -> None:
        """Legacy callback for compatibility - main processing now happens via scan_completed signal"""
        logger.debug("Legacy diff callback triggered")
        # Note: Main UI updates now happen via _on_scan_completed signal
        # This is kept for compatibility with the finished signal

    def resizeEvent(self, event):
        """Handle window resize to reposition status overlay"""
        super().resizeEvent(event)
        if hasattr(self, 'status_overlay') and self.status_overlay.isVisible():
            self.status_overlay._position_overlay()

# ----------------------------------------------------------------------
def run_app() -> None:
    app = QApplication(sys.argv)
    
    # Apply unified theme system - default to dark theme
    theme = get_theme('dark')
    app.setStyleSheet(theme['qss'])

    win = MainWindow()
    # centre on primary screen
    screen = app.primaryScreen().availableGeometry()
    win.move((screen.width()-win.width())//2, (screen.height()-win.height())//2)

    win.show()
    sys.exit(app.exec())
