"""
Light Theme - Unified Matte Plastic Design System
Recreating rich depth, shadows, and highlights from game library
"""

from .tokens import DESIGN_TOKENS

tokens = DESIGN_TOKENS

# Light theme color palette (natural lighting and shadows)
LIGHT_UNIFIED = {
    # === CORE THEME ===
    'mode': 'light',
    'background': '#f8f9fa',
    'primary': '#e60012',
    'surface': '#ffffff',
    'text': '#2c3e50',
    'shadow': 'rgba(0,0,0,0.08)',
    'glow': 'rgba(230, 0, 18, 0.2)',
    
    # === LIGHT THEME DEPTH SYSTEM - Matching Dark Theme Contrast Ratios ===
    'panel_top': '#ffffff',        # Pure white highlight (equivalent to dark's #2e2e2e)
    'panel_bot': '#e0e0e0',        # Base surface (equivalent to dark's #1a1a1a)  
    'panel_edge': '#808080',       # Strong shadow (equivalent to dark's #0a0a0a)
    'panel_rim': '#ffffff',        # Pure white rim light (equivalent to dark's #404040)
    
    # Shadow layers - MATCHING dark theme's contrast ratios
    'shadow_inset_light': '#ffffff',                         # Pure white inner highlight
    'shadow_inset_dark': 'rgba(0, 0, 0, 0.6)',              # Strong dark inner shadow (matching dark's 0.8)
    'shadow_outer_near': 'rgba(0, 0, 0, 0.25)',             # Close shadow (matching dark's 0.4)
    'shadow_outer_far': 'rgba(0, 0, 0, 0.4)',               # Far shadow (matching dark's 0.6)
    
    # === CLEAN SURFACE VARIATIONS - Matching Dark Theme Relationships ===
    'surface_solid': '#e0e0e0',      # Base surface (equivalent to dark's #1a1a1a)
    'surface_secondary': '#d8d8d8',  # Secondary surfaces (equivalent to dark's #242424)
    'surface_elevated': '#ffffff',   # Elevated surfaces (equivalent to dark's #2e2e2e)
    'surface_sunken': '#c8c8c8',     # Sunken areas (equivalent to dark's #141414)
    'surface_raised': '#f8f8f8',     # Raised areas (equivalent to dark's #323232)
    
    # === NATURAL BORDERS - Soft and Clean ===
    'border': '#dee2e6',             # Soft natural border
    'border_light': '#f8f9fa',       # Light rim border
    'border_focus': '#e60012',       # Focus state
    'border_selection': '#e60012',   # Selection state
    
    # === READABLE TEXT HIERARCHY ===
    'text_primary': '#2c3e50',
    'text_secondary': 'rgba(44, 62, 80, 0.7)',
    'text_disabled': 'rgba(44, 62, 80, 0.4)',
    'text_inverse': '#ffffff',
    'text_highlight': '#2c3e50',     # Darker contrast for light theme emphasis
    
    # === INTERACTION STATES WITH DEPTH ===
    'hover': 'rgba(0, 0, 0, 0.04)',
    'hover_bright': 'rgba(0, 0, 0, 0.08)',
    'active': 'rgba(0, 0, 0, 0.12)',
    'active_deep': 'rgba(0, 0, 0, 0.20)',
    'selected': '#e60012',
    'focus': '#e60012',
    
    # === COMPONENT SPECIFIC WITH DARK THEME CONTRAST RATIOS ===
    'toolbar_bg': 'rgba(255,255,255,.96)',
    'toolbar_bg_top': '#ffffff',         # Pure white highlight (equivalent to dark's #2e2e2e)
    'toolbar_bg_bot': '#e0e0e0',         # Base surface (equivalent to dark's #1a1a1a)
    'toolbar_border_top': '#ffffff',     # Pure white rim light
    'toolbar_border_bot': '#808080',     # Strong shadow (equivalent to dark's #0a0a0a)
    
    # Clean up old button references - use new system  
    'button_bg_top': '#ffffff',          # Pure white highlight (equivalent to dark's #2e2e2e)
    'button_bg_bot': '#e0e0e0',          # Base surface color (equivalent to dark's #1a1a1a)
    'button_border_light': '#ffffff',    # Pure white rim light (equivalent to dark's #404040)
    'button_border_dark': '#808080',     # Strong shadow color (equivalent to dark's #0a0a0a)
    'button_hover_top': '#ffffff',       # Hover maintains highlight
    'button_hover_bot': '#d8d8d8',       # Slightly darker on hover (matching dark ratio)
    'button_pressed_top': '#d8d8d8',     # Pressed = darker (matching dark pressed ratio)
    'button_pressed_bot': '#808080',     # Strong shadow when pressed (matching dark edge)
    
    # Enhanced hover states for better illusion
    'tree_item_hover_light': 'rgba(230, 0, 18, 0.05)',
    'tree_item_hover_dark': 'rgba(0, 0, 0, 0.12)', # Stronger shadow on hover
}

def generate_light_qss() -> str:
    """Generate complete QSS stylesheet for light theme with rich matte plastic depth"""
    theme = LIGHT_UNIFIED
    
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
        stop:0.5 #f0f0f0, 
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
    border-top: 1px solid {theme['panel_top']};          /* Light highlight on top (matching dark's pattern) */
    border-left: 1px solid {theme['panel_top']};         /* Light highlight on left */
    border-right: 1px solid {theme['panel_edge']};       /* Dark shadow on right */
    border-bottom: 2px solid {theme['panel_edge']};      /* Stronger shadow on bottom */
    min-height: {tokens['button']['md']};
}}

