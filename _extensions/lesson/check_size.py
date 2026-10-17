#!/usr/bin/env python3
"""Check that every lesson fits its lecture time (project pre-render).

The size rules are in AUTHORING.md ("Size every lesson for its lecture time").
The lecture time comes from `course.minutes` in courses/<slug>/_metadata.yml.
For each lesson-NN.qmd (and its lesson-NN-slides.qmd) this script counts:

- main ideas      (## 1. …, ## 2. …)
- "Try it" boxes  and the questions in them (`:   answer` lines)
- worked examples (callouts titled "Example…")
- simulators      ({{< sim >}}) and "Live demo" slides
- slides          (## headings in the slides file, title slide not counted)

and prints a warning when a number is outside the range for that lecture time.
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
        "ideas": (2, 3),
        "try_its": (3, 5),
        "questions": (12, 20),
        "examples": (0, None),
        "sims": (0, 1),
        "slides": (12, 16),
    },
    90: {
        "ideas": (5, 7),
        "try_its": (8, 10),
        "questions": (30, 40),
        "examples": (3, None),
        "sims": (1, 2),
        "slides": (26, 34),
    },
}
# Parts every lesson of this lecture time must have (heading text, case does not matter).
REQUIRED = {
    60: ["class activity", "summary"],
    90: ["practice round", "class activity", "summary"],
}
# 90-min lesson B (even lesson number) starts with a warm-up on lesson A.
WARM_UP_MINUTES = (90,)

NAMES = {
    "ideas": "main ideas",
    "try_its": "Try it boxes",
    "questions": "Try it questions",
    "examples": "worked examples",
    "sims": "simulators",
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


def count_lesson(text):
    body = strip_front_matter(text)
    return {
        "ideas": len(re.findall(r"^## \d+\.", body, re.M)),
        "try_its": len(re.findall(r'^:::+ *\{\.callout-tip title="Try it', body, re.M)),
        "questions": len(re.findall(r"^:   \S", body, re.M)),
        "examples": len(re.findall(r'^:::+ *\{\.callout-note title="Example', body, re.M)),
        "sims": len(re.findall(r"\{\{< *sim ", body)),
        "headings": [h.strip().lower() for h in re.findall(r"^## ([^{\n]+)", body, re.M)],
    }


def count_slides(text):
    body = strip_front_matter(text)
    titles = re.findall(r"^## (.+)$", body, re.M)
    return {
        "slides": len(titles),
        "demos": sum(1 for t in titles if t.lower().startswith("live demo")),
    }


def check(project_dir):
    rows, warnings = [], []
    for path in sorted(glob.glob(os.path.join(project_dir, "courses", "*", "week-*", "lesson-*.qmd"))):
        name = os.path.basename(path)
        if name.endswith("-slides.qmd"):
            continue
        slug = path.split(os.sep)[-3]
        minutes = course_minutes(project_dir, slug)
        rel = os.path.relpath(path, project_dir)
        if minutes not in SIZES:
            continue
        with open(path, encoding="utf-8") as f:
            n = count_lesson(f.read())
        slides_path = path[:-4] + "-slides.qmd"
        if os.path.exists(slides_path):
            with open(slides_path, encoding="utf-8") as f:
                s = count_slides(f.read())
            n["slides"] = s["slides"]
            if s["demos"] < n["sims"]:
                warnings.append("%s: %d simulators but %d \"Live demo\" slides" % (rel, n["sims"], s["demos"]))
        else:
            n["slides"] = None
            warnings.append("%s: no slides file (%s)" % (rel, os.path.basename(slides_path)))

        for key, (lo, hi) in SIZES[minutes].items():
            v = n.get(key)
            if v is None:
                continue
            if v < lo or (hi is not None and v > hi):
                want = "%d–%d" % (lo, hi) if hi is not None else "%d or more" % lo
                warnings.append("%s: %d %s, a %d-min lesson needs %s" % (rel, v, NAMES[key], minutes, want))
        for part in REQUIRED[minutes]:
            if not any(h.startswith(part) for h in n["headings"]):
                warnings.append("%s: no \"%s\" section" % (rel, part.capitalize()))
        m = re.match(r"lesson-(\d+)\.qmd$", name)
        if minutes in WARM_UP_MINUTES and m and int(m.group(1)) % 2 == 0:
            if not any(h.startswith("warm-up") for h in n["headings"]):
                warnings.append("%s: lesson B has no \"Warm-up\" section" % rel)
        rows.append((rel, minutes, n))
    return rows, warnings


def main():
    project_dir = os.environ.get("QUARTO_PROJECT_DIR") or os.getcwd()
    rows, warnings = check(project_dir)
    if "--all" in sys.argv:
        print("%-46s %4s %5s %6s %9s %8s %4s %6s" % ("lesson", "min", "ideas", "try-it", "questions", "examples", "sims", "slides"))
        for rel, minutes, n in rows:
            print("%-46s %4d %5d %6d %9d %8d %4d %6s" % (rel, minutes, n["ideas"], n["try_its"], n["questions"],
                                                      n["examples"], n["sims"], n["slides"] if n["slides"] is not None else "-"))
    if warnings:
        print("Lesson size check (see AUTHORING.md, \"Size every lesson\"):")
        for w in warnings:
            print("  WARNING " + w)
    else:
        print("Lesson size check: %d lessons fit their lecture time." % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
