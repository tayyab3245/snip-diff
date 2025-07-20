"""
Core design tokens shared across all themes
"""

# ========== DESIGN TOKENS ==========
# Single source of truth for all design values

DESIGN_TOKENS = {
    # === SPACING SYSTEM ===
    'spacing': {
        'xs': '4px',
        'sm': '8px', 
        'md': '12px',
        'lg': '16px',
        'xl': '24px',
        'xxl': '32px',
        'xxxl': '48px',
    },
    
    # === BORDER RADIUS ===
    'radius': {
        'sm': '6px',
        'md': '9px',
        'lg': '12px',
        'xl': '16px',
        'round': '50%',
    },
    
    # === TIMING & EASING ===
    'timing': {
        'fast': '0.12s',
        'normal': '0.18s', 
        'slow': '0.3s',
        'slower': '0.5s',
    },
    
    'easing': {
        'ease': 'ease',
        'ease_out': 'ease-out',
        'ease_in': 'ease-in',
        'ease_in_out': 'ease-in-out',
    },
    
    # === COMPONENT SIZES ===
    'button': {
        'sm': '32px',
        'md': '48px', 
        'lg': '64px',
    },
    
    # === FONTS ===
    'font': {
        'family': '-apple-system, "Segoe UI", "Fira Sans", sans-serif',
        'size': {
            'xs': '9pt',
            'sm': '10pt',
            'md': '11.2pt',
            'lg': '14pt',
            'xl': '18pt',
            'xxl': '24pt',
        },
        'weight': {
            'normal': '400',
            'medium': '500',
            'semibold': '600',
            'bold': '700',
        }
    },
    
    # === ICON SIZES ===
    'icon': {
        'sm': '16px',
        'md': '20px',
        'lg': '24px',
        'xl': '32px',
    }
}
