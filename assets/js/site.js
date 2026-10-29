/* ==========================================================================
   Skill360 — interactions
   Aucune dépendance. Chaque module est isolé : une erreur dans l'un
   n'empêche pas les autres de fonctionner.
   ========================================================================== */
(() => {
  'use strict';
  window.__s360 = true;

  // URL du service qui reçoit les demandes de contact (Formspree, API maison…).
  // Laisser vide = mode démo : le formulaire affiche la confirmation sans rien envoyer.
  const CONTACT_ENDPOINT = '';

  const doc = document.documentElement;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const easeInOut = t => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const pad = n => String(n).padStart(2, '0');
  const norm = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const icon = (id, cls = 'i') => `<svg class="${cls}" aria-hidden="true"><use href="#i-${id}"></use></svg>`;

  doc.classList.add('js');

  function run(name, fn) {
    try { fn(); } catch (err) { console.error(`[Skill360] ${name}`, err); }
  }

  function tween({ duration = 900, easing = easeInOut, onUpdate, onDone }) {
    if (reduceMotion) { onUpdate(1); onDone && onDone(); return () => {}; }
    let raf, start;
    const step = now => {
      if (start === undefined) start = now;
      const t = clamp((now - start) / duration, 0, 1);
      onUpdate(easing(t));
      if (t < 1) raf = requestAnimationFrame(step);
      else if (onDone) onDone();
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }

  function whenVisible(el, cb, { once = true, margin = '0px 0px -12% 0px' } = {}) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (once) {
          if (e.isIntersecting) { cb(true); io.disconnect(); }
        } else cb(e.isIntersecting);
      });
    }, { rootMargin: margin });
    io.observe(el);
  }

  /* ---------- Année du pied de page ---------- */
  run('year', () => {
    $$('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
  });

  /* ---------- En-tête, barre de progression, retour en haut ---------- */
  run('header', () => {
    const header = $('.site-header');
    const bar = $('.scroll-progress');
    if (!header) return;
    let lastY = scrollY;
    let ticking = false;
    const update = () => {
      const y = scrollY;
      header.classList.toggle('is-scrolled', y > 8);
      if (!doc.classList.contains('menu-open') && !header.contains(document.activeElement)) {
        header.classList.toggle('is-hidden', y > lastY && y > 320);
      }
      if (y < lastY) header.classList.remove('is-hidden');
      lastY = y;
      if (bar) {
        const max = doc.scrollHeight - innerHeight;
        bar.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
      }
      ticking = false;
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    header.addEventListener('focusin', () => header.classList.remove('is-hidden'));
    update();

    $$('[data-to-top]').forEach(b => b.addEventListener('click', () => scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' })));
  });

  /* ---------- Menu mobile ---------- */
  run('menu', () => {
    const toggle = $('.nav-toggle');
    const menu = $('#menu');
    if (!toggle || !menu) return;
    const setOpen = open => {
      doc.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', open);
      toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    };
    toggle.addEventListener('click', () => setOpen(!doc.classList.contains('menu-open')));
    menu.addEventListener('click', e => { if (e.target.closest('a, button')) setOpen(false); });
    addEventListener('keydown', e => { if (e.key === 'Escape' && doc.classList.contains('menu-open')) { setOpen(false); toggle.focus(); } });
    matchMedia('(min-width: 1081px)').addEventListener('change', e => { if (e.matches) setOpen(false); });
  });

  /* ---------- Titres : apparition mot par mot ---------- */
  run('split', () => {
    $$('[data-split]').forEach(el => {
      const label = el.textContent.replace(/\s+/g, ' ').trim();
      const nodes = [...el.childNodes];
      el.textContent = '';
      let i = 0;
      let last = null;
      nodes.forEach(node => {
        if (node.nodeType === 3) {
          node.textContent.split(/([ \n\t]+)/).forEach(part => {
            if (!part) return;
            if (/^[ \n\t]+$/.test(part)) { el.append(' '); return; }
            const w = document.createElement('span');
            const inner = document.createElement('span');
            w.className = 'w';
            inner.textContent = part;
            inner.style.setProperty('--i', i++);
            w.append(inner);
            el.append(w);
            last = inner;
          });
        } else {
          (last || el).append(node);
        }
      });
      el.style.setProperty('--n', i);
      el.classList.add('split');
      el.setAttribute('aria-label', label);
      $$('.w', el).forEach(w => w.setAttribute('aria-hidden', 'true'));
      whenVisible(el, () => el.classList.add('is-in'));
    });
  });

  /* ---------- Apparitions au scroll ---------- */
  run('reveal', () => {
    $$('[data-stagger]').forEach(parent => {
      const step = Number(parent.dataset.stagger) || 90;
      [...parent.children].forEach((child, i) => {
        if (!child.hasAttribute('data-reveal')) child.setAttribute('data-reveal', '');
        child.style.setProperty('--d', `${i * step}ms`);
      });
    });
    // Une fois l'entrée terminée, on retire data-reveal pour rendre la main
    // aux transitions propres au composant (survol des cartes, etc.).
    const settle = el => {
      if (!el.hasAttribute('data-reveal')) return;
      const delay = parseFloat(getComputedStyle(el).transitionDelay) || 0;
      setTimeout(() => {
        el.removeAttribute('data-reveal');
        el.style.removeProperty('--d');
      }, delay * 1000 + 1600);
    };
    $$('[data-reveal], .bar, [data-inview]').forEach(el => whenVisible(el, () => {
      el.classList.add('is-in');
      settle(el);
    }));
  });

  /* ---------- Chiffres qui défilent ---------- */
  run('scramble', () => {
    $$('[data-scramble]').forEach(el => {
      const final = el.textContent;
      if (reduceMotion) return;
      whenVisible(el, () => {
        const duration = 1100;
        const start = performance.now();
        const frame = now => {
          const p = clamp((now - start) / duration, 0, 1);
          const settled = Math.floor(p * final.length);
          el.textContent = [...final].map((ch, i) => (i < settled || !/[0-9A-Za-zÀ-ÿ]/.test(ch) ? ch : String(Math.floor(Math.random() * 10)))).join('');
          if (p < 1) requestAnimationFrame(frame);
          else el.textContent = final;
        };
        requestAnimationFrame(frame);
      });
    });
  });

  /* ---------- Boutons magnétiques ---------- */
  run('magnetic', () => {
    if (!finePointer || reduceMotion) return;
    $$('[data-magnetic]').forEach(el => {
      el.addEventListener('pointermove', e => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * .22;
        const y = (e.clientY - r.top - r.height / 2) * .35;
        el.style.translate = `${x}px ${y}px`;
      });
      el.addEventListener('pointerleave', () => { el.style.translate = ''; });
    });
  });

  /* ---------- Halo qui suit la souris sur les panneaux sombres ---------- */
  run('glow', () => {
    if (!finePointer) return;
    $$('.panel-dark, .cta__media').forEach(el => {
      el.addEventListener('pointermove', e => {
        const r = el.getBoundingClientRect();
        el.style.setProperty('--mx', `${e.clientX - r.left}px`);
        el.style.setProperty('--my', `${e.clientY - r.top}px`);
      });
    });
  });

  /* ---------- Parallaxe du visuel d'accueil ---------- */
  run('parallax', () => {
    const scene = $('[data-tilt-scene]');
    if (!scene || !finePointer || reduceMotion) return;
    const layers = $$('[data-depth]', scene);
    let tx = 0, ty = 0, cx = 0, cy = 0, raf = 0;
    const loop = () => {
      cx = lerp(cx, tx, .07);
      cy = lerp(cy, ty, .07);
      layers.forEach(l => {
        const d = Number(l.dataset.depth);
        l.style.translate = `${(cx * d).toFixed(2)}px ${(cy * d).toFixed(2)}px`;
      });
      raf = Math.abs(cx - tx) + Math.abs(cy - ty) > .0005 ? requestAnimationFrame(loop) : 0;
    };
    addEventListener('pointermove', e => {
      tx = e.clientX / innerWidth - .5;
      ty = e.clientY / innerHeight - .5;
      if (!raf) raf = requestAnimationFrame(loop);
    }, { passive: true });
  });

  /* ---------- Radars de compétences ---------- */
  const RADAR = { cx: 120, cy: 120, r: 90 };
  const radarXY = (v, i) => {
    const a = (-90 + i * 60) * Math.PI / 180;
    return [RADAR.cx + Math.cos(a) * RADAR.r * v, RADAR.cy + Math.sin(a) * RADAR.r * v];
  };
  const radarPoints = vals => vals.map((v, i) => radarXY(v, i).map(n => n.toFixed(2)).join(',')).join(' ');
  const parseVals = s => s.split(',').map(Number);

  class Radar {
    constructor(svg) {
      this.svg = svg;
      this.now = $('[data-radar-now]', svg);
      this.goal = $('[data-radar-goal]', svg);
      this.values = svg.dataset.now ? parseVals(svg.dataset.now) : new Array(6).fill(0);
      this.current = this.values.slice();
      this.dots = this.values.map(() => {
        const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        c.setAttribute('r', '3.6');
        c.setAttribute('class', 'radar__dot');
        svg.append(c);
        return c;
      });
      this.cancel = () => {};
    }
    draw(vals) {
      this.current = vals;
      this.now.setAttribute('points', radarPoints(vals));
      vals.forEach((v, i) => {
        const [x, y] = radarXY(v, i);
        this.dots[i].setAttribute('cx', x.toFixed(2));
        this.dots[i].setAttribute('cy', y.toFixed(2));
      });
    }
    to(target, duration = 1100) {
      this.cancel();
      const from = this.current.slice();
      return new Promise(resolve => {
        this.cancel = tween({ duration, onUpdate: t => this.draw(from.map((f, i) => lerp(f, target[i], t))), onDone: resolve });
      });
    }
    setGoal(vals) { if (this.goal) this.goal.setAttribute('points', radarPoints(vals)); }
  }

  run('radars', () => {
    $$('svg[data-radar]').forEach(svg => {
      const radar = new Radar(svg);
      const mode = svg.dataset.radar;
      const goalVals = svg.dataset.goal ? parseVals(svg.dataset.goal) : null;
      radar.draw(new Array(6).fill(0.05));
      whenVisible(svg, async () => {
        svg.classList.add('is-in');
        await radar.to(radar.values, 1400);
        if (mode === 'loop' && goalVals && !reduceMotion) {
          const pts = svg.closest('.radar-card')?.querySelector('.pts');
          if (pts) pts.textContent = 'AVANT';
          const cycle = async () => {
            await new Promise(r => setTimeout(r, 1600));
            if (pts) { pts.textContent = '+12 PTS'; pts.classList.add('is-up'); }
            await radar.to(goalVals, 1300);
            await new Promise(r => setTimeout(r, 2200));
            if (pts) { pts.textContent = 'AVANT'; pts.classList.remove('is-up'); }
            await radar.to(radar.values, 1300);
            cycle();
          };
          cycle();
        }
      });
      if (mode === 'toggle' && goalVals) {
        const group = svg.closest('.skills')?.querySelector('.seg');
        group && group.addEventListener('click', e => {
          const btn = e.target.closest('button[data-show]');
          if (!btn) return;
          $$('button', group).forEach(b => b.setAttribute('aria-pressed', b === btn));
          radar.to(btn.dataset.show === 'goal' ? goalVals : radar.values, 1000);
        });
      }
    });
  });

  /* ---------- Badge « compétence validée » ---------- */
  run('badge', () => {
    const el = $('[data-skills]');
    if (!el || reduceMotion) return;
    const skills = el.dataset.skills.split('|');
    const check = el.closest('.badge-card')?.querySelector('.chip-check');
    let i = 0;
    setInterval(() => {
      if (document.hidden) return;
      i = (i + 1) % skills.length;
      el.animate([{ transform: 'none', opacity: 1 }, { transform: 'translateY(-100%)', opacity: 0 }], { duration: 260, easing: 'ease-in' }).onfinish = () => {
        el.textContent = skills[i];
        el.animate([{ transform: 'translateY(100%)', opacity: 0 }, { transform: 'none', opacity: 1 }], { duration: 420, easing: 'cubic-bezier(.22,1,.36,1)' });
        if (check) { check.classList.remove('is-pulse'); void check.offsetWidth; check.classList.add('is-pulse'); }
      };
    }, 3200);
  });

  /* ---------- Anneau de progression ---------- */
  run('rings', () => {
    $$('[data-ring]').forEach(circle => {
      const target = Number(circle.dataset.ring) / 100;
      const label = circle.closest('.aud__widget')?.querySelector('[data-ring-label]');
      const c = 2 * Math.PI * Number(circle.getAttribute('r'));
      circle.setAttribute('stroke-dasharray', `0 ${c}`);
      whenVisible(circle, () => tween({
        duration: 1600,
        onUpdate: t => {
          circle.setAttribute('stroke-dasharray', `${(c * target * t).toFixed(1)} ${c}`);
          if (label) label.textContent = `${Math.round(target * 100 * t)} %`;
        }
      }));
    });
  });

  /* ---------- Méthode 360 : étapes ---------- */
  run('steps', () => {
    const root = $('[data-steps]');
    if (!root) return;
    const items = $$('.step', root);
    const fill = $('.steps__fill', root);
    const track = $('.steps__track', root);
    const loop = $('.loop');
    const vertical = matchMedia('(max-width: 560px)');
    let active = -1, timer = 0, visible = false, paused = false;

    const place = () => {
      if (active < 0) return;
      const tr = track.getBoundingClientRect();
      const c = $('.step__num', items[active]).getBoundingClientRect();
      if (getComputedStyle(track).display === 'none') return;
      if (vertical.matches) fill.style.transform = `scaleY(${clamp((c.top + c.height / 2 - tr.top) / tr.height, 0, 1)})`;
      else fill.style.transform = `scaleX(${clamp((c.left + c.width / 2 - tr.left) / tr.width, 0, 1)})`;
    };
    const set = i => {
      active = i;
      items.forEach((s, k) => {
        s.classList.toggle('is-active', k === i);
        s.classList.toggle('is-done', k < i);
        $('.step__num', s).setAttribute('aria-pressed', k === i);
      });
      place();
    };
    const next = () => {
      if (active === items.length - 1) {
        loop && loop.classList.add('is-looping');
        setTimeout(() => { loop && loop.classList.remove('is-looping'); set(0); }, 1300);
      } else set(active + 1);
    };
    const schedule = () => {
      clearInterval(timer);
      if (visible && !paused && !reduceMotion) timer = setInterval(next, 2800);
    };
    items.forEach((s, k) => {
      s.addEventListener('click', () => { set(k); schedule(); });
      s.addEventListener('pointerenter', () => { paused = true; set(k); schedule(); });
      s.addEventListener('pointerleave', () => { paused = false; schedule(); });
    });
    root.addEventListener('focusin', () => { paused = true; schedule(); });
    root.addEventListener('focusout', () => { paused = false; schedule(); });
    whenVisible(root, v => {
      visible = v;
      if (v && active < 0) setTimeout(() => set(0), 300);
      schedule();
    }, { once: false, margin: '0px 0px -20% 0px' });
    addEventListener('resize', place);
  });

  /* ---------- Aperçu image qui suit le curseur ---------- */
  run('preview', () => {
    const list = $('[data-preview-list]');
    if (!list || !finePointer || reduceMotion) return;
    const rows = $$('[data-preview]', list);
    const box = document.createElement('div');
    box.className = 'cursor-preview';
    box.setAttribute('aria-hidden', 'true');
    const imgs = rows.map(r => {
      const img = new Image();
      img.src = r.dataset.preview;
      img.alt = '';
      box.append(img);
      return img;
    });
    document.body.append(box);
    let x = 0, y = 0, tx = 0, ty = 0, vis = 0, tvis = 0, raf = 0, fresh = true;
    const loop = () => {
      x = lerp(x, tx, .16);
      y = lerp(y, ty, .16);
      vis = lerp(vis, tvis, .14);
      const rot = clamp((tx - x) * .06, -10, 10);
      box.style.transform = `translate3d(${x + 28}px, ${y - 98}px, 0) rotate(${rot}deg) scale(${.7 + .3 * vis})`;
      box.style.opacity = vis.toFixed(3);
      raf = (Math.abs(tx - x) + Math.abs(ty - y) + Math.abs(tvis - vis) > .05) ? requestAnimationFrame(loop) : 0;
    };
    const kick = () => { if (!raf) raf = requestAnimationFrame(loop); };
    list.addEventListener('pointermove', e => {
      tx = e.clientX; ty = e.clientY;
      if (fresh) { x = tx; y = ty; fresh = false; }
      kick();
    });
    rows.forEach((r, i) => r.addEventListener('pointerenter', () => {
      tvis = 1;
      imgs.forEach((im, k) => im.classList.toggle('is-on', k === i));
      kick();
    }));
    list.addEventListener('pointerleave', () => { tvis = 0; fresh = true; kick(); });
  });

  /* ---------- Carrousel de témoignages ---------- */
  run('carousel', () => {
    const root = $('[data-carousel]');
    if (!root) return;
    const slides = $$('.testi__slide', root);
    const authors = $$('.testi__author', root);
    const count = $('[data-count]', root);
    const prog = $('.testi__progress', root);
    const n = slides.length;
    const DURATION = 7000;
    let idx = 0;

    const restart = () => {
      if (reduceMotion || !prog) return;
      prog.classList.remove('run');
      void prog.offsetWidth;
      prog.style.animationDuration = `${DURATION}ms`;
      prog.classList.add('run');
    };
    const go = i => {
      idx = (i + n) % n;
      slides.forEach((s, k) => { s.classList.toggle('is-active', k === idx); s.setAttribute('aria-hidden', k !== idx); });
      authors.forEach((a, k) => a.classList.toggle('is-active', k === idx));
      if (count) count.textContent = `${pad(idx + 1)} / ${pad(n)}`;
      restart();
    };
    $('[data-prev]', root).addEventListener('click', () => go(idx - 1));
    $('[data-next]', root).addEventListener('click', () => go(idx + 1));
    prog && prog.addEventListener('animationend', () => go(idx + 1));
    const setPlay = state => { if (prog) prog.style.animationPlayState = state; };
    root.addEventListener('pointerenter', () => setPlay('paused'));
    root.addEventListener('pointerleave', () => setPlay('running'));
    root.addEventListener('focusin', () => setPlay('paused'));
    root.addEventListener('focusout', () => setPlay('running'));
    whenVisible(root, v => setPlay(v ? 'running' : 'paused'), { once: false });

    let startX = null;
    root.addEventListener('pointerdown', e => { startX = e.clientX; });
    root.addEventListener('pointerup', e => {
      if (startX === null) return;
      const dx = e.clientX - startX;
      if (Math.abs(dx) > 50) go(idx + (dx < 0 ? 1 : -1));
      startX = null;
    });
    go(0);
    setPlay('paused');
  });

  /* ---------- Rails horizontaux ---------- */
  run('rails', () => {
    $$('[data-rail]').forEach(root => {
      const rail = $('.rail', root);
      const prev = $('[data-rail-prev]', root);
      const next = $('[data-rail-next]', root);
      if (!rail) return;
      const step = () => (rail.firstElementChild?.getBoundingClientRect().width || 300) + 20;
      const update = () => {
        if (prev) prev.disabled = rail.scrollLeft < 4;
        if (next) next.disabled = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 4;
      };
      prev && prev.addEventListener('click', () => rail.scrollBy({ left: -step(), behavior: 'smooth' }));
      next && next.addEventListener('click', () => rail.scrollBy({ left: step(), behavior: 'smooth' }));
      rail.addEventListener('scroll', update, { passive: true });
      addEventListener('resize', update);
      update();
    });
  });

  /* ---------- Catalogue (données de recherche) ---------- */
  const FICHE = 'fiche-manager-equipe.html';
  const CATALOG = [
    { t: 'Manager une équipe au quotidien', c: 'Management', f: ['Présentiel'], d: '3 jours' },
    { t: 'Prendre son premier poste de manager', c: 'Management', f: ['Hybride'], d: '4 jours' },
    { t: 'Manager une équipe à distance', c: 'Management', f: ['Distanciel'], d: '2 jours' },
    { t: 'Conduire les entretiens annuels', c: 'Management', f: ['Présentiel'], d: '1 jour' },
    { t: 'Gérer les tensions et les conflits', c: 'Management', f: ['Présentiel'], d: '2 jours' },
    { t: 'Accompagner le changement', c: 'Management', f: ['Hybride'], d: '2 jours' },
    { t: 'Prendre la parole en public', c: 'Communication', f: ['Hybride'], d: '2 jours' },
    { t: 'Excel : tableaux croisés et automatisations', c: 'Numérique', f: ['Distanciel'], d: '14 heures' },
    { t: 'Anglais professionnel, niveau intermédiaire', c: 'Langues', f: ['Distanciel'], d: '30 heures' }
  ].map(item => ({ ...item, href: FICHE, key: norm(`${item.t} ${item.c}`) }));

  /* ---------- Recherche avec suggestions ---------- */
  run('search', () => {
    const form = $('[data-search]');
    if (!form) return;
    const input = $('input[type="search"]', form);
    const panel = $('.suggest', form);
    const list = $('.suggest__list', panel);
    const chips = $$('.chip', form);
    let results = [];
    let active = -1;

    const escape = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const highlight = (text, q) => {
      if (!q) return escape(text);
      const i = norm(text).indexOf(norm(q));
      if (i < 0) return escape(text);
      return `${escape(text.slice(0, i))}<mark>${escape(text.slice(i, i + q.length))}</mark>${escape(text.slice(i + q.length))}`;
    };
    const open = state => {
      panel.classList.toggle('is-open', state);
      input.setAttribute('aria-expanded', state);
    };
    const setActive = i => {
      active = i;
      $$('.suggest__item', list).forEach((li, k) => li.classList.toggle('is-active', k === i));
      if (i >= 0) input.setAttribute('aria-activedescendant', `sugg-${i}`);
      else input.removeAttribute('aria-activedescendant');
    };
    const render = () => {
      const q = input.value.trim();
      const formats = chips.filter(c => c.getAttribute('aria-pressed') === 'true').map(c => c.dataset.format);
      const strict = formats.filter(f => f !== 'Intra-entreprise');
      if (!q && !formats.length) { open(false); return; }
      results = CATALOG.filter(item => (!q || item.key.includes(norm(q))) && (!strict.length || item.f.some(f => strict.includes(f))));
      if (!results.length) {
        list.innerHTML = `<li class="suggest__empty">Aucune formation ne correspond. <a href="#" data-open="contact" data-subject="Demande de formation sur-mesure" data-message="Je recherche une formation sur : ${escape(q)}">Demander un sur-mesure</a></li>`;
      } else {
        list.innerHTML = results.map((item, i) => `
          <li class="suggest__item" role="option" id="sugg-${i}">
            <a href="${item.href}"><span class="suggest__title">${highlight(item.t, q)}</span>
            <span class="suggest__meta">${item.c.toUpperCase()} · ${item.d.toUpperCase()} · ${item.f.join(', ').toUpperCase()}</span></a>
          </li>`).join('');
      }
      setActive(-1);
      open(true);
    };
    input.addEventListener('input', render);
    input.addEventListener('focus', () => { if (input.value.trim()) render(); });
    input.addEventListener('keydown', e => {
      const items = $$('.suggest__item', list);
      if (e.key === 'ArrowDown') { e.preventDefault(); if (!panel.classList.contains('is-open')) render(); setActive(Math.min(active + 1, items.length - 1)); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(Math.max(active - 1, -1)); }
      else if (e.key === 'Escape') { open(false); }
      else if (e.key === 'Enter' && active >= 0 && items[active]) { e.preventDefault(); location.href = $('a', items[active]).href; }
    });
    chips.forEach(chip => chip.addEventListener('click', () => {
      chip.setAttribute('aria-pressed', chip.getAttribute('aria-pressed') !== 'true');
      render();
    }));
    form.addEventListener('submit', e => {
      e.preventDefault();
      render();
      const first = $('.suggest__item a', list);
      if (first && panel.classList.contains('is-open')) first.focus();
    });
    document.addEventListener('click', e => { if (!form.contains(e.target)) open(false); });
  });

  /* ---------- Filtres de catégorie ---------- */
  run('filters', () => {
    const root = $('[data-catalog]');
    if (!root) return;
    const form = $('.filters', root);
    const grid = $('.grid-cards', root);
    const cards = $$('.tcard', grid);
    const countEl = $('[data-result-count]', root);
    const sortSel = $('[data-sort]', root);
    const empty = $('.empty', root);
    const toggle = $('.filters-toggle', root);
    const queryChip = $('.active-query', root);
    const LEVELS = { tous: 0, initiation: 1, perfectionnement: 2, expert: 3 };
    let query = new URLSearchParams(location.search).get('q') || '';

    cards.forEach((c, i) => { c.dataset.order = i; c.dataset.text = norm(c.textContent); });
    $$('[data-count-format]', form).forEach(el => {
      el.textContent = cards.filter(c => c.dataset.format === el.dataset.countFormat).length;
    });

    const values = name => $$(`input[name="${name}"]:checked`, form).map(i => i.value);
    const bucket = days => (days <= 1 ? 'court' : days <= 3 ? 'moyen' : 'long');

    const apply = (animate = true) => {
      const fmt = values('format');
      const dur = values('duree');
      const lvl = values('niveau');
      const q = norm(query.trim());
      const before = new Map(cards.filter(c => !c.hidden).map(c => [c, c.getBoundingClientRect()]));

      let shown = 0;
      cards.forEach(c => {
        const ok = (!fmt.length || fmt.includes(c.dataset.format))
          && (!dur.length || dur.includes(bucket(Number(c.dataset.days))))
          && (!lvl.length || c.dataset.level === 'tous' || lvl.includes(c.dataset.level))
          && (!q || c.dataset.text.includes(q));
        c.hidden = !ok;
        if (ok) shown++;
      });

      const sort = sortSel ? sortSel.value : 'sessions';
      const key = c => (sort === 'duree' ? Number(c.dataset.days) * 100 + Number(c.dataset.order)
        : sort === 'niveau' ? LEVELS[c.dataset.level] * 100 + Number(c.dataset.order)
          : Number(c.dataset.order));
      cards.slice().sort((a, b) => key(a) - key(b)).forEach(c => grid.append(c));

      if (animate && !reduceMotion) {
        cards.filter(c => !c.hidden).forEach(c => {
          const prev = before.get(c);
          const now = c.getBoundingClientRect();
          if (prev) {
            const dx = prev.left - now.left;
            const dy = prev.top - now.top;
            if (dx || dy) c.animate([{ transform: `translate(${dx}px, ${dy}px)` }, { transform: 'none' }], { duration: 550, easing: 'cubic-bezier(.22,1,.36,1)' });
          } else {
            c.animate([{ opacity: 0, transform: 'scale(.94)' }, { opacity: 1, transform: 'none' }], { duration: 450, easing: 'cubic-bezier(.22,1,.36,1)' });
          }
        });
      }

      if (countEl) countEl.textContent = `${shown} formation${shown > 1 ? 's' : ''}`;
      if (empty) empty.hidden = shown > 0;
      if (queryChip) {
        queryChip.hidden = !query;
        $('[data-query]', queryChip).textContent = query;
      }
      if (toggle) {
        const n = dur.length + lvl.length + (fmt.length < 3 ? 1 : 0);
        $('[data-active-filters]', toggle).textContent = n ? ` (${n})` : '';
      }
    };

    form.addEventListener('change', () => apply());
    form.addEventListener('submit', e => e.preventDefault());
    sortSel && sortSel.addEventListener('change', () => apply());
    $$('[data-reset]', root).forEach(b => b.addEventListener('click', () => {
      $$('input[name="format"]', form).forEach(i => { i.checked = true; });
      $$('input[name="duree"], input[name="niveau"]', form).forEach(i => { i.checked = false; });
      query = '';
      history.replaceState(null, '', location.pathname);
      apply();
    }));
    toggle && toggle.addEventListener('click', () => {
      const open = form.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open);
    });
    apply(false);
  });

  /* ---------- Programme en accordéon ---------- */
  run('accordion', () => {
    $$('.module__head').forEach(btn => {
      const panel = document.getElementById(btn.getAttribute('aria-controls'));
      if (!panel) return;
      const sync = () => {
        const open = btn.getAttribute('aria-expanded') === 'true';
        panel.toggleAttribute('data-closed', !open);
        panel.inert = !open;
      };
      btn.addEventListener('click', () => {
        btn.setAttribute('aria-expanded', btn.getAttribute('aria-expanded') !== 'true');
        sync();
      });
      sync();
    });
  });

  /* ---------- Barre d'inscription collante ---------- */
  run('buybar', () => {
    const bar = $('.buybar');
    const anchor = $('.booking');
    if (!bar || !anchor) return;
    const footer = $('.site-footer');
    let pastBooking = false, footerVisible = false;
    const update = () => {
      const show = pastBooking && !footerVisible;
      bar.classList.toggle('is-visible', show);
      bar.inert = !show;
    };
    new IntersectionObserver(([e]) => { pastBooking = !e.isIntersecting && e.boundingClientRect.top < 0; update(); }).observe(anchor);
    footer && new IntersectionObserver(([e]) => { footerVisible = e.isIntersecting; update(); }).observe(footer);
    update();
  });

  /* ==========================================================================
     Fenêtres modales
     ========================================================================== */
  const modals = {};
  const syncScrollLock = () => doc.classList.toggle('modal-open', Object.values(modals).some(m => m.open));

  function openModal(id) {
    const dlg = modals[id];
    if (!dlg) return;
    Object.values(modals).forEach(m => { if (m !== dlg && m.open) { m.classList.remove('is-closing'); m.close(); } });
    if (doc.classList.contains('menu-open')) $('.nav-toggle')?.click();
    if (!dlg.open) dlg.showModal();
    syncScrollLock();
    dlg.dispatchEvent(new Event('opened'));
  }

  function closeModal(dlg) {
    if (!dlg.open || dlg.classList.contains('is-closing')) return;
    const done = () => { dlg.classList.remove('is-closing'); dlg.close(); syncScrollLock(); };
    if (reduceMotion) { done(); return; }
    dlg.classList.add('is-closing');
    setTimeout(done, 300);
  }

  function registerModal(id, html) {
    document.body.insertAdjacentHTML('beforeend', html);
    const dlg = document.getElementById(`modal-${id}`);
    dlg.addEventListener('cancel', e => { e.preventDefault(); closeModal(dlg); });
    dlg.addEventListener('close', syncScrollLock);
    dlg.addEventListener('click', e => {
      if (e.target === dlg || e.target.closest('[data-close]')) closeModal(dlg);
    });
    modals[id] = dlg;
    return dlg;
  }

  /* ---------- Contact ---------- */
  run('contact', () => {
    const dlg = registerModal('contact', `
      <dialog class="modal modal--drawer" id="modal-contact" aria-labelledby="contact-title">
        <div class="modal__box">
          <form class="drawer" novalidate>
            <div class="drawer__head">
              <div>
                <p class="eyebrow">CONTACT</p>
                <h2 class="drawer__title" id="contact-title">Parlons de vos besoins</h2>
              </div>
              <button type="button" class="icon-btn" data-close aria-label="Fermer">${icon('close')}</button>
            </div>
            <p class="drawer__context" hidden>${icon('check', 'i i--sm')}<span data-context></span></p>
            <div class="field"><label for="c-name">Nom et prénom *</label><input id="c-name" name="name" autocomplete="name" required><span class="field__error" aria-live="polite"></span></div>
            <div class="field"><label for="c-email">E-mail professionnel *</label><input id="c-email" name="email" type="email" autocomplete="email" required><span class="field__error" aria-live="polite"></span></div>
            <div class="field-row">
              <div class="field"><label for="c-phone">Téléphone</label><input id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
              <div class="field"><label for="c-company">Entreprise</label><input id="c-company" name="company" autocomplete="organization"></div>
            </div>
            <div class="field"><label for="c-subject">Votre demande</label>
              <select id="c-subject" name="subject">
                <option>Être rappelé par un conseiller</option>
                <option>Inscription à une session</option>
                <option>Demande de devis intra-entreprise</option>
                <option>Demande de formation sur-mesure</option>
                <option>Diagnostic 360</option>
                <option>Autre</option>
              </select>
            </div>
            <div class="field"><label for="c-message">Message</label><textarea id="c-message" name="message" placeholder="Votre contexte, le nombre de personnes, vos délais…"></textarea></div>
            <p class="drawer__legal">Vos informations servent uniquement à vous recontacter au sujet de votre demande.</p>
            <button class="btn btn--block drawer__submit" type="submit">Envoyer ma demande ${icon('arrow')}</button>
          </form>
          <div class="drawer__done" hidden>
            <svg class="done-check" viewBox="0 0 84 84" fill="none" aria-hidden="true">
              <circle cx="42" cy="42" r="38" stroke="url(#doneGrad)" stroke-width="4"/>
              <path d="M27 43l10 10 21-22" stroke="#2F5FE8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
              <defs><linearGradient id="doneGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3ED3F4"/><stop offset="1" stop-color="#4B3BDB"/></linearGradient></defs>
            </svg>
            <h2 class="drawer__title">Merci, c’est bien reçu.</h2>
            <p class="lead">Un conseiller vous recontacte rapidement pour échanger sur votre besoin.</p>
            <p class="demo-note" data-demo hidden>MODE DÉMO · AUCUNE DONNÉE ENVOYÉE (CONFIGURER CONTACT_ENDPOINT DANS SITE.JS)</p>
            <button type="button" class="btn btn--outline" data-close>Fermer</button>
          </div>
        </div>
      </dialog>`);

    const form = $('form', dlg);
    const done = $('.drawer__done', dlg);
    const ctx = $('.drawer__context', dlg);
    const subject = $('#c-subject', dlg);

    const setError = (input, msg) => {
      const field = input.closest('.field');
      field.classList.toggle('has-error', !!msg);
      $('.field__error', field).textContent = msg || '';
      input.setAttribute('aria-invalid', !!msg);
    };
    const validate = () => {
      const name = $('#c-name', dlg);
      const email = $('#c-email', dlg);
      let ok = true;
      if (!name.value.trim()) { setError(name, 'Indiquez votre nom.'); ok = false; } else setError(name);
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) { setError(email, 'Indiquez une adresse e-mail valide.'); ok = false; } else setError(email);
      if (!ok) $('.has-error input', dlg).focus();
      return ok;
    };
    $$('#c-name, #c-email', dlg).forEach(i => i.addEventListener('input', () => { if (i.closest('.has-error')) validate(); }));

    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (!validate()) return;
      const btn = $('[type="submit"]', form);
      btn.disabled = true;
      try {
        if (CONTACT_ENDPOINT) {
          const res = await fetch(CONTACT_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify({ ...Object.fromEntries(new FormData(form)), context: ctx.hidden ? '' : ctx.textContent, page: location.pathname })
          });
          if (!res.ok) throw new Error(res.status);
        }
        $('[data-demo]', dlg).hidden = !!CONTACT_ENDPOINT;
        form.hidden = true;
        done.hidden = false;
        $('[data-close]', done).focus();
      } catch (err) {
        console.error('[Skill360] contact', err);
        alert('L’envoi n’a pas abouti. Merci de réessayer dans un instant.');
      } finally {
        btn.disabled = false;
      }
    });

    dlg.prepare = (subjectText, message) => {
      form.hidden = false;
      done.hidden = true;
      form.reset();
      $$('.field', form).forEach(f => f.classList.remove('has-error'));
      ctx.hidden = !subjectText;
      $('[data-context]', ctx).textContent = subjectText || '';
      if (subjectText) {
        const s = norm(subjectText);
        const match = [...subject.options].find(o => {
          const o2 = norm(o.text);
          return (s.includes('inscription') && o2.includes('inscription'))
            || (s.includes('devis') && o2.includes('devis'))
            || (s.includes('sur-mesure') && o2.includes('sur-mesure'))
            || (s.includes('diagnostic') && o2.includes('diagnostic'));
        });
        if (match) subject.value = match.value;
      }
      if (message) $('#c-message', dlg).value = message;
    };
    dlg.addEventListener('opened', () => setTimeout(() => $('#c-name', dlg).focus(), 80));
  });

  /* ---------- Diagnostic 360 ---------- */
  run('diagnostic', () => {
    const CAT_PAGE = 'categorie-management-leadership.html';
    const AXES = [
      { key: 'Management', q: 'Encadrer, déléguer, fixer des objectifs : où en est votre équipe ?', cat: 'Management & leadership', href: CAT_PAGE },
      { key: 'Communication', q: 'Prise de parole, relation client, feedback : quel est votre niveau ?', cat: 'Communication & soft skills', href: 'formations.html#categories' },
      { key: 'Digital', q: 'Bureautique, outils collaboratifs, IA au travail : à quel point êtes-vous à l’aise ?', cat: 'Outils numériques & bureautique', href: 'formations.html#categories' },
      { key: 'Langues', q: 'En anglais professionnel (ou une autre langue), vous êtes plutôt…', cat: 'Langues étrangères', href: 'formations.html#categories' },
      { key: 'Organisation', q: 'Priorités, gestion du temps, conduite de projet : comment ça se passe ?', cat: 'Management & leadership', href: CAT_PAGE },
      { key: 'Sécurité', q: 'Obligations réglementaires et prévention : votre équipe est-elle à jour ?', cat: 'Sécurité & réglementaire', href: 'formations.html#categories' }
    ];
    const LEVELS = [
      { label: 'On démarre', hint: 'Peu ou pas de pratique', v: .25 },
      { label: 'Les bases sont là', hint: 'Quelques réflexes, à consolider', v: .5 },
      { label: 'C’est solide', hint: 'Pratique régulière et maîtrisée', v: .75 },
      { label: 'On est experts', hint: 'On pourrait l’enseigner', v: .95 }
    ];
    const LABELS = [
      ['120', '18', 'middle'], ['204', '70', 'start'], ['204', '178', 'start'],
      ['120', '232', 'middle'], ['36', '178', 'end'], ['36', '70', 'end']
    ];

    const dlg = registerModal('diagnostic', `
      <dialog class="modal modal--diag" id="modal-diagnostic" aria-labelledby="diag-title">
        <div class="modal__box diag">
          <div class="diag__main">
            <div class="diag__top">
              <p class="eyebrow eyebrow--plain">DIAGNOSTIC 360 · 2 MINUTES</p>
              <button type="button" class="icon-btn" data-close aria-label="Fermer">${icon('close')}</button>
            </div>
            <div class="diag__progress" aria-hidden="true"><i></i></div>
            <div class="diag__stage" aria-live="polite"></div>
          </div>
          <div class="diag__viz">
            <p class="eyebrow eyebrow--light eyebrow--plain diag__caption">VOTRE CARTE DE COMPÉTENCES</p>
            <svg class="radar radar--dark" viewBox="-60 -4 360 248" role="img" aria-label="Radar de vos compétences">
              <defs><linearGradient id="diagRadar" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3ED3F4"/><stop offset="1" stop-color="#4B3BDB"/></linearGradient></defs>
              <polygon points="120,30 197.9,75 197.9,165 120,210 42.1,165 42.1,75" fill="#161D4A" stroke="#3D4790"/>
              <polygon points="120,60 171.96,90 171.96,150 120,180 68.04,150 68.04,90" fill="none" stroke="#3D4790"/>
              <path d="M120 120L120 30M120 120L197.9 75M120 120L197.9 165M120 120L120 210M120 120L42.1 165M120 120L42.1 75" stroke="#3D4790"/>
              <polygon data-radar-goal class="radar__goal" points="" fill="none" stroke="#9DB4FF" stroke-width="1.6" style="opacity:0;transition:opacity .8s"/>
              <polygon data-radar-now points="" fill="url(#diagRadar)" fill-opacity=".45" stroke="url(#diagRadar)" stroke-width="2.5" stroke-linejoin="round"/>
              <g font-family="JetBrains Mono, monospace" font-size="12" fill="#B9C0E0">
                ${AXES.map((a, i) => `<text x="${LABELS[i][0]}" y="${LABELS[i][1]}" text-anchor="${LABELS[i][2]}">${a.key}</text>`).join('')}
              </g>
            </svg>
            <p class="lead lead--dark diag__caption" style="font-size:15px">Chaque réponse redessine votre radar en direct.</p>
          </div>
        </div>
      </dialog>`);

    const stage = $('.diag__stage', dlg);
    const bar = $('.diag__progress i', dlg);
    const svg = $('svg.radar', dlg);
    const labels = $$('text', svg);
    const radar = new Radar(svg);
    const goal = $('[data-radar-goal]', svg);
    let answers = [];
    let step = 0;

    const radarValues = () => AXES.map((_, i) => (answers[i] !== undefined ? answers[i] : .1));
    const markAxis = i => labels.forEach((t, k) => t.classList.toggle('is-current', k === i));

    const renderQuestion = () => {
      const axis = AXES[step];
      bar.style.width = `${(step / AXES.length) * 100}%`;
      markAxis(step);
      stage.innerHTML = `
        <p class="mono muted">QUESTION ${step + 1} / ${AXES.length} · ${axis.key.toUpperCase()}</p>
        <h2 class="diag__q" id="diag-title">${axis.q}</h2>
        <div class="diag__opts" role="radiogroup" aria-labelledby="diag-title">
          ${LEVELS.map((l, i) => `
            <button type="button" class="opt" role="radio" aria-checked="${answers[step] === l.v}" data-v="${l.v}">
              <span class="opt__key">${i + 1}</span>
              <span class="opt__text"><strong>${l.label}</strong><small>${l.hint}</small></span>
              <span class="opt__meter" aria-hidden="true">${[0, 1, 2, 3].map(k => `<i class="${k <= i ? 'on' : ''}"></i>`).join('')}</span>
            </button>`).join('')}
        </div>
        <div class="diag__nav">
          <button type="button" class="link-btn" data-back ${step === 0 ? 'disabled' : ''}>← Question précédente</button>
          <span class="diag__hint">Raccourcis <kbd>1</kbd>–<kbd>4</kbd></span>
        </div>`;
    };

    const renderResult = () => {
      bar.style.width = '100%';
      markAxis(-1);
      const vals = radarValues();
      const score = Math.round(vals.reduce((a, b) => a + b, 0) / vals.length * 100);
      const order = vals.map((v, i) => [v, i]).sort((a, b) => a[0] - b[0]);
      const low = order.slice(0, 2).map(([, i]) => i);
      const top = AXES[low[0]];
      const strong = AXES[order[order.length - 1][1]];
      const goalVals = vals.map((v, i) => Math.min(.95, v + (low.includes(i) ? .3 : .12)));
      radar.setGoal(goalVals);
      goal.style.opacity = '1';
      const summary = AXES.map((a, i) => `${a.key} ${Math.round(vals[i] * 100)} %`).join(', ');
      stage.innerHTML = `
        <p class="mono muted">RÉSULTAT · SCORE GLOBAL ${score}/100</p>
        <h2 class="diag__q" id="diag-title">Votre priorité : <span class="grad-text">${top.cat}</span></h2>
        <ul class="diag__result-list">
          ${AXES.map((a, i) => `<li class="${low.includes(i) ? 'is-low' : ''}"><span>${a.key}</span><span class="bar"><i style="--w:${Math.round(vals[i] * 100)}%"></i></span><b>${Math.round(vals[i] * 100)}%</b></li>`).join('')}
        </ul>
        <p class="lead" style="font-size:16px">Point fort : <strong>${strong.key}</strong>. Le pointillé montre où un parcours ciblé peut vous emmener.</p>
        <div class="diag__nav" style="flex-wrap:wrap">
          <div class="btn-row">
            <a class="btn" href="${top.href}">Voir les formations ${icon('arrow')}</a>
            <button type="button" class="btn btn--outline" data-open="contact" data-subject="Diagnostic 360 — priorité : ${top.cat}" data-message="Résultats de mon diagnostic : ${summary}.">Être rappelé</button>
          </div>
          <button type="button" class="link-btn" data-restart>Recommencer</button>
        </div>`;
      requestAnimationFrame(() => $$('.bar', stage).forEach(b => b.classList.add('is-in')));
    };

    const choose = v => {
      answers[step] = v;
      $$('.opt', stage).forEach(o => o.setAttribute('aria-checked', Number(o.dataset.v) === v));
      radar.to(radarValues(), 700);
      setTimeout(() => {
        step++;
        if (step < AXES.length) renderQuestion();
        else renderResult();
        $('.diag', dlg).scrollTop = 0;
        $('.opt, .btn', stage)?.focus({ preventScroll: true });
      }, reduceMotion ? 0 : 420);
    };

    const reset = () => {
      answers = [];
      step = 0;
      goal.style.opacity = '0';
      radar.draw(new Array(6).fill(.1));
      renderQuestion();
      $('.diag', dlg).scrollTop = 0;
    };

    stage.addEventListener('click', e => {
      const opt = e.target.closest('.opt');
      if (opt) { choose(Number(opt.dataset.v)); return; }
      if (e.target.closest('[data-back]') && step > 0) { step--; renderQuestion(); radar.to(radarValues(), 500); }
      if (e.target.closest('[data-restart]')) reset();
    });
    dlg.addEventListener('keydown', e => {
      if (step >= AXES.length || !/^[1-4]$/.test(e.key)) return;
      if (e.target.closest('input, textarea, select')) return;
      choose(LEVELS[Number(e.key) - 1].v);
    });
    dlg.prepare = reset;
    dlg.addEventListener('opened', () => setTimeout(() => $('.opt', stage)?.focus({ preventScroll: true }), 80));
    reset();
  });

  /* ---------- Déclencheurs ---------- */
  run('triggers', () => {
    document.addEventListener('click', e => {
      const t = e.target.closest('[data-open]');
      if (!t || !modals[t.dataset.open]) return;
      e.preventDefault();
      const dlg = modals[t.dataset.open];
      if (dlg.prepare) dlg.prepare(t.dataset.subject, t.dataset.message);
      openModal(t.dataset.open);
    });
    const hash = location.hash.slice(1);
    if (hash === 'diagnostic' || hash === 'contact') {
      modals[hash].prepare && modals[hash].prepare();
      openModal(hash);
    }
  });
})();
