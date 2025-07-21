from PySide6.QtCore    import Signal, Qt, QTimer
from PySide6.QtGui     import QAction, QColor
from PySide6.QtWidgets import QToolBar, QFileDialog, QPushButton, QWidget, QHBoxLayout, QSizePolicy
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Neumorphism.Neumorphism import BoxShadow, BoxShadowWrapper


class NipToolBar(QToolBar):
    """
    Neumorphic toolbar with shadow effects.
    Emits high-level signals consumed by MainWindow.
    """
    choose_folder = Signal(str)
    run           = Signal()
    copy          = Signal()
    undo          = Signal()
    export        = Signal()
    theme_changed = Signal(str)  # Emit theme mode when changed

    def __init__(self, parent=None):
        super().__init__("Actions", parent)
        self.setObjectName("toolbar")
        self.setFixedHeight(150)  # Increased height even more for full visibility
        
        # Set toolbar styling to ensure proper spacing
        self.setStyleSheet("""
            QToolBar {
                background: #232428;
                border: none;
                spacing: 0px;
                padding: 0px;
                margin: 0px;
            }
        """)

        # Track current theme mode
        self._current_theme = 'dark'
        
        # Create main widget container
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 40, 20, 40)  # Even more vertical margins for better centering
        main_layout.setSpacing(25)  # More spacing between buttons
        
        # Define neumorphic shadow styles for dark theme
        self.dark_outside = [
            {"outside": True, "offset": [4, 4], "blur": 8, "color": QColor(0, 0, 0, 178)},
            {"outside": True, "offset": [-4, -4], "blur": 8, "color": QColor(58, 58, 58, 255)}
        ]
        self.dark_inside = [
            {"inside": True, "offset": [4, 4], "blur": 8, "color": QColor(0, 0, 0, 178)},
            {"inside": True, "offset": [-4, -4], "blur": 8, "color": QColor(58, 58, 58, 255)}
        ]
        
        # Define neumorphic shadow styles for light theme
        self.light_outside = [
            {"outside": True, "offset": [4, 4], "blur": 8, "color": QColor(111, 140, 176, 105)},
            {"outside": True, "offset": [-4, -4], "blur": 8, "color": "#FFFFFF"}
        ]
        self.light_inside = [
            {"inside": True, "offset": [4, 4], "blur": 8, "color": "#C1D5EE"},
            {"inside": True, "offset": [-4, -4], "blur": 8, "color": "#FFFFFF"}
        ]

        # Button styles
        self.dark_button_style = """
            QPushButton {
                background: #232428;
                border: none;
                border-radius: 12px;
                color: rgb(4, 236, 180);
                padding: 10px 20px;
                font-weight: 500;
                font-size: 11px;
                min-width: 80px;
            }
            QPushButton:hover {
                color: rgb(0, 255, 200);
            }
            QPushButton:pressed {
                background: #1a1d21;
            }
        """
        
        self.light_button_style = """
            QPushButton {
                background: #E3EDF7;
                border: none;
                border-radius: 12px;
                color: #979797;
                padding: 10px 20px;
                font-weight: 500;
                font-size: 11px;
                min-width: 80px;
            }
            QPushButton:hover {
                color: #666666;
            }
            QPushButton:pressed {
                background: #d8e2ec;
            }
        """

        # Create neumorphic buttons
        self.btn_choose = self._create_neumorphic_button("Choose Folder", self._on_choose)
        self.btn_run = self._create_neumorphic_button("Run", self.run.emit)
        self.btn_copy = self._create_neumorphic_button("Copy", self.copy.emit)
        
        # Add buttons to layout
        main_layout.addWidget(self.btn_choose)
        main_layout.addWidget(self.btn_run)
        main_layout.addWidget(self.btn_copy)
        
        # Add separator
        separator = QWidget()
        separator.setFixedWidth(20)
        separator.setStyleSheet("background: transparent;")
        main_layout.addWidget(separator)
        
        # Live Watch Toggle
        self.btn_live = self._create_neumorphic_button("Live Watch: ON", self._toggle_live_watch)
        self.btn_live._button.setCheckable(True)
        self.btn_live._button.setChecked(True)
        main_layout.addWidget(self.btn_live)
        
        # Add flexible spacer to push theme button to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        spacer.setStyleSheet("background: transparent;")
        main_layout.addWidget(spacer)
        
        # Theme Toggle Button (right-aligned)
        self.btn_theme = self._create_neumorphic_button("Dark", self._toggle_theme)
        main_layout.addWidget(self.btn_theme)
        
        # Add the main widget to toolbar
        self.addWidget(main_widget)
        
        # Apply initial theme
        self._apply_theme()

    def _create_neumorphic_button(self, text, callback):
        """Create a button with neumorphic shadow effects"""
        button = QPushButton(text)
        button.clicked.connect(callback)
        
        # Use current theme shadows
        shadows = self.dark_outside if self._current_theme == 'dark' else self.light_outside
        
        # Create wrapper with shadows
        wrapper = BoxShadowWrapper(button, shadows, smooth=True, disable_margins=True, margins=(16, 16))  # Increased margins for better shadow visibility
        
        # Apply button style
        style = self.dark_button_style if self._current_theme == 'dark' else self.light_button_style
        button.setStyleSheet(style)
        
        # Store references for theme updates
        wrapper._button = button
        wrapper._shadows = shadows
        
        return wrapper

    def _apply_theme(self):
        """Apply current theme to all buttons"""
        # Update toolbar background
        if self._current_theme == 'dark':
            toolbar_bg = "#232428"
        else:
            toolbar_bg = "#E3EDF7"
            
        self.setStyleSheet(f"""
            QToolBar {{
                background: {toolbar_bg};
                border: none;
                spacing: 0px;
                padding: 0px;
                margin: 0px;
            }}
        """)
        
        # Get all button wrappers
        buttons = [self.btn_choose, self.btn_run, self.btn_copy, self.btn_live, self.btn_theme]
        
        for wrapper in buttons:
            if hasattr(wrapper, '_button'):
                button = wrapper._button
                
                # Update shadows
                if self._current_theme == 'dark':
                    wrapper.setShadowList(self.dark_outside)
                    button.setStyleSheet(self.dark_button_style)
                else:
                    wrapper.setShadowList(self.light_outside)
                    button.setStyleSheet(self.light_button_style)

    # ─────────────────────────────────────────────────────────────────
    def _on_choose(self):
        folder = QFileDialog.getExistingDirectory(self.parent(), "Select folder")
        if folder:
            self.choose_folder.emit(folder)
    
    def _toggle_live_watch(self):
        """Toggle live file watching on/off"""
        is_enabled = self.btn_live._button.isChecked()
        if is_enabled:
            self.btn_live._button.setText("Live Watch: ON")
            # Re-enable the watcher if it exists
            if hasattr(self.parent(), '_watcher') and self.parent()._watcher:
                print("Live watch enabled")
        else:
            self.btn_live._button.setText("Live Watch: OFF")
            # Disable the watcher
            if hasattr(self.parent(), '_watcher') and self.parent()._watcher:
                self.parent()._watcher.deleteLater()
                self.parent()._watcher = None
                print("Live watch disabled")

    def _toggle_theme(self):
        """Toggle between light and dark themes"""
        if self._current_theme == 'dark':
            self._current_theme = 'light'
            self.btn_theme._button.setText("Light")
        else:
            self._current_theme = 'dark'
            self.btn_theme._button.setText("Dark")
        
        # Apply the new theme
        self._apply_theme()
        
        # Emit the theme change signal
        self.theme_changed.emit(self._current_theme)
