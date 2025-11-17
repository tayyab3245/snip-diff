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
