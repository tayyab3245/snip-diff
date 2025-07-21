"""
Dark Theme - Unified Matte Plastic Design System
Recreating the exact theme system from game library
"""

from .tokens import DESIGN_TOKENS

tokens = DESIGN_TOKENS

# Dark theme color palette (matching game library with rich depth)
DARK_UNIFIED = {
    # === CORE THEME ===
    'mode': 'dark',
    'background': '#0f0f0f',
    'primary': '#e60012',
    'surface': '#1a1a1a',
    'text': '#f4f4f4',
    'shadow': 'rgba(0,0,0,0.7)',
    'glow': 'rgba(230, 0, 18, 0.4)',
    
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
    'surface_solid': '#1a1a1a',
    'surface_secondary': '#242424',
    'surface_elevated': '#2e2e2e',
    'surface_sunken': '#141414',     # Sunken/inset areas
    'surface_raised': '#323232',     # Raised/button areas
    
    # === ENHANCED BORDERS WITH RIM LIGHTING ===
    'border': '#0a0a0a',             # Deep border
    'border_light': '#404040',       # Rim light border
    'border_focus': '#e60012',       # Focus state
    'border_selection': '#e60012',   # Selection state
    
    # === TEXT HIERARCHY ===
    'text_primary': '#f4f4f4',
    'text_secondary': 'rgba(244, 244, 244, 0.8)',
    'text_disabled': 'rgba(244, 244, 244, 0.4)',
    'text_inverse': '#0f0f0f',
    'text_highlight': '#ffffff',     # Pure white for emphasis
    
    # === INTERACTION STATES WITH DEPTH ===
    'hover': 'rgba(255, 255, 255, 0.08)',
    'hover_bright': 'rgba(255, 255, 255, 0.12)',
    'active': 'rgba(0, 0, 0, 0.3)',
    'active_deep': 'rgba(0, 0, 0, 0.5)',
    'selected': '#e60012',
    'focus': '#e60012',
    
    # === COMPONENT SPECIFIC WITH DEPTH ===
    'toolbar_bg': 'rgba(20, 20, 20, 0.98)',
    'toolbar_bg_top': '#2a2a2a',
    'toolbar_bg_bot': '#161616',
    'toolbar_border_top': '#404040',
    'toolbar_border_bot': '#0a0a0a',
    
    'button_bg_top': '#383838',      # Button highlight
    'button_bg_bot': '#1e1e1e',      # Button shadow
    'button_border_light': '#505050', # Button rim light
    'button_border_dark': '#0a0a0a',  # Button edge shadow
    'button_hover_top': '#424242',
    'button_hover_bot': '#282828',
    'button_pressed_top': '#1a1a1a',
    'button_pressed_bot': '#0e0e0e',
    
    'tree_bg': '#161616',
    'tree_bg_inset': '#121212',      # Sunken appearance
    'tree_border_outer': '#0a0a0a',
    'tree_border_inner': '#2a2a2a',
    'tree_item_hover_light': 'rgba(255, 255, 255, 0.06)',
    'tree_item_hover_dark': 'rgba(0, 0, 0, 0.2)',
    
    'preview_bg': '#161616',
    'preview_bg_inset': '#121212',
    'preview_border_outer': '#0a0a0a',
    'preview_border_inner': '#2a2a2a',
}

