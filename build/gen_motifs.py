#!/usr/bin/env python3
"""Generate 09_motifs.html — woodcut surf icon library + framed block panels.
Icons are bold charcoal SVG (fill=currentColor so tiles can recolor)."""
import os, math

# ---- icon library (viewBox 0 0 64 64, fill currentColor) ----
def _sun_rays(cx, cy, r0, r1, n, w):
    out=[]
    for k in range(n):
        a=2*math.pi*k/n
        bx,by=cx+math.cos(a)*r0, cy+math.sin(a)*r0
        tx,ty=cx+math.cos(a)*r1, cy+math.sin(a)*r1
        ux,uy=math.cos(a+math.pi/2), math.sin(a+math.pi/2)
        out.append(f'<path d="M {bx+ux*w:.1f} {by+uy*w:.1f} L {tx:.1f} {ty:.1f} '
                   f'L {bx-ux*w:.1f} {by-uy*w:.1f} Z"/>')
    return "".join(out)

ICONS = {
 "sunburst": f'<circle cx="32" cy="32" r="12"/>{_sun_rays(32,32,15,29,12,3)}',
 "sunrise":  '<path d="M6 40 a26 26 0 0 1 52 0 Z"/>'
             '<rect x="4" y="44" width="56" height="4" rx="2"/>'
             + _sun_rays(32,40,0,0,0,0),
 "wave":     '<path d="M4 42 q8 -15 16 0 q8 -15 16 0 q8 -15 16 0 l0 8 l-48 0 Z"/>',
 "curl":     '<path d="M8 46 C 8 22 30 12 46 20 C 36 16 26 24 28 34 '
             'C 30 42 40 42 44 36 C 42 46 30 50 22 46 C 34 50 46 44 46 34 '
             'L 56 40 C 54 52 36 58 22 54 C 14 52 8 50 8 46 Z"/>',
 "fin":      '<path d="M14 50 C 14 28 26 12 46 10 C 40 24 40 40 50 50 Z"/>',
 "board":    '<path d="M32 4 C 44 16 44 48 32 60 C 20 48 20 16 32 4 Z"/>'
             '<rect x="30.5" y="14" width="3" height="36" rx="1.5" fill="#EFE3D0"/>',
 "palm":     '<path d="M29 58 C 29 44 30 36 32 29 l4 1 C 34 37 33 46 35 58 Z"/>'
             '<path d="M32 29 C 19 21 9 22 3 29 C 12 17 26 21 32 29 Z"/>'
             '<path d="M32 29 C 45 21 55 22 61 29 C 52 17 38 21 32 29 Z"/>'
             '<path d="M32 29 C 23 17 15 11 8 10 C 22 10 30 19 32 29 Z"/>'
             '<path d="M32 29 C 41 17 49 11 56 10 C 42 10 34 19 32 29 Z"/>'
             '<path d="M32 29 C 30 16 30 9 32 3 C 36 11 35 21 32 29 Z"/>'
             '<circle cx="32" cy="29" r="4"/>',
 "hibiscus": ''.join(f'<ellipse cx="{32+math.cos(2*math.pi*k/5-1.57)*13:.1f}" '
             f'cy="{32+math.sin(2*math.pi*k/5-1.57)*13:.1f}" rx="9" ry="12" '
             f'transform="rotate({k*72} {32+math.cos(2*math.pi*k/5-1.57)*13:.1f} '
             f'{32+math.sin(2*math.pi*k/5-1.57)*13:.1f})"/>' for k in range(5))
             + '<circle cx="32" cy="32" r="5"/>',
 "gull":     '<path d="M4 38 Q 18 24 31 36 Q 44 24 58 38 Q 44 30 31 39 Q 18 30 4 38 Z"/>',
 "umbrella": '<path d="M6 32 a26 26 0 0 1 52 0 Z"/>'
             '<rect x="30" y="32" width="4" height="26" rx="2"/>'
             '<path d="M34 56 a6 6 0 0 0 10 0" stroke="currentColor" stroke-width="3" fill="none"/>',
 "fish":     '<path d="M6 32 C 18 18 40 18 50 32 C 40 46 18 46 6 32 Z"/>'
             '<path d="M50 32 L 60 22 L 58 32 L 60 42 Z"/>'
             '<circle cx="18" cy="30" r="3" fill="#EFE3D0"/>',
 "bolt":     '<path d="M36 4 L 16 36 L 28 36 L 24 60 L 48 26 L 34 26 Z"/>',
 "spiral":   '<path d="M32 3 L37 27 L61 32 L37 37 L32 61 L27 37 L3 32 L27 27 Z"/>'
             '<circle cx="32" cy="32" r="4"/>',
 "shades":   '<path d="M6 26 h22 a3 3 0 0 1 3 3 v6 a8 8 0 0 1 -16 0 v-6 Z"/>'
             '<path d="M58 26 h-22 a3 3 0 0 0 -3 3 v6 a8 8 0 0 0 16 0 v-6 Z"/>'
             '<rect x="29" y="27" width="6" height="3"/>',
 "monstera": '<path d="M32 60 C 14 46 12 18 32 4 C 52 18 50 46 32 60 Z"/>'
             '<path d="M30.5 12 L33.5 12 L33.5 54 L30.5 54 Z" fill="#EFE3D0"/>'
             '<path d="M32 22 L22 16 M32 30 L20 26 M32 38 L23 36" stroke="#EFE3D0" stroke-width="2" fill="none"/>'
             '<path d="M32 22 L42 16 M32 30 L44 26 M32 38 L41 36" stroke="#EFE3D0" stroke-width="2" fill="none"/>',
}

