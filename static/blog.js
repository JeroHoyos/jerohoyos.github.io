/* Blog: portadas animadas con el mismo estilo que las de los proyectos (papel sobre tinta).
   Uso: <canvas class="proj-canvas" data-cover="attention"></canvas>
   Tipos: attention · sine · power · voice · life */
(() => {
  const DPR = Math.min(devicePixelRatio || 1, 2);
  const paper = a => `rgba(244,244,239,${a})`;
  const MONO = '"Space Mono", ui-monospace, monospace';
  const hash = (a, b) => { const x = Math.sin(a * 127.1 + b * 311.7) * 43758.5453; return x - Math.floor(x); };

  const COVERS = {
    /* matriz de atención: una fila nueva cada vez, softmax con máscara causal */
    attention(ctx, W, H) {
      const n = 10, s = Math.min((H - 30) / n, (W - 40) / n), x0 = (W - n * s) / 2, y0 = (H - n * s) / 2;
      let row = 0, t = 0, seed = 1;
      const w = (i, j) => { const e = []; for (let k = 0; k <= i; k++) e.push(Math.exp(hash(i + seed, k) * 3 + (k === i ? 1 : 0))); const S = e.reduce((a, b) => a + b); return j <= i ? e[j] / S : 0; };
      return { frame(dt) {
        t += dt; if (t > 260) { t = 0; row++; if (row > n + 6) { row = 0; seed++; } }
        ctx.clearRect(0, 0, W, H);
        for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
          const on = i < row, a = j > i ? 0.04 : on ? 0.12 + Math.sqrt(w(i, j)) * 0.88 : 0.07;
          ctx.fillStyle = paper(a); ctx.fillRect(x0 + j * s + 1, y0 + i * s + 1, s - 2, s - 2);
        }
        if (row < n) { ctx.strokeStyle = paper(.9); ctx.strokeRect(x0 - 1, y0 + row * s, n * s + 2, s); }
        ctx.font = `10px ${MONO}`; ctx.fillStyle = paper(.5); ctx.fillText('softmax(QKᵀ/√d)', 10, H - 10);
      } };
    },
    /* embeddings posicionales: sin/cos a distintas frecuencias, desplazándose */
    sine(ctx, W, H) {
      let t = 0; const D = 7;
      return { frame(dt) {
        t += dt / 1000; ctx.clearRect(0, 0, W, H);
        for (let d = 0; d < D; d++) {
          const y = 18 + (d + .5) * (H - 36) / D, amp = (H - 36) / D * .38, f = 1 / Math.pow(2.1, d) * 0.12;
          ctx.beginPath();
          for (let x = 0; x <= W; x += 3) { const v = (d % 2 ? Math.cos : Math.sin)((x + t * 40) * f); x ? ctx.lineTo(x, y - v * amp) : ctx.moveTo(x, y - v * amp); }
          ctx.strokeStyle = paper(.25 + .1 * (D - d)); ctx.lineWidth = 1.2; ctx.stroke();
        }
        const px = (W * .62 + t * 18) % W;
        ctx.strokeStyle = paper(.85); ctx.setLineDash([3, 4]); ctx.beginPath(); ctx.moveTo(px, 8); ctx.lineTo(px, H - 8); ctx.stroke(); ctx.setLineDash([]);
        ctx.font = `10px ${MONO}`; ctx.fillStyle = paper(.6); ctx.fillText('pos ' + Math.floor(px / 6), px + 5, 18);
      } };
    },
    /* método de la potencia: A·v repetido converge al autovector dominante */
    power(ctx, W, H) {
      const cx = W / 2, cy = H / 2, R = Math.min(W, H) * .38;
      const A = [[2, 1], [1, 1.4]], ev = Math.atan2(0.79, 1);
      let v = [Math.cos(2.4), Math.sin(2.4)], trail = [], t = 0;
      return { frame(dt) {
        t += dt;
        if (t > 520) { t = 0; let x = A[0][0] * v[0] + A[0][1] * v[1], y = A[1][0] * v[0] + A[1][1] * v[1], m = Math.hypot(x, y); trail.push(v); v = [x / m, y / m]; if (trail.length > 9) { const a = Math.random() * Math.PI * 2; v = [Math.cos(a), Math.sin(a)]; trail = []; } }
        ctx.clearRect(0, 0, W, H);
        ctx.strokeStyle = paper(.18); ctx.beginPath(); ctx.arc(cx, cy, R, 0, 7); ctx.stroke();
        ctx.setLineDash([4, 5]); ctx.beginPath(); ctx.moveTo(cx - Math.cos(ev) * R * 1.3, cy + Math.sin(ev) * R * 1.3); ctx.lineTo(cx + Math.cos(ev) * R * 1.3, cy - Math.sin(ev) * R * 1.3); ctx.stroke(); ctx.setLineDash([]);
        const arrow = (u, a) => { const x = cx + u[0] * R, y = cy - u[1] * R; ctx.strokeStyle = paper(a); ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(x, y); ctx.stroke(); ctx.fillStyle = paper(a); ctx.beginPath(); ctx.arc(x, y, 3, 0, 7); ctx.fill(); };
        trail.forEach((u, i) => arrow(u, .12 + .5 * i / trail.length)); arrow(v, .95);
        ctx.font = `10px ${MONO}`; ctx.fillStyle = paper(.6); ctx.fillText('v := Av / ‖Av‖   k=' + trail.length, 10, H - 10);
      } };
    },
    /* charla: onda de voz que se mueve como un ecualizador */
    voice(ctx, W, H) {
      let t = 0; const N = 48;
      return { frame(dt) {
        t += dt / 1000; ctx.clearRect(0, 0, W, H);
        const bw = (W - 40) / N;
        for (let i = 0; i < N; i++) {
          const env = Math.sin(Math.PI * i / N), h = (H * .62) * env * (.25 + .75 * Math.abs(Math.sin(t * 3 + i * .45) * Math.cos(t * 1.7 + i * .13)));
          ctx.fillStyle = paper(.25 + .7 * env); ctx.fillRect(20 + i * bw + 1, H / 2 - h / 2, bw - 2, h);
        }
        ctx.font = `10px ${MONO}`; ctx.fillStyle = paper(.6); ctx.fillText('● rec', 10, 18);
      } };
    },
    /* juego de la vida en miniatura, por si un post no tiene portada propia */
    life(ctx, W, H) {
      const S = 8, c = Math.ceil(W / S), r = Math.ceil(H / S); let g = new Uint8Array(c * r).map(() => Math.random() < .25), t = 0;
      return { frame(dt) {
        t += dt; if (t > 140) { t = 0; const n = new Uint8Array(c * r); let alive = 0;
          for (let y = 0; y < r; y++) for (let x = 0; x < c; x++) { let k = 0; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) if (dx || dy) k += g[((y + dy + r) % r) * c + (x + dx + c) % c]; const i = y * c + x; n[i] = k === 3 || (k === 2 && g[i]); alive += n[i]; }
          g = alive < c * r * .04 ? n.map(() => Math.random() < .25) : n; }
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = paper(.75);
        for (let i = 0; i < g.length; i++) if (g[i]) ctx.fillRect((i % c) * S + 1, ((i / c) | 0) * S + 1, S - 2, S - 2);
      } };
    },
  };

  const anims = [];
  document.querySelectorAll('canvas[data-cover]').forEach(cv => {
    const make = COVERS[cv.dataset.cover] || COVERS.life, ctx = cv.getContext('2d'), a = { st: null, vis: false };
    const fit = () => { const w = cv.clientWidth, h = cv.clientHeight; if (w < 2 || h < 2) return; cv.width = w * DPR; cv.height = h * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0); a.st = make(ctx, w, h); a.st.frame(16); };
    new ResizeObserver(fit).observe(cv);
    new IntersectionObserver(([e]) => { a.vis = e.isIntersecting; }, { rootMargin: '120px' }).observe(cv);
    anims.push(a);
  });
  let last = performance.now();
  (function loop(now) {
    requestAnimationFrame(loop);
    const dt = now - last; if (dt < 31 || document.hidden) return; last = now;
    for (const a of anims) if (a.vis && a.st) a.st.frame(Math.min(dt, 50));
  })(last);
})();

/* copiar enlace del post y filtro por etiqueta en la lista del blog */
(() => {
  document.querySelectorAll('[data-copy-link]').forEach(b => b.addEventListener('click', () => {
    if (!navigator.clipboard) return;
    navigator.clipboard.writeText(location.href.split('#')[0]).then(() => {
      b.classList.add('copied');
      setTimeout(() => b.classList.remove('copied'), 1600);
    });
  }));
  document.querySelectorAll('[data-print]').forEach(b => b.addEventListener('click', () => print()));

  const chips = document.querySelectorAll('.blog-filter [data-tag]');
  const apply = tag => {
    chips.forEach(c => c.setAttribute('aria-pressed', c.dataset.tag === tag));
    document.querySelectorAll('.blist [data-tags]').forEach(li => { li.hidden = !!tag && !li.dataset.tags.split(' ').includes(tag); });
  };
  chips.forEach(c => c.addEventListener('click', () => {
    apply(c.dataset.tag);
    history.replaceState(null, '', c.dataset.tag ? '#' + c.dataset.tag : location.pathname);
  }));
  if (chips.length) apply(decodeURIComponent(location.hash.slice(1)));
})();
