#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║  Edita content.py y luego corre:  python build.py               ║
# ╚══════════════════════════════════════════════════════════════════╝

import content as C
from src.css          import build_css
from src.html         import (
    build_hero, build_tab_bar,
    build_panel_about, build_panel_projects,
    build_panel_blog, build_panel_arte,
    build_panel_contact, build_footer,
)
from src.js           import build_js
from src.blog_builder import build_blog_pages

FONTS = "https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Bebas+Neue&family=DM+Serif+Display:ital@0;1&display=swap"


def build():
    blog_items = build_blog_pages()

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{C.NOMBRE.replace('<br>', ' ')}</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🐈‍⬛</text></svg>">
<meta name="description" content="{C.TITULO} · {C.CIUDAD}, {C.PAIS}">
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

    print("✅  index.html generado correctamente.")
    print(f"   Nombre   : {C.NOMBRE.replace('<br>', ' ')}")
    print(f"   Email    : {C.EMAIL}")
    print(f"   GitHub   : {C.GITHUB}")
    print(f"   Proyectos: {len(C.PROYECTOS)}")
    print(f"   Blog     : {len(blog_items)} artículo(s)")
    print(f"   Arte     : {len(C.ARTE)} pieza(s)")


if __name__ == "__main__":
    build()
