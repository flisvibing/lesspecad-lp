---
name: ui-ux-pro-max
description: "UI/UX design intelligence for web and mobile. Use for landing pages, dashboards, admin panels, SaaS, e-commerce, portfolios, mobile apps, UI components, visual QA, accessibility review, responsive layout, typography, color systems, animation, forms, navigation, charts, and design-system generation."
---

# UI/UX Pro Max - Design Intelligence

Comprehensive design guide for web and mobile applications. This Codex skill mirrors the UI/UX Pro Max workflow for professional interface planning, implementation, and review.

## When to Apply

Use this skill when a task changes how an interface **looks, feels, moves, or is interacted with**.

### Must Use

- Designing new pages: landing page, dashboard, admin, SaaS, mobile app, e-commerce, portfolio, blog.
- Creating or refactoring UI components: buttons, modals, forms, tables, cards, navigation, charts.
- Choosing or auditing color schemes, typography systems, spacing, layout, icons, shadows, or gradients.
- Reviewing UI code for usability, accessibility, responsiveness, hierarchy, or visual consistency.
- Implementing navigation structures, loading states, empty states, animations, or dark mode.
- Making product-level design decisions: style, information architecture, brand expression.

### Skip

- Pure backend, database, API, infrastructure, DevOps, or non-visual scripting work.
- Performance work that does not affect interface rendering or user interaction.

## Priority Rule Categories

| Priority | Category | Impact | Key Checks | Avoid |
| --- | --- | --- | --- | --- |
| 1 | Accessibility | Critical | 4.5:1 contrast, visible focus, labels, alt text, keyboard nav | Removing focus rings, icon-only buttons without labels |
| 2 | Touch & Interaction | Critical | 44x44px targets, 8px spacing, loading/error feedback | Hover-only behavior, instant state changes |
| 3 | Performance | High | WebP/AVIF, lazy loading, reserved media dimensions, route splitting | CLS, layout thrashing, blocking scripts |
| 4 | Style Selection | High | Match product category, consistent icon/elevation language | Mixing unrelated styles, emoji as icons |
| 5 | Layout & Responsive | High | Mobile-first, viewport meta, no horizontal scroll, safe areas | Fixed-width layouts, disabled zoom |
| 6 | Typography & Color | Medium | 16px body baseline, semantic tokens, clear type scale | Tiny body text, gray-on-gray, raw hex sprawl |
| 7 | Animation | Medium | 150-300ms, transform/opacity, reduced motion support | Decorative motion, animating width/height |
| 8 | Forms & Feedback | Medium | Visible labels, inline errors, helper text, submit states | Placeholder-only labels, top-only errors |
| 9 | Navigation | High | Predictable back, active state, breadcrumbs/deep links | Overloaded nav, hidden escape routes |
| 10 | Charts & Data | Low | Legends, labels, tooltips, accessible colors, table alternative | Color-only meaning, overusing pie charts |

## Required Workflow

### Step 1: Analyze Requirements

Extract:

- Product type and industry.
- Target audience and usage context.
- Primary user goal and conversion action.
- Platform/stack.
- Style keywords, brand tone, and accessibility constraints.

### Step 2: Generate a Design System

Always start UI build work with a compact design-system recommendation:

```bash
python3 .codex/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard analytics" --design-system -p "Project Name"
```

For reusable project guidance, persist it:

```bash
python3 .codex/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard analytics" --design-system --persist -p "Project Name"
```

This creates `design-system/<project-slug>/MASTER.md`. For page-specific overrides:

```bash
python3 .codex/skills/ui-ux-pro-max/scripts/search.py "checkout ecommerce" --design-system --persist -p "Project Name" --page "checkout"
```

When building a page, read `design-system/<project-slug>/MASTER.md` first and then check `design-system/<project-slug>/pages/<page>.md`; page rules override the master only where they differ.

### Step 3: Supplement with Domain Searches

Use targeted searches when details are needed:

```bash
python3 .codex/skills/ui-ux-pro-max/scripts/search.py "glassmorphism SaaS" --domain style
python3 .codex/skills/ui-ux-pro-max/scripts/search.py "fintech banking" --domain color
python3 .codex/skills/ui-ux-pro-max/scripts/search.py "dashboard comparison" --domain chart
python3 .codex/skills/ui-ux-pro-max/scripts/search.py "form validation accessibility" --domain ux
python3 .codex/skills/ui-ux-pro-max/scripts/search.py "React list performance" --stack react
```

## Implementation Guardrails

- Prefer semantic design tokens over scattered raw values.
- Use one icon family and one elevation/radius scale per product.
- Ensure interactive elements have visible default, hover, focus, active, disabled, loading, success, and error states.
- Mobile-first layouts must not horizontally scroll at common widths: 320, 375, 390, 768, 1024, 1440.
- Use accessible color pairs and do not rely on color alone for state or chart meaning.
- Respect `prefers-reduced-motion`; keep UI transitions purposeful and interruptible.
- Use skeletons or reserved layout space for async content to avoid cumulative layout shift.
- Keep one primary CTA per screen and make secondary/destructive actions visually subordinate.

## Pre-delivery UI Checklist

Before finalizing UI work, verify:

- [ ] Contrast, focus, labels, alt text, and keyboard navigation are covered.
- [ ] Touch targets and spacing are comfortable on mobile.
- [ ] Layout works at mobile, tablet, and desktop widths without overflow.
- [ ] Typography has a clear scale and readable line lengths.
- [ ] Loading, empty, error, disabled, and success states are present where applicable.
- [ ] Motion uses transform/opacity and honors reduced-motion settings.
- [ ] Charts include labels, legends/tooltips, and non-color affordances.
- [ ] Visual direction matches product category and does not look generic.
