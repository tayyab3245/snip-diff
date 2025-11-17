/*
 * Copyright 2025 Tayyab
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * ThemeProvider for SNIP-DIFF
 * React context provider for theme management
 */

import React, { useEffect, ReactNode } from 'react';
import { createTheme, type EnhancedTheme, type ThemeMode } from './index';
import { ThemeContext, type ThemeContextType } from './theme-context';

// Re-export for convenience
export type { ThemeContextType };

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

  // Apply theme attributes to document root (CSS variables come from design-system.css)
  useEffect(() => {
    const root = document.documentElement;
    
    // Set theme mode as data attribute for CSS selectors
    root.setAttribute('data-theme', 'dark');
    
    // Add theme class for backward compatibility
    root.classList.remove('theme-light', 'theme-dark');
    root.classList.add('theme-dark');
    
    return () => {
      // Cleanup on unmount
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

export type { EnhancedTheme, ThemeMode };
