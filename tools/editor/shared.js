// Utilidades compartidas por el editor del blog y el del README.

export const $ = (s, root = document) => root.querySelector(s);
export const $$ = (s, root = document) => [...root.querySelectorAll(s)];
export const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

export async function api(method, url, body, raw = false) {
  const r = await fetch(url, { method, body: body === undefined ? undefined : raw ? body : JSON.stringify(body) });
  const out = (r.headers.get('content-type') || '').includes('json') ? await r.json() : await r.text();
  if (!r.ok) throw Object.assign(new Error(out.error || out || r.statusText), { log: out.log });
  return out;
}

// iconos (trazos al estilo Lucide)
const P = {
  pen: '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
  upload: '<path d="M12 15V3M7 8l5-5 5 5"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>',
  rocket: '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1Z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.9A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2Z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/>',
  more: '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>',
  external: '<path d="M15 3h6v6M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
  monitor: '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
  phone: '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/>',
  panel: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M15 3v18"/>',
  bold: '<path d="M6 4h8a4 4 0 0 1 0 8H6zM6 12h9a4 4 0 0 1 0 8H6z"/>',
  italic: '<path d="M19 4h-9M14 20H5M15 4 9 20"/>',
  heading: '<path d="M6 12h12M6 20V4M18 20V4"/>',
  link: '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
  code: '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>',
  quote: '<path d="M3 21c3 0 7-1 7-8V5c0-1.3-.8-2-2-2H4c-1.3 0-2 .8-2 2v6c0 1.3.8 2 2 2h1c0 2-.5 3.5-2 4.5ZM15 21c3 0 7-1 7-8V5c0-1.3-.8-2-2-2h-4c-1.3 0-2 .8-2 2v6c0 1.3.8 2 2 2h1c0 2-.5 3.5-2 4.5Z"/>',
  list: '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
  olist: '<path d="M10 6h11M10 12h11M10 18h11M4 6h1v4M4 10h2M6 18H4c0-1 2-2 2-3s-1-1.5-2-1"/>',
  sigma: '<path d="M18 7V4H6l6 8-6 8h12v-3"/>',
  table: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
  image: '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/>',
  trash: '<path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>',
  grip: '<circle cx="9" cy="6" r="1"/><circle cx="9" cy="12" r="1"/><circle cx="9" cy="18" r="1"/><circle cx="15" cy="6" r="1"/><circle cx="15" cy="12" r="1"/><circle cx="15" cy="18" r="1"/>',
  eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
  eyeOff: '<path d="M9.9 4.2A9.1 9.1 0 0 1 12 4c6.5 0 10 8 10 8a18 18 0 0 1-2.2 3.2M6.6 6.6A17.6 17.6 0 0 0 2 12s3.5 8 10 8a9.7 9.7 0 0 0 5.4-1.6M2 2l20 20M14.1 14.1a3 3 0 1 1-4.2-4.2"/>',
  x: '<path d="M18 6 6 18M6 6l12 12"/>',
  copy: '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
  download: '<path d="M12 3v12M7 10l5 5 5-5"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>',
  github: '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.1-1.3-.3-2.5-1-3.5.3-1.2.3-2.4 0-3.5 0 0-1 0-3 1.5a10.6 10.6 0 0 0-6 0C8 2 7 2 7 2c-.3 1.1-.3 2.3 0 3.5A5.4 5.4 0 0 0 6 9c0 3.5 3 5.5 6 5.5-.4.5-.8 1.1-1 1.7-.2.6-.2 1.2-.1 1.8v4"/><path d="M9 18c-4.5 2-5-2-7-2"/>',
  file: '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5Z"/><path d="M14 2v6h6"/>',
  settings: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 0 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 0 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 0 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 0 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1Z"/>',
  text: '<path d="M4 7V4h16v3M9 20h6M12 4v16"/>',
  mic: '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/>',
  folder: '<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.7-.9l-.8-1.2A2 2 0 0 0 7.9 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"/>',
  layout: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/>',
  footer: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 15h18"/>',
  calendar: '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
};
export const icon = (name, cls = '') => `<svg class="i ${cls}" viewBox="0 0 24 24" aria-hidden="true">${P[name] || ''}</svg>`;
// <i data-i="nombre"></i> en el HTML se reemplaza por el icono
export const hydrateIcons = (root = document) => $$('i[data-i]', root).forEach(el => { el.outerHTML = icon(el.dataset.i); });

