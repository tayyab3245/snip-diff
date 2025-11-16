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
    primary: '#2b303b',      // Main app background - matching mockup
    secondary: '#343941',    // Secondary background
    tertiary: '#3c424e',     // Elevated surfaces
    card: '#343941',         // Card backgrounds
    modal: '#2b303b',        // Modal backgrounds
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
    primary: '#e5e7eb',      // Primary text - softer white
    secondary: '#adb5bd',    // Secondary text
    tertiary: '#6c7a89',     // Tertiary text (muted)
    disabled: '#545d6d',     // Disabled text
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
    primary: '#1e2229',      // Primary borders - darker
    secondary: '#3c424e',    // Secondary borders
    light: '#4a5261',        // Light borders
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
      background: '#2b303b',
      hover: '#3c424e',
      selected: '#3c424e',
      text: '#adb5bd',
      icon: '#6c7a89',
    },
    
    // Diff viewer
    diffViewer: {
      background: '#343941',
      added: '#22c55e',
      removed: '#ef4444',
      modified: '#f59e0b',
      lineNumber: '#6c7a89',
      gutter: '#2b303b',
    },

    // Title bar
    titleBar: {
      background: '#2b303b',
      text: '#e5e7eb',
      controls: '#6c7a89',
      controlsHover: '#adb5bd',
    },

    // Toolbar
    toolbar: {
      background: '#343941',
      button: '#4a5261',
      buttonHover: '#545d6d',
      buttonActive: '#0ea5e9',
      text: '#adb5bd',
    },

    // Status overlay
    statusOverlay: {
      background: 'rgba(43, 48, 59, 0.95)',
      text: '#e5e7eb',
      accent: '#0ea5e9',
    },

    // Progress indicators
    progress: {
      background: '#3c424e',
      fill: '#0ea5e9',
      text: '#e5e7eb',
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
