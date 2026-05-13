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
  series:      mi-serie           ← opcional: slug de la serie
  series_es:   Mi Serie           ← opcional: nombre ES de la serie
  series_en:   My Series          ← opcional: nombre EN de la serie
  chapter:     1                  ← opcional: número de capítulo (entero)

Cuerpo: Markdown estándar con soporte de $...$ y $$...$$ para LaTeX.

Si el cuerpo está vacío (solo frontmatter), el builder registra el post
en el índice pero NO sobreescribe el HTML ya existente — útil para
artículos escritos a mano.
"""

import re
import html as _html
from pathlib import Path


def _e(s):
    """Escape a plain-text string for safe insertion into HTML."""
    return _html.escape(str(s), quote=True)

FONTS = (
    "https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400"
    "&family=Bebas+Neue&family=DM+Serif+Display:ital@0;1&display=swap"
)

KATEX_CSS = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"
KATEX_JS  = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"
KATEX_AR  = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
KATEX_CSS_SRI = "sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+"
KATEX_JS_SRI  = "sha384-7zkQWkzuo3B5mTepMUcHkMB5jZaolc2xDwL6VFqjFALcbeS9Ggm/Yr2r3Dy4lfFg"
KATEX_AR_SRI  = "sha384-43gviWU0YVjaDtb/GhzOouOXtZMP/7XUzwPTstBeZFe/+rCMvRwr4yROQP43s0Xk"


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
    # Bloques de código cercados — escapar contenido para evitar inyección HTML
    text = re.sub(
        r"```[\w]*\n(.*?)```",
        lambda m: f"<pre><code>{_html.escape(m.group(1))}</code></pre>",
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

def _series_nav_html(current_slug, all_chapter_metas):
    series_name = _e(all_chapter_metas[0].get("series_es", all_chapter_metas[0].get("series", "")))
    chs = ""
    for ch in all_chapter_metas:
        slug = ch.get("slug", "")
        num = str(ch.get("chapter", 0)).zfill(2)
        title = _e(ch.get("title_es", ""))
        if slug == current_slug:
            chs += f'<span class="sn-ch sn-ch--active"><span class="sn-num">{num}</span>{title}</span>'
        else:
            chs += f'<a href="{slug}.html" class="sn-ch"><span class="sn-num">{num}</span>{title}</a>'
    return f'<div class="series-nav"><div class="sn-label">SERIE — <span class="sn-name">{series_name}</span></div><div class="sn-chapters">{chs}</div></div>'


def _blog_template(meta, body_html, series_nav=""):
    title   = _e(meta.get("title_es", ""))
    date    = _e(meta.get("date_es", ""))
    excerpt = _e(meta.get("excerpt_es", ""))
    rt      = _e(meta.get("read_time", ""))
    chapter = meta.get("chapter", "")
    series_name = _e(meta.get("series_es", ""))

    # Kicker: "SERIE · CAP 1" o solo la fecha
    if series_name and chapter:
        kicker = f'{series_name} &nbsp;·&nbsp; CAP. {_e(str(chapter))}'
    elif series_name:
        kicker = series_name
    else:
        kicker = date

    # Footer meta del hero
    foot_items = []
    if date:
        foot_items.append(f'<span>{date}</span>')
    if rt:
        foot_items.append(f'<span>{rt} de lectura</span>')
    foot_html = '<span class="hero-foot-sep">·</span>'.join(foot_items)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Blog</title>
<meta name="description" content="{excerpt}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="{KATEX_CSS}" integrity="{KATEX_CSS_SRI}" crossorigin="anonymous">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth;font-size:18px}}
:root{{--bg:#fafaf8;--ink:#0d0d0d;--mid:#555;--soft:#888;--faint:#bbb;--rule:#e8e8e5;--code-bg:#f2f2f0;--accent:#0d0d0d}}
body{{background:var(--bg);color:var(--ink);font-family:'Space Mono',monospace;overflow-x:hidden;line-height:1.8}}

#progress{{position:fixed;top:0;left:0;height:2px;background:var(--ink);width:0%;z-index:300;pointer-events:none;transition:width .08s linear}}

nav{{position:sticky;top:0;z-index:200;background:rgba(250,250,248,.96);backdrop-filter:blur(14px);border-bottom:1px solid var(--rule);padding:.9rem 5vw;display:flex;align-items:center;justify-content:space-between;gap:1rem}}
.nav-back{{display:inline-flex;align-items:center;gap:.5rem;font-size:.48rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--soft);text-decoration:none;border:1px solid var(--rule);padding:.45rem 1rem;transition:all .2s;white-space:nowrap}}
.nav-back:hover{{color:var(--ink);border-color:var(--ink);background:rgba(0,0,0,.03)}}
.nav-title{{font-size:.5rem;letter-spacing:1px;color:var(--faint);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;text-align:center;opacity:0;transition:opacity .3s}}
.nav-title.visible{{opacity:1}}
.nav-rt{{font-size:.46rem;letter-spacing:2px;text-transform:uppercase;color:var(--faint);white-space:nowrap}}

.article-hero{{padding:5.5rem 5vw 5rem;border-bottom:1px solid var(--rule);background:var(--bg)}}
.hero-kicker{{font-size:.46rem;letter-spacing:4px;text-transform:uppercase;color:var(--soft);margin-bottom:2.2rem;display:flex;align-items:center;gap:.9rem}}
.hero-kicker-bar{{width:1.8rem;height:1px;background:var(--faint);flex-shrink:0}}
.article-hero h1{{font-family:'DM Serif Display',serif;font-size:clamp(2rem,4.5vw,4.2rem);letter-spacing:-.02em;line-height:1.1;color:var(--ink);margin-bottom:2rem;max-width:1000px}}
.hero-excerpt{{font-size:.9rem;line-height:2;color:var(--mid);max-width:860px;margin-bottom:2.5rem}}
.hero-foot{{display:flex;align-items:center;gap:.8rem;font-size:.48rem;letter-spacing:2px;text-transform:uppercase;color:var(--faint);padding-top:1.8rem;border-top:1px solid var(--rule)}}
.hero-foot-sep{{color:var(--rule)}}

.article-wrap{{max-width:1200px;margin:0 auto;padding:4.5rem 5vw 8rem}}
.article-wrap h2{{font-family:'Bebas Neue',sans-serif;font-size:clamp(1.9rem,4vw,3rem);letter-spacing:1px;line-height:1;color:var(--ink);margin:4rem 0 1.4rem;padding-top:1.2rem;border-top:2px solid var(--ink)}}
.article-wrap h3{{font-family:'DM Serif Display',serif;font-size:1.5rem;color:var(--ink);margin:2.8rem 0 .9rem;font-style:italic}}
.article-wrap h4{{font-size:.65rem;letter-spacing:3px;text-transform:uppercase;color:var(--soft);margin:2rem 0 .7rem}}
.article-wrap p{{font-size:1rem;line-height:2;color:#2a2a2a;margin-bottom:1.6rem}}
.article-wrap strong{{color:var(--ink);font-weight:700}}
.article-wrap em{{font-family:'DM Serif Display',serif;font-style:italic;font-size:1.05em}}
.article-wrap a{{color:var(--ink);text-underline-offset:3px}}
.article-wrap a:hover{{color:var(--soft)}}
.article-wrap code{{font-family:'Space Mono',monospace;font-size:.72rem;background:var(--code-bg);padding:.18rem .45rem;border-radius:2px}}
.article-wrap pre{{background:var(--code-bg);border-left:3px solid var(--ink);padding:1.6rem 1.8rem;overflow-x:auto;margin:2.4rem 0}}
.article-wrap pre code{{background:none;padding:0;font-size:.7rem;line-height:2;border-radius:0}}
.article-wrap blockquote{{border-left:3px solid var(--faint);padding-left:1.6rem;margin:2.4rem 0;color:var(--mid);font-family:'DM Serif Display',serif;font-style:italic;font-size:1.05rem;line-height:1.9}}
.article-wrap ul,.article-wrap ol{{margin:1.2rem 0 1.8rem 1.8rem}}
.article-wrap li{{font-size:1rem;line-height:2;color:#2a2a2a;margin-bottom:.4rem}}
.article-wrap hr{{border:none;border-top:1px solid var(--rule);margin:3.5rem 0}}
.article-wrap table{{width:100%;border-collapse:collapse;font-size:.75rem;margin:2rem 0}}
.article-wrap th{{text-align:left;border-bottom:2px solid var(--ink);padding:.6rem .8rem;font-size:.55rem;letter-spacing:2.5px;text-transform:uppercase}}
.article-wrap td{{border-bottom:1px solid var(--rule);padding:.6rem .8rem;color:#444}}
.katex-display{{overflow-x:auto;padding:.9rem 0}}

.series-nav{{background:#efefed;border-left:3px solid var(--ink);padding:1.2rem 1.5rem;margin:0 0 3.5rem}}
.sn-label{{font-size:.46rem;letter-spacing:3.5px;text-transform:uppercase;color:var(--soft);margin-bottom:.9rem}}
.sn-name{{color:var(--ink)}}
.sn-chapters{{display:flex;flex-direction:column}}
.sn-ch,.sn-ch--active{{display:flex;align-items:baseline;gap:.8rem;padding:.55rem 0;border-top:1px solid var(--rule);text-decoration:none;color:var(--soft);font-size:.75rem;transition:color .2s}}
.sn-ch:hover{{color:var(--ink)}}
.sn-ch--active{{color:var(--ink);pointer-events:none;font-family:'DM Serif Display',serif;font-style:italic}}
.sn-num{{font-size:.44rem;letter-spacing:2px;min-width:2.2rem;padding-top:.1rem}}

@media(max-width:700px){{
  nav{{padding:.8rem 1.4rem}}
  .nav-title{{display:none}}
  .article-hero{{padding:3.5rem 1.4rem 3.5rem}}
  .article-wrap{{padding:3rem 1.4rem 5rem}}
}}
@media(max-width:420px){{
  html{{font-size:16px}}
  .article-hero{{padding:2.5rem 1.2rem 2.5rem}}
  .article-wrap{{padding:2.5rem 1.2rem 4rem}}
}}
</style>
</head>
<body>
<div id="progress"></div>
<nav>
  <a href="../index.html" class="nav-back">← Blog</a>
  <span class="nav-title" id="nav-title">{title}</span>
  <span class="nav-rt">{rt + ' lectura' if rt else ''}</span>
</nav>
<div class="article-hero">
  <div class="hero-kicker"><span class="hero-kicker-bar"></span>{kicker}</div>
  <h1>{title}</h1>
  <p class="hero-excerpt">{excerpt}</p>
  <div class="hero-foot">{foot_html}</div>
</div>
<article class="article-wrap">
{series_nav}
{body_html}
</article>
<script>
(function(){{
  const bar=document.getElementById('progress');
  const nav=document.getElementById('nav-title');
  const hero=document.querySelector('.article-hero');
  window.addEventListener('scroll',function(){{
    const d=document.documentElement;
    const s=d.scrollTop||document.body.scrollTop;
    const h=d.scrollHeight-d.clientHeight;
    if(h>0) bar.style.width=(s/h*100)+'%';
    if(hero) nav.classList.toggle('visible', s > hero.offsetHeight * .6);
  }},{{passive:true}});
}})();
</script>
<script defer src="{KATEX_JS}" integrity="{KATEX_JS_SRI}" crossorigin="anonymous"></script>
<script defer src="{KATEX_AR}" integrity="{KATEX_AR_SRI}" crossorigin="anonymous" onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}]}})"></script>
</body>
</html>"""


