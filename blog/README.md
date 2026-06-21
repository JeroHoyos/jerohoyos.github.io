# The ML Diarys

A *Gravity Falls*–style field-journal blog about Machine Learning: an atmospheric
"grimoire" hero (parchment pages, bloody handprint, rising embers) that descends
into **The Archive** — leather tomes, each a different ML concept, opening into an
aged two-page reader with hand-drawn diagrams.

You write each diary as a plain **Markdown** file. A tiny `build.py` turns those
into the site's data. No npm, no frameworks, no external Python packages.

## Structure

| File | Purpose | Edit it? |
|------|---------|----------|
| `blog/posts/*.md` | **One diary per file** — this is what you edit | ✅ yes |
| `build.py` | Compiles the `.md` files into `books-data.js` | rarely |
| `books-data.js` | **Auto-generated** book data — overwritten on each build | ❌ never |
| `diagrams.js` | Hand-coded SVG diagrams + cover emblems | only for new diagrams |
| `blog.js` | Builds the entries, drives the reader, animates the embers | rarely |
| `index.html` | The whole page shell + all the CSS | for layout/style |
| `assets/hand.png` | The bloody handprint on the hero | — |
| `.nojekyll` | Tells GitHub Pages to serve files verbatim | — |

## The workflow (this is the part you'll use)

0. **New diary, the comfy way** — scaffold one with the title you want:

   ```powershell
   py blog/new.py "Mi Título"          # → blog/posts/NN-mi-titulo.md
   py blog/new.py "My Topic" --kind Bestiary --date "Jun 20, 2026"
   ```

   It writes a ready-to-edit bilingual template with the frontmatter filled in and
   examples of every block (chapters, math, `@chart`, `@fig`, code). Then just
   rewrite the content.
1. Edit a file in `blog/posts/`, or copy one to start a new diary.
2. Build:

   ```powershell
   py build.py
   ```

   (Use `py` on Windows; `python3` on Mac/Linux.)
3. Preview — open `index.html`, or serve the folder:

   ```powershell
   py -m http.server 8000   # then visit http://localhost:8000
   ```
4. Commit & push. GitHub Pages publishes the new `books-data.js`.

> **Always run `py build.py` after editing a `.md`.** The browser reads
> `books-data.js`, not your Markdown directly.

## Writing a diary

Each file in `blog/posts/` looks like this:

```markdown
---
num: VII
title: The<br>Vanishing Gradient
kind: Cautionary
date: Mar 7, 2026
booktitle: The Fading Signal
leather: oklch(0.30 0.05 200)
gilt: oklch(0.80 0.12 82)
emblem: backprop
teaser: The deeper it gets, the fainter the message — until **nothing** learns.
---

@date Mar 7th, 2026

# THE<br>VANISHING GRADIENT

## the signal that fades

Your first paragraph of handwritten field notes goes here.

<!-- page -->

@fig backprop | fig. 1 — the message dies on the way home

Second page. Each `<!-- page -->` starts a new page in the reader
(pages are shown two at a time, like an open book).
```

### Frontmatter (between the `---` lines)

| Key | Meaning |
|-----|---------|
| `num` | Volume label on the cover (`I`, `II`, …) |
| `title` | Title. Use `<br>` to force a line break (e.g. `The<br>Transformer`) |
| `kind` | Small label under the cover (`Bestiary`, `Ritual`, …) |
| `date` | Shown on the cover and as the first page's folio |
| `booktitle` | Subtitle shown at the top of the open reader |
| `leather` | Cover color (any CSS color; `oklch(...)` matches the theme) |
| `gilt` | Gold trim / formula / sigil color |
| `formula` | **A LaTeX formula shown big and gilt on the cover** (e.g. `\hat{y} = \sigma(Wx + b)`). Rendered with KaTeX. |
| `emblem` | Fallback cover sigil if there's no `formula` — one of: `net`, `descent`, `attn`, `overfit`, `backprop`, `halluc` |
| `teaser` | The hand-scrawled excerpt shown on the homepage scrap |

The cover shows the **`formula`** if you give one, otherwise the `emblem` sigil.
Write plain LaTeX (no `$…$` wrappers): `\frac`, `\sigma`, `^`, `_`, `\nabla`,
`\sqrt`, `\partial`, etc. Long formulas are shrunk automatically to fit the cover.

### Two languages (Spanish + English)