def generate_dark_qss() -> str:
    """Generate complete QSS stylesheet for dark theme with rich matte plastic depth"""
    theme = DARK_UNIFIED
    
    return f'''
/* === GLOBAL STYLES === */
* {{
    font-family: {tokens['font']['family']};
    font-size: {tokens['font']['size']['md']};
    color: {theme['text_primary']};
    outline: none;
}}

QMainWindow, QWidget {{
    background: {theme['background']};
    color: {theme['text_primary']};
    margin: 0px;
    padding: 0px;
}}

QMainWindow {{
    background: {theme['background']};
    margin: 0px;
    padding: 0px;
}}

/* === MAIN LAYOUT COMPONENTS === */
QSplitter {{
    background: {theme['background']};
    border: none;
    margin: 0px;
    padding: 0px;
}}

QSplitter::handle {{
    background: {theme['background']};
    border: none;
    width: {tokens['spacing']['sm']};
    height: {tokens['spacing']['sm']};
}}

/* === CARVED/INSET SURFACES - No Container Effect === */
QFrame, QGroupBox {{
    /* Carved directly into background - no floating container */
    background: {theme['background']};
    border: none;
    border-radius: {tokens['radius']['md']};
}}

QFrame#surface {{
    /* Deep carved surface directly in background canvas */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_sunken']},
        stop:0.1 {theme['surface_solid']},
        stop:0.9 {theme['surface_solid']},
        stop:1 {theme['surface_sunken']});
    
    /* Inset borders - carved into background */
    border-top: 2px solid {theme['shadow_inset_dark']};
    border-left: 2px solid {theme['shadow_inset_dark']};
    border-right: 1px solid {theme['shadow_inset_light']};
    border-bottom: 1px solid {theme['shadow_inset_light']};
    border-radius: {tokens['radius']['md']};
}}

/* === LEFT SIDEBAR - Carved Directory Panel === */
QTreeView#leftPanel {{
    /* Carved left panel extending to edges with proper spacing */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_sunken']},
        stop:0.1 {theme['tree_bg_inset']},
        stop:0.9 {theme['tree_bg_inset']},
        stop:1 {theme['surface_sunken']});
    
    /* Enhanced carved borders with stronger contrast */
    border-top: 3px solid {theme['shadow_inset_dark']};
    border-left: 3px solid {theme['shadow_inset_dark']};
    border-right: 2px solid {theme['panel_rim']};
    border-bottom: 2px solid {theme['panel_rim']};
    border-radius: {tokens['radius']['md']};
    
    margin-top: {tokens['spacing']['lg']};  /* Spacing from toolbar */
    margin-left: {tokens['spacing']['lg']};  /* Spacing from left edge */
    margin-right: {tokens['spacing']['md']};  /* Spacing from right panel */
    margin-bottom: {tokens['spacing']['lg']};  /* Spacing from bottom edge */
    selection-background-color: {theme['selected']};
    selection-color: white;
}}

/* === RIGHT CONTENT AREA - Carved Context Panel === */
QWidget#rightPanel {{
    /* Identical carved panel as tree - exact same styling */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_sunken']},
        stop:0.1 {theme['tree_bg_inset']},
        stop:0.9 {theme['tree_bg_inset']},
        stop:1 {theme['surface_sunken']}) !important;
    
    /* Enhanced carved borders with stronger contrast */
    border-top: 3px solid {theme['shadow_inset_dark']} !important;
    border-left: 3px solid {theme['shadow_inset_dark']} !important;
    border-right: 2px solid {theme['panel_rim']} !important;
    border-bottom: 2px solid {theme['panel_rim']} !important;
    border-radius: {tokens['radius']['md']} !important;
    
    /* Enhanced spacing for the carved effect */
    margin-top: {tokens['spacing']['lg']} !important;  /* Spacing from toolbar */
    margin-left: {tokens['spacing']['md']} !important;  /* Spacing from left panel */
    margin-right: {tokens['spacing']['lg']} !important;  /* Spacing from right edge */
    margin-bottom: {tokens['spacing']['lg']} !important;  /* Spacing from bottom edge */
}}

/* === Alternative selector for Enhanced Preview Panel === */
EnhancedPreviewPanel {{
    /* Force carved background on the preview panel */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_sunken']},
        stop:0.1 {theme['tree_bg_inset']},
        stop:0.9 {theme['tree_bg_inset']},
        stop:1 {theme['surface_sunken']}) !important;
    
    border-top: 2px solid {theme['shadow_inset_dark']} !important;
    border-left: 2px solid {theme['shadow_inset_dark']} !important;
    border-right: 1px solid {theme['shadow_inset_light']} !important;
    border-bottom: 2px solid {theme['shadow_inset_light']} !important;
    border-radius: {tokens['radius']['md']} !important;
    margin-top: {tokens['spacing']['lg']} !important;
    margin-left: {tokens['spacing']['md']} !important;
    margin-right: {tokens['spacing']['lg']} !important;
    margin-bottom: {tokens['spacing']['lg']} !important;
}}

/* === STATIC TOOLBAR - Fixed at Top === */
QToolBar, #toolbar {{
    /* Static toolbar - flush to top edge */
    background: {theme['background']};
    border: none;
    padding: {tokens['spacing']['md']};
    spacing: {tokens['spacing']['md']};
    margin: 0px;
}}

#toolbar QToolButton {{
    padding: {tokens['spacing']['sm']} {tokens['spacing']['lg']};
    margin: 0 {tokens['spacing']['xs']};
    border-radius: 16px;  /* Reduced capsule shape */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_bg_top']},
        stop:0.1 {theme['surface_elevated']},
        stop:0.9 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    color: {theme['text_primary']};
    font-weight: {tokens['font']['weight']['medium']};
    border-top: 2px solid {theme['button_border_light']};
    border-left: 2px solid {theme['button_border_light']};
    border-right: 2px solid {theme['button_border_dark']};
    border-bottom: 3px solid {theme['button_border_dark']};
    min-height: {tokens['button']['sm']};
    min-width: 60px;
}}

#toolbar QToolButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_hover_top']},
        stop:0.1 {theme['surface_raised']},
        stop:0.9 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    border-top: 2px solid {theme['shadow_inset_light']};
    border-left: 2px solid {theme['shadow_inset_light']};
    border-right: 2px solid {theme['border_focus']};
    border-bottom: 3px solid {theme['border_focus']};
    color: {theme['text_highlight']};
}}

#toolbar QToolButton:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_pressed_top']},
        stop:0.2 {theme['surface_sunken']},
        stop:0.8 {theme['surface_sunken']},
        stop:1 {theme['button_pressed_bot']});
    border-top: 2px solid {theme['shadow_inset_dark']};
    border-left: 2px solid {theme['shadow_inset_dark']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 1px solid {theme['border_focus']};
    color: white;
}}

/* === RICH BUTTONS WITH CAPSULE SHAPE === */
QPushButton {{
    padding: {tokens['spacing']['md']} {tokens['spacing']['xl']};
    border-radius: 18px;  /* Capsule shape */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_bg_top']},
        stop:0.1 {theme['surface_elevated']},
        stop:0.9 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    color: {theme['text_primary']};
    font-weight: {tokens['font']['weight']['medium']};
    border-top: 2px solid {theme['button_border_light']};
    border-left: 2px solid {theme['button_border_light']};
    border-right: 2px solid {theme['button_border_dark']};
    border-bottom: 3px solid {theme['button_border_dark']};
    min-height: {tokens['button']['md']};
    min-width: 80px;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_hover_top']},
        stop:0.1 {theme['surface_raised']},
        stop:0.9 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    border-top: 2px solid {theme['shadow_inset_light']};
    border-left: 2px solid {theme['shadow_inset_light']};
    border-right: 2px solid {theme['border_focus']};
    border-bottom: 3px solid {theme['border_focus']};
    color: {theme['text_highlight']};
}}

QPushButton:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_pressed_top']},
        stop:0.2 {theme['surface_sunken']},
        stop:0.8 {theme['surface_sunken']},
        stop:1 {theme['button_pressed_bot']});
    border-top: 2px solid {theme['shadow_inset_dark']};
    border-left: 2px solid {theme['shadow_inset_dark']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 1px solid {theme['border_focus']};
    color: white;
}}

QPushButton:disabled {{
    background: {theme['surface_sunken']};
    color: {theme['text_disabled']};
    border: 1px solid {theme['border']};
}}

/* === GLOWING PRIMARY BUTTONS === */
QPushButton#primary {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff1a2b,
        stop:0.1 {theme['primary']},
        stop:0.9 #cc0010,
        stop:1 #990008);
    color: white;
    border-top: 2px solid #ff4d5a;
    border-left: 2px solid #ff4d5a;
    border-right: 2px solid #990008;
    border-bottom: 3px solid #660006;
    font-weight: {tokens['font']['weight']['bold']};
    border-radius: 18px;  /* Capsule shape */
}}

QPushButton#primary:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff4d5a,
        stop:0.1 #ff1a2b,
        stop:0.9 {theme['primary']},
        stop:1 #cc0010);
    border-top: 2px solid #ff8a94;
    border-left: 2px solid #ff8a94;
    border-right: 2px solid #660006;
    border-bottom: 3px solid #440004;
    color: white;
}}

QPushButton#primary:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #990008,
        stop:0.2 #cc0010,
        stop:0.8 #cc0010,
        stop:1 #660006);
    border-top: 2px solid #440004;
    border-left: 2px solid #440004;
    border-right: 1px solid #ff4d5a;
    border-bottom: 1px solid #ff4d5a;
    color: white;
}}

/* === TREE VIEW ITEMS - Styling for tree content === */
QTreeView::item {{
    padding: {tokens['spacing']['xs']} {tokens['spacing']['sm']};
    border: none;
    border-radius: {tokens['radius']['sm']};
}}

QTreeView::item:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['tree_item_hover_light']},
        stop:0.5 {theme['hover']},
        stop:1 {theme['tree_item_hover_dark']});
    border: 1px solid {theme['border_light']};
}}

QTreeView::item:selected {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff1a2b,
        stop:0.5 {theme['selected']},
        stop:1 #cc0010);
    color: white;
    border: 1px solid #ff4d5a;
    font-weight: {tokens['font']['weight']['bold']};
}}

QTreeView::indicator {{
    width: 15px;
    height: 15px;
    border-radius: {tokens['radius']['sm']};
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_elevated']},
        stop:0.5 {theme['surface_solid']},
        stop:1 {theme['surface_sunken']});
    border-top: 1px solid {theme['border_light']};
    border-left: 1px solid {theme['border_light']};
    border-right: 1px solid {theme['border']};
    border-bottom: 1px solid {theme['border']};
}}

QTreeView::indicator:checked {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff1a2b,
        stop:0.5 {theme['selected']},
        stop:1 #cc0010);
    border-top: 1px solid #ff4d5a;
    border-left: 1px solid #ff4d5a;
    border-right: 2px solid #990008;
    border-bottom: 2px solid #990008;
}}

QTreeView::indicator:unchecked:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_raised']},
        stop:0.5 {theme['surface_elevated']},
        stop:1 {theme['surface_solid']});
    border-top: 1px solid {theme['shadow_inset_light']};
    border-left: 1px solid {theme['shadow_inset_light']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 1px solid {theme['border_focus']};
}}

/* === SIMPLE TEXT AREAS - No Carved Effect === */
QPlainTextEdit, QTextEdit {{
    /* Simple text area - flat appearance */
    background: {theme['background']};
    color: {theme['text_primary']};
    border: none;
    border-radius: 0px;
    padding: {tokens['spacing']['md']};
    font-family: {tokens['font']['family']};
    font-size: {tokens['font']['size']['sm']};
}}

QPlainTextEdit:focus, QTextEdit:focus {{
    /* Simple focus state - just a subtle border */
    border: 1px solid {theme['border_focus']};
    background: {theme['background']};
}}

/* === SIMPLE LABELS AND HEADERS === */
QLabel {{
    /* Flat labels - no 3D styling */
    background: transparent;
    color: {theme['text_primary']};
    border: none;
    padding: {tokens['spacing']['xs']};
    font-family: {tokens['font']['family']};
}}

QLabel#fileTitle, QLabel#headerLabel {{
    /* File titles and headers - simple and clean */
    background: transparent;
    color: {theme['text_primary']};
    border: none;
    padding: {tokens['spacing']['sm']};
    font-weight: {tokens['font']['weight']['medium']};
    font-size: {tokens['font']['size']['md']};
}}

/* === CARVED SCROLLBARS - Inset Channels === */
QScrollBar:vertical {{
    /* Scrollbar track carved into background */
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {theme['surface_sunken']},
        stop:0.5 {theme['background']},
        stop:1 {theme['surface_sunken']});
    width: 14px;
    border-radius: 7px;
    
    /* Inset track appearance */
    border-top: 1px solid {theme['shadow_inset_dark']};
    border-left: 1px solid {theme['shadow_inset_dark']};
    border-right: 1px solid {theme['shadow_inset_light']};
    border-bottom: 1px solid {theme['shadow_inset_light']};
}}

QScrollBar::handle:vertical {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {theme['button_bg_top']},
        stop:0.1 {theme['surface_elevated']},
        stop:0.9 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    border-radius: 6px;
    border-top: 1px solid {theme['button_border_light']};
    border-left: 1px solid {theme['button_border_light']};
    border-right: 1px solid {theme['button_border_dark']};
    border-bottom: 1px solid {theme['button_border_dark']};
    min-height: 25px;
    margin: 1px;
}}

QScrollBar::handle:vertical:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {theme['button_hover_top']},
        stop:0.1 {theme['surface_raised']},
        stop:0.9 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    border-top: 1px solid {theme['shadow_inset_light']};
    border-left: 1px solid {theme['shadow_inset_light']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 1px solid {theme['border_focus']};
}}

QScrollBar::handle:vertical:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {theme['button_pressed_top']},
        stop:0.3 {theme['surface_sunken']},
        stop:0.7 {theme['surface_sunken']},
        stop:1 {theme['button_pressed_bot']});
    border-top: 1px solid {theme['shadow_inset_dark']};
    border-left: 1px solid {theme['shadow_inset_dark']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 1px solid {theme['border_focus']};
}}

QScrollBar:horizontal {{
    /* Horizontal scrollbar track carved into background */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_sunken']},
        stop:0.5 {theme['background']},
        stop:1 {theme['surface_sunken']});
    height: 14px;
    border-radius: 7px;
    
    /* Inset track appearance */
    border-top: 1px solid {theme['shadow_inset_dark']};
    border-left: 1px solid {theme['shadow_inset_dark']};
    border-right: 1px solid {theme['shadow_inset_light']};
    border-bottom: 1px solid {theme['shadow_inset_light']};
}}

QScrollBar::handle:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_bg_top']},
        stop:0.1 {theme['surface_elevated']},
        stop:0.9 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    border-radius: 6px;
    border-top: 1px solid {theme['button_border_light']};
    border-left: 1px solid {theme['button_border_light']};
    border-right: 1px solid {theme['button_border_dark']};
    border-bottom: 1px solid {theme['button_border_dark']};
    min-width: 25px;
    margin: 1px;
}}

QScrollBar::handle:horizontal:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_hover_top']},
        stop:0.1 {theme['surface_raised']},
        stop:0.9 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    border-top: 1px solid {theme['shadow_inset_light']};
    border-left: 1px solid {theme['shadow_inset_light']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 1px solid {theme['border_focus']};
}}

QScrollBar::handle:horizontal:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_pressed_top']},
        stop:0.3 {theme['surface_sunken']},
        stop:0.7 {theme['surface_sunken']},
        stop:1 {theme['button_pressed_bot']});
    border-top: 1px solid {theme['shadow_inset_dark']};
    border-left: 1px solid {theme['shadow_inset_dark']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 1px solid {theme['border_focus']};
}}

QScrollBar::add-line, QScrollBar::sub-line {{
    background: transparent;
    border: none;
    width: 0px;
    height: 0px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    background: transparent;
    border: none;
    width: 0px;
    height: 0px;
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    background: transparent;
    border: none;
    width: 0px;
    height: 0px;
}}

QScrollBar::up-arrow, QScrollBar::down-arrow, 
QScrollBar::left-arrow, QScrollBar::right-arrow {{
    background: transparent;
    border: none;
    width: 0px;
    height: 0px;
}}

/* === RAISED COMBO BOXES WITH CAPSULE SHAPE === */
QComboBox {{
    padding: {tokens['spacing']['md']} {tokens['spacing']['lg']};
    border-radius: 16px;  /* Capsule shape */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_bg_top']},
        stop:0.1 {theme['surface_elevated']},
        stop:0.9 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    color: {theme['text_primary']};
    border-top: 2px solid {theme['button_border_light']};
    border-left: 2px solid {theme['button_border_light']};
    border-right: 2px solid {theme['button_border_dark']};
    border-bottom: 3px solid {theme['button_border_dark']};
    min-height: {tokens['button']['sm']};
}}

QComboBox:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_hover_top']},
        stop:0.1 {theme['surface_raised']},
        stop:0.9 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    border-top: 2px solid {theme['shadow_inset_light']};
    border-left: 2px solid {theme['shadow_inset_light']};
    border-right: 2px solid {theme['border_focus']};
    border-bottom: 3px solid {theme['border_focus']};
    color: {theme['text_highlight']};
}}

QComboBox::drop-down {{
    border: none;
    background: transparent;
    width: 12px;  /* Reduced from 20px */
    padding: 2px;  /* Minimal padding */
}}

QComboBox::down-arrow {{
    image: none;
    border-style: solid;
    border-width: 3px 2px 0 2px;  /* Reduced from 5px 4px 0 4px */
    border-color: {theme['text_primary']} transparent transparent transparent;
    margin: 1px;  /* Minimal margin */
}}

QComboBox QAbstractItemView {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_elevated']},
        stop:0.5 {theme['surface_solid']},
        stop:1 {theme['surface_sunken']});
    border: 2px solid {theme['border']};
    border-radius: {tokens['radius']['md']};
    selection-background-color: {theme['selected']};
    outline: none;
}}

/* === FILE SECTIONS - Simple Borders Around Content === */
QFrame#diffSectionHeader {{
    /* Clean header - no border */
    background: transparent;
    border: none;
    padding: {tokens['spacing']['xs']};
    margin: {tokens['spacing']['xs']} 0;
}}

QPushButton#diffToggleButton {{
    /* Small compact toggle button */
    background: transparent;
    border: none;
    padding: 0px;
    margin: 0px;
    font-size: 10px;
    color: {theme['text_secondary']};
    min-width: 16px;
    min-height: 16px;
    max-width: 16px;
    max-height: 16px;
}}

QPushButton#diffToggleButton:hover {{
    color: {theme['text_primary']};
    background: {theme['hover']};
    border-radius: 2px;
}}

QLabel#diffSectionTitle {{
    /* Clean file title styling - reduced spacing */
    background: transparent;
    color: {theme['text_primary']};
    border: none;
    padding: 2px {tokens['spacing']['xs']};  /* Reduced padding */
    font-weight: {tokens['font']['weight']['medium']};
    font-size: {tokens['font']['size']['sm']};
}}

QPlainTextEdit#diffContentEditor {{
    /* Flat code area - no container, transparent on carved background */
    background: transparent;
    color: {theme['text_primary']};
    border: none;
    border-radius: 0px;
    padding: {tokens['spacing']['md']};
    font-family: "Consolas, Monaco, monospace";
    font-size: {tokens['font']['size']['sm']};
}}

/* Continue with remaining components... */
/* === TOOLTIPS === */
QToolTip {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_raised']},
        stop:0.5 {theme['surface_elevated']},
        stop:1 {theme['surface_solid']});
    color: {theme['text_highlight']};
    border-top: 1px solid {theme['border_light']};
    border-left: 1px solid {theme['border_light']};
    border-right: 2px solid {theme['border']};
    border-bottom: 2px solid {theme['border']};
    border-radius: {tokens['radius']['md']};
    padding: {tokens['spacing']['sm']};
    font-weight: {tokens['font']['weight']['medium']};
}}

/* === STATUS BAR === */
QStatusBar {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['toolbar_bg_top']},
        stop:0.5 {theme['toolbar_bg']},
        stop:1 {theme['toolbar_bg_bot']});
    color: {theme['text_primary']};
    border: none;
    border-top: 2px solid {theme['toolbar_border_top']};
}}

QProgressBar {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_sunken']},
        stop:0.5 {theme['surface_solid']},
        stop:1 {theme['surface_elevated']});
    border-top: 1px solid {theme['border']};
    border-left: 1px solid {theme['border']};
    border-right: 1px solid {theme['border_light']};
    border-bottom: 1px solid {theme['border_light']};
    border-radius: {tokens['radius']['sm']};
    text-align: center;
    color: {theme['text_highlight']};
    font-weight: {tokens['font']['weight']['bold']};
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff1a2b,
        stop:0.5 {theme['primary']},
        stop:1 #cc0010);
    border-radius: {tokens['radius']['sm']};
    margin: 1px;
}}
'''

# Export the QSS
DARK_THEME = generate_dark_qss()
