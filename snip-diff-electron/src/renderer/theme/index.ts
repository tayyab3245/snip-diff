/**
 * Theme System Index for SNIP-DIFF
 * Unified access to all theme data and utilities
 */

import { designTokens, type DesignTokens } from './tokens';
import { darkTheme, type DarkTheme } from './dark-theme';

// Re-export everything for easy access
export { designTokens } from './tokens';
export { darkTheme } from './dark-theme';
export { 
  ThemeProvider, 
  useTheme, 
  useThemedStyles, 
  useThemeValue, 
  useSystemTheme,
  withTheme,
  themes as prebuiltThemes
} from './theme-provider';

// Union type for both themes
export type Theme = DarkTheme;
export type ThemeMode = 'dark';

// Enhanced theme interface with tokens and utilities
export interface EnhancedTheme {
  mode: ThemeMode;
  colors: Theme;
  tokens: DesignTokens;
  utils: ThemeUtils;
}

// Theme utilities for common operations
export interface ThemeUtils {
  // Get color with opacity
  alpha: (color: string, opacity: number) => string;
  
  // Mix two colors
  mix: (color1: string, color2: string, amount: number) => string;
  
  // Get contrast color (black or white) for a background
  getContrastColor: (backgroundColor: string) => string;
  
  // Generate neumorphic box shadow
  neumorphic: (type: 'raised' | 'pressed' | 'float', intensity?: number) => string;
  
  // Responsive value based on breakpoint
  responsive: (values: { [key: string]: string }) => string;
}

// Theme utilities implementation
const createThemeUtils = (theme: Theme): ThemeUtils => ({
  alpha: (color: string, opacity: number) => {
    // Simple implementation - in production you'd use a color library
    if (color.startsWith('#')) {
      const hex = color.slice(1);
      const alpha = Math.round(opacity * 255).toString(16).padStart(2, '0');
      return `#${hex}${alpha}`;
    }
    return `rgba(${color}, ${opacity})`;
  },

  mix: (color1: string, _color2: string, _amount: number) => {
    // Simplified mixing - use a proper color library in production
    return color1; // Placeholder
  },

  getContrastColor: (_backgroundColor: string) => {
    // Simple contrast logic - enhance with proper luminance calculation
    return theme.mode === 'dark' ? theme.text.primary : theme.text.inverse;
  },

  neumorphic: (type: 'raised' | 'pressed' | 'float', _intensity = 1) => {
    const shadows = theme.shadows.neumorphic;
    switch (type) {
      case 'raised':
        return shadows.raised;
      case 'pressed':
        return shadows.pressed;
      case 'float':
        return shadows.float;
      default:
        return shadows.raised;
    }
  },

  responsive: (values: { [key: string]: string }) => {
    // Generate responsive CSS - simplified implementation
    return values.base || Object.values(values)[0];
  },
});

// Theme factory function
export const createTheme = (mode: ThemeMode): EnhancedTheme => {
  const colors = darkTheme;
  
  return {
    mode,
    colors,
    tokens: designTokens,
    utils: createThemeUtils(colors),
  };
};

// Pre-built themes
export const themes = {
  dark: createTheme('dark'),
} as const;

// Default theme
export const defaultTheme = themes.dark;

// Theme type guards
export const isDarkTheme = (theme: Theme): theme is DarkTheme => theme.mode === 'dark';

// CSS custom properties generator
export const generateCSSVariables = (theme: EnhancedTheme): Record<string, string> => {
  const vars: Record<string, string> = {};
  
  // Generate CSS variables for colors
  Object.entries(theme.colors.primary).forEach(([key, value]) => {
    vars[`--color-primary-${key}`] = value;
  });
  
  Object.entries(theme.colors.background).forEach(([key, value]) => {
    vars[`--color-bg-${key}`] = value;
  });
  
  Object.entries(theme.colors.text).forEach(([key, value]) => {
    vars[`--color-text-${key}`] = value;
  });
  
  // Generate CSS variables for tokens
  Object.entries(theme.tokens.spacing).forEach(([key, value]) => {
    vars[`--spacing-${key}`] = value;
  });
  
  Object.entries(theme.tokens.radius).forEach(([key, value]) => {
    vars[`--radius-${key}`] = value;
  });
  
  return vars;
};
