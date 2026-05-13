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
          <button onclick="document.querySelector('[data-tab=contact]').click()" class="apm-ver-mas"><span data-es="Ver formulario completo →" data-en="See full contact form →">Ver formulario completo →</span></button>
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
    rows = ""
    for i, a in enumerate(items):
        tags = "".join(f'<span class="br-tag">{t}</span>' for t in a["tags"])
        num = str(i + 1).zfill(2)
        rows += f"""
        <a href="{a['url']}" class="blog-row">
          <div class="br-left">
            <div class="br-num">{num}</div>
            <div class="br-date" data-es="{a['date_es']}" data-en="{a['date_en']}">{a['date_es']}</div>
          </div>
          <div class="br-right">
            <div class="br-tags">{tags}</div>
            <div class="br-title" data-es="{a['title_es']}" data-en="{a['title_en']}">{a['title_es']}</div>
            <div class="br-excerpt" data-es="{a['excerpt_es']}" data-en="{a['excerpt_en']}">{a['excerpt_es']}</div>
            <div class="br-read" data-es="{a['read_es']}" data-en="{a['read_en']}">{a['read_es']}</div>
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
    return f"""
      <div class="arte-piece">
        <div class="arte-img-wrap">
          <img src="{pieza["url"]}" alt="{pieza["titulo_es"]}" loading="lazy">
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
      <div class="ct-form-wrap">
        <form id="contact-form" class="cf-wrap" novalidate>
          <label class="cf-label">
            <span data-es="Nombre" data-en="Name">Nombre</span>
            <input type="text" name="name" required>
          </label>
          <label class="cf-label">
            <span data-es="Correo Electrónico" data-en="Email">Correo Electrónico</span>
            <input type="email" name="email" required>
          </label>
          <label class="cf-label">
            <span data-es="Asunto" data-en="Subject">Asunto</span>
            <input type="text" name="subject" required>
          </label>
          <label class="cf-label">
            <span data-es="Mensaje" data-en="Message">Mensaje</span>
            <textarea name="message" rows="5" required></textarea>
          </label>
          <button type="submit" class="cf-btn" data-es="Enviar Mensaje" data-en="Send Message">Enviar Mensaje</button>
        </form>
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
