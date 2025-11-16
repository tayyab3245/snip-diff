# SNIP-DIFF Theme System

A comprehensive dark theme system for the SNIP-DIFF application with neumorphic styling, design tokens, and component-specific colors.

## Architecture Overview

```
theme/
├── tokens.ts          # Design system tokens (spacing, typography, etc.)
├── dark-theme.ts      # Complete dark theme color palette
├── index.ts           # Theme orchestration and utilities
├── theme-provider.tsx # React context provider
└── README.md          # This documentation
```

## Quick Start

### 1. Wrap your app with ThemeProvider

```tsx
import { ThemeProvider } from './theme/ThemeProvider';

function App() {
  return (
    <ThemeProvider defaultTheme="dark">
      <YourAppComponents />
    </ThemeProvider>
  );
}
```

### 2. Use the theme in components

```tsx
import { useTheme } from './theme';

function MyComponent() {
  const { theme } = useTheme();

  return (
    <div style={{
      backgroundColor: theme.colors.background.primary,
      color: theme.colors.text.primary,
      padding: theme.tokens.spacing.md,
      borderRadius: theme.tokens.radius.lg,
    }}>
      Themed component
    </div>
  );
}
```

### 3. Access theme values directly

```tsx
import { darkTheme } from './theme';

const styles = {
  background: darkTheme.background.primary,
  textColor: darkTheme.text.primary,
};
```

## Theme Structure

### Design Tokens (tokens.ts)
Shared values across themes:
- **Spacing**: `xs`, `sm`, `md`, `lg`, `xl`, `xxl`, `xxxl`
- **Border Radius**: `none`, `sm`, `md`, `lg`, `xl`, `xxl`, `round`
- **Typography**: Font families, sizes, weights, line heights
- **Shadows**: Standard box shadows and neumorphic shadows
- **Transitions**: Animation timings
- **Breakpoints**: Responsive design points

### Dark Theme (dark-theme.ts)
Complete dark mode palette including:
- **Primary Colors**: Blue scale (50-900)
- **Backgrounds**: Primary, secondary, tertiary, card, modal
- **Surfaces**: Base, raised, pressed, hover (neumorphic)
- **Text**: Primary, secondary, tertiary, disabled, inverse
- **Semantic**: Success, warning, error, info
- **Borders**: Primary, secondary, light, focus
- **Component Colors**: FileTree, DiffViewer, TitleBar, Toolbar, etc.
- **Neumorphic Shadows**: Raised, pressed, and float effects

## Theme Hooks

### useTheme()
Main theme hook providing:
```tsx
const { theme, themeMode, isDark } = useTheme();
```

### useThemedStyles()
CSS-in-JS styling:
```tsx
const styles = useThemedStyles((theme) => ({
  container: {
    backgroundColor: theme.colors.background.primary,
    padding: theme.tokens.spacing.md,
  },
}));
```

### useThemeValue()
Conditional values (currently always returns dark values):
```tsx
const color = useThemeValue(lightValue, darkValue); // Always returns darkValue
```

## CSS Custom Properties

The theme automatically generates CSS variables on the document root:

```css
:root {
  --color-primary-500: #0ea5e9;
  --color-bg-primary: #2b303b;
  --color-text-primary: #e5e7eb;
  --spacing-md: 12px;
  --radius-lg: 12px;
}
```

## Component Integration

All major SNIP-DIFF components use the theme system:

- **FileTree**: Uses `theme.colors.components.fileTree.*`
- **TitleBar**: Uses `theme.colors.components.titleBar.*`
- **ActionBar**: Uses `theme.colors.background.secondary`
- **Layout**: Uses `theme.colors.background.primary`
- **ContextBar**: Uses neumorphic shadows

## Color Palette

### Primary Colors
```
50: #f0f9ff  100: #e0f2fe  200: #bae6fd
300: #7dd3fc  400: #38bdf8  500: #0ea5e9 (main)
600: #0284c7  700: #0369a1  800: #075985
900: #0c4a6e
```

### Background Hierarchy
- **Primary**: `#2b303b` (main app background)
- **Secondary**: `#343941` (elevated surfaces)
- **Tertiary**: `#3c424e` (highest elevation)
- **Card**: `#343941` (card backgrounds)

### Text Colors
- **Primary**: `#e5e7eb` (main text)
- **Secondary**: `#adb5bd` (muted text)
- **Tertiary**: `#6c7a89` (very muted)
- **Disabled**: `#545d6d` (inactive text)

## Neumorphic Design

The theme includes neumorphic shadow effects:

```css
/* Raised effect */
box-shadow:
  20px 20px 60px #bebebe,
  -20px -20px 60px #ffffff;

/* Pressed effect */
box-shadow:
  inset 20px 20px 60px #bebebe,
  inset -20px -20px 60px #ffffff;
```

## Current Limitations

- **Dark theme only**: No light theme implementation
- **No theme switching**: Always uses dark theme
- **No styled components**: Uses inline styles and CSS modules
- **No pre-built UI library**: Components use theme values directly

## Future Enhancements

- Light theme implementation
- Theme switching capability
- Styled components library
- Pre-built UI component library
- Theme customization options

## Usage Examples

### Basic Theming
```tsx
function ThemedButton({ children, onClick }) {
  const { theme } = useTheme();

  return (
    <button
      onClick={onClick}
      style={{
        backgroundColor: theme.colors.primary[500],
        color: theme.colors.text.inverse,
        padding: `${theme.tokens.spacing.sm} ${theme.tokens.spacing.md}`,
        borderRadius: theme.tokens.radius.md,
        border: 'none',
        cursor: 'pointer',
      }}
    >
      {children}
    </button>
  );
}
```

### Component-Specific Styling
```tsx
function FileTreeItem({ file, isSelected }) {
  const { theme } = useTheme();

  return (
    <div style={{
      backgroundColor: isSelected
        ? theme.colors.components.fileTree.selected
        : theme.colors.components.fileTree.background,
      color: theme.colors.components.fileTree.text,
      padding: theme.tokens.spacing.sm,
    }}>
      {file.name}
    </div>
  );
}
```

## Development

The theme system is actively used throughout the SNIP-DIFF application and provides consistent styling across all components.
