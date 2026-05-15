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

SITE_URL = "https://jerohoyos.github.io"
OG_IMAGE = f"{SITE_URL}/og.png"

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
    """Conversión robusta sin dependencias externas."""
    saved, idx = {}, [0]

    def save_code(m):
        lang = (m.group(1) or "").strip()
        code = _html.escape(m.group(2))
        key = f"\x00{idx[0]}\x00"
        cls = f' class="language-{lang}"' if lang else ""
        saved[key] = f"<pre><code{cls}>{code}</code></pre>"
        idx[0] += 1
        return f"\n\n{key}\n\n"

    text = re.sub(r"```(\w*)\n(.*?)```", save_code, text, flags=re.DOTALL)

    for n in range(6, 0, -1):
        text = re.sub(rf"^{'#' * n} (.+)$", rf"<h{n}>\1</h{n}>", text, flags=re.MULTILINE)

    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*",     r"<em>\1</em>",         text)
    text = re.sub(r"`([^`]+)`",     r"<code>\1</code>",     text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)

    parts = []
    for b in re.split(r"\n{2,}", text.strip()):
        b = b.strip()
        if not b:
            continue
        if b in saved:
            parts.append(saved[b])
        elif b.startswith("<"):
            parts.append(b)
        elif re.match(r"^[-*] ", b, re.MULTILINE):
            lis = "".join(
                f"<li>{m.group(1)}</li>"
                for m in re.finditer(r"^[-*] (.+)$", b, re.MULTILINE)
            )
            parts.append(f"<ul>{lis}</ul>")
        elif re.match(r"^\d+\. ", b):
            lis = "".join(
                f"<li>{m.group(1)}</li>"
                for m in re.finditer(r"^\d+\. (.+)$", b, re.MULTILINE)
            )
            parts.append(f"<ol>{lis}</ol>")
        elif re.match(r"^\|", b):
            lines = [l for l in b.splitlines() if l.strip() and not re.match(r"^[\|\-:\s]+$", l)]
            if lines:
                def _cells(line):
                    cs = [c.strip() for c in line.split("|")]
                    return [c for c in cs if c]
                ths = _cells(lines[0])
                th_html = "<tr>" + "".join(f"<th>{h}</th>" for h in ths) + "</tr>"
                tr_html = "".join(
                    "<tr>" + "".join(f"<td>{c}</td>" for c in _cells(l)) + "</tr>"
                    for l in lines[1:]
                )
                parts.append(f"<table><thead>{th_html}</thead><tbody>{tr_html}</tbody></table>")
        elif b.startswith(">"):
            inner = re.sub(r"^> ?", "", b, flags=re.MULTILINE).replace("\n", " ")
            parts.append(f"<blockquote><p>{inner}</p></blockquote>")
        elif re.match(r"^-{3,}$", b) or re.match(r"^\*{3,}$", b):
            parts.append("<hr>")
        else:
            parts.append(f"<p>{b.replace(chr(10), ' ')}</p>")

    return "\n".join(parts)


# ── Plantilla HTML ─────────────────────────────────────────────────────────

def _series_nav_html(current_slug, all_chapter_metas):
    m0 = all_chapter_metas[0]
    sn_es = _e(m0.get("series_es", m0.get("series", "")))
    sn_en = _e(m0.get("series_en", m0.get("series_es", m0.get("series", ""))))
    chs = ""
    for ch in all_chapter_metas:
        slug   = ch.get("slug", "")
        num    = str(ch.get("chapter", 0)).zfill(2)
        t_es   = _e(ch.get("title_es", ""))
        t_en   = _e(ch.get("title_en", ch.get("title_es", "")))
        d_es   = _e(ch.get("date_es", ""))
        d_en   = _e(ch.get("date_en", ch.get("date_es", "")))
        inner = (
            f'<span class="sn-num">{num}</span>'
            f'<span class="sn-info">'
            f'<span class="sn-title" data-es="{t_es}" data-en="{t_en}">{t_es}</span>'
            f'<span class="sn-date" data-es="{d_es}" data-en="{d_en}">{d_es}</span>'
            f'</span>'
        )
        if slug == current_slug:
            chs += f'<div class="sn-ch sn-ch--active">{inner}</div>'
        else:
            chs += f'<a href="{slug}.html" class="sn-ch">{inner}</a>'
    return (
        f'<div class="series-nav">'
        f'<div class="sn-header">'
        f'<span class="sn-kicker" data-es="Serie" data-en="Series">Serie</span>'
        f'<span class="sn-name" data-es="{sn_es}" data-en="{sn_en}">{sn_es}</span>'
        f'</div>'
        f'<div class="sn-chapters">{chs}</div>'
        f'</div>'
    )


