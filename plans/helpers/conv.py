#!/usr/bin/env python3
"""Helpers to convert an old lesson into a new lecture.

    conv.py renumber FILE OLD NEW      sections, definitions, examples, `lesson:`, slide subtitle
    conv.py whys FILE REASONS          one reason per line, in the order of the `:   answer` lines
    conv.py checks FILE CHECKS         blocks "=== start of a box title" + the text of its .check
    conv.py intro FILE                 the standard intro paragraph of a lecture page
"""
import re
import sys


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8").write(s)


def renumber(p, old, new):
    s = read(p)
    s = re.sub(r"^(## )%s\.(\d)" % old, r"\g<1>%s.\2" % new, s, flags=re.M)
    s = re.sub(r"\b(Definition|Example|section|sections|Section) %s\.(\d)" % old, r"\1 %s.\2" % new, s)
    s = re.sub(r"^lesson: %s$" % old, "lesson: %s" % new, s, flags=re.M)
    s = re.sub(r'^subtitle: "Lecture %s[^"]*"' % old, 'subtitle: "Lecture %s"' % new, s, flags=re.M)
    write(p, s)


def whys(p, reasons_file):
    reasons = [l.strip() for l in read(reasons_file).splitlines() if l.strip()]
    lines = read(p).splitlines()
    out, k = [], 0
    i = 0
    while i < len(lines):
        out.append(lines[i])
        if re.match(r"^:   \S", lines[i]):
            # skip if a Why: already follows
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            has = j < len(lines) and lines[j].strip().startswith("Why:")
            if not has:
                if k >= len(reasons):
                    sys.exit("not enough reasons (answer %d: %s)" % (k + 1, lines[i]))
                out.append("")
                out.append("    Why: " + reasons[k])
                k += 1
        i += 1
    if k != len(reasons):
        sys.exit("%d reasons for %d answers" % (len(reasons), k))
    write(p, "\n".join(out) + "\n")


def checks(p, checks_file):
    blocks = re.split(r"^=== ", read(checks_file), flags=re.M)[1:]
    lines = read(p).splitlines()
    for b in blocks:
        head, text = b.split("\n", 1)
        head = head.strip()
        start = next((i for i, l in enumerate(lines) if re.match(r'^:::+ *\{\.callout-note[^}]*title="' + re.escape(head), l)), None)
        if start is None:
            sys.exit("box not found: " + head)
        depth, end = 0, None
        for i in range(start, len(lines)):
            m = re.match(r"^(:{3,})\s*(\S.*)?$", lines[i])
            if not m:
                continue
            if m.group(2):
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    end = i
                    break
        new = ["", "::: {.check}"] + text.strip("\n").splitlines() + [":::"]
        # drop a blank line just before the closing fence
        while lines[end - 1].strip() == "":
            del lines[end - 1]
            end -= 1
        lines[end:end] = new
    write(p, "\n".join(lines) + "\n")


INTRO = """This page is the interactive version of the lesson notes (PDF). Each section
starts with a problem in a game studio. Then it explains one idea. It ends
with a **Do it** task and one set of questions. Every question on this page
has its answer: try first, then check."""


def intro(p):
    s = read(p)
    s2 = re.sub(r"This page is the interactive version of the lesson notes \(PDF\)\..*?(?=\n\n)", INTRO, s, count=1, flags=re.S)
    if s2 == s:
        sys.exit("intro not found")
    write(p, s2)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "renumber":
        renumber(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "whys":
        whys(sys.argv[2], sys.argv[3])
    elif cmd == "checks":
        checks(sys.argv[2], sys.argv[3])
    elif cmd == "intro":
        intro(sys.argv[2])
