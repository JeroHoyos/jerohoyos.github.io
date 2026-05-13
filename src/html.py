import content as C
from src.icons import ICON_GITHUB, ICON_LINKEDIN, ICON_KAGGLE, ICON_EMAIL, ICON_LOCATION
from src.badges import badge_style


def build_hero():
    return f"""
<!-- LANGUAGE TOGGLE -->
<div class="lang-toggle">
  <button class="lang-btn active" data-lang="es">ES</button>
  <button class="lang-btn" data-lang="en">EN</button>
</div>

<!-- HERO -->
<section id="hero">
  <canvas id="c-conway"></canvas>
  <div class="hero-inner">
    <div class="hero-name" style="letter-spacing:-2px;">{C.NOMBRE}</div>
    <div class="hero-sub" data-es="{C.TITULO}" data-en="{C.TITULO_EN}">{C.TITULO}</div>
  </div>
  <div class="hero-bottom">
    <div class="hero-socials">
      <a href="{C.GITHUB}" target="_blank" rel="noopener noreferrer">
        {ICON_GITHUB}<span>GitHub</span>
      </a>
      <a href="{C.LINKEDIN}" target="_blank" rel="noopener noreferrer">
        {ICON_LINKEDIN}<span>LinkedIn</span>
      </a>
      <a href="{C.KAGGLE}" target="_blank" rel="noopener noreferrer">
        {ICON_KAGGLE}<span>Kaggle</span>
      </a>
    </div>
  </div>
</section>"""


def build_tab_bar():
    tabs = [
        ("about",    "Sobre mí",  "About"),
        ("projects", "Proyectos", "Projects"),
        ("blog",     "Blog",      "Blog"),
        ("arte",     "Arte",      "Art"),
        ("contact",  "Contacto",  "Contact"),
    ]
    buttons = ""
    for i, (tid, es, en) in enumerate(tabs):
        active = ' active' if i == 0 else ''
        buttons += f'\n    <button class="tab-btn{active}" data-tab="{tid}" data-es="{es}" data-en="{en}">{es}</button>'
    return f"""
<div id="shell">
  <nav id="tab-bar" role="tablist">{buttons}
  </nav>"""


def _bio_paragraphs():
    es_html = "".join(f"<p>{p}</p>" for p in C.BIO_ES)
    en_html = "".join(f"<p>{p}</p>" for p in C.BIO_EN)
    return f'<div class="about-bio" data-es="{es_html.replace(chr(34), "&quot;")}" data-en="{en_html.replace(chr(34), "&quot;")}">{es_html}</div>'


def _stack():
    tiers = ""
    for tier in C.STACK:
        chips = "".join(f'<span class="chip {tier["chip_class"]}">{item}</span>' for item in tier["items"])
        tiers += f"""
      <div class="stack-tier">
        <div class="stack-tier-label" data-es="{tier['label_es']}" data-en="{tier['label_en']}">{tier['label_es']} <span></span></div>
        <div class="stack-chips">{chips}</div>
      </div>"""
    return tiers


def _education():
    items = ""
    for edu in C.EDUCACION:
        items += f"""
      <div class="edu-item">
        <div class="edu-year" data-es="{edu['year_es']}" data-en="{edu['year_en']}">{edu['year_es']}</div>
        <div class="edu-name" data-es="{edu['name_es']}" data-en="{edu['name_en']}">{edu['name_es']}</div>
        <div class="edu-inst">{edu['institution']}</div>
      </div>"""
    return items


def _idiomas():
    items = ""
    for lang in C.IDIOMAS:
        items += f"""
      <div class="idioma-item">
        <span class="idioma-name">{lang['name']}</span>
        <span class="idioma-level" data-es="{lang['level_es']}" data-en="{lang['level_en']}">{lang['level_es']}</span>
      </div>"""
    return items


