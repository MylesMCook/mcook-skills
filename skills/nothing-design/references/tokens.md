# Nothing Design System — Tokens

Use these values when you need exact implementation details. If the user's existing
codebase already has a token system, map these semantics onto it instead of inventing a
parallel design system.

## 1. Typography

### Font stack

| Role | Preferred font | Fallback | Notes |
|---|---|---|---|
| Display | `Geist Pixel` | `Geist Mono`, monospace | Hero numbers, clocks, and signal moments only |
| Body / UI | `Geist Sans` | `Inter`, `system-ui`, sans-serif | Primary reading and layout text |
| Data / labels | `Geist Mono` | `JetBrains Mono`, `SFMono-Regular`, monospace | Labels, metrics, units, controls |

### Type scale

| Token | Size | Line height | Letter spacing | Use |
|---|---:|---:|---:|---|
| `--display-xl` | 72px | 1.0 | -0.03em | Hero number / time |
| `--display-lg` | 48px | 1.05 | -0.02em | Section hero / key percentage |
| `--display-md` | 36px | 1.1 | -0.02em | Page title / compact hero |
| `--heading` | 24px | 1.2 | -0.01em | Section heading |
| `--subheading` | 18px | 1.3 | 0 | Secondary heading |
| `--body` | 16px | 1.5 | 0 | Standard body text |
| `--body-sm` | 14px | 1.5 | 0.01em | Secondary copy |
| `--caption` | 12px | 1.4 | 0.04em | Footnotes / timestamps |
| `--label` | 11px | 1.2 | 0.08em | ALL CAPS labels |

### Typographic rules

- Use **Geist Pixel** only at 36px or above, usually for one hero number, clock, or
  status readout per screen.
- The default working pair is **Geist Sans** + **Geist Mono**. Most interface text
  should stay in that pair even when the layout is visually expressive.
- Labels are usually **Geist Mono** at `--label` or `--caption`; use ALL CAPS only
  when the extra rigidity helps clarity.
- Data-heavy values are usually **Geist Mono** even when surrounding copy is Geist Sans.
- Buttons, inputs, nav, cards, and long-form body copy should normally use **Geist Sans**.
- **Geist Pixel** should never carry dense UI, repeated card headings, or body copy.
- Units should sit adjacent to values and read smaller than the value itself.
- Four hierarchy levels are enough for most screens: display, heading, body, label.

## 2. Color system

### Dark mode

| Token | Value | Role |
|---|---|---|
| `--black` | `#000000` | Primary background |
| `--surface` | `#111111` | Elevated surfaces |
| `--surface-raised` | `#1A1A1A` | Secondary elevation |
| `--border` | `#222222` | Subtle separators |
| `--border-visible` | `#333333` | Intentional outlines |
| `--text-disabled` | `#666666` | Disabled / hints |
| `--text-secondary` | `#999999` | Labels / metadata |
| `--text-primary` | `#E8E8E8` | Main text |
| `--text-display` | `#FFFFFF` | Hero contrast |
| `--accent` | `#D71921` | Urgent / destructive / signal |
| `--accent-subtle` | `rgba(215, 25, 33, 0.15)` | Accent tint |
| `--success` | `#4A9E5C` | Good / connected / complete |
| `--warning` | `#D4A843` | Caution / pending |
| `--interactive` | `#5B9BF6` | Links and tappable text |

### Light mode

| Token | Value |
|---|---|
| `--black` | `#F5F5F5` |
| `--surface` | `#FFFFFF` |
| `--surface-raised` | `#F0F0F0` |
| `--border` | `#E8E8E8` |
| `--border-visible` | `#CCCCCC` |
| `--text-disabled` | `#999999` |
| `--text-secondary` | `#666666` |
| `--text-primary` | `#1A1A1A` |
| `--text-display` | `#000000` |
| `--interactive` | `#007AFF` |

### Color usage rules

- Build hierarchy with grayscale first.
- Red is a **signal**. Use it sparingly and intentionally.
- For status-heavy tables and widgets, apply status color to the **value** or marker,
  not the label or row background.
- If multiple datasets must be distinguished, prefer opacity, dash, dot, or stripe
  patterns before introducing extra colors.

## 3. Spacing, layout, and shape

### Spacing scale

| Token | Value | Typical use |
|---|---:|---|
| `--space-2xs` | 2px | Optical correction only |
| `--space-xs` | 4px | Tight icon/unit gaps |
| `--space-sm` | 8px | Internal component spacing |
| `--space-md` | 16px | Standard gaps / padding |
| `--space-lg` | 24px | Group separation |
| `--space-xl` | 32px | Section spacing |
| `--space-2xl` | 48px | Major section break |
| `--space-3xl` | 64px | Page rhythm |
| `--space-4xl` | 96px | Hero breathing room |

### Shape and grid

- Card radius: **12-16px**
- Compact component radius: **8px**
- Technical radius: **4px**
- Pill radius: **999px**
- Border width: **1px** standard, **2px** signal indicator
- Minimum hit target: **44x44px**
- Prefer asymmetrical layouts, edge anchoring, and visible negative space over centered grids.

## 4. Motion and interaction

- Micro-interactions: **150-250ms**
- Larger transitions: **300-400ms**
- Easing: `cubic-bezier(0.25, 0.1, 0.25, 1)`
- Prefer opacity or subtle border/text changes over large movement.
- No spring, bounce, parallax, or ornamental motion.
- Focus states must be visible in both dark and light mode.

## 5. Iconography

- Monoline, about **1.5px stroke**
- No fills, no multicolor icon packs
- 24x24 canvas with a 20x20 live area works well
- Icons inherit surrounding text color
- Prefer simple technical icon families (for example, thin Lucide-like shapes)

## 6. Dot-matrix motif

Use the dot matrix motif for hero typography, decorative grids, compact indicators, and
loading states — not as a blanket texture on every component.

```css
.dot-grid {
  background-image: radial-gradient(circle, var(--border-visible) 1px, transparent 1px);
  background-size: 16px 16px;
}

.dot-grid-subtle {
  background-image: radial-gradient(circle, var(--border) 0.5px, transparent 0.5px);
  background-size: 12px 12px;
}
```

Guidelines:
- Dot size: **1-2px**
- Grid: **12-16px**
- Background opacity: **0.1-0.2**
- Use it as a moment, not a wallpaper
