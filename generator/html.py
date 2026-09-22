from . import content as C
from .icons import ICON_GITHUB, ICON_LINKEDIN, ICON_KAGGLE, ICON_EMAIL, ICON_LOCATION
from .badges import badge_style


def build_hero():
    return f"""
<div class="lang-toggle">
  <button class="lang-btn active" data-lang="es">ES</button>
  <button class="lang-btn" data-lang="en">EN</button>
</div>

<section id="hero">
  <canvas id="c-conway"></canvas>
  <div class="hero-inner">
    <div class="hero-name" style="letter-spacing:-2px;">{C.NOMBRE}</div>
  </div>
</section>"""


def build_tab_bar():
    tabs = [
        ("about",    "Sobre mí",  "About"),
        ("projects", "Proyectos", "Projects"),
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


def _proj_card_light(p, show_img=False):
    name_es = p["title"] if p.get("featured") else p.get("title_es", p.get("title", ""))
    name_en = p["title"] if p.get("featured") else p.get("title_en", name_es)
    desc_es = p.get("body_es", p.get("desc_es", ""))
    desc_en = p.get("body_en", p.get("desc_en", ""))
    tags = "".join(f'<span class="proj-c-tag" style="{badge_style(b)}">{b}</span>' for b in p["badges"])
    cls = "proj-card" + (" proj-card--featured" if p.get("featured") else "")
    cta_es = "Ver repositorio ↗"
    cta_en = "View repository ↗"
    img_html = f'<div class="proj-c-img"><img src="{p["img"]}" alt="{name_es}" loading="lazy"></div>' if (show_img and p.get("img")) else ""
    return f"""
          <a href="{p['url']}" target="_blank" rel="noopener noreferrer" class="{cls}">
            {img_html}
            <div class="proj-c-name" data-es="{name_es}" data-en="{name_en}">{name_es}</div>
            <div class="proj-c-desc" data-es="{desc_es}" data-en="{desc_en}">{desc_es}</div>
            <div class="proj-c-tags">{tags}</div>
            <div class="proj-c-cta" data-es="{cta_es}" data-en="{cta_en}">{cta_es}</div>
          </a>"""


def _about_proj_mini(p, idx):
    return _proj_card_light(p, show_img=True)


def build_panel_about():
    proj_minis = "".join(_about_proj_mini(p, i + 1) for i, p in enumerate(C.PROYECTOS[:2]))

    return f"""
  <div class="tab-panel active" id="panel-about" role="tabpanel">
    <canvas id="c-delaunay" aria-hidden="true"></canvas>
    <div class="panel-content light-panel">
      <div class="sec-title" data-es="SOBRE MÍ" data-en="ABOUT ME">SOBRE MÍ</div>
      <div class="about-layout">

        <div>
          <div class="about-sub-label" data-es="Quién soy" data-en="Who I am">Quién soy</div>
          {_bio_paragraphs()}
        </div>

        <figure class="bio-talk">
          <img src="static/epam-talk.jpg" alt="Jerónimo presentando en Medellín IA" loading="lazy">
          <figcaption data-es="Presentando &ldquo;How to build a transformer from scratch&rdquo; en Medellín IA community · EPAM Medellín" data-en="Presenting &ldquo;How to build a transformer from scratch&rdquo; at Medellín IA community · EPAM Medellín">Presentando &ldquo;How to build a transformer from scratch&rdquo; en Medellín IA community · EPAM Medellín</figcaption>
        </figure>

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

      </div>
    </div>
  </div>"""


def _proj_names(p):
    name_es = p["title"] if p.get("featured") else p.get("title_es", p.get("title", ""))
    name_en = p["title"] if p.get("featured") else p.get("title_en", name_es)
    return name_es, name_en


def _proj_kicker(p, lead=False):
    lang = p.get("lang", "")
    if lead:
        es = "Proyecto destacado" + (f" · {lang}" if lang else "")
        en = "Featured project" + (f" · {lang}" if lang else "")
    else:
        es = lang or "Proyecto"
        en = lang or "Project"
    return f'<div class="proj-kicker" data-es="{es}" data-en="{en}">{es}</div>'


def _proj_tags(p):
    tags = "".join(f'<span class="proj-tag" style="{badge_style(b)}">{b}</span>' for b in p["badges"])
    return f'<div class="proj-tags">{tags}</div>'


def _proj_lead(p):
    name_es, name_en = _proj_names(p)
    deck_es = p.get("body_es", p.get("desc_es", ""))
    deck_en = p.get("body_en", p.get("desc_en", ""))
    img_html = (f'<a href="{p["url"]}" target="_blank" rel="noopener noreferrer" '
                f'class="proj-lead-media"><img src="{p["img"]}" alt="{name_es}" loading="lazy"></a>'
                if p.get("img") else "")
    cta_es, cta_en = "Ver repositorio ↗", "View repository ↗"
    return f"""
        <article class="proj-lead">
          {img_html}
          <div class="proj-lead-body">
            <div class="proj-lead-badge" data-es="★ Destacado" data-en="★ Featured">★ Destacado</div>
            <a href="{p['url']}" target="_blank" rel="noopener noreferrer" class="proj-lead-title" data-es="{name_es}" data-en="{name_en}">{name_es}</a>
            <p class="proj-lead-deck" data-es="{deck_es}" data-en="{deck_en}">{deck_es}</p>
            {_proj_tags(p)}
            <a href="{p['url']}" target="_blank" rel="noopener noreferrer" class="proj-readmore" data-es="{cta_es}" data-en="{cta_en}">{cta_es}</a>
          </div>
        </article>"""


def _proj_post(p):
    name_es, name_en = _proj_names(p)
    desc_es = p.get("desc_es", p.get("body_es", ""))
    desc_en = p.get("desc_en", p.get("body_en", ""))
    img_html = (f'<div class="proj-post-media"><img src="{p["img"]}" alt="{name_es}" loading="lazy"></div>'
                if p.get("img") else "")
    cta_es, cta_en = "Ver repositorio ↗", "View repository ↗"
    return f"""
          <a href="{p['url']}" target="_blank" rel="noopener noreferrer" class="proj-post">
            {img_html}
            <div class="proj-post-body">
              <div class="proj-post-title" data-es="{name_es}" data-en="{name_en}">{name_es}</div>
              <p class="proj-post-excerpt" data-es="{desc_es}" data-en="{desc_en}">{desc_es}</p>
              <div class="proj-post-foot">
                {_proj_tags(p)}
              </div>
              <span class="proj-readmore proj-post-cta" data-es="{cta_es}" data-en="{cta_en}">{cta_es}</span>
            </div>
          </a>"""


def build_panel_projects():
    lead = next((p for p in C.PROYECTOS if p.get("featured")), None)
    rest = [p for p in C.PROYECTOS if p is not lead]
    lead_html = _proj_lead(lead) if lead else ""
    feed_html = "".join(_proj_post(p) for p in rest)
    masthead_es = "Más proyectos"
    masthead_en = "More projects"
    return f"""
  <div class="tab-panel" id="panel-projects" role="tabpanel">
    <canvas id="c-lorenz" aria-hidden="true"></canvas>
    <div class="panel-content light-panel">
      <div class="sec-title" data-es="PROYECTOS" data-en="PROJECTS">PROYECTOS</div>
      <div class="sec-sub" data-es="{C.PROYECTOS_SUB_ES}" data-en="{C.PROYECTOS_SUB_EN}">{C.PROYECTOS_SUB_ES}</div>
      <div class="proj-paper">
        {lead_html}
        <div class="proj-feed-head">
          <span class="proj-feed-label" data-es="{masthead_es}" data-en="{masthead_en}">{masthead_es}</span>
          <span class="proj-feed-rule"></span>
        </div>
        <div class="proj-feed">{feed_html}
        </div>
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
          <img src="{url}" alt="{pieza['titulo_es']}" loading="lazy"{dims} data-full="{url}" class="lb-trigger">
        </div>
      </div>"""


def build_panel_arte():
    pieces = [_arte_piece(p) for p in C.ARTE]
    grid_content = "".join(pieces).strip()
    if not grid_content:
        grid_content = '<div class="arte-empty" data-es="Próximamente" data-en="Coming soon">Próximamente</div>'

    return f"""
  <div class="tab-panel" id="panel-arte" role="tabpanel">
    <canvas id="c-dp" aria-hidden="true"></canvas>
    <div class="panel-content light-panel">
      <div class="sec-title" data-es="ARTE" data-en="ART">ARTE</div>
      <div class="sec-sub" data-es="{C.ARTE_SUB_ES}" data-en="{C.ARTE_SUB_EN}">{C.ARTE_SUB_ES}</div>
      <div class="arte-grid">{grid_content}
      </div>
    </div>
  </div>
  <div id="lightbox" role="dialog" aria-modal="true" aria-label="Imagen ampliada">
    <button id="lb-close" aria-label="Cerrar">&#x2715;</button>
    <img id="lb-img" src="" alt="">
  </div>"""


def build_panel_contact():
    return f"""
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
</div>"""


def build_footer():
    return f"""
<footer>
  <span>© {C.AÑO} {C.NOMBRE.replace('<br>', ' ')}</span>
  <span>{C.CIUDAD}, {C.PAIS}</span>
</footer>"""
