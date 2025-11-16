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
    primary: '#0d0f12',      // Main app background - much darker
    secondary: '#13151a',    // Secondary background - much darker
    tertiary: '#1a1d23',     // Elevated surfaces - much darker
    card: '#13151a',         // Card backgrounds - much darker
    modal: '#0d0f12',        // Modal backgrounds - much darker
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
    primary: '#000000',      // Primary borders - darkest
    secondary: '#1a1d23',    // Secondary borders - much darker
    light: '#282c34',        // Light borders - darker
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
      background: '#0d0f12',
      hover: '#1a1d23',
      selected: '#1a1d23',
      text: '#adb5bd',
      icon: '#6c7a89',
    },
    
    // Diff viewer
    diffViewer: {
      background: '#13151a',
      added: '#22805e',      // Desaturated green - less bright
      removed: '#c53030',    // Desaturated red - less bright  
      modified: '#d69e2e',   // Desaturated yellow/orange
      lineNumber: '#6c7a89',
      gutter: '#0d0f12',
      border: '#1a1d23',
    },

    // Title bar
    titleBar: {
      background: '#0d0f12',
      text: '#e5e7eb',
      controls: '#6c7a89',
      controlsHover: '#adb5bd',
    },

    // Toolbar
    toolbar: {
      background: '#13151a',
      button: '#3a3f4b',
      buttonHover: '#454d5d',
      buttonActive: '#0ea5e9',
      text: '#adb5bd',
    },

    // Status overlay
    statusOverlay: {
      background: 'rgba(26, 29, 35, 0.95)',
      text: '#e5e7eb',
      accent: '#0ea5e9',
    },

    // Progress indicators
    progress: {
      background: '#282c34',
      fill: '#0ea5e9',
      text: '#e5e7eb',
    },

    // Chat panel
    chatPanel: {
      background: '#0a0c0f',
      messagesBackground: 'linear-gradient(135deg, rgba(10, 12, 15, 0.3) 0%, rgba(13, 15, 18, 0.2) 100%)',
      emptyStateText: '#adb5bd',
      
      // Message styles
      aiMessage: {
        background: 'transparent',
        text: '#e5e7eb',
        border: 'none',
      },
      systemMessage: {
        background: 'rgba(56, 139, 253, 0.1)',
        text: '#d1d5db',
        border: '1px solid #282c34',
      },
      errorMessage: {
        background: 'rgba(220, 38, 38, 0.1)',
        text: '#fca5a5',
        border: '1px solid rgba(220, 38, 38, 0.3)',
      },
      
      // Status and loading
      statusText: '#9ca3af',
      loadingDotsBackground: 'rgba(0, 0, 0, 0.1)',
      
      // Scrollbar
      scrollbar: {
        width: '6px',
        track: 'rgba(0, 0, 0, 0.1)',
        thumb: 'rgba(156, 163, 175, 0.5)',
        thumbHover: 'rgba(156, 163, 175, 0.7)',
      },
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
