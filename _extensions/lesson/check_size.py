#!/usr/bin/env python3
"""Check that every lesson fits its lecture time (project pre-render).

The size rules are in AUTHORING.md ("Size every lesson for its lecture time").
The lecture time comes from `course.minutes` in courses/<slug>/_metadata.yml.
A lesson has three files; this script counts:

lesson-NN-book.qmd   (lesson notes, PDF: the main text)
  - sections         (## 1.1 …, ## 1.2 …)
  - words            (text only: no front matter, code, shortcodes or markup)
  - worked examples  (callouts titled "Example…")
  - exercises        (numbered items in "## Exercises")
lesson-NN.qmd        (interactive lesson, HTML)
  - sections         (the same ## 1.1 … headings as the notes)
  - "Try it" boxes and the questions in them (`:   answer` lines)
  - simulators and mini-games ({{< sim >}})
  - repetition: at most one "Try it" box in a section (one question set per
    concept), and every section of the notes is also on the page
lesson-NN-slides.qmd (slides)
  - slides (## headings, title slide not counted), one "Live demo" per sim

It prints a warning when a number is outside the range for that lecture time.
It never stops the render. Run it by hand for the full table:

    python3 _extensions/lesson/check_size.py --all

Only the Python standard library is used.
"""

import glob
import os
import re
import sys

# (min, max) for each lecture time. None = no limit. Keep in step with AUTHORING.md.
SIZES = {
    60: {
        "book_sections": (3, 4),
        "words": (1500, 3500),
        "examples": (2, None),
        "exercises": (6, 10),
        "try_its": (4, 6),
        "questions": (15, 28),
        "sims": (0, 2),
        "slides": (15, 22),
    },
    90: {
        "book_sections": (5, 7),
        "words": (2500, 6000),
        "examples": (4, None),
        "exercises": (10, 16),
        "try_its": (6, 9),
        "questions": (30, 45),
        "sims": (1, 3),
        "slides": (26, 36),
    },
}
# Parts every lesson must have (heading text, case does not matter).
BOOK_REQUIRED = ["key terms", "exercises", "answers to the exercises"]
PAGE_REQUIRED = ["key terms", "game challenge", "summary"]
# Parts no lesson may have: no group work; the "Game challenge" (each student
# alone) replaces the class activity.
FORBIDDEN = ["class activity", "practice round"]

NAMES = {
    "book_sections": "sections in the notes",
    "words": "words in the notes",
    "examples": "worked examples in the notes",
    "exercises": "exercises in the notes",
    "try_its": "Try it boxes",
    "questions": "Try it questions",
    "sims": "simulators and mini-games",
    "slides": "slides",
}


def course_minutes(project_dir, slug):
    path = os.path.join(project_dir, "courses", slug, "_metadata.yml")
    try:
        with open(path, encoding="utf-8") as f:
            m = re.search(r"^\s+minutes:\s*(\d+)", f.read(), re.M)
            return int(m.group(1)) if m else None
    except OSError:
        return None


def strip_front_matter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def read(path):
    with open(path, encoding="utf-8") as f:
        return strip_front_matter(f.read())


SECTION_RE = re.compile(r"^## (\d+\.\d+)\b", re.M)


def headings(body):
    return [h.strip().lower() for h in re.findall(r"^## ([^{\n]+)", body, re.M)]


def count_words(body):
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    body = re.sub(r"\{\{<.*?>\}\}", " ", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = re.sub(r"^:::.*$", " ", body, flags=re.M)
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)(\{[^}]*\})?", " ", body)
    return len(re.findall(r"[A-Za-z][A-Za-z'’-]*", body))


def count_book(body):
    ex = 0
    m = re.search(r"^## Exercises\b(.*?)(?=^## |\Z)", body, re.M | re.S)
    if m:
        ex = len(re.findall(r"^\d+\.\s", m.group(1), re.M))
    main = re.split(r"^## Answers", body, flags=re.M)[0]
    return {
        "sections": SECTION_RE.findall(body),
        "words": count_words(main),
        "examples": len(re.findall(r'^:::+ *\{\.callout-\w+ title="Example', body, re.M)),
        "exercises": ex,
        "headings": headings(body),
    }


