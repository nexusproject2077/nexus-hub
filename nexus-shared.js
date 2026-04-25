/* ═══════════════════════════════════════════════
   NEXUS SHARED — Common JS for all pages
   Requires in HTML:
     <canvas id="bg">
     <div id="spotlight">
     <div id="cdot" class="c-dot">
     <div id="cring" class="c-ring">
     <span id="system-time">  (optional)
   ═══════════════════════════════════════════════ */
(function () {
  'use strict';

  // ── Service Worker ─────────────────────────────
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('./sw.js')
        .catch(() => {}); // silent fail — doesn't matter offline
    });
  }

  // ── Clock ──────────────────────────────────────
  const timeEl = document.getElementById('system-time');
  if (timeEl) {
    const tick = () => timeEl.textContent =
      new Date().toLocaleTimeString('fr-FR', { hour12: false });
    setInterval(tick, 1000); tick();
  }

  // ── Custom Cursor ──────────────────────────────
  const dot  = document.getElementById('cdot');
  const ring = document.getElementById('cring');
  const sp   = document.getElementById('spotlight');

  if (dot && ring) {
    let mx = innerWidth / 2, my = innerHeight / 2, rx = mx, ry = my;

    document.addEventListener('mousemove', e => {
      mx = e.clientX; my = e.clientY;
      dot.style.left = mx + 'px';
      dot.style.top  = my + 'px';
      if (sp) {
        sp.style.setProperty('--mx', mx + 'px');
        sp.style.setProperty('--my', my + 'px');
      }
    });

    (function lerpRing() {
      rx += (mx - rx) * .1;
      ry += (my - ry) * .1;
      ring.style.left = rx + 'px';
      ring.style.top  = ry + 'px';
      requestAnimationFrame(lerpRing);
    })();

    document.querySelectorAll('a, button, input, [data-hover]').forEach(el => {
      el.addEventListener('mouseenter', () => ring.classList.add('big'));
      el.addEventListener('mouseleave', () => ring.classList.remove('big'));
    });
  }

  // ── Particle Network Canvas ────────────────────
  const cv = document.getElementById('bg');
  if (cv) {
    const cx = cv.getContext('2d');
    let W, H, pts = [];

    const resize = () => { W = cv.width = innerWidth; H = cv.height = innerHeight; };
    window.addEventListener('resize', resize); resize();

    class Particle {
      constructor() { this.init(); }
      init() {
        this.x  = Math.random() * W;
        this.y  = Math.random() * H;
        this.vx = (Math.random() - .5) * .25;
        this.vy = (Math.random() - .5) * .25;
        this.r  = Math.random() * 1.2 + .4;
        this.a  = Math.random() * .35 + .08;
      }
      step() {
        this.x += this.vx; this.y += this.vy;
        if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.init();
      }
      draw() {
        cx.beginPath();
        cx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
        cx.fillStyle = `rgba(180,180,255,${this.a})`;
        cx.fill();
      }
    }

    for (let i = 0; i < 90; i++) pts.push(new Particle());

    (function frame() {
      cx.clearRect(0, 0, W, H);
      for (let i = 0; i < pts.length; i++) {
        pts[i].step(); pts[i].draw();
        for (let j = i + 1; j < pts.length; j++) {
          const dx = pts[i].x - pts[j].x;
          const dy = pts[i].y - pts[j].y;
          const d  = Math.sqrt(dx * dx + dy * dy);
          if (d < 110) {
            cx.beginPath();
            cx.moveTo(pts[i].x, pts[i].y);
            cx.lineTo(pts[j].x, pts[j].y);
            cx.strokeStyle = `rgba(99,102,241,${.12 * (1 - d / 110)})`;
            cx.lineWidth = .5;
            cx.stroke();
          }
        }
      }
      requestAnimationFrame(frame);
    })();
  }

  // ── 3-D Card Tilt (.tilt-card) ─────────────────
  document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width  - .5;
      const y = (e.clientY - r.top)  / r.height - .5;
      card.style.transform =
        `perspective(700px) rotateX(${-y * 9}deg) rotateY(${x * 9}deg) translateY(-4px)`;
    });
    card.addEventListener('mouseleave', () => { card.style.transform = ''; });
  });

  // ── Scroll-to-top button ───────────────────────
  const scrollBtn = document.getElementById('scroll-top');
  if (scrollBtn) {
    window.addEventListener('scroll', () => {
      scrollBtn.classList.toggle('visible', window.scrollY > 300);
    });
    scrollBtn.addEventListener('click', () =>
      window.scrollTo({ top: 0, behavior: 'smooth' })
    );
  }

  // ── Keyboard shortcut: '/' → focus search ─────
  document.addEventListener('keydown', e => {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
      e.preventDefault();
      const s = document.getElementById('searchInput');
      if (s) s.focus();
    }
    if (e.key === 'Escape') {
      const s = document.getElementById('searchInput');
      if (s) { s.blur(); s.value = ''; s.dispatchEvent(new Event('input')); }
    }
  });

})();
