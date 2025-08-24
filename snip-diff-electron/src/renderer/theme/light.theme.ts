/**
 * Light Theme for SNIP-DIFF  
 * Complete light mode color palette and styling definitions
 */

export const lightTheme = {
  mode: 'light' as const,
  
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
    primary: '#ffffff',      // Main app background
    secondary: '#f8fafc',    // Secondary background
    tertiary: '#f1f5f9',     // Elevated surfaces
    card: '#ffffff',         // Card backgrounds
    modal: '#ffffff',        // Modal backgrounds
  },

  // === NEUMORPHIC SURFACES ===
  surface: {
    base: '#e0e5ec',         // Main neumorphic surface
    raised: '#f0f0f3',       // Raised elements
    pressed: '#d1d9e6',      // Pressed/inset elements
    hover: '#e8edf5',        // Hover states
  },

  // === TEXT COLORS ===
  text: {
    primary: '#1e293b',      // Primary text (high contrast)
    secondary: '#475569',    // Secondary text
    tertiary: '#64748b',     // Tertiary text (muted)
    disabled: '#94a3b8',     // Disabled text
    inverse: '#f8fafc',      // Text on dark backgrounds
  },

  // === SEMANTIC COLORS ===
  semantic: {
    success: '#059669',      // Success states
    warning: '#d97706',      // Warning states
    error: '#dc2626',        // Error states
    info: '#2563eb',         // Info states
  },

  // === BORDERS ===
  border: {
    primary: '#e2e8f0',      // Primary borders
    secondary: '#cbd5e1',    // Secondary borders
    light: '#f1f5f9',        // Light borders
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
    light: {
      sm: '0 2px 4px rgba(0, 0, 0, 0.1)',
      md: '0 4px 8px rgba(0, 0, 0, 0.08)',
      lg: '0 8px 16px rgba(0, 0, 0, 0.06)',
      xl: '0 16px 32px rgba(0, 0, 0, 0.04)',
    },
  },

  // === COMPONENT-SPECIFIC COLORS ===
  components: {
    // File tree
    fileTree: {
      background: '#ffffff',
      hover: '#f1f5f9',
      selected: '#0ea5e9',
      text: '#475569',
      icon: '#64748b',
    },
    
    // Diff viewer
    diffViewer: {
      background: '#f8fafc',
      added: '#059669',
      removed: '#dc2626',
      modified: '#d97706',
      lineNumber: '#94a3b8',
      gutter: '#f1f5f9',
    },

    // Title bar
    titleBar: {
      background: '#ffffff',
      text: '#1e293b',
      controls: '#64748b',
      controlsHover: '#475569',
    },

    // Toolbar
    toolbar: {
      background: '#f8fafc',
      button: '#e2e8f0',
      buttonHover: '#cbd5e1',
      buttonActive: '#0ea5e9',
      text: '#475569',
    },

    // Status overlay
    statusOverlay: {
      background: 'rgba(255, 255, 255, 0.9)',
      text: '#1e293b',
      accent: '#0ea5e9',
    },

    // Progress indicators
    progress: {
      background: '#e2e8f0',
      fill: '#0ea5e9',
      text: '#1e293b',
    },
  },

  // === GRADIENTS ===
  gradients: {
    primary: 'linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)',
    surface: 'linear-gradient(145deg, #f0f0f3 0%, #e0e5ec 100%)',
    background: 'linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)',
  },
} as const;

// Type for light theme
export type LightTheme = typeof lightTheme;
