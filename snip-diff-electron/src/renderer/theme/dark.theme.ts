/**
 * Dark Theme for SNIP-DIFF
 * Complete dark mode color palette and styling definitions
 */

export const darkTheme = {
  mode: 'dark' as const,
  
  // === PRIMARY COLORS ===
  primary: {
    50: '#f0f9ff',
    100: '#e0f2fe', 
    200: '#bae6fd',
    300: '#7dd3fc',
    400: '#38bdf8',
    500: '#0ea5e9',  // Main brand color
    600: '#0284c7',
    700: '#0369a1',
    800: '#075985',
    900: '#0c4a6e',
  },

  // === SURFACES & BACKGROUNDS ===
  background: {
    primary: '#0f0f23',      // Main app background
    secondary: '#1a1a2e',    // Secondary background
    tertiary: '#16213e',     // Elevated surfaces
    card: '#1e1e2e',         // Card backgrounds
    modal: '#16213e',        // Modal backgrounds
  },

  // === NEUMORPHIC SURFACES ===
  surface: {
    base: '#e0e5ec',         // Main neumorphic surface (kept light for contrast)
    raised: '#f0f0f3',       // Raised elements
    pressed: '#d1d9e6',      // Pressed/inset elements
    hover: '#e8edf5',        // Hover states
  },

  // === TEXT COLORS ===
  text: {
    primary: '#f8fafc',      // Primary text (high contrast)
    secondary: '#cbd5e1',    // Secondary text
    tertiary: '#94a3b8',     // Tertiary text (muted)
    disabled: '#64748b',     // Disabled text
    inverse: '#1e293b',      // Text on light backgrounds
  },

  // === SEMANTIC COLORS ===
  semantic: {
    success: '#10b981',      // Success states
    warning: '#f59e0b',      // Warning states  
    error: '#ef4444',        // Error states
    info: '#3b82f6',         // Info states
  },

  // === BORDERS ===
  border: {
    primary: '#334155',      // Primary borders
    secondary: '#475569',    // Secondary borders
    light: '#64748b',        // Light borders
    focus: '#0ea5e9',        // Focus rings
  },

  // === NEUMORPHIC SHADOWS ===
  shadows: {
    neumorphic: {
      raised: `
        20px 20px 60px #bebebe,
        -20px -20px 60px #ffffff
      `,
      pressed: `
        inset 20px 20px 60px #bebebe,
        inset -20px -20px 60px #ffffff
      `,
      float: `
        0 8px 32px rgba(0, 0, 0, 0.12),
        0 4px 16px rgba(0, 0, 0, 0.08)
      `,
    },
    dark: {
      sm: '0 2px 4px rgba(0, 0, 0, 0.5)',
      md: '0 4px 8px rgba(0, 0, 0, 0.4)',
      lg: '0 8px 16px rgba(0, 0, 0, 0.3)',
      xl: '0 16px 32px rgba(0, 0, 0, 0.2)',
    },
  },

  // === COMPONENT-SPECIFIC COLORS ===
  components: {
    // File tree
    fileTree: {
      background: '#1a1a2e',
      hover: '#252545',
      selected: '#0ea5e9',
      text: '#cbd5e1',
      icon: '#94a3b8',
    },
    
    // Diff viewer
    diffViewer: {
      background: '#16213e',
      added: '#10b981',
      removed: '#ef4444',
      modified: '#f59e0b',
      lineNumber: '#64748b',
      gutter: '#1e293b',
    },

    // Title bar
    titleBar: {
      background: '#0f0f23',
      text: '#f8fafc',
      controls: '#94a3b8',
      controlsHover: '#cbd5e1',
    },

    // Toolbar
    toolbar: {
      background: '#1a1a2e',
      button: '#334155',
      buttonHover: '#475569',
      buttonActive: '#0ea5e9',
      text: '#cbd5e1',
    },

    // Status overlay
    statusOverlay: {
      background: 'rgba(15, 15, 35, 0.9)',
      text: '#f8fafc',
      accent: '#0ea5e9',
    },

    // Progress indicators
    progress: {
      background: '#334155',
      fill: '#0ea5e9',
      text: '#f8fafc',
    },
  },

  // === GRADIENTS ===
  gradients: {
    primary: 'linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)',
    surface: 'linear-gradient(145deg, #e0e5ec 0%, #d1d9e6 100%)',
    background: 'linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%)',
  },
} as const;

// Type for dark theme
export type DarkTheme = typeof darkTheme;
