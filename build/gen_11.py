#!/usr/bin/env python3
"""Sticker 11 — SHAKA HAND. Charcoal circle, bone shaka silhouette,
HANG LOOSE ring text in Ultra, small WELIGAMA in terracotta."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "..", "assets", "stickers", "11_shaka.svg")
INK, TERRA, BONE, CLAY, TEAL = "#241D18", "#C24A2C", "#EFE3D0", "#9E3A20", "#2F5D57"

def arc(s, cx, cy, r, center, step, size, font, color, weight="400"):
    out=[]; n=len(s)
    for i,ch in enumerate(s):
        if ch==" ": continue
        a=center+(i-(n-1)/2)*step; rad=math.radians(a)
        x=cx+r*math.cos(rad); y=cy+r*math.sin(rad)
        rot=a+90 if center<0 else a-90
        esc={"&":"&amp;","<":"&lt;",">":"&gt;"}.get(ch,ch)
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
                   f'font-family="{font}" font-weight="{weight}" text-anchor="middle" '
                   f'dominant-baseline="central" transform="rotate({rot:.2f} {x:.1f} {y:.1f})">{esc}</text>')
    return "\n".join(out)

# ---- shaka hand silhouette (thumb up-left, pinky up-right, fist below) ----
SHAKA = (
    "M 158 282 "
    "C 140 280 130 256 129 230 "
    "C 128 208 126 190 120 175 "      # left palm edge up to thumb base
    "C 110 158 96 134 84 114 "        # thumb outer edge up-left (thick)
    "C 77 103 82 94 92 97 "           # thumb tip cap
    "C 104 101 120 126 134 150 "      # thumb inner edge back down
    "C 140 160 145 168 150 175 "      # web between thumb & fingers
    "C 153 165 156 160 162 160 "      # knuckle peak 1
    "C 167 160 169 166 174 166 "      # valley
    "C 178 166 180 160 186 160 "      # knuckle peak 2
    "C 191 160 193 166 198 166 "      # valley
    "C 202 166 205 161 212 163 "      # ridge to pinky base
    "C 220 150 230 132 242 120 "      # pinky outer edge up-right (thin)
    "C 250 111 258 108 266 111 "      # pinky tip cap
    "C 272 113 271 122 266 130 "      # pinky inner edge start
    "C 256 145 246 160 240 174 "      # pinky inner edge down
    "C 238 188 236 206 235 226 "      # right palm edge
    "C 234 250 226 280 212 282 "      # down to wrist (right)
    "C 198 290 172 290 158 282 "      # rounded wrist
    "Z"
)

def svg(vb, body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb}" preserveAspectRatio="xMidYMid meet">{body}</svg>'

cx=cy=180
b  = f'<circle cx="{cx}" cy="{cy}" r="176" fill="{INK}"/>'
b += f'<circle cx="{cx}" cy="{cy}" r="167" fill="none" stroke="{TERRA}" stroke-width="3"/>'
# top ring text
b += arc("HANG LOOSE", cx, cy, 142, -90, 16.5, 30, "Ultra", BONE)
# shaka hand
b += f'<path d="{SHAKA}" fill="{BONE}"/>'
# bottom label
b += f'<text x="{cx}" y="322" font-size="17" fill="{TERRA}" font-family="DM Sans" font-weight="700" letter-spacing="9" text-anchor="middle">WELIGAMA</text>'

open(OUT,"w").write(svg("360 360", b))
print("wrote", os.path.abspath(OUT))
