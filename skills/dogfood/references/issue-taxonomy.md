# Issue Taxonomy

Read this at the start of a dogfood run so severity and coverage stay consistent.

## Severity

| Severity | Use when |
| --- | --- |
| `critical` | A core workflow is blocked, data is lost, or the app crashes |
| `high` | A major feature is broken or badly degraded without a real workaround |
| `medium` | The task still works, but the UX, reliability, or correctness is notably off |
| `low` | Minor but real defect, polish issue, or inconsistency |

## Issue Families

### Visual and UI

- broken layout, overlap, clipping, or stacking
- inconsistent spacing, sizing, or alignment
- missing icons, images, or broken media
- theme or responsive rendering problems
- contrast or readability problems
- animation glitches or obvious jank

### Functional

- broken links or wrong destinations
- controls that do nothing
- invalid validation behavior
- silent failures after submit or save
- state that disappears unexpectedly
- broken search, filtering, sorting, pagination, upload, or download flows

### UX

- confusing navigation
- unclear or missing feedback
- dead ends
- weak loading, empty, or error states
- destructive actions without confirmation
- missing keyboard or focus handling where it matters

### Content

- typos or broken copy
- placeholder text left in production UI
- incorrect labels or terminology
- truncated text without a usable fallback

### Performance and Runtime

- slow page loads or interactions
- noticeable layout shifts
- noisy or repeated network failures
- JavaScript exceptions, promise rejections, or console-visible failures

### Accessibility

- unlabeled inputs
- missing alt text
- broken tab order or trapped focus
- poor contrast
- dynamic UI without usable semantics

## Exploration Checklist

Use this as a route-by-route checklist:

1. Scan the page visually.
2. Click the main controls and calls to action.
3. Exercise forms with valid, invalid, and empty input when relevant.
4. Follow major navigation paths and deep links.
5. Check loading, empty, error, and success states.
6. Review `console` and `errors`.
7. Check responsive layout if the app claims mobile support or the user cares about it.
8. Note auth walls, role boundaries, and blocked areas honestly.
