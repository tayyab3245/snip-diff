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
    QLabel, QPushButton, QFrame, QScrollArea, QSplitter
)

from pygments import lex
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.token import Token


def _fmt(col: str) -> QTextCharFormat:
    """Create text format with color"""
    f = QTextCharFormat()
    f.setForeground(QColor(col))
    f.setFont(QFont("Menlo, Consolas, monospace"))
    return f


class CollapsibleSection(QWidget):
    """A collapsible section widget for organizing diff content"""
    
    def __init__(self, title: str, content: str = "", collapsed: bool = False):
        super().__init__()
        self.title = title
        self.content = content
        self._collapsed = collapsed
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)  # No spacing since we're hiding the header
        
        # Header with toggle button - HIDDEN for full view
        header = QFrame()
        header.setFrameStyle(QFrame.Box)
        header.setObjectName("diffSectionHeader")
        header.hide()  # Hide the navigation header completely
        
        header_layout = QHBoxLayout(header)
        
        # Toggle button
        self.toggle_btn = QPushButton("▼" if not self._collapsed else "▶")
        self.toggle_btn.setFixedSize(16, 16)
        self.toggle_btn.setObjectName("diffToggleButton")
        self.toggle_btn.clicked.connect(self.toggle)
        
        # Title label
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("diffSectionTitle")
        
        header_layout.addWidget(self.toggle_btn)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        # Content area - full view, no containers
        self.content_widget = QPlainTextEdit()
        self.content_widget.setPlainText(self.content)
        self.content_widget.setReadOnly(True)
        self.content_widget.setFont(QFont("Consolas, Monaco, monospace", 11))
        
        # Remove minimum height constraints for full view
        self.content_widget.setMinimumHeight(0)
        
        self.content_widget.setObjectName("diffContentEditor")
        
        # Apply syntax highlighting
        self._apply_diff_highlighting()
        
        layout.addWidget(header)  # Header is hidden but still in layout
        layout.addWidget(self.content_widget)
        
        # Force content to always be visible (no collapsing)
        self._collapsed = False
        self.content_widget.show()
    
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
    
    def toggle(self):
        """Toggle functionality disabled - always show full content"""
        # Force content to always be visible
        self._collapsed = False
        self.content_widget.show()
        self.toggle_btn.setText("▼")
    
    def get_content(self) -> str:
        """Get the content for copying"""
        return self.content
    
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
        
        # Scroll area for sections (removed control buttons for simplicity)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # REMOVED transparent background - let parent's carved styling show through
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(8, 8, 8, 8)  # More generous margins
        self.scroll_layout.setSpacing(12)  # More spacing between sections
        # REMOVED transparent background - let parent's carved styling show through
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
            print(f"DEBUG: Showing PLACEHOLDER content with key: {effective_cache_key}")
        else:
            effective_cache_key = cache_key
            # ASSERTION: Ensure cache key is provided for real data
            if cache_key == "":
                print("WARNING: Empty cache key provided for real data - this may cause UI update issues")
            print(f"DEBUG: Showing REAL data with key: {effective_cache_key}")
        
        print(f"DEBUG: EnhancedPreviewPanel.show_sections called with {len(sections_data)} sections")
        print(f"DEBUG: Cache key: {self._current_cache_key} -> {effective_cache_key}")
        
        # Compute content hash for memoization (avoid unnecessary re-renders)
        import hashlib
        content_hash = hashlib.md5(str(sections_data).encode()).hexdigest()[:8]
        
        for i, (title, content, collapsed) in enumerate(sections_data):
            print(f"  Received section {i}: {title} (collapsed={collapsed}, content_length={len(content)})")
        
        # Check if we need to update (either cache key changed OR content changed)
        cache_key_changed = effective_cache_key != self._current_cache_key
        content_changed = content_hash != self._last_sections_hash
        
        if not cache_key_changed and not content_changed and not is_placeholder:
            print(f"DEBUG: SKIPPING re-render - no changes detected (cache_key: {effective_cache_key}, content_hash: {content_hash})")
            return
        
        # Force re-render if cache key changed or is placeholder
        if cache_key_changed or is_placeholder:
            if is_placeholder:
                print(f"DEBUG: FORCE RE-RENDER - Placeholder content")
            else:
                print(f"DEBUG: FORCE RE-RENDER - Cache key changed from {self._current_cache_key} to {effective_cache_key}")
            self._current_cache_key = effective_cache_key
            
        if content_changed:
            print(f"DEBUG: CONTENT CHANGED - Hash changed from {self._last_sections_hash} to {content_hash}")
            self._last_sections_hash = content_hash
        
        # Clear existing sections (always for now, could optimize later)
        self.clear_sections()
        
        # Add new sections
        for title, content, collapsed in sections_data:
            section = CollapsibleSection(title, content, collapsed)
            # Use effective cache key and mark placeholder status
            section.setProperty("cache_key", effective_cache_key)
            section.setProperty("content_hash", content_hash)
            section.setProperty("is_placeholder", is_placeholder)
            self.sections.append(section)
            self.scroll_layout.addWidget(section)
        
        print(f"DEBUG: Added {len(self.sections)} sections to preview panel")
        
        # Add stretch at the end
        self.scroll_layout.addStretch()
    
    def show_text(self, text: str):
        """Show plain text (fallback for compatibility) - treated as placeholder"""
        # Generate a cache key for text content to enable proper change detection
        import hashlib
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:8]
        cache_key = f"text_{text_hash}"
        # Mark as placeholder since this is fallback content - use informative title
        self.show_sections([("Ready", text, False)], cache_key, is_placeholder=True)
    
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
    
    def copy_all(self):
        """Copy all content to clipboard"""
        full_content = []
        for section in self.sections:
            full_content.append(f"# {section.title}")
            full_content.append(section.get_content())
            full_content.append("")  # Empty line between sections
        
        clipboard_text = "\n".join(full_content)
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(clipboard_text)
    
    def start_search(self):
        """Start search functionality (placeholder for now)"""
        search_text, ok = QInputDialog.getText(self, "Search", "Find:")
        if ok and search_text:
            # TODO: Implement search across all sections
            pass
