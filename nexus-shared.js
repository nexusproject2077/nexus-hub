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

//âge
  function calculateAge(birthDate) {
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    // Si le mois actuel est avant juillet, ou si on est en juillet mais avant le 8
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    return age;
  }

  document.addEventListener('DOMContentLoaded', () => {
    // Date de naissance : 8 Juillet 2006 (les mois commencent à 0 en JS : 6 = Juillet)
    const birthDate = new Date(2006, 6, 8); 
    const ageElement = document.getElementById('user-age');
    
    if (ageElement) {
      ageElement.textContent = calculateAge(birthDate);
    }
  });

  //année
  (function () {
  const year = new Date().getFullYear();
  document.querySelectorAll('.current-year').forEach(el => {
    el.textContent = year;
  });
})();

  // ── Compteur d'abonnés Instagram ───────────────
  // Lit le fichier JSON tenu à jour par le workflow GitHub (instagrapi),
  // avec repli sur le backend Cloud Run /api/followers si besoin.
  (function () {
    const el = document.getElementById('follower-count');
    if (!el) return;

    const fmt = n => Number(n).toLocaleString('fr-FR');

    const fromStatic = () =>
      fetch('./followers_data.json?t=' + Date.now(), { cache: 'no-store' })
        .then(r => (r.ok ? r.json() : Promise.reject()));

    const fromApi = () =>
      fetch('/api/followers', { cache: 'no-store' })
        .then(r => (r.ok ? r.json() : Promise.reject()));

    // Le JSON statique est la source de vérité (mis à jour toutes les 6 h).
    fromStatic()
      .catch(fromApi)
      .then(d => {
        if (d && typeof d.followers === 'number' && d.followers > 0) {
          el.textContent = fmt(d.followers);
        }
      })
      .catch(() => { /* on garde la valeur affichée par défaut */ });
  })();

//blog
(function () {
  const startYear = 2020;
  const currentYear = new Date().getFullYear();
  const yearsOfCoding = currentYear - startYear;
  
  const codingElement = document.getElementById('coding-years');
  if (codingElement) {
    codingElement.textContent = yearsOfCoding;
  }
})();

//ticker
  // Construit un marquee fluide : duplique le motif de texte juste assez pour
  // remplir la largeur visible (mobile → 4K), puis une 2e copie identique pour
  // une boucle sans trou. Fini la piste géante qui part « à l'autre bout du monde ».
  function buildTicker(track) {
    const wrap = track.closest('.ticker-wrap');
    if (!wrap) return;

    // Capture le motif d'origine une seule fois (avant duplication).
    if (!track.dataset.unit) {
      const first = track.querySelector('.ticker-content');
      if (!first) return;
      track.dataset.unit = first.innerHTML;
      track.dataset.contentClass = first.getAttribute('class') || 'ticker-content';
    }
    const unit = track.dataset.unit;
    const cls = track.dataset.contentClass || 'ticker-content';

    // Mesure la largeur d'un motif et celle du conteneur.
    track.innerHTML = '<div class="' + cls + '">' + unit + '</div>';
    const unitW = track.firstElementChild.getBoundingClientRect().width;
    const contW = wrap.getBoundingClientRect().width;

    // Répète le motif pour qu'un groupe dépasse la largeur visible (pas plus).
    let reps = 1;
    if (unitW > 0) reps = Math.max(1, Math.ceil((contW + unitW) / unitW));
    const group = unit.repeat(reps);

    // Deux groupes identiques -> translateX(-50%) sans coupure.
    track.innerHTML =
      '<div class="' + cls + '">' + group + '</div>' +
      '<div class="' + cls + '" aria-hidden="true">' + group + '</div>';

    const year = new Date().getFullYear();
    track.querySelectorAll('.current-year').forEach(el => { el.textContent = year; });
    track.dataset.marquee = 'ready';
  }

  function buildAllTickers() {
    document.querySelectorAll('.ticker-track').forEach(buildTicker);
  }

  document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('ticker-container');
    if (container) {
      fetch('ticker.html')
        .then(r => { if (!r.ok) throw new Error('Erreur de chargement du ticker'); return r.text(); })
        .then(html => {
          container.innerHTML = html;
          const track = container.querySelector('.ticker-track');
          if (track) buildTicker(track);
        })
        .catch(err => console.error('Ticker Load Error:', err));
    }
    // Tickers déjà présents dans la page (ex. blog)
    document.querySelectorAll('.ticker-track').forEach(buildTicker);
  });

  // Recalcule après le chargement des polices et à chaque redimensionnement.
  window.addEventListener('load', buildAllTickers);
  let _tickerResize;
  window.addEventListener('resize', () => {
    clearTimeout(_tickerResize);
    _tickerResize = setTimeout(buildAllTickers, 200);
  });

   //footer
   document.addEventListener("DOMContentLoaded", () => {
  // Injection automatique du Footer
  const footerContainer = document.getElementById("footer-container");
  if (footerContainer) {
    fetch("footer.html")
      .then((response) => response.text())
      .then((data) => {
        footerContainer.innerHTML = data;
        
        // Met à jour l'année automatiquement après insertion
        const yearSpans = footerContainer.querySelectorAll(".current-year");
        yearSpans.forEach((el) => {
          el.textContent = new Date().getFullYear();
        });
      })
      .catch((err) => console.error("Erreur de chargement du footer:", err));
  }
});
   
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
