"""
Blog builder: lee blog/posts/*.md y genera páginas HTML + lista para el índice.

Estructura de un post:
  blog/posts/mi-articulo.md

Frontmatter (entre --- ... ---):
  slug:        mi-articulo        ← nombre del archivo HTML de salida
  title_es:    Título en español
  title_en:    Title in English
  date_es:     Enero 2025
  date_en:     January 2025
  tags:        Tag1, Tag2, Tag3
  excerpt_es:  Resumen corto en español.
  excerpt_en:  Short summary in English.
  read_time:   10 min             ← opcional
  read_es:     Leer artículo →    ← opcional
  read_en:     Read article →     ← opcional

Cuerpo: Markdown estándar con soporte de $...$ y $$...$$ para LaTeX.

Si el cuerpo está vacío (solo frontmatter), el builder registra el post
en el índice pero NO sobreescribe el HTML ya existente — útil para
artículos escritos a mano.
"""

import re
from pathlib import Path

FONTS = (
    "https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400"
    "&family=Bebas+Neue&family=DM+Serif+Display:ital@0;1&display=swap"
)

KATEX_CSS = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"
KATEX_JS  = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"
KATEX_AR  = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"


# ── Parseo de frontmatter ──────────────────────────────────────────────────

def _parse_frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)", text, re.DOTALL)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2).strip()


# ── Markdown → HTML ────────────────────────────────────────────────────────

def _md_to_html(text):
    try:
        import markdown as md_lib
        return md_lib.markdown(
            text,
            extensions=["extra", "toc", "fenced_code", "tables"],
        )
    except ImportError:
        return _simple_md(text)


def _simple_md(text):
    """Conversión mínima sin dependencias externas."""
    # Bloques de código cercados
    text = re.sub(
        r"```[\w]*\n(.*?)```",
        lambda m: f"<pre><code>{m.group(1)}</code></pre>",
        text,
        flags=re.DOTALL,
    )
    # Encabezados
    for n in range(6, 0, -1):
        text = re.sub(
            rf"^{'#' * n} (.+)$",
            rf"<h{n}>\1</h{n}>",
            text,
            flags=re.MULTILINE,
        )
    # Negrita / cursiva / código inline
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*",     r"<em>\1</em>",         text)
    text = re.sub(r"`(.+?)`",       r"<code>\1</code>",     text)
    # Párrafos
    blocks = re.split(r"\n\n+", text.strip())
    parts = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        parts.append(b if b.startswith("<") else f"<p>{b.replace(chr(10), ' ')}</p>")
    return "\n".join(parts)


# ── Plantilla HTML ─────────────────────────────────────────────────────────

def _blog_template(meta, body_html):
    title    = meta.get("title_es", "")
    date     = meta.get("date_es", "")
    excerpt  = meta.get("excerpt_es", "")
    rt       = meta.get("read_time", "")
    tags_raw = meta.get("tags", "")
    tags     = [t.strip() for t in tags_raw.split(",") if t.strip()]
    tags_html = "".join(f'<span class="hero-tag">{t}</span>' for t in tags)
    rt_html  = f'<span class="hero-tag hero-tag--accent">{rt} lectura</span>' if rt else ""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Blog</title>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="{KATEX_CSS}">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
