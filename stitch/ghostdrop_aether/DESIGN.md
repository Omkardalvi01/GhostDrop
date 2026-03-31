# GhostDrop: Design System Documentation

## 1. Overview & Creative North Star
### The Creative North Star: "Ethereal Precision"
This design system is built to feel like a high-end digital ghost—present, powerful, yet weightless. It moves away from the "boxed-in" nature of traditional SaaS platforms, favoring an editorial approach that treats the screen as a canvas of light and depth. 

We achieve this through **Atmospheric Minimalis**m. Instead of rigid grids and heavy borders, we utilize intentional asymmetry, significant breathing room, and a "weightless" layering logic. The goal is to make the user feel like they are interacting with data that is floating in a structured, atmospheric space. Every element must feel intentional, precise, and premium.

---

## 2. Colors & Surface Logic
The palette is rooted in a deep, atmospheric blue, punctuated by a vibrant, high-energy primary blue.

### The "No-Line" Rule
To maintain a premium, custom feel, **1px solid borders are strictly prohibited for sectioning.** Boundaries must be defined through:
*   **Tonal Transitions:** Moving from `surface` to `surface-container-low`.
*   **Negative Space:** Using the Spacing Scale (e.g., `spacing-16`) to create mental separation without physical lines.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers. Use the `surface-container` tiers to create depth:
1.  **Base Layer:** `surface` (#06092f).
2.  **Sectioning:** `surface-container-low` (#0b0e38) for large secondary areas.
3.  **Interaction Nodes:** `surface-container-high` (#161a4b) for cards or floating panels.
4.  **Floating Elements:** `surface-container-highest` (#1b2055) for active popovers.

### The Glass & Gradient Rule
To move beyond a flat appearance, use **Glassmorphism** for floating elements (e.g., Modals, Tooltips). 
*   **Background:** Apply `primary_container` at 10-20% opacity.
*   **Effect:** `backdrop-filter: blur(20px)`.
*   **Signature Texture:** Use a subtle linear gradient on main CTAs, transitioning from `primary` (#90abff) to `primary_dim` (#2269ff) at a 45-degree angle to give the vibrant blue "soul."

---

## 3. Typography: Editorial Manrope
We use **Manrope** for its technical precision and modern geometry. The hierarchy is designed to feel like a high-end magazine layout.

*   **Display Scales (`display-lg` to `display-sm`):** Reserved for hero moments. These should use tight letter-spacing (-0.02em) and may be placed with intentional asymmetry (e.g., left-aligned with a large right-side gutter) to break the "template" look.
*   **Headline & Title:** Use `headline-md` for section entries. These convey authority and "GhostDrop's" precise nature.
*   **Body & Labels:** `body-md` (0.875rem) is the workhorse. It must remain legible with generous line-height to ensure the "weightless" aesthetic isn't compromised by dense text blocks.

---

## 4. Elevation & Depth
In this design system, height is expressed through light and tone, not shadows.

*   **Tonal Layering Principle:** Depth is achieved by "stacking." A `surface-container-lowest` (#000000) card placed on a `surface` background creates a recessed, "etched" look. Conversely, a `surface-container-highest` card creates a natural lift.
*   **Ambient Shadows:** If a shadow is required for a floating state (like a dropdown), it must be an "Ambient Glow." Use the `on_surface` color at 6% opacity with a blur of `32px` and a `12px` Y-offset.
*   **The "Ghost Border" Fallback:** If an edge is absolutely necessary for accessibility, use the `outline_variant` (#42456c) at **15% opacity**. Never use a 100% opaque border.
*   **Roundedness:** Use `md` (0.375rem) for standard components and `xl` (0.75rem) for main containers to soften the technical precision.

---

## 5. Components

### Buttons
*   **Primary:** A gradient fill using `primary` to `primary_dim`. Text color is `on_primary`. Roundedness is `full` for a "pill" look that feels modern and weightless.
*   **Secondary:** A "Ghost" style. No fill, `outline_variant` at 20% opacity, and `primary` text.
*   **Tertiary:** Purely typographic with a subtle `primary` underline on hover.

### Cards & Containers
*   **Rule:** Forbid divider lines.
*   **Layout:** Use background color shifts (e.g., `surface-container-low` for the card body) and vertical padding (`spacing-6`) to separate content.
*   **Hover State:** Transition the background to `surface_bright` and apply the "Ghost Border" (15% opacity) to create a "magnified" focus effect.

### Input Fields
*   **Visual Style:** Inputs should use `surface_container_lowest` (#000000) to create a sense of depth (the "well" effect). 
*   **States:** On focus, the border doesn't thicken; instead, the background shifts to `surface_container_low` and a `primary` glow is applied via a subtle outer box-shadow.

### Chips & Tags
*   **Selection Chips:** Use `secondary_container` with `on_secondary_container` text. These should feel like small glass pebbles—minimal and smooth.

---

## 6. Do's and Don'ts

### Do
*   **Do use asymmetrical white space.** Allow large areas of the screen to remain empty (the "Atmospheric" requirement).
*   **Do nest containers.** Use the surface tiers to create logical groupings rather than lines.
*   **Do use backdrop blurs.** Make the interface feel like it is sitting on top of the vibrant blue primary energy.

### Don't
*   **Don't use 1px solid borders.** It breaks the "Ghost" aesthetic and makes the UI feel "boxy."
*   **Don't use pure grey shadows.** Always tint shadows with the background or `on_surface` color to maintain tonal harmony.
*   **Don't crowd the typography.** If a section feels heavy, increase the spacing using the `spacing-8` or `spacing-10` tokens.
*   **Don't use "Standard" Grids.** Feel free to offset elements by `spacing-4` to create a more custom, editorial rhythm.