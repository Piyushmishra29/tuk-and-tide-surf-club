#!/bin/zsh
# Render the logo SVG on terracotta; apply worn distress ONLY to the bold
# wave+wordmark zone (below the tuk-tuk), leaving the line-art frame crisp.
set -e
cd ~/Desktop/tuk-and-tide-club
python3 assets/logo/generate_logo.py >/dev/null
# page proportional to the 960x1025 viewBox so the svg fills it with NO offset
python3 - <<'PY'
svg=open('assets/logo/logo.svg').read()
head='''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Ultra';src:url('../assets/fonts/Ultra.ttf');}
@font-face{font-family:'Permanent Marker';src:url('../assets/fonts/PermanentMarker.ttf');}
@page{size:192mm 205mm;margin:0;}
body{margin:0;background:#C24A2C;}
svg{display:block;width:192mm;height:205mm;}
</style></head><body>'''
open('build/_logotest.html','w').write(head+svg+"</body></html>")
PY
python3 -m weasyprint build/_logotest.html build/_logotest.pdf 2>&1 | head -2
pdftoppm -png -r 150 build/_logotest.pdf build/_logoclean >/dev/null
CLEAN=build/_logoclean-1.png
DIM=$(magick identify -format "%wx%h" "$CLEAN"); W=${DIM%x*}; H=${DIM#*x}
cp "$CLEAN" build/logo-preview-clean.png
# --- worn distress: bold ink only, AND only below the tuk (region mask) ---
magick "$CLEAN" -colorspace gray -threshold 55% -negate build/_inkmask.png
magick build/_inkmask.png -morphology Open Disk:5 build/_thick.png
magick -size ${W}x${H} xc: +noise Random -channel R -separate -blur 0x0.3 -threshold 80% build/_grain.png
BND=$(python3 -c "print(int($H*0.42))")                                    # below the tuk
magick -size ${W}x${H} xc:black -fill white -draw "rectangle 0,${BND} ${W},${H}" build/_region.png
magick build/_thick.png build/_grain.png -compose multiply -composite build/_h1.png
magick build/_h1.png build/_region.png -compose multiply -composite build/_holes.png
magick -size ${W}x${H} xc:#C24A2C build/_terra.png
magick "$CLEAN" build/_terra.png build/_holes.png -compose over -composite build/logo-preview-worn.png
echo "done: clean + worn previews written"