def _article_footer(current_slug, series_chapters):
    """Bottom-of-article nav: prev/next chapter + back-to-blog."""
    prev_ch = next_ch = None
    if series_chapters:
        for i, ch in enumerate(series_chapters):
            if ch.get("slug") == current_slug:
                if i > 0:
                    prev_ch = series_chapters[i - 1]
                if i < len(series_chapters) - 1:
                    next_ch = series_chapters[i + 1]
                break

    def _ch_link(ch, direction):
        n = str(ch.get("chapter", 0)).zfill(2)
        t_es = _e(ch.get("title_es", ""))
        t_en = _e(ch.get("title_en", ch.get("title_es", "")))
        if direction == "prev":
            d_es, d_en, cls = "← Capítulo anterior", "← Previous chapter", "af-ch af-ch--prev"
        else:
            d_es, d_en, cls = "Siguiente capítulo →", "Next chapter →", "af-ch af-ch--next"
        return (
            f'<a href="{ch["slug"]}.html" class="{cls}">'
            f'<span class="af-dir" data-es="{_e(d_es)}" data-en="{_e(d_en)}">{_e(d_es)}</span>'
            f'<span class="af-ch-title" data-es="{t_es}" data-en="{t_en}">{t_es}</span>'
            f'<span class="af-ch-num">Cap. {n}</span>'
            f'</a>'
        )

    prev_html = _ch_link(prev_ch, "prev") if prev_ch else ""
    next_html = _ch_link(next_ch, "next") if next_ch else ""

    nav_html = ""
    if prev_html or next_html:
        nav_html = (
            f'<div class="af-nav">'
            f'{prev_html or "<div></div>"}'
            f'{next_html or "<div></div>"}'
            f'</div>'
        )

    return (
        f'<footer class="article-footer">'
        f'{nav_html}'
        f'<a href="../index.html#blog" class="af-back"'
        f' data-es="← Volver al blog" data-en="← Back to blog">← Volver al blog</a>'
        f'</footer>'
    )


def _build_toc(body_html, read_time="", id_prefix="", lang="es"):
    """Inject IDs into h2/h3 headings and return (modified_html, toc_html)."""
    seen = {}

    def _slug(text):
        t = re.sub(r"<[^>]+>", "", text).lower().strip()
        t = re.sub(r"[^\w\s-]", "", t)
        t = re.sub(r"[\s_]+", "-", t)
        return t or "section"

    items = []

    def replace(m):
        lvl, attrs, inner = m.group(1), m.group(2) or "", m.group(3)
        base = _slug(inner)
        n = seen.get(base, 0)
        seen[base] = n + 1
        sid = id_prefix + (base if n == 0 else f"{base}-{n}")
        items.append((lvl, sid, re.sub(r"<[^>]+>", "", inner)))
        if "id=" not in attrs:
            return f'<h{lvl}{attrs} id="{sid}">{inner}</h{lvl}>'
        return m.group(0)

    modified = re.sub(r"<h([23])([^>]*)>(.*?)</h\1>", replace, body_html, flags=re.DOTALL)

    if not items:
        return modified, ""

    links = ""
    for lvl, sid, text in items:
        escaped = _html.escape(text)
        if lvl == "2":
            links += f'<a href="#{sid}" class="toc-link">{escaped}</a>\n'
        else:
            links += f'<a href="#{sid}" class="toc-link toc-h3">{escaped}</a>\n'

    kicker = "Contenido" if lang == "es" else "Contents"

    toc_html = (
        f'<div class="toc-kicker">{kicker}</div>'
        f'<nav class="toc-nav">\n{links}</nav>'
    )
    return modified, toc_html


