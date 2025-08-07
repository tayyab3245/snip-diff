"""
Enhanced preview panel with visual separation and collapsible sections
──────────────────────────────────────────────────────────────────────────
• Collapsible sections for different folders/file types
• Visual indicators for change types (added/modified/deleted)
• Maintains full copy functionality
• Progressive loading for better performance
"""

from __future__ import annotations
from typing import List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import (
    QGuiApplication, QTextCharFormat, QColor, QFont, QTextCursor,
    QSyntaxHighlighter, QAction
)
from PySide6.QtWidgets import (
    QPlainTextEdit, QWidget, QVBoxLayout, QInputDialog, QHBoxLayout,
    QLabel, QPushButton, QFrame, QScrollArea, QSplitter, QComboBox
)

from pygments import lex
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.token import Token

# Import neumorphic scroll bar
from .neumorphic_scrollbar import NeumorphicScrollArea


def _fmt(col: str) -> QTextCharFormat:
    """Create text format with color"""
    f = QTextCharFormat()
    f.setForeground(QColor(col))
    f.setFont(QFont("Menlo, Consolas, monospace"))
    return f


class CollapsibleSection(QWidget):
    """A collapsible section widget for organizing diff content"""
    
    # Signal for requesting copy operation
    copy_requested = Signal(str)
    
    def __init__(self, title: str, content: str = "", collapsed: bool = False):
        super().__init__()
        self.title = title
        self.content = content
        self._collapsed = collapsed
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)  # No spacing between header and content
        
        # Header with toggle button - NOW VISIBLE for interaction
        self.header = QFrame()
        self.header.setFrameStyle(QFrame.Box)
        self.header.setObjectName("diffSectionHeader")
        # REMOVED: header.hide() - header is now visible for interaction
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(6, 2, 6, 2)  # Very compact margins
        header_layout.setSpacing(6)  # Minimal spacing between items
        
        # Toggle button
        self.toggle_btn = QPushButton("▼" if not self._collapsed else "▶")
        self.toggle_btn.setFixedSize(16, 16)
        self.toggle_btn.setObjectName("diffToggleButton")
        self.toggle_btn.clicked.connect(self.toggle)
        
        # Title label
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("diffSectionTitle")
        
        # Copy button
        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setObjectName("copySectionButton")
        self.copy_btn.clicked.connect(self._handle_copy_click)
        
        header_layout.addWidget(self.toggle_btn)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.copy_btn)
        
        # Content area - with proper lazy loading
        self.content_widget = None  # Lazy loading - create only when needed
        
        layout.addWidget(self.header)
        
        # Apply initial collapsed state correctly
        self._update_visibility()
    
    def _apply_diff_highlighting(self):
        """Apply basic diff syntax highlighting"""
        doc = self.content_widget.document()
        cursor = QTextCursor(doc)
        
        # Define formats
        added_fmt = QTextCharFormat()
        added_fmt.setBackground(QColor("#1e3a1e"))
        added_fmt.setForeground(QColor("#4ec94e"))
        
        deleted_fmt = QTextCharFormat()
        deleted_fmt.setBackground(QColor("#3a1e1e"))
        deleted_fmt.setForeground(QColor("#f14c4c"))
        
        modified_fmt = QTextCharFormat()
        modified_fmt.setBackground(QColor("#3a3a1e"))
        modified_fmt.setForeground(QColor("#f1c40f"))
        
        # Apply highlighting line by line
        cursor.movePosition(QTextCursor.Start)
        while not cursor.atEnd():
            cursor.select(QTextCursor.LineUnderCursor)
            line = cursor.selectedText()
            
            if line.startswith("+"):
                cursor.setCharFormat(added_fmt)
            elif line.startswith("-"):
                cursor.setCharFormat(deleted_fmt)
            elif line.startswith("@"):
                cursor.setCharFormat(modified_fmt)
            
            cursor.movePosition(QTextCursor.NextBlock)
    
    def _create_content_widget(self):
        """Lazy creation of content widget for performance"""
        if self.content_widget is None:
            self.content_widget = QPlainTextEdit()
            self.content_widget.setPlainText(self.content)
            self.content_widget.setReadOnly(True)
            self.content_widget.setFont(QFont("Consolas, Monaco, monospace", 11))
            self.content_widget.setObjectName("diffContentEditor")
            
            # Remove individual scrollbars since we show full content
            self.content_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.content_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            
            # Document-style: Set a large fixed height to show ALL content
            # Calculate actual content height needed
            doc = self.content_widget.document()
            doc.setTextWidth(-1)  # No text wrapping - full width
            
            # Count lines and calculate proper height
            line_count = self.content.count('\n') + 1
            font_metrics = self.content_widget.fontMetrics()
            line_height = font_metrics.lineSpacing()
            
            # Full document height = lines * line height + padding
            full_document_height = line_count * line_height + 40
            
            # Always use the full calculated height, never compress
            self.content_widget.setFixedHeight(full_document_height)
            self.content_widget.setMinimumHeight(full_document_height)
            self.content_widget.setMaximumHeight(full_document_height)
            
            # Add to layout once
            self.layout().addWidget(self.content_widget)
            
            # Force layout update to recognize new size
            self.updateGeometry()
            if self.parent():
                self.parent().updateGeometry()
            
            # Apply syntax highlighting
            self._apply_diff_highlighting()
    
    def _update_visibility(self):
        """Update widget visibility based on collapsed state"""
        if self._collapsed:
            # Hide content widget
            if self.content_widget:
                self.content_widget.hide()
            self.toggle_btn.setText("▶")
        else:
            # Create content widget if needed and show it
            self._create_content_widget()
            self.content_widget.show()
            self.toggle_btn.setText("▼")
    
    def toggle(self):
        """Toggle section visibility - NOW PROPERLY FUNCTIONAL"""
        self._collapsed = not self._collapsed
        self._update_visibility()
    
    def get_content(self) -> str:
        """Get the content for copying"""
        return self.content
    
    def _handle_copy_click(self):
        """Handle copy button click by emitting signal"""
        self.copy_requested.emit(self.get_content())
    
    def set_content(self, content: str):
        """Update the content"""
        self.content = content
        self.content_widget.setPlainText(content)
        self._apply_diff_highlighting()


