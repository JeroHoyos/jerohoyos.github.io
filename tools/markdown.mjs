// Conversor de Markdown pequeño y sin dependencias.
// Lo usan el generador (tools/blog.mjs, en Node) y la vista previa del editor (en el navegador).
//
// Soporta: front matter, # títulos, **negrita**, *cursiva*, ~~tachado~~, `código`,
// bloques ``` con lenguaje, > citas, listas - y 1., tablas | a | b |, ---, enlaces,
// ![imágenes](ruta "pie de foto"), notas al pie no, HTML tal cual, y fórmulas $…$ / $$…$$ (KaTeX).

// portadas animadas disponibles (están en static/blog.js).
// En el front matter, `cover:` también acepta la ruta de una imagen (p. ej. img/portada.jpg).
export const COVERS = ['attention', 'sine', 'power', 'voice', 'life'];
export const isImageCover = c => /\.(png|jpe?g|gif|webp|svg)$/i.test(c || '');

export function parseFrontmatter(text) {
  text = text.replace(/\r\n?/g, '\n');
  const m = /^---\n([\s\S]*?)\n---\n?/.exec(text);
  const data = {};
  if (!m) return { data, body: text };
  for (const line of m[1].split('\n')) {
    const kv = /^([A-Za-z_][\w-]*)\s*:\s*(.*)$/.exec(line);
    if (!kv) continue;
    let v = kv[2].trim();
    if (/^\[.*\]$/.test(v)) v = v.slice(1, -1).split(',').map(s => unquote(s.trim())).filter(Boolean);
    else if (v === 'true' || v === 'false') v = v === 'true';
    else v = unquote(v);
    data[kv[1]] = v;
  }
  return { data, body: text.slice(m[0].length) };
}
const unquote = s => s.replace(/^(['"])(.*)\1$/, '$2');

export function toFrontmatter(data) {
  const out = ['---'];
  for (const [k, v] of Object.entries(data)) {
    if (v === undefined || v === '' || (Array.isArray(v) && !v.length)) continue;
    out.push(`${k}: ${Array.isArray(v) ? `[${v.join(', ')}]` : typeof v === 'string' && /[:#]/.test(v) ? JSON.stringify(v) : v}`);
  }
  out.push('---', '');
  return out.join('\n');
}

export const slugify = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80);

export const escapeHtml = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// resolveUrl(url) permite reescribir rutas relativas de imágenes y enlaces
export function markdown(src, { resolveUrl = u => u } = {}) {
  const lines = src.replace(/\r\n?/g, '\n').split('\n');
  const out = [], toc = [], ids = new Set();
  let i = 0;

  const fixUrl = u => (/^([a-z]+:|\/|#)/i.test(u) ? u : resolveUrl(u));
  const inline = text => {
    const keep = [];
    const stash = html => `\u0000${keep.push(html) - 1}\u0000`;
    text = text
      .replace(/(`+)([\s\S]*?[^`])\1(?!`)/g, (_, __, c) => stash(`<code>${escapeHtml(c.trim())}</code>`))
      .replace(/\$\$([\s\S]+?)\$\$/g, m => stash(escapeHtml(m)))
      .replace(/(^|[^\\$])\$([^\s$](?:[^$]*?[^\s$])?)\$/g, (_, pre, m) => pre + stash(escapeHtml(`$${m}$`)))
      .replace(/!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+"([^"]*)")?\s*\)/g, (_, alt, url, title) =>
        stash(`<img src="${escapeHtml(fixUrl(url))}" alt="${escapeHtml(alt)}" loading="lazy"${title ? ` title="${escapeHtml(title)}"` : ''}>`))
      .replace(/\[([^\]]+)\]\(\s*<?([^)\s>]+)>?\s*\)/g, (_, label, url) => {
        const ext = /^https?:/i.test(url);
        return stash(`<a href="${escapeHtml(fixUrl(url))}"${ext ? ' target="_blank" rel="noopener noreferrer"' : ''}>`) + label + stash('</a>');
      })
      .replace(/<(https?:\/\/[^>\s]+)>/g, (_, u) => stash(`<a href="${escapeHtml(u)}" target="_blank" rel="noopener noreferrer">${escapeHtml(u)}</a>`))
      .replace(/\*\*([^*]+?)\*\*|__([^_]+?)__/g, (_, a, b) => `<strong>${a || b}</strong>`)
      .replace(/(^|[^*\w])\*([^*\s](?:[^*]*?[^*\s])?)\*(?!\*)/g, '$1<em>$2</em>')
      .replace(/(^|[^_\w])_([^_\s](?:[^_]*?[^_\s])?)_(?![_\w])/g, '$1<em>$2</em>')
      .replace(/~~([^~]+)~~/g, '<del>$1</del>')
      .replace(/ {2,}\n|\\\n/g, '<br>\n');
    return text.replace(/\u0000(\d+)\u0000/g, (_, n) => keep[n]);
  };
  const isBlank = l => !l.trim();
  const startsBlock = l => /^(#{1,6}\s|```|~~~|>|\s*([-*+]|\d+[.)])\s|\$\$|<\/?(div|figure|table|iframe|video|details|section|aside|p|ul|ol|pre|blockquote|hr|img|svg)\b)/i.test(l) || /^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(l);

  while (i < lines.length) {
    const line = lines[i];
    if (isBlank(line)) { i++; continue; }

    let m;
    if ((m = /^(```|~~~)\s*([\w+#.-]*)/.exec(line))) {               // bloque de código
      const fence = m[1], lang = m[2], buf = [];
      i++;
      while (i < lines.length && !lines[i].startsWith(fence)) buf.push(lines[i++]);
      i++;
      out.push(`<pre><code${lang ? ` class="language-${escapeHtml(lang)}"` : ''}>${escapeHtml(buf.join('\n'))}</code></pre>`);
      continue;
    }
    if (/^\$\$/.test(line.trim())) {                                   // fórmula en bloque
      const buf = [line];
      if (!(line.trim().length > 2 && line.trim().endsWith('$$'))) {
        i++;
        while (i < lines.length && !lines[i].trim().endsWith('$$')) buf.push(lines[i++]);
        if (i < lines.length) buf.push(lines[i]);
      }
      i++;
      out.push(`<div class="math">${escapeHtml(buf.join('\n'))}</div>`);
      continue;
    }
    if ((m = /^(#{1,6})\s+(.*?)\s*#*\s*$/.exec(line))) {               // títulos
      const level = m[1].length, html = inline(m[2]);
      let id = slugify(m[2].replace(/[`*_$]/g, '')) || 'seccion', base = id, n = 2;
      while (ids.has(id)) id = `${base}-${n++}`;
      ids.add(id);
      if (level <= 3) toc.push({ level, id, text: html.replace(/<[^>]+>/g, '') });
      out.push(`<h${level} id="${id}">${html}</h${level}>`);
      i++; continue;
    }
    if (/^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(line)) { out.push('<hr>'); i++; continue; }
    if (/^>/.test(line)) {                                             // cita
      const buf = [];
      while (i < lines.length && /^>/.test(lines[i])) buf.push(lines[i++].replace(/^>\s?/, ''));
      out.push(`<blockquote>${markdown(buf.join('\n'), { resolveUrl }).html}</blockquote>`);
      continue;
    }
    if ((m = /^(\s*)([-*+]|\d+[.)])\s+/.exec(line))) {                 // listas
      const ordered = /\d/.test(m[2]), items = [], base = m[1].length;
      const itemRe = new RegExp(`^ {${base}}${ordered ? '\\d+[.)]' : '[-*+]'}\\s+(.*)$`);
      const deeper = new RegExp(`^ {${base + 2},}\\S`);
      while (i < lines.length) {
        const im = itemRe.exec(lines[i]);
        if (im) { items.push([im[1]]); i++; continue; }
        if (items.length && deeper.test(lines[i])) { items[items.length - 1].push(lines[i].slice(base + 2).replace(/^ {1,2}(?=[-*+\d])/, '')); i++; continue; }
        break;
      }
      const li = items.map(parts => {
        const [first, ...rest] = parts;
        const task = /^\[( |x)\]\s+/i.exec(first);
        const head = task ? `<input type="checkbox" disabled${task[1] !== ' ' ? ' checked' : ''}> ` + inline(first.slice(task[0].length)) : inline(first);
        return `<li>${head}${rest.length ? markdown(rest.join('\n'), { resolveUrl }).html : ''}</li>`;
      });
      out.push(`<${ordered ? 'ol' : 'ul'}>${li.join('')}</${ordered ? 'ol' : 'ul'}>`);
      continue;
    }
    if (/^\|.*\|\s*$/.test(line) && i + 1 < lines.length && /^\|?\s*:?-{2,}/.test(lines[i + 1])) {   // tablas
      const cells = l => l.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim());
      const align = cells(lines[i + 1]).map(c => (c.startsWith(':') && c.endsWith(':') ? 'center' : c.endsWith(':') ? 'right' : ''));
      const td = (tag, c, k) => `<${tag}${align[k] ? ` style="text-align:${align[k]}"` : ''}>${inline(c)}</${tag}>`;
      const head = cells(line).map((c, k) => td('th', c, k)).join('');
      i += 2;
      const rows = [];
      while (i < lines.length && /^\|.*\|\s*$/.test(lines[i])) rows.push(`<tr>${cells(lines[i++]).map((c, k) => td('td', c, k)).join('')}</tr>`);
      out.push(`<div class="table-wrap"><table><thead><tr>${head}</tr></thead><tbody>${rows.join('')}</tbody></table></div>`);
      continue;
    }
    if (/^<\/?[a-z][\w-]*[\s>/]/i.test(line) || /^<!--/.test(line)) {   // HTML tal cual
      const buf = [];
      while (i < lines.length && !isBlank(lines[i])) buf.push(lines[i++]);
      out.push(buf.join('\n'));
      continue;
    }
    const buf = [];                                                    // párrafo
    while (i < lines.length && !isBlank(lines[i]) && !(buf.length && startsBlock(lines[i]))) buf.push(lines[i++]);
    const para = buf.join('\n');
    // una imagen sola en su párrafo se vuelve figura con pie de foto
    const fig = /^!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+"([^"]*)")?\s*\)$/.exec(para.trim());
    if (fig) {
      const cap = fig[3] || fig[1];
      out.push(`<figure><img src="${escapeHtml(fixUrl(fig[2]))}" alt="${escapeHtml(fig[1])}" loading="lazy">${cap ? `<figcaption>${inline(cap)}</figcaption>` : ''}</figure>`);
    } else out.push(`<p>${inline(para)}</p>`);
  }
  return { html: out.join('\n'), toc };
}

// minutos de lectura aproximados (≈220 palabras por minuto)
export const readingTime = body => Math.max(1, Math.round(body.replace(/```[\s\S]*?```/g, '').split(/\s+/).filter(Boolean).length / 220));
