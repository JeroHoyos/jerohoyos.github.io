import { parseFrontmatter, toFrontmatter, slugify, isImageCover } from '/tools/markdown.mjs';
import { $, $$, esc, api, icon, hydrateIcons, toast, saveState, debounce, splitter } from './shared.js';

hydrateIcons();
const setSave = saveState($('#save'));
const body = $('#body'), frame = $('#preview');
const F = { title: $('#f-title'), summary: $('#f-summary'), date: $('#f-date'), title_en: $('#f-title_en'), summary_en: $('#f-summary_en'), draft: $('#f-draft') };

let posts = [], current = null, meta = {}, tags = [], cover = '', dirty = false;

/* ───────── documento ↔ archivo .md ───────── */
function compose() {
  return toFrontmatter({
    ...meta,                         // conserva campos que el editor no muestra (slug…)
    title: F.title.value.trim(), title_en: F.title_en.value.trim() || undefined,
    date: F.date.value, tags, cover: cover || undefined,
    summary: F.summary.value.trim() || undefined, summary_en: F.summary_en.value.trim() || undefined,
    draft: F.draft.checked || undefined,
  }) + '\n' + body.value.replace(/^\n+/, '');
}
function fill(text) {
  const { data, body: md } = parseFrontmatter(text);
  meta = data;
  F.title.value = data.title || ''; F.summary.value = data.summary || ''; F.date.value = data.date || '';
  F.title_en.value = data.title_en || ''; F.summary_en.value = data.summary_en || '';
  F.draft.checked = data.draft === true;
  tags = Array.isArray(data.tags) ? data.tags : data.tags ? String(data.tags).split(',').map(s => s.trim()).filter(Boolean) : [];
  cover = data.cover || '';
  body.value = md.replace(/^\n+/, '');
  renderTags(); renderCover(); autosize(); count();
  $('#slug').textContent = `/blog/${slugify(data.slug || current.replace(/\.md$/, ''))}/`;
  $('#file').textContent = `posts/${current}`;
  $('#doc-name').textContent = data.title || current;
}

/* ───────── lista de posts ───────── */
async function loadList() {
  posts = await api('GET', '/api/posts');
  renderList();
}
function renderList() {
  const q = $('#search').value.trim().toLowerCase();
  const shown = posts.filter(p => !q || p.title.toLowerCase().includes(q));
  const item = p => `<button type="button" class="post-item" data-file="${esc(p.file)}" aria-current="${p.file === current}">
      <span class="thumb" style="${isImageCover(p.cover) ? `background-image:url('/posts/${esc(p.cover)}')` : ''}"></span>
      <span class="txt"><span class="t">${esc(p.title)}</span>
      <span class="d">${esc(p.date)} ${p.draft ? '<span class="pill draft">Borrador</span>' : '<span class="pill live">Publicable</span>'}</span></span></button>`;
  const drafts = shown.filter(p => p.draft), live = shown.filter(p => !p.draft);
  $('#posts').innerHTML = !posts.length ? '<p class="empty">Aún no hay posts.<br>Crea el primero arriba</p>'
    : !shown.length ? '<p class="empty">Nada coincide con la búsqueda.</p>'
    : (drafts.length ? `<div class="group-label">Borradores</div>${drafts.map(item).join('')}` : '') +
      (live.length ? `<div class="group-label">Publicables</div>${live.map(item).join('')}` : '');
  $('#posts-count').textContent = `${posts.length} post${posts.length === 1 ? '' : 's'} · ${posts.filter(p => p.draft).length} borradores`;
}
$('#search').addEventListener('input', renderList);
$('#posts').addEventListener('click', e => { const b = e.target.closest('[data-file]'); if (b) open(b.dataset.file); });

async function open(file) {
  if (dirty) await save();
  current = file;
  fill(await api('GET', '/api/post?file=' + encodeURIComponent(file)));
  dirty = false; setSave('saved');
  localStorage.setItem('estudio:last', file);
  showDoc(true); renderList(); preview();
  $('#doc-scroll').scrollTop = 0;
}
function showDoc(on) { $('#doc').hidden = !on; $('#empty').hidden = on; $('.toolbar').style.visibility = on ? '' : 'hidden'; }

