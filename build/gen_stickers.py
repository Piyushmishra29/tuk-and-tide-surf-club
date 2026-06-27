#!/usr/bin/env python3
"""Generate a Tuk & Tide Surf Club sticker pack — varied vintage surf stickers
in the heritage palette. Emits individual sticker SVGs + a sheet HTML."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "assets", "logo")
INK, TERRA, BONE, CLAY, TEAL = "#241D18", "#C24A2C", "#EFE3D0", "#9E3A20", "#2F5D57"

def arc(s, cx, cy, r, center, step, size, font, color, weight="400", spacing=0):
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

def traced(fname, color, scale, tx, ty):
    s=open(os.path.join(LOGO,fname)).read()
    inner=s[s.index("<g "):s.rindex("</g>")+5].replace("#241d18",color).replace("#241D18",color)
    return f'<g transform="translate({tx},{ty}) scale({scale})">{inner}</g>'

# ---- a few woodcut icons (fill placeholder __C__) ----
def sun(cx,cy,r,c):
    p=[f'<path d="M {cx-r} {cy} a {r} {r} 0 0 1 {2*r} 0 Z" fill="{c}"/>']
    for k in range(9):
        a=math.pi*(k+0.5)/9; dx,dy=math.cos(math.pi-a),-math.sin(a); ux,uy=math.sin(a),-math.cos(a)
        bx,by=cx+dx*(r+3),cy+dy*(r+3); tx,ty=cx+dx*(r+r*0.7),cy+dy*(r+r*0.7)
        wb,wt=r*0.30,r*0.10
        p.append(f'<path d="M {bx+ux*wb:.1f} {by+uy*wb:.1f} L {tx+ux*wt:.1f} {ty+uy*wt:.1f} '
                 f'L {tx-ux*wt:.1f} {ty-uy*wt:.1f} L {bx-ux*wb:.1f} {by-uy*wb:.1f} Z" fill="{c}"/>')
    return "".join(p)
def palm(cx,cy,s,c):
    g=f'<g transform="translate({cx-32*s},{cy-32*s}) scale({s})" fill="{c}">'
    g+=('<path d="M29 58 C 29 44 30 36 32 29 l4 1 C 34 37 33 46 35 58 Z"/>'
        '<path d="M32 29 C 19 21 9 22 3 29 C 12 17 26 21 32 29 Z"/>'
        '<path d="M32 29 C 45 21 55 22 61 29 C 52 17 38 21 32 29 Z"/>'
        '<path d="M32 29 C 23 17 15 11 8 10 C 22 10 30 19 32 29 Z"/>'
        '<path d="M32 29 C 41 17 49 11 56 10 C 42 10 34 19 32 29 Z"/>'
        '<path d="M32 29 C 30 16 30 9 32 3 C 36 11 35 21 32 29 Z"/>'
        '<circle cx="32" cy="29" r="4"/>')
    return g+'</g>'
def waves3(cx,cy,w,c):
    return (f'<g fill="none" stroke="{c}" stroke-width="{w*0.04}" stroke-linecap="round">'
            f'<path d="M {cx-w/2} {cy-w*0.12} q {w*0.12} -{w*0.1} {w*0.24} 0 q {w*0.12} {w*0.1} {w*0.24} 0 q {w*0.12} -{w*0.1} {w*0.24} 0"/>'
            f'<path d="M {cx-w/2} {cy} q {w*0.12} -{w*0.1} {w*0.24} 0 q {w*0.12} {w*0.1} {w*0.24} 0 q {w*0.12} -{w*0.1} {w*0.24} 0"/>'
            f'<path d="M {cx-w/2} {cy+w*0.12} q {w*0.12} -{w*0.1} {w*0.24} 0 q {w*0.12} {w*0.1} {w*0.24} 0 q {w*0.12} -{w*0.1} {w*0.24} 0"/></g>')
def hibiscus(cx,cy,r,c,center=None):
    center=center or c; p=[]
    for k in range(5):
        a=2*math.pi*k/5-math.pi/2; px=cx+math.cos(a)*r*0.5; py=cy+math.sin(a)*r*0.5
        p.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{r*0.42:.1f}" ry="{r*0.6:.1f}" '
                 f'transform="rotate({math.degrees(a)+90:.1f} {px:.1f} {py:.1f})" fill="{c}"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.2:.1f}" fill="{center}"/>')
    return "".join(p)

def svg(vb, body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb}" preserveAspectRatio="xMidYMid meet">{body}</svg>'

S = {}

# 1 — round stamp: tuk-tuk, terracotta
b=f'<circle cx="180" cy="180" r="176" fill="{TERRA}"/><circle cx="180" cy="180" r="176" fill="none" stroke="{INK}" stroke-width="6"/><circle cx="180" cy="180" r="150" fill="none" stroke="{INK}" stroke-width="3"/>'
b+=arc("TUK · TIDE · SURF CLUB",180,180,128,-90,16.5,21,"Ultra",INK)
b+=arc("WELIGAMA · SRI LANKA",180,180,130,90,-14.5,18,"Ultra",INK)
b+=traced("tuktuk_ink.svg",INK,0.108,86,118)
S["01_stamp_tuk"]=svg("360 360",b)

# 2 — round stamp: wave, charcoal
b=f'<circle cx="180" cy="180" r="176" fill="{INK}"/><circle cx="180" cy="180" r="150" fill="none" stroke="{TERRA}" stroke-width="4"/>'
b+=arc("TWO WAVES · THREE WHEELS",180,180,130,-90,12.5,16,"Ultra",BONE)
b+=arc("· ONE CLUB ·",180,180,132,90,-17,18,"Ultra",TERRA)
b+=traced("wave_ink.svg",BONE,0.135,92,150)
b+=f'<text x="180" y="135" font-size="20" fill="{TERRA}" font-family="Permanent Marker" text-anchor="middle">est. 26</text>'
S["02_stamp_wave"]=svg("360 360",b)

# 3 — oval badge: palm, bone
b=f'<ellipse cx="180" cy="180" rx="170" ry="125" fill="{BONE}"/><ellipse cx="180" cy="180" rx="170" ry="125" fill="none" stroke="{INK}" stroke-width="6"/><ellipse cx="180" cy="180" rx="150" ry="106" fill="none" stroke="{INK}" stroke-width="2"/>'
b+=arc("TUK & TIDE SURF CLUB",180,182,98,-90,12,18,"Ultra",INK)
b+=palm(180,168,1.5,INK)
b+=f'<text x="180" y="250" font-size="15" fill="{INK}" font-family="DM Sans" font-weight="700" letter-spacing="3" text-anchor="middle">WELIGAMA · SRI LANKA</text>'
S["03_oval_palm"]=svg("360 250",b)

# 4 — groovy slogan blob: SURF RIDE REPEAT
b=f'<rect x="6" y="6" width="348" height="348" rx="60" fill="{TERRA}"/><rect x="6" y="6" width="348" height="348" rx="60" fill="none" stroke="{INK}" stroke-width="6"/>'
b+=f'<text x="180" y="120" font-size="62" fill="{INK}" font-family="Shrikhand" text-anchor="middle">Surf</text>'
b+=f'<text x="180" y="200" font-size="62" fill="{BONE}" font-family="Shrikhand" text-anchor="middle">Ride</text>'
b+=f'<text x="180" y="280" font-size="62" fill="{INK}" font-family="Shrikhand" text-anchor="middle">Repeat</text>'
b+=waves3(180,322,180,INK)
S["04_groovy_srr"]=svg("360 360",b)

# 5 — sun seal: SALTY ALL DAY
b=f'<circle cx="180" cy="180" r="176" fill="{TERRA}"/><circle cx="180" cy="180" r="176" fill="none" stroke="{INK}" stroke-width="6"/>'
b+=sun(180,150,52,INK)
b+=arc("· SALTY ALL DAY ·",180,180,138,90,-15,22,"Ultra",INK)
b+=f'<text x="180" y="235" font-size="17" fill="{INK}" font-family="Permanent Marker" text-anchor="middle">Weligama</text>'
S["05_sun_seal"]=svg("360 360",b)

# 6 — script TIDE oval (swimwear-style)
b=f'<ellipse cx="180" cy="130" rx="168" ry="96" fill="{INK}"/><ellipse cx="180" cy="130" rx="150" ry="80" fill="none" stroke="{TERRA}" stroke-width="4"/>'
b+=f'<text x="180" y="150" font-size="86" fill="{BONE}" font-family="Pacifico" text-anchor="middle">Tide</text>'
b+=f'<text x="180" y="230" font-size="20" fill="{INK}" font-family="DM Sans" font-weight="700" letter-spacing="8" text-anchor="middle">SURF CLUB</text>'
S["06_script_tide"]=svg("360 260",b)

# 7 — patch: EST MMXXVI
b=f'<rect x="6" y="6" width="408" height="208" rx="28" fill="{INK}"/><rect x="18" y="18" width="384" height="184" rx="20" fill="none" stroke="{TERRA}" stroke-width="3"/>'
b+=f'<text x="210" y="86" font-size="46" fill="{BONE}" font-family="Ultra" text-anchor="middle" letter-spacing="2">EST. MMXXVI</text>'
b+=waves3(210,120,210,TERRA)
b+=f'<text x="210" y="170" font-size="17" fill="{BONE}" font-family="DM Sans" font-weight="700" letter-spacing="6" text-anchor="middle">SOUTH COAST · SRI LANKA</text>'
S["07_patch_est"]=svg("420 220",b)

# 8 — street sign: TUK LN
b=f'<rect x="6" y="6" width="408" height="148" rx="16" fill="{TEAL}"/><rect x="16" y="16" width="388" height="128" rx="10" fill="none" stroke="{BONE}" stroke-width="4"/>'
b+=palm(58,80,1.3,BONE)
b+=f'<text x="232" y="98" font-size="60" fill="{BONE}" font-family="Ultra" text-anchor="middle" letter-spacing="2">TUK LN</text>'
S["08_street_sign"]=svg("420 160",b)

# 9 — hibiscus circle: RIDE THE TIDE
b=f'<circle cx="180" cy="180" r="176" fill="{BONE}"/><circle cx="180" cy="180" r="176" fill="none" stroke="{INK}" stroke-width="6"/>'
b+=hibiscus(180,168,70,TERRA,INK)
b+=arc("· RIDE THE TIDE ·",180,180,140,90,-15,22,"Ultra",INK)
S["09_hibiscus"]=svg("360 360",b)

# 10 — wordmark die-cut (the locked logo wordmark, simple)
b=f'<rect x="4" y="4" width="412" height="172" rx="20" fill="{BONE}"/><rect x="4" y="4" width="412" height="172" rx="20" fill="none" stroke="{INK}" stroke-width="5"/>'
b+=traced("wave_ink.svg",INK,0.14,118,18)
b+=f'<text x="210" y="120" font-size="62" fill="{INK}" font-family="Ultra" text-anchor="middle" letter-spacing="1">TUK &amp; TIDE</text>'
b+=f'<text x="210" y="156" font-size="22" fill="{INK}" font-family="Permanent Marker" text-anchor="middle">surf club</text>'
S["10_wordmark"]=svg("420 180",b)

# ---- write individual svgs ----
outdir=os.path.join(HERE,"..","assets","stickers"); os.makedirs(outdir,exist_ok=True)
for k,v in S.items(): open(os.path.join(outdir,k+".svg"),"w").write(v)
print("wrote",len(S),"sticker svgs")

# ---- sticker sheet html ----
cells="".join(f'<div class="st">{v}</div>' for v in S.values())
html=f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'Ultra';src:url('../assets/fonts/Ultra.ttf');}}
@font-face{{font-family:'Permanent Marker';src:url('../assets/fonts/PermanentMarker.ttf');}}
@font-face{{font-family:'Shrikhand';src:url('../assets/fonts/Shrikhand.ttf');}}
@font-face{{font-family:'Pacifico';src:url('../assets/fonts/Pacifico.ttf');}}
@font-face{{font-family:'DM Sans';src:url('../assets/fonts/DMSans.ttf');font-weight:700;}}
@page{{size:230mm 300mm;margin:0;}}
body{{margin:0;background:#EFE3D0;}}
.sheet{{padding:16mm 14mm;}}
.head{{font-family:'Ultra';font-size:30pt;color:#241D18;margin:0 0 1mm;}}
.sub{{font-family:'DM Sans';font-weight:700;font-size:9pt;letter-spacing:.3em;text-transform:uppercase;color:#9E3A20;margin-bottom:8mm;}}
.grid{{display:flex;flex-wrap:wrap;gap:9mm;align-items:center;justify-content:flex-start;}}
.st{{width:54mm;display:flex;align-items:center;justify-content:center;}}
.st svg{{width:100%;height:auto;display:block;}}
</style></head><body><div class="sheet">
<div class="head">Sticker Pack</div>
<div class="sub">Tuk &amp; Tide Surf Club · Weligama · peel &amp; stick</div>
<div class="grid">{cells}</div>
</div></body></html>'''
open(os.path.join(HERE,"_stickers.html"),"w").write(html)
print("wrote sheet html")
