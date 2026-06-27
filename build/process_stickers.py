#!/usr/bin/env python3
"""Render each sticker SVG to a transparent PNG, then apply a vintage die-cut
treatment: subtle sun-fade + grain + light distress + bone kiss-cut border +
drop shadow. Outputs assets/stickers/png/NN.png (premium die-cut stickers)."""
import glob, os, re, subprocess, math
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
OUT=os.path.join(ROOT,"assets","stickers","png"); os.makedirs(OUT,exist_ok=True)
FONTS={ 'Ultra':'Ultra.ttf','Permanent Marker':'PermanentMarker.ttf','Shrikhand':'Shrikhand.ttf',
        'Pacifico':'Pacifico.ttf','DM Sans':'DMSans.ttf'}
ff="".join(f"@font-face{{font-family:'{k}';src:url('../assets/fonts/{v}');}}\n" for k,v in FONTS.items())

def sh(cmd): subprocess.run(cmd, shell=True, check=True)

# shared grain + grunge textures (big; resized per sticker)
sh(f'magick -size 1500x1500 xc:gray50 -attenuate 0.7 +noise Gaussian -blur 0x0.4 -colorspace Gray {HERE}/_grain.png')
sh(f'magick -size 1500x1500 xc:black -attenuate 2 +noise Laplacian -blur 0x2 -auto-level -threshold 78% -negate {HERE}/_grunge.png')

for f in sorted(glob.glob(os.path.join(ROOT,"assets","stickers","*.svg"))):
    name=os.path.splitext(os.path.basename(f))[0]
    svg=open(f).read()
    m=re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"',svg); W,H=(float(m.group(1)),float(m.group(2))) if m else (360,360)
    pw=96.0; ph=pw*H/W
    html=(f'<!doctype html><html><head><meta charset="utf-8"><style>{ff}'
          f'@page{{size:{pw:.1f}mm {ph:.1f}mm;margin:0;}}html,body{{margin:0;background:transparent;}}'
          f'svg{{display:block;width:{pw:.1f}mm;height:{ph:.1f}mm;}}</style></head><body>{svg}</body></html>')
    open(f"{HERE}/_s.html","w").write(html)
    sh(f'python3 -m weasyprint {HERE}/_s.html {HERE}/_s.pdf 2>/dev/null')
    sh(f'pdftocairo -png -transp -r 200 {HERE}/_s.pdf {HERE}/_s')
    raw=f"{HERE}/_s-1.png"
    sh(f'magick {raw} -bordercolor none -border 60 {HERE}/_pad.png')          # room for border+shadow
    sh(f'magick identify -format "%wx%h" {HERE}/_pad.png > {HERE}/_dim.txt')
    dim=open(f"{HERE}/_dim.txt").read().strip(); PW,PH=[int(x) for x in dim.split("x")]
    disk=max(10,int(min(PW,PH)*0.022))                                        # border thickness ~2.2%
    # 1) texture: slight desat + grain (multiply) + light distress, alpha preserved
    sh(f'magick {HERE}/_pad.png \\( {HERE}/_grain.png -resize {PW}x{PH}! \\) -compose Multiply -composite '
       f'{HERE}/_pad.png -compose CopyOpacity -composite -modulate 100,92,100 {HERE}/_tex.png')
    sh(f'magick {HERE}/_tex.png \\( {HERE}/_tex.png -alpha extract \\( {HERE}/_grunge.png -resize {PW}x{PH}! \\) '
       f'-compose Multiply -composite \\) -alpha off -compose CopyOpacity -composite {HERE}/_dis.png')
    # 2) bone kiss-cut border
    sh(f'magick {HERE}/_dis.png -alpha extract -morphology Dilate Disk:{disk} -threshold 1% {HERE}/_mask.png')
    sh(f'magick {HERE}/_mask.png -background "#EFE3D0" -alpha shape '
       f'\\( {HERE}/_dis.png \\) -compose Over -composite {HERE}/_cut.png')
    # 3) drop shadow
    sh(f'magick {HERE}/_cut.png \\( +clone -background black -shadow 46x10+0+9 \\) '
       f'+swap -background none -layers merge +repage -trim +repage {OUT}/{name}.png')
    print("processed", name)
print("DONE")
