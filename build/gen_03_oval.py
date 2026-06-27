#!/usr/bin/env python3
import math, pathlib

INK  = "#241D18"   # charcoal
BONE = "#EFE3D0"   # bone/cream

CX, CY = 210, 140
RX, RY = 200, 132          # outer keyline ellipse
W, H   = 420, 280


def arc(s, cx, cy, r, center, step, size, font, color, weight=700):
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
        esc = {"&": "&amp;"}.get(ch, ch)
        out.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'font-family="{font}" font-weight="{weight}" text-anchor="middle" '
            f'dominant-baseline="central" letter-spacing="0.5" '
            f'transform="rotate({rot:.2f} {x:.1f} {y:.1f})">{esc}</text>'
        )
    return "\n".join(out)


def leaf(ox, oy, ang_deg, length, width, droop, color):
    """Filled palm frond (lens shape) from origin, drooping tip."""
    a = math.radians(ang_deg)
    dx, dy = math.cos(a), math.sin(a)
    # tip with gravity droop
    tx = ox + length * dx
    ty = oy + length * dy + droop
    # midpoint
    mx = (ox + tx) / 2
    my = (oy + ty) / 2
    # perpendicular
    px, py = -dy, dx
    c1x, c1y = mx + px * width, my + py * width + droop * 0.4
    c2x, c2y = mx - px * width, my - py * width + droop * 0.4
    return (
        f'<path d="M {ox:.1f} {oy:.1f} '
        f'Q {c1x:.1f} {c1y:.1f} {tx:.1f} {ty:.1f} '
        f'Q {c2x:.1f} {c2y:.1f} {ox:.1f} {oy:.1f} Z" fill="{color}"/>'
    )


# --- palm tree ---
ox, oy = 211, 126          # crown origin
trunk = (
    f'<path d="M 205 198 '
    f'C 201 172 207 148 209 128 '
    f'L 217 128 '
    f'C 215 150 213 174 215 198 Z" fill="{INK}"/>'
)
# bark notches
bark = "".join(
    f'<rect x="{206+ (i%2)*0.5:.1f}" y="{y}" width="9" height="2.4" rx="1.2" fill="{BONE}"/>'
    for i, y in enumerate([150, 162, 174, 186])
)

fronds = []
# (angle, length, width, droop)
specs = [
    (-172, 66, 9, 24),
    (-142, 72, 10, 16),
    (-110, 58, 9, 8),
    (-90,  42, 7, 2),
    (-70,  58, 9, 8),
    (-38,  72, 10, 16),
    ( -8,  66, 9, 24),
]
for ang, ln, wd, dr in specs:
    fronds.append(leaf(ox, oy, ang, ln, wd, dr, INK))
# coconuts
coconuts = (
    f'<circle cx="205" cy="130" r="4.2" fill="{INK}"/>'
    f'<circle cx="218" cy="131" r="4.2" fill="{INK}"/>'
    f'<circle cx="211" cy="136" r="4.2" fill="{INK}"/>'
)

# small ground swell
ground = f'<path d="M 165 200 Q 211 210 257 200" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>'

palm = trunk + "".join(fronds) + coconuts + bark + ground

# --- ring text ---
top = arc("TUK & TIDE SURF CLUB", CX, 196, 138, -90, 6.4, 21, "DM Sans", INK, 700)

# bottom straight label
bottom = (
    f'<text x="{CX}" y="232" font-size="15" fill="{INK}" font-family="DM Sans" '
    f'font-weight="700" text-anchor="middle" letter-spacing="2.2">'
    f'WELIGAMA &#183; SRI LANKA</text>'
)
# small star separators flanking bottom label
stars = (
    f'<circle cx="92" cy="227" r="2.4" fill="{INK}"/>'
    f'<circle cx="328" cy="227" r="2.4" fill="{INK}"/>'
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
  <ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="{BONE}" stroke="{INK}" stroke-width="5"/>
  <ellipse cx="{CX}" cy="{CY}" rx="{RX-12}" ry="{RY-12}" fill="none" stroke="{INK}" stroke-width="1.6"/>
  {palm}
  {top}
  {bottom}
  {stars}
</svg>'''

out = pathlib.Path("/Users/piyushmishra/Desktop/tuk-and-tide-club/assets/stickers/03_oval_palm.svg")
out.write_text(svg)
print("wrote", out)
