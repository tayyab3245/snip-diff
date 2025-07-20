"""
Light Theme - Modern Minimalist White Design System
Professional, clean aesthetic with enhanced contrast and visible depth
Balanced between flat design and 3D depth perception
"""

from .tokens import DESIGN_TOKENS

tokens = DESIGN_TOKENS

# Light theme color palette (modern minimalist white theme)
LIGHT_UNIFIED = {
    # === CORE THEME - Modern Minimalist Palette ===
    'mode': 'light',
    'background': '#f6f8fa',       # Very light, slightly cool gray for clarity
    'primary': '#e60012',
    'surface': '#ffffff',          # Pure white for raised elements like buttons and panels
    'text': '#24292e',             # Dark, near-black for maximum readability
    'shadow': 'rgba(0,0,0,0.08)',
    'glow': 'rgba(230, 0, 18, 0.2)',
    
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
    'surface_solid': '#e8eaed',      # Darker base surface
    'surface_secondary': '#dee1e6',  # Mid-tone secondary surfaces
    'surface_elevated': '#ffffff',   # Pure white for elevated surfaces
    'surface_sunken': '#d3d7dc',     # Noticeably darker for sunken areas
    'surface_raised': '#ffffff',     # Pure white for raised areas
    
    # === MODERN BORDERS - Enhanced Definition ===
    'border': '#b0b3b8',             # Stronger border color for definition
    'border_light': '#d8dce1',       # Mid-tone light border
    'border_focus': '#e60012',       # Focus state
    'border_selection': '#e60012',   # Selection state
    
    # === READABLE TEXT HIERARCHY ===
    'text_primary': '#24292e',       # Dark, near-black for maximum readability
    'text_secondary': 'rgba(36, 41, 46, 0.7)',
    'text_disabled': 'rgba(36, 41, 46, 0.4)',
    'text_inverse': '#ffffff',
    'text_highlight': '#24292e',     # Same as primary for consistency
    
    # === INTERACTION STATES WITH ENHANCED DEPTH ===
    'hover': 'rgba(0, 0, 0, 0.06)',
    'hover_bright': 'rgba(0, 0, 0, 0.10)',
    'active': 'rgba(0, 0, 0, 0.15)',
    'active_deep': 'rgba(0, 0, 0, 0.20)',
    'selected': '#e60012',
    'focus': '#e60012',
    
    # === COMPONENT SPECIFIC - Enhanced Contrast ===
    'toolbar_bg': 'rgba(255,255,255,.98)',
    'toolbar_bg_top': '#ffffff',         # Pure white for toolbar top
    'toolbar_bg_bot': '#e8eaed',         # Darker base for contrast
    'toolbar_border_top': 'rgba(255, 255, 255, 0.9)',     # Bright highlight
    'toolbar_border_bot': '#b0b3b8',     # Strong shadow for definition
    
    # Enhanced button system with better depth definition
    'button_bg_top': '#ffffff',          # Pure white for button highlights
    'button_bg_bot': '#e8eaed',          # Darker base for contrast
    'button_border_light': 'rgba(255, 255, 255, 0.9)',    # Bright highlight border
    'button_border_dark': '#b0b3b8',     # Strong border color for definition
    'button_hover_top': '#ffffff',       # Hover maintains white
    'button_hover_bot': '#dee1e6',       # More noticeable hover change
    'button_pressed_top': '#dee1e6',     # Pressed = noticeably darker
    'button_pressed_bot': '#d3d7dc',     # Clear press depth
    
    # Enhanced hover states with better contrast
    'tree_item_hover_light': 'rgba(230, 0, 18, 0.04)',
    'tree_item_hover_dark': 'rgba(0, 0, 0, 0.10)', # More visible shadow on hover
}

def generate_light_qss() -> str:
    """Generate complete QSS stylesheet for modern minimalist white theme with enhanced depth contrast"""
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
        stop:0 {theme['panel_rim']},
        stop:0.05 {theme['panel_top']},
        stop:0.95 {theme['surface_solid']},
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
        stop:0 {theme['panel_rim']},
        stop:0.05 {theme['button_bg_top']},
        stop:0.95 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    color: {theme['text_primary']};
    font-weight: {tokens['font']['weight']['medium']};
    border-top: 1px solid {theme['panel_rim']};          /* Bright rim light on top */
    border-left: 1px solid {theme['panel_rim']};         /* Bright rim light on left */
    border-right: 1px solid {theme['panel_edge']};       /* Dark shadow on right */
    border-bottom: 2px solid {theme['panel_edge']};      /* Stronger shadow on bottom */
    min-height: {tokens['button']['md']};
}}

#toolbar QToolButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['shadow_inset_light']},
        stop:0.05 {theme['button_hover_top']},
        stop:0.95 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    border-top: 2px solid {theme['shadow_inset_light']};  /* Brighter rim light on hover */
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
        stop:0 {theme['panel_rim']},
        stop:0.05 {theme['panel_top']},
        stop:0.95 {theme['surface_solid']},
        stop:1 {theme['panel_bot']});
    color: {theme['text_primary']};
    font-weight: {tokens['font']['weight']['medium']};
    min-height: {tokens['button']['md']};
    
    /* Raised button: rim light on top/left, shadows on bottom/right - matching dark theme exactly */
    border-top: 1px solid {theme['panel_rim']};
    border-left: 1px solid {theme['panel_rim']};
    border-right: 1px solid {theme['button_border_dark']};
    border-bottom: 2px solid {theme['button_border_dark']};
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['shadow_inset_light']},
        stop:0.05 {theme['button_hover_top']},
        stop:0.95 {theme['surface_elevated']},
        stop:1 {theme['button_hover_bot']});
    color: {theme['text_highlight']};
    
    /* Enhanced rim light appearance on hover - matching dark theme exactly */
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
        stop:0 {theme['panel_rim']},
        stop:0.05 {theme['button_bg_top']},
        stop:0.95 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    border-radius: 6px;
    border-top: 1px solid {theme['panel_rim']};
    border-left: 1px solid {theme['panel_rim']};
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
        stop:0 {theme['panel_rim']},
        stop:0.05 {theme['button_bg_top']},
        stop:0.95 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    border-radius: 6px;
    border-top: 1px solid {theme['panel_rim']};
    border-left: 1px solid {theme['panel_rim']};
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
        stop:0 {theme['panel_rim']},
        stop:0.05 {theme['button_bg_top']},
        stop:0.95 {theme['surface_solid']},
        stop:1 {theme['button_bg_bot']});
    color: {theme['text_primary']};
    border-top: 1px solid {theme['panel_rim']};
    border-left: 1px solid {theme['panel_rim']};
    border-right: 1px solid {theme['button_border_dark']};
    border-bottom: 2px solid {theme['button_border_dark']};
    min-height: {tokens['button']['sm']};
}}

QComboBox:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme['shadow_inset_light']},
        stop:0.05 {theme['button_hover_top']},
        stop:0.95 {theme['surface_elevated']},
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