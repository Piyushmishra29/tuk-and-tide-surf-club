# TUK & TIDE SURF CLUB — WEBSITE BRIEF (read fully, follow exactly)

You are building ONE section of an aesthetic, **awwwards-grade** single-page website for a heritage
surf brand: **Tuk & Tide Surf Club** — tuk-tuk + surf rentals / lessons / tours in **Weligama Bay,
south-coast Sri Lanka**. Vintage woodcut / screenprint, **charcoal-on-terracotta**, warm sun-faded film.

## The look (non-negotiable)
- Heritage but modern. Big confident display type, generous whitespace, warm film photography,
  woodcut accents. **Restraint > clutter**: 2–3 deliberate motion beats per view, never 10.
- Cohesive with the brand book. Use ONLY the design system below. Mobile-perfect at **390px** too.

## Design system (already in assets/css/site.css — DO NOT redefine tokens; USE them)
Colour vars: `--ink #241D18` `--terra #C24A2C` `--clay #9E3A20` `--bone #EFE3D0` `--bone-2 #E7D8C2`
`--sand #D8C4A6` `--teal #2F5D57`; helpers `--ink-70 --bone-70`.
Font vars: `--display`=Ultra (HERO/headlines, UPPERCASE), `--anton`=Anton (alt condensed display),
`--marker`=Permanent Marker (hand accents), `--script`=Pacifico (script asides), `--body`=DM Sans (UI/body).
Classes you SHOULD reuse: `.container .section .bg-ink .bg-terra .bg-bone .bg-bone2 .bg-teal .grain`
`.display .anton .h-xl .h-lg .h-md .eyebrow .lead .marker .script .t-terra .t-bone .t-clay .t-teal`
`.btn .btn--primary .btn--ink .btn--ghost .btn--bone .pill .rule` and helpers `.grid .flex .center
.between .wrap .gap .stack .muted .muted-bone .maxch .ta-c .mx-auto`.

## Section structure (your deliverable)
Output ONE self-contained HTML fragment = a single `<section id="..." class="section bg-...">` with a
`.container` inside (hero/footer may differ). Put section CSS in ONE `<style>` block at the TOP of the
fragment, and **PREFIX EVERY custom class with your section name** (e.g. `.svc-card`, `.hero-title`)
so sections never collide. Use the tokens (`var(--terra)` etc.), never hard-code new palettes.

## Motion contract (don't build your own scroll engine)
Add `data-reveal` to elements you want animated in on scroll (variants: `data-reveal="left"`,
`"right"`, `"scale"`, `"fade"`). The shared site.js + IntersectionObserver handles it. Stagger by
wrapping siblings each with `data-reveal`. Content must still read with JS off — never rely on JS to
make text visible beyond the reveal classes. Hover micro-interactions (transform/opacity) are welcome.

## Anchors / nav ids (use these exact ids)
`#hero #about #services #spots #gallery #pricing #merch #book` + footer. Nav links jump to them.

## Brand facts / copy
- Name: **Tuk & Tide Surf Club**. Tagline: **"Surf, ride, repeat."**
- Positioning: *"The easygoing way to surf Sri Lanka's south coast — board under your arm, tuk-tuk at the curb."*
- Services: **Surf lessons** (group/private/courses), **Board & gear rental**, **Tuk-tuk tours & transfers** (self-drive hire too).
- Surf breaks: **Weligama Bay** (beginner beach break, our home) · **Mirissa** (whales & sunsets) ·
  **Midigama** (Lazy Left / Ram's Right, reef) · **Ahangama** (points).
- Values: Salt-cured craft · Local & proud · Easy stoke · Ride anywhere · Good company.
- Indicative rates (USD): Group lesson ~$20 · Private ~$35 · 3-lesson course ~$55 · Soft-top board $5/hr·$15/day ·
  Performance $7/hr·$20/day · Tuk-tuk transfers & day surf-safaris (Weligama–Midigama–Ahangama).
- Contacts (DRAFT): WhatsApp **+94 76 555 0123** · IG **@tukandtide.lk** · **hello@tukandtide.lk** ·
  **tukandtide.lk** · Weligama Bay, Sri Lanka. WhatsApp is the primary CTA (wa.me/94765550123).

## Assets (relative to site/ root, i.e. use `assets/img/...`)
- Photos (warm-graded): `assets/img/photos/` → r1_night_road, r2_moon, r3_stall, r4_stall2, r5_stall_dusk,
  r6_river_sunset, r7_forest_stars, r8_taillights, r9_muddy_moon, r10_sunset_front (.jpg). The blue auto in real scenes.
- Mockups: `assets/img/mockups/` → 07_tuktuk.png (golden-hour door decal), 09_stickerlay.png (sticker flat-lay),
  08_livery_lite.png (night livery), 06_sign_lite.png (painted sign), 01_cap,02_tee,03_board,04_tote.png.
- Stickers (transparent die-cut): `assets/img/stickers/` → 01_stamp_tuk … 20_*.png (20 files).
- Woodcut icons (SVG, charcoal+terra): `assets/img/icons/` → elephant, leopard, turtle, stilt_fisher, king_coconut.svg.
- Editorial refs: `assets/img/mag/` → m2 (vintage stamp), m3 (red tuk-tuk+surfboard), m4 (illustrated SL map),
  m6 (fruit stall), m7 (logo-over-photo), m8 (red linocut sheet). .jpg
- Logo: `assets/img/logo/` → logo.svg, logo-reversed.png (bone on dark), logo-terracotta.png,
  mark-tuktuk-EFE3D0.png / -C24A2C.png, mark-wave-EFE3D0.png / -C24A2C.png.
- Textures: `assets/img/tex/` → paper-ink.jpg, paper-bone.jpg, paper-terra.jpg, grain.png.

## Quality bar / self-verify
The site is assembled with `python3 build.py` and screenshotted with Puppeteer in `?static` mode
(reveals shown). Your section must look premium at 1440px AND 390px, with real hierarchy, no overflow,
legible contrast, and tasteful motion hooks. Write clean, valid HTML/CSS. No external CSS frameworks.
