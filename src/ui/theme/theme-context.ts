/**
 * Theme Context for SNIP-DIFF
 * Separated to fix Fast Refresh warnings
 */

import { createContext } from 'react';
import type { EnhancedTheme, ThemeMode } from './index';

// Theme context interface
export interface ThemeContextType {
  theme: EnhancedTheme;
  themeMode: ThemeMode;
  toggleTheme: () => void;
  setThemeMode: (_mode: ThemeMode) => void;
  isDark: boolean;
  isLight: boolean;
}

// Create the context
export const ThemeContext = createContext<ThemeContextType | undefined>(undefined);
