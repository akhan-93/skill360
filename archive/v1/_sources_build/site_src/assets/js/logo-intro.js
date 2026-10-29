/*!
 * Skill360 — animation du logo
 *
 * 1. le point (l'apprenant) apparaît au centre ;
 * 2. l'orbite se trace autour de lui (DrawSVG) ;
 * 3. le O fait un tour complet sur lui-même en se transformant (MorphSVG) :
 *    la ligne d'orbite se gonfle puis se fend en trois segments à coupes en chevron ;
 * 4. le O roule jusqu'à sa place, le point quitte le centre et rejoint le « i » ;
 * 5. le logotype s'écrit lettre à lettre (tracé du contour puis remplissage) ;
 * 6. la signature apparaît, l'orbite se verrouille.
 *
 * Dépendances : gsap 3.13+, MorphSVGPlugin, DrawSVGPlugin.
 * Usage : Skill360.createLogoIntro(svgElement, { onReveal, onComplete, repeat, paused })
 */
(function (root) {
  'use strict';

  function createLogoIntro(svg, options) {
    var o = Object.assign({
      startScale: 1.3,      // taille de l'orbite pendant la phase centrale
      paused: false,
      repeat: 0,
      repeatDelay: 1.8,
      onReveal: null,       // appelé quand le logo est lisible (pour révéler le reste de la page)
      onComplete: null
    }, options || {});

    var $ = function (s) { return svg.querySelector(s); };
    var $$ = function (s) { return Array.prototype.slice.call(svg.querySelectorAll(s)); };

    var data = svg.dataset;
    var lcx = +data.lcx, ocx = +data.ocx, ocy = +data.ocy, dcx = +data.dcx, dcy = +data.dcy;
    var origin = ocx + ' ' + ocy;

    var move = $('.lg-orbit-move');
    var spin = $('.lg-orbit-spin');
    var trace = $('.lg-trace');
    var halo = $('.lg-halo');
    var dot = $('.lg-dot');
    var segs = $$('.lg-seg');
    var letters = $$('.lg-ltr');
    var tag = $$('.lg-tg');

    var startX = lcx - ocx;   // l'orbite naît au centre du logotype
    var dotX = lcx - dcx;     // le point naît au centre de l'orbite
    var dotY = ocy - dcy;

    var tl = gsap.timeline({
      paused: o.paused,
      repeat: o.repeat,
      repeatDelay: o.repeatDelay,
      onComplete: o.onComplete,
      defaults: { ease: 'power3.out' }
    });

    // 0 — état de départ, posé dans la timeline : restart() et repeat remettent tout à zéro
    tl.set(move, { x: startX, y: 0, scale: o.startScale, svgOrigin: origin }, 0)
      .set(spin, { rotation: 0, scale: 1, svgOrigin: origin }, 0)
      .set(halo, { opacity: 0, scale: 0.35, svgOrigin: origin }, 0)
      .set(trace, { opacity: 1, drawSVG: '0% 0%' }, 0)
      .set(segs, { opacity: 0 }, 0)
      .set(dot, { x: dotX, y: dotY, scale: 0, scaleX: 0, scaleY: 0, transformOrigin: '50% 50%' }, 0)
      .set(letters, { drawSVG: '0% 0%', fillOpacity: 0, strokeOpacity: 1 }, 0)
      .set(tag, { opacity: 0, y: 70 }, 0);
    segs.forEach(function (s) {
      tl.set(s, { morphSVG: { shape: s.getAttribute('data-thin'), shapeIndex: 0 } }, 0);
    });

    // 1 — le point : l'apprenant
    tl.to(dot, { scale: o.startScale, duration: 0.7, ease: 'back.out(2.6)' }, 0.1)
      .to(halo, { opacity: 1, scale: 0.7, duration: 1.1, ease: 'power2.out' }, 0.1)

    // 2 — l'orbite se trace autour de lui
      .to(trace, { drawSVG: '0% 100%', duration: 0.9, ease: 'power2.inOut' }, 0.45)
      .to(dot, { scale: o.startScale * 0.84, duration: 0.42, ease: 'sine.inOut', yoyo: true, repeat: 1 }, 0.62)

    // 3 — rotation du O et morphing
      .addLabel('morph', 1.32)
      .set(segs, { opacity: 1 }, 'morph')
      .set(trace, { opacity: 0 }, 'morph')
      .to(spin, { rotation: 360, duration: 1.75, ease: 'power3.inOut' }, 'morph')
      .to(halo, { scale: 1.05, duration: 1.4, ease: 'power2.inOut' }, 'morph');
    segs.forEach(function (s, i) {
      tl.to(s, {
        morphSVG: { shape: s.getAttribute('data-fat'), shapeIndex: 0 },
        duration: 0.8, ease: 'power2.in'
      }, 'morph+=' + (0.06 + i * 0.05))
        .to(s, {
          morphSVG: { shape: s.getAttribute('data-final'), shapeIndex: 0 },
          duration: 1.05, ease: 'elastic.out(1, 0.55)'
        }, 'morph+=' + (0.9 + i * 0.05));
    });

    // 4 — l'orbite roule jusqu'à sa place, le point rejoint le « i »
    tl.addLabel('travel', 2.8)
      .to(move, { x: 0, scale: 1, duration: 1.3, ease: 'power3.inOut' }, 'travel')
      .to(spin, { rotation: 720, duration: 1.3, ease: 'power3.inOut' }, 'travel')
      .to(halo, { opacity: 0.4, scale: 0.85, duration: 1.3, ease: 'power2.inOut' }, 'travel')
      .to(dot, { x: 0, duration: 1.05, ease: 'power2.inOut' }, 'travel+=0.15')
      .to(dot, { y: -380, duration: 0.5, ease: 'power2.out' }, 'travel+=0.15')
      .to(dot, { y: 0, duration: 0.55, ease: 'power2.in' }, 'travel+=0.65')
      .to(dot, { scale: 1, duration: 1.05, ease: 'power1.inOut' }, 'travel+=0.15')
      .to(dot, { scaleX: 1.3, scaleY: 0.7, duration: 0.09, ease: 'power1.out' }, 'travel+=1.2')
      .to(dot, { scaleX: 1, scaleY: 1, duration: 0.7, ease: 'elastic.out(1, 0.35)' }, 'travel+=1.29')

    // 5 — le logotype s'écrit
      .addLabel('write', 2.95)
      .to(letters, { drawSVG: '0% 100%', duration: 1.0, ease: 'power2.inOut', stagger: 0.1 }, 'write')
      .to(letters, { fillOpacity: 1, duration: 0.6, ease: 'power1.out', stagger: 0.1 }, 'write+=0.65')
      .to(letters, { strokeOpacity: 0, duration: 0.5, ease: 'power1.out', stagger: 0.1 }, 'write+=1.0')

    // 6 — la signature, puis l'orbite se verrouille
      .to(tag, { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out', stagger: 0.012 }, 'write+=1.05')
      .to(spin, { scale: 1.07, duration: 0.2, ease: 'power2.out', yoyo: true, repeat: 1 }, 'write+=1.3')
      .to(halo, { opacity: 0.7, duration: 0.25, ease: 'power1.inOut', yoyo: true, repeat: 1 }, 'write+=1.3')
      .to(halo, { opacity: 0, duration: 0.9, ease: 'power1.inOut' }, 'write+=1.85');

    if (typeof o.onReveal === 'function') tl.call(o.onReveal, null, 'write+=1.1');

    return tl;
  }

  // épaisseur du tracé d'écriture : ~1,6 px quelle que soit la taille d'affichage
  function fitLogoStroke(svg) {
    var vb = svg.viewBox && svg.viewBox.baseVal;
    var w = svg.getBoundingClientRect().width;
    if (!vb || !w) return;
    var px = Math.max(1.3, Math.min(2.2, w / 560));
    var sw = (px * vb.width / w).toFixed(1);
    Array.prototype.forEach.call(svg.querySelectorAll('.lg-ltr'), function (p) { p.setAttribute('stroke-width', sw); });
  }

  root.Skill360 = Object.assign(root.Skill360 || {}, {
    createLogoIntro: createLogoIntro,
    fitLogoStroke: fitLogoStroke
  });
})(window);