def _blog_template(meta, body_html, series_nav="", toc_html="", series_chapters=None, body_html_en="", toc_html_en=""):
    title      = _e(meta.get("title_es", ""))
    title_en   = _e(meta.get("title_en", meta.get("title_es", "")))
    date       = _e(meta.get("date_es", ""))
    date_en    = _e(meta.get("date_en", ""))
    excerpt    = _e(meta.get("excerpt_es", ""))
    excerpt_en = _e(meta.get("excerpt_en", meta.get("excerpt_es", "")))
    rt         = _e(meta.get("read_time", ""))
    chapter    = meta.get("chapter", "")
    series_name    = _e(meta.get("series_es", ""))
    series_name_en = _e(meta.get("series_en", meta.get("series_es", "")))

    # Kicker bilingüe
    if series_name and chapter:
        kicker    = f'{series_name} &nbsp;·&nbsp; CAP. {_e(str(chapter))}'
        kicker_en = f'{series_name_en} &nbsp;·&nbsp; CH. {_e(str(chapter))}'
    elif series_name:
        kicker    = series_name
        kicker_en = series_name_en
    else:
        kicker    = ""
        kicker_en = ""

    # Tags chips
    raw_tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    tags_html = (
        '<div class="hero-tags">'
        + "".join(f'<span class="hero-tag">{_e(t)}</span>' for t in raw_tags)
        + '</div>'
    ) if raw_tags else ""

    rt_es = f'{rt} lectura' if rt else ''
    rt_en = f'{rt} read'    if rt else ''

    # Date span for hero-meta
    hero_date_html = (
        f'<span class="hero-date" data-es="{date}" data-en="{date_en or date}">{date}</span>'
        if date else ''
    )

    # Kicker div (solo si hay contenido de kicker)
    kicker_div = (
        f'<div class="hero-kicker"><span data-es="{kicker}" data-en="{kicker_en}">{kicker}</span></div>'
        if kicker else ''
    )

    # Article footer (prev/next + back)
    footer_html = _article_footer(meta.get("slug", ""), series_chapters)

    # Body divs (bilingual if EN body provided)
    body_divs = f'<div id="body-es">{body_html}</div>'
    if body_html_en:
        body_divs += f'\n<div id="body-en" style="display:none">{body_html_en}</div>'

    # TOC sidebar (bilingual if EN toc provided)
    if toc_html or toc_html_en:
        toc_sidebar_html = (
            f'<aside class="toc-sidebar">'
            f'<div id="toc-es">{toc_html}</div>'
            + (f'<div id="toc-en" style="display:none">{toc_html_en}</div>' if toc_html_en else '')
            + f'</aside>'
        )
    else:
        toc_sidebar_html = ""

    slug = _e(meta.get("slug", ""))

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Blog</title>
<meta name="description" content="{excerpt}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE_URL}/blog/{slug}.html">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{OG_IMAGE}">
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

body>nav{{position:sticky;top:0;z-index:200;background:rgba(250,250,248,.97);backdrop-filter:blur(14px);border-bottom:1px solid var(--rule);padding:.85rem 5vw;display:flex;align-items:center;justify-content:space-between;gap:1.2rem}}
.nav-back{{display:inline-flex;align-items:center;gap:.5rem;font-size:.55rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--ink);text-decoration:none;border:1px solid rgba(0,0,0,.18);padding:.5rem 1.1rem;transition:all .2s;white-space:nowrap;font-weight:700}}
.nav-back:hover{{border-color:var(--ink);background:rgba(0,0,0,.04)}}
.nav-title{{font-size:.82rem;letter-spacing:.5px;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;text-align:center;opacity:0;transition:opacity .3s;font-weight:700}}
.nav-title.visible{{opacity:1}}
.nav-end{{display:flex;align-items:center;gap:.9rem;flex-shrink:0}}
.nav-rt{{font-size:.48rem;letter-spacing:2px;text-transform:uppercase;color:var(--soft);white-space:nowrap}}
.lang-toggle{{display:flex;gap:.2rem}}
.lang-btn{{font-family:'Space Mono',monospace;font-size:.44rem;letter-spacing:2px;text-transform:uppercase;padding:.32rem .6rem;background:none;border:1px solid var(--rule);color:var(--soft);cursor:pointer;transition:all .18s}}
.lang-btn.active{{border-color:var(--ink);color:var(--ink);font-weight:700}}
.lang-btn:hover{{border-color:var(--soft);color:var(--ink)}}

