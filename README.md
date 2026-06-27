# Tuk & Tide Surf Club — Brand System

A complete heritage brand identity for **Tuk & Tide Surf Club** — a tuk-tuk + surf
rental / lessons / tours business in **Weligama, Sri Lanka**.

Vintage woodcut / screenprint aesthetic · charcoal ink on terracotta.

![Logo](build/logo-preview-worn.png)

## What's inside

| Deliverable | File |
|---|---|
| **Brand Book (13pp PDF)** | `build/tuk-and-tide-surf-club-brand-kit.pdf` |
| **Sticker Pack (20 designs)** | `build/sticker-sheet.pdf` |
| **Logo** (clean + worn + reversed + marks) | `assets/brand/` |
| **Stickers** (SVG + die-cut PNG) | `assets/stickers/` |

### Brand book pages
Cover · The Club · Moodboard · Manifesto interstitial · Logo System · Logo Don'ts ·
Colour · Typography · Voice & Tone · Motifs & Icons · In the Wild (mockups) ·
Next Steps · Back cover.

## The system
- **Palette** — Charcoal `#241D18` · Terracotta `#C24A2C` · Bone `#EFE3D0` · Deep Clay `#9E3A20` · Surf Teal `#2F5D57`
- **Type** — Ultra (wood-type display) · Permanent Marker / Shrikhand / Pacifico (accents) · DM Sans (body)
- **Marks** — a vectorised auto-rickshaw line-art + a bold woodcut wave, riding a flush-width wordmark.

## How it's built
Everything is generated from source — no design app:
- Logo & motifs: Python → SVG, rendered with **WeasyPrint**; the tuk-tuk & wave are
  **potrace**-traced from reference line-art and recoloured.
- Pages: HTML partials + `assets/brand.css` → WeasyPrint → PDF.
- Stickers: per-sticker SVG → WeasyPrint → die-cut treatment (kiss-cut border, grain,
  drop shadow) via **ImageMagick**.
- Photography: the club's own auto-rickshaw, lightly graded.

### Rebuild
```bash
python3 assets/logo/generate_logo.py        # logo
zsh build/render_logo.sh                     # logo previews
python3 build/gen_motifs.py                  # icon page
python3 build/assemble.py                    # stitch partials -> book.html
python3 -m weasyprint build/book.html build/tuk-and-tide-surf-club-brand-kit.pdf
python3 build/process_stickers.py            # die-cut stickers
python3 build/make_sticker_sheet.py && python3 -m weasyprint build/sticker_sheet.html build/sticker-sheet.pdf
```

---
*Weligama · Sri Lanka · Surf, ride, repeat.*
