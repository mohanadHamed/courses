#!/usr/bin/env python3
"""Rewrite task boxes of the lesson sources from a patch file.

Used when a rule changes for every session (for example 2026-11-04: every
task on a page ends with an interactive check, AUTHORING.md "The page checks
every task"): write the new boxes once in a patch file, then

    python3 plans/helpers/boxes.py PATCH [PATCH ...]

Each box is found by its title (exactly once in its file) and replaced as a
whole, with its nested fences; the fences of the file must balance after.

Patch format (blocks run to the next line that starts with "@@@"):

@@@ FILE courses/game-math/week-02/lesson-02.qmd
@@@ BOX Do it · Head to tail in GeoGebra
<the new box, with its opening and closing fences>
@@@ REPLACE
<exact old text, once in the file>
@@@ WITH
<new text>
@@@ AFTER-CHECK 3
<text inserted after the 3rd ::: {.check} block, indented like it>
@@@ DELETE-BOX <exact title>
@@@ DOIT <a unique part of a slide's "**Do it:**" line>
**Result:** <its result, put under the line in a ::: {.reveal}>
@@@ ANSWER <a unique part of a slide's {{< sim … >}} line>
<the answer of its task, added as answer="…">
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..") + os.sep
OPEN = re.compile(r"^(\s*)(:{3,})\s*(\{.*\}|[\w.-]+)\s*$")
CLOSE = re.compile(r"^(\s*)(:{3,})\s*$")


def block_end(lines, i):
    """Index of the closing fence of the fenced div that opens at line i."""
    depth = 0
    for k in range(i, len(lines)):
        if OPEN.match(lines[k]):
            depth += 1
        elif CLOSE.match(lines[k]):
            depth -= 1
            if depth == 0:
                return k
    raise SystemExit("unclosed div at line %d" % (i + 1))


def find_box(lines, title):
    hits = [i for i, l in enumerate(lines) if OPEN.match(l) and ('title="%s"' % title) in l]
    if len(hits) != 1:
        raise SystemExit("box %r found %d times" % (title, len(hits)))
    return hits[0]


def strip_blank(text):
    return text.strip("\n").split("\n")


def apply(path, ops):
    full = ROOT + path
    with open(full, encoding="utf-8") as f:
        text = f.read()
    for op in ops:
        kind, arg, body = op
        lines = text.split("\n")
        if kind == "BOX" or kind == "DELETE-BOX":
            i = find_box(lines, arg)
            j = block_end(lines, i)
            new = strip_blank(body) if kind == "BOX" else []
            if kind == "DELETE-BOX":
                # remove one blank line after the box as well
                if j + 1 < len(lines) and lines[j + 1].strip() == "":
                    j += 1
            lines[i:j + 1] = new
            text = "\n".join(lines)
        elif kind == "REPLACE":
            old, new = body
            n = text.count(old)
            if n != 1:
                raise SystemExit("%s: REPLACE text found %d times: %r" % (path, n, old[:80]))
            text = text.replace(old, new)
        elif kind == "DOIT":
            # Slides: the result of a Do it bullet, on a click, right under it.
            hits = [i for i, l in enumerate(lines) if "**Do it:**" in l and arg in l]
            if len(hits) != 1:
                raise SystemExit("%s: Do it line %r found %d times" % (path, arg, len(hits)))
            i = hits[0]
            res = " ".join(strip_blank(body)).strip()
            lines[i + 1:i + 1] = ["", "::: {.reveal}", "- " + res, ":::"]
            text = "\n".join(lines)
        elif kind == "ANSWER":
            # Slides: the answer of a simulator task, shown on a click.
            hits = [i for i, l in enumerate(lines) if "{{< sim" in l and arg in l]
            if len(hits) != 1:
                raise SystemExit("%s: sim line %r found %d times" % (path, arg, len(hits)))
            i = hits[0]
            res = " ".join(strip_blank(body)).strip()
            if '"' in res or "answer=" in lines[i]:
                raise SystemExit("%s: bad answer for %r" % (path, arg))
            lines[i] = re.sub(r"\s*>\}\}\s*$", ' answer="%s" >}}' % res, lines[i])
            text = "\n".join(lines)
        elif kind == "AFTER-CHECK":
            n = int(arg)
            checks = [i for i, l in enumerate(lines) if re.match(r"^\s*:{3,}\s*\{\.check", l)]
            if n > len(checks):
                raise SystemExit("%s: only %d checks, not %d" % (path, len(checks), n))
            i = checks[n - 1]
            j = block_end(lines, i)
            indent = re.match(r"^(\s*)", lines[i]).group(1)
            new = [(indent + l if l.strip() else "") for l in strip_blank(body)]
            lines[j + 1:j + 1] = [""] + new
            text = "\n".join(lines)
        else:
            raise SystemExit("unknown op " + kind)
    # every fence closed
    depth = 0
    for l in text.split("\n"):
        if OPEN.match(l):
            depth += 1
        elif CLOSE.match(l):
            depth -= 1
    if depth != 0:
        raise SystemExit("%s: fences do not balance (%d)" % (path, depth))
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print("patched %s (%d ops)" % (path, len(ops)))


def parse(patch):
    files, cur, op, buf, old = [], None, None, [], None

    def flush():
        nonlocal op, buf, old
        if op is None:
            return
        body = "\n".join(buf)
        if op[0] == "REPLACE":
            raise SystemExit("REPLACE without WITH")
        if op[0] == "WITH":
            cur[1].append(("REPLACE", None, (old, body.strip("\n"))))
        else:
            cur[1].append((op[0], op[1], body))
        op, buf = None, []

    for line in patch.split("\n"):
        m = re.match(r"^@@@ (FILE|BOX|REPLACE|WITH|AFTER-CHECK|DELETE-BOX|DOIT|ANSWER)\s*(.*)$", line)
        if not m:
            buf.append(line)
            continue
        kind, arg = m.group(1), m.group(2).strip()
        if kind == "WITH":
            old = "\n".join(buf).strip("\n")
            op, buf = ("WITH", None), []
            continue
        flush()
        if kind == "FILE":
            cur = (arg, [])
            files.append(cur)
        elif kind == "REPLACE":
            op, buf = ("REPLACE", None), []
        else:
            op, buf = (kind, arg), []
    if op and op[0] == "REPLACE":
        raise SystemExit("REPLACE without WITH")
    flush()
    return files


def main():
    for p in sys.argv[1:]:
        with open(p, encoding="utf-8") as f:
            for path, ops in parse(f.read()):
                apply(path, ops)


if __name__ == "__main__":
    main()