.article-hero{{padding:5.5rem 4vw 5rem;border-bottom:1px solid var(--rule);background:var(--bg)}}
.hero-kicker{{font-size:.46rem;letter-spacing:4px;text-transform:uppercase;color:var(--soft);margin-bottom:2rem;display:flex;align-items:center;gap:.9rem}}
.hero-meta{{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin-bottom:1rem;flex-wrap:wrap}}
.hero-date{{font-size:.65rem;letter-spacing:3px;text-transform:uppercase;color:var(--mid);white-space:nowrap;flex-shrink:0}}
.article-hero h1{{font-family:'DM Serif Display',serif;font-size:clamp(2.5rem,6vw,5.5rem);letter-spacing:-.025em;line-height:1.06;color:var(--ink);margin-bottom:1.2rem;max-width:1000px}}
.hero-excerpt{{font-family:'DM Serif Display',serif;font-style:italic;font-size:1.3rem;line-height:1.65;color:#2a2a2a;max-width:820px}}

.article-outer{{max-width:1560px;margin:0 auto;padding:4.5rem 4vw 8rem;display:grid;grid-template-columns:1fr 290px;gap:3.5rem;align-items:start}}
.article-wrap{{min-width:0}}
.toc-sidebar{{position:sticky;top:5rem;max-height:calc(100vh - 7rem);overflow-y:auto;scrollbar-width:none;width:100%;box-sizing:border-box}}
.toc-sidebar::-webkit-scrollbar{{display:none}}
.toc-kicker{{font-size:11px;letter-spacing:2px;text-transform:uppercase;color:var(--soft);margin-bottom:.3rem;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
.toc-label{{display:block;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:17px;font-weight:700;color:var(--ink);margin-bottom:.9rem;padding-bottom:.75rem;border-bottom:1px solid var(--rule)}}
.toc-nav{{display:block;padding-top:2px}}
.toc-link{{display:block;width:100%;box-sizing:border-box;padding:5px 8px 5px 22px;border-radius:6px;position:relative;color:#777;text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13.5px;line-height:1.5;transition:background .15s,color .15s}}
.toc-link::before{{content:"•";position:absolute;left:8px;top:7px;font-size:10px;line-height:1;color:#ccc;transition:color .15s}}
.toc-link:hover{{color:var(--ink)}}
.toc-link:hover::before{{color:var(--soft)}}
.toc-link.active{{background:var(--ink);color:#fff;font-weight:600}}
.toc-link.active::before{{color:#fff}}
.toc-h3{{padding-left:34px;font-size:12.5px;color:#999}}
.toc-h3::before{{font-size:7px;top:9px}}
.toc-h3.active{{background:var(--ink);color:#fff;font-weight:600}}
.toc-footer{{margin-top:.9rem;padding-top:.65rem;border-top:1px solid var(--rule);font-size:12px;color:var(--soft);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
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
.stub-msg{{font-size:.52rem!important;letter-spacing:4px;text-transform:uppercase;color:var(--faint)!important;padding:5rem 0;margin:0!important}}
.article-wrap table{{width:100%;border-collapse:collapse;font-size:.75rem;margin:2rem 0}}
.article-wrap th{{text-align:left;border-bottom:2px solid var(--ink);padding:.6rem .8rem;font-size:.55rem;letter-spacing:2.5px;text-transform:uppercase}}
.article-wrap td{{border-bottom:1px solid var(--rule);padding:.6rem .8rem;color:#444}}
.katex-display{{overflow-x:auto;padding:.9rem 0}}

.hero-tags{{display:flex;flex-wrap:wrap;gap:.45rem}}
.hero-tag{{font-size:.38rem;letter-spacing:2px;text-transform:uppercase;padding:.25rem .65rem;border:1px solid var(--rule);color:var(--soft)}}

.series-nav{{border:1px solid var(--rule);border-left:3px solid var(--ink);padding:1.4rem 1.6rem;margin:0 0 3.5rem}}
.sn-header{{display:flex;align-items:baseline;gap:.7rem;margin-bottom:1rem;padding-bottom:.8rem;border-bottom:1px solid var(--rule)}}
.sn-kicker{{font-size:.4rem;letter-spacing:3px;text-transform:uppercase;color:var(--faint)}}
.sn-name{{font-family:'DM Serif Display',serif;font-size:1.05rem;color:var(--ink)}}
.sn-chapters{{display:flex;flex-direction:column}}
.sn-ch,.sn-ch--active{{display:flex;align-items:center;gap:.9rem;padding:.6rem 0;border-bottom:1px solid var(--rule);text-decoration:none;color:inherit;transition:background .15s}}
.sn-ch:last-child,.sn-ch--active:last-child{{border-bottom:none}}
.sn-ch:hover .sn-title{{color:var(--ink)}}
.sn-ch--active{{pointer-events:none}}
.sn-num{{font-family:'Bebas Neue',sans-serif;font-size:1.1rem;color:var(--faint);min-width:2rem;flex-shrink:0;line-height:1}}
.sn-ch--active .sn-num{{color:var(--ink)}}
.sn-info{{display:flex;flex-direction:column;gap:.1rem;min-width:0}}
.sn-title{{font-size:.7rem;color:var(--soft);line-height:1.35;transition:color .15s}}
.sn-ch--active .sn-title{{color:var(--ink);font-weight:700}}
.sn-date{{font-size:.4rem;letter-spacing:2px;text-transform:uppercase;color:var(--faint)}}

.article-footer{{border-top:2px solid var(--ink);margin-top:5rem;padding:3rem 5vw 5rem;max-width:1280px;margin-left:auto;margin-right:auto}}
.af-nav{{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;margin-bottom:2rem}}
.af-ch{{display:flex;flex-direction:column;gap:.35rem;padding:1.3rem 1.5rem;border:1px solid var(--rule);text-decoration:none;color:inherit;transition:border-color .2s,background .2s}}
.af-ch:hover{{border-color:var(--ink);background:rgba(0,0,0,.02)}}
.af-dir{{font-size:.4rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--faint)}}
.af-ch-title{{font-family:'DM Serif Display',serif;font-size:1rem;line-height:1.3;color:var(--ink)}}
.af-ch-num{{font-size:.38rem;letter-spacing:2px;text-transform:uppercase;color:var(--faint)}}
.af-ch--next{{text-align:right}}
.af-back{{display:inline-flex;align-items:center;gap:.5rem;font-size:.44rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--soft);text-decoration:none;border:1px solid var(--rule);padding:.55rem 1.2rem;transition:all .2s}}
.af-back:hover{{color:var(--ink);border-color:var(--ink);background:rgba(0,0,0,.02)}}

@media(max-width:600px){{
  .af-nav{{grid-template-columns:1fr}}
}}

@media(max-width:900px){{
  .article-outer{{grid-template-columns:1fr}}
  .toc-sidebar{{display:none}}
}}
@media(max-width:700px){{
  nav{{padding:.8rem 1.4rem}}
  .nav-title{{display:none}}
  .article-hero{{padding:3.5rem 1.4rem 3.5rem}}
  .article-outer{{padding:3rem 1.4rem 5rem}}
}}
@media(max-width:420px){{
  html{{font-size:16px}}
  .article-hero{{padding:2.5rem 1.2rem 2.5rem}}
  .article-outer{{padding:2.5rem 1.2rem 4rem}}
}}
</style>
</head>
<body>
<div id="progress"></div>
<nav>
  <a href="../index.html#blog" class="nav-back" data-es="← Blog" data-en="← Blog">← Blog</a>
  <span class="nav-title" id="nav-title" data-es="{title}" data-en="{title_en}">{title}</span>
  <div class="nav-end">
    <span class="nav-rt" data-es="{rt_es}" data-en="{rt_en}">{rt_es}</span>
    <div class="lang-toggle">
      <button class="lang-btn active" data-lang="es">ES</button>
      <button class="lang-btn" data-lang="en">EN</button>
    </div>
  </div>
</nav>
<div class="article-hero">
  {kicker_div}
  <div class="hero-meta">{hero_date_html}</div>
  <h1 data-es="{title}" data-en="{title_en}">{title}</h1>
  <p class="hero-excerpt" data-es="{excerpt}" data-en="{excerpt_en}">{excerpt}</p>
</div>
<div class="article-outer">
<article class="article-wrap">
{series_nav}
{body_divs}
</article>
{toc_sidebar_html}
</div>
<script>
/* ── Language toggle ── */
function setLang(lang){{
  document.documentElement.lang=lang;
  document.querySelectorAll('.lang-btn').forEach(function(b){{b.classList.toggle('active',b.dataset.lang===lang);}});
  document.querySelectorAll('[data-es]').forEach(function(el){{
    var txt=el.getAttribute('data-'+lang);
    if(txt!==null) el.innerHTML=txt;
  }});
  var bEn=document.getElementById('body-en');
  var bEs=document.getElementById('body-es');
  var tEn=document.getElementById('toc-en');
  var tEs=document.getElementById('toc-es');
  if(bEn){{
    document.querySelectorAll('.toc-link.active').forEach(function(l){{l.classList.remove('active');}});
    bEs.style.display=lang==='en'?'none':'';
    bEn.style.display=lang==='en'?'':'none';
    if(tEs) tEs.style.display=lang==='en'?'none':'';
    if(tEn) tEn.style.display=lang==='en'?'':'none';
  }}
  try{{localStorage.setItem('lang',lang);}}catch(e){{}}
}}
document.querySelectorAll('.lang-btn').forEach(function(btn){{
  btn.addEventListener('click',function(){{setLang(btn.dataset.lang);}});
}});
(function(){{try{{var s=localStorage.getItem('lang');if(s&&s!=='es')setLang(s);}}catch(e){{}}}}());
/* ── Scroll progress + nav title ── */
(function(){{
  const bar=document.getElementById('progress');
  const navTitle=document.getElementById('nav-title');
  const hero=document.querySelector('.article-hero');
  window.addEventListener('scroll',function(){{
    const d=document.documentElement;
    const s=d.scrollTop||document.body.scrollTop;
    const h=d.scrollHeight-d.clientHeight;
    if(h>0) bar.style.width=(s/h*100)+'%';
    if(hero) navTitle.classList.toggle('visible', s > hero.offsetHeight * .6);
  }},{{passive:true}});
  const tocLinks=document.querySelectorAll('.toc-link');
  if(tocLinks.length){{
    const obs=new IntersectionObserver(function(entries){{
      entries.forEach(function(e){{
        if(e.isIntersecting){{
          tocLinks.forEach(function(l){{l.classList.remove('active')}});
          const a=document.querySelector('.toc-link[href="#'+e.target.id+'"]');
          if(a)a.classList.add('active');
        }}
      }});
    }},{{rootMargin:'-5% 0px -80% 0px'}});
    document.querySelectorAll('.article-wrap h2[id],.article-wrap h3[id]').forEach(function(h){{obs.observe(h)}});
  }}
}})();
</script>
{footer_html}
<script defer src="{KATEX_JS}" integrity="{KATEX_JS_SRI}" crossorigin="anonymous"></script>
<script defer src="{KATEX_AR}" integrity="{KATEX_AR_SRI}" crossorigin="anonymous" onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}]}})"></script>
</body>
</html>"""


# ── Página de presentación de serie ───────────────────────────────────────

def _series_landing_template(series_slug, all_metas, has_content_set):
    m0       = all_metas[0]
    title_es = _e(m0.get("series_es", series_slug))
    title_en = _e(m0.get("series_en", m0.get("series_es", series_slug)))
    desc_es  = _e(m0.get("series_desc_es", ""))
    desc_en  = _e(m0.get("series_desc_en", desc_es))
    n        = len(all_metas)
    badge_es = f"Serie &nbsp;·&nbsp; {n} capítulo{'s' if n != 1 else ''}"
    badge_en = f"Series &nbsp;·&nbsp; {n} chapter{'s' if n != 1 else ''}"

    excerpt_html = (
        f'<p class="hero-excerpt" data-es="{desc_es}" data-en="{desc_en}">{desc_es}</p>'
        if desc_es else ''
    )

    # Párrafos de introducción (separados por ||)
    raw_about_es = m0.get("series_about_es", "")
    raw_about_en = m0.get("series_about_en", raw_about_es)
    about_es_parts = [_e(p.strip()) for p in raw_about_es.split("||") if p.strip()]
    about_en_parts = [_e(p.strip()) for p in raw_about_en.split("||") if p.strip()]
    about_html = ""
    for i, para_es in enumerate(about_es_parts):
        para_en = about_en_parts[i] if i < len(about_en_parts) else para_es
        about_html += f'<p class="sl-about-p" data-es="{para_es}" data-en="{para_en}">{para_es}</p>\n'
    about_section = f'<div class="sl-about">{about_html}</div>' if about_html else ""

    chapters_html = ""
    for meta in all_metas:
        slug = meta.get("slug", "")
        num  = str(meta.get("chapter", 0)).zfill(2)
        t_es = _e(meta.get("title_es", ""))
        t_en = _e(meta.get("title_en", meta.get("title_es", "")))
        d_es = _e(meta.get("date_es", ""))
        d_en = _e(meta.get("date_en", d_es))
        live = slug in has_content_set
        if live:
            chapters_html += (
                f'<a href="{slug}.html" class="sl-ch">'
                f'<span class="sl-num">{num}</span>'
                f'<div class="sl-info">'
                f'<span class="sl-title" data-es="{t_es}" data-en="{t_en}">{t_es}</span>'
                f'<span class="sl-date" data-es="{d_es}" data-en="{d_en}">{d_es}</span>'
                f'</div>'
                f'<span class="sl-arrow">→</span>'
                f'</a>'
            )
        else:
            chapters_html += (
                f'<div class="sl-ch sl-ch--soon">'
                f'<span class="sl-num">{num}</span>'
                f'<div class="sl-info">'
                f'<span class="sl-title" data-es="{t_es}" data-en="{t_en}">{t_es}</span>'
                f'<span class="sl-soon" data-es="Próximamente" data-en="Coming soon">Próximamente</span>'
                f'</div>'
                f'</div>'
            )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_es} — Serie</title>
<meta name="description" content="{desc_es}">
<meta property="og:title" content="{title_es}">
<meta property="og:description" content="{desc_es}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}/blog/{series_slug}.html">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth;font-size:18px}}
:root{{--bg:#fafaf8;--ink:#0d0d0d;--mid:#555;--soft:#888;--faint:#bbb;--rule:#e8e8e5}}
body{{background:var(--bg);color:var(--ink);font-family:'Space Mono',monospace;overflow-x:hidden;line-height:1.8}}
body>nav{{position:sticky;top:0;z-index:200;background:rgba(250,250,248,.97);backdrop-filter:blur(14px);border-bottom:1px solid var(--rule);padding:.85rem 5vw;display:flex;align-items:center;justify-content:space-between;gap:1.2rem}}
.nav-back{{display:inline-flex;align-items:center;gap:.5rem;font-size:.55rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--ink);text-decoration:none;border:1px solid rgba(0,0,0,.18);padding:.5rem 1.1rem;transition:all .2s;white-space:nowrap;font-weight:700}}
.nav-back:hover{{border-color:var(--ink);background:rgba(0,0,0,.04)}}
.nav-end{{display:flex;align-items:center}}
.lang-toggle{{display:flex;gap:.2rem}}
.lang-btn{{font-family:'Space Mono',monospace;font-size:.44rem;letter-spacing:2px;text-transform:uppercase;padding:.32rem .6rem;background:none;border:1px solid var(--rule);color:var(--soft);cursor:pointer;transition:all .18s}}
.lang-btn.active{{border-color:var(--ink);color:var(--ink);font-weight:700}}
.lang-btn:hover{{border-color:var(--soft);color:var(--ink)}}
.article-hero{{padding:5.5rem 4vw 4rem;border-bottom:1px solid var(--rule)}}
.hero-meta{{margin-bottom:1rem}}
.hero-date{{font-size:.65rem;letter-spacing:3px;text-transform:uppercase;color:var(--mid)}}
.article-hero h1{{font-family:'DM Serif Display',serif;font-size:clamp(2.5rem,6vw,5.5rem);letter-spacing:-.025em;line-height:1.06;color:var(--ink);margin-bottom:1.2rem;max-width:900px}}
.hero-excerpt{{font-family:'DM Serif Display',serif;font-style:italic;font-size:1.3rem;line-height:1.65;color:#2a2a2a;max-width:820px}}
.sl-outer{{max-width:1100px;margin:0 auto;padding:4rem 4vw 8rem}}
.sl-list{{display:flex;flex-direction:column}}
.sl-ch{{display:flex;align-items:center;gap:1.5rem;padding:1.4rem 1rem;border-bottom:1px solid var(--rule);text-decoration:none;color:inherit;transition:background .15s;border-radius:4px;margin:0 -1rem}}
.sl-ch:last-child{{border-bottom:none}}
.sl-ch:not(.sl-ch--soon):hover{{background:rgba(0,0,0,.03)}}
.sl-ch--soon{{opacity:.4;cursor:default}}
.sl-num{{font-family:'Bebas Neue',sans-serif;font-size:2.8rem;color:var(--faint);min-width:3.2rem;line-height:1;flex-shrink:0;transition:color .15s}}
.sl-ch:not(.sl-ch--soon):hover .sl-num{{color:var(--ink)}}
.sl-info{{flex:1;display:flex;flex-direction:column;gap:.3rem;min-width:0}}
.sl-title{{font-family:'DM Serif Display',serif;font-size:1.15rem;color:var(--ink);line-height:1.3}}
.sl-date,.sl-soon{{font-size:.58rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--soft)}}
.sl-soon{{color:var(--faint)}}
.sl-arrow{{font-size:1.1rem;color:var(--faint);transition:color .15s;flex-shrink:0}}
.sl-ch:not(.sl-ch--soon):hover .sl-arrow{{color:var(--ink)}}
.sl-about{{margin-bottom:3rem;padding-bottom:3rem;border-bottom:1px solid var(--rule)}}
.sl-about-p{{font-family:'DM Serif Display',serif;font-style:italic;font-size:1.1rem;line-height:1.75;color:#3a3a3a;margin-bottom:1.1rem}}
.sl-about-p:last-child{{margin-bottom:0}}
.af-back{{display:inline-flex;align-items:center;gap:.5rem;font-size:.44rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--soft);text-decoration:none;border:1px solid var(--rule);padding:.55rem 1.2rem;transition:all .2s;margin-top:3rem}}
.af-back:hover{{color:var(--ink);border-color:var(--ink);background:rgba(0,0,0,.02)}}
@media(max-width:700px){{nav{{padding:.8rem 1.4rem}}.article-hero{{padding:3.5rem 1.4rem 3rem}}.sl-outer{{padding:3rem 1.4rem 5rem}}}}
@media(max-width:420px){{html{{font-size:16px}}.article-hero{{padding:2.5rem 1.2rem 2.5rem}}}}
</style>
</head>
<body>
<nav>
  <a href="../index.html#blog" class="nav-back" data-es="← Blog" data-en="← Blog">← Blog</a>
  <div class="nav-end">
    <div class="lang-toggle">
      <button class="lang-btn active" data-lang="es">ES</button>
      <button class="lang-btn" data-lang="en">EN</button>
    </div>
  </div>
</nav>
<div class="article-hero">
  <div class="hero-meta"><span class="hero-date" data-es="{badge_es}" data-en="{badge_en}">{badge_es}</span></div>
  <h1 data-es="{title_es}" data-en="{title_en}">{title_es}</h1>
  {excerpt_html}
</div>
<div class="sl-outer">
  {about_section}
  <div class="sl-list">{chapters_html}
  </div>
  <a href="../index.html#blog" class="af-back" data-es="← Volver al blog" data-en="← Back to blog">← Volver al blog</a>
</div>
<script>
function setLang(lang){{
  document.documentElement.lang=lang;
  document.querySelectorAll('.lang-btn').forEach(function(b){{b.classList.toggle('active',b.dataset.lang===lang);}});
  document.querySelectorAll('[data-es]').forEach(function(el){{
    var txt=el.getAttribute('data-'+lang);
    if(txt!==null)el.innerHTML=txt;
  }});
  try{{localStorage.setItem('lang',lang);}}catch(e){{}}
}}
document.querySelectorAll('.lang-btn').forEach(function(btn){{
  btn.addEventListener('click',function(){{setLang(btn.dataset.lang);}});
}});
(function(){{try{{var s=localStorage.getItem('lang');if(s&&s!=='es')setLang(s);}}catch(e){{}}}}());
</script>
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
    has_content_set = set()
    entries = []
    for _, meta, content in post_data:
        slug = meta["slug"]
        output_path = Path("blog") / f"{slug}.html"

        if content:
            has_content_set.add(slug)
            parts = re.split(r'\n<!--\s*EN\s*-->\n', content, maxsplit=1)
            content_es = parts[0].strip()
            content_en = parts[1].strip() if len(parts) > 1 else ""

            body_html = _md_to_html(content_es)
            body_html, toc_html = _build_toc(body_html, meta.get("read_time", ""), lang="es")

            body_html_en = toc_html_en = ""
            if content_en:
                body_html_en = _md_to_html(content_en)
                body_html_en, toc_html_en = _build_toc(body_html_en, meta.get("read_time", ""), id_prefix="en-", lang="en")
        else:
            body_html = '<p class="stub-msg" data-es="Próximamente" data-en="Coming soon">Próximamente</p>'
            body_html_en = toc_html = toc_html_en = ""

        s = meta.get("series")
        series_nav = _series_nav_html(slug, series_map[s]) if s else ""
        s_chapters = series_map.get(s) if s else None
        output_path.write_text(
            _blog_template(meta, body_html, series_nav, toc_html, s_chapters, body_html_en, toc_html_en),
            encoding="utf-8",
        )
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

    # Generar páginas de presentación para cada serie
    for s, chapters in series_map.items():
        landing_path = Path("blog") / f"{s}.html"
        landing_path.write_text(
            _series_landing_template(s, chapters, has_content_set),
            encoding="utf-8",
        )
        print(f"   📚 Serie:    blog/{s}.html")

    return entries
