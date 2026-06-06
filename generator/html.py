from . import content as C
from .icons import ICON_GITHUB, ICON_LINKEDIN, ICON_KAGGLE, ICON_EMAIL, ICON_LOCATION
from .badges import badge_style


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
    return _proj_card_light(p)


def build_panel_about(blog_items=None):
    proj_minis = "".join(_about_proj_mini(p, i + 1) for i, p in enumerate(C.PROYECTOS[:4]))

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
          <figure class="bio-talk">
            <img src="static/epam-talk.jpg" alt="Jerónimo presentando en Medellín IA" loading="lazy">
            <figcaption data-es="Presentando &ldquo;How to build a transformer from scratch&rdquo; en Medellín IA community · EPAM Medellín" data-en="Presenting &ldquo;How to build a transformer from scratch&rdquo; at Medellín IA community · EPAM Medellín">Presentando &ldquo;How to build a transformer from scratch&rdquo; en Medellín IA community · EPAM Medellín</figcaption>
          </figure>
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
    return _proj_card_light(p, show_img=True)


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


_MONTHS = {
    'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,
    'julio':7,'agosto':8,'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12,
    'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
    'july':7,'august':8,'september':9,'october':10,'november':11,'december':12,
}

def _date_key(date_str):
    p = date_str.lower().split()
    yr  = int(p[1]) if len(p) > 1 and p[1].isdigit() else 0
    mon = _MONTHS.get(p[0], 0) if p else 0
    return (yr, mon)

def _group_date(group):
    kind, data = group
    if kind == "standalone":
        return _date_key(data.get("date_es", ""))
    dates = [_date_key(ch.get("date_es", "")) for ch in data["chapters"]]
    return max(dates) if dates else (0, 0)


