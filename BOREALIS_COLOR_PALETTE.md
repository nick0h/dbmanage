# BOREALIS BIOSCIENCES Color Palette

## 🎨 Primary Colors (From Logo)

| Color | Hex Code | Usage |
|-------|----------|-------|
| **Deep Purple** | `#6a0dad` | Primary accent, gradients |
| **Blue** | `#4a90e2` | Primary buttons, links |
| **Teal** | `#00bcd4` | Secondary elements, info |
| **Green** | `#4caf50` | Success states, confirmations |
| **Dark Blue** | `#1e3a8a` | Text, borders, emphasis |

## 🌈 Extended Palette

### Purple Variations
- **Light Purple**: `#8b5cf6` - Hover states, highlights
- **Dark Purple**: `#581c87` - Active states, pressed

### Blue Variations  
- **Light Blue**: `#60a5fa` - Hover states, secondary actions
- **Dark Blue**: `#1d4ed8` - Active states, emphasis

### Teal Variations
- **Light Teal**: `#22d3ee` - Hover states, highlights
- **Dark Teal**: `#0891b2` - Active states, pressed

### Green Variations
- **Light Green**: `#22c55e` - Hover states, highlights  
- **Dark Green**: `#15803d` - Active states, pressed

## 🎭 Neutral Colors

| Shade | Hex Code | Usage |
|-------|----------|-------|
| **50** | `#f8fafc` | Backgrounds, cards |
| **100** | `#f1f5f9` | Secondary backgrounds |
| **200** | `#e2e8f0` | Borders, dividers |
| **300** | `#cbd5e1` | Disabled states |
| **400** | `#94a3b8` | Placeholder text |
| **500** | `#64748b` | Secondary text |
| **600** | `#475569` | Body text |
| **700** | `#334155` | Headings |
| **800** | `#1e293b` | Dark backgrounds |
| **900** | `#0f172a` | Very dark backgrounds |

## 🚦 Semantic Colors

| Purpose | Color | Hex Code |
|---------|-------|----------|
| **Primary** | Blue | `#4a90e2` |
| **Secondary** | Teal | `#00bcd4` |
| **Success** | Green | `#4caf50` |
| **Info** | Teal | `#00bcd4` |
| **Warning** | Amber | `#f59e0b` |
| **Danger** | Red | `#ef4444` |
| **Light** | Gray-100 | `#f1f5f9` |
| **Dark** | Gray-800 | `#1e293b` |

## 🎯 Usage Guidelines

### Buttons
- **Primary Actions**: Use `--borealis-blue`
- **Secondary Actions**: Use `--borealis-teal`  
- **Success Actions**: Use `--borealis-green`
- **Destructive Actions**: Use `--borealis-danger`

### Navigation
- **Active States**: Use `--borealis-blue-dark`
- **Hover States**: Use `--borealis-blue-light`
- **Background**: Use gradient from purple to teal

### Cards & Containers
- **Headers**: Use `--borealis-blue` border
- **Backgrounds**: Use `--borealis-gray-50` to `--borealis-gray-100`
- **Shadows**: Subtle shadows with `--borealis-gray-200`

### Forms
- **Focus States**: Use `--borealis-blue` with 25% opacity shadow
- **Validation**: Use semantic colors (success, warning, danger)
- **Labels**: Use `--borealis-gray-700`

### Tables
- **Headers**: Use gradient from purple to blue
- **Striped Rows**: Use `--borealis-gray-50`
- **Hover States**: Use `--borealis-teal-light`

## 🔧 CSS Variables

All colors are available as CSS custom properties:

```css
:root {
  --borealis-purple: #6a0dad;
  --borealis-blue: #4a90e2;
  --borealis-teal: #00bcd4;
  --borealis-green: #4caf50;
  --borealis-dark-blue: #1e3a8a;
  /* ... and many more */
}
```

## 📱 Responsive Considerations

- **Mobile**: Slightly reduced color intensity for better readability
- **Dark Mode**: Use darker variants for better contrast
- **Accessibility**: Ensure sufficient contrast ratios (WCAG AA compliant)

## 🎨 Design Principles

1. **Consistency**: Use the same color for the same purpose throughout
2. **Hierarchy**: Use color to establish visual hierarchy
3. **Accessibility**: Maintain sufficient contrast for readability
4. **Brand Identity**: Reflect the scientific, professional nature of BOREALIS
5. **Emotional Impact**: Purple for innovation, Blue for trust, Teal for clarity

## 🚀 Implementation

The color palette is implemented in `requests_app/static/css/borealis-theme.css` and automatically applied to all pages through the base template.

### Quick Usage Examples:

```css
/* Use primary brand color */
.my-element {
  color: var(--borealis-blue);
}

/* Use gradient background */
.my-header {
  background: var(--bg-borealis-gradient);
}

/* Use utility classes */
<button class="btn btn-primary">Primary Action</button>
<div class="text-borealis-success">Success Message</div>
```