Every diary holds **both** a Spanish and an English version, and a floating
**ES / EN** button (top-left) flips the whole site between them.

In the body, write the Spanish version first, then a separator line, then the
English version:

```markdown
<!-- es -->
（contenido en español…）

<!-- en -->
(English content…)
```

For the cover/metadata, add an `_en` twin to any frontmatter field you want
translated — `title_en`, `kind_en`, `date_en`, `booktitle_en`, `teaser_en`.
Anything without an `_en` twin falls back to the Spanish value. `leather`,
`gilt`, `emblem` and `formula` are shared (no translation needed). If you omit
the `<!-- en -->` section entirely, the English view simply reuses the Spanish
one. See `01-template.md` for a complete bilingual example.

### Body syntax

Separate every element with a **blank line**. Start a new page with `<!-- page -->`.

| You write | You get |
|-----------|---------|
| `@chapter Title` | **Starts a new chapter** — begins a fresh page, adds a chapter head, and shows the chapter in the reader's top bar |
| `# Big Title` | Large diary heading (use `<br>` for line breaks) |
| `## small kicker` | Small-caps subheading |
| `@date Oct 3rd, 2025` | Handwritten date |
| plain text | A handwritten paragraph |
| `@type ...` | Typewriter / technical note |
| `@math TeX` | A display LaTeX formula (KaTeX). Inline math anywhere: `$a^2+b^2=c^2$` |
| `> ...` | Bordered ⚠ warning box |
| `! ...` | Red handwritten note |
| `- item` (lines) | A bullet list |
| `@fig NAME \| caption` | A hand-drawn diagram. Names live in `diagrams.js` (`net`, `curse`, `corrmatrix`, `varimp`, `featsel`, `pca`, `scree`, `tree`, `iv`, `scaling`, `binning`, `skew`, `entropy`, `onehot`, …) |
| `@chart TYPE \| data \| caption` | A **data-driven** chart in the sketch style (`bars`, `line`, `scatter`) — no SVG needed, see below |
| triple-backtick fences | A code block (verbatim; `<`, `>`, `&` are escaped, nothing inside is interpreted) |

A code block looks like this in the Markdown:

````text
```python
print("hola")
```
````

### Chapters

Add `@chapter Title` anywhere in the body. Each one automatically starts a new
page (you don't also need `<!-- page -->`), numbers itself `Chapter I, II, III…`,
and every page after it shows that chapter in the open reader's title bar until
the next `@chapter`. Diary I (`01-neural-network.md`) is set up with two chapters
as a working example. A diary with no `@chapter` simply has no chapters — both
styles work.

Inline marks (work inside any text):

| You write | You get |
|-----------|---------|
| `**text**` | blood-red emphasis |
| `++text++` | teal emphasis |
| `__text__` | underline |
| `~~text~~` | struck through |
| `*text*` | italic |

Plain HTML is allowed too (that's how `<br>` works), so you can drop in anything
the CSS already styles.

### `@chart` — data-driven charts (no SVG)

Write the **data** and the chart draws itself in the grimoire style. Three kinds:

| Kind | Data format | Example |
|------|-------------|---------|
| `bars` | `label: value, label: value, …` | `@chart bars \| Displacement: 62, Weight: 46, MPG: 30 \| fig. 1` |
| `line` | `x: a b c ; Name: v v v ; Name2: v v v` (the `x:` segment is optional) | `@chart line \| x: e10 e11 e12 ; cuBLAS: 40 55 68 ; CPU: 8 12 15 \| fig. 2` |
| `scatter` | `x,y  x,y  x,y` | `@chart scatter \| 1,2  2,3.5  3,3  4,5 \| fig. 3` |

`line` series cycle through ink → blood → teal. Add a new chart kind by adding a
function to the `CHART` map in `diagrams.js` (it gets the raw data string and
returns an `<svg>`).

### Adding a brand-new diagram

Diagrams are real drawing code, so they live in `diagrams.js`. Add a function,
register it in the `FIGS` map (and, if it's also a cover sigil, in `tomeEmblem`
+ `EMBLEM_ORDER`), then reference it from Markdown with `@fig yourname | caption`.

## Deploy to GitHub Pages

```powershell
git init
git add .
git commit -m "The ML Diarys"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

Then **Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)`**.
The site goes live at `https://<you>.github.io/<repo>/`. Everything uses relative
paths, so it also works from a user/org root (`<you>.github.io`).