class EnhancedPreviewPanel(QWidget):
    """Enhanced preview panel with collapsible sections"""
    
    def __init__(self):
        super().__init__()
        self.sections: List[CollapsibleSection] = []
        self._current_cache_key: str = ""  # Track cache key for forced re-renders
        self._last_sections_hash: str = ""  # Track content hash to avoid unnecessary re-renders
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        
        # Instructions panel
        instructions_panel = QWidget()
        instructions_layout = QVBoxLayout(instructions_panel)
        instructions_layout.setContentsMargins(4, 4, 4, 4)
        instructions_layout.setSpacing(4)
        
        # Instructions label
        instructions_label = QLabel("Custom AI Instructions")
        instructions_label.setObjectName("instructionsLabel")
        instructions_layout.addWidget(instructions_label)
        
        # Instructions input
        self.instructions_input = QPlainTextEdit()
        self.instructions_input.setObjectName("instructionsInput")
        self.instructions_input.setPlaceholderText("Your custom instructions for the AI go here...")
        self.instructions_input.setMaximumHeight(80)  # Keep it compact
        instructions_layout.addWidget(self.instructions_input)
        
        # Position control
        position_layout = QHBoxLayout()
        position_label = QLabel("Position:")
        position_layout.addWidget(position_label)
        
        self.position_control = QComboBox()
        self.position_control.setObjectName("positionControl")
        self.position_control.addItem("Prepend (Instructions at Top)")
        self.position_control.addItem("Append (Instructions at Bottom)")
        position_layout.addWidget(self.position_control)
        position_layout.addStretch()
        
        instructions_layout.addLayout(position_layout)
        layout.addWidget(instructions_panel)
        
        # Control bar for expand/collapse all functionality
        control_bar = QWidget()
        control_layout = QHBoxLayout(control_bar)
        control_layout.setContentsMargins(4, 4, 4, 4)
        
        # Expand/Collapse All buttons
        self.expand_all_btn = QPushButton("Expand All")
        self.expand_all_btn.clicked.connect(self._expand_all)
        self.expand_all_btn.setObjectName("controlButton")
        
        self.collapse_all_btn = QPushButton("Collapse All")
        self.collapse_all_btn.clicked.connect(self._collapse_all)
        self.collapse_all_btn.setObjectName("controlButton")
        
        control_layout.addWidget(self.expand_all_btn)
        control_layout.addWidget(self.collapse_all_btn)
        control_layout.addStretch()
        
        layout.addWidget(control_bar)
        
        # Scroll area for sections
        self.scroll_area = NeumorphicScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(4, 4, 4, 4)  # Reduced top margin
        self.scroll_layout.setSpacing(2)  # Reduced spacing between sections
        self.scroll_widget.setStyleSheet("QWidget { border: none; }")
        
        self.scroll_area.setWidget(self.scroll_widget)
        
        layout.addWidget(self.scroll_area)
    
    def show_sections(self, sections_data: List[tuple], cache_key: str = "", is_placeholder: bool = False):
        """
        Show diff sections with cache key for forced re-rendering
        sections_data: List of (title, content, collapsed) tuples
        cache_key: Cache key to force re-render when changed
        is_placeholder: True if this is placeholder content, False for real data
        """
        
        # Handle placeholder vs real data with different component keys
        if is_placeholder:
            effective_cache_key = f"placeholder_{cache_key}"
        else:
            effective_cache_key = cache_key
            if cache_key == "":
                # Use timestamp as fallback for empty cache keys
                import time
                effective_cache_key = f"fallback_{int(time.time())}"
        
        # Compute content hash for memoization (avoid unnecessary re-renders)
        import hashlib
        content_hash = hashlib.md5(str(sections_data).encode()).hexdigest()[:8]
        
        # Check if we need to update (either cache key changed OR content changed)
        cache_key_changed = effective_cache_key != self._current_cache_key
        content_changed = content_hash != self._last_sections_hash
        
        if not cache_key_changed and not content_changed and not is_placeholder:
            return
        
        # Update tracking variables
        if cache_key_changed or is_placeholder:
            self._current_cache_key = effective_cache_key
            
        if content_changed:
            self._last_sections_hash = content_hash
        
        # Clear existing sections
        self.clear_sections()
        
        # Add new sections with separators
        for i, (title, content, collapsed) in enumerate(sections_data):
            # Add separator before each section (except the first one)
            if i > 0:
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setFrameShadow(QFrame.Sunken)
                separator.setObjectName("documentSeparator")
                separator.setFixedHeight(2)  # Make it slightly thicker and more visible
                # Remove inline styling to let theme CSS take effect
                self.scroll_layout.addWidget(separator)
            
            section = CollapsibleSection(title, content, collapsed)
            section.setProperty("cache_key", effective_cache_key)
            section.setProperty("content_hash", content_hash)
            section.setProperty("is_placeholder", is_placeholder)
            
            # Connect per-file copy signal to central copy handler
            section.copy_requested.connect(self._execute_copy)
            
            self.sections.append(section)
            self.scroll_layout.addWidget(section)
    
    def show_text(self, text: str):
        """Show plain text as a compact message at the top (not collapsible)"""
        # Clear any existing sections first
        self.clear_sections()
        
        # Create a simple, compact message widget instead of collapsible section
        message_widget = QWidget()
        message_layout = QVBoxLayout(message_widget)
        message_layout.setContentsMargins(12, 12, 12, 12)  # Compact margins
        message_layout.setSpacing(8)  # Tight spacing
        
        # Create a simple label for the message
        message_label = QLabel(text)
        message_label.setObjectName("welcomeMessage")
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        message_layout.addWidget(message_label)
        message_layout.addStretch()  # Push content to top
        
        # Add to scroll layout at the top
        self.scroll_layout.addWidget(message_widget)
    
    def clear_sections(self):
        """Clear all sections"""
        for section in self.sections:
            section.deleteLater()
        self.sections.clear()
        
        # Clear layout
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def _expand_all(self):
        """Expand all sections"""
        for section in self.sections:
            if section._collapsed:
                section.toggle()
    
    def _collapse_all(self):
        """Collapse all sections"""
        for section in self.sections:
            if not section._collapsed:
                section.toggle()
    
    def _execute_copy(self, code_content: str):
        """Central method to handle all copy operations with custom instructions"""
        # Read instructions and position
        instructions = self.instructions_input.toPlainText().strip()
        position = self.position_control.currentText()
        
        # Prepare final content
        if instructions:
            separator = "\n" + "-" * 50 + "\n"
            if "Prepend" in position:
                # Instructions at top
                final_content = instructions + separator + code_content
            else:
                # Instructions at bottom
                final_content = code_content + separator + instructions
        else:
            # No instructions, just the code
            final_content = code_content
        
        # Copy to clipboard
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(final_content)
    
    def copy_all(self):
        """Copy all content to clipboard"""
        full_content = []
        for section in self.sections:
            full_content.append(f"# {section.title}")
            full_content.append(section.get_content())
            full_content.append("")  # Empty line between sections
        
        clipboard_text = "\n".join(full_content)
        self._execute_copy(clipboard_text)
    
    def start_search(self):
        """Start search functionality (placeholder for now)"""
        search_text, ok = QInputDialog.getText(self, "Search", "Find:")
        if ok and search_text:
            # TODO: Implement search across all sections
            pass
    
    def set_theme(self, theme_colors):
        """Update the theme for neumorphic scroll bars"""
        if hasattr(self, 'scroll_area') and hasattr(self.scroll_area, 'set_theme'):
            self.scroll_area.set_theme(theme_colors)
