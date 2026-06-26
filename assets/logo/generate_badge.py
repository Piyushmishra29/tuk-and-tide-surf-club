#!/usr/bin/env python3
"""Generate badge.svg for Tuk & Tide Club.
Ring text is placed glyph-by-glyph (rotated) because WeasyPrint's SVG
renderer does not support <textPath>. Run: python3 generate_badge.py"""
import math

CX = CY = 300

def arc_text(s, radius, center_deg, step_deg, size, color="#2E211A"):
    """Place each glyph of s on a circle. step_deg>0 => clockwise (top text);
    use center at top (-90) with +step, or bottom (+90) with -step."""
    n = len(s)
    out = []
    for i, ch in enumerate(s):
        if ch == " ":
            continue
        ang = center_deg + (i - (n - 1) / 2) * step_deg
        rad = math.radians(ang)
        x = CX + radius * math.cos(rad)
        y = CY + radius * math.sin(rad)
        # glyph upright relative to its position on the ring
        rot = ang + 90 if center_deg < 0 else ang - 90
        esc = "&amp;" if ch == "&" else ch
        out.append(
            f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{color}" '
            f'text-anchor="middle" dominant-baseline="central" '
            f'transform="rotate({rot:.2f} {x:.2f} {y:.2f})">{esc}</text>'
        )
    return "\n    ".join(out)

top = arc_text("TUK · TIDE · CLUB", radius=212, center_deg=-90, step_deg=9.2, size=29)
bot = arc_text("WELIGAMA · SRI LANKA", radius=214, center_deg=90, step_deg=-7.6, size=22)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <!-- plate -->
  <circle cx="300" cy="300" r="288" fill="#F4EAD5"/>
  <circle cx="300" cy="300" r="288" fill="none" stroke="#C8502A" stroke-width="10"/>
  <circle cx="300" cy="300" r="252" fill="none" stroke="#2E7D74" stroke-width="4"/>
  <circle cx="300" cy="300" r="244" fill="none" stroke="#2E7D74" stroke-width="2"/>

  <!-- ring text (glyph-by-glyph, Fredoka) -->
  <g font-family="Fredoka, sans-serif" font-weight="700">
    {top}
    {bot}
  </g>
  <!-- side dots -->
  <circle cx="66"  cy="300" r="6" fill="#C8502A"/>
  <circle cx="534" cy="300" r="6" fill="#C8502A"/>

  <!-- rising sun -->
  <circle cx="300" cy="262" r="86" fill="#E0A434"/>
  <g stroke="#E0A434" stroke-width="9" stroke-linecap="round">
    <line x1="300" y1="150" x2="300" y2="128"/>
    <line x1="238" y1="166" x2="227" y2="147"/>
    <line x1="362" y1="166" x2="373" y2="147"/>
    <line x1="196" y1="210" x2="177" y2="199"/>
    <line x1="404" y1="210" x2="423" y2="199"/>
  </g>

  <!-- tuk-tuk (side profile) -->
  <g>
    <path d="M236 246 q64 -34 128 0 l6 14 q-70 -26 -140 0 z" fill="#C8502A"/>
    <path d="M232 262 q-6 -10 6 -12 l16 0 q14 -22 40 -22 l44 0 q26 0 30 22 l18 2
             q14 2 14 16 l0 18 q0 8 -10 8 l-160 0 q-10 0 -10 -10 z" fill="#C8502A"/>
    <path d="M262 250 q12 -16 30 -16 l0 24 l-34 0 z" fill="#2E7D74" opacity="0.85"/>
    <rect x="300" y="240" width="50" height="34" rx="6" fill="#F4EAD5"/>
    <circle cx="372" cy="276" r="5" fill="#E0A434"/>
    <circle cx="262" cy="312" r="20" fill="#2E211A"/><circle cx="262" cy="312" r="8" fill="#F4EAD5"/>
    <circle cx="352" cy="312" r="20" fill="#2E211A"/><circle cx="352" cy="312" r="8" fill="#F4EAD5"/>
  </g>

  <!-- wave -->
  <path d="M150 330 q40 -28 86 -10 q40 16 78 4 q44 -14 86 6 q26 12 50 2 l0 70 l-300 0 z" fill="#2E7D74"/>
  <path d="M150 352 q60 -22 120 0 q60 22 130 -2 l0 40 l-250 0 z" fill="#215A53"/>
  <g fill="#F4EAD5">
    <circle cx="210" cy="338" r="4"/><circle cx="262" cy="330" r="3"/>
    <circle cx="318" cy="336" r="4"/><circle cx="372" cy="330" r="3"/>
  </g>
</svg>
'''
open("badge.svg", "w").write(svg)
print("wrote badge.svg")
