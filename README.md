# jerohoyos.github.io — Portafolio personal

Sitio estático generado con Python. Para actualizar cualquier cosa, editá el archivo correspondiente y corré:

```bash
py build.py
```

---

## Estructura del proyecto

```
├── content.py          ← Toda la info personal (bio, proyectos, stack, etc.)
├── build.py            ← Script de generación — corre esto para publicar
├── blog/
│   ├── posts/          ← Archivos .md de los posts del blog
│   └── *.html          ← Generados automáticamente (no editar)
├── src/
│   ├── html.py         ← Estructura HTML de cada sección
│   ├── css.py          ← Estilos del sitio principal
│   ├── js.py           ← Animaciones y lógica de la página
│   └── blog_builder.py ← Template de los posts individuales
├── dibujos/            ← Imágenes para la sección Arte
└── index.html          ← Generado automáticamente (no editar)
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
    # Agregar más entradas con el mismo formato
]
```

### Stack tecnológico

Cada categoría tiene un nombre, una clase CSS de color, y una lista de tecnologías:

```python
STACK = [
    {
        "label_es": "Lenguajes",
        "label_en": "Languages",
        "chip_class": "chip-lang",       # chip-lang / chip-ml / chip-data /
        "items": ["Python", "C++", "R"], # chip-viz / chip-ops / chip-gpu
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

Poné las imágenes en la carpeta `dibujos/` y registralas en `ARTE`:

```python
ARTE = [
    {"tipo": "imagen", "url": "dibujos/mi-dibujo.webp",
     "titulo_es": "Título", "titulo_en": "Title"},
]
```

> Usar `.webp` para mejor rendimiento. Podés convertir con cualquier herramienta online.

---

## Escribir posts del blog

Los posts se crean como archivos `.md` en `blog/posts/`. Al correr `build.py`, se generan automáticamente como páginas HTML.

### Frontmatter obligatorio

```markdown
---
slug: mi-articulo              ← nombre-del-archivo.html (sin espacios)
title_es: Título en español
title_en: Title in English
date_es: Enero 2025
date_en: January 2025
tags: Python, ML, Estadística
excerpt_es: Resumen corto que aparece en el listing del blog.
excerpt_en: Short summary shown in the blog listing.
read_time: 10 min
---

## Primera sección

Contenido del artículo en Markdown...
```

### Frontmatter opcional

```markdown
read_es: Leer artículo →       ← texto del botón en español
read_en: Read article →        ← texto del botón en inglés
series:     nombre-serie       ← slug de la serie (ver abajo)
series_es:  Nombre en español  ← nombre visible de la serie
series_en:  Series name        ← nombre visible en inglés
chapter:    1                  ← número de capítulo (entero)
```

### Markdown soportado

| Sintaxis | Resultado |
|---|---|
| `## Título` | Sección h2 (aparece en el TOC) |
| `### Subtítulo` | Subsección h3 |
| `**negrita**` | **negrita** |
| `*cursiva*` | *cursiva* |
| `` `código` `` | código inline |
| ` ```python ... ``` ` | bloque de código con sintaxis |
| `- item` | lista con viñetas |
| `1. item` | lista numerada |
| `> texto` | cita/blockquote |
| `[texto](url)` | enlace |
| `\| col \| col \|` | tabla |
| `$formula$` | LaTeX inline (KaTeX) |
| `$$formula$$` | LaTeX en bloque (KaTeX) |

### Crear una serie de artículos

Los artículos de una misma serie se agrupan en el blog y muestran navegación entre capítulos.

**Capítulo 1** (`blog/posts/mi-serie-cap1.md`):
```markdown
---
slug: mi-serie-cap1
title_es: Título del capítulo 1
title_en: Chapter 1 Title
date_es: Enero 2025
date_en: January 2025
tags: ML, Python
excerpt_es: Descripción del capítulo.
excerpt_en: Chapter description.
read_time: 15 min
series:    mi-serie
series_es: Nombre de la Serie
series_en: Series Name
chapter:   1
---

## Contenido...
```

**Capítulo 2** (`blog/posts/mi-serie-cap2.md`): mismo formato, `chapter: 2`, mismo `series: mi-serie`.

### Post stub (sin contenido)

Si querés registrar un post en el listing pero aún no tenés contenido, dejá el cuerpo vacío (solo frontmatter). El builder lo agrega al índice pero **no sobreescribe** el HTML si ya existe.

---

## Publicar cambios

El sitio se aloja en GitHub Pages. Después de editar:

```bash
# 1. Regenerar
py build.py

# 2. Subir a GitHub
git add .
git commit -m "actualizar contenido"
git push
```

GitHub Pages publica automáticamente desde la rama `main` en unos segundos.
