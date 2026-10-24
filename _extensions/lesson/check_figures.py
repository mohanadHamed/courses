#!/usr/bin/env python3
"""Find cross shapes in figures and simulators (project pre-render).

AUTHORING.md ("Rich and visual") says: no religious symbols and no cross
shapes in drawings. A pole with a crossbar, an antenna drawn as a mast with
bars, a grave or a first-aid sign drawn as a plus all read as a cross.

The script reads the straight strokes of
  - every figure and poster (`courses/*/week-*/images/*.svg`, `sims/*.svg`,
    `shared/sims/*.svg`): <line>, thin <rect>, <polyline>, and the straight
    parts (M, L, H, V) of a <path>;
  - every simulator and mini-game (`*.html`): canvas `moveTo(x, y)` followed
    by `lineTo(x, y)`, and thin `fillRect(x, y, w, h)`, written with numbers.
It warns when a short upright stroke is crossed by a short level stroke, and
the crossing is inside both strokes (an arm on every side). Grids, charts and
axes are not crosses: a stroke that crosses three or more others, or a long
one, is left out. A figure where a plus shape is right (a "+" button, the
axes of a small graph) may contain the text `cross-ok` (an SVG or HTML
comment) to skip the check.
"""
import glob
import os
import re
import sys

MAX_LEN = 120     # a symbol is small; longer strokes are axes, walls, tables
THIN = 4          # a rect is a stroke if its length is 4 times its width
SIDE_ARM = 0.2    # the crossbar sticks out at least 20 % of its length on each side
END_ARM = 0.1     # the upright continues at least 10 % beyond the crossbar

NUM = r"(-?\d+(?:\.\d+)?)"
ATTR_RE = re.compile(r'([\w:-]+)="([^"]*)"')
SVG_TAG_RE = re.compile(r"<(line|rect|polyline|path)\b([^>]*)>")
MOVE_LINE_RE = re.compile(r"moveTo\(\s*%s\s*,\s*%s\s*\)\s*;?\s*(?:\w+\.)?lineTo\(\s*%s\s*,\s*%s\s*\)" % (NUM, NUM, NUM, NUM))
FILL_RECT_RE = re.compile(r"fillRect\(\s*%s\s*,\s*%s\s*,\s*%s\s*,\s*%s\s*\)" % (NUM, NUM, NUM, NUM))
PATH_TOKEN_RE = re.compile(r"[MLHVZmlhvzCcSsQqTtAa]|-?\d*\.?\d+(?:e-?\d+)?")


def rect_stroke(x, y, w, h):
    """A thin rectangle as a stroke along its middle, or None."""
    if w <= 0 or h <= 0:
        return None
    if w >= THIN * h:
        return (x, y + h / 2, x + w, y + h / 2)
    if h >= THIN * w:
        return (x + w / 2, y, x + w / 2, y + h)
    return None


def path_strokes(d):
    """The straight parts of a path (absolute M, L, H, V only)."""
    out, cmd, cur, start, nums = [], None, None, None, []
    tokens = PATH_TOKEN_RE.findall(d)

    def flush():
        nonlocal cur, start
        if cmd == "M":
            for i in range(0, len(nums) - 1, 2):
                p = (nums[i], nums[i + 1])
                if i and cur:
                    out.append(cur + p)
                cur = p
                if not i:
                    start = p
        elif cmd == "L" and cur:
            for i in range(0, len(nums) - 1, 2):
                p = (nums[i], nums[i + 1])
                out.append(cur + p)
                cur = p
        elif cmd == "H" and cur:
            for v in nums:
                p = (v, cur[1])
                out.append(cur + p)
                cur = p
        elif cmd == "V" and cur:
            for v in nums:
                p = (cur[0], v)
                out.append(cur + p)
                cur = p
        elif cmd in ("Z", "z") and cur and start:
            out.append(cur + start)
            cur = start
        elif cmd is not None and cmd not in "MLHVZz":
            cur = None  # relative or curved: lose the position
    for t in tokens:
        if t.isalpha():
            flush()
            cmd, nums = t, []
        else:
            nums.append(float(t))
    flush()
    return out


