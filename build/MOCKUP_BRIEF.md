# MOCKUP BRIEF — Tuk & Tide Surf Club (read fully)

Make ONE photoreal product mockup: composite a brand sticker/artwork onto a real product
photo so it looks genuinely printed/embroidered/stuck ON it — warm, film-like, Pinterest-worthy.
Tools: ImageMagick 7 (`magick`), `pdftocairo`. Work at full product-photo resolution.

## Inputs
- Product photos: `assets/mockup/products/` (cap.jpg, tee.jpg, board.jpg, tote.jpg, mug.jpg, wood_sign.jpg)
- Real auto photos: `assets/mood/real/` (r3_stall, r6_river_sunset, r9_muddy_moon … the blue tuk-tuk)
- Brand artwork = the die-cut sticker PNGs (transparent): `assets/stickers/png/*.png`
  (e.g. 01_stamp_tuk, 02_stamp_wave, 10_wordmark, 17_stay_salty, 19_weligama). Pick the one that fits.
- Palette: charcoal #241D18 · terracotta #C24A2C · bone #EFE3D0.

## The pipeline (the trick = stack these so the art doesn't "float")
```bash
PROD=assets/mockup/products/tee.jpg
ART=assets/stickers/png/02_stamp_wave.png      # transparent artwork
SIZE=$(magick identify -format '%wx%h' "$PROD")

# 1) displacement map from the product's own folds/curve
magick "$PROD" -colorspace Gray -blur 0x6 -auto-level build/_dmap.png

# 2) shading layer (HardLight) so light/shadow falls across the art
#    (use the product's gray, blurred)

# 3) place artwork on a product-sized transparent canvas (position/scale over the print area)
magick -size "$SIZE" xc:none \( "$ART" -resize 40% \) -gravity center -geometry +0-60 build/_placed.png

# 4) warp it to the folds (DIAL compose:args 10..22)
magick build/_placed.png build/_dmap.png -virtual-pixel transparent \
  -compose Displace -define compose:args=14x14 -composite build/_warp.png

# 5) shade it (HardLight = ink takes the cloth's light; Multiply for darker print)
magick build/_warp.png \( "$PROD" -colorspace Gray -blur 0x1.5 \) -compose HardLight -composite build/_shaded.png

# 6) (optional) mask to the print area with a drawn ellipse/polygon + DstIn

# 7) drop onto product, knock art opacity ~90% so fabric breathes
magick "$PROD" \( build/_shaded.png -channel A -evaluate multiply 0.9 +channel \) -compose over -composite build/_m.png

# 8) WARM FILM GRADE (apply to the final so all mockups match)
magick build/_m.png -modulate 100,90,100 -level 6%,96% -brightness-contrast 2x-6 \
   -fill "#C24A2C" -colorize 5% +noise Gaussian -attenuate 0.35 FINAL.png
```
- For a **cylinder (mug/bottle)**: use a synthetic horizontal bow, displace mostly in X (`compose:args=34x4`).
- For an **angled plane (tuk-tuk door, wood sign, laptop)**: use `-distort Perspective 'x1,y1 X1,Y1 x2,y2 X2,Y2 x3,y3 X3,Y3 x4,y4 X4,Y4'` (TL,TR,BL,BR — read the door/sign corner pixels off the photo) BEFORE displace.
- For a **sticker on a board**: keep its bone die-cut border, add a real drop shadow (`-shadow 50x6+4+6`), slight curl optional — do NOT multiply it flat (stickers sit ON the surface).
- Embroidery (cap): scale art small, HardLight, add a faint 1px highlight/shadow per the brief if you can — at minimum displace + HardLight so it reads stitched, not printed.

## Failure modes → fix
art looks pasted → add displace + shading. melts → lower compose:args / raise map blur. too dark → HardLight not Multiply. too crisp → opacity 0.9 + tiny blur. spills off panel → mask. floats → add shadow.

## SELF-VERIFY (required)
Render your FINAL to a small preview and LOOK:
`magick FINAL.png -resize 700x build/_chk_<name>.png` then read it. Iterate until it genuinely looks
like a real photo of the product with the design on it (warm, grounded, not floating). Delete temp files.

## Deliverable
Write the FINAL composite to the EXACT path in your task (`assets/mockup/out/NN_name.png`),
high-res (≥1000px). Return a one-line summary of what you made.
