import content as C
from src.icons import ICON_GITHUB, ICON_LINKEDIN, ICON_KAGGLE, ICON_EMAIL


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
    <button class="hero-scroll" id="scroll-cta">Scroll ↓</button>
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
    html = '<div class="stack-section"><div class="stack-header">Stack Tecnológico</div>'
    for tier in C.STACK:
        chips = "".join(f'<span class="chip {tier["chip_class"]}">{item}</span>' for item in tier["items"])
        html += f"""
      <div class="stack-tier">
        <div class="stack-tier-label" data-es="{tier['label_es']}" data-en="{tier['label_en']}" style="color:#333;">{tier['label_es']} <span></span></div>
        <div class="stack-chips">{chips}</div>
      </div>"""
    html += "</div>"
    return html


def _education():
    items = ""
    for edu in C.EDUCACION:
        items += f"""
          <div class="edu-item">
            <div class="edu-year" data-es="{edu['year_es']}" data-en="{edu['year_en']}">{edu['year_es']}</div>
            <div class="edu-name" data-es="{edu['name_es']}" data-en="{edu['name_en']}">{edu['name_es']}</div>
            <div class="edu-inst">{edu['institution']}</div>
          </div>"""
    return f"""
      <div class="edu-strip">
        <div class="edu-strip-label" data-es="Formación académica" data-en="Education">Formación académica</div>
        <div class="edu-grid">{items}</div>
      </div>"""


def build_panel_about():
    return f"""
  <!-- ABOUT -->
  <div class="tab-panel active" id="panel-about" role="tabpanel">
    <canvas id="c-delaunay" aria-hidden="true"></canvas>
    <div class="panel-content light-panel">
      <div class="sec-title" style="font-size:clamp(3rem,8vw,8rem);margin-bottom:3.5rem;" data-es="SOBRE MÍ" data-en="ABOUT ME">SOBRE MÍ</div>
      <div class="about-grid">
        <div>
          {_bio_paragraphs()}
          {_stack()}
          {_education()}
          <div class="edu-strip">
            <div class="edu-strip-label">Explorar</div>
            <div style="display:flex;flex-wrap:wrap;gap:.8rem;">
              <button onclick="document.querySelector('[data-tab=projects]').click()" class="explore-btn" data-es="Proyectos →" data-en="Projects →">Proyectos →</button>
              <button onclick="document.querySelector('[data-tab=blog]').click()" class="explore-btn" data-es="Blog →" data-en="Blog →">Blog →</button>
              <button onclick="document.querySelector('[data-tab=arte]').click()" class="explore-btn" data-es="Arte →" data-en="Art →">Arte →</button>
              <button onclick="document.querySelector('[data-tab=contact]').click()" class="explore-btn" data-es="Contacto →" data-en="Contact →">Contacto →</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>"""


def _project_card(p):
    badges = "".join(f'<span class="p-badge">{b}</span>' for b in p["badges"])
    if p.get("featured"):
        stats_es = "".join(f'<div class="proj-star-stat"><span class="proj-star-stat-label">{k}</span><span class="proj-star-stat-val">{v}</span></div>' for k, v in p["stats_es"])
        stats_en = "".join(f'<div class="proj-star-stat"><span class="proj-star-stat-label">{k}</span><span class="proj-star-stat-val">{v}</span></div>' for k, v in p["stats_en"])
        return f"""
        <a href="{p['url']}" target="_blank" rel="noopener noreferrer" class="proj-star">
          <div class="proj-star-inner">
            <div>
              <div class="p-lang">{p['lang']}</div>
              <div class="p-title" style="font-family:'DM Serif Display',serif;font-size:1.55rem;position:relative;z-index:1;transition:color .3s;">{p['title']}</div>
              <div class="proj-star-body" data-es="{p['body_es']}" data-en="{p['body_en']}">{p['body_es']}</div>
              <div class="p-badges" style="margin-top:1.5rem;">{badges}</div>
            </div>
            <div class="proj-star-details">
              <div id="proj-star-stats-es" data-es="{stats_es}" data-en="{stats_en}">{stats_es}</div>
            </div>
          </div>
          <div class="p-arrow">↗</div>
        </a>"""
    else:
        return f"""
        <a href="{p['url']}" target="_blank" rel="noopener noreferrer" class="proj-card">
          <div class="p-lang">{p['lang']}</div>
          <div class="p-title" data-es="{p['title_es']}" data-en="{p['title_en']}">{p['title_es']}</div>
          <div class="p-desc" data-es="{p['desc_es']}" data-en="{p['desc_en']}">{p['desc_es']}</div>
          <div class="p-badges">{badges}</div>
          <div class="p-meta" data-es="{p['meta_es']}" data-en="{p['meta_en']}">{p['meta_es']}</div>
          <div class="p-arrow">↗</div>
        </a>"""


