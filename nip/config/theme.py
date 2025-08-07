"""
================================================================================
SNIP-DIFF - AI workflow tool for preparing code context outside agentic environments
================================================================================

Copyright (c) 2025 Tayyab. All Rights Reserved.

PROPRIETARY AND CONFIDENTIAL

This software and associated documentation files (the "Software") are the 
exclusive property of the copyright holder. This Software contains proprietary 
and confidential information and is protected by copyright laws and 
international treaty provisions.

RESTRICTIONS:
- No part of this Software may be reproduced, distributed, or transmitted 
  in any form or by any means without the prior written permission of the 
  copyright holder.
- This Software is not for sale, license, or distribution to third parties.
- Reverse engineering, decompilation, or disassembly of this Software is 
  strictly prohibited.
- Any unauthorized use, copying, or distribution may result in severe civil 
  and criminal penalties.

This Software is provided "AS IS" without warranty of any kind, express or 
implied, including but not limited to the warranties of merchantability, 
fitness for a particular purpose, and non-infringement.

For licensing inquiries, please contact: tayyab3245@github.com
================================================================================
"""


"""
Unified Theme System - Single Source of Truth
Based on unified matte plastic design system with consistent visual DNA
"""

from .tokens import DESIGN_TOKENS
from .dark_theme_new import generate_dark_qss, DARK_UNIFIED
from .light_theme_fixed import generate_light_qss, LIGHT_UNIFIED

# Export design tokens for direct access
__all__ = ['DESIGN_TOKENS', 'get_theme', 'ThemeManager', 'STYLE']

class ThemeManager:
    """Enhanced theme manager with styling methods and utilities"""
    
    def __init__(self, mode: str = 'dark'):
        self.mode = mode
        self._themes = {
            'dark': {
                'qss': generate_dark_qss(),
                'colors': DARK_UNIFIED,
                'name': 'Dark Theme'
            },
            'light': {
                'qss': generate_light_qss(), 
                'colors': LIGHT_UNIFIED,
                'name': 'Light Theme'
            }
        }
    
    def get_qss(self, mode: str = None) -> str:
        """Get the complete QSS stylesheet for the specified theme"""
        theme_mode = mode or self.mode
        return self._themes.get(theme_mode, self._themes['dark'])['qss']
    
    def get_colors(self, mode: str = None) -> dict:
        """Get the color palette for the specified theme"""
        theme_mode = mode or self.mode
        return self._themes.get(theme_mode, self._themes['dark'])['colors']
    
    def get_theme_name(self, mode: str = None) -> str:
        """Get the human-readable name of the theme"""
        theme_mode = mode or self.mode
        return self._themes.get(theme_mode, self._themes['dark'])['name']
    
    def set_mode(self, mode: str):
        """Set the current theme mode"""
        if mode in self._themes:
            self.mode = mode
        else:
            raise ValueError(f"Unknown theme mode: {mode}. Available: {list(self._themes.keys())}")
    
    def get_available_themes(self) -> list:
        """Get list of available theme modes"""
        return list(self._themes.keys())
    
    def get_token(self, category: str, key: str = None):
        """Get design token value"""
        if key:
            return DESIGN_TOKENS.get(category, {}).get(key)
        return DESIGN_TOKENS.get(category)

# Global theme manager instance
theme_manager = ThemeManager()

def get_theme(mode: str = 'dark') -> dict:
    """
    Get theme with enhanced styling capabilities
    Returns theme object with colors, tokens, and utilities
    """
    return {
        'mode': mode,
        'qss': theme_manager.get_qss(mode),
        'colors': theme_manager.get_colors(mode),
        'tokens': DESIGN_TOKENS,
        'name': theme_manager.get_theme_name(mode)
    }

def get_component_color(component: str, state: str = 'default', mode: str = None) -> str:
    """
    Get color for specific component and state
    
    Args:
        component: Component name (e.g., 'toolbar', 'tree', 'button')
        state: State name (e.g., 'default', 'hover', 'pressed', 'disabled')
        mode: Theme mode ('dark' or 'light')
    
    Returns:
        Color value as string
    """
    colors = theme_manager.get_colors(mode)
    
    # Build key name from component and state
    if state == 'default':
        key = f'{component}_bg'
    else:
        key = f'{component}_{state}'
    
    return colors.get(key, colors.get('surface_solid', '#000000'))

def apply_theme_to_widget(widget, mode: str = None):
    """
    Apply theme stylesheet to a Qt widget
    
    Args:
        widget: Qt widget to apply theme to
        mode: Theme mode to apply ('dark' or 'light')
    """
    qss = theme_manager.get_qss(mode)
    widget.setStyleSheet(qss)

# Legacy compatibility - default to dark theme
STYLE = theme_manager.get_qss('dark')
