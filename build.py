#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║  Edita content.py y luego corre:  python build.py               ║
# ╚══════════════════════════════════════════════════════════════════╝

import content as C
from pathlib import Path
from src.css          import build_css
from src.html         import (
    build_hero, build_tab_bar,
    build_panel_about, build_panel_projects,
    build_panel_blog, build_panel_arte,
    build_panel_contact, build_footer,
)
from src.js           import build_js
from src.blog_builder import build_blog_pages

FONTS    = "https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Bebas+Neue&family=DM+Serif+Display:ital@0;1&display=swap"
SITE_URL = "https://jerohoyos.github.io"
NOMBRE   = C.NOMBRE.replace("<br>", " ")


def build():
    blog_items = build_blog_pages()

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{NOMBRE}</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🐈‍⬛</text></svg>">
<meta name="description" content="{C.TITULO} en {C.CIUDAD}. {C.BIO_EN[0].replace(chr(34), '&quot;')}">
<meta property="og:title" content="{NOMBRE} — {C.TITULO}">
<meta property="og:description" content="{C.TITULO} en {C.CIUDAD}. Estudiante de Ingeniería en Sistemas, Universidad Nacional de Colombia.">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}/">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link href="{FONTS}" rel="stylesheet">
{build_css()}
</head>
<body>
{build_hero()}
{build_tab_bar()}
{build_panel_about(blog_items)}
{build_panel_projects()}
{build_panel_blog(blog_items)}
{build_panel_arte()}
{build_panel_contact()}
{build_footer()}
{build_js()}
<script src="oneko.js"></script>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # robots.txt
    Path("robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )

    # sitemap.xml
    urls = [{"loc": f"{SITE_URL}/", "priority": "1.0"}]
    for item in blog_items:
        urls.append({"loc": f"{SITE_URL}/{item['url']}", "priority": "0.7"})
    xml_urls = "\n".join(
        f'  <url><loc>{u["loc"]}</loc><priority>{u["priority"]}</priority></url>'
        for u in urls
    )
    Path("sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{xml_urls}\n'
        f'</urlset>\n',
        encoding="utf-8",
    )

    print("✅  index.html generado correctamente.")
    print(f"   Nombre   : {NOMBRE}")
    print(f"   Email    : {C.EMAIL}")
    print(f"   GitHub   : {C.GITHUB}")
    print(f"   Proyectos: {len(C.PROYECTOS)}")
    print(f"   Blog     : {len(blog_items)} artículo(s)")
    print(f"   Arte     : {len(C.ARTE)} pieza(s)")
    print("   robots.txt y sitemap.xml generados.")


if __name__ == "__main__":
    build()
