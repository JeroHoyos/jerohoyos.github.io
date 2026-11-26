#!/usr/bin/env node
// Generador del blog. Sin dependencias: solo Node 18+.
//
//   node tools/blog.mjs              → genera todo a partir de posts/*.md
//   node tools/blog.mjs --borradores → incluye también los posts con `draft: true` (solo para mirar en local)
//
// Escribe: blog/<slug>/index.html, blog/index.html, blog/feed.xml, el bloque del blog en index.html
// (entre <!-- BLOG:START --> y <!-- BLOG:END -->) y sitemap.xml.

import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync, rmSync, statSync } from 'node:fs';
import { join, dirname, basename } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { parseFrontmatter, markdown, escapeHtml as esc, slugify, readingTime, isImageCover, COVERS } from './markdown.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SITE = 'https://jerohoyos.github.io';
const AUTHOR = 'Jerónimo Hoyos Botero';
const GEN = '<meta name="generator" content="tools/blog.mjs">';
const CSS_V = () => (/style\.css\?v=([\w.-]+)/.exec(readFileSync(join(ROOT, 'index.html'), 'utf8')) || [])[1] || '1';
const JS_V = () => (/main\.js\?v=([\w.-]+)/.exec(readFileSync(join(ROOT, 'index.html'), 'utf8')) || [])[1] || '1';

const bi = (en, es) => (en === es ? esc(es) : `<span lang="en">${esc(en)}</span><span lang="es">${esc(es)}</span>`);

/* ───────── leer los posts ───────── */
export function loadPosts({ drafts = false } = {}) {
  const dir = join(ROOT, 'posts');
  if (!existsSync(dir)) return [];
  const posts = [], errors = [];
  for (const file of readdirSync(dir)) {
    if (!file.endsWith('.md') || file.startsWith('_') || file.toLowerCase() === 'readme.md') continue;
    const { data, body } = parseFrontmatter(readFileSync(join(dir, file), 'utf8'));
    if (data.draft === true && !drafts) continue;
    if (!data.title) { errors.push(`${file}: falta "title"`); continue; }
    if (!/^\d{4}-\d{2}-\d{2}$/.test(data.date || '')) { errors.push(`${file}: "date" debe ser AAAA-MM-DD`); continue; }
    const tags = Array.isArray(data.tags) ? data.tags : data.tags ? String(data.tags).split(',').map(s => s.trim()).filter(Boolean) : [];
    const cover = data.cover || COVERS[posts.length % COVERS.length];
    posts.push({
      file, body, draft: data.draft === true,
      slug: slugify(data.slug || basename(file, '.md')),
      title: data.title, title_en: data.title_en || data.title,
      summary: data.summary || '', summary_en: data.summary_en || data.summary || '',
      date: data.date, tags: tags.map(t => slugify(t)).filter(Boolean), cover,
      minutes: readingTime(body),
    });
  }
  if (errors.length) throw new Error('Hay posts con errores:\n  ' + errors.join('\n  '));
  const seen = new Set();
  for (const p of posts) { if (seen.has(p.slug)) throw new Error(`Dos posts tienen el mismo slug: ${p.slug}`); seen.add(p.slug); }
  return posts.sort((a, b) => b.date.localeCompare(a.date) || a.slug.localeCompare(b.slug));
}

/* ───────── piezas de HTML ───────── */
const cover = (p, up) => isImageCover(p.cover)
  ? `<img src="${up}posts/${esc(p.cover)}" alt="" loading="lazy">`
  : `<canvas class="proj-canvas" data-cover="${esc(p.cover)}" aria-hidden="true"></canvas>`;
const tagList = (p, up) => p.tags.length ? `<div class="tags">${p.tags.map(t => `<span class="tag">${esc(t)}</span>`).join('')}</div>` : '';
const meta = p => `${p.date} · ${p.minutes} min${p.draft ? ' · BORRADOR' : ''}`;

const featured = (p, up) => `
          <a class="featured" href="${up}blog/${p.slug}/">
            <div class="proj-media">${cover(p, up)}<span class="proj-badge">${bi('LATEST', 'ÚLTIMO')}</span></div>
            <div class="proj-body">
              <span class="post-date">${meta(p)}</span>
              <h3 class="proj-name">${bi(p.title_en, p.title)}</h3>
              ${p.summary ? `<p class="proj-desc">${bi(p.summary_en, p.summary)}</p>` : ''}
              ${tagList(p, up)}
            </div>
          </a>`;
