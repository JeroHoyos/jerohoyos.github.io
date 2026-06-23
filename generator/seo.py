"""SEO and auxiliary file generation: 404, robots.txt, sitemap.xml."""

from pathlib import Path


def build_404(site_name: str, fonts_url: str, output: str = "docs/404.html") -> None:
    """Generate a 404 page matching the site's dark-hero aesthetic."""
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>404 — {site_name}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts_url}" rel="stylesheet">
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
    Path(output).write_text(html, encoding="utf-8")


def build_robots_txt(site_url: str, output: str = "docs/robots.txt") -> None:
    """Generate robots.txt allowing all crawlers."""
    Path(output).write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {site_url}/sitemap.xml\n",
        encoding="utf-8",
    )


def build_sitemap(site_url: str, urls: list[dict],
                  output: str = "docs/sitemap.xml") -> None:
    """Generate sitemap.xml from a list of {loc, priority} dicts."""
    entries = "\n".join(
        f'  <url><loc>{u["loc"]}</loc><priority>{u["priority"]}</priority></url>'
        for u in urls
    )
    Path(output).write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{entries}\n'
        '</urlset>\n',
        encoding="utf-8",
    )
