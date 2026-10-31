"""Split a .qmd into front matter and level-2 blocks, and put blocks together again.

Used to merge two old lectures into one (plan v3): take the blocks of both
files, set new section numbers (set_section), renumber definitions and
examples (renumber_defs) and Try it boxes (renumber_tryits,
renumber_slide_tryits), then join them with a new front matter.
"""
import re

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def split(text):
    """Return (front_matter, [(heading or None, body)]). body keeps its trailing newline."""
    fm = ""
    if text.startswith("---\n"):
        end = text.index("\n---\n", 4)
        fm = text[: end + 5]
        text = text[end + 5:]
    blocks, head, buf, fence = [], None, [], False
    for line in text.splitlines(keepends=True):
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            blocks.append((head, "".join(buf)))
            head, buf = line.rstrip("\n"), []
        else:
            buf.append(line)
    blocks.append((head, "".join(buf)))
    return fm, blocks

def get(blocks, start):
    """The block whose heading starts with '## ' + start."""
    for h, b in blocks:
        if h and h[3:].startswith(start):
            return h, b
    raise KeyError(start)

def join(fm, blocks):
    out = [fm]
    for h, b in blocks:
        if h:
            out.append(h + "\n")
        out.append(b)
    text = "".join(out)
    return re.sub(r"\n{3,}", "\n\n", text).rstrip("\n") + "\n"

def renumber_heading(h, old, new):
    return re.sub(r"^## %d\.(\d+)" % old, lambda m: "## %d.%s" % (new, m.group(1)), h)

def set_section(h, new_num):
    return re.sub(r"^## \d+\.\d+", "## " + new_num, h)

def renumber_defs(text, n):
    """Definition X.Y and Example X.Y numbered N.1, N.2 ... in order of appearance."""
    for kind in ("Definition", "Example"):
        count = [0]
        def rep(m):
            count[0] += 1
            return "%s %d.%d" % (kind, n, count[0])
        text = re.sub(r"%s \d+\.\d+" % kind, rep, text)
    return text

def renumber_tryits(text):
    count = [0]
    def rep(m):
        count[0] += 1
        return 'title="Try it %d ·' % count[0]
    return re.sub(r'title="Try it \d+ ·', rep, text)

def renumber_slide_tryits(text):
    count = [0]
    def rep(m):
        count[0] += 1
        return "## Try it %d ·" % count[0]
    return re.sub(r"^## Try it [\d–-]+ ·", rep, text, flags=re.M)
