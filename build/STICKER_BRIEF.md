# STICKER BRIEF — Tuk & Tide Surf Club (read fully)

You design **ONE unique die-cut sticker** as a standalone SVG. Many agents each make a
different sticker; yours must be distinct and self-contained.

## Vibe
Vintage surf-shop sticker / heritage screenprint — like Rip Curl, Ron Jon, "Costa Mesa Surf
Club", "Sunshine All The Time", Hawaii badges. Bold, characterful, slightly retro, confident.
Hand-made, not corporate. Charcoal-ink-on-terracotta heritage system.

## Palette (use these exact hexes — no others)
- Charcoal ink `#241D18` · Terracotta `#C24A2C` · Bone/cream `#EFE3D0`
- Deep Clay `#9E3A20` · Surf Teal `#2F5D57`
Most stickers use 2–3 of these. Strong contrast. A sticker usually has ONE bg colour + a
contrasting ink, optionally a thin keyline border and a second accent.

## Fonts (reference by family name; the renderer embeds them)
| family | file | use |
|---|---|---|
| `Ultra` | assets/fonts/Ultra.ttf | fat wood-type — bold display, ring text |
| `Shrikhand` | assets/fonts/Shrikhand.ttf | groovy fat retro display |
| `Pacifico` | assets/fonts/Pacifico.ttf | flowing surf script |
| `Permanent Marker` | assets/fonts/PermanentMarker.ttf | hand-brush accents |
| `DM Sans` (weight 700) | assets/fonts/DMSans.ttf | clean caps labels |

## Reusable marks (optional — embed if your concept wants them)
- Tuk-tuk line-art: `assets/logo/tuktuk_ink.svg` — read it, take the inner `<g>…</g>`,
  replace `#241D18` with your ink colour, wrap in `<g transform="translate(X,Y) scale(S)">…</g>`.
  Art box ≈ 1740×1180 units → scale ≈ 0.10 gives a ~174-wide mark.
- Woodcut wave: `assets/logo/wave_ink.svg` — same method. Art box ≈ 1186×299 → scale ≈ 0.13.

## Curved ring text (WeasyPrint has NO textPath — place glyphs manually)
```
import math
def arc(s, cx, cy, r, center, step, size, font, color):
    out=[]; n=len(s)
    for i,ch in enumerate(s):
        if ch==" ": continue
        a=center+(i-(n-1)/2)*step; rad=math.radians(a)
        x=cx+r*math.cos(rad); y=cy+r*math.sin(rad)
        rot=a+90 if center<0 else a-90
        esc={"&":"&amp;"}.get(ch,ch)
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
          f'font-family="{font}" text-anchor="middle" dominant-baseline="central" '
          f'transform="rotate({rot:.2f} {x:.1f} {y:.1f})">{esc}</text>')
    return "\n".join(out)
# top arc: center=-90, step≈ +14.  bottom arc: center=90, step≈ -14 (reads L→R).
```
Generate the SVG with a small python script (write it, run it) — don't hand-place glyphs.

## HARD RULES
1. Output ONE self-contained `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H">…</svg>`.
   Pick a viewBox to fit the shape (square ~360×360 for circles; ~420×220 for ovals/banners).
2. WeasyPrint-safe SVG: solid fills/strokes, `<text>`, `<path>`, `<circle>`, `<rect rx>`,
   `<ellipse>`, `<g transform>`. NO `<textPath>`, NO filters, NO `currentColor`/`var()` —
   use concrete hexes. Text needs a concrete `fill` and `font-family`.
3. A clear die-cut SHAPE (filled circle / oval / rounded-rect / banner) with optional 1–2px
   keyline border. Bold, legible, balanced. Spelling: "Tuk & Tide Surf Club", "Weligama".

## SELF-VERIFY (required)
Write a python script that builds your SVG, then render + look:
```
# build/_try_<name>.html
<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:'Ultra';src:url('../assets/fonts/Ultra.ttf');}
@font-face{font-family:'Shrikhand';src:url('../assets/fonts/Shrikhand.ttf');}
@font-face{font-family:'Pacifico';src:url('../assets/fonts/Pacifico.ttf');}
@font-face{font-family:'Permanent Marker';src:url('../assets/fonts/PermanentMarker.ttf');}
@font-face{font-family:'DM Sans';src:url('../assets/fonts/DMSans.ttf');font-weight:700;}
body{margin:0;background:#cfcfcf;padding:20px}
svg{width:340px;height:auto}
</style><body> …your <svg>… </body>
```
```
cd ~/Desktop/tuk-and-tide-club
python3 -m weasyprint build/_try_<name>.html build/_try_<name>.pdf
pdftoppm -png -r 150 build/_try_<name>.pdf build/_try_<name>
```
Read the PNG. Fix anything broken/ugly/illegible/off-palette. Iterate until it looks like a
sticker you'd actually want on a board. Delete your `_try_*` files when done.

## Deliverable
Write the FINAL standalone SVG to the EXACT path in your task
(`assets/stickers/NN_name.svg`). Return a one-line summary.