def svg_strokes(text):
    out = []
    for tag, attrs in SVG_TAG_RE.findall(text):
        a = dict(ATTR_RE.findall(attrs))
        try:
            if tag == "line":
                out.append(tuple(float(a.get(k, 0)) for k in ("x1", "y1", "x2", "y2")))
            elif tag == "rect" and "x" in a and "y" in a:
                s = rect_stroke(*(float(a[k]) for k in ("x", "y", "width", "height")))
                if s:
                    out.append(s)
            elif tag == "polyline":
                pts = [float(v) for v in re.findall(NUM, a.get("points", ""))]
                for i in range(0, len(pts) - 3, 2):
                    out.append(tuple(pts[i:i + 4]))
            elif tag == "path":
                out.extend(path_strokes(a.get("d", "")))
        except (KeyError, ValueError):
            continue
    return out


def html_strokes(text):
    out = [tuple(float(v) for v in m) for m in MOVE_LINE_RE.findall(text)]
    for m in FILL_RECT_RE.findall(text):
        s = rect_stroke(*(float(v) for v in m))
        if s:
            out.append(s)
    return out


def upright(s):
    x1, y1, x2, y2 = s
    return abs(x2 - x1) <= 0.15 * abs(y2 - y1) and abs(y2 - y1) > 0


def level(s):
    x1, y1, x2, y2 = s
    return abs(y2 - y1) <= 0.15 * abs(x2 - x1) and abs(x2 - x1) > 0


def crossing(v, h, side=SIDE_ARM, end=END_ARM):
    """Where the bar h crosses the upright v with arms on all sides, or None."""
    vx = (v[0] + v[2]) / 2
    vt, vb = sorted((v[1], v[3]))
    hy = (h[1] + h[3]) / 2
    hl, hr = sorted((h[0], h[2]))
    vlen, hlen = vb - vt, hr - hl
    if not (hl + max(side * hlen, 1) < vx < hr - max(side * hlen, 1)):
        return None
    if not (vt + max(end * vlen, 1) < hy < vb - max(end * vlen, 1)):
        return None
    return (round(vx), round(hy))


def short(s):
    return max(abs(s[2] - s[0]), abs(s[3] - s[1])) <= MAX_LEN


def crosses(strokes):
    ups = [s for s in strokes if upright(s)]
    bars = [s for s in strokes if level(s)]
    # a stroke that crosses three or more others belongs to a grid or a chart
    n_up = [sum(1 for h in bars if crossing(v, h, 0, 0)) for v in ups]
    n_bar = [sum(1 for v in ups if crossing(v, h, 0, 0)) for h in bars]
    return sorted({p for i, v in enumerate(ups) for j, h in enumerate(bars)
                   if short(v) and short(h) and n_up[i] <= 2 and n_bar[j] <= 2
                   for p in [crossing(v, h)] if p})


def files(project_dir):
    pats = ["courses/*/week-*/images/*.svg", "courses/*/week-*/sims/*.svg",
            "courses/*/week-*/sims/*.html", "shared/sims/*.svg", "shared/sims/*.html"]
    for pat in pats:
        yield from sorted(glob.glob(os.path.join(project_dir, pat)))


def check(project_dir):
    warnings = []
    for path in files(project_dir):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if "cross-ok" in text:
            continue
        strokes = svg_strokes(text) if path.endswith(".svg") else html_strokes(text)
        for x, y in crosses(strokes):
            warnings.append("%s: a cross shape at (%d, %d); draw it without a crossbar"
                            % (os.path.relpath(path, project_dir), x, y))
    return warnings


def main():
    project_dir = os.environ.get("QUARTO_PROJECT_DIR") or os.getcwd()
    warnings = check(project_dir)
    if warnings:
        print("Figure check (see AUTHORING.md, \"Rich and visual\"):")
        for w in warnings:
            print("  WARNING " + w)
    else:
        print("Figure check: no cross shapes in figures and simulators.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
