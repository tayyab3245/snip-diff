import sys
import os
import time
import logging
from typing import Set, Optional, Tuple
from PySide6.QtCore import Qt, QTimer                 # +QTimer

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox,
    QSplitter, QStatusBar, QProgressBar, QWidget, QVBoxLayout
)

from nip.ui.file_tree   import FileTree
from nip.ui.enhanced_preview_panel import EnhancedPreviewPanel
from nip.ui.toolbar_neumorphic import NipToolBar
from nip.ui.status_overlay import StatusOverlay, StatusManager
from nip.core.worker      import DiffWorker
from nip.core.fast_diff_worker import FastDiffWorker
from nip.config           import theme_manager


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
        self.tree.setObjectName("leftPanel")  # Set object name for CSS styling
        
        # Create a wrapper widget for the preview panel to hold carved styling
        self.preview_wrapper = QWidget()
        self.preview_wrapper.setObjectName("rightPanel")
        
        self.preview = EnhancedPreviewPanel()
        
        # Layout the preview inside the wrapper with margins to show wrapper background
        wrapper_layout = QVBoxLayout(self.preview_wrapper)
        wrapper_layout.setContentsMargins(16, 16, 16, 16)  # Original margins for proper carved look
        wrapper_layout.addWidget(self.preview)
        
        # Status overlay for non-intrusive messages
        self.status_overlay = StatusOverlay(self)
        self.status_manager = StatusManager(self.status_overlay)
        
        splitter.addWidget(self.tree)
        splitter.addWidget(self.preview_wrapper)  # Add wrapper instead of preview directly
        splitter.setStretchFactor(1, 2)
        self.setCentralWidget(splitter)
        
        # Set up central theme system and apply initial theme
        self._setup_connections()
        self._apply_theme()
        
        # Show welcome message on startup
        welcome_text = (
            "Welcome to NIP-Diff!\n\n"
            "📁 Choose a folder to begin\n"
            "📄 Select files to view differences\n"
            "🔄 Changes are scanned automatically\n\n"
            "Use the toolbar to choose a folder and get started."
        )
        self.preview.show_text(welcome_text)

        self._worker: FastDiffWorker | None = None   # Use fast worker
        self._watcher = None               # LiveWatcher after first Run
        self._latest_scan_id = 0           # Race condition guard - track latest scan request
        self._live_scan_in_progress = False  # Track background live scans separately
        self._debounce = QTimer(singleShot=True)
        self._debounce.setInterval(300)    # ms – lump rapid saves together
        self._debounce.timeout.connect(lambda: (print("DEBUG: Debounce timer fired!"), self._start_fast_diff(is_user_action=False))[1])  # Live watch = background

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
        self.preview.show_text("Folder selected. Select files in the tree to view differences.")
        
        # Show status
        self.status_manager.show_info(f"Selected folder: {os.path.basename(folder_path)}")

    def _on_selection_changed(self, new_selection):
        """Handle immediate file selection changes - trigger scan automatically with debouncing"""
        print(f"DEBUG: MainWindow received selection_changed signal with {len(new_selection)} files")
        logger.debug(f"Selection changed to: {new_selection}")
        
        # Auto-scan if we have a folder (regardless of selection state)
        if hasattr(self.tree, '_root_path') and self.tree._root_path:
            print(f"DEBUG: Auto-triggering scan for folder {self.tree._root_path}")
            logger.debug("Auto-triggering debounced background scan for selection change")
            # Use debouncing to handle rapid selection changes
            self._debounce.start()  # This will restart the timer if already active
        else:
            print("DEBUG: Skipping auto-scan - no folder selected")
            logger.debug("Skipping auto-scan - no folder selected")

    def _setup_connections(self):
        """Set up all signal connections"""
        # Connect toolbar signals
        self.toolbar.choose_folder.connect(self._on_folder_selected)
        self.toolbar.copy.connect(self.preview.copy_all)
        self.toolbar.theme_changed.connect(self._on_theme_changed)  # Connect theme toggle
        
        # Connect file tree selection changes to immediate scan triggering
        self.tree.selection_changed.connect(self._on_selection_changed)
        print("DEBUG: Connected tree.selection_changed to _on_selection_changed")

    def _apply_theme(self):
        """Apply the current theme using the central theme system"""
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            # Get the current theme's QSS and apply it globally
            qss = theme_manager.get_qss()
            app.setStyleSheet(qss)
            print(f"✓ Applied central theme: {theme_manager.mode} mode")
            
        # Update neumorphic scroll bars in preview panel with complete color dictionary
        if hasattr(self, 'preview') and hasattr(self.preview, 'set_theme'):
            theme_colors = theme_manager.get_colors()
            self.preview.set_theme(theme_colors)

    def _on_theme_changed(self, theme_mode: str):
        """Handle theme change using central theme system"""
        logger.debug(f"Theme changed to: {theme_mode}")
        
        # Update theme manager
        theme_manager.set_mode(theme_mode)
        
        # Apply the new theme using central system
        self._apply_theme()
            
        # Show status message
        theme_name = "Dark" if theme_mode == 'dark' else "Light"
        self.status_manager.show_info(f"Applied {theme_name} Theme successfully")
        logger.debug(f"Applied {theme_name} Theme successfully")

    def _start_fast_diff(self, is_user_action: bool = True) -> None:
        """Start fast diff with intelligent caching - allows concurrent requests, discards stale results
        
        Args:
            is_user_action: True for explicit user scans (show spinner), False for background scans (no spinner)
        """
        print(f"DEBUG: _start_fast_diff called with is_user_action={is_user_action}")
        
        # Stop any pending debounced scan
        if self._debounce.isActive():
            logger.debug("Stopping pending debounced scan")
            self._debounce.stop()
            
        if self.tree._root_path is None:      # property would raise, test private
            print("DEBUG: No folder selected, showing warning")
            QMessageBox.warning(self, "No folder", "Please choose a folder first.")
            return

        include: Set[str] = self.tree.checked_paths()
        print(f"DEBUG: Checked paths: {include}")
        logger.debug(f"Scan triggered - selection: {include}, user_action: {is_user_action}")
        
        if not include:               # nothing checked → clear preview or show hint
            if is_user_action:
                # Only show message for explicit user actions, not automatic scans
                QMessageBox.information(
                    self, "Nothing selected",
                    "Tick one or more check-boxes in the tree first "
                    "(left-click on a row to toggle)."
                )
            else:
                # For automatic scans with empty selection, just clear the preview
                logger.debug("Empty selection in automatic scan - clearing preview")
                self.preview.show_text("Select files to view differences")
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
        if self._watcher is None and self.toolbar.btn_live._button.isChecked():
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

    def showEvent(self, event):
        """Handle window show event to ensure proper styling is applied"""
        super().showEvent(event)
        # Reapply theme when window becomes visible
        if hasattr(self, 'preview_wrapper'):
            self._apply_theme()

# ----------------------------------------------------------------------
def run_app() -> None:
    app = QApplication(sys.argv)
    
    # Initialize theme manager and apply default theme
    theme_manager.set_mode('dark')  # Default to dark theme
    qss = theme_manager.get_qss()
    app.setStyleSheet(qss)

    win = MainWindow()
    # centre on primary screen
    screen = app.primaryScreen().availableGeometry()
    win.move((screen.width()-win.width())//2, (screen.height()-win.height())//2)

    win.show()
    sys.exit(app.exec())
