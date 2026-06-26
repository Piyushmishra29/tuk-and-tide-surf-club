# Tuk & Tide Club — Brand Book Design Spec

**Date:** 2026-06-26
**Client:** Tuk & Tide Club (owner: Piyush's new business)
**Location:** Weligama, Sri Lanka
**Deliverable:** ONE cohesive multi-page PDF brand book (HTML → WeasyPrint → PDF)
**Build method:** Fleet of parallel agents + subagents against a shared design system

---

## 1. The Business

Surf lessons + surfboard rentals, and tuk-tuk tours + tuk-tuk rentals — all under one
warm, fun, local club in Weligama. Bookings are WhatsApp-first (consistent with sibling
projects Alpha Ocean Hub, Aurora Midigama).

## 2. Positioning & Voice

- **One-liner:** *Surf, ride, repeat. Weligama's tuk-tuk & surf club.*
- **Personality:** Laid-back local soul with a "let's-go" grin. Salty, friendly, a little
  cheeky. Never corporate.
- **Voice samples:** "Grab a board, grab a tuk, we'll sort the rest." /
  "No stress — just sand, surf and three wheels."
- **Locator line:** Weligama, Sri Lanka.

## 3. Logo System (combo)

- **Wordmark:** "Tuk & Tide Club" in chunky retro-surf lettering — rounded, warm, 70s
  poster weight, with a wave-curl / rising-sun detail in the type.
- **Badge emblem (standalone):** circular club stamp — a tuk-tuk riding a wave, ringed by
  `TUK & TIDE CLUB · WELIGAMA · SRI LANKA`. The sticker / decal / rashguard mark.
- **Lockups:** full horizontal, stacked, badge-only, one-color (stamp/embroidery).
- **Format:** built as inline SVG (WeasyPrint rasterizes natively); exported PNG for the pack.

## 4. Color Palette (Sun-faded × Retro surf)

| Role | Name | Hex |
|---|---|---|
| Primary | Tuk-Tuk Terracotta | `#C8502A` |
| Secondary | Golden Mustard | `#E0A434` |
| Accent | Ocean Teal | `#2E7D74` |
| Background | Sand Cream | `#F4EAD5` |
| Text | Deep Cacao | `#2E211A` |

## 5. Typography

- **Display / wordmark:** Fredoka (bold) or Righteous — 70s retro-rounded warmth.
- **Headings:** Bricolage Grotesque.
- **Body:** DM Sans.
- All fonts downloaded as TTF and embedded via `@font-face` for WeasyPrint.

## 6. The PDF — Page Plan (single document, A4 portrait)

1. **Cover** — badge + wordmark on Sand Cream, terracotta wave, locator line.
2. **The Club / Story** — who we are, the one-liner, the vibe.
3. **Logo System** — wordmark, badge, all lockups, clear-space, min-size.
4. **Logo Don'ts** — misuse examples.
5. **Color Palette** — swatches, hex/RGB/CMYK, proportions.
6. **Typography** — type scale, pairings, sample settings.
7. **Voice & Tone** — do/don't, sample copy lines.
8. **Mockups** — tuk-tuk livery, sticker sheet, tee, surfboard, signage.
9. **Contact / Back cover** — WhatsApp, IG handle, badge sign-off.

> The "asset pack" (SVG/PNG logo files) and "digital style guide" requirements are folded
> in: the SVG sources produced for the PDF double as the asset pack; the digital style
> guide is deferred to the website phase (it shares this palette/type).

## 7. Build Architecture (multi-agent)

**Phase 0 — Foundation (main agent, sequential, shared by all):**
- Download + embed fonts (Fredoka, Bricolage Grotesque, DM Sans).
- Write `assets/brand.css` — CSS variables (colors, type, spacing), `@page` rules, A4.
- Build the **logo + badge SVG** (everything depends on this) — done first.

**Phase 1 — Section builders (parallel agents, one HTML partial each):**
Each agent builds ONE self-contained page partial against `brand.css`, no shared mutable
state, returning an HTML fragment:
- Agent A: Cover + Back cover
- Agent B: Story + Voice & Tone
- Agent C: Color + Typography pages
- Agent D: Logo System + Logo Don'ts
- Agent E: Mockups (SVG-illustrated)

**Phase 2 — Assembly (main agent):**
- Concatenate partials in page order into `book.html`, render with WeasyPrint to
  `build/tuk-and-tide-club-brand-book.pdf`.

**Phase 3 — Review (review agent — REQUIRED after every PDF generation):**
- Render PDF pages to images, inspect for overflow, broken fonts, color fidelity,
  WeasyPrint-dropped CSS, consistency. File issues → fix → re-render until clean.

## 8. Constraints / Gotchas

- WeasyPrint silently drops: `inset:`, `display:contents`, `mix-blend-mode`,
  `text-shadow`, filter `drop-shadow`. Avoid these; use supported equivalents.
- Fonts MUST be embedded via `@font-face` with local TTF paths (no network at render time).
- Keep each page partial isolated so parallel agents never edit the same file.

## 9. Success Criteria

- One PDF, all 9 sections, fonts render correctly, colors match the palette, no overflow,
  logo + badge crisp, review agent passes clean.
- SVG logo sources saved in `assets/logo/` as a reusable asset pack.

## 10. Out of Scope (separate later spec)

- The website (built on this identity).
- Standalone digital style-guide webpage.