const row = (p, href, up) => `
            <li data-tags="${p.tags.join(' ')}"><a class="brow" href="${href}">
              <div class="proj-media">${cover(p, up)}</div>
              <div><span class="post-date">${meta(p)}</span><h3 class="proj-name">${bi(p.title_en, p.title)}</h3>${tagList(p, up)}</div>
            </a></li>`;

function homeBlock(posts) {
  if (!posts.length) return '';
  const [first, ...rest] = posts;
  const shown = rest.slice(0, 4);
  return `
      <article class="post" id="blog">
        <header class="post-head">
          <h2 class="post-title">~ blog ~</h2>
          <span class="post-date">${posts.length} ${posts.length === 1 ? 'post' : 'posts'}</span>
        </header>
        <div class="post-body">${featured(first, '')}${shown.length ? `
          <ul class="blist">${shown.map(p => row(p, `blog/${p.slug}/`, '')).join('')}
          </ul>` : ''}
          <a class="more" href="blog/">${bi('all posts', 'todos los posts')}</a>
        </div>
      </article>
`;
}

const head = ({ title, description, url, up, extra = '' }) => `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<script>try{var l=localStorage.getItem('lang')}catch(e){}document.documentElement.lang=l||(/^es/i.test(navigator.language||'')?'es':'en')</script>
${GEN}
<meta name="description" content="${esc(description)}">
<meta name="theme-color" content="#050505">
<link rel="canonical" href="${url}">
<link rel="alternate" type="application/rss+xml" title="Blog de ${AUTHOR}" href="${SITE}/blog/feed.xml">
<link rel="icon" href="${up}favicon.ico" sizes="32x32">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${SITE}/og.png?v=2">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Serif+Display:ital@0;1&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="${up}static/style.css?v=${CSS_V()}">${extra}
</head>
<body>
<canvas id="bg" aria-hidden="true"></canvas>

<div class="page">

  <header class="banner banner-sm">
    <canvas id="c-life" aria-hidden="true"></canvas>
    <div class="banner-inner"><h1><a href="${up}">${AUTHOR}</a></h1></div>
    <div class="lang" role="group" aria-label="Language">
      <button type="button" data-set-lang="es" aria-pressed="false">ES</button>
      <button type="button" data-set-lang="en" aria-pressed="true">EN</button>
    </div>
  </header>

  <div class="grid">
`;
const foot = up => `
  </div>

  <footer class="foot">
    <span>© ${new Date().getFullYear()} ${AUTHOR}, Medellín, Colombia</span>
    <span><a href="${up}">${bi('home', 'inicio')}</a> · <a href="${up}blog/">blog</a> · <a href="${up}blog/feed.xml">RSS</a></span>
  </footer>

</div>

<script src="${up}static/main.js?v=${JS_V()}"></script>
<script src="${up}static/blog.js?v=${CSS_V()}"></script>
<script src="${up}static/oneko.js" data-cat="${up}static/oneko.gif"></script>
</body>
</html>
`;

const KATEX = `
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.querySelector('.prose'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false})"></script>`;

