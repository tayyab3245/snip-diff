/**
 * ThemeProvider for SNIP-DIFF
 * React context provider for theme management
 */

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
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
  defaultTheme = 'light',
  storageKey = DEFAULT_STORAGE_KEY,
}) => {
  // Initialize theme from localStorage or default
  const [themeMode, setThemeModeState] = useState<ThemeMode>(() => {
    if (typeof window === 'undefined') return defaultTheme;
    
    try {
      const stored = localStorage.getItem(storageKey);
      if (stored && (stored === 'light' || stored === 'dark')) {
        return stored as ThemeMode;
      }
    } catch (error) {
      console.warn('Failed to read theme from localStorage:', error);
    }
    
    return defaultTheme;
  });

  // Create current theme
  const theme = createTheme(themeMode);

  // Update localStorage when theme changes
  useEffect(() => {
    try {
      localStorage.setItem(storageKey, themeMode);
    } catch (error) {
      console.warn('Failed to save theme to localStorage:', error);
    }
  }, [themeMode, storageKey]);

  // Apply CSS variables to document root
  useEffect(() => {
    const root = document.documentElement;
    const cssVariables = generateCSSVariables(theme);
    
    // Apply CSS custom properties
    Object.entries(cssVariables).forEach(([property, value]) => {
      root.style.setProperty(property, value);
    });
    
    // Set theme mode as data attribute for CSS selectors
    root.setAttribute('data-theme', themeMode);
    
    // Add theme class for backward compatibility
    root.classList.remove('theme-light', 'theme-dark');
    root.classList.add(`theme-${themeMode}`);
    
    return () => {
      // Cleanup on unmount
      Object.keys(cssVariables).forEach((property) => {
        root.style.removeProperty(property);
      });
      root.removeAttribute('data-theme');
      root.classList.remove('theme-light', 'theme-dark');
    };
  }, [theme, themeMode]);

  // Theme management functions
  const setThemeMode = (mode: ThemeMode) => {
    setThemeModeState(mode);
  };

  const toggleTheme = () => {
    setThemeModeState(prev => prev === 'light' ? 'dark' : 'light');
  };

  // Context value
  const contextValue: ThemeContextType = {
    theme,
    themeMode,
    toggleTheme,
    setThemeMode,
    isDark: themeMode === 'dark',
    isLight: themeMode === 'light',
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

// System theme detection hook
export function useSystemTheme(): ThemeMode {
  const [systemTheme, setSystemTheme] = useState<ThemeMode>('light');

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const updateTheme = (e: MediaQueryListEvent) => {
      setSystemTheme(e.matches ? 'dark' : 'light');
    };

    // Set initial value
    setSystemTheme(mediaQuery.matches ? 'dark' : 'light');

    // Listen for changes
    mediaQuery.addEventListener('change', updateTheme);

    return () => {
      mediaQuery.removeEventListener('change', updateTheme);
    };
  }, []);

  return systemTheme;
}

// Export pre-configured themes for direct use
export { themes };
export type { EnhancedTheme, ThemeMode, ThemeContextType };
