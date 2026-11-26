import { markdown } from '/tools/markdown.mjs';
import { renderReadme, renderBlocks, rawBase, badgeUrl } from '/tools/perfil.mjs';
import { $, $$, esc, api, icon, hydrateIcons, toast, saveState, debounce, splitter, menus, sortable, moveItem } from './shared.js';

hydrateIcons(); menus();
const setSave = saveState($('#save'));
let data, sel = 'header', dirty = false;

const TYPES = {
  text: { name: 'Texto', icon: 'text' },
  talks: { name: 'Charlas', icon: 'mic', item: 'talk', add: 'Añadir charla', blank: { venue: '', title: '', url: '' } },
  projects: { name: 'Proyectos', icon: 'folder', item: 'project', add: 'Añadir proyecto', blank: { name: '', url: '', desc: '' } },
  list: { name: 'Lista', icon: 'list', item: 'list', add: 'Añadir elemento', blank: { text: '' } },
};
const SWATCHES = ['21364D', '0D1117', '4F46E5', '2EA043', 'D97757', 'E11D48'];
const fullSrc = src => (!src ? '' : /^(https?:|data:)/.test(src) ? src : rawBase(data) + src.replace(/^\.?\//, ''));

/* ───────── guardar solo ───────── */
const autosave = debounce(async () => {
  setSave('saving');
  try { await api('PUT', '/api/perfil', data); dirty = false; setSave('saved'); }
  catch (e) { setSave('error'); toast(e.message, 'err'); }
}, 800);
function changed({ outline = false } = {}) {
  dirty = true; setSave('dirty'); autosave(); preview();
  if (outline) renderOutline();
}
addEventListener('beforeunload', e => { if (dirty) e.preventDefault(); });
addEventListener('keydown', e => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') { e.preventDefault(); autosave(); } });

/* ───────── esquema de bloques ───────── */
function renderOutline() {
  const row = (key, ic, label, { idx, hidden, fixed } = {}) => `
    <li class="ol-item${fixed ? ' fixed' : ''}${hidden ? ' is-hidden' : ''}" ${idx !== undefined ? `data-idx="${idx}"` : ''} aria-current="${String(sel) === String(key)}">
      <span class="grip" title="Arrastra para mover">${icon('grip')}</span>
      <button type="button" class="sel" data-sel="${key}">${icon(ic)}<span>${esc(label)}</span></button>
      ${hidden ? `<span class="off" title="Oculta en el README">${icon('eyeOff')}</span>` : ''}
    </li>`;
  $('#outline').innerHTML =
    row('header', 'layout', 'Encabezado', { fixed: true }) + '<li class="ol-sep" aria-hidden="true"></li>' +
    data.sections.map((s, i) => row(i, TYPES[s.type].icon, s.title || TYPES[s.type].name, { idx: i, hidden: s.hidden })).join('') +
    '<li class="ol-sep" aria-hidden="true"></li>' + row('footer', 'footer', 'Pie de página', { fixed: true });
}
const outline = $('#outline');
outline.addEventListener('click', e => { const b = e.target.closest('[data-sel]'); if (b) select(isNaN(b.dataset.sel) ? b.dataset.sel : +b.dataset.sel); });
outline.addEventListener('pointerdown', e => { const li = e.target.closest('.grip') && e.target.closest('[data-idx]'); if (li) li.draggable = true; });
outline.addEventListener('dragend', e => { e.target.draggable = false; });
sortable(outline, (from, to) => {
  const cur = typeof sel === 'number' ? data.sections[sel] : null;
  moveItem(data.sections, from, to);
  if (cur) sel = data.sections.indexOf(cur);
  changed({ outline: true });
});

$$('[data-add]').forEach(b => b.onclick = () => {
  const t = b.dataset.add;
  data.sections.push(t === 'text' ? { type: t, title: '', body: '' } : { type: t, title: '', items: [{ ...TYPES[t].blank }] });
  changed({ outline: true });
  select(data.sections.length - 1);
  $('.b-title')?.focus();
});

/* ───────── editor del bloque elegido ───────── */
function select(key) {
  sel = key;
  renderOutline(); renderBlock(); highlight(true);
}
function field(label, html, hint = '') { return `<label class="field"><span>${label}${hint ? ` <small>${hint}</small>` : ''}</span>${html}</label>`; }

function renderBlock() {
  const box = $('#block'), isSec = typeof sel === 'number', s = isSec ? data.sections[sel] : null;
  $('#block-kind').innerHTML = sel === 'header' ? `${icon('layout')}Encabezado` : sel === 'footer' ? `${icon('footer')}Pie de página` : `${icon(TYPES[s.type].icon)}Sección · ${TYPES[s.type].name}`;
  $('#btn-hide').hidden = $('#btn-del').hidden = !isSec;
  if (isSec) $('#btn-hide').lastElementChild.textContent = s.hidden ? 'Mostrar' : 'Ocultar';

  if (sel === 'header') {
    const h = data.header;
    box.innerHTML = `
      <div class="section"><h3>Imagen o GIF</h3>
        <div class="img-field"><div class="img-thumb" id="thumb"></div>
          <div class="field">${field('Ruta en el repo del perfil o URL', `<input type="text" data-k="header.image" value="${esc(h.image)}">`)}
            <div class="range"><input type="range" min="60" max="600" step="10" data-k="header.imageWidth" value="${esc(h.imageWidth || 300)}" aria-label="Ancho de la imagen"><output id="w-out">${h.imageWidth || 300} px</output></div></div></div>
        ${field('Texto alternativo', `<input type="text" data-k="header.imageAlt" value="${esc(h.imageAlt)}">`, 'para lectores de pantalla')}
      </div>
      <div class="section"><h3>Título</h3>
        ${field('Título', `<input type="text" data-k="header.title" value="${esc(h.title)}">`)}
        ${field('Subtítulo', `<input type="text" data-k="header.subtitle" value="${esc(h.subtitle)}" placeholder="Machine learning · Rust · gatos">`, 'opcional')}
      </div>
      <div class="section"><h3>Insignias <small>los botones de enlaces</small></h3>
        <div class="color-field"><input type="color" id="badge-color" value="#${esc((h.badgeColor || '21364D').replace('#', ''))}" aria-label="Color de las insignias">
          <div class="swatches">${SWATCHES.map(c => `<button type="button" data-sw="${c}" style="background:#${c}" aria-label="Color #${c}"></button>`).join('')}</div></div>
        <div class="items" data-list="header.badges" data-kind="badge"></div>
        <button type="button" class="btn sm add-item" data-additem="header.badges">${icon('plus')}Añadir insignia</button>
      </div>`;
    $('#thumb').style.backgroundImage = `url("${fullSrc(h.image)}")`;
  } else if (sel === 'footer') {
    box.innerHTML = `<div class="section">${field('Texto pequeño centrado al final', `<input type="text" data-k="footer" value="${esc(data.footer)}">`, 'admite HTML, p. ej. enlaces')}<p class="hint">Déjalo vacío para quitar el pie (y la línea de arriba).</p></div>`;
  } else {
    const T = TYPES[s.type];
    box.innerHTML = `<input type="text" class="b-title" data-k="sections.${sel}.title" value="${esc(s.title)}" placeholder="Título de la sección (opcional)" aria-label="Título de la sección">` +
      (s.type === 'text'
        ? `<textarea class="text-area" data-k="sections.${sel}.body" aria-label="Texto" placeholder="Escribe aquí. Admite **Markdown**.">${esc(s.body)}</textarea><p class="hint">Admite Markdown: **negrita**, [enlaces](https://…), listas…</p>`
        : `<div class="items" data-list="sections.${sel}.items" data-kind="${T.item}"></div><button type="button" class="btn sm add-item" data-additem="sections.${sel}.items">${icon('plus')}${T.add}</button>`);
  }
  $$('[data-list]', box).forEach(bindList);
}

// los campos simples escriben directo en `data`
const get = path => path.split('.').reduce((o, k) => o?.[k], data);
const set = (path, v) => { const ks = path.split('.'), last = ks.pop(); ks.reduce((o, k) => (o[k] ??= {}), data)[last] = v; };
$('#block').addEventListener('input', e => {
  const k = e.target.dataset.k; if (!k) return;
  set(k, e.target.type === 'range' ? +e.target.value : e.target.value);
  if (k === 'header.imageWidth') $('#w-out').textContent = e.target.value + ' px';
  if (k === 'header.image') $('#thumb').style.backgroundImage = `url("${fullSrc(e.target.value)}")`;
  changed({ outline: /\.title$/.test(k) && k.startsWith('sections') });
});
$('#block').addEventListener('click', e => {
  const sw = e.target.closest('[data-sw]');
  if (sw) { data.header.badgeColor = sw.dataset.sw; $('#badge-color').value = '#' + sw.dataset.sw; refreshBadges(); changed(); }
  const add = e.target.closest('[data-additem]');
  if (add) {
    const arr = get(add.dataset.additem), list = add.previousElementSibling;
    arr.push(list.dataset.kind === 'badge' ? { emoji: '😺', label: '', url: '' } : { ...TYPES[data.sections[sel].type].blank });
    renderItems(list); changed();
    list.lastElementChild.querySelector('input:not(.emoji)')?.focus();
  }
});
$('#block').addEventListener('change', e => { if (e.target.id === 'badge-color') { data.header.badgeColor = e.target.value.slice(1).toUpperCase(); refreshBadges(); changed(); } });

/* ───────── listas de elementos ───────── */
const ROW = {
  badge: it => `<div class="fields badge">
      <input type="text" class="emoji" data-f="emoji" value="${esc(it.emoji)}" aria-label="Emoji" maxlength="4">
      <input type="text" class="strong" data-f="label" value="${esc(it.label)}" placeholder="Texto" aria-label="Texto de la insignia">
      <input type="url" data-f="url" value="${esc(it.url)}" placeholder="https://…" aria-label="Enlace">
      <div class="badge-prev">${it.label ? `<img alt="" src="${esc(badgeUrl(it, data.header.badgeColor))}">` : ''}</div></div>`,
  talk: it => `<div class="fields two">
      <input type="text" class="strong full" data-f="title" value="${esc(it.title)}" placeholder="Título de la charla" aria-label="Título de la charla">
      <input type="text" data-f="venue" value="${esc(it.venue)}" placeholder="Evento" aria-label="Evento">
      <input type="url" data-f="url" value="${esc(it.url)}" placeholder="https://github.com/…" aria-label="Enlace"></div>`,
  project: it => `<div class="fields two">
      <input type="text" class="strong" data-f="name" value="${esc(it.name)}" placeholder="Nombre" aria-label="Nombre del proyecto">
      <input type="url" data-f="url" value="${esc(it.url)}" placeholder="https://github.com/…" aria-label="Enlace">
      <textarea class="full" data-f="desc" rows="2" placeholder="Descripción corta" aria-label="Descripción">${esc(it.desc)}</textarea></div>`,
  list: it => `<div class="fields"><input type="text" data-f="text" value="${esc(it.text)}" placeholder="Texto (admite Markdown)" aria-label="Texto"></div>`,
};
function renderItems(list) {
  const arr = get(list.dataset.list), kind = list.dataset.kind;
  list.innerHTML = arr.map((it, i) => `<div class="item" data-idx="${i}"><span class="grip" title="Arrastra para mover">${icon('grip')}</span>${ROW[kind](it)}<button type="button" class="del" data-del aria-label="Borrar">${icon('trash')}</button></div>`).join('')
    || '<p class="hint">Vacío. Añade el primero abajo</p>';
}
function bindList(list) {
  renderItems(list);
  list.addEventListener('input', e => {
    const row = e.target.closest('[data-idx]'); if (!row) return;
    e.stopPropagation();
    get(list.dataset.list)[row.dataset.idx][e.target.dataset.f] = e.target.value;
    if (list.dataset.kind === 'badge') refreshBadges(row);
    changed();
  });
  list.addEventListener('click', e => {
    if (!e.target.closest('[data-del]')) return;
    const arr = get(list.dataset.list), i = +e.target.closest('[data-idx]').dataset.idx;
    const it = arr[i], name = it.label || it.title || it.name || it.text || 'este elemento';
    arr.splice(i, 1); renderItems(list); changed();
    toast(`Borrado: ${name}`);
  });
  list.addEventListener('pointerdown', e => { const row = e.target.closest('.grip') && e.target.closest('[data-idx]'); if (row) row.draggable = true; });
  list.addEventListener('dragend', e => { e.target.draggable = false; });
  sortable(list, (from, to) => { moveItem(get(list.dataset.list), from, to); renderItems(list); changed(); });
}
const refreshBadges = debounce((only) => {
  $$('[data-kind=badge] .item').forEach(row => {
    if (only && row !== only) return;
    const it = data.header.badges[row.dataset.idx];
    row.querySelector('.badge-prev').innerHTML = it.label ? `<img alt="" src="${esc(badgeUrl(it, data.header.badgeColor))}">` : '';
  });
}, 400);

$('#btn-hide').onclick = () => { const s = data.sections[sel]; s.hidden = !s.hidden; renderBlock(); changed({ outline: true }); toast(s.hidden ? 'Sección oculta: no sale en el README' : 'Sección visible'); };
$('#btn-del').onclick = () => {
  const s = data.sections[sel];
  if (!confirm(`¿Borrar la sección «${s.title || TYPES[s.type].name}»?`)) return;
  data.sections.splice(sel, 1); changed(); select('header');
};

/* ───────── vista previa ───────── */
let md = '';
function preview() {
  md = renderReadme(data);
  const base = rawBase(data);
  $('#gh').innerHTML = renderBlocks(data).map(b =>
    `<div class="blk" data-b="${b.id}">${markdown(b.md).html.replace(/src="(?!https?:|data:|\/)(?:\.\/)?([^"]+)"/g, (_, p) => `src="${base}${p}"`)}</div>`).join('');
  $$('#gh a').forEach(a => { a.target = '_blank'; a.rel = 'noopener'; });
  $('#code').textContent = md;
  highlight();
}
function highlight(scroll = false) {
  const id = typeof sel === 'number' ? `sec-${sel}` : sel;
  $$('#gh .blk').forEach(b => {
    b.classList.toggle('sel', b.dataset.b === id);
    if (scroll && b.dataset.b === id) b.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });
}
$('#gh').addEventListener('click', e => {
  if (e.target.closest('a')) e.preventDefault();
  const b = e.target.closest('.blk'); if (!b) return;
  const id = b.dataset.b;
  select(id.startsWith('sec-') ? +id.slice(4) : id);
});
$$('[data-tab]').forEach(b => b.onclick = () => {
  $$('[data-tab]').forEach(x => x.setAttribute('aria-pressed', x === b));
  $('#gh').hidden = b.dataset.tab !== 'preview'; $('#code').hidden = b.dataset.tab !== 'code';
});
$$('button[data-theme]').forEach(b => b.onclick = () => {
  $$('button[data-theme]').forEach(x => x.setAttribute('aria-pressed', x === b));
  $('#gh-wrap').dataset.theme = b.dataset.theme; localStorage.setItem('estudio:gh-theme', b.dataset.theme);
});
function setPreview(on) {
  document.body.classList.toggle('no-preview', !on);
  $('#toggle-preview').setAttribute('aria-pressed', on);
  localStorage.setItem('estudio:preview-readme', on ? '1' : '0');
}
$('#toggle-preview').onclick = () => setPreview(document.body.classList.contains('no-preview'));
splitter($('#splitter'), $('#pane-editor'), 'estudio:split-readme');

/* ───────── copiar, descargar, ajustes, publicar ───────── */
$('#btn-copy').onclick = async () => { await navigator.clipboard.writeText(md); toast('Markdown copiado'); };
$('#btn-download').onclick = () => {
  const a = Object.assign(document.createElement('a'), { href: URL.createObjectURL(new Blob([md], { type: 'text/markdown' })), download: 'README.md' });
  a.click(); URL.revokeObjectURL(a.href);
};
$('#btn-settings').onclick = () => { $$('#dlg-settings [data-k]').forEach(i => { i.value = data[i.dataset.k] || ''; }); $('#dlg-settings').showModal(); };
$$('#dlg-settings [data-k]').forEach(i => i.addEventListener('input', () => { data[i.dataset.k] = i.value.trim(); changed(); }));

const dlg = $('#dlg-publish');
$('#btn-publish').onclick = () => { $('#dlg-repo').textContent = data.repo || 'JeroHoyos/JeroHoyos'; $('#dlg-log').hidden = true; dlg.showModal(); };
$('#dlg-go').onclick = async () => {
  const btn = $('#dlg-go'), log = $('#dlg-log');
  btn.disabled = true; btn.lastChild.textContent = 'Publicando…';
  try {
    if (dirty) await api('PUT', '/api/perfil', data);
    const r = await api('POST', '/api/perfil/publish', { message: $('#dlg-msg').value });
    log.className = 'log ok'; log.textContent = 'Listo, ya está en tu perfil.\n' + r.url;
  } catch (e) {
    log.className = 'log err'; log.textContent = e.message + (e.log ? '\n\n' + e.log : '');
  } finally { log.hidden = false; btn.disabled = false; btn.lastChild.textContent = 'Publicar'; }
};
$$('[data-close]').forEach(b => b.onclick = () => b.closest('dialog').close());

/* ───────── arranque ───────── */
data = await api('GET', '/api/perfil');
data.header ??= {}; data.header.badges ??= []; data.sections ??= [];
$('#lnk-profile').href = 'https://github.com/' + (data.repo || 'JeroHoyos/JeroHoyos').split('/')[0];
const theme = localStorage.getItem('estudio:gh-theme');
if (theme) $(`button[data-theme=${theme}]`)?.click();
setPreview(localStorage.getItem('estudio:preview-readme') !== '0');
preview(); select('header');
