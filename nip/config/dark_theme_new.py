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
}}

QMainWindow {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        stop:0 {theme['background']}, 
        stop:0.5 #0a0a0a, 
        stop:1 {theme['background']});
}}

/* === DEEP MATTE PLASTIC SURFACES === */
QFrame, QGroupBox {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['panel_top']},
        stop:0.1 {theme['surface_elevated']},
        stop:0.9 {theme['surface_solid']},
        stop:1 {theme['panel_bot']});
    border-top: 2px solid {theme['border_light']};
    border-left: 1px solid {theme['border_light']};
    border-right: 1px solid {theme['border']};
    border-bottom: 2px solid {theme['border']};
    border-radius: {tokens['radius']['md']};
}}

QFrame#surface {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['panel_rim']},
        stop:0.05 {theme['panel_top']},
        stop:0.95 {theme['panel_bot']},
        stop:1 {theme['panel_edge']});
    border-top: 2px solid {theme['shadow_inset_light']};
    border-left: 1px solid {theme['shadow_inset_light']};
    border-right: 2px solid {theme['shadow_inset_dark']};
    border-bottom: 3px solid {theme['shadow_inset_dark']};
    border-radius: {tokens['radius']['md']};
}}

/* === RICH TOOLBAR WITH DEPTH === */
#toolbar {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['toolbar_bg_top']},
        stop:0.1 {theme['toolbar_bg']},
        stop:0.9 {theme['toolbar_bg']},
        stop:1 {theme['toolbar_bg_bot']});
    border: none;
    border-top: 1px solid {theme['toolbar_border_top']};
    border-bottom: 2px solid {theme['toolbar_border_bot']};
    padding: {tokens['spacing']['sm']};
    border-radius: {tokens['radius']['md']};
}}

#toolbar QToolButton {{
    padding: {tokens['spacing']['sm']} {tokens['spacing']['lg']};
    margin: 0 {tokens['spacing']['xs']};
    border-radius: {tokens['radius']['sm']};
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_bg_top']},
        stop:0.1 {theme['surface_elevated']},
        stop:0.9 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    color: {theme['text_primary']};
    font-weight: {tokens['font']['weight']['medium']};
    border-top: 1px solid {theme['button_border_light']};
    border-left: 1px solid {theme['button_border_light']};
    border-right: 1px solid {theme['button_border_dark']};
    border-bottom: 2px solid {theme['button_border_dark']};
    min-height: {tokens['button']['md']};
}}

#toolbar QToolButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_hover_top']},
        stop:0.1 {theme['surface_raised']},
        stop:0.9 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    border-top: 2px solid {theme['shadow_inset_light']};
    border-left: 1px solid {theme['shadow_inset_light']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 2px solid {theme['border_focus']};
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

/* === RICH BUTTONS WITH MULTI-LAYER DEPTH === */
QPushButton {{
    padding: {tokens['spacing']['sm']} {tokens['spacing']['lg']};
    border-radius: {tokens['radius']['sm']};
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_bg_top']},
        stop:0.1 {theme['surface_elevated']},
        stop:0.9 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    color: {theme['text_primary']};
    font-weight: {tokens['font']['weight']['medium']};
    border-top: 1px solid {theme['button_border_light']};
    border-left: 1px solid {theme['button_border_light']};
    border-right: 1px solid {theme['button_border_dark']};
    border-bottom: 2px solid {theme['button_border_dark']};
    min-height: {tokens['button']['md']};
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_hover_top']},
        stop:0.1 {theme['surface_raised']},
        stop:0.9 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    border-top: 2px solid {theme['shadow_inset_light']};
    border-left: 1px solid {theme['shadow_inset_light']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 2px solid {theme['border_focus']};
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
    border-top: 1px solid #ff4d5a;
    border-left: 1px solid #ff4d5a;
    border-right: 2px solid #990008;
    border-bottom: 3px solid #660006;
    font-weight: {tokens['font']['weight']['bold']};
}}

QPushButton#primary:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff4d5a,
        stop:0.1 #ff1a2b,
        stop:0.9 {theme['primary']},
        stop:1 #cc0010);
    border-top: 2px solid #ff8a94;
    border-left: 1px solid #ff8a94;
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

/* === DEEP INSET TREE VIEW === */
QTreeView {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['tree_bg_inset']},
        stop:0.1 {theme['tree_bg']},
        stop:0.9 {theme['tree_bg']},
        stop:1 {theme['surface_solid']});
    border-top: 2px solid {theme['tree_border_outer']};
    border-left: 2px solid {theme['tree_border_outer']};
    border-right: 1px solid {theme['tree_border_inner']};
    border-bottom: 1px solid {theme['tree_border_inner']};
    border-radius: {tokens['radius']['md']};
    selection-background-color: {theme['selected']};
    selection-color: white;
}}

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