def build_panel_blog(blog_items=None):
    items = blog_items if blog_items is not None else C.BLOG

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
                "slug":       s,
                "series_es":  chapters[0].get("series_es", s),
                "series_en":  chapters[0].get("series_en", s),
                "excerpt_es": chapters[0].get("series_excerpt_es", chapters[0].get("excerpt_es", "")),
                "excerpt_en": chapters[0].get("series_excerpt_en", chapters[0].get("excerpt_en", "")),
                "tags":       chapters[0].get("tags", []),
                "chapters":   chapters,
            }))

    groups.sort(key=_group_date, reverse=True)

    wide_entry = ""
    col1 = []
    col2 = []
    scroll_inits = []

    for i, (kind, data) in enumerate(groups):
        is_new = i == 0
        new_badge = '\n          <div class="bc-new"><span class="bc-new-dot"></span><span data-es="Nuevo" data-en="New">Nuevo</span></div>' if is_new else ''
        if kind == "standalone":
            a = data
            new_cls = " bc-entry--new" if is_new else ""
            entry_html = f"""
        <a href="{a['url']}" class="bc-entry{new_cls}">{new_badge}
          <div class="bc-title" data-es="{a['title_es']}" data-en="{a['title_en']}">{a['title_es']}</div>
          <p class="bc-excerpt" data-es="{a['excerpt_es']}" data-en="{a['excerpt_en']}">{a['excerpt_es']}</p>
          <div class="bc-foot">
            <div class="bc-meta">
              <span data-es="{a['date_es']}" data-en="{a['date_en']}">{a['date_es']}</span>
            </div>
            <span class="bc-arrow" data-es="{a['read_es']}" data-en="{a['read_en']}">{a['read_es']}</span>
          </div>
        </a>"""
        else:
            d = data
            n_ch = len(d["chapters"])
            count_es = f"{n_ch} capítulos"
            count_en = f"{n_ch} chapters"
            first_url = f"blog/{d['slug']}.html"
            sid = d["slug"]

            new_cls = " bc-entry--new" if is_new else ""
            if n_ch <= 3:
                chs_html = ""
                for ch in d["chapters"]:
                    cn = str(ch.get("chapter", 0)).zfill(2)
                    chs_html += f"""
              <div class="bc-ch">
                <span class="bc-ch-num">{cn}</span>
                <span class="bc-ch-title" data-es="{ch['title_es']}" data-en="{ch['title_en']}">{ch['title_es']}</span>
                <span class="bc-ch-date" data-es="{ch['date_es']}" data-en="{ch['date_en']}">{ch['date_es']}</span>
              </div>"""
                entry_html = f"""
        <div class="bc-entry bc-entry--series{new_cls}">{new_badge}
          <div class="bc-series-title" data-es="{d['series_es']}" data-en="{d['series_en']}">{d['series_es']}</div>
          <p class="bc-excerpt" data-es="{d['excerpt_es']}" data-en="{d['excerpt_en']}">{d['excerpt_es']}</p>
          <div class="bc-chapters">{chs_html}
          </div>
          <div class="bc-foot">
            <div class="bc-meta"><span data-es="{count_es}" data-en="{count_en}">{count_es}</span></div>
            <a href="{first_url}" class="bc-arrow" data-es="Ver serie →" data-en="View series →">Ver serie →</a>
          </div>
        </div>"""
            else:
                rows_html = ""
                for ch in d["chapters"]:
                    cn = str(ch.get("chapter", 0)).zfill(2)
                    rows_html += f"""
              <div class="bc-scroll-row">
                <div class="bc-scroll-inner"><span class="bc-ch-num">{cn}</span><span class="bc-ch-title" data-es="{ch['title_es']}" data-en="{ch['title_en']}">{ch['title_es']}</span></div>
                <span class="bc-ch-date" data-es="{ch['date_es']}" data-en="{ch['date_en']}">{ch['date_es']}</span>
              </div>"""
                scroll_inits.append(f"_s['{sid}']="+"{"+f"c:0,m:{n_ch-3},t:{n_ch}"+"}"+";")
                entry_html = f"""
        <div class="bc-entry bc-entry--series{new_cls}">{new_badge}
          <div class="bc-series-title" data-es="{d['series_es']}" data-en="{d['series_en']}">{d['series_es']}</div>
          <p class="bc-excerpt" data-es="{d['excerpt_es']}" data-en="{d['excerpt_en']}">{d['excerpt_es']}</p>
          <div class="bc-scroll-wrap">
            <div class="bc-scroll-vp" id="svp-{sid}">
              <div class="bc-scroll-list" id="sl-{sid}">{rows_html}
              </div>
            </div>
          </div>
          <div class="bc-scroll-ctrl">
            <div class="bc-scroll-btns">
              <button class="bc-scroll-btn" id="sbp-{sid}" onclick="bcScroll('{sid}',-1)" disabled>↑</button>
              <button class="bc-scroll-btn bc-scroll-btn--on" id="sbn-{sid}" onclick="bcScroll('{sid}',1)">↓</button>
            </div>
            <span class="bc-scroll-counter" id="sc-{sid}">1–3 / {n_ch}</span>
          </div>
          <div class="bc-foot">
            <div class="bc-meta"><span data-es="{count_es}" data-en="{count_en}">{count_es}</span></div>
            <a href="{first_url}" class="bc-arrow" data-es="Ver serie →" data-en="View series →">Ver serie →</a>
          </div>
        </div>"""

        if i == 0:
            wide_entry = entry_html
        elif i % 2 == 1:
            col1.append(entry_html)
        else:
            col2.append(entry_html)

    scroll_js = ""
    if scroll_inits:
        inits_str = "\n  ".join(scroll_inits)
        scroll_js = (
            "\n<script>\n(function(){\n  var _s = {};\n"
            "  window.bcScroll = function(id, dir) {\n"
            "    var s = _s[id]; if (!s) return;\n"
            "    s.c = Math.max(0, Math.min(s.m, s.c + dir));\n"
            "    document.getElementById('sl-' + id).style.transform = 'translateY(-' + (s.c * 48) + 'px)';\n"
            "    var bp = document.getElementById('sbp-' + id);\n"
            "    var bn = document.getElementById('sbn-' + id);\n"
            "    var sc = document.getElementById('sc-' + id);\n"
            "    bp.disabled = s.c === 0;\n"
            "    bp.className = 'bc-scroll-btn' + (s.c > 0 ? ' bc-scroll-btn--on' : '');\n"
            "    bn.disabled = s.c >= s.m;\n"
            "    bn.className = 'bc-scroll-btn' + (s.c < s.m ? ' bc-scroll-btn--on' : '');\n"
            "    sc.textContent = (s.c + 1) + '–' + Math.min(s.c + 3, s.t) + ' / ' + s.t;\n"
            "  };\n"
            f"  {inits_str}\n"
            "}());\n</script>"
        )

    col1_html = "".join(col1)
    col2_html = "".join(col2)

    return f"""
  <!-- BLOG -->
  <div class="tab-panel" id="panel-blog" role="tabpanel">
    <canvas id="c-scatter" aria-hidden="true"></canvas>
    <div class="panel-content dark-panel">
      <div class="sec-title">BLOG</div>
      <div class="sec-sub" data-es="{C.BLOG_SUB_ES}" data-en="{C.BLOG_SUB_EN}">{C.BLOG_SUB_ES}</div>
      <div class="blog-list">{wide_entry}
        <div class="blog-cols">
          <div class="bc-col">{col1_html}
          </div>
          <div class="bc-col">{col2_html}
          </div>
        </div>
      </div>
    </div>
  </div>{scroll_js}"""


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
  <!-- ARTE -->
  <div class="tab-panel" id="panel-arte" role="tabpanel">
    <canvas id="c-dp" aria-hidden="true"></canvas>
    <div class="panel-content light-panel">
      <div class="sec-title" data-es="ARTE" data-en="ART">ARTE</div>
      <div class="sec-sub" data-es="{C.ARTE_SUB_ES}" data-en="{C.ARTE_SUB_EN}">{C.ARTE_SUB_ES}</div>
      <div class="arte-grid">{grid_content}
      </div>
    </div>
  </div>
  <!-- LIGHTBOX -->
  <div id="lightbox" role="dialog" aria-modal="true" aria-label="Imagen ampliada">
    <button id="lb-close" aria-label="Cerrar">&#x2715;</button>
    <img id="lb-img" src="" alt="">
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