export function toast(msg, kind = '') {
  let box = $('.toasts');
  if (!box) { box = document.createElement('div'); box.className = 'toasts'; box.setAttribute('role', 'status'); document.body.append(box); }
  const t = document.createElement('div'); t.className = 'toast ' + kind; t.textContent = msg;
  box.append(t); setTimeout(() => t.remove(), kind === 'err' ? 6000 : 2600);
}

// indicador «Guardado / Sin guardar / Guardando…»
export function saveState(el) {
  const labels = { saved: 'Guardado', dirty: 'Sin guardar', saving: 'Guardando…', error: 'Error al guardar' };
  return s => { el.dataset.s = s; el.textContent = labels[s]; };
}

export const debounce = (fn, ms) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; };

// divisor arrastrable entre dos paneles; recuerda la proporción
export function splitter(handle, left, key) {
  const saved = Number(localStorage.getItem(key));
  if (saved) { left.style.flex = `0 0 ${saved}%`; }
  handle.addEventListener('pointerdown', e => {
    e.preventDefault();
    const box = left.parentElement.getBoundingClientRect(), start = left.getBoundingClientRect().left;
    handle.classList.add('drag'); document.body.classList.add('resizing');
    const move = ev => {
      const pct = Math.min(75, Math.max(25, ((ev.clientX - start) / (box.right - start)) * 100));
      left.style.flex = `0 0 ${pct}%`; localStorage.setItem(key, pct.toFixed(1));
    };
    const up = () => { handle.classList.remove('drag'); document.body.classList.remove('resizing'); removeEventListener('pointermove', move); removeEventListener('pointerup', up); };
    addEventListener('pointermove', move); addEventListener('pointerup', up);
  });
  handle.addEventListener('dblclick', () => { left.style.flex = ''; localStorage.removeItem(key); });
}

// menús «⋯»: abre/cierra y se cierra al hacer clic fuera
export function menus() {
  $$('.menu').forEach(m => {
    const btn = $('[data-menu]', m);
    btn.setAttribute('aria-haspopup', 'true'); btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', e => { e.stopPropagation(); const open = !m.classList.contains('open'); $$('.menu.open').forEach(x => x.classList.remove('open')); m.classList.toggle('open', open); btn.setAttribute('aria-expanded', open); });
    $('.menu-list', m).addEventListener('click', () => { m.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); });
  });
  addEventListener('click', () => $$('.menu.open').forEach(m => m.classList.remove('open')));
  addEventListener('keydown', e => { if (e.key === 'Escape') $$('.menu.open').forEach(m => m.classList.remove('open')); });
}

// arrastrar para reordenar los hijos [draggable] de una lista
export function sortable(list, onMove) {
  let from = null;
  list.addEventListener('dragstart', e => { const it = e.target.closest('[data-idx]'); if (!it) return; from = +it.dataset.idx; it.classList.add('dragging'); e.dataTransfer.effectAllowed = 'move'; });
  list.addEventListener('dragend', e => { e.target.closest('[data-idx]')?.classList.remove('dragging'); $$('.drop-before,.drop-after', list).forEach(x => x.classList.remove('drop-before', 'drop-after')); });
  list.addEventListener('dragover', e => {
    const it = e.target.closest('[data-idx]'); if (from === null || !it) return;
    e.preventDefault();
    const after = e.clientY > it.getBoundingClientRect().top + it.offsetHeight / 2;
    $$('.drop-before,.drop-after', list).forEach(x => x.classList.remove('drop-before', 'drop-after'));
    it.classList.add(after ? 'drop-after' : 'drop-before');
  });
  list.addEventListener('drop', e => {
    const it = e.target.closest('[data-idx]'); if (from === null || !it) return;
    e.preventDefault();
    let to = +it.dataset.idx + (it.classList.contains('drop-after') ? 1 : 0);
    if (to > from) to--;
    const f = from; from = null;
    if (to !== f) onMove(f, to);
  });
}
export const moveItem = (arr, from, to) => arr.splice(to, 0, arr.splice(from, 1)[0]);
