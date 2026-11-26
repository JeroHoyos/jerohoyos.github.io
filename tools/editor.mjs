#!/usr/bin/env node
// App para escribir el blog. Sin dependencias.
//
//   node tools/editor.mjs      (o: npm run escribir)
//
// Abre http://localhost:4321/__editor/ — solo escucha en tu computador (127.0.0.1).
// Además sirve todo el sitio, así que http://localhost:4321/ es tu web tal como quedará.

import { createServer } from 'node:http';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync, unlinkSync, statSync } from 'node:fs';
import { join, dirname, extname, normalize, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFile, exec, spawn } from 'node:child_process';
import { parseFrontmatter, slugify } from './markdown.mjs';
import { renderReadme } from './perfil.mjs';
import { build, loadPosts, postPage } from './blog.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const POSTS = join(ROOT, 'posts');
const IMG = join(POSTS, 'img');
const PORT = Number(process.env.PORT) || 4321;

const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8', '.json': 'application/json', '.xml': 'application/xml; charset=utf-8', '.md': 'text/plain; charset=utf-8', '.txt': 'text/plain; charset=utf-8', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.pdf': 'application/pdf' };

const send = (res, code, body, type = 'application/json; charset=utf-8') => {
  res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(typeof body === 'string' || Buffer.isBuffer(body) ? body : JSON.stringify(body));
};
const readBody = (req, limit = 20e6) => new Promise((ok, fail) => {
  const chunks = []; let size = 0;
  req.on('data', c => { size += c.length; if (size > limit) { fail(new Error('Archivo demasiado grande (máx. 20 MB)')); req.destroy(); } else chunks.push(c); });
  req.on('end', () => ok(Buffer.concat(chunks)));
  req.on('error', fail);
});
const safeMd = name => (/^[a-z0-9][a-z0-9-]*\.md$/.test(name || '') ? join(POSTS, name) : null);
const PERFIL = join(ROOT, 'perfil', 'perfil.json');
const gh = (args, input) => new Promise(ok => {
  const p = spawn('gh', args, { cwd: ROOT, windowsHide: true });
  let out = '';
  p.stdout.on('data', d => (out += d)); p.stderr.on('data', d => (out += d));
  p.on('error', e => ok({ ok: false, out: e.code === 'ENOENT' ? 'No encontré gh (GitHub CLI) instalado.' : e.message }));
  p.on('close', code => ok({ ok: code === 0, out: out.trim() }));
  if (input) p.stdin.end(input); else p.stdin.end();
});
const git = (...args) => new Promise(ok => execFile('git', args, { cwd: ROOT }, (err, stdout, stderr) => ok({ ok: !err, out: (stdout + stderr).trim() })));

function listPosts() {
  if (!existsSync(POSTS)) return [];
  return readdirSync(POSTS).filter(f => f.endsWith('.md') && !f.startsWith('_') && f.toLowerCase() !== 'readme.md').map(file => {
    const { data } = parseFrontmatter(readFileSync(join(POSTS, file), 'utf8'));
    return { file, title: data.title || file, date: data.date || '', draft: data.draft === true, cover: data.cover || '' };
  }).sort((a, b) => b.date.localeCompare(a.date));
}

