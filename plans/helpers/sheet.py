#!/usr/bin/env python3
"""Convert a Digital Skills lecture to the worksheet model (the mechanical part).

    python3 plans/helpers/sheet.py page  courses/.../lesson-NN.qmd [--files]
    python3 plans/helpers/sheet.py notes courses/.../lesson-NN-book.qmd "what exp 1 does" "what exp 2 does" ...

page:  the Lab task box of every numbered section becomes {{< experiment N >}};
       "## Before you start" (the start files with --files, the figure of the
       worksheet) after Key terms; "## Table of results" before the Game
       challenge.
notes: the Lab task box of every numbered section becomes "*In class:
       Experiment N of the worksheet, …*"; Lab task boxes outside the numbered
       sections (the case study) are removed.

The worksheet (lesson-NN-sheet.qmd), the slides and the intro paragraphs are
written by hand (AUTHORING.md, "Lecture worksheets").
"""
import re
import sys

BOX = re.compile(r'^::: \{\.callout-note title="Lab task · [^"]*"\}\n.*?^:::\n:::\n', re.M | re.S)
SECTION = re.compile(r"^## \d+\.\d+ ", re.M)


def split_sections(text):
    """[(heading line or "", text)] split at every level-2 heading."""
    parts = re.split(r"^(?=## )", text, flags=re.M)
    return parts


def page(path, files):
    text = open(path, encoding="utf-8").read()
    parts = split_sections(text)
    n = 0
    for i, part in enumerate(parts):
        if SECTION.match(part):
            boxes = BOX.findall(part)
            if len(boxes) != 1:
                sys.exit("%s: section %r has %d Lab task boxes" % (path, part.splitlines()[0], len(boxes)))
            n += 1
            parts[i] = part.replace(boxes[0], "{{< experiment %d >}}\n" % n, 1)
    text = "".join(parts)
    before = ["## Before you start", ""]
    before.append("- **You need:** a computer with the apps of today's experiments (see the worksheet).")
    if files:
        before.append("- **Start file:** download it, then open it. Every student works with the")
        before.append("  same data.")
        before += ["", "{{< start-files >}}", ""]
    before.append("- What you type in the boxes stays in this browser only.")
    before += ["", "![How the worksheet works: do the step, write your result, check it.](../week-01/images/worksheet-steps.png){width=100%}", "", ""]
    m = re.search(r"^## \d+\.\d+ ", text, re.M)
    text = text[:m.start()] + "\n".join(before) + text[m.start():]
    m = re.search(r"^## Game challenge", text, re.M)
    text = text[:m.start()] + "## Table of results\n\n{{< experiment results >}}\n\n" + text[m.start():]
    open(path, "w", encoding="utf-8").write(text)
    print("%s: %d experiments" % (path, n))


def notes(path, descs):
    text = open(path, encoding="utf-8").read()
    parts = split_sections(text)
    n = 0
    for i, part in enumerate(parts):
        boxes = BOX.findall(part)
        if SECTION.match(part):
            if len(boxes) != 1:
                sys.exit("%s: section %r has %d Lab task boxes" % (path, part.splitlines()[0], len(boxes)))
            n += 1
            line = "*In class: Experiment %d of the worksheet, %s.*\n" % (n, descs[n - 1].replace("$", "\\$"))
            parts[i] = part.replace(boxes[0], line, 1)
        else:
            for b in boxes:
                parts[i] = parts[i].replace("\n" + b, "", 1).replace(b, "", 1)
    if n != len(descs):
        sys.exit("%s: %d sections, %d descriptions" % (path, n, len(descs)))
    open(path, "w", encoding="utf-8").write("".join(parts))
    print("%s: %d pointers" % (path, n))


if __name__ == "__main__":
    if sys.argv[1] == "page":
        page(sys.argv[2], "--files" in sys.argv)
    else:
        notes(sys.argv[2], sys.argv[3:])
