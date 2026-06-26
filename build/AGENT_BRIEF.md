# SHARED BRIEF — Tuk & Tide Club Brand Book (read fully before building)

You are building **ONE page partial** of a single PDF brand book. Many agents work in
parallel; stay strictly inside your assigned file so nothing collides.

## Brand snapshot
- **Name:** Tuk & Tide Club · **Locator:** Weligama, Sri Lanka
- **Business:** surf lessons + board rentals, and tuk-tuk tours + tuk-tuk rentals.
- **One-liner:** "Surf, ride, repeat. Weligama's tuk-tuk & surf club."
- **Personality:** laid-back local soul with a "let's-go" grin. Salty, friendly, a touch
  cheeky. Never corporate. Voice samples: "Grab a board, grab a tuk, we'll sort the rest." /
  "No stress — just sand, surf and three wheels."
- **Aesthetic:** 70s retro surf poster × sun-faded Sri Lankan tuk-tuk warmth.

## Colors (use the CSS variables, never hardcode unless inside an SVG)
| token | name | hex |
|---|---|---|
| `--terracotta` | Tuk-Tuk Terracotta (primary) | #C8502A |
| `--mustard` | Golden Mustard | #E0A434 |
| `--teal` | Ocean Teal | #2E7D74 |
| `--cream` | Sand Cream (bg) | #F4EAD5 |
| `--cacao` | Deep Cacao (text) | #2E211A |
| `--cream-deep` | panel | #EADBBE |
| `--terracotta-deep` | #A63E1E · `--teal-deep` #215A53 |

## Type
- Display/headlines: **Fredoka** (`var(--display)`), retro rounded.
- Subheads: **Bricolage** (`var(--head)`).
- Body: **DM Sans** (`var(--body)`).

## HARD RULES
1. Output is an HTML **fragment only** — one or more `<div class="page">…</div>` blocks.
   NO `<html>`, `<head>`, `<body>`, or `<style>` linking. Inline `<style scoped>` is allowed
   ONLY for page-specific layout, but prefer the shared classes in `assets/brand.css`.
2. The book is assembled at `build/book.html`, so all asset paths are relative to `build/`:
   - badge image: `../assets/logo/badge.svg`
   - (brand.css and fonts are already linked by the assembler — do not re-link them)
3. **WeasyPrint-safe CSS ONLY.** Do NOT use: `inset:`, `display:contents`,
   `mix-blend-mode`, `text-shadow`, `filter: drop-shadow`, CSS grid `gap` is fine,
   flexbox is fine. Use `position:absolute` with explicit top/left/right/bottom (NOT `inset`).
4. Page size is A4 (210mm × 297mm), enforced by `.page`. Keep all content inside the
   padding; NOTHING may overflow. Use `.page.bleed` (zero padding) for full-bleed pages.
5. Use the shared helpers: `.kicker`, `h1.sec`, `h2.sub`, `p`, `.lead`, `.small`,
   `.divider`, `.chip`, `.panel`, `.pgmark`, `.wordmark` (see brand.css).

## Shared wordmark (render EXACTLY this where a wordmark is needed)
```html
<div class="wordmark">
  <div class="wm-main">Tuk <span class="amp">&amp;</span> Tide Club</div>
  <div class="wm-rule"></div>
  <div class="wm-sub">Weligama · Sri Lanka</div>
</div>
```

## Page footer mark (put on interior pages, not full-bleed covers)
```html
<div class="pgmark"><span>Tuk &amp; Tide Club</span><span>Brand Book · Weligama</span></div>
```

## SELF-VERIFY before you finish (REQUIRED)
Create a throwaway tester in `build/` so paths match, render it, and LOOK at it:
```
# build/_try_<yourfile>.html  (links the real CSS, includes your partial inline)
<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/brand.css"></head><body>
 …your <div class="page"> content here… </body></html>
```
Then:
```
cd ~/Desktop/tuk-and-tide-club
python3 -m weasyprint build/_try_<yourfile>.html build/_try_<yourfile>.pdf
pdftoppm -png -r 150 build/_try_<yourfile>.pdf build/_try_<yourfile>
```
Read the PNG. Fix overflow, broken fonts, wrong colors, ugly spacing. Iterate until it
looks polished and premium. Delete your `_try_*` files when done. Leave ONLY your partial.

## Your deliverable
Write your final partial to the EXACT path given in your task. Return a one-line summary.
