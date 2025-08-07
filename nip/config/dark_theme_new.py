"""
Dark Theme - Neumorphic Design System
Migrated from main_window.py hardcoded styles
"""

from .tokens import DESIGN_TOKENS

tokens = DESIGN_TOKENS

# Dark theme color palette (matching neumorphic design from main_window.py)
DARK_UNIFIED = {
    # === CORE THEME - NEUMORPHIC COLORS ===
    'mode': 'dark',
    'background': '#232428',       # Neumorphic dark background
    'primary': '#e60012',
    'surface': '#232428',          # Same as background for neumorphic consistency
    'text': 'rgb(4, 236, 180)',    # Teal text color from neumorphic theme
    'shadow': 'rgba(0,0,0,0.7)',
    'glow': 'rgba(230, 0, 18, 0.4)',
    
    # === NEUMORPHIC SYSTEM - Exact colors from main_window.py ===
    'main_bg': '#232428',              # Dark neumorphic background
    'inner_bg': '#232428',             # Same for consistency
    'inner_shadow': 'rgba(0, 0, 0, 0.8)',      # Dark inner shadow
    'inner_highlight': 'rgba(58, 58, 58, 1.0)', # Subtle highlight
    'text_color': 'rgb(4, 236, 180)',  # Teal text
    
    # === MATTE PLASTIC SYSTEM - Deep Multi-Layer Shadows ===
    'panel_top': '#2e2e2e',        # Highlight surface
    'panel_bot': '#1a1a1a',        # Shadow surface 
    'panel_edge': '#0a0a0a',       # Deep edge shadow
    'panel_rim': '#404040',        # Rim light highlight
    
    # Multiple shadow layers for true depth
    'shadow_inset_light': 'rgba(255, 255, 255, 0.15)',  # Inner highlight
    'shadow_inset_dark': 'rgba(0, 0, 0, 0.8)',          # Inner shadow
    'shadow_outer_near': 'rgba(0, 0, 0, 0.4)',          # Close shadow
    'shadow_outer_far': 'rgba(0, 0, 0, 0.6)',           # Far shadow
    
    # === RICH SURFACE VARIATIONS ===
    'surface_solid': '#232428',      # Use neumorphic background
    'surface_secondary': '#242424',
    'surface_elevated': '#2e2e2e',
    'surface_sunken': '#232428',     # Use neumorphic background for sunken areas
    'surface_raised': '#323232',     # Raised/button areas
    
    # === ENHANCED BORDERS WITH RIM LIGHTING ===
    'border': '#0a0a0a',             # Deep border
    'border_light': '#404040',       # Rim light border
    'border_focus': '#e60012',       # Focus state
    'border_selection': '#e60012',   # Selection state
    
    # === TEXT HIERARCHY - NEUMORPHIC ===
    'text_primary': 'rgb(4, 236, 180)',  # Neumorphic teal text
    'text_secondary': 'rgba(4, 236, 180, 0.8)',
    'text_disabled': 'rgba(4, 236, 180, 0.4)',
    'text_inverse': '#232428',
    'text_highlight': 'rgb(4, 236, 180)',
    'selected': '#e60012',           # Selection color
    
    # === COMPONENT SPECIFIC WITH NEUMORPHIC DEPTH ===
    'toolbar_bg': '#232428',         # Use neumorphic background
    'toolbar_bg_top': '#2a2a2a',
    'toolbar_bg_bot': '#232428',     # Use neumorphic background
    'toolbar_border_top': '#404040',
    'toolbar_border_bot': '#0a0a0a',
    
    'button_bg_top': '#383838',      # Button highlight
    'button_bg_bot': '#232428',      # Use neumorphic background
    'button_border_light': '#505050', # Button rim light
    'button_border_dark': '#0a0a0a',  # Button edge shadow
    'button_hover_top': '#424242',
    'button_hover_bot': '#282828',
    'button_pressed_top': '#1a1a1a',
    'button_pressed_bot': '#0e0e0e',
    
    'tree_bg': '#232428',            # Use neumorphic background
    'tree_bg_inset': '#232428',      # Use neumorphic background for consistency
    'tree_border_outer': 'rgba(0, 0, 0, 0.8)',    # Use neumorphic inner shadow
    'tree_border_inner': 'rgba(58, 58, 58, 1.0)',  # Use neumorphic inner highlight
    'tree_item_hover_light': 'rgba(255, 255, 255, 0.06)',
    'tree_item_hover_dark': 'rgba(0, 0, 0, 0.2)',
    
    'preview_bg': '#232428',         # Use neumorphic background
    'preview_bg_inset': '#232428',   # Use neumorphic background
    'preview_border_outer': 'rgba(0, 0, 0, 0.8)',    # Use neumorphic inner shadow
    'preview_border_inner': 'rgba(58, 58, 58, 1.0)',  # Use neumorphic inner highlight
}

def generate_dark_qss() -> str:
    """Generate complete QSS stylesheet for dark neumorphic theme"""
    theme = DARK_UNIFIED
    
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
        stop: 0 {theme['tree_border_outer']}, stop: 1 {theme['main_bg']});
    border-top: 1px solid {theme['tree_border_outer']};
    border-left: 1px solid {theme['tree_border_outer']};
    border-bottom: 1px solid {theme['tree_border_inner']};
    border-right: 1px solid {theme['tree_border_inner']};
    color: {theme['text_color']};
}}

/* === ACCORDION SECTIONS === */
QFrame#diffSectionHeader {{
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 {theme['surface_elevated']}, stop: 1 {theme['main_bg']});
    border-bottom: 1px solid {theme['border']};
    border-radius: {tokens['radius']['sm']};
    padding: {tokens['spacing']['xs']};
    margin-bottom: 2px;
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
    background: {theme['tree_item_hover_light']};
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
