// Genera el README del perfil de GitHub (repo JeroHoyos/JeroHoyos) a partir de perfil/perfil.json.
// Lo usan el editor (vista previa en vivo) y el servidor (guardar / publicar).

const shieldsText = s => encodeURIComponent(s.replace(/-/g, '--').replace(/_/g, '__'));
export const badgeUrl = (b, color) =>
  `https://img.shields.io/badge/${shieldsText(`${b.emoji ? b.emoji + ' ' : ''}${b.label}`)}-${(b.color || color || '21364D').replace('#', '')}?style=${b.style || 'for-the-badge'}`;

const attr = s => String(s ?? '').replace(/&/g, '&amp;').replace(/"/g, '&quot;');
const cell = s => String(s ?? '').replace(/\|/g, '\\|').replace(/\n+/g, ' ').trim();
const link = (text, url) => (url ? `[${text}](${url})` : text);

export const renderReadme = p => renderBlocks(p).map(b => b.md).join('\n\n') + '\n';

// el README por bloques ({id, md}) para que el editor sepa qué parte de la vista previa es cada uno
export function renderBlocks(p) {
  const h = p.header || {};
  const out = [];

  // encabezado centrado: imagen, título, insignias
  const head = [];
  if (h.image) head.push(`    <img width="${attr(h.imageWidth || 300)}" src="${attr(h.image)}" alt="${attr(h.imageAlt || '')}"/>`);
  if (h.title) head.push(`    <h1>${h.title}</h1>`);
  if (h.subtitle) head.push(`    <p>${h.subtitle}</p>`);
  for (const b of (h.badges || []).filter(b => b.label)) {
    const img = `<img src="${attr(badgeUrl(b, h.badgeColor))}" alt="${attr(b.label)}"/>`;
    head.push(`    ${b.url ? `<a href="${attr(b.url)}">${img}</a>` : img}`);
  }
  if (head.length) out.push({ id: 'header', md: `<div align="center">\n${head.join('\n')}\n</div>` });

  (p.sections || []).forEach((s, i) => {
    if (s.hidden) return;
    const block = [];
    if (s.type === 'text' && s.body?.trim()) block.push(s.body.trim());
    if (s.type === 'talks') {
      const items = (s.items || []).filter(t => t.title);
      if (items.length) block.push(items.map(t => `- ${t.venue ? `**${t.venue}**: ` : ''}${link(t.title, t.url)}`).join('\n'));
    }
    if (s.type === 'projects') {
      const items = (s.items || []).filter(t => t.name);
      if (items.length) block.push(['| Project | Description |', '| --- | --- |', ...items.map(t => `| ${link(cell(t.name), t.url)} | ${cell(t.desc)} |`)].join('\n'));
    }
    if (s.type === 'list') {
      const items = (s.items || []).filter(t => t.text);
      if (items.length) block.push(items.map(t => `- ${t.text}`).join('\n'));
    }
    if (!block.length) return;
    out.push({ id: `sec-${i}`, md: (s.title ? `## ${s.title}\n\n` : '') + block.join('\n\n') });
  });

  if (p.footer?.trim()) out.push({ id: 'footer', md: `---\n\n<div align="center">\n    <sub>${p.footer.trim()}</sub>\n</div>` });
  return out;
}

// rutas relativas del README (./assets/cat.gif) → URL real del repo, para la vista previa
export const rawBase = p => `https://raw.githubusercontent.com/${p.repo || 'JeroHoyos/JeroHoyos'}/${p.branch || 'main'}/`;