def _proj_card_light(p):
    name_es = p["title"] if p.get("featured") else p.get("title_es", p.get("title", ""))
    name_en = p["title"] if p.get("featured") else p.get("title_en", name_es)
    desc_es = p.get("body_es", p.get("desc_es", ""))
    desc_en = p.get("body_en", p.get("desc_en", ""))
    tags = "".join(f'<span class="proj-c-tag" style="{badge_style(b)}">{b}</span>' for b in p["badges"])
    cls = "proj-card" + (" proj-card--featured" if p.get("featured") else "")
    cta_es = "Ver repositorio ↗"
    cta_en = "View repository ↗"
    return f"""
          <a href="{p['url']}" target="_blank" rel="noopener noreferrer" class="{cls}">
            <div class="proj-c-name" data-es="{name_es}" data-en="{name_en}">{name_es}</div>
            <div class="proj-c-desc" data-es="{desc_es}" data-en="{desc_en}">{desc_es}</div>
            <div class="proj-c-tags">{tags}</div>
            <div class="proj-c-cta" data-es="{cta_es}" data-en="{cta_en}">{cta_es}</div>
          </a>"""


def _about_proj_mini(p, idx):
    return _proj_card_light(p)


def build_panel_about(blog_items=None):
    proj_minis = "".join(_about_proj_mini(p, i + 1) for i, p in enumerate(C.PROYECTOS[:3]))

    return f"""
  <!-- ABOUT -->
  <div class="tab-panel active" id="panel-about" role="tabpanel">
    <canvas id="c-delaunay" aria-hidden="true"></canvas>
    <div class="panel-content light-panel">
      <div class="sec-title" data-es="SOBRE MÍ" data-en="ABOUT ME">SOBRE MÍ</div>
      <div class="about-layout">

        <div>
          <div class="about-sub-label" data-es="Quién soy" data-en="Who I am">Quién soy</div>
          {_bio_paragraphs()}
        </div>

        <div>
          <div class="about-sub-label" data-es="Stack tecnológico" data-en="Tech stack">Stack tecnológico</div>
          {_stack()}
        </div>

        <div class="about-bottom">
          <div>
            <div class="about-sub-label" data-es="Formación" data-en="Education">Formación</div>
            {_education()}
          </div>
          <div>
            <div class="about-sub-label" data-es="Idiomas" data-en="Languages">Idiomas</div>
            {_idiomas()}
          </div>
        </div>

        <div class="about-preview">
          <div class="about-sub-label" data-es="Proyectos" data-en="Projects">Proyectos</div>
          <div class="apm-row">{proj_minis}
          </div>
          <button onclick="document.querySelector('[data-tab=projects]').click()" class="apm-ver-mas"><span data-es="Ver todos los proyectos →" data-en="See all projects →">Ver todos los proyectos →</span></button>
        </div>

        <div class="about-contact">
          <div class="about-sub-label" data-es="Contacto" data-en="Contact">Contacto</div>
          <div class="ac-socials">
            <a href="{C.GITHUB}" target="_blank" rel="noopener noreferrer" class="ac-soc">
              {ICON_GITHUB}<span>GitHub</span>
            </a>
            <a href="{C.LINKEDIN}" target="_blank" rel="noopener noreferrer" class="ac-soc">
              {ICON_LINKEDIN}<span>LinkedIn</span>
            </a>
            <a href="{C.KAGGLE}" target="_blank" rel="noopener noreferrer" class="ac-soc">
              {ICON_KAGGLE}<span>Kaggle</span>
            </a>
            <a href="mailto:{C.EMAIL}" class="ac-soc">
              {ICON_EMAIL}<span>Email</span>
            </a>
          </div>
          <button onclick="document.querySelector('[data-tab=contact]').click()" class="apm-ver-mas"><span data-es="Todos los canales →" data-en="All channels →">Todos los canales →</span></button>
        </div>

      </div>
    </div>
  </div>"""


def _project_card(p, idx):
    return _proj_card_light(p)