async function api(req, res, url) {
  const q = url.searchParams;
  const route = `${req.method} ${url.pathname}`;

  if (route === 'GET /api/posts') return send(res, 200, listPosts());

  if (route === 'GET /api/post') {
    const f = safeMd(q.get('file'));
    if (!f || !existsSync(f)) return send(res, 404, { error: 'No existe ese post' });
    return send(res, 200, readFileSync(f, 'utf8'), 'text/plain; charset=utf-8');
  }

  if (route === 'PUT /api/post') {
    const f = safeMd(q.get('file'));
    if (!f) return send(res, 400, { error: 'Nombre de archivo inválido' });
    if (q.get('new') === '1' && existsSync(f)) return send(res, 409, { error: 'Ya existe un post con ese nombre. Cambia el título o el slug.' });
    mkdirSync(POSTS, { recursive: true });
    writeFileSync(f, (await readBody(req)).toString('utf8'));
    return send(res, 200, { ok: true, file: q.get('file') });
  }

  if (route === 'DELETE /api/post') {
    const f = safeMd(q.get('file'));
    if (!f || !existsSync(f)) return send(res, 404, { error: 'No existe ese post' });
    unlinkSync(f);
    return send(res, 200, { ok: true });
  }

  if (route === 'POST /api/upload') {
    const raw = (q.get('name') || 'imagen').toLowerCase();
    const ext = extname(raw).replace(/^\./, '').replace('jpeg', 'jpg');
    if (!['png', 'jpg', 'gif', 'webp', 'svg', 'pdf'].includes(ext)) return send(res, 400, { error: 'Formato no permitido (png, jpg, gif, webp, svg, pdf)' });
    let base = slugify(raw.slice(0, -extname(raw).length)) || 'imagen', name = `${base}.${ext}`, n = 2;
    mkdirSync(IMG, { recursive: true });
    while (existsSync(join(IMG, name))) name = `${base}-${n++}.${ext}`;
    writeFileSync(join(IMG, name), await readBody(req));
    return send(res, 200, { ok: true, path: `img/${name}` });
  }

  if (route === 'GET /api/images') {
    const list = existsSync(IMG) ? readdirSync(IMG).filter(f => !f.startsWith('.')).map(f => `img/${f}`) : [];
    return send(res, 200, list);
  }

  if (route === 'POST /api/preview' || route === 'GET /api/view') {
    // vista previa: el post tal como se verá, con las rutas apuntando a este servidor
    let text, file;
    if (req.method === 'GET') {
      file = q.get('file'); const f = safeMd(file);
      if (!f || !existsSync(f)) return send(res, 404, { error: 'Guarda el post primero' });
      text = readFileSync(f, 'utf8');
    } else ({ text, file } = JSON.parse((await readBody(req)).toString('utf8')));
    const { data, body } = parseFrontmatter(text);
    let posts = [];
    try { posts = loadPosts({ drafts: true }); } catch { /* un post roto no impide la vista previa */ }
    const slug = slugify(data.slug || (file || '').replace(/\.md$/, '') || data.title || 'nuevo');
    const tags = Array.isArray(data.tags) ? data.tags : data.tags ? String(data.tags).split(',') : [];
    const p = {
      slug, body, draft: data.draft === true, title: data.title || 'Sin título', title_en: data.title_en || data.title || 'Sin título',
      summary: data.summary || '', summary_en: data.summary_en || data.summary || '', date: data.date || '', tags: tags.map(t => slugify(String(t))).filter(Boolean),
      cover: data.cover || 'life', minutes: Math.max(1, Math.round(body.split(/\s+/).length / 220)),
    };
    const list = [p, ...posts.filter(o => o.slug !== slug)].sort((a, b) => b.date.localeCompare(a.date));
    return send(res, 200, postPage(p, list, { up: '/' }), 'text/html; charset=utf-8');
  }

  if (route === 'POST /api/build') {
    try { const r = build({ log: () => {} }); return send(res, 200, { ok: true, posts: r.posts.length, changed: r.changed }); }
    catch (e) { return send(res, 400, { error: e.message }); }
  }

  if (route === 'GET /api/status') {
    const s = await git('status', '--porcelain', '--', 'posts', 'blog', 'index.html', 'sitemap.xml');
    const b = await git('rev-parse', '--abbrev-ref', 'HEAD');
    return send(res, 200, { pending: s.out ? s.out.split('\n') : [], branch: b.out, git: s.ok });
  }

  if (route === 'POST /api/publish') {
    // genera el sitio, hace commit solo de los archivos del blog y sube a GitHub
    const { message } = JSON.parse((await readBody(req)).toString('utf8') || '{}');
    let built;
    try { built = build({ log: () => {} }); } catch (e) { return send(res, 400, { error: e.message }); }
    const paths = ['posts', 'blog', 'index.html', 'sitemap.xml'].filter(p => existsSync(join(ROOT, p)));
    const steps = [];
    const add = await git('add', '-A', '--', ...paths); steps.push(add);
    if (!add.ok) return send(res, 500, { error: 'git add falló', log: add.out });
    const staged = await git('diff', '--cached', '--name-only', '--', ...paths);
    if (!staged.out) return send(res, 200, { ok: true, nothing: true, posts: built.posts.length });
    const commit = await git('commit', '-m', message || 'blog: actualizar posts', '--', ...paths); steps.push(commit);
    if (!commit.ok) return send(res, 500, { error: 'git commit falló', log: commit.out });
    const push = await git('push'); steps.push(push);
    if (!push.ok) return send(res, 500, { error: 'El commit se hizo, pero git push falló', log: push.out });
    return send(res, 200, { ok: true, posts: built.posts.length, files: staged.out.split('\n'), log: steps.map(s => s.out).join('\n') });
  }

  /* ───────── README del perfil de GitHub ───────── */
  if (route === 'GET /api/perfil') {
    if (!existsSync(PERFIL)) return send(res, 404, { error: 'No existe perfil/perfil.json' });
    return send(res, 200, readFileSync(PERFIL, 'utf8'), 'application/json; charset=utf-8');
  }

  if (route === 'PUT /api/perfil') {
    const data = JSON.parse((await readBody(req)).toString('utf8'));
    mkdirSync(dirname(PERFIL), { recursive: true });
    writeFileSync(PERFIL, JSON.stringify(data, null, 2) + '\n');
    writeFileSync(join(dirname(PERFIL), 'README.md'), renderReadme(data));
    return send(res, 200, { ok: true });
  }

  if (route === 'POST /api/perfil/publish') {
    // sube perfil/README.md al repo del perfil con la API de GitHub (vía gh, con tu sesión)
    const data = JSON.parse(readFileSync(PERFIL, 'utf8'));
    const { message } = JSON.parse((await readBody(req)).toString('utf8') || '{}');
    const repo = data.repo || 'JeroHoyos/JeroHoyos', branch = data.branch || 'main';
    if (!/^[\w.-]+\/[\w.-]+$/.test(repo) || !/^[\w./-]+$/.test(branch)) return send(res, 400, { error: 'repo o branch inválidos en perfil.json' });
    const auth = await gh(['auth', 'status']);
    if (!auth.ok) return send(res, 401, { error: 'gh no tiene sesión. Abre una terminal y ejecuta: gh auth login', log: auth.out });
    const cur = await gh(['api', `repos/${repo}/contents/README.md?ref=${branch}`, '--jq', '.sha']);
    const content = Buffer.from(renderReadme(data), 'utf8').toString('base64');
    const payload = JSON.stringify({ message: message || 'Actualizar README', content, branch, ...(cur.ok && cur.out ? { sha: cur.out.trim() } : {}) });
    const put = await gh(['api', '-X', 'PUT', `repos/${repo}/contents/README.md`, '--input', '-', '--jq', '.commit.html_url'], payload);
    if (!put.ok) return send(res, 500, { error: 'GitHub rechazó la subida', log: put.out });
    return send(res, 200, { ok: true, url: put.out.trim() });
  }

  return send(res, 404, { error: 'Ruta desconocida' });
}

