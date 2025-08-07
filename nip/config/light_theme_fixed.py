"""
Light Theme - Neumorphic Design System
Migrated from main_window.py hardcoded styles
"""

from .tokens import DESIGN_TOKENS

tokens = DESIGN_TOKENS

# Light theme color palette (neumorphic light design from main_window.py)
LIGHT_UNIFIED = {
    # === CORE THEME - NEUMORPHIC LIGHT COLORS ===
    'mode': 'light',
    'background': '#E3EDF7',       # Neumorphic light background
    'primary': '#e60012',
    'surface': '#E3EDF7',          # Same as background for neumorphic consistency
    'text': '#979797',             # Gray text from neumorphic theme
    'shadow': 'rgba(0,0,0,0.08)',
    'glow': 'rgba(230, 0, 18, 0.2)',
    
    # === NEUMORPHIC SYSTEM - Exact colors from main_window.py ===
    'main_bg': '#E3EDF7',              # Light neumorphic background
    'inner_bg': '#E3EDF7',             # Same for consistency
    'inner_shadow': 'rgba(111, 140, 176, 0.4)',      # Light inner shadow
    'inner_highlight': 'rgba(255, 255, 255, 0.8)',   # Bright highlight
    'text_color': '#979797',           # Gray text
    
    # === MODERN MINIMALIST DEPTH SYSTEM - Enhanced Contrast ===
    'panel_top': '#ffffff',        # Pure white for raised surfaces
    'panel_bot': '#e8eaed',        # Darker base surface for contrast
    'panel_edge': '#b0b3b8',       # Stronger shadow/border color for definition
    'panel_rim': '#ffffff',        # Pure white rim light
    
    # Shadow layers - Enhanced contrast for better depth perception
    'shadow_inset_light': 'rgba(255, 255, 255, 0.9)',   # Brighter inner highlight
    'shadow_inset_dark': 'rgba(0, 0, 0, 0.25)',         # Darker inner shadow for definition
    'shadow_outer_near': 'rgba(0, 0, 0, 0.15)',         # More visible close shadow
    'shadow_outer_far': 'rgba(0, 0, 0, 0.12)',          # Noticeable far shadow
    
    # === CLEAN SURFACE VARIATIONS - More Contrast ===
    'surface_solid': '#E3EDF7',      # Use neumorphic background
    'surface_secondary': '#dee1e6',  # Mid-tone secondary surfaces
    'surface_elevated': '#ffffff',   # Pure white for elevated surfaces
    'surface_sunken': '#E3EDF7',     # Use neumorphic background for sunken areas
    'surface_raised': '#ffffff',     # Pure white for raised areas
    
    # === MODERN BORDERS - Enhanced Definition ===
    'border': '#b0b3b8',             # Stronger border color for definition
    'border_light': '#d8dce1',       # Mid-tone light border
    'border_focus': '#e60012',       # Focus state
    'border_selection': '#e60012',   # Selection state
    
    # === READABLE TEXT HIERARCHY - NEUMORPHIC ===
    'text_primary': '#979797',       # Neumorphic gray text
    'text_secondary': 'rgba(151, 151, 151, 0.7)',
    'text_disabled': 'rgba(151, 151, 151, 0.4)',
    'text_inverse': '#ffffff',
    'text_highlight': '#979797',     # Same as primary neumorphic text
    
    # === INTERACTION STATES WITH ENHANCED DEPTH ===
    'hover': 'rgba(0, 0, 0, 0.06)',
    'hover_bright': 'rgba(0, 0, 0, 0.10)',
    'active': 'rgba(0, 0, 0, 0.15)',
    'active_deep': 'rgba(0, 0, 0, 0.20)',
    'selected': '#e60012',
    'focus': '#e60012',
    
    # === COMPONENT SPECIFIC - NEUMORPHIC ===
    'toolbar_bg': '#E3EDF7',         # Use neumorphic background
    'toolbar_bg_top': '#ffffff',         # Pure white for toolbar top
    'toolbar_bg_bot': '#E3EDF7',         # Use neumorphic background
    'toolbar_border_top': 'rgba(255, 255, 255, 0.9)',     # Bright highlight
    'toolbar_border_bot': '#b0b3b8',     # Strong shadow for definition
    
    # Enhanced button system with neumorphic colors
    'button_bg_top': '#ffffff',          # Pure white for button highlights
    'button_bg_bot': '#E3EDF7',          # Use neumorphic background
    'button_border_light': 'rgba(255, 255, 255, 0.9)',    # Bright highlight border
    'button_border_dark': '#b0b3b8',     # Strong border color for definition
    'button_hover_top': '#ffffff',       # Hover maintains white
    'button_hover_bot': '#dee1e6',       # More noticeable hover change
    'button_pressed_top': '#dee1e6',     # Pressed = noticeably darker
    'button_pressed_bot': '#d3d7dc',     # Clear press depth
    
    # Enhanced hover states with better contrast
    'tree_item_hover_light': 'rgba(230, 0, 18, 0.04)',
    'tree_item_hover_dark': 'rgba(0, 0, 0, 0.10)', # More visible shadow on hover
    
    # === NEUMORPHIC COLORS FOR CARVED PANELS ===
    'tree_bg': '#E3EDF7',            # Use neumorphic background
    'tree_bg_inset': '#E3EDF7',      # Use neumorphic background for consistency
    'tree_border_outer': 'rgba(111, 140, 176, 0.4)',    # Use neumorphic inner shadow
    'tree_border_inner': 'rgba(255, 255, 255, 0.8)',    # Use neumorphic inner highlight
    
    'preview_bg': '#E3EDF7',         # Use neumorphic background
    'preview_bg_inset': '#E3EDF7',   # Use neumorphic background
    'preview_border_outer': 'rgba(111, 140, 176, 0.4)',    # Use neumorphic inner shadow
    'preview_border_inner': 'rgba(255, 255, 255, 0.8)',    # Use neumorphic inner highlight
}

