/**
 * ThemeProvider for SNIP-DIFF
 * React context provider for theme management
 */

import React, { createContext, useContext, useEffect, ReactNode } from 'react';
import { createTheme, type EnhancedTheme, type ThemeMode, themes, generateCSSVariables } from './index';

// Theme context interface
interface ThemeContextType {
  theme: EnhancedTheme;
  themeMode: ThemeMode;
  toggleTheme: () => void;
  setThemeMode: (mode: ThemeMode) => void;
  isDark: boolean;
  isLight: boolean;
}

// Create the context
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Theme provider props
interface ThemeProviderProps {
  children: ReactNode;
  defaultTheme?: ThemeMode;
  storageKey?: string;
}

// Local storage key for theme persistence
const DEFAULT_STORAGE_KEY = 'snip-diff-theme-mode';

// Theme provider component
export const ThemeProvider: React.FC<ThemeProviderProps> = ({
  children,
  storageKey = DEFAULT_STORAGE_KEY,
}) => {
  // Create current theme (always dark)
  const theme = createTheme('dark');

  // Update localStorage when theme changes (always dark)
  useEffect(() => {
    try {
      localStorage.setItem(storageKey, 'dark');
    } catch (error) {
      console.warn('Failed to save theme to localStorage:', error);
    }
  }, [storageKey]);

  // Apply CSS variables to document root
  useEffect(() => {
    const root = document.documentElement;
    const cssVariables = generateCSSVariables(theme);
    
    // Apply CSS custom properties
    Object.entries(cssVariables).forEach(([property, value]) => {
      root.style.setProperty(property, value);
    });
    
    // Set theme mode as data attribute for CSS selectors
    root.setAttribute('data-theme', 'dark');
    
    // Add theme class for backward compatibility
    root.classList.remove('theme-light', 'theme-dark');
    root.classList.add('theme-dark');
    
    return () => {
      // Cleanup on unmount
      Object.keys(cssVariables).forEach((property) => {
        root.style.removeProperty(property);
      });
      root.removeAttribute('data-theme');
      root.classList.remove('theme-dark');
    };
  }, [theme]);

  // Theme management functions (no-op now, always dark)
  const setThemeMode = (_mode: ThemeMode) => {
    // Always dark mode, do nothing
  };

  const toggleTheme = () => {
    // Always dark mode, do nothing
  };

  // Context value
  const contextValue: ThemeContextType = {
    theme,
    themeMode: 'dark',
    toggleTheme,
    setThemeMode,
    isDark: true,
    isLight: false,
  };

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
};

// Custom hook to use theme context
export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  
  return context;
};

// HOC for class components
export function withTheme<P extends object>(
  Component: React.ComponentType<P & { theme: EnhancedTheme }>
) {
  const ThemedComponent = (props: P) => {
    const { theme } = useTheme();
    return <Component {...props} theme={theme} />;
  };
  
  ThemedComponent.displayName = `withTheme(${Component.displayName || Component.name})`;
  return ThemedComponent;
}

// Hook for CSS-in-JS styling
export function useThemedStyles<T extends Record<string, any>>(
  stylesFactory: (theme: EnhancedTheme) => T
): T {
  const { theme } = useTheme();
  return React.useMemo(() => stylesFactory(theme), [theme, stylesFactory]);
}

// Helper hook for conditional theme values
export function useThemeValue<T>(lightValue: T, darkValue: T): T {
  const { isDark } = useTheme();
  return isDark ? darkValue : lightValue;
}

// System theme detection hook (always returns dark)
export function useSystemTheme(): ThemeMode {
  return 'dark';
}

// Export pre-configured themes for direct use
export { themes };
export type { EnhancedTheme, ThemeMode, ThemeContextType };
