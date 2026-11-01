# NexAbility frontend design and accessibility

Permanent instructions for work inside `frontend/`. Do not modify `backend/`. Do not create a second React project. Reuse this Vite + React app.

## Brand sources

- Website layout language: NexAbility Inclusive Hiring UI Showcase (landing, login, registration, candidate dashboard, employer dashboard).
- Colour system: official blue palette derived from the flowing-ribbon logo, not the purple Stitch preview.
- Logo file: `/assets/nexability-logo.png` (served from `frontend/public/assets/nexability-logo.png`). Use that path for every brand mark.

## Official colours

Use CSS variables from `src/styles/tokens.css`. Do not introduce one-off HEX values in components.

| Token | HEX | Use |
|---|---|---|
| `--color-primary` | `#082048` | Navy wordmark / primary actions / headings |
| `--color-primary-hover` | `#083068` | Primary hover |
| `--color-secondary` | `#0068B0` | Links and secondary UI text on light surfaces (WCAG AA) |
| `--color-accent` | `#00B0F0` | Logo cyan highlights, decorative accent |
| `--color-accent-strong` | `#0088F0` | Stronger cyan |
| `--color-background` | `#F4F8FC` | Page canvas |
| `--color-surface` | `#FFFFFF` | Cards, forms, header, dashboards |
| `--color-text` | `#082048` | Body headings and primary copy |
| `--color-text-muted` | `#2F4563` | Supporting copy |
| `--color-border` | `#C5D7E8` | Dividers and card edges |
| `--color-focus` | `#082048` | Focus ring on light surfaces |
| `--color-focus-inverse` | `#00B0F0` | Focus ring on navy surfaces |

Do not use white text on `--color-accent` (`#00B0F0` fails WCAG AA on white and as white-on-cyan). Accent fills must use `--color-text-on-accent` (`#082048`). Cyan is not a body-text colour on white.

Inverse/navy panels (hero, dark auth rail, dark footer) use `--color-surface-inverse` with `--color-text-inverse`.

## Typography, space, controls

- Font: Inter, then Segoe UI, Arial, sans-serif.
- Body: 1rem / 1.6. Headings use `--font-size-h1`–`--font-size-h3` and tight tracking.
- Spacing scale: `--space-1` (4px) through `--space-8` (64px). Content width: `--layout-max`.
- Radius: `--radius-md` for inputs, `--radius-lg` for cards, `--radius-pill` for buttons.
- Shadows: `--shadow-sm` / `--shadow-md` / `--shadow-lg` (navy-tinted).
- Buttons: `.btn-primary`, `.btn-secondary`, `.btn-accent`. Minimum hit area `--control-min-size` (48px).
- Breakpoints: 1024px, 760px, 480px. Stack marketing grids and dashboard sidebars on small screens.

These rules apply equally to landing, login, registration, candidate dashboard, and employer dashboard.

## Accessibility (required)

Target WCAG 2.2 Level AA for keyboard-only, screen-reader, low-vision, motor, and cognitive use.

- Every action must be possible with the keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`, arrow keys where a pattern needs them).
- Visible `:focus-visible` rings are mandatory. Never remove them.
- Provide a skip link to main content on every page shell.
- Use landmarks (`header`, `nav`, `main`, `footer`), labelled headings, and `aria-*` only when native HTML is not enough.
- Images that convey meaning need `alt`. Decorative images use `alt=""` or `aria-hidden="true"`.
- Form controls need visible labels tied with `for`/`id`. Errors must be announced (text, not colour alone).
- Honour `prefers-reduced-motion`. Do not make motion the only way to understand content.
- Contrast: navy text on white, white text on navy. Check new combinations before shipping.

## Implementation rules

- Keep API calls, tokens, and env usage out of presentational CSS. Use `VITE_API_BASE_URL` when wiring APIs later.
- Centralize styles in `src/styles/tokens.css` and `src/styles/base.css`. Page CSS may compose variables; it must not fork a second palette.
- Preserve existing Vite/React configuration unless a change is required for accessibility or the design tokens.
- Do not add UI libraries unless the team explicitly agrees. Prefer semantic HTML and these tokens.
