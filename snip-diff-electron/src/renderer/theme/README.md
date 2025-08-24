# SNIP-DIFF Theme System

A comprehensive, modular theme system for the SNIP-DIFF application with support for dark and light modes, neumorphic styling, and design tokens.

## Architecture Overview

The theme system follows a modular architecture with separate files as the source of truth:

```
theme/
├── tokens.ts          # Design system tokens (spacing, typography, etc.)
├── dark.theme.ts      # Complete dark theme color palette
├── light.theme.ts     # Complete light theme color palette
├── index.ts           # Theme orchestration and utilities
├── ThemeProvider.tsx  # React context provider
├── styled.ts          # Styled components
├── styled.d.ts        # TypeScript declarations
└── demo.tsx           # Example usage
```

## Quick Start

### 1. Wrap your app with ThemeProvider

```tsx
import { ThemeProvider } from './theme/ThemeProvider';

function App() {
  return (
    <ThemeProvider defaultTheme="light">
      <YourAppComponents />
    </ThemeProvider>
  );
}
```

### 2. Use the theme in components

```tsx
import { useTheme } from './theme/ThemeProvider';
import { GlobalThemeStyles, Button, Surface, Text } from './theme/styled';

function MyComponent() {
  const { theme, toggleTheme, isDark } = useTheme();
  
  return (
    <>
      <GlobalThemeStyles />
      <Surface variant="raised">
        <Text size="lg" weight="semibold">
          Current theme: {theme.mode}
        </Text>
        <Button onClick={toggleTheme} variant="primary">
          Switch to {isDark ? 'Light' : 'Dark'}
        </Button>
      </Surface>
    </>
  );
}
```

### 3. Access theme values directly

```tsx
function CustomComponent() {
  const { theme } = useTheme();
  
  return (
    <div style={{
      backgroundColor: theme.colors.background.primary,
      color: theme.colors.text.primary,
      padding: theme.tokens.spacing.md,
      borderRadius: theme.tokens.radius.lg,
    }}>
      Custom styled component
    </div>
  );
}
```

## Theme Structure

### Design Tokens (tokens.ts)
Shared values across all themes:
- **Spacing**: `xs`, `sm`, `md`, `lg`, `xl`, `xxl`, `xxxl`
- **Border Radius**: `none`, `sm`, `md`, `lg`, `xl`, `xxl`, `round`
- **Typography**: Font families, sizes, weights, line heights
- **Shadows**: Standard box shadows
- **Transitions**: Animation timings
- **Breakpoints**: Responsive design points

### Dark Theme (dark.theme.ts)
Complete dark mode palette including:
- **Primary Colors**: Blue scale (50-900)
- **Backgrounds**: Primary, secondary, tertiary, card, modal
- **Surfaces**: Base, raised, pressed, hover (neumorphic)
- **Text**: Primary, secondary, tertiary, disabled, inverse
- **Semantic**: Success, warning, error, info
- **Borders**: Primary, secondary, tertiary
- **Shadows**: Standard and neumorphic shadows
- **Component Colors**: FileTree, DiffViewer, TitleBar, etc.

### Light Theme (light.theme.ts)
Matching light mode structure with appropriate colors.

## Using Styled Components

### Pre-built Components

```tsx
import { 
  Container, 
  FlexContainer, 
  Surface, 
  Button, 
  Input, 
  Text, 
  Divider 
} from './theme/styled';

// Layout
<Container maxWidth="1200px">
  <FlexContainer direction="column" gap="20px">
    <Surface variant="raised" padding="24px">
      Content here
    </Surface>
  </FlexContainer>
</Container>

// Typography
<Text size="xl" weight="bold" variant="primary">
  Heading
</Text>
<Text size="sm" variant="secondary">
  Subtitle
</Text>

// Buttons
<Button variant="primary" size="lg" onClick={handleClick}>
  Primary Action
</Button>
<Button variant="secondary" size="sm">
  Secondary Action
</Button>

// Inputs
<Input placeholder="Enter text..." />
<Input variant="filled" hasError />
```

### Component Variants

**Surface variants:**
- `flat` (default): Basic border
- `raised`: Elevated appearance
- `pressed`: Inset appearance

**Button variants:**
- `primary`: Main brand color
- `secondary`: Subtle background
- `ghost`: Transparent background

**Text variants:**
- `primary`: Main text color
- `secondary`: Muted text
- `tertiary`: Very muted text
- `error`: Error color
- `success`: Success color
- `warning`: Warning color

## Theme Hooks

### useTheme()
Main theme hook providing:
```tsx
const {
  theme,        // Current enhanced theme object
  themeMode,    // 'light' | 'dark'
  toggleTheme,  // Function to switch themes
  setThemeMode, // Function to set specific theme
  isDark,       // Boolean for dark mode
  isLight,      // Boolean for light mode
} = useTheme();
```

### useThemeValue()
Conditional values based on theme:
```tsx
const iconColor = useThemeValue('#333', '#fff'); // light, dark
const fontSize = useThemeValue('14px', '16px');
```

### useThemedStyles()
CSS-in-JS styling:
```tsx
const styles = useThemedStyles((theme) => ({
  container: {
    backgroundColor: theme.colors.background.primary,
    padding: theme.tokens.spacing.md,
  },
  text: {
    color: theme.colors.text.primary,
    fontSize: theme.tokens.typography.fontSize.lg,
  },
}));
```

## Customization

### Adding New Colors
1. Add to both `dark.theme.ts` and `light.theme.ts`
2. Maintain consistent structure between themes
3. Use semantic naming for reusability

### Extending Design Tokens
1. Add new tokens to `tokens.ts`
2. Update TypeScript interfaces if needed
3. Use tokens consistently across themes

### Custom Components
Create theme-aware components:
```tsx
import styled from 'styled-components';
import { EnhancedTheme } from './theme';

const CustomCard = styled.div<{ variant?: 'default' | 'highlighted' }>`
  background-color: ${({ theme, variant }) => 
    variant === 'highlighted' 
      ? theme.colors.primary[100] 
      : theme.colors.background.card
  };
  padding: ${({ theme }) => theme.tokens.spacing.lg};
  border-radius: ${({ theme }) => theme.tokens.radius.lg};
  border: 1px solid ${({ theme }) => theme.colors.border.primary};
`;
```

## Best Practices

1. **Use semantic color names** instead of specific colors
2. **Leverage design tokens** for consistent spacing and typography
3. **Test in both light and dark modes** during development
4. **Use the pre-built components** when possible for consistency
5. **Follow the component variant patterns** when creating custom components

## Integration with Existing Components

To integrate with existing SNIP-DIFF components:

1. **Wrap the app** with `ThemeProvider`
2. **Replace hardcoded colors** with theme values
3. **Use styled components** or theme hooks
4. **Apply GlobalThemeStyles** for baseline styling

Example migration:
```tsx
// Before
<div style={{ backgroundColor: '#1a1a2e', color: '#f8fafc' }}>

// After
<div style={{ 
  backgroundColor: theme.colors.background.secondary, 
  color: theme.colors.text.primary 
}}>
```

## Development

Run the theme demo to see all components and colors:
```tsx
import ThemeDemoApp from './theme/demo';

// Render ThemeDemoApp to see the full theme showcase
```

The demo includes examples of all components, color palettes, typography scales, and interactive theme switching.