export function postPage(p, posts, { up = '../../', html } = {}) {
  const md = markdown(p.body, { resolveUrl: u => `${up}posts/${u}` });
  const others = posts.filter(o => o.slug !== p.slug).slice(0, 3);
  const i = posts.indexOf(p);
  const newer = posts[i - 1], older = posts[i + 1];
  const hasMath = /\$[^$\s]/.test(p.body);
  return head({
    title: `${p.title} · ${AUTHOR}`, description: p.summary || p.title,
    url: `${SITE}/blog/${p.slug}/`, up, extra: hasMath ? KATEX : '',
  }) + `
    <aside class="side side-left">
${md.toc.length > 1 ? `      <section class="widget">
        <h2 class="widget-title"><span><span lang="en">~ contents</span><span lang="es">~ contenido</span></span></h2>
        <div class="widget-body">
          <ol class="toc">${md.toc.map(t => `<li class="l${t.level}"><a href="#${t.id}">${esc(t.text)}</a></li>`).join('')}</ol>
        </div>
      </section>
` : ''}      <section class="widget">
        <h2 class="widget-title"><span>~ blog</span></h2>
        <div class="widget-body post-nav">
          ${newer ? `<a href="${up}blog/${newer.slug}/">${bi(newer.title_en, newer.title)}</a>` : ''}
          ${older ? `<a href="${up}blog/${older.slug}/">${bi(older.title_en, older.title)}</a>` : ''}
          <a class="more" style="margin:0;font-family:var(--mono)" href="${up}blog/">${bi('all posts', 'todos los posts')}</a>
        </div>
      </section>
    </aside>

    <main class="feed">
      <article class="post article">
        <header class="post-head"><h2 class="post-title">~ blog ~</h2><span class="post-date">${meta(p)}</span></header>
        <div class="proj-media article-cover">${cover(p, up)}</div>
        <div class="article-head">
          ${tagList(p, up)}
          <h1 class="article-title">${bi(p.title_en, p.title)}</h1>
          ${p.summary ? `<p class="article-sub">${bi(p.summary_en, p.summary)}</p>` : ''}
          <div class="actions">
            <button type="button" class="btn-ink" data-print><span lang="en">Download PDF</span><span lang="es">Descargar PDF</span></button>
            <button type="button" class="btn-ink ghost" data-copy-link><span class="addr"><span lang="en">Copy link</span><span lang="es">Copiar enlace</span></span><span class="ok"><span lang="en">✓ copied</span><span lang="es">✓ copiado</span></span></button>
          </div>
        </div>
        <div class="post-body">
          <div class="prose">
${html ?? md.html}
          </div>
        </div>
      </article>
    </main>

    <aside class="side side-right">
${others.map(o => `      <section class="widget">
        <h2 class="widget-title"><span><span lang="en">~ read next</span><span lang="es">~ sigue leyendo</span></span></h2>
        <a href="${up}blog/${o.slug}/" style="text-decoration:none;color:inherit">
          <div class="proj-media" style="aspect-ratio:16/9">${cover(o, up)}</div>
          <div class="widget-body"><span class="post-date">${o.date}</span><p style="font-family:var(--serif);line-height:1.25">${bi(o.title_en, o.title)}</p></div>
        </a>
      </section>`).join('\n')}
    </aside>
` + foot(up);
}

function listPage(posts) {
  const up = '../';
  const tags = [...new Set(posts.flatMap(p => p.tags))].sort();
  return head({ title: `Blog · ${AUTHOR}`, description: `Posts de ${AUTHOR} sobre machine learning, Rust, GPU y estadística.`, url: `${SITE}/blog/`, up }) + `
    <aside class="side side-left">
      <section class="widget">
        <h2 class="widget-title"><span>~ blog</span></h2>
        <canvas id="c-sort" class="widget-fig" aria-hidden="true"></canvas>
        <div class="widget-body">
          <p lang="en">Notes on what I'm learning: machine learning, Rust, GPUs and statistics.</p>
          <p lang="es">Notas de lo que voy aprendiendo: machine learning, Rust, GPU y estadística.</p>
          <a class="more" href="feed.xml">RSS</a>
        </div>
      </section>
    </aside>

    <main class="feed">
      <article class="post">
        <header class="post-head"><h2 class="post-title">~ blog ~</h2><span class="post-date">${posts.length} posts</span></header>
        <div class="post-body">
${tags.length > 1 ? `          <div class="blog-filter"><button type="button" class="tag" data-tag="" aria-pressed="true">${bi('all', 'todo')}</button>${tags.map(t => `<button type="button" class="tag" data-tag="${t}" aria-pressed="false">${t}</button>`).join('')}</div>\n` : ''}          <ul class="blist">${posts.map(p => row(p, `${p.slug}/`, up)).join('')}
          </ul>
          <a class="more" href="${up}">${bi('home', 'inicio')}</a>
        </div>
      </article>
    </main>

    <aside class="side side-right">
      <section class="widget">
        <h2 class="widget-title"><span><span lang="en">~ visitor</span><span lang="es">~ visitante</span></span></h2>
        <div class="peek"><img src="${up}static/cat2.gif?v=20261014b" width="200" height="172" alt="Pixel art of a grey cat"></div>
        <div class="widget-body">
          <p lang="en">There's a cat chasing your cursor. This is expected behaviour.</p>
          <p lang="es">Hay un gato persiguiendo tu cursor. Es el comportamiento esperado.</p>
        </div>
      </section>
    </aside>
` + foot(up);
}

