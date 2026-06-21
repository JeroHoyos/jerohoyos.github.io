#!/usr/bin/env python3
"""Crea un diario nuevo de The ML Diarys a partir de una plantilla lista para editar.

Uso:
    py blog/new.py "Mi Título"
    py blog/new.py "Reducción de Dimensionalidad" --kind Reducción

Genera  blog/posts/NN-mi-titulo.md  (NN = siguiente número disponible) con el
frontmatter y un cuerpo de ejemplo que muestra TODO lo que podés usar: capítulos,
títulos, math (LaTeX), figuras dibujadas, gráficos por datos (@chart) y código.
Después corré  py build.py  (desde la raíz) para publicarlo.
"""
import sys
import os
import re
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
POSTS = os.path.join(HERE, "posts")

_ACCENTS = str.maketrans("áàäâãéèëêíìïîóòöôõúùüûñç", "aaaaaeeeeiiiiooooouuuunc")


def slugify(title):
    s = title.lower().translate(_ACCENTS)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "diario"


def to_roman(n):
    out, table = "", [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    for value, sym in table:
        while n >= value:
            out += sym
            n -= value
    return out or "I"


def next_num():
    nums = []
    for p in glob.glob(os.path.join(POSTS, "*.md")):
        m = re.match(r"(\d+)", os.path.basename(p))
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) + 1) if nums else 1


TEMPLATE = '''---
num: {roman}
title: {title}
title_en: {title}
kind: {kind}
kind_en: {kind}
date: {date}
date_en: {date}
booktitle: {title}
booktitle_en: {title}
leather: oklch(0.30 0.06 264)
gilt: oklch(0.80 0.12 84)
emblem: net
formula: e = mc^2
teaser: Una línea de gancho — lo que se ve en el Archivo.
teaser_en: A one-line hook — what shows on the Archive.
---

<!-- es -->

@chapter Introducción

@date {date}

# {upper}<br>EN DOS LÍNEAS

## subtítulo en versalitas

Primer párrafo manuscrito. Marcas dentro del texto: **rojo sangre**, *cursiva*,
`código`, y math en línea $a^2 + b^2 = c^2$.

@math E = mc^2

> ⚠ Una caja de advertencia.

! Una nota roja a mano.

<!-- page -->

@chapter Gráficos por datos

# GRÁFICOS<br>SIN SVG

Escribís los datos y el gráfico sale solo, en el estilo del grimorio:

@chart bars | Displacement: 62, Weight: 46, Horsepower: 38, MPG: 30 | fig. 1 — barras desde datos

@chart line | x: e10 e11 e12 e13 ; cuBLAS: 40 55 68 82 ; CPU: 8 12 15 18 | fig. 2 — líneas

<!-- page -->

@chapter Figuras y código

# DIBUJOS<br>A MANO

Diagramas dibujados a mano (los nombres están en diagrams.js):

@fig net | fig. 3 — una red neuronal

```python
print("hola, archivo")
```

! — fin del tomo

<!-- en -->

@chapter Introduction

@date {date}

# {upper}<br>ON TWO LINES

## a small-caps subtitle

First handwritten paragraph. Inline marks: **blood red**, *italic*, `code`, and
inline math $a^2 + b^2 = c^2$.

@math E = mc^2

> ⚠ A warning box.

! A red handwritten note.

<!-- page -->

@chapter Data-driven charts

# CHARTS<br>WITHOUT SVG

Write the data and the chart draws itself, in the grimoire style:

@chart bars | Displacement: 62, Weight: 46, Horsepower: 38, MPG: 30 | fig. 1 — bars from data

@chart line | x: e10 e11 e12 e13 ; cuBLAS: 40 55 68 82 ; CPU: 8 12 15 18 | fig. 2 — lines

<!-- page -->

@chapter Figures and code

# HAND-DRAWN<br>DIAGRAMS

Hand-drawn diagrams (names live in diagrams.js):

@fig net | fig. 3 — a neural network

```python
print("hello, archive")
```

! — end of tome
'''


def main():
    args, opts, it = [], {}, iter(sys.argv[1:])
    for a in it:
        if a.startswith("--"):
            opts[a.lstrip("-")] = next(it, "")
        else:
            args.append(a)
    if not args:
        print('Uso: py blog/new.py "Mi Título" [--kind Diario] [--date "Jun 20, 2026"]')
        sys.exit(1)

    title = args[0]
    kind = opts.get("kind", "Diario")
    date = opts.get("date", "")
    if not date:
        try:
            from datetime import date as _d
            date = _d.today().strftime("%b %d, %Y")
        except Exception:
            date = "Jun 20, 2026"

    num = next_num()
    fname = "{:02d}-{}.md".format(num, slugify(title))
    path = os.path.join(POSTS, fname)
    if os.path.exists(path):
        print("Ya existe:", path)
        sys.exit(1)

    body = TEMPLATE.format(
        roman=to_roman(num), title=title, kind=kind, date=date,
        upper=title.upper(),
    )
    os.makedirs(POSTS, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)

    print("✅ Diario creado:  blog/posts/{}".format(fname))
    print("   Editá el contenido y luego corré:  py build.py")


if __name__ == "__main__":
    main()