/* ───────── nuevo, guardar, borrar ───────── */
const dlgNew = $('#dlg-new');
$$('#btn-new, [data-new]').forEach(b => b.onclick = () => { $('#new-title').value = ''; $('#new-slug').textContent = '/blog/…/'; dlgNew.showModal(); });
$('#new-title').oninput = e => { $('#new-slug').textContent = `/blog/${slugify(e.target.value) || '…'}/`; };
$('#form-new').onsubmit = async e => {
  e.preventDefault();
  const title = $('#new-title').value.trim(), file = slugify(title) + '.md';
  const today = new Date(Date.now() - new Date().getTimezoneOffset() * 6e4).toISOString().slice(0, 10);
  try {
    await api('PUT', `/api/post?file=${encodeURIComponent(file)}&new=1`, toFrontmatter({ title, date: today, draft: true }) + '\n', true);
    dlgNew.close(); await loadList(); await open(file);
    body.focus(); toast('Post creado como borrador');
  } catch (err) { toast(err.message, 'err'); }
};

async function save() {
  if (!current || !dirty) return true;
  setSave('saving');
  try {
    await api('PUT', '/api/post?file=' + encodeURIComponent(current), compose(), true);
    dirty = false; setSave('saved');
    const p = posts.find(p => p.file === current);
    if (p) { Object.assign(p, { title: F.title.value || current, date: F.date.value, draft: F.draft.checked, cover }); renderList(); }
    return true;
  } catch (e) { setSave('error'); toast(e.message, 'err'); return false; }
}
const autosave = debounce(save, 900);
function changed() {
  dirty = true; setSave('dirty'); autosave(); preview(); count();
  $('#doc-name').textContent = F.title.value || current;
}
[...Object.values(F), body].forEach(el => el.addEventListener('input', changed));
addEventListener('keydown', e => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') { e.preventDefault(); save().then(ok => ok && toast('Guardado')); } });
addEventListener('beforeunload', e => { if (dirty) { save(); e.preventDefault(); } });

$('#btn-delete').onclick = async () => {
  if (!confirm(`¿Borrar «${F.title.value || current}»? Se elimina posts/${current}.`)) return;
  await api('DELETE', '/api/post?file=' + encodeURIComponent(current));
  dirty = false; current = null; localStorage.removeItem('estudio:last');
  await loadList(); showDoc(false); frame.srcdoc = ''; $('#doc-name').textContent = '—';
  toast('Post borrado');
};
$('#btn-more').onclick = e => { const m = $('#more'); m.hidden = !m.hidden; e.currentTarget.setAttribute('aria-expanded', !m.hidden); };

/* ───────── campos que crecen solos ───────── */
function autosize() { for (const t of [F.title, F.summary, body]) { t.style.height = 'auto'; t.style.height = t.scrollHeight + 'px'; } }
[F.title, F.summary, body].forEach(t => t.addEventListener('input', autosize));
addEventListener('resize', autosize);
F.title.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); F.summary.focus(); } });
F.summary.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); body.focus(); } });
function count() {
  const words = body.value.split(/\s+/).filter(Boolean).length;
  $('#count').textContent = `${words} palabras · ${Math.max(1, Math.round(words / 220))} min`;
}

/* ───────── etiquetas ───────── */
function renderTags() {
  $$('#tags .chip').forEach(c => c.remove());
  $('#tag-input').insertAdjacentHTML('beforebegin', tags.map((t, i) => `<span class="chip">${esc(t)}<button type="button" data-rm="${i}" aria-label="Quitar ${esc(t)}">${icon('x')}</button></span>`).join(''));
}
$('#tags').addEventListener('click', e => {
  const rm = e.target.closest('[data-rm]');
  if (rm) { tags.splice(+rm.dataset.rm, 1); renderTags(); changed(); } else $('#tag-input').focus();
});
$('#tag-input').addEventListener('keydown', e => {
  const inp = e.target, v = slugify(inp.value);
  if ((e.key === 'Enter' || e.key === ',') && v) { e.preventDefault(); if (!tags.includes(v)) tags.push(v); inp.value = ''; renderTags(); changed(); }
  else if (e.key === 'Backspace' && !inp.value && tags.length) { tags.pop(); renderTags(); changed(); }
});