function feed(posts) {
  const item = p => `  <item>
    <title>${esc(p.title)}</title>
    <link>${SITE}/blog/${p.slug}/</link>
    <guid>${SITE}/blog/${p.slug}/</guid>
    <pubDate>${new Date(p.date + 'T12:00:00Z').toUTCString()}</pubDate>
    <description>${esc(p.summary || p.title)}</description>
  </item>`;
  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Blog de ${AUTHOR}</title>
  <link>${SITE}/blog/</link>
  <description>Machine learning, Rust, GPU y estadística.</description>
${posts.slice(0, 20).map(item).join('\n')}
</channel>
</rss>
`;
}

/* ───────── escribir ───────── */
const write = (path, text) => {
  mkdirSync(dirname(path), { recursive: true });
  const old = existsSync(path) ? readFileSync(path, 'utf8') : null;
  if (old !== text) writeFileSync(path, text);
  return old !== text;
};

export function build({ drafts = false, log = console.log } = {}) {
  const posts = loadPosts({ drafts });
  const changed = [];
  const blogDir = join(ROOT, 'blog');

  for (const p of posts) if (write(join(blogDir, p.slug, 'index.html'), postPage(p, posts))) changed.push(`blog/${p.slug}/`);
  // borra páginas de posts que ya no existen (solo las que generó este script)
  if (existsSync(blogDir)) for (const d of readdirSync(blogDir)) {
    const f = join(blogDir, d, 'index.html');
    if (statSync(join(blogDir, d)).isDirectory() && !posts.some(p => p.slug === d) && existsSync(f) && readFileSync(f, 'utf8').includes(GEN)) {
      rmSync(join(blogDir, d), { recursive: true }); changed.push(`blog/${d}/ (borrado)`);
    }
  }
  if (posts.length) {
    if (write(join(blogDir, 'index.html'), listPage(posts))) changed.push('blog/index.html');
    if (write(join(blogDir, 'feed.xml'), feed(posts))) changed.push('blog/feed.xml');
  } else {
    for (const f of ['index.html', 'feed.xml']) if (existsSync(join(blogDir, f))) { rmSync(join(blogDir, f)); changed.push(`blog/${f} (borrado)`); }
  }

  // bloque del inicio (respeta los saltos de línea CRLF del index)
  const idxPath = join(ROOT, 'index.html');
  const idx = readFileSync(idxPath, 'utf8');
  const nl = idx.includes('\r\n') ? '\r\n' : '\n';
  const re = /(<!-- BLOG:START[^>]*-->)[\s\S]*?(\s*<!-- BLOG:END -->)/;
  if (!re.test(idx)) throw new Error('index.html no tiene los marcadores <!-- BLOG:START --> / <!-- BLOG:END -->');
  const block = homeBlock(posts).replace(/\r?\n/g, nl);
  if (write(idxPath, idx.replace(re, (_, a, b) => a + block + b))) changed.push('index.html');

  const urls = [['/', '1.0'], ...(posts.length ? [['/blog/', '0.8']] : []), ...posts.filter(p => !p.draft).map(p => [`/blog/${p.slug}/`, '0.7'])];
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map(([u, pr]) => `  <url><loc>${SITE}${u}</loc><priority>${pr}</priority></url>`).join('\n')}\n</urlset>\n`;
  if (write(join(ROOT, 'sitemap.xml'), sitemap)) changed.push('sitemap.xml');

  log(`${posts.length} post(s)${drafts ? ' (con borradores)' : ''}. ${changed.length ? 'Cambió: ' + changed.join(', ') : 'Nada cambió.'}`);
  return { posts, changed };
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  try { build({ drafts: process.argv.includes('--borradores') }); }
  catch (e) { console.error('✗ ' + e.message); process.exit(1); }
}