#toolbar QToolButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_hover_top']},
        stop:0.1 {theme['surface_raised']},
        stop:0.9 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    border-top: 2px solid {theme['shadow_inset_light']};  /* Brighter highlight on hover */
    border-left: 1px solid {theme['shadow_inset_light']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 2px solid {theme['border_focus']};
    color: {theme['text_primary']};
}}

#toolbar QToolButton:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_pressed_top']},
        stop:0.2 {theme['surface_sunken']},
        stop:0.8 {theme['surface_sunken']},
        stop:1 {theme['button_pressed_bot']});
    border-top: 2px solid {theme['shadow_inset_dark']};   /* Dark shadow on top when pressed */
    border-left: 2px solid {theme['shadow_inset_dark']};  /* Dark shadow on left when pressed */
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 1px solid {theme['border_focus']};
    color: {theme['text_primary']};
}}

/* === RICH BUTTONS WITH HIGH-CONTRAST DEPTH === */
QPushButton {{
    padding: {tokens['spacing']['sm']} {tokens['spacing']['lg']};
    border-radius: {tokens['radius']['sm']};
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['panel_top']},
        stop:0.1 {theme['surface_elevated']},
        stop:0.9 {theme['surface_solid']},
        stop:1 {theme['panel_bot']});
    color: {theme['text_primary']};
    font-weight: {tokens['font']['weight']['medium']};
    min-height: {tokens['button']['md']};
    
    /* Raised button: highlights on top/left, shadows on bottom/right - matching dark theme exactly */
    border-top: 1px solid {theme['button_border_light']};
    border-left: 1px solid {theme['button_border_light']};
    border-right: 1px solid {theme['button_border_dark']};
    border-bottom: 2px solid {theme['button_border_dark']};
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_hover_top']},
        stop:0.1 {theme['surface_raised']},
        stop:0.9 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    color: {theme['text_highlight']};
    
    /* Enhanced raised appearance on hover - matching dark theme exactly */
    border-top: 2px solid {theme['shadow_inset_light']};
    border-left: 1px solid {theme['shadow_inset_light']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 2px solid {theme['border_focus']};
}}

QPushButton:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['button_pressed_top']},
        stop:0.2 {theme['surface_sunken']},
        stop:0.8 {theme['surface_sunken']},
        stop:1 {theme['button_pressed_bot']});
    color: {theme['text_primary']};
    
    /* Pressed = inset: shadows on top/left, highlights on bottom/right - matching dark theme exactly */
    border-top: 2px solid {theme['shadow_inset_dark']};
    border-left: 2px solid {theme['shadow_inset_dark']};
    border-right: 1px solid {theme['border_focus']};
    border-bottom: 1px solid {theme['border_focus']};
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

/* === DEEP INSET TREE VIEW (Light Theme) === */
QTreeView {{
    background: {theme['surface_sunken']};
    border-radius: {tokens['radius']['md']};
    selection-background-color: {theme['selected']};
    selection-color: white;
    
    /* Inset appearance: dark shadows on top/left, highlights on bottom/right - matching dark exactly */
    border-top: 2px solid {theme['panel_edge']};
    border-left: 2px solid {theme['panel_edge']};
    border-right: 1px solid {theme['panel_top']};
    border-bottom: 1px solid {theme['panel_top']};
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
    border: 1px solid {theme['border_light']};  /* Light border like dark theme */
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

/* === DEEPLY INSET TEXT AREAS (Light Theme) === */
QPlainTextEdit, QTextEdit {{
    background: {theme['surface_sunken']};
    color: {theme['text_primary']};
    border-radius: {tokens['radius']['md']};
    padding: {tokens['spacing']['md']};
    font-family: {tokens['font']['family']};
    font-size: {tokens['font']['size']['sm']};
    
    /* Inset appearance: dark shadows on top/left, highlights on bottom/right - matching dark exactly */
    border-top: 2px solid {theme['panel_edge']};
    border-left: 2px solid {theme['panel_edge']};
    border-right: 1px solid {theme['panel_top']};
    border-bottom: 1px solid {theme['panel_top']};
}}

QPlainTextEdit:focus, QTextEdit:focus {{
    background: {theme['surface_sunken']};
    
    /* Focus state maintains inset depth with colored borders - matching dark exactly */
    border-top: 2px solid {theme['border_focus']};
    border-left: 2px solid {theme['border_focus']};
    border-right: 1px solid {theme['panel_top']};
    border-bottom: 1px solid {theme['panel_top']};
}}

/* === RICH SCROLLBARS WITH DEPTH === */
QScrollBar:vertical {{
    background: {theme['surface_sunken']};               /* Consistent inset background */
    width: 14px;
    border-radius: 7px;
    border-top: 2px solid {theme['panel_edge']};         /* Dark shadow on top (inset) */
    border-left: 2px solid {theme['panel_edge']};        /* Dark shadow on left (inset) */
    border-right: 1px solid {theme['panel_top']};        /* Light highlight on right */
    border-bottom: 1px solid {theme['panel_top']};       /* Light highlight on bottom */
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
    background: {theme['surface_sunken']};               /* Consistent inset background */
    height: 14px;
    border-radius: 7px;
    border-top: 2px solid {theme['panel_edge']};         /* Dark shadow on top (inset) */
    border-left: 2px solid {theme['panel_edge']};        /* Dark shadow on left (inset) */
    border-right: 1px solid {theme['panel_top']};        /* Light highlight on right */
    border-bottom: 1px solid {theme['panel_top']};       /* Light highlight on bottom */
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
LIGHT_THEME = generate_light_qss()