/* ───────── portada: solo subir una imagen ───────── */
function renderCover() {
  const has = isImageCover(cover);
  $('#cover-drop').hidden = has; $('.cover-img').hidden = !has;
  if (has) $('#cover-img').src = '/posts/' + cover;
}
async function upload(file) {
  const name = file.name && file.name !== 'image.png' ? file.name : `imagen-${Date.now()}.${(file.type.split('/')[1] || 'png').replace('jpeg', 'jpg')}`;
  try { return (await api('POST', '/api/upload?name=' + encodeURIComponent(name), file, true)).path; }
  catch (e) { toast(e.message, 'err'); return null; }
}
async function setCoverFile(file) {
  if (!file || !file.type.startsWith('image/')) return toast('La portada tiene que ser una imagen', 'err');
  const path = await upload(file);
  if (path) { cover = path; renderCover(); changed(); toast('Portada lista'); }
}
$$('#cover-drop, #cover-change').forEach(b => b.onclick = () => $('#cover-file').click());
$('#cover-file').onchange = e => { setCoverFile(e.target.files[0]); e.target.value = ''; };
$('#cover-remove').onclick = () => { cover = ''; renderCover(); changed(); };
const coverBox = $('#cover');
coverBox.addEventListener('dragover', e => { e.preventDefault(); coverBox.classList.add('over'); });
coverBox.addEventListener('dragleave', () => coverBox.classList.remove('over'));
coverBox.addEventListener('drop', e => { e.preventDefault(); coverBox.classList.remove('over'); setCoverFile(e.dataTransfer.files[0]); });

/* ───────── barra de formato ───────── */
function wrap(before, after = before, ph = '') {
  const { selectionStart: s, selectionEnd: e, value } = body, sel = value.slice(s, e) || ph;
  body.focus(); body.setRangeText(before + sel + after, s, e, 'end');
  if (s === e) body.setSelectionRange(s + before.length, s + before.length + sel.length);
  body.dispatchEvent(new Event('input'));
}
function prefix(p) {
  const { selectionStart: s, selectionEnd: e, value } = body, a = value.lastIndexOf('\n', s - 1) + 1;
  body.focus(); body.setRangeText(value.slice(a, e).split('\n').map((l, i) => (typeof p === 'function' ? p(i) : p) + l).join('\n'), a, e, 'end');
  body.dispatchEvent(new Event('input'));
}
function block(text) {
  const { selectionStart: s, value } = body;
  const pre = !s ? '' : value[s - 1] !== '\n' ? '\n\n' : value[s - 2] !== '\n' ? '\n' : '';
  body.focus(); body.setRangeText(pre + text + '\n\n', s, body.selectionEnd, 'end');
  body.dispatchEvent(new Event('input'));
}
const ACT = {
  bold: () => wrap('**', '**', 'negrita'), italic: () => wrap('*', '*', 'cursiva'),
  h2: () => prefix('## '), quote: () => prefix('> '), ul: () => prefix('- '), ol: () => prefix(i => `${i + 1}. `),
  link: () => { const u = prompt('Dirección del enlace', 'https://'); if (u) wrap('[', `](${u})`, 'texto del enlace'); },
  code: () => (body.value.slice(body.selectionStart, body.selectionEnd).includes('\n') || body.selectionStart === body.selectionEnd ? wrap('```python\n', '\n```', '# código') : wrap('`')),
  math: () => (body.selectionStart === body.selectionEnd ? block('$$\n\\mathrm{softmax}(x_i) = \\frac{e^{x_i}}{\\sum_j e^{x_j}}\n$$') : wrap('$')),
  table: () => block('| columna | valor |\n| --- | ---: |\n| a | 1 |\n| b | 2 |'),
  image: () => { const i = Object.assign(document.createElement('input'), { type: 'file', accept: 'image/*,application/pdf', multiple: true }); i.onchange = () => insertFiles([...i.files]); i.click(); },
};
$$('[data-md]').forEach(b => b.onclick = () => ACT[b.dataset.md]());
body.addEventListener('keydown', e => {
  const k = { b: 'bold', i: 'italic', k: 'link' }[e.key.toLowerCase()];
  if ((e.ctrlKey || e.metaKey) && k) { e.preventDefault(); ACT[k](); }
  if (e.key === 'Tab' && !e.shiftKey) { e.preventDefault(); body.setRangeText('  ', body.selectionStart, body.selectionEnd, 'end'); changed(); }
});

