#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for The ML Diarys.

Reads every Markdown diary in  blog/posts/*.md  and generates  books-data.js
(the `const BOOKS = [...]` that the site reads). No external dependencies — just
the Python standard library.

    py build.py            # build everything
    py build.py --check    # build, but fail if something looks wrong

WORKFLOW
    1. Edit (or add) a file in  blog/posts/  — see README.md for the format.
    2. Run  py build.py
    3. Commit & push.  GitHub Pages serves the new books-data.js.

Books are ordered by filename, so name them 01-..., 02-..., etc.
"""

import os
import re
import sys
import glob
import json

POSTS_DIR = "posts"
OUTPUT    = "books-data.js"
PAGE_SEP  = re.compile(r"^\s*<!--\s*page\s*-->\s*$", re.IGNORECASE | re.MULTILINE)


# ---------------------------------------------------------------- frontmatter
def split_frontmatter(text):
    """Return (meta_dict, body) from a `--- ... ---` YAML-ish header."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    meta, i = {}, 1
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
        i += 1
    body = "\n".join(lines[i + 1:])
    return meta, body


# ---------------------------------------------------------------- inline marks
def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def attr_escape(s):
    """Escape a string so it survives inside a double-quoted HTML attribute
    (used to carry raw LaTeX in data-tex for KaTeX to render client-side)."""
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def inline(s):
    """Convert the small set of inline marks into the site's styled spans.

        `code`      ->  inline code
        **blood**   ->  red emphasis
        ++teal++    ->  teal emphasis
        __under__   ->  underline
        ~~strike~~  ->  struck through
        *italic*    ->  <em>
    Raw HTML (e.g. <br>) is left untouched on purpose.
    """
    # pull inline `code` out first so its contents aren't touched by other marks
    codes = []
    def stash(m):
        codes.append(m.group(1))
        return "\x00{}\x00".format(len(codes) - 1)
    s = re.sub(r"`([^`]+)`", stash, s)

    # pull $…$ inline math out too, so KaTeX receives the raw TeX untouched
    maths = []
    def stash_math(m):
        maths.append(m.group(1))
        return "\x01{}\x01".format(len(maths) - 1)
    s = re.sub(r"\$(?!\s)([^$\n]+?)\$", stash_math, s)

    s = re.sub(r"\*\*(.+?)\*\*", r'<span class="red">\1</span>', s)
    s = re.sub(r"\+\+(.+?)\+\+", r'<span class="teal">\1</span>', s)
    s = re.sub(r"__(.+?)__",     r'<span class="underline">\1</span>', s)
    s = re.sub(r"~~(.+?)~~",     r'<span class="strike">\1</span>', s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)

    s = re.sub(r"\x00(\d+)\x00",
               lambda m: '<code class="ic">' + html_escape(codes[int(m.group(1))]) + '</code>', s)
    s = re.sub(r"\x01(\d+)\x01",
               lambda m: '<span class="mathinline" data-tex="'
                         + attr_escape(maths[int(m.group(1))]) + '"></span>', s)
    return s


# ---------------------------------------------------------------- block render
def render_block(block):
    """Turn one Markdown block (paragraph-separated) into one styled element."""
    # fenced code block: ```lang ... ```
    if block.startswith("```"):
        body = block.split("\n")[1:]
        if body and body[-1].strip().startswith("```"):
            body = body[:-1]
        return '<pre class="code">' + html_escape("\n".join(body)) + '</pre>'

    lines = block.split("\n")

    # bullet list -> ul.jot
    if all(l.lstrip().startswith("- ") for l in lines):
        items = "".join(
            "<li>{}</li>".format(inline(l.lstrip()[2:].strip())) for l in lines
        )
        return '<ul class="jot">{}</ul>'.format(items)

    first = lines[0]

    if first.startswith("# "):                       # big diary head
        return '<div class="head">{}</div>'.format(inline(first[2:].strip()))
    if first.startswith("## "):                      # small caps kicker
        return '<div class="kicker">{}</div>'.format(inline(first[3:].strip()))
    if first.startswith("@date "):                   # handwritten date
        return '<div class="date">{}</div>'.format(inline(first[6:].strip()))
    if first.startswith("@type "):                   # typewriter / technical note
        text = " ".join([first[6:].strip()] + [l.strip() for l in lines[1:]])
        return '<p class="type">{}</p>'.format(inline(text))
    if first.startswith("@math"):                    # display LaTeX (KaTeX)
        tex = " ".join([first[5:].strip()] + [l.strip() for l in lines[1:]]).strip()
        return '<div class="mathblock" data-tex="{}"></div>'.format(attr_escape(tex))
    if first.startswith("@fig"):                     # in-page diagram
        rest = first[4:].strip()
        name, _, cap = rest.partition("|")
        return ('<div class="fig tape"><div class="figbody" data-fig="{}"></div>'
                '<div class="cap">{}</div></div>').format(name.strip(), inline(cap.strip()))
    if first.startswith("@chart"):                   # data-driven chart (CHART toolkit)
        body = " ".join([first[6:].strip()] + [l.strip() for l in lines[1:]])
        parts = body.split("|")
        ctype = parts[0].strip()
        cdata = parts[1].strip() if len(parts) > 1 else ""
        cap   = parts[2].strip() if len(parts) > 2 else ""
        return ('<div class="fig tape"><div class="figbody" data-chart="{}" data-cdata="{}"></div>'
                '<div class="cap">{}</div></div>').format(ctype, attr_escape(cdata), inline(cap))
    if first.startswith("> "):                        # bordered warning box
        text = " ".join(re.sub(r"^>\s?", "", l) for l in lines)
        return '<span class="warn">{}</span>'.format(inline(text))
    if first.startswith("! "):                        # red handwritten note
        text = " ".join([first[2:].strip()] + [l.strip() for l in lines[1:]])
        return '<p class="note">{}</p>'.format(inline(text))

    # default: handwritten paragraph
    return '<p class="hand">{}</p>'.format(inline(" ".join(l.strip() for l in lines)))


def split_blocks(md):
    """Split a page into blocks separated by blank lines, but keep a fenced
    ``` code block ``` together even when it contains blank lines."""
    blocks, cur, in_code = [], [], False
    for line in md.strip("\n").split("\n"):
        fence = line.strip().startswith("```")
        if fence and not in_code:
            if any(c.strip() for c in cur):
                blocks.append("\n".join(cur).strip())
            cur, in_code = [line], True
            continue
        if fence and in_code:
            cur.append(line)
            blocks.append("\n".join(cur))
            cur, in_code = [], False
            continue
        if in_code:
            cur.append(line)
        elif line.strip() == "":
            if any(c.strip() for c in cur):
                blocks.append("\n".join(cur).strip())
            cur = []
        else:
            cur.append(line)
    if any(c.strip() for c in cur):
        blocks.append("\n".join(cur).strip())
    return [b for b in blocks if b.strip()]


def to_roman(n):
    out = ""
    for value, sym in [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= value:
            out += sym
            n -= value
    return out or "I"


def render_chapter(no, title, word="Chapter"):
    """A small running head that opens a chapter inside a page."""
    return ('<div class="chap-head">'
            '<span class="chap-no">{} {}</span>'
            '<span class="chap-name">{}</span>'
            '</div>').format(word, to_roman(no), inline(title))


# ---------------------------------------------------------------- one diary
def plain_title(title):
    return title.replace("-<br>", "").replace("<br>", " ").strip()


def split_languages(body):
    """Split a body into (spanish, english).

    Everything before a `<!-- en -->` line is Spanish; everything after is
    English. An optional `<!-- es -->` marker may head the Spanish part and is
    removed. If there is no `<!-- en -->`, english is returned as None.
    """
    body = re.sub(r"(?im)^[ \t]*<!--\s*es\s*-->[ \t]*$\n?", "", body)
    parts = re.split(r"(?im)^[ \t]*<!--\s*en\s*-->[ \t]*$", body, maxsplit=1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return body, None


def build_pages(body, date, chapter_word="Chapter"):
    # every @chapter begins a fresh page (empty pages are dropped below)
    body = re.sub(r"(?m)^[ \t]*@chapter\b", "<!-- page -->\n@chapter", body)
    raw_pages = [blocks for blocks in (split_blocks(p) for p in PAGE_SEP.split(body)) if blocks]

    pages = []
    chap_no = 0
    current_chapter = ""
    n = len(raw_pages)
    for idx, blocks in enumerate(raw_pages):
        chap_parts, body_parts = [], []
        for block in blocks:
            head = block.split("\n", 1)[0]
            if head.startswith("@chapter"):
                chap_no += 1
                current_chapter = head[len("@chapter"):].strip()
                chap_parts.append(render_chapter(chap_no, current_chapter, chapter_word))
            else:
                body_parts.append(render_block(block))
        # chapter head stays pinned at the top; the rest goes in a centered body
        page_html = "".join(chap_parts) + '<div class="pgbody">' + "".join(body_parts) + "</div>"

        if idx == 0:
            folio = date or "i"
        elif idx == n - 1:
            folio = "finis"
        else:
            folio = "p. {}".format(idx)

        pages.append({
            "html":      page_html,
            "folio":     folio,
            "chapter":   current_chapter,
            "chapterNo": chap_no,
        })

    return pages, chap_no > 0


def build_lang(meta, body, suffix):
    """Build one language's view of a book (suffix is '' for ES, '_en' for EN)."""
    pick = lambda key: meta.get(key + suffix) or meta.get(key, "")
    title = pick("title")
    date = pick("date")
    chapter_word = "Chapter" if suffix == "_en" else "Capítulo"
    pages, has_chapters = build_pages(body, date, chapter_word)
    return {
        "title":       title,
        "kind":        pick("kind"),
        "date":        date,
        "booktitle":   meta.get("booktitle" + suffix) or meta.get("booktitle") or plain_title(title),
        "teaser":      inline(pick("teaser")),
        "hasChapters": has_chapters,
        "pages":       pages,
    }


def build_book(path):
    with open(path, "r", encoding="utf-8") as fh:
        meta, body = split_frontmatter(fh.read())

    es_body, en_body = split_languages(body)
    es = build_lang(meta, es_body, "")
    en = build_lang(meta, en_body if en_body is not None else es_body, "_en")

    return {
        "num":     meta.get("num", ""),
        "leather": meta.get("leather", "oklch(0.30 0.05 45)"),
        "gilt":    meta.get("gilt", "oklch(0.80 0.12 82)"),
        "emblem":  meta.get("emblem", "net"),
        "formula": meta.get("formula", ""),
        "es":      es,
        "en":      en,
    }


# ---------------------------------------------------------------- main
def main():
    check = "--check" in sys.argv[1:]
    paths = sorted(glob.glob(os.path.join(POSTS_DIR, "*.md")))
    if not paths:
        print("No diaries found in {}/ — nothing to build.".format(POSTS_DIR))
        sys.exit(1 if check else 0)

    books, problems = [], []
    for path in paths:
        book = build_book(path)
        if not book["es"]["pages"]:
            problems.append("{}: no content pages".format(path))
        if not book["num"] or not book["es"]["title"]:
            problems.append("{}: missing 'num' or 'title' in frontmatter".format(path))
        if len(book["en"]["pages"]) != len(book["es"]["pages"]):
            print("    (note: {} has a different page count in EN vs ES)".format(os.path.basename(path)))
        books.append(book)
        print("  + {:<30} {} ES / {} EN page(s)".format(
            os.path.basename(path), len(book["es"]["pages"]), len(book["en"]["pages"])))

    if problems:
        print("\nProblems:")
        for p in problems:
            print("  ! " + p)
        if check:
            sys.exit(1)

    header = ("/* AUTO-GENERATED by build.py — do NOT edit by hand.\n"
              "   Edit the Markdown diaries in blog/posts/ and run:  py build.py */\n")
    data = json.dumps(books, indent=2, ensure_ascii=False)
    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write(header + "const BOOKS = " + data + ";\n")

    print("\nWrote {} ({} diaries).".format(OUTPUT, len(books)))


if __name__ == "__main__":
    main()