function serveFile(res, urlPath) {
  let rel = decodeURIComponent(urlPath);
  if (rel.startsWith('/__editor')) rel = '/tools/editor' + (rel.slice('/__editor'.length) || '/');
  const full = normalize(join(ROOT, rel));
  if (full !== ROOT && !full.startsWith(ROOT + sep)) return send(res, 403, 'Prohibido', 'text/plain');
  if (full.slice(ROOT.length).split(sep).some(seg => seg.startsWith('.') || seg === 'node_modules')) return send(res, 403, 'Prohibido', 'text/plain');
  let file = full;
  if (existsSync(file) && statSync(file).isDirectory()) {
    if (!rel.endsWith('/')) { res.writeHead(301, { Location: urlPath + '/' }); return res.end(); }
    file = join(file, 'index.html');
  }
  if (!existsSync(file)) {
    const nf = join(ROOT, '404.html');
    return send(res, 404, existsSync(nf) ? readFileSync(nf) : 'No encontrado', 'text/html; charset=utf-8');
  }
  send(res, 200, readFileSync(file), TYPES[extname(file).toLowerCase()] || 'application/octet-stream');
}

createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  try {
    if (url.pathname.startsWith('/api/')) return await api(req, res, url);
    if (url.pathname === '/__editor') { res.writeHead(301, { Location: '/__editor/' }); return res.end(); }
    serveFile(res, url.pathname);
  } catch (e) {
    send(res, 500, { error: e.message });
  }
}).listen(PORT, '127.0.0.1', () => {
  const link = `http://localhost:${PORT}/__editor/`;
  console.log(`\n  ✎  Editor del blog: ${link}\n  ✎  README de GitHub: ${link}readme.html\n  ◎  Tu web en local: http://localhost:${PORT}/\n\n  (Ctrl+C para cerrar)\n`);
  if (!process.argv.includes('--no-open')) {
    const cmd = process.platform === 'win32' ? `start "" "${link}"` : process.platform === 'darwin' ? `open "${link}"` : `xdg-open "${link}"`;
    exec(cmd, () => {});
  }
});