def build_panel_projects():
    cards = "".join(_project_card(p, i + 1) for i, p in enumerate(C.PROYECTOS))
    return f"""
  <!-- PROJECTS -->
  <div class="tab-panel" id="panel-projects" role="tabpanel">
    <canvas id="c-flow" aria-hidden="true"></canvas>
    <div class="panel-content light-panel">
      <div class="sec-title" data-es="PROYECTOS" data-en="PROJECTS">PROYECTOS</div>
      <div class="sec-sub" data-es="{C.PROYECTOS_SUB_ES}" data-en="{C.PROYECTOS_SUB_EN}">{C.PROYECTOS_SUB_ES}</div>
      <div class="proj-grid">{cards}
      </div>
    </div>
  </div>"""


def build_panel_blog(blog_items=None):
    items = blog_items if blog_items is not None else C.BLOG

    # Group: standalone entries + series blocks (first chapter of each series wins the slot)
    groups = []
    series_seen = set()
    for entry in items:
        s = entry.get("series")
        if not s:
            groups.append(("standalone", entry))
        elif s not in series_seen:
            series_seen.add(s)
            chapters = sorted(
                [e for e in items if e.get("series") == s],
                key=lambda e: int(e.get("chapter", 0)),
            )
            groups.append(("series", {
                "series_es": chapters[0].get("series_es", s),
                "series_en": chapters[0].get("series_en", s),
                "tags":      chapters[0].get("tags", []),
                "chapters":  chapters,
            }))

    rows = ""
    for i, (kind, data) in enumerate(groups):
        num = str(i + 1).zfill(2)
        if kind == "standalone":
            a = data
            rows += f"""
        <a href="{a['url']}" class="blog-row">
          <span class="br-num">{num}</span>
          <div class="br-body">
            <div class="br-title-row">
              <div class="br-title" data-es="{a['title_es']}" data-en="{a['title_en']}">{a['title_es']}</div>
              <span class="br-arrow" aria-hidden="true">↗</span>
            </div>
            <p class="br-excerpt" data-es="{a['excerpt_es']}" data-en="{a['excerpt_en']}">{a['excerpt_es']}</p>
            <div class="br-meta">
              <span class="br-date" data-es="{a['date_es']}" data-en="{a['date_en']}">{a['date_es']}</span>
              <span class="br-dot">·</span>
              <span class="br-read" data-es="{a['read_es']}" data-en="{a['read_en']}">{a['read_es']}</span>
            </div>
          </div>
        </a>"""
        else:
            d = data
            count_es = f"{len(d['chapters'])} capítulos"
            count_en = f"{len(d['chapters'])} chapters"
            first_url = d["chapters"][0]["url"]
            chs_html = ""
            for ch in d["chapters"]:
                cn = str(ch.get("chapter", 0)).zfill(2)
                chs_html += f"""
              <span class="sb-ch">
                <span class="sb-ch-num">{cn}</span>
                <span class="sb-ch-title" data-es="{ch['title_es']}" data-en="{ch['title_en']}">{ch['title_es']}</span>
                <span class="sb-ch-date" data-es="{ch['date_es']}" data-en="{ch['date_en']}">{ch['date_es']}</span>
              </span>"""
            rows += f"""
        <a href="{first_url}" class="blog-row series-block">
          <span class="br-num">{num}</span>
          <div class="br-body">
            <div class="br-title-row">
              <div class="br-serie-badge" data-es="SERIE" data-en="SERIES">SERIE</div>
              <span class="br-arrow" aria-hidden="true">↗</span>
            </div>
            <div class="br-title" data-es="{d['series_es']}" data-en="{d['series_en']}">{d['series_es']}</div>
            <div class="sb-chapters">{chs_html}
            </div>
            <div class="br-count" data-es="{count_es}" data-en="{count_en}">{count_es}</div>
          </div>
        </a>"""

    return f"""
  <!-- BLOG -->
  <div class="tab-panel" id="panel-blog" role="tabpanel">
    <canvas id="c-scatter" aria-hidden="true"></canvas>
    <div class="panel-content dark-panel">
      <div class="sec-title">BLOG</div>
      <div class="sec-sub" data-es="{C.BLOG_SUB_ES}" data-en="{C.BLOG_SUB_EN}">{C.BLOG_SUB_ES}</div>
      <div class="blog-list">{rows}
      </div>
    </div>
  </div>"""