def generate_light_qss() -> str:
    """Generate complete QSS stylesheet for light neumorphic theme"""
    theme = LIGHT_UNIFIED
    
    return f'''
/* === NEUMORPHIC GLOBAL STYLES === */
QMainWindow {{
    background-color: {theme['main_bg']};
    color: {theme['text_color']};
}}

QWidget {{
    background-color: {theme['main_bg']};
    color: {theme['text_color']};
}}

QSplitter {{
    background-color: {theme['main_bg']};
    border: none;
}}

QSplitter::handle {{
    background-color: {theme['main_bg']};
}}

/* === NEUMORPHIC TREE VIEW === */
QTreeView {{
    background-color: {theme['inner_bg']};
    color: {theme['text_color']};
    border: none;
    margin: 8px;
    border-top: 2px solid {theme['inner_shadow']};
    border-left: 2px solid {theme['inner_shadow']};
    border-right: 2px solid {theme['inner_highlight']};
    border-bottom: 2px solid {theme['inner_highlight']};
    border-radius: 4px;
}}

/* === NEUMORPHIC SCROLL AREA === */
QScrollArea {{
    background-color: {theme['inner_bg']};
    color: {theme['text_color']};
    border: none;
    margin: 8px;
    border-top: 2px solid {theme['inner_shadow']};
    border-left: 2px solid {theme['inner_shadow']};
    border-right: 2px solid {theme['inner_highlight']};
    border-bottom: 2px solid {theme['inner_highlight']};
    border-radius: 4px;
}}

/* === NEUMORPHIC TEXT EDIT === */
QTextEdit {{
    background-color: {theme['inner_bg']};
    color: {theme['text_color']};
    border: none;
    margin: 8px;
    border-top: 2px solid {theme['inner_shadow']};
    border-left: 2px solid {theme['inner_shadow']};
    border-right: 2px solid {theme['inner_highlight']};
    border-bottom: 2px solid {theme['inner_highlight']};
    border-radius: 4px;
}}

/* === NEUMORPHIC RIGHT PANEL === */
QWidget[objectName="rightPanel"], QWidget#rightPanel {{
    background-color: {theme['inner_bg']} !important;
    color: {theme['text_color']} !important;
    border: none;
    margin: 8px;
    border-top: 2px solid {theme['inner_shadow']};
    border-left: 2px solid {theme['inner_shadow']};
    border-right: 2px solid {theme['inner_highlight']};
    border-bottom: 2px solid {theme['inner_highlight']};
    border-radius: 4px;
}}

/* === TOOLBAR STYLING === */
QToolBar {{
    background-color: {theme['main_bg']};
    color: {theme['text_color']};
    border: none;
    padding: {tokens['spacing']['md']};
}}

/* === BUTTON STYLING === */
QPushButton {{
    background-color: {theme['inner_bg']};
    color: {theme['text_color']};
    border: none;
    margin: 2px;
    padding: 8px 16px;
    border-top: 2px solid {theme['inner_shadow']};
    border-left: 2px solid {theme['inner_shadow']};
    border-right: 2px solid {theme['inner_highlight']};
    border-bottom: 2px solid {theme['inner_highlight']};
    border-radius: 4px;
}}

QPushButton:hover {{
    background-color: {theme['surface_elevated']};
}}

QPushButton:pressed {{
    border-top: 2px solid {theme['inner_highlight']};
    border-left: 2px solid {theme['inner_highlight']};
    border-right: 2px solid {theme['inner_shadow']};
    border-bottom: 2px solid {theme['inner_shadow']};
}}

/* === ENHANCED PREVIEW PANEL === */
EnhancedPreviewPanel {{
    background-color: {theme['inner_bg']};
    color: {theme['text_color']};
    border: none;
    margin: 8px;
    border-top: 2px solid {theme['inner_shadow']};
    border-left: 2px solid {theme['inner_shadow']};
    border-right: 2px solid {theme['inner_highlight']};
    border-bottom: 2px solid {theme['inner_highlight']};
    border-radius: 4px;
}}

/* === SCROLL BAR STYLING === */
QScrollBar:vertical {{
    background: {theme['inner_bg']};
    width: 12px;
    border: none;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background: {theme['surface_elevated']};
    border-radius: 6px;
    border-top: 1px solid {theme['inner_shadow']};
    border-left: 1px solid {theme['inner_shadow']};
    border-right: 1px solid {theme['inner_highlight']};
    border-bottom: 1px solid {theme['inner_highlight']};
}}

QScrollBar::handle:vertical:hover {{
    background: {theme['surface_raised']};
}}

QScrollBar:horizontal {{
    background: {theme['inner_bg']};
    height: 12px;
    border: none;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background: {theme['surface_elevated']};
    border-radius: 6px;
    border-top: 1px solid {theme['inner_shadow']};
    border-left: 1px solid {theme['inner_shadow']};
    border-right: 1px solid {theme['inner_highlight']};
    border-bottom: 1px solid {theme['inner_highlight']};
}}

QScrollBar::handle:horizontal:hover {{
    background: {theme['surface_raised']};
}}

/* === MISC CONTROLS === */
QLabel {{
    background: transparent;
    color: {theme['text_color']};
}}

QFrame {{
    background-color: {theme['main_bg']};
    color: {theme['text_color']};
}}

/* === TREE VIEW ITEMS === */
QTreeView::item {{
    border: none;
    padding: 4px 8px;
    background: transparent;
    border-radius: 2px;
    margin: 1px;
}}

QTreeView::item:hover {{
    background: {theme['tree_item_hover_light']};
}}

QTreeView::item:selected {{
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 {theme['inner_shadow']}, stop: 1 {theme['main_bg']});
    border-top: 1px solid {theme['inner_shadow']};
    border-left: 1px solid {theme['inner_shadow']};
    border-bottom: 1px solid {theme['inner_highlight']};
    border-right: 1px solid {theme['inner_highlight']};
    color: {theme['text_color']};
}}

/* === ACCORDION SECTIONS === */
QFrame#diffSectionHeader {{
    background-color: {theme['inner_bg']};
    height: 32px;
    padding: {tokens['spacing']['xs']};
    margin: 0px;
    border-top: 1px solid {theme['button_border_light']};
    border-left: 1px solid {theme['button_border_light']};
    border-right: 1px solid {theme['button_border_dark']};
    border-bottom: 1px solid {theme['button_border_dark']};
    border-radius: {tokens['radius']['sm']};
}}

QLabel#diffSectionTitle {{
    font-weight: {tokens['font']['weight']['medium']};
    color: {theme['text_color']};
}}

QPushButton#diffToggleButton {{
    background: transparent;
    border: none;
    color: {theme['text_color']};
    padding: 2px;
}}

QPushButton#diffToggleButton:hover {{
    background: {theme['hover']};
    border-radius: 2px;
}}

/* === MENUS === */
QMenu {{
    background: {theme['surface_elevated']};
    color: {theme['text_color']};
    border: 2px solid {theme['border']};
    border-radius: 4px;
    padding: 2px;
}}

QMenu::item {{
    background: transparent;
    padding: 4px 16px;
    border-radius: 2px;
}}

QMenu::item:selected {{
    background: {theme['selected']};
    color: white;
}}
'''
