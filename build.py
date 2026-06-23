#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║  Edita generator/content.py y luego corre:  python build.py     ║
# ╚══════════════════════════════════════════════════════════════════╝

import re
from pathlib import Path

import generator.content as C
from generator.css    import build_css
from generator.html   import (
    build_hero, build_tab_bar,
    build_panel_about, build_panel_projects,
    build_panel_arte, build_panel_contact, build_footer,
)
from generator.images import build_favicon, build_og_image
from generator.js     import build_js
from generator.seo    import build_404, build_robots_txt, build_sitemap

FONTS    = ("https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400"
            "&family=Bebas+Neue&family=DM+Serif+Display:ital@0;1&family=Rye&family=Special+Elite"
            "&family=Nosifer&family=EB+Garamond:ital,wght@0,500;1,500&family=Caveat:wght@600;700"
            "&display=swap")
SITE_URL = "https://jerohoyos.github.io"
NOMBRE   = C.NOMBRE.replace("<br>", " ")
OG_IMAGE = f"{SITE_URL}/og.png"

_strip_html = lambda s: re.sub(r'<[^>]+>', '', s)


def build() -> None:
    build_favicon()
    build_og_image(NOMBRE, C.TITULO, SITE_URL)
    build_404(NOMBRE, FONTS)
    build_robots_txt(SITE_URL)
    build_sitemap(SITE_URL, [{"loc": f"{SITE_URL}/", "priority": "1.0"}])

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{NOMBRE}</title>
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🐈‍⬛</text></svg>" type="image/svg+xml">
<meta name="description" content="{C.TITULO} en {C.CIUDAD}. {_strip_html(C.BIO_EN[0]).replace(chr(34), '&quot;')}">
<meta property="og:title" content="{NOMBRE} — {C.TITULO}">
<meta property="og:description" content="{C.TITULO} en {C.CIUDAD}. Estudiante de Ingeniería en Sistemas, Universidad Nacional de Colombia.">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link href="{FONTS}" rel="stylesheet">
{build_css()}
</head>
<body>
{build_hero()}
{build_tab_bar()}
{build_panel_about()}
{build_panel_projects()}
{build_panel_arte()}
{build_panel_contact()}
{build_footer()}
{build_js()}
<script src="static/oneko.js" data-cat="static/oneko.gif"></script>
</body>
</html>"""

    Path("docs/index.html").write_text(html, encoding="utf-8")

    print("✅  docs/index.html generado correctamente.")
    print(f"   Nombre   : {NOMBRE}")
    print(f"   Email    : {C.EMAIL}")
    print(f"   GitHub   : {C.GITHUB}")
    print(f"   Proyectos: {len(C.PROYECTOS)}")
    print(f"   Arte     : {len(C.ARTE)} pieza(s)")
    print("   docs/robots.txt, sitemap.xml, og.png, favicon.ico y 404.html generados.")


if __name__ == "__main__":
    build()