INK="#241D18"; BONE="#EFE3D0"; TERRA="#C24A2C"
def icon(name, color=INK, bg=BONE):
    # concrete colours (WeasyPrint SVG can't resolve currentColor/var here); cut-outs = bg
    inner=ICONS[name].replace("currentColor", color).replace("#EFE3D0", bg)
    return (f'<svg viewBox="0 0 64 64" style="width:100%;height:100%;display:block;" '
            f'fill="{color}">{inner}</svg>')

# ---- page ----
GRID = ["sunburst","wave","fin","board","palm","hibiscus","gull","umbrella",
        "fish","bolt","spiral","shades","monstera","curl","sunrise"]

tiles=[]
schemes=[(BONE,INK),(INK,BONE),(TERRA,INK)]
for i,name in enumerate(GRID):
    bg,fg=schemes[i%3]
    tiles.append(f'<div class="ic" style="background:{bg};">'
                 f'<div class="ic-in">{icon(name, fg, bg)}</div></div>')

# framed 2x2 block panel (SOLMATES style) — bordered squares on bone
block=f'''<div class="block">
  <div class="bsq">{icon("board", INK, BONE)}</div>
  <div class="bsq">{icon("sunrise", INK, BONE)}</div>
  <div class="bsq">{icon("curl", INK, BONE)}</div>
  <div class="bsq">{icon("palm", INK, BONE)}</div>
</div>'''

# repeat pattern strip (terracotta icons on charcoal)
pat="".join(f'<span>{icon(GRID[k%len(GRID)], TERRA, INK)}</span>' for k in range(11))

html=f'''<div class="page bone">
  <style scoped>
    .intro{{ max-width:150mm; margin-bottom:6mm; }}
    .marks{{ display:flex; gap:5mm; margin-bottom:7mm; }}
    .markcard{{ flex:1; border:2px solid var(--ink); border-radius:3mm; padding:5mm;
                display:flex; align-items:center; gap:5mm; }}
    .markcard img{{ height:20mm; }}
    .markcard .mc-t{{ font-family:var(--display); font-size:13pt; }}
    .markcard .mc-s{{ font-family:var(--body); font-size:8pt; color:var(--ink-60); }}
    .icgrid{{ display:grid; grid-template-columns:repeat(5,1fr); gap:3.5mm; margin-bottom:7mm; }}
    .ic{{ border-radius:2.5mm; height:30mm; border:2px solid var(--ink);
          display:flex; align-items:center; justify-content:center; }}
    .ic-in{{ width:60%; height:60%; }}
    .lower{{ display:flex; gap:5mm; align-items:flex-start; }}
    .block{{ display:grid; grid-template-columns:1fr 1fr; gap:3mm; width:74mm; }}
    .bsq{{ height:33mm; border:3px solid var(--ink); border-radius:2mm; padding:6mm;
           background:var(--bone); color:var(--ink);
           display:flex; align-items:center; justify-content:center; }}
    .lower-x{{ flex:1; }}
    .pat{{ display:flex; gap:0; background:var(--ink); border-radius:3mm; padding:5mm 4mm;
           overflow:hidden; }}
    .pat span{{ width:17mm; height:15mm; flex:none; display:flex; align-items:center; justify-content:center; }}
    .pat span svg{{ width:11mm; }}
  </style>

  <div class="kicker">Toolkit</div>
  <h1 class="disp">Motifs &amp; Icons</h1>
  <p class="intro">A hand-carved kit for tees, stickers, stamps and signage. Block-print
    icons, the two signature marks, and a repeat that runs down the whole lane.</p>

  <div class="marks">
    <div class="markcard"><img src="../assets/brand/mark-tuktuk-EFE3D0.png"
      style="background:var(--ink);border-radius:2mm;padding:2mm;" alt="">
      <div><div class="mc-t">The Tuk</div><div class="mc-s">Primary mark · the road</div></div></div>
    <div class="markcard"><img src="../assets/brand/mark-wave-C24A2C.png" alt="">
      <div><div class="mc-t">The Wave</div><div class="mc-s">Secondary mark · the tide</div></div></div>
  </div>

  <div class="icgrid">{"".join(tiles)}</div>

  <h2 class="sub" style="margin-top:1mm;">Repeat &amp; Pattern</h2>
  <p style="font-size:9.5pt;margin-bottom:4mm;">Tile the icons into a carved block-print repeat —
    for tee backs, totes, board bags and signage that runs down the whole lane.</p>
  <div class="pat">{pat}</div>
  <div style="font-family:var(--body);font-weight:700;font-size:7pt;letter-spacing:.16em;
              text-transform:uppercase;color:var(--ink-60);margin-top:2.5mm;">Repeat pattern · endless lane</div>

  <div class="pgmark"><span>Tuk &amp; Tide Surf Club</span><span>Brand Kit · Weligama</span></div>
</div>'''

out=os.path.join(os.path.dirname(os.path.abspath(__file__)),"partials","09_motifs.html")
open(out,"w").write(html)
print("wrote",out)