def _arte_piece(pieza):
    if pieza["tipo"] != "imagen":
        return ""
    url = pieza["url"]
    dims = ""
    try:
        from PIL import Image
        img = Image.open(url)
        w, h = img.size
        img.close()
        dims = f' width="{w}" height="{h}"'
    except Exception:
        pass
    return f"""
      <div class="arte-piece">
        <div class="arte-img-wrap">
          <img src="{url}" alt="{pieza['titulo_es']}" loading="lazy"{dims}>
        </div>
      </div>"""


def build_panel_arte():
    pieces = [_arte_piece(p) for p in C.ARTE]
    grid_content = "".join(pieces).strip()
    if not grid_content:
        grid_content = '<div class="arte-empty" data-es="Próximamente" data-en="Coming soon">Próximamente</div>'

    return f"""
  <!-- ARTE -->
  <div class="tab-panel" id="panel-arte" role="tabpanel">
    <canvas id="c-dp" aria-hidden="true"></canvas>
    <div class="panel-content light-panel">
      <div class="sec-title" data-es="ARTE" data-en="ART">ARTE</div>
      <div class="sec-sub" data-es="{C.ARTE_SUB_ES}" data-en="{C.ARTE_SUB_EN}">{C.ARTE_SUB_ES}</div>
      <div class="arte-grid">{grid_content}
      </div>
    </div>
  </div>"""


def build_panel_contact():
    return f"""
  <!-- CONTACT -->
  <div class="tab-panel" id="panel-contact">
    <canvas id="c-fourier" aria-hidden="true"></canvas>
    <div class="panel-content dark-panel">
      <div class="ct-header">
        <div class="sec-title ct-big" data-es="{C.CONTACTO_TITULO_ES}" data-en="{C.CONTACTO_TITULO_EN}">{C.CONTACTO_TITULO_ES}</div>
        <div class="ct-sub" data-es="{C.CONTACTO_SUB_ES}" data-en="{C.CONTACTO_SUB_EN}">{C.CONTACTO_SUB_ES}</div>
      </div>
      <div class="ct-email-wrap">
        <button class="ct-email-btn" id="ct-email-copy" data-email="{C.EMAIL}">
          <span>{C.EMAIL}</span>
        </button>
        <div class="ct-email-hint" data-es="clic para copiar" data-en="click to copy">clic para copiar</div>
      </div>
      <div class="ct-socials">
        <a href="{C.GITHUB}" target="_blank" rel="noopener noreferrer" class="ct-soc">
          {ICON_GITHUB}<span>GitHub</span>
        </a>
        <a href="{C.LINKEDIN}" target="_blank" rel="noopener noreferrer" class="ct-soc">
          {ICON_LINKEDIN}<span>LinkedIn</span>
        </a>
        <a href="{C.KAGGLE}" target="_blank" rel="noopener noreferrer" class="ct-soc">
          {ICON_KAGGLE}<span>Kaggle</span>
        </a>
        <a href="mailto:{C.EMAIL}" class="ct-soc">
          {ICON_EMAIL}<span>Email</span>
        </a>
      </div>
    </div>
  </div>
</div><!-- /shell -->"""


def build_footer():
    return f"""
<footer>
  <span>© {C.AÑO} {C.NOMBRE.replace('<br>', ' ')}</span>
  <span>{C.CIUDAD}, {C.PAIS}</span>
</footer>"""
