# SHARED BRIEF — Tuk & Tide Surf Club · Brand Kit (read fully before building)

You build **ONE page partial** of a single PDF brand book. Many agents work in
parallel; stay strictly inside your assigned file.

## The brand
- **Name:** Tuk & Tide Surf Club · **Locator:** Weligama, Sri Lanka (south coast)
- **Business:** surf lessons + board rentals, and tuk-tuk tours + tuk-tuk rentals.
- **One-liner:** "Surf, ride, repeat." · alt: "Weligama's tuk-tuk & surf club."
- **Aesthetic:** VINTAGE WOODCUT / SCREENPRINT heritage surf club. Hand-carved,
  sun-faded, analog. Charcoal ink on terracotta. NOT clean/corporate, NOT glossy.
- **Personality / voice:** laid-back local with a let's-go grin. Salty, friendly,
  a touch cheeky. Never corporate.
  - Voice samples: "Grab a board, grab a tuk, we'll sort the rest." /
    "No stress — just sand, surf and three wheels." / "Two waves. Three wheels. One club."
- **Services:** Surf Lessons · Board Rentals · Tuk-Tuk Tours · Tuk-Tuk Rentals
- **Mood words:** sun-faded · hand-carved · salty · analog · heritage · three-wheeled · south-coast

## Colour (use the CSS variables)
| token | name | hex |
|---|---|---|
| `--ink` | Charcoal (primary ink) | #241D18 |
| `--terra` | Terracotta (primary bg) | #C24A2C |
| `--bone` | Bone / Sand (light bg) | #EFE3D0 |
| `--clay` | Deep Clay (accent) | #9E3A20 |
| `--teal` | Surf Teal (sparing accent) | #2F5D57 |

## Type
- Display / headlines: **Ultra** (`var(--display)`) — fat retro wood-type.
- Hand-brush accents: **Marker** (`var(--marker)`, Permanent Marker).
- Body / labels: **DM Sans** (`var(--body)`).

## HARD RULES
1. Output is an HTML **fragment only** — one or more `<div class="page">…</div>` blocks.
   NO `<html>/<head>/<body>`, no linking css/fonts (the assembler does that).
   Inline `<style scoped>` is allowed for page-specific layout, but prefer the shared
   classes in `assets/brand.css`.
2. Asset paths are relative to `build/` (where book.html lives):
   - `../assets/brand/logo-terracotta.png`  full lockup on terracotta (clean)
   - `../assets/brand/logo-terracotta-worn.png`  full lockup, worn screenprint
   - `../assets/brand/logo-reversed.png`  full lockup on charcoal (bone ink)
   - `../assets/brand/mark-tuktuk-C24A2C.png` · `mark-tuktuk-EFE3D0.png`  tuk-tuk mark
   - `../assets/brand/mark-wave-C24A2C.png` · `mark-wave-EFE3D0.png`  wave mark
3. **WeasyPrint-safe CSS ONLY.** NO `inset:`, `display:contents`, `mix-blend-mode`,
   `text-shadow`, `filter:drop-shadow`. Use `position:absolute` with explicit
   top/left/right/bottom. flexbox + grid OK. Equal-width borders only on rounded
   boxes (single-side thick border + border-radius mis-renders).
4. A4 (210×297mm). NOTHING overflows. Use `.page` (terracotta), `.page.bone`
   (light), or `.page.ink` (charcoal) per your page. Use `.page.bleed` for full-bleed.
5. Shared helpers: `.kicker`, `h1.disp`, `h2.sub`, `.marker`, `p`, `.lead`, `.small`,
   `.rule`, `.chip`, `.panel`, `.panel.solid`, `.pgmark`.

## Page footer mark (interior pages, not full-bleed covers)
```html
<div class="pgmark"><span>Tuk &amp; Tide Surf Club</span><span>Brand Kit · Weligama</span></div>
```

## SELF-VERIFY before finishing (REQUIRED)
Make a throwaway tester in `build/` (paths match), render, and LOOK:
```
# build/_try_<file>.html
<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/brand.css"></head><body>
 …your <div class="page"> here… </body></html>
```
```
cd ~/Desktop/tuk-and-tide-club
python3 -m weasyprint build/_try_<file>.html build/_try_<file>.pdf
pdftoppm -png -r 150 build/_try_<file>.pdf build/_try_<file>
```
Read the PNG. Fix overflow, broken fonts, wrong colours, ugly spacing. Iterate until
it looks premium and on-brand (heritage, hand-made, confident). Delete `_try_*` when done.

## Deliverable
Write your FINAL partial to the EXACT path in your task. Return a one-line summary.
