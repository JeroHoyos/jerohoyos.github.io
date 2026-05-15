# jerohoyos.github.io — Portafolio personal

Sitio estático generado con Python. Para actualizar cualquier cosa, editá el archivo correspondiente y corré:

```bash
py build.py
```

---

## Estructura del proyecto

```
├── content.py              ← Toda la info personal (bio, proyectos, stack, etc.)
├── build.py                ← Script de generación — corre esto para publicar
├── requirements.txt        ← Dependencias Python (markdown, Pillow)
├── oneko.js / oneko.gif    ← Gato animado que sigue el cursor
├── _headers                ← Cabeceras de seguridad HTTP
├── blog/
│   ├── posts/              ← Fuente de los posts (.md) — editá aquí
│   └── *.html              ← Generados automáticamente por build.py
├── dibujos/                ← Imágenes para la sección Arte (.webp)
├── src/
│   ├── html.py             ← Estructura HTML de cada sección del portafolio
│   ├── css.py              ← Estilos del sitio principal
│   ├── js.py               ← Animaciones y lógica de la página
│   ├── blog_builder.py     ← Template y generador de posts y series
│   ├── badges.py           ← Colores de los chips de tecnologías
│   └── icons.py            ← SVGs de redes sociales
└── index.html              ← Generado automáticamente (no editar)
```

---

## Editar información personal

Todo está en **`content.py`**.

### Datos básicos

```python
NOMBRE   = "Jerónimo<br>Hoyos Botero"   # <br> = salto de línea en el hero
TITULO   = "Data Scientist"
EMAIL    = "tu@email.com"
CIUDAD   = "Medellín"
GITHUB   = "https://github.com/tuUsuario"
LINKEDIN = "https://linkedin.com/in/tu-perfil"
KAGGLE   = "https://kaggle.com/tuUsuario"
```

### Bio

Cada elemento de la lista es un párrafo. Podés usar `<strong>texto</strong>` para negrita:

```python
BIO_ES = [
    "Primer párrafo en español.",
    "Segundo párrafo con <strong>texto importante</strong>.",
]
BIO_EN = [
    "First paragraph in English.",
    "Second paragraph with <strong>important text</strong>.",
]
```

### Educación

```python
EDUCACION = [
    {
        "year_es": "2024 - Actualidad",
        "year_en": "2024 - Present",
        "name_es": "Ingeniería en Sistemas",
        "name_en": "Computer Engineering",
        "institution": "Universidad Nacional de Colombia",
    },
]
```

### Stack tecnológico

```python
STACK = [
    {
        "label_es": "Lenguajes",
        "label_en": "Languages",
        "chip_class": "chip-lang",        # chip-lang / chip-ml / chip-data /
        "items": ["Python", "C++", "R"],  # chip-viz / chip-ops / chip-gpu
    },
]
```

### Proyectos

**Proyecto destacado** (ocupa 2 columnas):

```python
{
    "featured": True,
    "url": "https://github.com/tuUsuario/proyecto",
    "title": "Nombre del Proyecto",
    "body_es": "Descripción en español.",
    "body_en": "Description in English.",
    "badges": ["PyTorch", "CUDA", "Python"],
},
```

**Proyecto normal**:

```python
{
    "featured": False,
    "url": "https://github.com/tuUsuario/proyecto",
    "title_es": "Nombre en español",
    "title_en": "Name in English",
    "desc_es": "Descripción corta.",
    "desc_en": "Short description.",
    "badges": ["scikit-learn", "Pandas"],
},
```

### Arte

Poné las imágenes en `dibujos/` y registralas en `ARTE`. Usar `.webp` para mejor rendimiento:

```python
ARTE = [
    {"tipo": "imagen", "url": "dibujos/mi-dibujo.webp",
     "titulo_es": "Título", "titulo_en": "Title"},
]
```

---

## Escribir posts del blog

Los posts se crean como archivos `.md` en `blog/posts/`. Al correr `build.py` se generan las páginas HTML automáticamente.

### Frontmatter

```markdown
---
slug: mi-articulo              ← nombre del archivo HTML de salida
title_es: Título en español
title_en: Title in English
date_es: Enero 2025
date_en: January 2025
tags: Python, ML, Estadística
excerpt_es: Resumen corto que aparece en el listing del blog.
excerpt_en: Short summary shown in the blog listing.
read_time: 10 min             ← opcional
---

## Primera sección

Contenido en Markdown...
```

### Markdown soportado

| Sintaxis | Resultado |
|---|---|
| `## Título` | Sección h2 (aparece en el TOC) |
| `### Subtítulo` | Subsección h3 |
| `**negrita**` | **negrita** |
| `*cursiva*` | *cursiva* |
| `` `código` `` | código inline |
| ` ```python ... ``` ` | bloque de código |
| `- item` | lista con viñetas |
| `1. item` | lista numerada |
| `> texto` | blockquote |
| `[texto](url)` | enlace |
| `\| col \| col \|` | tabla |
| `$formula$` | LaTeX inline (KaTeX) |
| `$$formula$$` | LaTeX en bloque (KaTeX) |

### Posts bilingües

Escribí el contenido en español, luego agregá `<!-- EN -->` y repetí en inglés:

```markdown
## Sección en español

Contenido...

<!-- EN -->

## Section in English

Content...
```

### Post stub (sin contenido aún)

Si solo querés registrar un post en el listing sin tener el contenido listo, dejá el cuerpo vacío (solo frontmatter). El builder genera el HTML con un mensaje "Próximamente".

---

## Series de posts

Una serie agrupa varios capítulos bajo una **página de presentación** (`blog/{serie-slug}.html`) que muestra todos los capítulos con botones de navegación. Los capítulos sin contenido aparecen como "Próximamente".

### Estructura de archivos

```text
blog/posts/
├── mi-serie-01.md   ← capítulo 1 (con contenido)
├── mi-serie-02.md   ← capítulo 2 (con contenido)
└── mi-serie-03.md   ← capítulo 3 (stub, "Próximamente")
```

`build.py` genera automáticamente:

- `blog/mi-serie.html` — landing page de la serie
- `blog/mi-serie-01.html`, `02.html`, `03.html` — páginas de cada capítulo

### Frontmatter de un capítulo

```markdown
---
slug: mi-serie-01
title_es: Título del capítulo
title_en: Chapter Title
date_es: Enero 2025
date_en: January 2025
tags: ML, Python
excerpt_es: Descripción del capítulo.
excerpt_en: Chapter description.
read_time: 15 min
series:    mi-serie            ← slug de la serie (= nombre del archivo landing)
series_es: Nombre de la Serie  ← nombre visible en español
series_en: Series Name         ← nombre visible en inglés
chapter:   1                   ← número de capítulo (entero)
---

## Contenido...
```

### Campos opcionales del capítulo 1 (aparecen en la landing de la serie)

```markdown
series_desc_es: Tagline corto de la serie.
series_desc_en: Short series tagline.
series_about_es: Párrafo 1 sobre la serie. || Párrafo 2 sobre la serie.
series_about_en: Paragraph 1 about the series. || Paragraph 2 about the series.
```

> Los párrafos en `series_about_es` se separan con `||`.

---

## Publicar cambios

```bash
# 1. Regenerar
py build.py

# 2. Subir a GitHub
git add .
git commit -m "actualizar contenido"
git push
```

GitHub Pages publica automáticamente desde la rama `main`.
