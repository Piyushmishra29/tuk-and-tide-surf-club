# TUK & TIDE — ANIMATION BRIEF (read fully)

The shared motion engine (assets/js/site.js) is DONE and tested. You ADD animation to ONE section
by adding data-attributes to markup + section-scoped CSS (hover/keyframes). **Never edit site.js or
the global token block of site.css.** Keep all custom classes PREFIXED by your section.

Goal: a LOT of tasteful motion on every section — but premium, not janky. Layer 3-6 beats per section
(an entrance + a scroll beat + hover micro-interactions). Everything must still read with the final
state correct (we verify in `?static`, which forces final/visible state) and respect reduced-motion
(the engine + CSS already handle that — just use the API, don't fight it).

## The data-attribute API (all opt-in)

### Reveal on scroll — `data-reveal="<variant>"`
Variants: (default = up) · `left` · `right` · `up-lg` · `scale` · `scale-up` · `fade` · `blur` ·
`rotate` · `clip` (wipe L→R) · `clip-up` (wipe bottom→up).
- Stagger a set: put `data-reveal-group` on the PARENT; give each child `data-reveal`. Auto-delays 80ms each.
- The engine adds `.is-in` when it scrolls into view; CSS animates from hidden→final. Use freely on
  headings, cards, images, list rows, paragraphs, buttons.

### Split-text headline reveal — `data-split="words"` or `data-split="chars"`
Word/char line-mask rise (each unit slides up from a clip). Optional `data-split-stagger="60"` (ms).
**ONLY use on elements whose content is PLAIN TEXT** (no nested spans/markup — the engine reads
textContent). Great for eyebrows and big `.h-lg`/`.h-xl` headlines that are plain text. If a heading
has a coloured nested span (e.g. an `&`), DON'T split it — use `data-reveal` instead.

### Parallax (scroll-driven, transform only)
- `data-parallax="0.15"` → vertical drift (bigger = more). Already used on hero bg.
- `data-parallax-x="0.1"` → horizontal drift.
- `data-img-parallax="0.12"` → put on an `overflow:hidden` FRAME; its inner `<img>` drifts within the
  frame with a slight overscale (the engine sets scale(1.18)). Perfect for gallery/photo frames — gives
  that premium "image floats inside its window" feel. (Ensure the frame has `overflow:hidden`.)

### Scroll-scrub — `data-scrub` (+ optional shorthands)
Exposes CSS var `--p` (0→1) on the element as it passes the viewport; drive any CSS with it.
Shorthand transforms (centered on mid-pass): `data-scrub-y="80"`, `data-scrub-x="60"`,
`data-scrub-rotate="8"`, `data-scrub-scale="0.1"`, `data-scrub-opacity`. Combine for marquee strips,
big background type, decorative marks drifting, etc. Use for ONE or two accents per section, not everything.

### Hover tilt — `data-tilt` (+ `data-tilt-max="8"`)
Subtle 3D tilt toward cursor (fine-pointer only, auto-disabled on touch/reduced-motion). Good on cards,
product tiles, framed photos, the map.

### Magnetic buttons
Auto-applied to `.btn--primary`. Add `data-magnetic` to any other `.btn` to opt-in, or
`data-magnetic="false"` to opt-out.

### Count-up — `data-count="500"` (+ `data-count-suffix="+"`, `data-count-prefix`, `data-count-duration`)
Already used in stats. Use for any number stat.

### Marquee — `<div class="marquee" data-marquee="0.4"><div class="marquee__track">…</div></div>`
Continuous loop, velocity-nudged. `data-direction="right"` to reverse.

## Section CSS you SHOULD add (hover micro-interactions & ambient)
- Card/tile HOVER: lift (`transform:translateY(-6px)`), border/colour shift, image zoom, icon nudge,
  an accent bar growing, shadow deepen. Use `transition: … var(--ease)`.
- Link underlines that wipe in, button arrow nudges (`.btn:hover .arr`), CTA shine.
- Ambient loops via `@keyframes` (PREFIXED): a slow floating sticker, a rotating sun/seal, a pulsing
  dot, a drifting wave — keep subtle, wrap in `@media (prefers-reduced-motion:no-preference)`.
- Animated SVG accents (e.g. stroke-dash draw-on with `data-reveal` toggling a class) welcome.

## RESTRAINT (the brand veto is "too busy")
- 3-6 deliberate beats per section. One hero/entrance beat + scroll beat(s) + hover details.
- Don't animate every single element; choose focal points. Stagger groups instead of N independent reveals.
- Keep durations .5–.9s, easing `var(--ease)`. No bounce/spin overload. No layout-shifting animations
  (transform/opacity/filter/clip-path only — never animate width/height/top/left).

## Verify (required)
1. `python3 build.py` (from site/ dir) — assembles index.html.
2. Screenshot your section at desktop+mobile in static mode (final state) and READ them — confirm nothing
   is broken/clipped/invisible and the layout is intact:
   `node shot.js desktop chk_<sec> '#<id>'` and `node shot.js mobile chk_<sec> '#<id>'` then read the PNGs.
   (Static mode forces final state, so this proves your final styles are correct. The engine drives the timing.)
3. If you used `data-split`, double-check the element was plain text and still reads correctly.
Delete your chk_ PNGs when done. Keep edits surgical; don't break existing content/links.