def count_page(body):
    parts = re.split(r"^(?=## )", body, flags=re.M)
    per_section = {}
    for part in parts:
        m = SECTION_RE.match(part)
        if m:
            per_section[m.group(1)] = len(re.findall(r'^:::+ *\{\.callout-tip title="Try it', part, re.M))
    return {
        "sections": SECTION_RE.findall(body),
        "per_section": per_section,
        "try_its": len(re.findall(r'^:::+ *\{\.callout-tip title="Try it', body, re.M)),
        "questions": len(re.findall(r"^:   \S", body, re.M)),
        "sims": len(re.findall(r"\{\{< *sim ", body)),
        "headings": headings(body),
    }


def count_slides(body):
    titles = re.findall(r"^## (.+)$", body, re.M)
    return {
        "slides": len(titles),
        "demos": sum(1 for t in titles if t.lower().startswith("live demo")),
    }


def check(project_dir):
    rows, warnings = [], []
    pattern = os.path.join(project_dir, "courses", "*", "week-*", "lesson-[0-9][0-9].qmd")
    for path in sorted(glob.glob(pattern)):
        slug = path.split(os.sep)[-3]
        minutes = course_minutes(project_dir, slug)
        rel = os.path.relpath(path, project_dir)
        if minutes not in SIZES:
            continue
        n = {}
        page = count_page(read(path))
        n.update({k: page[k] for k in ("try_its", "questions", "sims")})

        book_path = path[:-4] + "-book.qmd"
        if os.path.exists(book_path):
            book = count_book(read(book_path))
            n.update({"book_sections": len(book["sections"]), "words": book["words"],
                      "examples": book["examples"], "exercises": book["exercises"]})
            for part in BOOK_REQUIRED:
                if not any(h.startswith(part) for h in book["headings"]):
                    warnings.append("%s: no \"%s\" section in the notes" % (rel, part.capitalize()))
            missing = [s for s in book["sections"] if s not in page["sections"]]
            if missing:
                warnings.append("%s: sections %s of the notes are not on the page" % (rel, ", ".join(missing)))
        else:
            warnings.append("%s: no lesson notes (%s)" % (rel, os.path.basename(book_path)))

        for sec, k in page["per_section"].items():
            if k > 1:
                warnings.append("%s: section %s has %d Try it boxes; use one question set per concept" % (rel, sec, k))

        slides_path = path[:-4] + "-slides.qmd"
        if os.path.exists(slides_path):
            s = count_slides(read(slides_path))
            n["slides"] = s["slides"]
            if s["demos"] < n["sims"]:
                warnings.append("%s: %d simulators but %d \"Live demo\" slides" % (rel, n["sims"], s["demos"]))
        else:
            warnings.append("%s: no slides file (%s)" % (rel, os.path.basename(slides_path)))

        for key, (lo, hi) in SIZES[minutes].items():
            v = n.get(key)
            if v is None:
                continue
            if v < lo or (hi is not None and v > hi):
                want = "%d–%d" % (lo, hi) if hi is not None else "%d or more" % lo
                warnings.append("%s: %d %s, a %d-min lesson needs %s" % (rel, v, NAMES[key], minutes, want))
        for part in PAGE_REQUIRED:
            if not any(h.startswith(part) for h in page["headings"]):
                warnings.append("%s: no \"%s\" section" % (rel, part.capitalize()))
        for part in FORBIDDEN:
            if any(h.startswith(part) for h in page["headings"]):
                warnings.append("%s: no \"%s\" in lessons (use a Game challenge)" % (rel, part.capitalize()))
        rows.append((rel, minutes, n))
    return rows, warnings


def main():
    project_dir = os.environ.get("QUARTO_PROJECT_DIR") or os.getcwd()
    rows, warnings = check(project_dir)
    if "--all" in sys.argv:
        cols = ["book_sections", "words", "examples", "exercises", "try_its", "questions", "sims", "slides"]
        short = ["sect", "words", "exmpl", "exer", "try", "quest", "sims", "slides"]
        print("%-44s %4s " % ("lesson", "min") + " ".join("%6s" % c for c in short))
        for rel, minutes, n in rows:
            print("%-44s %4d " % (rel, minutes) + " ".join("%6s" % (n.get(c, "-")) for c in cols))
    if warnings:
        print("Lesson size check (see AUTHORING.md, \"Size every lesson\"):")
        for w in warnings:
            print("  WARNING " + w)
    else:
        print("Lesson size check: %d lessons fit their lecture time." % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
