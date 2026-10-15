(() => {
  'use strict';

  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const DPR = Math.min(window.devicePixelRatio || 1, 2);

  /* ───────── language ───────── */
  // the initial language is picked in <head> (saved choice, else browser language)
  function setLang(lang, save) {
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-set-lang]').forEach(b =>
      b.setAttribute('aria-pressed', String(b.dataset.setLang === lang)));
    if (save) try { localStorage.setItem('lang', lang); } catch (e) {}
  }
  document.querySelectorAll('[data-set-lang]').forEach(b =>
    b.addEventListener('click', () => setLang(b.dataset.setLang, true)));
  setLang(document.documentElement.lang === 'es' ? 'es' : 'en');

  /* ───────── copy email ───────── */
  const emailBtn = document.getElementById('email-copy');
  if (emailBtn) {
    let timer;
    emailBtn.addEventListener('click', () => {
      const email = emailBtn.dataset.email;
      const fallback = () => { location.href = 'mailto:' + email; };
      if (!navigator.clipboard) return fallback();
      navigator.clipboard.writeText(email).then(() => {
        emailBtn.classList.add('copied');
        clearTimeout(timer);
        timer = setTimeout(() => emailBtn.classList.remove('copied'), 1800);
      }, fallback);
    });
  }

  /* ───────── lightbox ───────── */
  const lb = document.getElementById('lightbox');
  if (lb && lb.showModal) {
    const lbImg = lb.querySelector('img');
    document.querySelectorAll('[data-full]').forEach(btn => btn.addEventListener('click', () => {
      lbImg.src = btn.dataset.full;
      lbImg.alt = btn.querySelector('img').alt;
      lb.showModal();
    }));
    lb.addEventListener('click', e => { if (e.target !== lbImg) lb.close(); });
    lb.addEventListener('close', () => lbImg.removeAttribute('src'));
  }

  /* ───────── nav: highlight the section on screen ───────── */
  const navLinks = [...document.querySelectorAll('.nav-links a')];
  const spy = new IntersectionObserver(entries => {
    for (const en of entries) if (en.isIntersecting)
      navLinks.forEach(a => a.classList.toggle('on', a.hash === '#' + en.target.id));
  }, { rootMargin: '-40% 0px -55% 0px' });
  navLinks.forEach(a => { const t = document.querySelector(a.hash); if (t) spy.observe(t); });

  /* ───────── canvas animations ─────────
     Each one is make(ctx, w, h) → { frame(dt), still(), resize?(w, h), ... }.
     A single rAF loop drives only the ones on screen; with reduced motion
     they draw one still frame instead. */
  const anims = [];

  function canvasAnim(id, make) {
    const cv = document.getElementById(id);
    if (!cv || !cv.getContext) return null;
    const ctx = cv.getContext('2d');
    const a = { cv, state: null, visible: false, w: 0, h: 0 };
    const fit = () => {
      const w = cv.clientWidth, h = cv.clientHeight;
      if (w < 2 || h < 2 || (w === a.w && h === a.h)) return;
      a.w = w; a.h = h;
      cv.width = Math.round(w * DPR); cv.height = Math.round(h * DPR);
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      if (a.state && a.state.resize) a.state.resize(w, h);
      else { a.state = make(ctx, w, h); if (reduce) a.state.still(); }
    };
    new ResizeObserver(fit).observe(cv);
    new IntersectionObserver(([e]) => { a.visible = e.isIntersecting; }, { rootMargin: '120px' }).observe(cv);
    anims.push(a);
    return a;
  }

  if (!reduce) {
    let last = performance.now();
    const loop = now => {
      requestAnimationFrame(loop);
      const dt = now - last;
      if (dt < 15 || document.hidden) return;   // cap at ~60fps on high-refresh screens
      last = now;
      const step = Math.min(dt, 50);
      for (const a of anims) if (a.visible && a.state) a.state.frame(step);
    };
    requestAnimationFrame(loop);
  }

  /* fig. 0 — Conway's game of life (B3/S23) on the banner */
  const life = canvasAnim('c-life', (ctx, W, H) => {
    const S = W < 640 ? 12 : 10, cols = Math.ceil(W / S), rows = Math.ceil(H / S), N = cols * rows;
    let g = new Uint8Array(N), nx = new Uint8Array(N);
    const age = new Uint16Array(N);
    for (let i = 0; i < N; i++) g[i] = Math.random() < 0.3 ? 1 : 0;
    let acc = 0;

    const seed = (cx, cy, r, p) => {
      for (let y = cy - r; y <= cy + r; y++) for (let x = cx - r; x <= cx + r; x++) {
        if (Math.random() >= p) continue;
        const i = ((y + rows) % rows) * cols + ((x + cols) % cols);
        if (!g[i]) { g[i] = 1; age[i] = 0; }
      }
    };
    function step() {
      let pop = 0;
      for (let y = 0; y < rows; y++) {
        const up = ((y + rows - 1) % rows) * cols, mid = y * cols, dn = ((y + 1) % rows) * cols;
        for (let x = 0; x < cols; x++) {
          const l = (x + cols - 1) % cols, r = (x + 1) % cols;
          const n = g[up + l] + g[up + x] + g[up + r] + g[mid + l] + g[mid + r] + g[dn + l] + g[dn + x] + g[dn + r];
          const i = mid + x, alive = n === 3 || (n === 2 && g[i]) ? 1 : 0;
          nx[i] = alive;
          age[i] = alive ? (g[i] ? Math.min(age[i] + 1, 999) : 0) : 0;
          pop += alive;
        }
      }
      [g, nx] = [nx, g];
      if (pop < N * 0.05) seed(Math.random() * cols | 0, Math.random() * rows | 0, 4, 0.5);
    }
    function draw() {
      ctx.clearRect(0, 0, W, H);
      for (const young of [false, true]) {
        ctx.beginPath();
        for (let i = 0; i < N; i++) if (g[i] && (age[i] < 2) === young)
          ctx.rect((i % cols) * S + 1, ((i / cols) | 0) * S + 1, S - 2, S - 2);
        ctx.fillStyle = young ? 'rgba(244,244,239,.36)' : 'rgba(244,244,239,.14)';
        ctx.fill();
      }
    }
    return {
      frame(dt) { acc += dt; if (acc >= 120) { acc = 0; step(); } draw(); },
      still: draw,
      poke(px, py) { seed(px / S | 0, py / S | 0, 1, 0.6); if (reduce) draw(); },
    };
  });
  const banner = document.querySelector('.banner');
  if (life && banner) banner.addEventListener('pointermove', e => {
    const r = life.cv.getBoundingClientRect();
    if (life.state) life.state.poke(e.clientX - r.left, e.clientY - r.top);
  });

  /* fig. 1 — Lorenz attractor (σ=10, ρ=28, β=8/3), slowly rotating about z */
  canvasAnim('c-lorenz', (ctx, W, H) => {
    const NP = 6, L = 560, DT = 0.005, CH = 12, TILT = 0.38;
    const step = p => {
      const dx = 10 * (p.y - p.x), dy = p.x * (28 - p.z) - p.y, dz = p.x * p.y - 8 / 3 * p.z;
      p.x += dx * DT; p.y += dy * DT; p.z += dz * DT;
    };
    const trails = Array.from({ length: NP }, () => {
      const q = { x: Math.random() * 2 - 1, y: Math.random() * 2 - 1, z: 20 + Math.random() * 10 };
      for (let i = 0, m = 800 + Math.random() * 800; i < m; i++) step(q);
      const tr = [];
      for (let i = 0; i < L; i++) { step(q); tr.push([q.x, q.y, q.z]); }
      return { q, tr, head: 0 };   // ring buffer: tr[head] is the oldest point
    });
    const sc = Math.min(W * 0.9 / 50, H * 0.94 / 58), seg = Math.ceil(L / CH);
    const ct = Math.cos(TILT), st = Math.sin(TILT);
    let th = Math.random() * 6;

    function draw() {
      ctx.clearRect(0, 0, W, H);
      const co = Math.cos(th), si = Math.sin(th);
      // rotate about z, then tilt the camera a little so it reads as 3D
      const px = p => W / 2 + (p[0] * co - p[1] * si) * sc;
      const py = p => H / 2 + ((25 - p[2]) * ct - (p[0] * si + p[1] * co) * st) * sc;
      ctx.lineWidth = 0.8;
      for (let c = 0; c < CH; c++) {
        ctx.beginPath();
        for (const t of trails) for (let k = c * seg, e = Math.min(L - 1, (c + 1) * seg); k <= e; k++) {
          const p = t.tr[(t.head + k) % L];
          k === c * seg ? ctx.moveTo(px(p), py(p)) : ctx.lineTo(px(p), py(p));
        }
        ctx.strokeStyle = `rgba(5,5,5,${(0.05 + 0.6 * (c + 1) / CH).toFixed(3)})`;
        ctx.stroke();
      }
      ctx.fillStyle = '#050505';
      for (const t of trails) {
        const p = t.tr[(t.head + L - 1) % L];
        ctx.beginPath(); ctx.arc(px(p), py(p), 1.8, 0, 6.2832); ctx.fill();
      }
    }
    return {
      frame(dt) {
        th += dt * 0.00022;
        for (const t of trails) for (let k = 0; k < 2; k++) {
          step(t.q);
          t.tr[t.head] = [t.q.x, t.q.y, t.q.z];
          t.head = (t.head + 1) % L;
        }
        draw();
      },
      still: draw,
    };
  });

  /* fig. 2 — Chladni figures: nodal lines of cos(nπx)cos(mπy) − cos(mπx)cos(nπy) */
  const mnLabel = document.getElementById('chladni-mn');
  canvasAnim('c-chladni', (ctx, W, H) => {
    // always m < n, so interpolating between modes never hits the all-zero m = n case
    const MODES = [[2, 5], [3, 4], [1, 6], [3, 5], [4, 5], [2, 7], [5, 6], [3, 7], [4, 7], [1, 4], [2, 3], [3, 8]];
    const SC = 2, cols = Math.ceil(W / SC), rows = Math.ceil(H / SC);
    const off = document.createElement('canvas');
    off.width = cols; off.height = rows;
    const oc = off.getContext('2d'), img = oc.createImageData(cols, rows), d = img.data;
    const HOLD = 2600, TRANS = 2200;
    let k = 0, t = 0;

    function render(m, n) {
      for (let i = 0; i < rows; i++) {
        const y = i / (rows - 1);
        for (let j = 0; j < cols; j++) {
          const x = j / (cols - 1);
          const v = Math.cos(n * Math.PI * x) * Math.cos(m * Math.PI * y) - Math.cos(m * Math.PI * x) * Math.cos(n * Math.PI * y);
          const s = Math.exp(-v * v * 45) * 0.9, o = (i * cols + j) * 4;
          d[o] = d[o + 1] = 244 - 239 * s; d[o + 2] = 239 - 234 * s; d[o + 3] = 255;
        }
      }
      oc.putImageData(img, 0, 0);
      ctx.drawImage(off, 0, 0, W, H);
    }
    const label = () => { if (mnLabel) mnLabel.textContent = MODES[k].join(', '); };
    const still = () => { render(...MODES[k]); label(); };
    still();
    return {
      frame(dt) {
        t += dt;
        if (t < HOLD) return;
        const k2 = (k + 1) % MODES.length, u = Math.min(1, (t - HOLD) / TRANS), e = u * u * (3 - 2 * u);
        const [m0, n0] = MODES[k], [m1, n1] = MODES[k2];
        render(m0 + (m1 - m0) * e, n0 + (n1 - n0) * e);
        if (u >= 1) { k = k2; t = 0; label(); }
      },
      still,
    };
  });

  /* fig. 3 — particles following a drifting sinusoidal flow field */
  canvasAnim('c-flow', (ctx, W, H) => {
    const N = Math.round(Math.min(520, W * H / 180));
    const spawn = p => {
      p.x = Math.random() * W; p.y = Math.random() * H;
      p.vx = p.vy = 0; p.life = 0; p.max = 90 + Math.random() * 160;
      return p;
    };
    const ps = Array.from({ length: N }, () => {
      const p = spawn({ w: 0.4 + Math.random() * 0.9 });
      p.life = Math.random() * p.max | 0;
      return p;
    });
    let t = Math.random() * 100;
    const noise = (x, y) =>
      Math.sin(x * 0.0055 + t) * Math.cos(y * 0.0048 + t * 0.79) +
      Math.sin(x * 0.012 - t * 0.63) * Math.cos(y * 0.0095 + t * 0.31) +
      Math.sin((x - y) * 0.0038 + t * 0.47) * 0.55;

    ctx.fillStyle = '#f4f4ef'; ctx.fillRect(0, 0, W, H);
    ctx.lineCap = 'round';
    function frame() {
      t += 0.004;
      ctx.fillStyle = 'rgba(244,244,239,.07)'; ctx.fillRect(0, 0, W, H);
      const ax = W * 0.5 + Math.cos(t * 0.9) * W * 0.32, ay = H * 0.5 + Math.sin(t * 1.3) * H * 0.3;
      for (const p of ps) {
        const ang = noise(p.x, p.y) * Math.PI * 2;
        const dx = ax - p.x, dy = ay - p.y, d2 = dx * dx + dy * dy + 400;
        p.vx = p.vx * 0.9 + Math.cos(ang) * 1.4 + dx / d2 * 40;
        p.vy = p.vy * 0.9 + Math.sin(ang) * 1.4 + dy / d2 * 40;
        const sp = Math.hypot(p.vx, p.vy);
        if (sp > 4) { p.vx *= 4 / sp; p.vy *= 4 / sp; }
        const nx = p.x + p.vx, ny = p.y + p.vy, age = ++p.life / p.max;
        const fade = age < 0.1 ? age / 0.1 : age > 0.8 ? (1 - age) / 0.2 : 1;
        ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(nx, ny);
        ctx.strokeStyle = `rgba(5,5,5,${(0.6 * fade).toFixed(3)})`;
        ctx.lineWidth = p.w; ctx.stroke();
        p.x = nx; p.y = ny;
        if (p.life > p.max || nx < -8 || nx > W + 8 || ny < -8 || ny > H + 8) spawn(p);
      }
    }
    return { frame, still() { for (let i = 0; i < 140; i++) frame(); } };
  });

  /* background — Delaunay triangulation of drifting points (+ the cursor) */
  const ptr = { x: 0, y: 0, on: false };
  addEventListener('pointermove', e => {
    if (e.pointerType !== 'mouse') return;
    ptr.x = e.clientX; ptr.y = e.clientY; ptr.on = true;
  }, { passive: true });
  document.documentElement.addEventListener('mouseleave', () => { ptr.on = false; });

  function circum(P, a, b, c) {
    const A = P[a], B = P[b], C = P[c];
    const D = 2 * (A.x * (B.y - C.y) + B.x * (C.y - A.y) + C.x * (A.y - B.y));
    if (Math.abs(D) < 1e-9) return { a, b, c, x: 0, y: 0, r2: -1 };
    const a2 = A.x * A.x + A.y * A.y, b2 = B.x * B.x + B.y * B.y, c2 = C.x * C.x + C.y * C.y;
    const x = (a2 * (B.y - C.y) + b2 * (C.y - A.y) + c2 * (A.y - B.y)) / D;
    const y = (a2 * (C.x - B.x) + b2 * (A.x - C.x) + c2 * (B.x - A.x)) / D;
    return { a, b, c, x, y, r2: (A.x - x) ** 2 + (A.y - y) ** 2 };
  }
  // Bowyer–Watson: insert points one by one, re-triangulating the hole each one opens
  function delaunay(pts) {
    const n = pts.length, P = pts.concat([{ x: -1e4, y: -1e4 }, { x: 3e4, y: -1e4 }, { x: -1e4, y: 3e4 }]);
    let tris = [circum(P, n, n + 1, n + 2)];
    for (let i = 0; i < n; i++) {
      const p = P[i], edges = new Map(), keep = [];
      const edge = (u, v) => {
        const key = u < v ? u * 8192 + v : v * 8192 + u;
        edges.set(key, edges.has(key) ? null : [u, v]);
      };
      for (const t of tris) {
        if ((p.x - t.x) ** 2 + (p.y - t.y) ** 2 < t.r2) { edge(t.a, t.b); edge(t.b, t.c); edge(t.c, t.a); }
        else keep.push(t);
      }
      for (const e of edges.values()) if (e) keep.push(circum(P, e[0], e[1], i));
      tris = keep;
    }
    return tris.filter(t => t.a < n && t.b < n && t.c < n);
  }

  canvasAnim('bg', (ctx, W, H) => {
    const N = Math.round(Math.min(64, Math.max(22, W * H / 24000)));
    const pts = Array.from({ length: N }, () => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.036, vy: (Math.random() - 0.5) * 0.036,
    }));
    let t = 0;

    function draw() {
      ctx.clearRect(0, 0, W, H);
      const P = ptr.on ? pts.concat([{ x: ptr.x, y: ptr.y }]) : pts;
      ctx.lineWidth = 0.7;
      for (const tr of delaunay(P)) {
        const A = P[tr.a], B = P[tr.b], C = P[tr.c];
        const pulse = Math.sin((A.x + B.x + C.x) * 0.001 + (A.y + B.y + C.y) * 0.001 + t * 0.0012) * 0.5 + 0.5;
        ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y); ctx.lineTo(C.x, C.y); ctx.closePath();
        ctx.fillStyle = `rgba(5,5,5,${(pulse * 0.035).toFixed(4)})`; ctx.fill();
        ctx.strokeStyle = `rgba(5,5,5,${(0.07 + pulse * 0.07).toFixed(3)})`; ctx.stroke();
      }
      ctx.fillStyle = 'rgba(5,5,5,.22)';
      for (const p of P) { ctx.beginPath(); ctx.arc(p.x, p.y, 1.8, 0, 6.2832); ctx.fill(); }
    }
    return {
      frame(dt) {
        t += dt;
        for (const p of pts) {
          p.x += p.vx * dt; p.y += p.vy * dt;
          if (p.x < 0 || p.x > W) { p.vx *= -1; p.x = Math.max(0, Math.min(W, p.x)); }
          if (p.y < 0 || p.y > H) { p.vy *= -1; p.y = Math.max(0, Math.min(H, p.y)); }
        }
        draw();
      },
      still: draw,
      // keep the mesh when the viewport changes (e.g. the mobile URL bar), just rescale it
      resize(w, h) {
        for (const p of pts) { p.x *= w / W; p.y *= h / H; }
        W = w; H = h;
        if (reduce) draw();
      },
    };
  });
})();