/* ───────── imágenes dentro del texto ───────── */
async function insertFiles(files) {
  for (const f of files) {
    const path = await upload(f); if (!path) continue;
    const alt = f.name.replace(/\.[^.]+$/, '').replace(/[-_]+/g, ' ');
    block(/\.pdf$/i.test(path) ? `[📄 ${f.name}](${path})` : `![${alt}](${path} "Pie de foto")`);
  }
}
body.addEventListener('dragover', e => { if (e.dataTransfer.types.includes('Files')) { e.preventDefault(); body.classList.add('over'); } });
body.addEventListener('dragleave', () => body.classList.remove('over'));
body.addEventListener('drop', e => { if (!e.dataTransfer.files.length) return; e.preventDefault(); body.classList.remove('over'); insertFiles([...e.dataTransfer.files]); });
body.addEventListener('paste', e => { const fs = [...e.clipboardData.files]; if (fs.length) { e.preventDefault(); insertFiles(fs); } });

/* ───────── vista previa ───────── */
let scrollY = 0;
const preview = debounce(async () => {
  if (!current || document.body.classList.contains('no-preview')) return;
  try {
    const html = await api('POST', '/api/preview', { text: compose(), file: current });
    try { scrollY = frame.contentWindow.scrollY; } catch { /* aún no cargó */ }
    frame.srcdoc = html;
  } catch (e) { toast('Vista previa: ' + e.message, 'err'); }
}, 350);
frame.addEventListener('load', () => { try { frame.contentWindow.scrollTo(0, scrollY); } catch { /* nada */ } });
$$('[data-size]').forEach(b => b.onclick = () => {
  $$('[data-size]').forEach(x => x.setAttribute('aria-pressed', x === b));
  $('#preview-body').classList.toggle('mobile', b.dataset.size === 'mobile');
});
$('#open-tab').onclick = async () => { await save(); window.open('/api/view?file=' + encodeURIComponent(current), '_blank'); };
function setPreview(on) {
  document.body.classList.toggle('no-preview', !on);
  $('#toggle-preview').setAttribute('aria-pressed', on);
  localStorage.setItem('estudio:preview', on ? '1' : '0');
  if (on) preview();
}
$('#toggle-preview').onclick = () => setPreview(document.body.classList.contains('no-preview'));
splitter($('#splitter'), $('#pane-editor'), 'estudio:split-blog');

/* ───────── publicar ───────── */
const dlgPub = $('#dlg-publish');
$('#btn-publish').onclick = async () => {
  await save();
  $('#publish-log').hidden = true;
  $('#commit-msg').value = current ? `blog: ${F.title.value}` : 'blog: actualizar posts';
  $('#pending').textContent = 'Revisando cambios…';
  dlgPub.showModal();
  try {
    const st = await api('GET', '/api/status');
    $('#pending').textContent = st.pending.length ? st.pending.map(l => l.replace(/^\s*\S+\s+/, '')).join('\n') : 'No hay cambios nuevos en el blog.';
  } catch { $('#pending').textContent = ''; }
};
$('#btn-publish-go').onclick = async () => {
  const btn = $('#btn-publish-go'), log = $('#publish-log');
  btn.disabled = true; btn.lastChild.textContent = 'Publicando…';
  try {
    const r = await api('POST', '/api/publish', { message: $('#commit-msg').value });
    log.className = 'log ok';
    log.textContent = r.nothing ? 'No había nada nuevo que publicar.' : `Listo. ${r.posts} post(s) publicados.\nGitHub Pages tarda ~1 minuto en actualizar.\n\n${r.files.join('\n')}`;
  } catch (e) {
    log.className = 'log err'; log.textContent = e.message + (e.log ? '\n\n' + e.log : '');
  } finally { log.hidden = false; btn.disabled = false; btn.lastChild.textContent = 'Publicar'; }
};
$$('[data-close]').forEach(b => b.onclick = () => b.closest('dialog').close());

/* ───────── arranque ───────── */
setPreview(localStorage.getItem('estudio:preview') !== '0');
await loadList();
const last = localStorage.getItem('estudio:last');
const first = posts.find(p => p.file === last) || posts[0];
if (first) await open(first.file); else showDoc(false);
