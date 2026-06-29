/* ============================================================
   TUK & TIDE SURF CLUB — site.js (MOTION engine)
   Dependency-light vanilla JS. Smooth scroll (Lenis), reveals,
   nav, marquee, parallax, magnetic buttons, count-up.
   Every selector is guarded — sections load independently and
   any element may be absent. No build step, no console errors.
   ============================================================ */
(function () {
  'use strict';

  var doc = document;
  var html = doc.documentElement;
  var win = window;

  var REDUCED = win.matchMedia && win.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FINE_POINTER = win.matchMedia && win.matchMedia('(pointer: fine)').matches;
  var IS_STATIC = html.classList.contains('is-static') ||
    /(?:\?|&)static\b/.test(win.location.search);

  // Mark JS as available so the CSS reveal/initial-hidden states engage.
  html.classList.add('has-js');

  function ready(fn) {
    if (doc.readyState === 'loading') {
      doc.addEventListener('DOMContentLoaded', fn, { once: true });
    } else {
      fn();
    }
  }

  function $(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function $$(sel, ctx) {
    return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel));
  }
  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  /* ----------------------------------------------------------
     1. SMOOTH SCROLL — Lenis
     ---------------------------------------------------------- */
  var lenis = null;
  var scrollVelocity = 0; // px/frame-ish, fed to marquee

  function initLenis() {
    if (REDUCED || IS_STATIC) return;            // honour reduced motion
    if (typeof win.Lenis !== 'function') return; // CDN missing → graceful no-op

    try {
      lenis = new win.Lenis({
        duration: 1.1,
        easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); },
        smoothWheel: true,
        wheelMultiplier: 1,
        touchMultiplier: 1.4
      });
    } catch (e) {
      lenis = null;
      return;
    }

    html.classList.add('lenis');

    lenis.on('scroll', function (e) {
      if (e && typeof e.velocity === 'number') scrollVelocity = e.velocity;
    });

    function raf(time) {
      lenis.raf(time);
      win.requestAnimationFrame(raf);
    }
    win.requestAnimationFrame(raf);

    // Anchor links → smooth scroll through Lenis
    $$('a[href^="#"]').forEach(function (a) {
      var id = a.getAttribute('href');
      if (!id || id === '#' || id.length < 2) return;
      a.addEventListener('click', function (ev) {
        var target = doc.getElementById(id.slice(1));
        if (!target) return;
        ev.preventDefault();
        lenis.scrollTo(target, { offset: -10 });
      });
    });
  }

  function lockScroll(on) {
    if (lenis) { on ? lenis.stop() : lenis.start(); }
    doc.body.style.overflow = on ? 'hidden' : '';
  }

  /* ----------------------------------------------------------
     2. REVEALS — IntersectionObserver + stagger
     ---------------------------------------------------------- */
  function initReveals() {
    var els = $$('[data-reveal]');
    if (!els.length) return;

    // Stagger groups: incremental transition-delay on children.
    $$('[data-reveal-group]').forEach(function (group) {
      var kids = $$('[data-reveal]', group);
      kids.forEach(function (kid, i) {
        kid.style.transitionDelay = (i * 80) + 'ms';
      });
    });

    if (REDUCED || IS_STATIC || !('IntersectionObserver' in win)) {
      els.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px -10% 0px' });

    els.forEach(function (el) { io.observe(el); });

    // safety net: anything already in/above the viewport at load reveals immediately
    var vh0 = win.innerHeight;
    els.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < vh0 * 0.9) el.classList.add('is-in');
    });
  }

  /* ----------------------------------------------------------
     3. NAV — stuck / hide-on-scroll-down + mobile menu
     ---------------------------------------------------------- */
  function initNav() {
    var nav = $('[data-nav]');
    if (!nav) return;

    var hero = doc.getElementById('hero');
    var stuck = false;
    var lastY = win.pageYOffset || 0;
    var ticking = false;

    function threshold() {
      if (hero) {
        var r = hero.getBoundingClientRect();
        return (win.pageYOffset || 0) + r.bottom - 80;
      }
      return win.innerHeight * 0.8;
    }

    function update() {
      ticking = false;
      var y = win.pageYOffset || 0;
      var past = y > threshold();

      if (past !== stuck) {
        stuck = past;
        nav.classList.toggle('is-stuck', stuck);
      }

      if (stuck) {
        var goingDown = y > lastY + 4;
        var goingUp = y < lastY - 4;
        if (goingDown && y > win.innerHeight) {
          nav.classList.add('is-hidden');
        } else if (goingUp) {
          nav.classList.remove('is-hidden');
        }
      } else {
        nav.classList.remove('is-hidden');
      }
      lastY = y;
    }

    function onScroll() {
      if (!ticking) {
        ticking = true;
        win.requestAnimationFrame(update);
      }
    }

    win.addEventListener('scroll', onScroll, { passive: true });
    if (lenis) lenis.on('scroll', onScroll);
    update();

    /* mobile menu */
    var toggle = $('[data-menu-toggle]');
    var menu = $('[data-menu]');

    function setMenu(open) {
      nav.classList.toggle('is-open', open);
      if (menu) menu.classList.toggle('is-open', open);
      if (toggle) toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      lockScroll(open);
    }

    if (toggle) {
      toggle.addEventListener('click', function () {
        setMenu(!nav.classList.contains('is-open'));
      });
    }

    if (menu) {
      $$('a', menu).forEach(function (link) {
        link.addEventListener('click', function () { setMenu(false); });
      });
    }

    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) setMenu(false);
    });
  }

  /* ----------------------------------------------------------
     4. MARQUEE — continuous rAF scroll, velocity-nudged
     ---------------------------------------------------------- */
  function initMarquees() {
    var marquees = $$('[data-marquee]');
    if (!marquees.length) return;

    marquees.forEach(function (marquee) {
      var track = $('.marquee__track', marquee);
      if (!track) return;

      // Duplicate content for a seamless loop (until track is >= 2x viewport).
      var safety = 0;
      while (track.scrollWidth < marquee.offsetWidth * 2 && safety < 8) {
        track.innerHTML += track.innerHTML;
        safety++;
      }

      var base = parseFloat(marquee.getAttribute('data-marquee')) || 0.4; // px/frame
      var dir = marquee.getAttribute('data-direction') === 'right' ? 1 : -1;
      var half = track.scrollWidth / 2 || 1;
      var offset = 0;
      var paused = false;

      marquee.addEventListener('mouseenter', function () { paused = true; });
      marquee.addEventListener('mouseleave', function () { paused = false; });

      if (REDUCED) return; // leave static for reduced motion

      function tick() {
        if (!paused) {
          var velBoost = clamp(Math.abs(scrollVelocity) * 0.03, 0, 6);
          offset += (base + velBoost) * dir;
          if (offset <= -half) offset += half;
          if (offset >= 0) offset -= half;
          track.style.transform = 'translate3d(' + offset + 'px,0,0)';
        }
        win.requestAnimationFrame(tick);
      }
      win.requestAnimationFrame(tick);
    });
  }

  /* ----------------------------------------------------------
     5. HERO PARALLAX — transform-only translateY
     ---------------------------------------------------------- */
  function initParallax() {
    var nodes = $$('[data-parallax]');
    if (!nodes.length || REDUCED || IS_STATIC) return;

    var items = nodes.map(function (el) {
      var speed = parseFloat(el.getAttribute('data-parallax'));
      if (isNaN(speed)) speed = 0.15;
      return { el: el, speed: speed };
    });

    var ticking = false;

    function update() {
      ticking = false;
      var vh = win.innerHeight;
      items.forEach(function (it) {
        var rect = it.el.getBoundingClientRect();
        if (rect.bottom < -vh || rect.top > vh * 2) return; // off-screen skip
        var center = rect.top + rect.height / 2 - vh / 2;
        var shift = -center * it.speed;
        it.el.style.transform = 'translate3d(0,' + shift.toFixed(2) + 'px,0)';
      });
    }

    function onScroll() {
      if (!ticking) {
        ticking = true;
        win.requestAnimationFrame(update);
      }
    }

    win.addEventListener('scroll', onScroll, { passive: true });
    win.addEventListener('resize', onScroll, { passive: true });
    if (lenis) lenis.on('scroll', onScroll);
    update();
  }

  /* ----------------------------------------------------------
     6. MAGNETIC buttons — fine pointer only
     ---------------------------------------------------------- */
  function initMagnetic() {
    if (!FINE_POINTER || REDUCED) return;

    var btns = $$('.btn[data-magnetic]');
    // auto-apply to primary buttons that haven't opted out
    $$('.btn--primary').forEach(function (b) {
      if (!b.hasAttribute('data-magnetic') &&
          b.getAttribute('data-magnetic') !== 'false' &&
          btns.indexOf(b) === -1) {
        btns.push(b);
      }
    });
    if (!btns.length) return;

    var STRENGTH = 0.2;
    var MAX = 10;

    btns.forEach(function (btn) {
      if (btn.getAttribute('data-magnetic') === 'false') return;

      btn.addEventListener('mousemove', function (e) {
        var r = btn.getBoundingClientRect();
        var mx = e.clientX - (r.left + r.width / 2);
        var my = e.clientY - (r.top + r.height / 2);
        var x = clamp(mx * STRENGTH, -MAX, MAX);
        var y = clamp(my * STRENGTH, -MAX, MAX);
        btn.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0)';
      });

      btn.addEventListener('mouseleave', function () {
        btn.style.transform = '';
      });
    });
  }

  /* ----------------------------------------------------------
     7. COUNT-UP — animate 0 → number when revealed
     ---------------------------------------------------------- */
  function initCountUp() {
    var nodes = $$('[data-count]');
    if (!nodes.length) return;

    function parse(el) {
      var raw = el.getAttribute('data-count');
      var num = parseFloat(String(raw).replace(/[^0-9.\-]/g, ''));
      return isNaN(num) ? 0 : num;
    }

    function format(el, value) {
      var target = parse(el);
      var decimals = (String(target).split('.')[1] || '').length;
      var pre = el.getAttribute('data-count-prefix') || '';
      var suf = el.getAttribute('data-count-suffix') || '';
      el.textContent = pre + value.toFixed(decimals) + suf;
    }

    function run(el) {
      var target = parse(el);
      if (REDUCED || IS_STATIC) { format(el, target); return; }
      var dur = parseFloat(el.getAttribute('data-count-duration')) || 1600;
      var start = null;
      function step(ts) {
        if (start === null) start = ts;
        var p = clamp((ts - start) / dur, 0, 1);
        var eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
        format(el, target * eased);
        if (p < 1) win.requestAnimationFrame(step);
        else format(el, target);
      }
      win.requestAnimationFrame(step);
    }

    if (REDUCED || IS_STATIC || !('IntersectionObserver' in win)) {
      nodes.forEach(function (el) { format(el, parse(el)); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          run(entry.target);
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });

    nodes.forEach(function (el) {
      format(el, 0);
      io.observe(el);
    });
  }

  /* ----------------------------------------------------------
     8. SPLIT TEXT — wrap words/chars for staggered reveal
        <h2 data-split="words"> … </h2>  (or "chars")
        Each unit becomes a span that the reveal system staggers.
     ---------------------------------------------------------- */
  function initSplit() {
    var nodes = $$('[data-split]');
    if (!nodes.length) return;

    nodes.forEach(function (el) {
      if (el.getAttribute('data-split-done')) return;
      var mode = el.getAttribute('data-split') || 'words';
      var step = parseInt(el.getAttribute('data-split-stagger'), 10);
      if (isNaN(step)) step = mode === 'chars' ? 26 : 70;
      var text = el.textContent;
      el.setAttribute('aria-label', text);
      el.textContent = '';
      el.setAttribute('data-split-done', '1');

      var units = mode === 'chars' ? text.split('') : text.split(/(\s+)/);
      var idx = 0;
      units.forEach(function (u) {
        if (mode === 'words' && /^\s+$/.test(u)) { el.appendChild(doc.createTextNode(u)); return; }
        if (u === '') return;
        var outer = doc.createElement('span');
        outer.className = 'split-u';
        outer.setAttribute('aria-hidden', 'true');
        var inner = doc.createElement('span');
        inner.className = 'split-i';
        inner.textContent = u;
        outer.appendChild(inner);
        if (!(REDUCED || IS_STATIC)) inner.style.transitionDelay = (idx * step) + 'ms';
        el.appendChild(outer);
        if (mode === 'chars' && u === ' ') {} else idx++;
      });
      el.classList.add('split-ready');
    });

    if (REDUCED || IS_STATIC || !('IntersectionObserver' in win)) {
      nodes.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.2, rootMargin: '0px 0px -10% 0px' });
    nodes.forEach(function (el) { io.observe(el); });
  }

  /* ----------------------------------------------------------
     9. SCROLL SCRUB + extended parallax (shared rAF)
        data-scrub            → exposes CSS var --p (0..1) across viewport pass
        data-scrub-y="80"     → translateY (px) mapped from p-0.5 (centered)
        data-scrub-x="60"     → translateX
        data-scrub-rotate="8" → rotate(deg)
        data-scrub-scale="0.1"→ scale 1±value
        data-scrub-opacity    → fade 0.4→1 around center
        data-parallax-x="0.1" → horizontal parallax (companion to data-parallax)
        data-img-parallax     → inner <img> drifts + slight overscale (place on overflow:hidden frame)
     ---------------------------------------------------------- */
  function initScrub() {
    var scrubEls = $$('[data-scrub],[data-scrub-y],[data-scrub-x],[data-scrub-rotate],[data-scrub-scale],[data-scrub-opacity]');
    var xEls = $$('[data-parallax-x]');
    var imgFrames = $$('[data-img-parallax]');
    if ((!scrubEls.length && !xEls.length && !imgFrames.length) || REDUCED || IS_STATIC) {
      // still set inner img to fill nicely
      imgFrames.forEach(function (f) { var im = $('img', f); if (im) im.style.willChange = ''; });
      return;
    }

    var imgs = imgFrames.map(function (f) {
      var im = $('img', f);
      if (im) { im.style.willChange = 'transform'; im.style.transform = 'scale(1.18)'; }
      return { frame: f, img: im, speed: parseFloat(f.getAttribute('data-img-parallax')) || 0.12 };
    }).filter(function (o) { return o.img; });

    var ticking = false;
    function update() {
      ticking = false;
      var vh = win.innerHeight;

      scrubEls.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -vh * 0.4 || r.top > vh * 1.4) return;
        // p: 0 when element enters bottom, 1 when it exits top
        var p = clamp((vh - r.top) / (vh + r.height), 0, 1);
        var c = p - 0.5; // centered −0.5..0.5
        el.style.setProperty('--p', p.toFixed(4));
        var t = '';
        var y = parseFloat(el.getAttribute('data-scrub-y'));
        if (!isNaN(y)) t += ' translateY(' + (-c * 2 * y).toFixed(2) + 'px)';
        var x = parseFloat(el.getAttribute('data-scrub-x'));
        if (!isNaN(x)) t += ' translateX(' + (-c * 2 * x).toFixed(2) + 'px)';
        var rot = parseFloat(el.getAttribute('data-scrub-rotate'));
        if (!isNaN(rot)) t += ' rotate(' + (c * 2 * rot).toFixed(2) + 'deg)';
        var sc = parseFloat(el.getAttribute('data-scrub-scale'));
        if (!isNaN(sc)) t += ' scale(' + (1 + (0.5 - Math.abs(c)) * 2 * sc).toFixed(3) + ')';
        if (t) el.style.transform = t.trim();
        if (el.hasAttribute('data-scrub-opacity')) {
          el.style.opacity = clamp(1 - Math.abs(c) * 1.4, 0.15, 1).toFixed(3);
        }
      });

      xEls.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -vh || r.top > vh * 2) return;
        var center = r.top + r.height / 2 - vh / 2;
        var sp = parseFloat(el.getAttribute('data-parallax-x')) || 0.1;
        el.style.transform = 'translate3d(' + (-center * sp).toFixed(2) + 'px,0,0)';
      });

      imgs.forEach(function (o) {
        var r = o.frame.getBoundingClientRect();
        if (r.bottom < -vh || r.top > vh * 2) return;
        var center = r.top + r.height / 2 - vh / 2;
        o.img.style.transform = 'translate3d(0,' + (-center * o.speed).toFixed(2) + 'px,0) scale(1.18)';
      });
    }
    function onScroll() {
      if (!ticking) { ticking = true; win.requestAnimationFrame(update); }
    }
    win.addEventListener('scroll', onScroll, { passive: true });
    win.addEventListener('resize', onScroll, { passive: true });
    if (lenis) lenis.on('scroll', onScroll);
    update();
  }

  /* ----------------------------------------------------------
     10. TILT — subtle 3D tilt toward cursor (fine pointer)
         data-tilt           on a card/image
         data-tilt-max="8"   max degrees (default 8)
     ---------------------------------------------------------- */
  function initTilt() {
    if (!FINE_POINTER || REDUCED) return;
    $$('[data-tilt]').forEach(function (el) {
      var max = parseFloat(el.getAttribute('data-tilt-max')) || 8;
      el.style.transformStyle = 'preserve-3d';
      el.style.transition = 'transform .3s var(--ease)';
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        el.style.transition = 'transform .08s linear';
        el.style.transform = 'perspective(800px) rotateX(' + (-py * max).toFixed(2) +
          'deg) rotateY(' + (px * max).toFixed(2) + 'deg)';
      });
      el.addEventListener('mouseleave', function () {
        el.style.transition = 'transform .5s var(--ease)';
        el.style.transform = '';
      });
    });
  }

  /* ----------------------------------------------------------
     boot
     ---------------------------------------------------------- */
  ready(function () {
    initLenis();      // must precede nav/parallax/marquee (they hook lenis.scroll)
    initSplit();      // before reveals so split units get observed too
    initReveals();
    initNav();
    initMarquees();
    initParallax();
    initScrub();
    initTilt();
    initMagnetic();
    initCountUp();
  });
})();
