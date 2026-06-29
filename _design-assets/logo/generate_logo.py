#!/usr/bin/env python3
"""Generate logo.svg — Tuk & Tide Surf Club heritage wordmark (v2).
Woodcut half-sun + tuk-tuk-on-a-wave figure + unified wood-type stack (Ultra)
+ brushed 'SURF CLUB' arc (Permanent Marker). Charcoal ink, transparent-ish
bg (cutouts use terracotta to match the print). Arc text placed glyph-by-glyph
(WeasyPrint has no <textPath>)."""
import math, os

CX = 480
INK = "#241d18"
TERRA = "#C24A2C"

def _traced(fname, tx, ty, scale):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    s = open(p).read()
    inner = s[s.index("<g "):s.rindex("</g>") + 5]
    return f'<g transform="translate({tx},{ty}) scale({scale})">{inner}</g>'

def traced_auto(tx, ty, scale):
    """Vectorised auto-rickshaw line-art (from the reference frame)."""
    return _traced("tuktuk_ink.svg", tx, ty, scale)

def traced_wave(tx, ty, scale):
    """Vectorised bold woodcut wave (from the reference)."""
    return _traced("wave_ink.svg", tx, ty, scale)

def arc_text(s, radius, cy, center_deg, step_deg, size, font, weight="400"):
    n = len(s); out = []
    for i, ch in enumerate(s):
        if ch == " ":
            continue
        ang = center_deg + (i - (n - 1) / 2) * step_deg
        rad = math.radians(ang)
        x = CX + radius * math.cos(rad)
        y = cy + radius * math.sin(rad)
        rot = ang + 90 if center_deg < 0 else ang - 90
        esc = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(ch, ch)
        out.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{INK}" '
            f'font-family="{font}" font-weight="{weight}" text-anchor="middle" '
            f'dominant-baseline="central" '
            f'transform="rotate({rot:.2f} {x:.1f} {y:.1f})">{esc}</text>')
    return "\n    ".join(out)

def sun(cx, cy, r, n=8):
    """Solid half-disc + few thick, slightly irregular carved wedge rays."""
    parts = [f'<path d="M {cx-r} {cy} a {r} {r} 0 0 1 {2*r} 0 Z" fill="{INK}"/>']
    wb, wt = 30, 11
    for k in range(n):
        a = math.pi * (k + 0.5) / n
        jitter = ((k * 37) % 11 - 5) * 1.4          # deterministic wobble
        rb, rt = r + 5, r + 70 + jitter
        dx, dy = math.cos(math.pi - a), -math.sin(a)
        ux, uy = math.sin(a), -math.cos(a)
        bx, by = cx + dx*rb, cy + dy*rb
        tx, ty = cx + dx*rt, cy + dy*rt
        p1 = (bx+ux*wb, by+uy*wb); p2 = (bx-ux*wb, by-uy*wb)
        p3 = (tx-ux*wt, ty-uy*wt); p4 = (tx+ux*wt, ty+uy*wt)
        parts.append(f'<path d="M {p1[0]:.1f} {p1[1]:.1f} L {p4[0]:.1f} {p4[1]:.1f} '
                     f'L {p3[0]:.1f} {p3[1]:.1f} L {p2[0]:.1f} {p2[1]:.1f} Z" fill="{INK}"/>')
    return "\n  ".join(parts)

