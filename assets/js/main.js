/* Skill360 — animations de page (GSAP 3 + ScrollTrigger + SplitText) */
(function () {
  'use strict';

  gsap.registerPlugin(ScrollTrigger, MorphSVGPlugin, DrawSVGPlugin, SplitText);

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hero = document.querySelector('.hero');
  var logo = document.querySelector('.hero .lg');
  var nav = document.getElementById('nav');

  /* ------------------------------------------------------------------
     1. Landing : animation du logo puis révélation de l'interface
     ------------------------------------------------------------------ */
  var uiShown = false;
  function showUI(instant) {
    if (uiShown) return;
    uiShown = true;
    hero.classList.add('is-done');
    var items = [nav, '.hero__promise', '.hero__lead', '.hero__ctas', '.hero__scroll'];
    if (instant) { gsap.set(items, { opacity: 1 }); return; }
    gsap.timeline({ defaults: { ease: 'power3.out' } })
      .to(nav, { opacity: 1, duration: 0.9 }, 0)
      .fromTo('.hero__promise', { opacity: 0, y: 28, filter: 'blur(10px)' },
        { opacity: 1, y: 0, filter: 'blur(0px)', duration: 1.1, clearProps: 'filter' }, 0.05)
      .fromTo('.hero__lead', { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.9 }, 0.22)
      .fromTo('.hero__ctas', { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.9 }, 0.34)
      .fromTo('.hero__scroll', { opacity: 0 }, { opacity: 1, duration: 1.2 }, 0.7);
  }

  var intro = null;
  if (logo && window.Skill360) {
    Skill360.fitLogoStroke(logo);
    window.addEventListener('resize', function () { Skill360.fitLogoStroke(logo); });
    intro = Skill360.createLogoIntro(logo, {
      paused: reduce,
      onReveal: function () { showUI(false); }
    });
    if (reduce) {
      intro.progress(1, true);
      showUI(true);
    }
    window.__skill360Intro = intro; // pratique pour la recette (pause, seek…)
  } else {
    showUI(true);
  }

  var skipBtn = document.querySelector('.hero__skip');
  var replayBtn = document.querySelector('.hero__replay');
  if (skipBtn) skipBtn.addEventListener('click', function () {
    if (intro) intro.progress(1);
    showUI(false);
  });
  if (replayBtn) replayBtn.addEventListener('click', function () {
    if (intro) intro.restart();
  });

  /* ------------------------------------------------------------------
     2. Fond de la landing : ciel, halos, anneaux d'orbite
     ------------------------------------------------------------------ */
  (function starfield() {
    var canvas = document.querySelector('.hero__stars');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = 0, h = 0, stars = [], visible = true;

    function resize() {
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round((w * h) / 7000);
      stars = [];
      for (var i = 0; i < n; i++) {
        stars.push({
          x: Math.random() * w, y: Math.random() * h,
          r: Math.random() * 1.05 + 0.25,
          a: Math.random() * 0.55 + 0.12,
          s: Math.random() * 1.6 + 0.4,
          p: Math.random() * Math.PI * 2,
          c: Math.random() < 0.18 ? '#6FE0FF' : '#EEF2FA'
        });
      }
      draw(0);
    }
    function draw(t) {
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        ctx.globalAlpha = s.a * (0.6 + 0.4 * Math.sin(t * s.s + s.p));
        ctx.fillStyle = s.c;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, 6.2832);
        ctx.fill();
      }
    }
    resize();
    window.addEventListener('resize', resize);
    if (reduce) return;
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(hero);
    }
    gsap.ticker.add(function (time) { if (visible) draw(time); });
  })();

  if (!reduce) {
    gsap.set(['.hero__smoke', '.hero__rings'], { xPercent: -50, yPercent: -50, x: 0, y: 0 });
    gsap.to('.ring--1', { rotation: 360, svgOrigin: '0 0', duration: 70, ease: 'none', repeat: -1 });
    gsap.to('.ring--2', { rotation: -360, svgOrigin: '0 0', duration: 110, ease: 'none', repeat: -1 });
    gsap.to('.ring--3', { rotation: 360, svgOrigin: '0 0', duration: 150, ease: 'none', repeat: -1 });
    gsap.to('.hero__smoke', { rotation: 360, duration: 80, ease: 'none', repeat: -1 });
    gsap.to('.hero__glow--a', { x: '6vw', y: '-5vh', duration: 9, ease: 'sine.inOut', yoyo: true, repeat: -1 });
    gsap.to('.hero__glow--b', { x: '-9vw', y: '6vh', scale: 1.25, duration: 11, ease: 'sine.inOut', yoyo: true, repeat: -1 });

    // parallaxe légère à la souris
    if (window.matchMedia('(pointer: fine)').matches) {
      var rx = gsap.quickTo('.hero__rings', 'x', { duration: 1.4, ease: 'power3.out' });
      var ry = gsap.quickTo('.hero__rings', 'y', { duration: 1.4, ease: 'power3.out' });
      var sx = gsap.quickTo('.hero__smoke', 'x', { duration: 2, ease: 'power3.out' });
      var sy = gsap.quickTo('.hero__smoke', 'y', { duration: 2, ease: 'power3.out' });
      hero.addEventListener('pointermove', function (e) {
        var nx = e.clientX / window.innerWidth - 0.5, ny = e.clientY / window.innerHeight - 0.5;
        rx(nx * -30); ry(ny * -30); sx(nx * 18); sy(ny * 18);
      });
    }

    // la landing s'éloigne au scroll
    gsap.to('.hero__inner', {
      yPercent: -14, opacity: 0.15, ease: 'none',
      scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true }
    });
  }

  /* ------------------------------------------------------------------
     3. Navigation
     ------------------------------------------------------------------ */
  var burger = document.querySelector('.nav__burger');
  function closeMenu() { nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', 'false'); }
  burger.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.querySelectorAll('.nav__menu a').forEach(function (a) { a.addEventListener('click', closeMenu); });

  ScrollTrigger.create({
    start: 0, end: 'max',
    onUpdate: function (self) {
      var y = self.scroll();
      nav.classList.toggle('is-solid', y > 60);
      if (nav.classList.contains('is-open')) return;
      if (self.direction === 1 && y > window.innerHeight * 0.9) nav.classList.add('is-hidden');
      else if (self.direction === -1) nav.classList.remove('is-hidden');
    }
  });
  document.querySelectorAll('.nav__menu ul a').forEach(function (link) {
    var section = document.querySelector(link.getAttribute('href'));
    if (!section) return;
    ScrollTrigger.create({
      trigger: section, start: 'top 55%', end: 'bottom 55%',
      onToggle: function (self) { link.classList.toggle('is-active', self.isActive); }
    });
  });

  if (reduce) { bindForm(); return; }

  /* ------------------------------------------------------------------
     4. Manifeste : les mots s'allument au fil du scroll
     ------------------------------------------------------------------ */
  var manifesto = SplitText.create('.manifesto__text', { type: 'words', wordsClass: 'word' });
  gsap.fromTo(manifesto.words, { opacity: 0.14 }, {
    opacity: 1, stagger: 0.1, ease: 'none',
    scrollTrigger: { trigger: '.manifesto__text', start: 'top 82%', end: 'bottom 40%', scrub: true }
  });

  /* ------------------------------------------------------------------
     5. Les trois dimensions : l'Orbite s'éclaire segment par segment
     ------------------------------------------------------------------ */
  var dims = gsap.utils.toArray('.dim');
  var dimSegs = gsap.utils.toArray('.dim-seg');
  var dimLabels = gsap.utils.toArray('.dim-label');
  var progressRing = document.querySelector('.dim-progress');
  var dimOrbit = document.querySelector('.dim-orbit');
  var current = -1;

  function activate(i) {
    if (i === current) return;
    current = i;
    var seg = dims[i].getAttribute('data-seg');
    dims.forEach(function (d, k) { d.classList.toggle('is-active', k === i); });
    dimLabels.forEach(function (l) { l.classList.toggle('is-active', l.getAttribute('data-seg') === seg); });
    dimSegs.forEach(function (s) {
      var on = s.getAttribute('data-seg') === seg;
      var a = (+s.getAttribute('data-mid')) * Math.PI / 180;
      gsap.to(s, {
        opacity: on ? 1 : 0.2,
        x: on ? Math.sin(a) * 34 : 0, y: on ? -Math.cos(a) * 34 : 0,
        duration: 0.7, ease: 'power3.out', overwrite: 'auto'
      });
    });
  }

  if (dimOrbit) {
    var bb = dimOrbit.viewBox.baseVal;
    var center = (bb.x + bb.width / 2) + ' ' + (bb.y + bb.height / 2);
    gsap.to('.dim-ring', { rotation: 360, svgOrigin: center, duration: 60, ease: 'none', repeat: -1 });
    gsap.set(progressRing, { drawSVG: '0%' });
    gsap.set('.dim-segs', { svgOrigin: center });
  }

  var mm = gsap.matchMedia();
  mm.add('(min-width: 901px)', function () {
    activate(0);
    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: '.dimensions', start: 'top top', end: '+=200%', pin: true, scrub: 0.6,
        onUpdate: function (self) { activate(Math.min(2, Math.floor(self.progress * 3 * 0.999))); }
      }
    });
    tl.to(progressRing, { drawSVG: '100%', ease: 'none', duration: 1 }, 0)
      .fromTo('.dim-segs', { rotation: -20, svgOrigin: center }, { rotation: 20, svgOrigin: center, ease: 'none', duration: 1 }, 0);
    return function () { current = -1; };
  });
  mm.add('(max-width: 900px)', function () {
    activate(0);
    dims.forEach(function (d, i) {
      ScrollTrigger.create({ trigger: d, start: 'top 65%', end: 'bottom 35%', onToggle: function (self) { if (self.isActive) activate(i); } });
    });
    gsap.to(progressRing, { drawSVG: '100%', ease: 'none', scrollTrigger: { trigger: '.dims', start: 'top 70%', end: 'bottom 40%', scrub: true } });
    return function () { current = -1; };
  });

  /* ------------------------------------------------------------------
     6. Apparitions au scroll
     ------------------------------------------------------------------ */
  function reveal(selector, opts) {
    var els = gsap.utils.toArray(selector);
    if (!els.length) return;
    gsap.set(els, { opacity: 0, y: (opts && opts.y) || 40 });
    ScrollTrigger.batch(els, {
      start: 'top 88%', once: true,
      onEnter: function (batch) {
        gsap.to(batch, { opacity: 1, y: 0, duration: 1, ease: 'power3.out', stagger: (opts && opts.stagger) || 0.09, overwrite: true });
      }
    });
  }
  reveal('.section-head > *', { y: 30, stagger: 0.08 });
  reveal('.dimensions__content > .eyebrow, .dimensions__content > .h2, .dimensions__intro', { y: 30 });
  reveal('.card');
  reveal('.format');
  reveal('.audience', { y: 30 });
  reveal('.fund', { y: 30 });
  reveal('.form', { y: 50 });
  reveal('.footer__grid > *', { y: 24 });

  /* ------------------------------------------------------------------
     7. Méthode : la ligne se trace, les étapes s'allument
     ------------------------------------------------------------------ */
  var steps = gsap.utils.toArray('.step');
  gsap.set('.method__line-fg', { drawSVG: '0%' });
  reveal('.step', { y: 40, stagger: 0.12 });
  gsap.to('.method__line-fg', {
    drawSVG: '100%', ease: 'none',
    scrollTrigger: {
      trigger: '.method__track', start: 'top 72%', end: 'bottom 60%', scrub: 0.6,
      onUpdate: function (self) {
        steps.forEach(function (s, i) { s.classList.toggle('is-active', self.progress >= i / 3 - 0.02); });
      }
    }
  });

  /* ------------------------------------------------------------------
     8. Valeurs : défilement continu, accéléré par la vitesse de scroll
     ------------------------------------------------------------------ */
  var track = document.querySelector('.values__track');
  if (track) {
    var row = track.querySelector('.values__row');
    var clone = row.cloneNode(true);
    clone.setAttribute('aria-hidden', 'true');
    track.appendChild(clone);
    var loop = gsap.to(track, { xPercent: -50, ease: 'none', duration: 32, repeat: -1 });
    var speed = { v: 1 };
    ScrollTrigger.create({
      trigger: '.values', start: 'top bottom', end: 'bottom top',
      onUpdate: function (self) {
        var v = self.getVelocity() / 300;
        var target = gsap.utils.clamp(-6, 6, 1 + v);
        gsap.to(speed, {
          v: target, duration: 0.25, overwrite: true,
          onUpdate: function () { loop.timeScale(speed.v); },
          onComplete: function () { gsap.to(speed, { v: 1, duration: 1.2, ease: 'power2.out', onUpdate: function () { loop.timeScale(speed.v); } }); }
        });
      }
    });
  }

  gsap.to('.contact__decor .mini-orbit', { rotation: 360, duration: 70, ease: 'none', repeat: -1 });

  bindForm();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ScrollTrigger.refresh(); });

  /* ------------------------------------------------------------------
     9. Formulaire (front uniquement : brancher l'envoi sur le back-office)
     ------------------------------------------------------------------ */
  function bindForm() {
    var form = document.getElementById('contact-form');
    if (!form) return;
    var status = form.querySelector('.form__status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll('[required]').forEach(function (f) {
        var valid = f.type === 'checkbox' ? f.checked : f.value.trim() !== '' && (f.type !== 'email' || /.+@.+\..+/.test(f.value));
        var wrap = f.closest('.field') || f.closest('.check');
        if (wrap) wrap.classList.toggle('is-invalid', !valid);
        if (!valid) ok = false;
      });
      if (!ok) {
        status.textContent = 'Merci de compléter les champs indiqués.';
        return;
      }
      // TODO : envoyer les données (API, service e-mail ou CRM)
      form.reset();
      form.classList.add('is-sent');
      status.textContent = 'Merci ! Votre demande est bien partie en orbite : un conseiller vous recontacte très vite.';
    });
  }
})();
