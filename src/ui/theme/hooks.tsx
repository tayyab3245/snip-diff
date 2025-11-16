/**
 * Theme hooks for SNIP-DIFF
 * Separated from theme-provider to fix Fast Refresh warnings
 */

import React, { useContext } from 'react';
import { ThemeContext, type ThemeContextType } from './theme-context';
import type { EnhancedTheme, ThemeMode } from './index';

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
  stylesFactory: (_theme: EnhancedTheme) => T
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