def build_panel_projects():
    cards = "".join(_project_card(p) for p in C.PROYECTOS)
    return f"""
  <!-- PROJECTS -->
  <div class="tab-panel" id="panel-projects" role="tabpanel">
    <canvas id="c-flow" aria-hidden="true"></canvas>
    <div class="panel-content dark-panel">
      <div class="sec-label" data-es="Repositorios" data-en="Repositories">Repositorios</div>
      <div class="sec-title" data-es="PROYECTOS" data-en="PROJECTS">PROYECTOS</div>
      <div class="proj-grid">{cards}
      </div>
    </div>
  </div>"""


def build_panel_blog():
    articles = ""
    for i, a in enumerate(C.BLOG):
        tags = "".join(f'<span class="ba-tag">{t}</span>' for t in a["tags"])
        articles += f"""
        <a href="{a['url']}" class="blog-article">
          <div class="ba-date" data-es="{a['date_es']}" data-en="{a['date_en']}">{a['date_es']}</div>
          <div class="ba-tags">{tags}</div>
          <div class="ba-title" data-es="{a['title_es']}" data-en="{a['title_en']}">{a['title_es']}</div>
          <div class="ba-excerpt" data-es="{a['excerpt_es']}" data-en="{a['excerpt_en']}">{a['excerpt_es']}</div>
          <div class="ba-read" data-es="{a['read_es']}" data-en="{a['read_en']}">{a['read_es']}</div>
          <div class="ba-num">{str(i+1).zfill(2)}</div>
        </a>"""
    return f"""
  <!-- BLOG -->
  <div class="tab-panel" id="panel-blog" role="tabpanel">
    <canvas id="c-scatter" aria-hidden="true"></canvas>
    <div class="panel-content dark-panel">
      <div class="sec-label" data-es="Escritos" data-en="Articles">Escritos</div>
      <div class="sec-title">BLOG</div>
      <div class="blog-grid" style="grid-template-columns:1fr;">{articles}
      </div>
    </div>
  </div>"""


def _arte_piece(pieza):
    if pieza["tipo"] != "imagen":
        return ""
    titulo_attr = f'data-es="{pieza["titulo_es"]}" data-en="{pieza["titulo_en"]}"'
    return f"""
      <div class="arte-piece">
        <div class="arte-img-wrap">
          <img src="{pieza["url"]}" alt="{pieza["titulo_es"]}" loading="lazy">
        </div>
        <div class="arte-caption">
          <span class="arte-caption-year">{pieza["año"]}</span>
          <span class="arte-caption-title" {titulo_attr}>{pieza["titulo_es"]}</span>
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
      <div class="contact-wrap">
        <div class="contact-big" data-es="{C.CONTACTO_TITULO_ES}" data-en="{C.CONTACTO_TITULO_EN}">{C.CONTACTO_TITULO_ES}</div>
        <a href="mailto:{C.EMAIL}" class="contact-email">{C.EMAIL}</a>
        <a href="{C.CV_PDF}" class="contact-cv" download data-es="↓ Descargar CV" data-en="↓ Download CV">↓ Descargar CV</a>
        <div class="c-links">
          <a href="{C.GITHUB}" target="_blank" rel="noopener noreferrer" class="c-link gh">
            {ICON_GITHUB}<span>GitHub</span>
          </a>
          <a href="{C.LINKEDIN}" target="_blank" rel="noopener noreferrer" class="c-link li">
            {ICON_LINKEDIN}<span>LinkedIn</span>
          </a>
          <a href="{C.KAGGLE}" target="_blank" rel="noopener noreferrer" class="c-link kg">
            {ICON_KAGGLE}<span>Kaggle</span>
          </a>
          <a href="mailto:{C.EMAIL}" class="c-link em">
            {ICON_EMAIL}<span>Email</span>
          </a>
        </div>
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
