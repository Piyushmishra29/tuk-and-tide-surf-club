#!/usr/bin/env python3
"""Scatter the die-cut sticker PNGs onto a warm-paper sheet, gently rotated."""
import glob, os, re
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
pngs=sorted(glob.glob(os.path.join(ROOT,"assets","stickers","png","*.png")))
# heroes bigger; angle varies deterministically
HERO={"01_stamp_tuk","02_stamp_wave","05_sun_seal"}
cells=[]
for i,p in enumerate(pngs):
    nm=os.path.splitext(os.path.basename(p))[0]
    ang=((i*37)%13)-6                     # -6..+6 deg
    h=50 if nm in HERO else 38            # display height mm
    cells.append(f'<div class="st" style="transform:rotate({ang}deg);">'
                 f'<img src="../assets/stickers/png/{os.path.basename(p)}" style="height:{h}mm;"></div>')
html=f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'Ultra';src:url('../assets/fonts/Ultra.ttf');}}
@page{{size:300mm 360mm;margin:0;}}
body{{margin:0;background:#E7DAC4 url('../assets/tex/paper-bone.jpg') center/cover;}}
.sheet{{padding:20mm 18mm;}}
.head{{font-family:'Ultra';font-size:42pt;color:#241D18;margin:0;}}
.sub{{font-family:sans-serif;font-weight:700;font-size:10pt;letter-spacing:.34em;text-transform:uppercase;color:#9E3A20;margin:2mm 0 12mm;}}
.grid{{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:6mm 4mm;}}
.st{{display:flex;align-items:center;justify-content:center;}}
.st img{{display:block;width:auto;}}
</style></head><body><div class="sheet">
<div class="head">Sticker Pack</div>
<div class="sub">Tuk &amp; Tide Surf Club · Weligama · Peel &amp; Stick · {len(pngs)} designs</div>
<div class="grid">{''.join(cells)}</div>
</div></body></html>'''
open(os.path.join(HERE,"sticker_sheet.html"),"w").write(html)
print(f"sheet with {len(pngs)} stickers")
