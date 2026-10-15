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

  /* ───────── canvas animations ─────────
     Each one is make(ctx, w, h) → { frame(dt), still(), resize?(w, h), ... }.
     A single rAF loop drives only the ones on screen; with reduced motion
     they draw one still frame instead, unless registered with always = true. */
  const anims = [];

  function canvasAnim(id, make, always = false) {
    const cv = document.getElementById(id);
    if (!cv || !cv.getContext) return null;
    const ctx = cv.getContext('2d');
    const a = { cv, state: null, visible: false, w: 0, h: 0, always };
    const fit = () => {
      const w = cv.clientWidth, h = cv.clientHeight;
      if (w < 2 || h < 2 || (w === a.w && h === a.h)) return;
      a.w = w; a.h = h;
      cv.width = Math.round(w * DPR); cv.height = Math.round(h * DPR);
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      if (a.state && a.state.resize) a.state.resize(w, h);
      else { a.state = make(ctx, w, h); if (reduce && !always) a.state.still(); }
    };
    new ResizeObserver(fit).observe(cv);
    new IntersectionObserver(([e]) => { a.visible = e.isIntersecting; }, { rootMargin: '120px' }).observe(cv);
    anims.push(a);
    return a;
  }

  let last = performance.now();
  const loop = now => {
    requestAnimationFrame(loop);
    const dt = now - last;
    if (dt < 15 || document.hidden) return;   // cap at ~60fps on high-refresh screens
    last = now;
    const step = Math.min(dt, 50);
    for (const a of anims) if (a.visible && a.state && (a.always || !reduce)) a.state.frame(step);
  };
  requestAnimationFrame(loop);

  /* banner — Conway's game of life (B3/S23) on the banner */
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

  /* into — Lorenz attractor (σ=10, ρ=28, β=8/3), slowly rotating about z */
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

  /* contact — a Galton board: 9 coin-flip bounces per ball pile up into a bell curve */
  canvasAnim('c-galton', (ctx, W, H) => {
    const R = 9, cx = W / 2, sp = Math.min(W * 0.88 / (R + 1), 22);
    const y0 = 12, y1 = H * 0.52, vsp = (y1 - y0) / R, bottom = H - 6, unit = 1.6;
    const cap = (bottom - y1 - 10) / unit, sigma = Math.sqrt(R) / 2;
    const pegX = (r, j) => cx + (j - r / 2) * sp;   // peg j of row r (row R = the bins)
    const counts = new Array(R + 1).fill(0);
    let balls = [], spawnT = 0, holdT = 0, full = false;

    const coin = () => (Math.random() < 0.5 ? 0 : 1);
    const pos = b => {
      if (b.r < R) {   // bouncing from peg (r, k) to peg (r + 1, k + d)
        const xa = pegX(b.r, b.k), xb = pegX(b.r + 1, b.k + b.d), ya = y0 + b.r * vsp;
        return [xa + (xb - xa) * b.p, ya + vsp * b.p - Math.sin(Math.PI * b.p) * vsp * 0.45 - 3];
      }
      const top = bottom - counts[b.k] * unit - 2;   // falling into bin k
      return [pegX(R, b.k), y1 - 3 + (top - y1 + 3) * b.p * b.p];
    };

    function draw() {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = 'rgba(5,5,5,.45)';
      for (let r = 0; r < R; r++) for (let j = 0; j <= r; j++) {
        ctx.beginPath(); ctx.arc(pegX(r, j), y0 + r * vsp, 1.5, 0, 6.2832); ctx.fill();
      }
      const left = pegX(R, 0) - sp / 2, right = pegX(R, R) + sp / 2;
      ctx.strokeStyle = 'rgba(5,5,5,.18)'; ctx.lineWidth = 1; ctx.beginPath();
      for (let k = 0; k <= R + 1; k++) { ctx.moveTo(left + k * sp, y1 + 6); ctx.lineTo(left + k * sp, bottom); }
      ctx.moveTo(left, bottom); ctx.lineTo(right, bottom);
      ctx.stroke();
      ctx.fillStyle = 'rgba(5,5,5,.8)';
      counts.forEach((c, k) => { if (c) ctx.fillRect(pegX(R, k) - sp / 2 + 2.5, bottom - c * unit, sp - 5, c * unit); });
      // the normal curve N(R/2, R/4) these counts should approach
      const total = counts.reduce((a, c) => a + c, 0);
      if (total > 8) {
        ctx.setLineDash([3, 3]); ctx.strokeStyle = 'rgba(5,5,5,.55)'; ctx.beginPath();
        for (let u = -0.5; u <= R + 0.5; u += 0.1) {
          const f = Math.exp(-((u - R / 2) ** 2) / (2 * sigma * sigma)) / (sigma * Math.sqrt(2 * Math.PI));
          const x = pegX(R, u), y = bottom - total * f * unit;
          u === -0.5 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.stroke(); ctx.setLineDash([]);
      }
      ctx.fillStyle = '#050505';
      for (const b of balls) { const [x, y] = pos(b); ctx.beginPath(); ctx.arc(x, y, 2.2, 0, 6.2832); ctx.fill(); }
    }

    return {
      frame(dt) {
        if (!full && Math.max(...counts) >= cap) full = true;
        if (!full && (spawnT += dt) > 85) { spawnT = 0; balls.push({ r: 0, k: 0, d: coin(), p: 0 }); }
        for (const b of balls) {
          b.p += dt / (b.r < R ? 110 : 260);
          if (b.p < 1) continue;
          if (b.r < R) { b.k += b.d; b.r++; b.p = 0; b.d = coin(); }
          else { counts[b.k]++; b.done = true; }
        }
        balls = balls.filter(b => !b.done);
        if (full && !balls.length && (holdT += dt) > 1400) { counts.fill(0); full = false; holdT = 0; }
        draw();
      },
      still() {
        for (let i = 0; i < 130; i++) { let k = 0; for (let r = 0; r < R; r++) k += coin(); counts[k]++; }
        draw();
      },
    };
  });

  /* education — sorting algorithms at work: quicksort, insertion sort and selection sort, in turn */
  canvasAnim('c-sort', (ctx, W, H) => {
    const N = 24, STEP = 32, SWEEP = 25, PAD = 12;
    const swap = (A, i, j) => { [A[i], A[j]] = [A[j], A[i]]; };
    function* quick(A, lo = 0, hi = A.length - 1) {   // Lomuto partition
      if (lo >= hi) return;
      let i = lo;
      for (let j = lo; j < hi; j++) { yield [j, hi]; if (A[j] < A[hi]) swap(A, i++, j); }
      swap(A, i, hi); yield [i, hi];
      yield* quick(A, lo, i - 1);
      yield* quick(A, i + 1, hi);
    }
    function* insertion(A) {
      for (let i = 1; i < A.length; i++)
        for (let j = i; j > 0; j--) { yield [j - 1, j]; if (A[j - 1] > A[j]) swap(A, j - 1, j); else break; }
    }
    function* selection(A) {
      for (let i = 0; i < A.length - 1; i++) {
        let m = i;
        for (let j = i + 1; j < A.length; j++) { yield [m, j]; if (A[j] < A[m]) m = j; }
        swap(A, i, m); yield [i, m];
      }
    }
    const ALGOS = [quick, insertion, selection];
    let A, run, hl, phase, t, swept, algo = Math.random() * ALGOS.length | 0;

    function reset() {
      A = Array.from({ length: N }, (_, i) => i + 1);
      for (let i = N - 1; i > 0; i--) swap(A, i, Math.random() * (i + 1) | 0);
      algo = (algo + 1) % ALGOS.length;
      run = ALGOS[algo](A); phase = 'sort'; hl = []; t = 0; swept = 0;
    }
    reset();
    function draw() {
      ctx.clearRect(0, 0, W, H);
      const bw = (W - 2 * PAD) / N;
      A.forEach((v, i) => {
        const h = v / N * (H - 2 * PAD);
        ctx.fillStyle = hl.includes(i) ? '#050505' : i < swept ? 'rgba(5,5,5,.75)' : 'rgba(5,5,5,.28)';
        ctx.fillRect(PAD + i * bw + 1, H - PAD - h, bw - 2, h);
      });
    }
    return {
      frame(dt) {
        t += dt;
        if (phase === 'sort') {
          while (t > STEP) {
            t -= STEP;
            const r = run.next();
            if (r.done) { phase = 'sweep'; hl = []; t = 0; break; }
            hl = r.value;
          }
        } else {   // sorted: sweep across it once, then shuffle and run the next algorithm
          swept = t / SWEEP;
          if (t > N * SWEEP + 1200) reset();
        }
        draw();
      },
      still() { A.sort((a, b) => a - b); swept = N; hl = []; draw(); },
    };
  });

  /* links — modular times table: a chord from point i to point k·i (mod N), with k drifting */
  canvasAnim('c-times', (ctx, W, H) => {
    const N = 120, cx = W / 2, cy = H / 2, R = Math.min(W, H) * 0.44, KMAX = 34;
    let k = 2, dir = 1;
    function draw() {
      ctx.clearRect(0, 0, W, H);
      ctx.strokeStyle = 'rgba(5,5,5,.22)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, 6.2832); ctx.stroke();
      ctx.strokeStyle = 'rgba(5,5,5,.4)'; ctx.lineWidth = 0.6; ctx.beginPath();
      for (let i = 0; i < N; i++) {
        const a = 2 * Math.PI * i / N + Math.PI, b = 2 * Math.PI * k * i / N + Math.PI;
        ctx.moveTo(cx + R * Math.cos(a), cy + R * Math.sin(a));
        ctx.lineTo(cx + R * Math.cos(b), cy + R * Math.sin(b));
      }
      ctx.stroke();
    }
    return {
      frame(dt) {
        k += dir * dt * 0.00025;
        if (k > KMAX || k < 2) { dir = -dir; k = Math.max(2, Math.min(KMAX, k)); }
        draw();
      },
      still: draw,
    };
  });

  /* ───────── project covers: paper-on-ink, animated even with reduced motion ───────── */
  const paper = a => `rgba(244,244,239,${a})`;
  const MONO = '"Space Mono", ui-monospace, monospace';
  const hash = (a, b) => { const x = Math.sin(a * 127.1 + b * 311.7) * 43758.5453; return x - Math.floor(x); };

  /* Molinete-AI — the model writing the Quijote word by word, with its attention arcs */
  canvasAnim('c-molinete', (ctx, W, H) => {
    const WORDS = ('En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivía ' +
      'un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor.').split(' ');
    const FONT = `13px ${MONO}`, GAP = 9, BASE = H * 0.78, PAD = 18, CTX = 7, CHAR = 55;
    let xs = [], ws = [];
    const layout = () => {
      ctx.font = FONT; xs = []; ws = [];
      let x = 0;
      for (const w of WORDS) { const m = ctx.measureText(w).width; xs.push(x); ws.push(m); x += m + GAP; }
    };
    layout();
    if (document.fonts) document.fonts.ready.then(layout);
    let i = 0, t = 0, phase = 'type', off = 0;

    // softmax over the previous CTX words: pseudo-random scores plus a bias towards recent words
    const attn = i => {
      const e = [];
      for (let j = 1; j <= Math.min(i, CTX); j++) e.push(Math.exp(hash(i, j) * 3 - j * 0.25));
      const s = e.reduce((a, b) => a + b, 0);
      return e.map(v => v / s);
    };
    function draw(snap) {
      ctx.clearRect(0, 0, W, H);
      const target = Math.max(0, xs[i] + ws[i] - (W - 2 * PAD));
      off = snap ? target : off + (target - off) * 0.08;
      const X = j => PAD - off + xs[j];
      const typed = phase === 'type' ? Math.min(WORDS[i].length, Math.floor(t / CHAR)) : WORDS[i].length;

      if (phase !== 'type' && i > 0) {
        const a = phase === 'attend' ? Math.min(1, t / 350) : 1, xa = X(i) + ws[i] / 2, y = BASE - 16;
        attn(i).forEach((p, k) => {
          const j = i - 1 - k, xb = X(j) + ws[j] / 2;
          ctx.beginPath(); ctx.moveTo(xa, y);
          ctx.quadraticCurveTo((xa + xb) / 2, y - 10 - (xa - xb) * 0.34, xb, y);
          ctx.strokeStyle = paper(a * (0.15 + p * 0.85)); ctx.lineWidth = 0.6 + p * 3.2; ctx.stroke();
        });
      }
      ctx.font = FONT;
      for (let j = 0; j <= i; j++) {
        const x = X(j);
        if (x > W || x + ws[j] < 0) continue;
        ctx.fillStyle = paper(j === i ? 1 : 0.5);
        ctx.fillText(j === i ? WORDS[j].slice(0, typed) : WORDS[j], x, BASE);
      }
      if (phase === 'type') {
        ctx.fillStyle = paper(0.9);
        ctx.fillRect(X(i) + ctx.measureText(WORDS[i].slice(0, typed)).width + 2, BASE - 11, 7, 13);
      }
    }
    return {
      frame(dt) {
        t += dt;
        if (phase === 'type' && t > WORDS[i].length * CHAR + 120) { phase = 'attend'; t = 0; }
        else if (phase === 'attend' && t > 900) {
          if (i < WORDS.length - 1) { i++; phase = 'type'; } else phase = 'rest';
          t = 0;
        } else if (phase === 'rest' && t > 2200) { i = 0; off = 0; phase = 'type'; t = 0; }
        draw();
      },
      still() { i = 9; phase = 'rest'; draw(true); },
    };
  }, true);

  /* Sanghelios — blood stock so far and a 14-day forecast with its uncertainty band */
  canvasAnim('c-sanghelios', (ctx, W, H) => {
    const top = 18, bot = H - 18, left = 12, nowX = W * 0.6, HIST = 30, FC = 14, TH = 0.34;
    const pxDay = (nowX - left) / HIST;
    const trend = d => 0.52 + 0.2 * Math.sin(d * 0.21) + 0.11 * Math.sin(d * 0.53 + 1.3);
    const obs = d => trend(d) + (hash(d, 7) - 0.5) * 0.1;   // what was measured on day d
    const Y = v => top + (1 - v) * (bot - top);
    let now = 40 + Math.random() * 60, pulse = 0;

    function draw() {
      ctx.clearRect(0, 0, W, H);
      const X = d => nowX + (d - now) * pxDay, d0 = Math.floor(now);
      const vNow = obs(d0) + (obs(d0 + 1) - obs(d0)) * (now - d0);
      const fc = d => trend(d) + (vNow - trend(now)) * Math.exp(-(d - now) / 2);
      const band = d => 0.025 + 0.012 * (d - now);

      ctx.setLineDash([3, 4]); ctx.lineWidth = 1;
      ctx.strokeStyle = paper(0.4); ctx.beginPath(); ctx.moveTo(left, Y(TH)); ctx.lineTo(W - left, Y(TH)); ctx.stroke();
      ctx.strokeStyle = paper(0.22); ctx.beginPath(); ctx.moveTo(nowX, top - 8); ctx.lineTo(nowX, bot); ctx.stroke();
      ctx.setLineDash([]);

      ctx.beginPath();   // uncertainty band
      for (let d = now; d <= now + FC; d += 0.25) ctx.lineTo(X(d), Y(fc(d) + band(d)));
      for (let d = now + FC; d >= now; d -= 0.25) ctx.lineTo(X(d), Y(fc(d) - band(d)));
      ctx.fillStyle = paper(0.1); ctx.fill();

      ctx.setLineDash([4, 3]); ctx.strokeStyle = paper(0.85); ctx.lineWidth = 1.2; ctx.beginPath();
      for (let d = now; d <= now + FC; d += 0.25) ctx.lineTo(X(d), Y(fc(d)));
      ctx.stroke(); ctx.setLineDash([]);

      ctx.strokeStyle = paper(0.9); ctx.lineWidth = 1.3; ctx.beginPath();
      for (let d = Math.ceil(now - HIST); d <= d0; d++) ctx.lineTo(X(d), Y(obs(d)));
      ctx.lineTo(nowX, Y(vNow)); ctx.stroke();
      ctx.fillStyle = paper(0.55);
      for (let d = Math.ceil(now - HIST); d <= d0; d++) { ctx.beginPath(); ctx.arc(X(d), Y(obs(d)), 1.3, 0, 6.2832); ctx.fill(); }

      // first day the forecast drops below the shortage line
      for (let d = now; d <= now + FC; d += 0.25) {
        if (fc(d) >= TH) continue;
        const x = X(d), y = Y(fc(d)), p = pulse % 1;
        ctx.strokeStyle = paper(1 - p); ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(x, y, 3 + p * 9, 0, 6.2832); ctx.stroke();
        ctx.fillStyle = paper(1); ctx.beginPath(); ctx.arc(x, y, 2.4, 0, 6.2832); ctx.fill();
        break;
      }
    }
    return {
      frame(dt) { now += dt / 650; pulse += dt / 1100; draw(); },
      still: draw,
    };
  }, true);

  /* InvestigIA — the agent graph: plan → search → read (→ search again) → write → plan */
  canvasAnim('c-investigia', (ctx, W, H) => {
    const N = { plan: [W * 0.17, H * 0.54], search: [W * 0.5, H * 0.28], read: [W * 0.83, H * 0.54], write: [W * 0.5, H * 0.82] };
    const HW = 27, HH = 10, BEND = { 'search>read': 12, 'read>search': 12 };
    const ROUTE = ['plan', 'search', 'read', 'search', 'read', 'write', 'plan'], DWELL = 420, MOVE = 700;

    const clip = (p, q) => {   // where the segment p→q leaves the box around p
      const dx = q[0] - p[0], dy = q[1] - p[1], s = Math.min((HW + 3) / Math.abs(dx || 1e-9), (HH + 3) / Math.abs(dy || 1e-9));
      return [p[0] + dx * s, p[1] + dy * s];
    };
    const edges = {};
    for (const key of ['plan>search', 'search>read', 'read>search', 'read>write', 'write>plan']) {
      const [a, b] = key.split('>'), A = clip(N[a], N[b]), B = clip(N[b], N[a]);
      const len = Math.hypot(B[0] - A[0], B[1] - A[1]), c = BEND[key] || 0;
      edges[key] = [A, [(A[0] + B[0]) / 2 - (B[1] - A[1]) / len * c, (A[1] + B[1]) / 2 + (B[0] - A[0]) / len * c], B];
    }
    const bez = ([A, C, B], u) => [
      (1 - u) ** 2 * A[0] + 2 * (1 - u) * u * C[0] + u * u * B[0],
      (1 - u) ** 2 * A[1] + 2 * (1 - u) * u * C[1] + u * u * B[1],
    ];
    let s = 0, t = 0;

    function draw() {
      ctx.clearRect(0, 0, W, H);
      const moving = t > DWELL, u = Math.min(1, (t - DWELL) / MOVE);
      const active = moving ? ROUTE[s] + '>' + ROUTE[s + 1] : null;
      for (const [key, e] of Object.entries(edges)) {
        const [A, C, B] = e, on = key === active;
        ctx.strokeStyle = paper(on ? 0.7 : 0.28); ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(...A); ctx.quadraticCurveTo(...C, ...B); ctx.stroke();
        const ang = Math.atan2(B[1] - C[1], B[0] - C[0]);
        ctx.fillStyle = paper(on ? 0.7 : 0.35); ctx.beginPath(); ctx.moveTo(...B);
        ctx.lineTo(B[0] - 6 * Math.cos(ang - 0.4), B[1] - 6 * Math.sin(ang - 0.4));
        ctx.lineTo(B[0] - 6 * Math.cos(ang + 0.4), B[1] - 6 * Math.sin(ang + 0.4)); ctx.fill();
      }
      if (moving) for (let k = 0; k < 5; k++) {
        const [x, y] = bez(edges[active], Math.max(0, u - k * 0.04));
        ctx.fillStyle = paper(1 - k * 0.2); ctx.beginPath(); ctx.arc(x, y, 2.6 - k * 0.35, 0, 6.2832); ctx.fill();
      }
      ctx.font = `10px ${MONO}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      for (const [name, [x, y]] of Object.entries(N)) {
        const here = !moving && ROUTE[s] === name;
        ctx.beginPath();
        ctx.roundRect ? ctx.roundRect(x - HW, y - HH, HW * 2, HH * 2, 4) : ctx.rect(x - HW, y - HH, HW * 2, HH * 2);
        ctx.fillStyle = here ? paper(1) : '#050505'; ctx.fill();
        ctx.strokeStyle = paper(here ? 1 : 0.7); ctx.lineWidth = 1; ctx.stroke();
        ctx.fillStyle = here ? '#050505' : paper(0.85); ctx.fillText(name, x, y + 0.5);
      }
      ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    }
    return {
      frame(dt) {
        t += dt;
        if (t > DWELL + MOVE) {
          t = 0; s++;
          if (s === ROUTE.length - 1) s = 0;
        }
        draw();
      },
      still: draw,
    };
  }, true);

  /* Krylov on GPU — C = A × B one thread block at a time: each thread of the 3×3 tile
     walks its row of A and its column of B, accumulating one entry of C */
  canvasAnim('c-krylov', (ctx, W, H) => {
    const n = 6, TILE = 3, TILES = (n / TILE) ** 2, STEP = 150, HOLD = 1400;
    const s = Math.min((W - 90) / 3, H - 44), cs = s / n, g = (W - 3 * s) / 4, y0 = (H - s) / 2;
    const XA = g, XB = 2 * g + s, XC = 3 * g + 2 * s;
    const done = new Array(n * n).fill(false);
    let tile = 0, k = 0, t = 0, seed = Math.random() * 100;
    const val = (m, i, j) => 0.1 + 0.32 * hash(i + seed + m * 17, j + m * 5);

    const bracket = x => {
      ctx.strokeStyle = paper(0.7); ctx.lineWidth = 1.2; ctx.beginPath();
      ctx.moveTo(x - 1, y0 - 4); ctx.lineTo(x - 5, y0 - 4); ctx.lineTo(x - 5, y0 + s + 4); ctx.lineTo(x - 1, y0 + s + 4);
      ctx.moveTo(x + s + 1, y0 - 4); ctx.lineTo(x + s + 5, y0 - 4); ctx.lineTo(x + s + 5, y0 + s + 4); ctx.lineTo(x + s + 1, y0 + s + 4);
      ctx.stroke();
    };
    const cell = (x, i, j, a) => { ctx.fillStyle = paper(a); ctx.fillRect(x + j * cs + 1, y0 + i * cs + 1, cs - 2, cs - 2); };

    function draw() {
      ctx.clearRect(0, 0, W, H);
      const active = tile < TILES, tr = (tile / (n / TILE) | 0) * TILE, tc = (tile % (n / TILE)) * TILE;
      const inRows = i => active && i >= tr && i < tr + TILE, inCols = j => active && j >= tc && j < tc + TILE;
      const p = (k + t / STEP) / n;
      for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
        cell(XA, i, j, inRows(i) && j === k ? 0.95 : val(0, i, j));
        cell(XB, i, j, inCols(j) && i === k ? 0.95 : val(1, i, j));
        if (inRows(i) && inCols(j)) cell(XC, i, j, 0.1 + 0.55 * p);
        else cell(XC, i, j, done[i * n + j] ? 0.2 + val(2, i, j) : 0.05);
      }
      if (active) {   // the rows / columns this thread block is reading, and the tile it writes
        ctx.strokeStyle = paper(0.85); ctx.lineWidth = 1;
        ctx.strokeRect(XA + 0.5, y0 + tr * cs + 0.5, s - 1, TILE * cs - 1);
        ctx.strokeRect(XB + tc * cs + 0.5, y0 + 0.5, TILE * cs - 1, s - 1);
        ctx.strokeRect(XC + tc * cs + 0.5, y0 + tr * cs + 0.5, TILE * cs - 1, TILE * cs - 1);
      }
      bracket(XA); bracket(XB); bracket(XC);
      ctx.font = `16px ${MONO}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = paper(0.75);
      ctx.fillText('×', (XA + s + XB) / 2, y0 + s / 2);
      ctx.fillText('=', (XB + s + XC) / 2, y0 + s / 2);
      ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    }
    return {
      frame(dt) {
        t += dt;
        if (tile < TILES) {
          if (t > STEP) {
            t = 0;
            if (++k === n) {
              for (let i = 0; i < TILE; i++) for (let j = 0; j < TILE; j++)
                done[((tile / (n / TILE) | 0) * TILE + i) * n + (tile % (n / TILE)) * TILE + j] = true;
              k = 0; tile++;
            }
          }
        } else if (t > HOLD) { done.fill(false); tile = 0; t = 0; seed = Math.random() * 100; }
        draw();
      },
      still: draw,
    };
  }, true);

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