def tuktuk(tx, ty, s=1.0):
    """Solid charcoal auto-rickshaw (tuk-tuk) silhouette, facing left.
    Cues: small rounded driver nose + single small front wheel up front, taller
    canopied passenger cabin + larger rear wheel behind. Local box ~230x205."""
    g = [f'<g transform="translate({tx},{ty}) scale({s})">']
    # BODY (charcoal) — facing RIGHT. Tall rounded rear-left, big domed roof,
    # raked windshield sloping down to a rounded front-right snout.
    g.append(f'<path d="M 30 214 '
             f'C 14 214 10 198 10 172 '
             f'L 10 112 '
             f'C 10 54 40 34 96 34 '
             f'L 198 34 '
             f'C 232 34 250 48 258 80 '
             f'L 286 150 '
             f'C 296 172 298 194 288 214 '
             f'Z" fill="{INK}"/>')
    # windshield (terracotta, raked forward)
    g.append(f'<path d="M 214 66 L 250 80 L 274 150 L 230 150 Z" fill="{TERRA}"/>')
    # two passenger windows (terracotta) split by a thin pillar
    g.append(f'<path d="M 96 60 C 96 54 100 52 112 52 L 150 52 L 150 150 L 96 150 Z" fill="{TERRA}"/>')
    g.append(f'<path d="M 162 52 L 200 52 L 202 150 L 162 150 Z" fill="{TERRA}"/>')
    # door outline (terracotta stroke), lower middle
    g.append(f'<rect x="118" y="150" width="92" height="54" rx="9" fill="none" '
             f'stroke="{TERRA}" stroke-width="4"/>')
    # rear-panel deco (terracotta): zigzag + two stripes
    g.append(f'<path d="M 28 118 l 13 -9 l 13 9 l 13 -9 l 13 9" fill="none" '
             f'stroke="{TERRA}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
    g.append(f'<line x1="26" y1="140" x2="80" y2="140" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"/>')
    g.append(f'<line x1="26" y1="156" x2="80" y2="156" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"/>')
    # headlight cluster on the front snout + little front bump
    g.append(f'<circle cx="280" cy="176" r="9" fill="{TERRA}"/>'
             f'<circle cx="280" cy="176" r="4" fill="{INK}"/>')
    g.append(f'<circle cx="300" cy="196" r="11" fill="{INK}"/>')
    # WHEELS (charcoal) with terracotta hub — chunky, two visible
    g.append(f'<circle cx="80" cy="216" r="33" fill="{INK}"/>'
             f'<circle cx="80" cy="216" r="12" fill="{TERRA}"/>')
    g.append(f'<circle cx="246" cy="216" r="31" fill="{INK}"/>'
             f'<circle cx="246" cy="216" r="11" fill="{TERRA}"/>')
    g.append('</g>')
    return "\n  ".join(g)

def woodcut_waves(cx, y, w, n=3, h=54):
    """Bold woodcut swells: each crest rises on its back, hooks forward into a
    curl, with a terracotta barrel under the lip. y = crest line; band below."""
    x0 = cx - w/2.0
    sw = w / n
    yb = y + 28                              # trough line between waves
    d = [f"M {x0:.0f} {y+h:.0f}", f"L {x0:.0f} {yb:.0f}"]
    for k in range(n):
        bx = x0 + k*sw
        px = bx + sw*0.40                    # crest peak (left of centre)
        # steep back of the swell up to a tall crest
        d.append(f"C {bx+sw*0.08:.0f} {y-50:.0f} {px-sw*0.08:.0f} {y-58:.0f} {px:.0f} {y-40:.0f}")
        # crest hooks forward + down into the lip (the overhang)
        d.append(f"C {px+sw*0.20:.0f} {y-24:.0f} {px+sw*0.26:.0f} {y-6:.0f} {px+sw*0.18:.0f} {y+10:.0f}")
        # lip slides down the face to the next trough
        d.append(f"C {px+sw*0.12:.0f} {y+20:.0f} {bx+sw*0.84:.0f} {yb:.0f} {bx+sw:.0f} {yb:.0f}")
    d.append(f"L {x0+w:.0f} {y+h:.0f} Z")
    out = [f'<path d="{" ".join(d)}" fill="{INK}"/>']
    for k in range(n):                       # terracotta barrel tucked under each lip
        bx = x0 + k*sw
        px = bx + sw*0.40
        out.append(f'<path d="M {px-sw*0.06:.0f} {y-16:.0f} '
                   f'C {px+sw*0.14:.0f} {y-12:.0f} {px+sw*0.17:.0f} {y+6:.0f} {px+sw*0.04:.0f} {y+16:.0f} '
                   f'C {px-sw*0.04:.0f} {y+6:.0f} {px-sw*0.14:.0f} {y-4:.0f} {px-sw*0.06:.0f} {y-16:.0f} Z" '
                   f'fill="{TERRA}"/>')
    return "\n  ".join(out)

def wave_line(cx, y, w, amp=14, segs=6):
    seg = w/segs
    d = [f"M {cx-w/2:.0f} {y}"]
    up = True
    for k in range(segs):
        x0 = cx-w/2 + k*seg
        cy = y - amp if up else y + amp
        d.append(f"Q {x0+seg/2:.0f} {cy:.0f} {x0+seg:.0f} {y}")
        up = not up
    return f'<path d="{" ".join(d)}" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'

# =====================================================================
# Vertical stack, centred, evenly spaced (Sunburn-&-Waves layout):
#   TUK-TUK  /  WAVE  /  TUK & TIDE  /  SURF CLUB  /  WELIGAMA
# Each zone is its own band with generous, even breathing room.
# =====================================================================
# All zones share the SAME WIDTH (W) and are centred -> flush inline column.
# Tight, even vertical gaps.
W = 520
auto  = traced_auto(CX - W/2, 56, W/1740.0)    # zone 1  (width W, fills box)
waves = traced_wave(CX - W/2, 448, W/1186.0)   # zone 2  (width W, fills box)

hero1 = (f'<text x="{CX}" y="690" font-size="120" fill="{INK}" font-family="Ultra" '
         f'text-anchor="middle" letter-spacing="6" textLength="{W}" '
         f'lengthAdjust="spacingAndGlyphs">TUK &amp;</text>')
hero2 = (f'<text x="{CX}" y="838" font-size="170" fill="{INK}" font-family="Ultra" '
         f'text-anchor="middle" letter-spacing="2" textLength="{W}" '
         f'lengthAdjust="spacingAndGlyphs">TIDE</text>')

surf = (f'<text x="{CX}" y="912" font-size="62" fill="{INK}" font-family="Permanent Marker" '
        f'text-anchor="middle" textLength="455" lengthAdjust="spacing">SURF CLUB</text>')
place = (f'<text x="{CX}" y="972" font-size="32" fill="{INK}" font-family="Ultra" '
         f'text-anchor="middle" letter-spacing="6">WELIGAMA &#183; SRI LANKA</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 1025" width="960" height="1025">
  {auto}
  {waves}
  {hero1}
  {hero2}
  {surf}
  {place}
</svg>
'''
import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.svg")
open(out, "w").write(svg)
print("wrote", out)