:root{{--bg:#ffffff;--ink:#111111;--mid:#444;--soft:#888;--faint:#ccc;--rule:#e8e8e8;--code-bg:#f5f5f3}}
body{{background:var(--bg);color:var(--ink);font-family:'Space Mono',monospace;overflow-x:hidden;line-height:1.8}}

nav{{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--rule);padding:1.2rem 4rem;display:flex;align-items:center;justify-content:space-between}}
.nav-back{{font-size:.55rem;letter-spacing:3px;text-transform:uppercase;color:var(--soft);text-decoration:none;display:flex;align-items:center;gap:.5rem;transition:color .2s}}
.nav-back:hover{{color:var(--ink)}}
.nav-date{{font-size:.48rem;letter-spacing:2px;text-transform:uppercase;color:var(--faint)}}

.article-hero{{min-height:55vh;display:flex;flex-direction:column;justify-content:flex-end;padding:4rem;position:relative;overflow:hidden;border-bottom:1px solid var(--rule);background:#f9f9f7}}
.hero-bg{{position:absolute;inset:0;z-index:0;background:radial-gradient(ellipse 60% 50% at 80% 20%,rgba(0,0,0,.03) 0%,transparent 70%),radial-gradient(ellipse 40% 60% at 20% 80%,rgba(0,0,0,.02) 0%,transparent 60%)}}
.hero-grid{{position:absolute;inset:0;z-index:0;background-image:linear-gradient(rgba(0,0,0,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.04) 1px,transparent 1px);background-size:60px 60px}}
.hero-num{{font-family:'Bebas Neue',sans-serif;font-size:clamp(6rem,14vw,14rem);color:rgba(0,0,0,.05);position:absolute;top:1.5rem;right:3rem;line-height:1;z-index:1;pointer-events:none;letter-spacing:-4px}}
.hero-inner{{position:relative;z-index:2;max-width:860px}}
.hero-meta{{display:flex;align-items:center;gap:.8rem;margin-bottom:2rem;flex-wrap:wrap}}
.hero-tag{{font-size:.44rem;letter-spacing:3px;text-transform:uppercase;padding:.3rem .8rem;border:1px solid var(--rule);color:var(--soft)}}
.hero-tag--accent{{border-color:var(--ink);background:var(--ink);color:#fff}}
.hero-date{{font-size:.48rem;letter-spacing:2px;text-transform:uppercase;color:var(--faint)}}
.article-hero h1{{font-family:'Bebas Neue',sans-serif;font-size:clamp(2.8rem,6vw,5.5rem);letter-spacing:1px;line-height:.92;color:var(--ink);margin-bottom:1.8rem}}
.hero-excerpt{{font-family:'DM Serif Display',serif;font-style:italic;font-size:clamp(.95rem,2vw,1.2rem);color:var(--soft);line-height:1.75;max-width:640px}}

.article-wrap{{max-width:760px;margin:0 auto;padding:5rem 2rem 8rem}}
.article-wrap h2{{font-family:'Bebas Neue',sans-serif;font-size:clamp(1.8rem,4vw,3rem);letter-spacing:1px;line-height:1;color:var(--ink);margin:4rem 0 1.5rem;padding-top:1rem;border-top:1px solid var(--rule)}}
.article-wrap h3{{font-family:'DM Serif Display',serif;font-size:1.3rem;color:var(--ink);margin:2.5rem 0 1rem}}
.article-wrap h4{{font-size:.7rem;letter-spacing:2px;text-transform:uppercase;color:var(--mid);margin:2rem 0 .8rem}}
.article-wrap p{{font-size:.72rem;line-height:2.15;color:#333;margin-bottom:1.4rem}}
.article-wrap strong{{color:var(--ink)}}
.article-wrap em{{font-family:'DM Serif Display',serif;font-style:italic}}
.article-wrap a{{color:var(--ink);text-underline-offset:3px}}
.article-wrap a:hover{{color:var(--soft)}}
.article-wrap code{{font-family:'Space Mono',monospace;font-size:.63rem;background:var(--code-bg);padding:.15rem .4rem;border:1px solid #eee}}
.article-wrap pre{{background:var(--code-bg);border:1px solid #e5e5e5;padding:1.5rem;overflow-x:auto;margin:2rem 0}}
.article-wrap pre code{{background:none;border:none;padding:0;font-size:.62rem;line-height:1.8}}
.article-wrap blockquote{{border-left:3px solid var(--ink);padding-left:1.5rem;margin:2rem 0;color:var(--mid)}}
.article-wrap ul,.article-wrap ol{{margin:1rem 0 1.4rem 1.5rem}}
.article-wrap li{{font-size:.72rem;line-height:2;color:#333;margin-bottom:.3rem}}
.article-wrap hr{{border:none;border-top:1px solid var(--rule);margin:3rem 0}}
.article-wrap table{{width:100%;border-collapse:collapse;font-size:.63rem;margin:2rem 0}}
.article-wrap th{{text-align:left;border-bottom:2px solid var(--ink);padding:.5rem .8rem;font-size:.52rem;letter-spacing:2px;text-transform:uppercase}}
.article-wrap td{{border-bottom:1px solid var(--rule);padding:.5rem .8rem;color:#444}}
.katex-display{{overflow-x:auto;padding:.8rem 0}}

@media(max-width:600px){{
  nav{{padding:1rem 1.2rem}}
  .article-hero{{padding:2rem 1.2rem 3rem;min-height:40vh}}
  .hero-num{{display:none}}
  .article-wrap{{padding:3rem 1.2rem 5rem}}
}}
</style>
</head>
<body>
<nav>
  <a href="../index.html" class="nav-back">← Volver</a>
  <span class="nav-date">{date}</span>
</nav>
<div class="article-hero">
  <div class="hero-bg"></div>
  <div class="hero-grid"></div>
  <div class="hero-num">01</div>
  <div class="hero-inner">
    <div class="hero-meta">
      {tags_html}
      {rt_html}
      <span class="hero-date">{date}</span>
    </div>
    <h1>{title}</h1>
    <p class="hero-excerpt">{excerpt}</p>
  </div>
</div>
<article class="article-wrap">
{body_html}
</article>
<script defer src="{KATEX_JS}"></script>
<script defer src="{KATEX_AR}" onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}]}})"></script>
</body>
</html>"""


# ── Punto de entrada ───────────────────────────────────────────────────────

def build_blog_pages():
    """
    Escanea blog/posts/*.md, genera HTML para posts con contenido,
    y retorna la lista de entradas para el índice del blog.
    Los archivos ordenados por nombre descendente (más reciente primero
    si usas prefijo YYYY-MM).
    """
    posts_dir = Path("blog/posts")
    posts_dir.mkdir(parents=True, exist_ok=True)

    entries = []
    for md_file in sorted(posts_dir.glob("*.md"), reverse=True):
        text = md_file.read_text(encoding="utf-8")
        meta, content = _parse_frontmatter(text)
        slug = meta.get("slug", md_file.stem)

        output_path = Path("blog") / f"{slug}.html"
        if content:
            body_html = _md_to_html(content)
            output_path.write_text(_blog_template(meta, body_html), encoding="utf-8")
            print(f"   📝 Generado: blog/{slug}.html")

        tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
        entries.append({
            "url":        f"blog/{slug}.html",
            "date_es":    meta.get("date_es", ""),
            "date_en":    meta.get("date_en", ""),
            "tags":       tags,
            "title_es":   meta.get("title_es", ""),
            "title_en":   meta.get("title_en", ""),
            "excerpt_es": meta.get("excerpt_es", ""),
            "excerpt_en": meta.get("excerpt_en", ""),
            "read_es":    meta.get("read_es", "Leer artículo →"),
            "read_en":    meta.get("read_en", "Read article →"),
        })

    return entries
