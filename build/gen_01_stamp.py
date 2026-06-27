#!/usr/bin/env python3
import math, re, os

ROOT = "/Users/piyushmishra/Desktop/tuk-and-tide-club"
INK = "#241D18"
TERRA = "#C24A2C"

# ---- palette / geometry ----
W = H = 360
cx = cy = 180

def arc(s, cx, cy, r, center, step, size, font, color, weight="normal"):
    out = []
    n = len(s)
    for i, ch in enumerate(s):
        if ch == " ":
            continue
        a = center + (i - (n - 1) / 2) * step
        rad = math.radians(a)
        x = cx + r * math.cos(rad)
        y = cy + r * math.sin(rad)
        rot = a + 90 if center < 0 else a - 90
        esc = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(ch, ch)
        out.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'font-family="{font}" font-weight="{weight}" text-anchor="middle" '
            f'dominant-baseline="central" '
            f'transform="rotate({rot:.2f} {x:.1f} {y:.1f})">{esc}</text>'
        )
    return "\n".join(out)

# ---- pull the tuk-tuk line-art inner <g> ----
with open(os.path.join(ROOT, "assets/logo/tuktuk_ink.svg")) as f:
    raw = f.read()
inner = re.search(r"<g transform.*?</g>", raw, re.S).group(0)
# recolour to charcoal ink (already #241d18 but be explicit / case-safe)
inner = re.sub(r'fill="#241d18"', f'fill="{INK}"', inner, flags=re.I)

# art box ~1740x1178 ; we want ~136 wide -> scale, fit inside inner keyline r=150
S = 0.080
artw, arth = 1740 * S, 1178 * S      # ~139 x 94
tx = cx - artw / 2
ty = cy - arth / 2                   # centred
mark = f'<g transform="translate({tx:.1f},{ty:.1f}) scale({S})">{inner}</g>'

# ---- ring text (band between inner keyline and outer edge) ----
RT = 167
top = arc("TUK · TIDE · SURF CLUB", cx, cy, RT, -90, 7.6, 16, "Ultra", INK)
bot = arc("WELIGAMA · SRI LANKA", cx, cy, RT, 90, -8.2, 16, "Ultra", INK)

# small star separators flanking the L/R transition between the two arcs
def star(x, y, r=5):
    pts = []
    for k in range(10):
        ang = math.radians(-90 + k * 36)
        rr = r if k % 2 == 0 else r * 0.42
        pts.append(f"{x + rr*math.cos(ang):.1f},{y + rr*math.sin(ang):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{INK}"/>'

stars = star(cx - RT, cy) + star(cx + RT, cy)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<circle cx="{cx}" cy="{cy}" r="178" fill="{INK}"/>
<circle cx="{cx}" cy="{cy}" r="175" fill="{TERRA}"/>
<circle cx="{cx}" cy="{cy}" r="156" fill="none" stroke="{INK}" stroke-width="3"/>
<circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="{INK}" stroke-width="1.5"/>
{top}
{bot}
{stars}
{mark}
</svg>'''

out_dir = os.path.join(ROOT, "assets/stickers")
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, "01_stamp_tuk.svg"), "w") as f:
    f.write(svg)

# ---- self-verify html ----
with open(os.path.join(ROOT, "build/_try_01.html"), "w") as f:
    f.write(f'''<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:'Ultra';src:url('../assets/fonts/Ultra.ttf');}}
body{{margin:0;background:#cfcfcf;padding:20px}}
svg{{width:340px;height:auto}}
</style><body>{svg}</body>''')
print("wrote sticker + try html")
