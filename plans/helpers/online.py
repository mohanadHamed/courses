#!/usr/bin/env python3
"""Online activities by content type (AUTHORING.md, "Blended courses").

    python3 plans/helpers/online.py content FILE TYPE
        add or change `content:` in the front matter.
    python3 plans/helpers/online.py sims FILE SPEC
        a sims activity: each "## Step N" keeps only a short instruction (from
        SPEC: "=== N" then the text), its simulator and its Try it box; the
        bullets, figures and boxes of the step go.
"""
import re
import sys


def set_content(path, kind):
    text = open(path, encoding="utf-8").read()
    fm_end = text.index("\n---", 4)
    fm = text[:fm_end]
    if re.search(r"^content:", fm, re.M):
        fm = re.sub(r"^content:.*$", "content: %s" % kind, fm, flags=re.M)
    else:
        fm = re.sub(r"^(marks:.*)$", r"\1\ncontent: %s" % kind, fm, count=1, flags=re.M)
    open(path, "w", encoding="utf-8").write(fm + text[fm_end:])


def sims(path, spec):
    text = open(path, encoding="utf-8").read()
    parts = re.split(r"^(?=## )", text, flags=re.M)
    want = {}
    for block in re.split(r"^=== ", open(spec, encoding="utf-8").read(), flags=re.M)[1:]:
        n, _, body = block.partition("\n")
        want[int(n)] = body.strip()
    for i, part in enumerate(parts):
        m = re.match(r"## Step (\d+) ", part)
        if not m or int(m.group(1)) not in want:
            continue
        head = part.splitlines()[0]
        sim = re.search(r"^\{\{< *sim .*?>\}\}\n", part, re.M | re.S)
        tryit = re.search(r'^::: \{\.callout-tip title="Try it.*?^:::\n:::\n', part, re.M | re.S)
        if not sim or not tryit:
            sys.exit("%s: step %s needs a simulator and a Try it" % (path, m.group(1)))
        parts[i] = "%s\n\n%s\n\n%s\n%s\n" % (head, want[int(m.group(1))], sim.group(0), tryit.group(0))
    open(path, "w", encoding="utf-8").write("".join(parts))


if __name__ == "__main__":
    if sys.argv[1] == "content":
        set_content(sys.argv[2], sys.argv[3])
    else:
        sims(sys.argv[2], sys.argv[3])
