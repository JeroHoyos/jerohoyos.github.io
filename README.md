# jerohoyos.github.io — Portafolio personal

Sitio estático generado con Python. Para actualizar cualquier cosa, editá el archivo correspondiente y corré:

```bash
py build.py
```

---

## Estructura del proyecto

```
├── build.py                ← Script de generación — corre esto para publicar
├── requirements.txt        ← Dependencias Python (markdown, Pillow)
├── generator/              ← FUENTE DEL PORTAFOLIO
│   ├── content.py          ← Toda la info personal (bio, proyectos, stack, etc.)
│   ├── html.py             ← Estructura HTML de cada sección del portafolio
│   ├── css.py              ← Estilos del sitio principal
│   ├── js.py               ← Animaciones y lógica de la página
│   ├── badges.py           ← Colores de los chips de tecnologías
│   └── icons.py            ← SVGs de redes sociales
├── blog/                   ← FUENTE DEL BLOG (The ML Diarys, estética propia)
│   ├── posts/*.md          ← Los diarios — editá aquí (ver su README.md)
│   ├── build.py            ← Compila los .md en books-data.js
│   └── index.html, blog.js, diagrams.js, assets/
└── docs/                   ← SALIDA · GitHub Pages sirve desde aquí (no editar)
    ├── index.html, 404.html, favicon.ico, og.png, robots.txt, sitemap.xml
    ├── _headers, .nojekyll
    ├── static/             ← Gato animado (oneko.js / .gif)
    ├── dibujos/            ← Imágenes para la sección Arte (.webp)
    └── blog/               ← The ML Diarys desplegado (copiado por build.py)
```

> El `build.py` raíz compila The ML Diarys y copia su salida a `docs/blog/`, así que
> con correr `py build.py` se publica todo. La pestaña **Blog** del portafolio es un
> portal que entra al grimorio en `/blog/`.

---

## Editar información personal

Todo está en **`generator/content.py`**.

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

## Escribir en el blog (The ML Diarys)

El blog es **The ML Diarys**, un sitio-grimorio inmersivo que vive en la carpeta
`blog/` con su propia estética, build y documentación. La pestaña **Blog** del
portafolio es solo el portal que entra a él (`/blog/`).

Para escribir un diario nuevo:

1. Creá o editá un `.md` en `blog/posts/` (formato completo en `blog/README.md` —
   frontmatter del tomo, páginas, diagramas, fórmulas LaTeX, código y ES/EN).
2. Publicá desde la raíz con `py build.py`: compila los diarios (`blog/build.py` →
   `blog/books-data.js`) y copia el grimorio a `docs/blog/` automáticamente.

> No edités `docs/blog/` a mano: se regenera en cada build a partir de `blog/`.

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
