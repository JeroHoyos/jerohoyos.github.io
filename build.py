#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║  Edita content.py y luego corre:  python build.py               ║
# ╚══════════════════════════════════════════════════════════════════╝

import re
import content as C
from pathlib import Path

def _strip_html(s):
    return re.sub(r'<[^>]+>', '', s)
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
OG_IMAGE = f"{SITE_URL}/og.png"


def _build_favicon():
    """Generate favicon.ico (16/32/48px) as a dark-background 'J' monogram."""
    try:
        from PIL import Image, ImageDraw, ImageFont

        def _font(path, size):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                return None

        # Draw at 96px then downscale — gives clean results at all sizes
        SZ = 96
        img = Image.new("RGBA", (SZ, SZ), (5, 5, 5, 255))
        draw = ImageDraw.Draw(img)
        f = (
            _font(r"C:\Windows\Fonts\georgiab.ttf", 64) or
            _font(r"C:\Windows\Fonts\arialbd.ttf",  64) or
            ImageFont.load_default()
        )
        text = "J"
        bbox = draw.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((SZ - tw) // 2 - bbox[0], (SZ - th) // 2 - bbox[1]),
                  text, font=f, fill=(244, 244, 239, 255))

        # Save ICO with multiple sizes (Pillow resizes from the base image)
        img.save("favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
        return True
    except Exception as e:
        print(f"   ⚠️  favicon.ico no generado: {e}")
        return False


def _build_og_image():
    """Generate og.png (1200×630) for Open Graph social sharing."""
    try:
        from PIL import Image, ImageDraw, ImageFont

        W, H = 1200, 630
        BG    = (5, 5, 5)
        WHITE = (244, 244, 239)
        GRAY  = (90, 90, 90)
        MID   = (55, 55, 55)

        img  = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(img)

        # Left accent strip
        draw.rectangle([0, 0, 7, H], fill=WHITE)

        def _font(path, size):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                return None

        name_font = (
            _font(r"C:\Windows\Fonts\impact.ttf", 128) or
            _font(r"C:\Windows\Fonts\georgiab.ttf", 110) or
            ImageFont.load_default()
        )
        sub_font = (
            _font(r"C:\Windows\Fonts\georgiai.ttf", 42) or
            _font(r"C:\Windows\Fonts\georgia.ttf",  42) or
            ImageFont.load_default()
        )
        url_font = (
            _font(r"C:\Windows\Fonts\lucon.ttf", 24) or
            _font(r"C:\Windows\Fonts\cour.ttf",  24) or
            ImageFont.load_default()
        )

        PAD = 90
        name_parts = NOMBRE.upper().split(" ", 1)   # ["JERÓNIMO", "HOYOS BOTERO"]
        draw.text((PAD, 155), name_parts[0], font=name_font, fill=WHITE)
        draw.text((PAD, 290), name_parts[1] if len(name_parts) > 1 else "", font=name_font, fill=WHITE)

        draw.text((PAD, 456), C.TITULO, font=sub_font, fill=GRAY)

        # Thin rule
        draw.rectangle([PAD, 540, W - PAD, 541], fill=MID)

        draw.text((PAD, 556), "jerohoyos.github.io", font=url_font, fill=GRAY)

        img.save("og.png", "PNG", optimize=True)
        return True
    except Exception as e:
        print(f"   ⚠️  og.png no generado: {e}")
        return False


def _build_404():
    """Generate 404.html matching the site's dark hero aesthetic."""
    nombre_clean = NOMBRE
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>404 — {nombre_clean}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{height:100%}}
body{{background:#050505;color:#f4f4ef;font-family:'Space Mono',monospace;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:2rem;min-height:100vh}}
.num{{font-family:'Bebas Neue',sans-serif;font-size:clamp(8rem,22vw,18rem);line-height:.85;color:#f4f4ef;letter-spacing:-4px;opacity:.12}}
.msg{{font-family:'DM Serif Display',serif;font-style:italic;font-size:clamp(1.1rem,3vw,1.6rem);color:#666;margin-top:2rem;margin-bottom:3rem}}
.back{{display:inline-flex;align-items:center;gap:.5rem;font-size:.48rem;letter-spacing:3px;text-transform:uppercase;color:#999;text-decoration:none;border:1px solid #333;padding:.7rem 1.6rem;transition:all .25s}}
.back:hover{{color:#f4f4ef;border-color:#666}}
</style>
</head>
<body>
<div class="num">404</div>
<p class="msg">Esta página no existe (o fue movida).</p>
<a href="/" class="back">← Volver al inicio</a>
</body>
</html>"""
    Path("404.html").write_text(html, encoding="utf-8")


def build():
    blog_items = build_blog_pages()

    _build_favicon()
    _build_og_image()
    _build_404()

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
    series_seen = set()
    for item in blog_items:
        s = item.get("series")
        if s and s not in series_seen:
            series_seen.add(s)
            urls.append({"loc": f"{SITE_URL}/blog/{s}.html", "priority": "0.8"})
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
    print("   robots.txt, sitemap.xml, og.png, favicon.ico y 404.html generados.")


if __name__ == "__main__":
    build()