/* === DEEPLY INSET TEXT AREAS === */
QPlainTextEdit, QTextEdit {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['preview_bg_inset']},
        stop:0.1 {theme['preview_bg']},
        stop:0.9 {theme['preview_bg']},
        stop:1 {theme['surface_solid']});
    color: {theme['text_primary']};
    border-top: 2px solid {theme['preview_border_outer']};
    border-left: 2px solid {theme['preview_border_outer']};
    border-right: 1px solid {theme['preview_border_inner']};
    border-bottom: 1px solid {theme['preview_border_inner']};
    border-radius: {tokens['radius']['md']};
    padding: {tokens['spacing']['md']};
    font-family: {tokens['font']['family']};
    font-size: {tokens['font']['size']['sm']};
}}

QPlainTextEdit:focus, QTextEdit:focus {{
    border-top: 2px solid {theme['shadow_inset_dark']};
    border-left: 2px solid {theme['shadow_inset_dark']};
    border-right: 2px solid {theme['border_focus']};
    border-bottom: 2px solid {theme['border_focus']};
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_sunken']},
        stop:0.1 {theme['preview_bg']},
        stop:0.9 {theme['preview_bg']},
        stop:1 {theme['surface_elevated']});
}}

/* === RICH SCROLLBARS WITH DEPTH === */
QScrollBar:vertical {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {theme['surface_sunken']},
        stop:0.5 {theme['surface_solid']},
        stop:1 {theme['surface_elevated']});
    width: 14px;
    border-radius: 7px;
    border-top: 1px solid {theme['border']};
    border-left: 1px solid {theme['border']};
    border-right: 1px solid {theme['border_light']};
    border-bottom: 1px solid {theme['border_light']};
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
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['surface_sunken']},
        stop:0.5 {theme['surface_solid']},
        stop:1 {theme['surface_elevated']});
    height: 14px;
    border-radius: 7px;
    border-top: 1px solid {theme['border']};
    border-left: 1px solid {theme['border']};
    border-right: 1px solid {theme['border_light']};
    border-bottom: 1px solid {theme['border_light']};
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
    background: none;
    border: none;
}}

/* === RAISED COMBO BOXES === */
QComboBox {{
    padding: {tokens['spacing']['sm']} {tokens['spacing']['md']};
    border-radius: {tokens['radius']['sm']};
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_bg_top']},
        stop:0.1 {theme['surface_elevated']},
        stop:0.9 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    color: {theme['text_primary']};
    border-top: 1px solid {theme['button_border_light']};
    border-left: 1px solid {theme['button_border_light']};
    border-right: 1px solid {theme['button_border_dark']};
    border-bottom: 2px solid {theme['button_border_dark']};
    min-height: {tokens['button']['sm']};
}}

QComboBox:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_hover_top']},
        stop:0.1 {theme['surface_raised']},
        stop:0.9 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    border-top: 1px solid {theme['shadow_inset_light']};
    border-left: 1px solid {theme['shadow_inset_light']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 2px solid {theme['border_focus']};
    color: {theme['text_highlight']};
}}

QComboBox::drop-down {{
    border: none;
    background: transparent;
    width: 20px;
}}

QComboBox::down-arrow {{
    image: none;
    border-style: solid;
    border-width: 5px 4px 0 4px;
    border-color: {theme['text_primary']} transparent transparent transparent;
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