# ── Punto de entrada ───────────────────────────────────────────────────────

def build_blog_pages():
    """
    Escanea blog/posts/*.md, genera HTML para posts con contenido,
    y retorna la lista de entradas para el índice del blog.
    Los archivos se ordenan por nombre descendente (más reciente primero
    si usas prefijo YYYY-MM). Los posts de una misma serie quedan agrupados
    en el índice bajo un bloque de serie.
    """
    posts_dir = Path("blog/posts")
    posts_dir.mkdir(parents=True, exist_ok=True)

    # Pasada 1: parsear todo sin generar HTML
    post_data = []
    for md_file in sorted(posts_dir.glob("*.md"), reverse=True):
        text = md_file.read_text(encoding="utf-8")
        meta, content = _parse_frontmatter(text)
        meta["slug"] = meta.get("slug", md_file.stem)
        post_data.append((md_file, meta, content))

    # Construir mapa de series {slug: [meta, ...] ordenados por capítulo}
    series_map: dict = {}
    for _, meta, _ in post_data:
        s = meta.get("series")
        if s:
            series_map.setdefault(s, []).append(meta)
    for s in series_map:
        series_map[s].sort(key=lambda m: int(m.get("chapter", 0)))

    # Pasada 2: generar HTML y construir entradas
    entries = []
    for _, meta, content in post_data:
        slug = meta["slug"]
        output_path = Path("blog") / f"{slug}.html"

        if content:
            body_html = _md_to_html(content)
            s = meta.get("series")
            series_nav = _series_nav_html(slug, series_map[s]) if s else ""
            output_path.write_text(_blog_template(meta, body_html, series_nav), encoding="utf-8")
            print(f"   📝 Generado: blog/{slug}.html")

        tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
        entries.append({
            "url":        f"blog/{slug}.html",
            "slug":       slug,
            "date_es":    meta.get("date_es", ""),
            "date_en":    meta.get("date_en", ""),
            "tags":       tags,
            "title_es":   meta.get("title_es", ""),
            "title_en":   meta.get("title_en", ""),
            "excerpt_es": meta.get("excerpt_es", ""),
            "excerpt_en": meta.get("excerpt_en", ""),
            "read_es":    meta.get("read_es", "Leer artículo →"),
            "read_en":    meta.get("read_en", "Read article →"),
            "series":     meta.get("series", ""),
            "series_es":  meta.get("series_es", ""),
            "series_en":  meta.get("series_en", ""),
            "chapter":    int(meta.get("chapter", 0)),
        })

    return entries
