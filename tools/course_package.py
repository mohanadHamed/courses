#!/usr/bin/env python3
"""Build the 15-week course package for the dean (AUTHORING.md, "The course package").

Every semester the college asks for the complete materials of each course,
organised by the official weekly plan of its syllabus. Run this after a full
`quarto render`:

    python3 tools/course_package.py [slug ...]

For each course it reads

    courses/<slug>/schedule.yml             the units and their sessions
                                            (`week:` = syllabus week, `slot:`)
    ../courses-private/courses/<slug>/syllabus-weeks.yml
                                            the weekly table of the syllabus,
                                            word for word (private)
    _site/courses/<slug>/week-WW/           the rendered files

and writes `_package/<slug>/` (not in git):

    week-01/ … week-16/   the notes and worksheets (PDF), slides (PPTX),
                          homework and printed online tasks (PDF) of that
                          week, and pages.html with the address of every
                          interactive page
    index.html, index.pdf the syllabus weekly table exactly as approved, with
                          one added column, Materials, naming the sessions
                          that cover each row

It checks that every teaching row of the syllabus has its material and that
every session belongs to exactly one row. Exam rows (`exam: true`) show the
exam as the syllabus does.

syllabus-weeks.yml:

    columns: [Week, Lecture, Seminar, ILOs, PLOs, Descriptors]
    rows:
      - week: 1
        cells: ["1", "…", "…", "A1", "1", "K"]
      - week: 8
        exam: true
        cells: ["8", "Midterm Exam", "", "", "", ""]

Only the Python standard library is used. index.pdf needs Chrome (as
homework_pdf.py); without it only index.html is written.
"""

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIVATE = os.path.join(os.path.dirname(ROOT), "courses-private")
SITE = os.path.join(ROOT, "_site")
OUT = os.path.join(ROOT, "_package")
COURSES = ["game-math", "computing-systems", "digital-media", "digital-skills"]

LABEL = {"lecture": "Lecture", "seminar": "Seminar", "practice": "Practice", "online": "Online activity"}
STEM = {"lecture": "lesson", "seminar": "seminar", "practice": "practice", "online": "online"}
FILE = {"lecture": "lecture", "seminar": "seminar", "practice": "practice", "online": "online"}


# ------------------------------------------------------- a small YAML reader
# Enough for schedule.yml and syllabus-weeks.yml: block mappings and lists,
# flow mappings {a: 1} and lists [a, b], quoted and plain scalars, comments.

def _scalar(s):
    s = s.strip()
    if s == "" or s in ("~", "null"):
        return None
    if s[0] in "\"'":
        q = s[0]
        body = s[1:s.rindex(q)]
        return body.replace('\\"', '"').replace("\\\\", "\\") if q == '"' else body.replace("''", "'")
    if s in ("true", "false"):
        return s == "true"
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return s


def _flow(s, i=0):
    """Parse a flow value starting at s[i]; return (value, next index)."""
    while s[i] == " ":
        i += 1
    if s[i] in "[{":
        close = "]" if s[i] == "[" else "}"
        out = [] if close == "]" else {}
        i += 1
        while True:
            while s[i] in " ,":
                i += 1
            if s[i] == close:
                return out, i + 1
            if close == "]":
                v, i = _flow(s, i)
                out.append(v)
            else:
                m = re.compile(r"\s*([^:]+?)\s*:\s").match(s, i)
                key = m.group(1)
                v, i = _flow(s, m.end())
                out[key] = v
    if s[i] in "\"'":
        q = s[i]
        j = i + 1
        while s[j] != q or (q == '"' and s[j - 1] == "\\"):
            j += 1
        return _scalar(s[i:j + 1]), j + 1
    j = i
    while j < len(s) and s[j] not in ",]}":
        j += 1
    return _scalar(s[i:j]), j


def _strip_comment(line):
    out, q = [], None
    for k, ch in enumerate(line):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "#" and (k == 0 or line[k - 1] == " "):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _value(text):
    text = text.strip()
    if text[:1] in "[{":
        return _flow(text)[0]
    return _scalar(text)


def load_yaml(path):
    lines = []
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = _strip_comment(raw.rstrip("\n"))
            if line.strip():
                lines.append((len(line) - len(line.lstrip(" ")), line.strip()))
    pos = [0]

    def block(indent):
        if pos[0] >= len(lines):
            return None
        ind, text = lines[pos[0]]
        if text.startswith("- ") or text == "-":
            out = []
            while pos[0] < len(lines) and lines[pos[0]][0] == ind and lines[pos[0]][1][:1] == "-":
                item = lines[pos[0]][1][1:].strip()
                if re.match(r"^[^\[{\"'][^:]*:(\s|$)", item):
                    # "- key: value" starts a mapping; its other keys are indented further
                    lines[pos[0]] = (ind + 2, item)
                    out.append(block(ind + 2))
                elif item:
                    pos[0] += 1
                    out.append(_value(item))
                else:
                    pos[0] += 1
                    out.append(block(lines[pos[0]][0]))
            return out
        out = {}
        while pos[0] < len(lines) and lines[pos[0]][0] == ind and not lines[pos[0]][1].startswith("- "):
            key, _, rest = lines[pos[0]][1].partition(":")
            pos[0] += 1
            if rest.strip():
                out[key.strip()] = _value(rest)
            elif pos[0] < len(lines) and lines[pos[0]][0] > ind:
                out[key.strip()] = block(lines[pos[0]][0])
            elif pos[0] < len(lines) and lines[pos[0]][0] == ind and lines[pos[0]][1].startswith("- "):
                out[key.strip()] = block(ind)
            else:
                out[key.strip()] = None
        return out

    return block(lines[0][0]) if lines else {}


# ------------------------------------------------------------------ package

def file_prefix(slug):
    with open(os.path.join(ROOT, "courses", slug, "_metadata.yml"), encoding="utf-8") as f:
        m = re.search(r'^\s+file-prefix:\s*"([^"]+)"', f.read(), re.M)
    return m.group(1) if m else slug.replace("-", "_")


def site_url():
    with open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8") as f:
        m = re.search(r'site-url:\s*"([^"]+)"', f.read())
    url = m.group(1) if m else ""
    return url if url.endswith("/") else url + "/"


def materials(slug, unit, prefix):
    """(label, files to copy, page addresses) for the sessions of one unit."""
    wdir = "week-%02d" % unit["week"]
    src = os.path.join(SITE, "courses", slug, wdir)
    url = site_url() + "courses/%s/%s/" % (slug, wdir)
    labels, files, pages = [], [], []
    for s in unit.get("sessions") or []:
        kind, n = s.get("kind", "lecture"), s["n"]
        label = "%s %d" % (LABEL[kind], n)
        if kind in ("seminar", "practice") and s.get("core") is False:
            label += " (flexible)"
        labels.append(label)
        base = "%s_%s%d" % (prefix, FILE[kind], n)
        names = [base + "_tasks.pdf"] if kind == "online" else [base + ".pdf", base + "_slides.pptx"]
        files += [os.path.join(src, x) for x in names]
        pages.append((label, s.get("title", ""), url + "%s-%02d.html" % (STEM[kind], n)))
    hw = os.path.join(src, "%s_homework%d.pdf" % (prefix, unit["unit"]))
    if os.path.exists(os.path.join(ROOT, "courses", slug, wdir, "homework-%02d.qmd" % unit["unit"])):
        labels.append("Homework %d" % unit["unit"])
        files.append(hw)
        pages.append(("Homework %d" % unit["unit"], "", url + "homework-%02d.html" % unit["unit"]))
    return labels, files, pages


CSS = """
body { font: 10pt/1.35 "Noto Sans", Arial, sans-serif; color: #222; margin: 1.2cm; }
h1 { font-size: 15pt; margin: 0 0 0.2rem; } p.sub { margin: 0 0 0.8rem; color: #555; }
table { border-collapse: collapse; width: 100%; } th, td { border: 1px solid #999; padding: 4px 6px; vertical-align: top; }
th { background: #eee; } td.mat { background: #f6fbf6; font-weight: 600; } tr.exam td { background: #fafafa; font-style: italic; }
@page { size: A4 landscape; margin: 1cm; }
"""


def write_index(slug, course_title, syl, row_mats, out_dir):
    cols = syl.get("columns") or []
    head = "".join("<th>%s</th>" % html.escape(str(c)) for c in cols) + "<th>Materials</th>"
    body = []
    for row in syl.get("rows") or []:
        cells = "".join("<td>%s</td>" % html.escape("" if c is None else str(c)) for c in row.get("cells") or [])
        mats = row_mats.get(row["week"], [])
        mat = "<br>".join(html.escape(m) for m in mats) if mats else ("Exam" if row.get("exam") else "")
        body.append('<tr class="%s">%s<td class="mat">%s</td></tr>' % ("exam" if row.get("exam") else "", cells, mat))
    page = ("<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><title>%s: course package</title><style>%s</style>"
            "<h1>%s</h1><p class=\"sub\">Weekly plan of the syllabus, with the materials of each week. "
            "The files are in the folders week-01 … week-16.</p><table><tr>%s</tr>%s</table></html>"
            % (html.escape(course_title), CSS, html.escape(course_title), head, "".join(body)))
    path = os.path.join(out_dir, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    return path


def find_chrome():
    for c in [os.environ.get("CHROME", ""), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium", "google-chrome", "chromium"]:
        if c and (os.path.isabs(c) and os.path.exists(c) or shutil.which(c)):
            return c if os.path.isabs(c) else shutil.which(c)
    return None


def print_pdf(html_path):
    chrome = find_chrome()
    if not chrome:
        print("  index.pdf not made: Chrome not found (set CHROME=...)")
        return
    profile = tempfile.mkdtemp(prefix="pkg-chrome-")
    try:
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--user-data-dir=" + profile,
                        "--no-pdf-header-footer", "--print-to-pdf=" + html_path[:-5] + ".pdf",
                        "file://" + html_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    finally:
        shutil.rmtree(profile, ignore_errors=True)


def build(slug):
    problems = []
    schedule = load_yaml(os.path.join(ROOT, "courses", slug, "schedule.yml"))
    units = schedule.get("units")
    if not units:
        return ["%s: schedule.yml has no `units:`" % slug]
    syl_path = os.path.join(PRIVATE, "courses", slug, "syllabus-weeks.yml")
    if not os.path.exists(syl_path):
        return ["%s: %s is missing (the syllabus weekly table, private)" % (slug, syl_path)]
    syl = load_yaml(syl_path)
    with open(os.path.join(ROOT, "courses", slug, "_metadata.yml"), encoding="utf-8") as f:
        title = re.search(r'^\s+title:\s*"([^"]+)"', f.read(), re.M).group(1)
    prefix = file_prefix(slug)
    out_dir = os.path.join(OUT, slug)
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir)

    rows = {r["week"]: r for r in syl.get("rows") or []}
    row_mats, seen = {}, {}
    for u in units:
        w = u["week"]
        if w not in rows:
            problems.append("%s: unit %s is in syllabus week %s, which the syllabus table does not have" % (slug, u["unit"], w))
            continue
        labels, files, pages = materials(slug, u, prefix)
        for s in u.get("sessions") or []:
            key = (s.get("kind", "lecture"), s["n"])
            if key in seen:
                problems.append("%s: %s %d is in weeks %s and %s" % (slug, LABEL[key[0]], key[1], seen[key], w))
            seen[key] = w
        row_mats.setdefault(w, []).extend(labels)
        wdir = os.path.join(out_dir, "week-%02d" % w)
        os.makedirs(wdir, exist_ok=True)
        for f in files:
            if os.path.exists(f):
                shutil.copy2(f, wdir)
            else:
                problems.append("%s: week %d: %s was not rendered" % (slug, w, os.path.relpath(f, ROOT)))
        with open(os.path.join(wdir, "pages.html"), "w", encoding="utf-8") as fh:
            fh.write("<!doctype html><meta charset=\"utf-8\"><title>Week %d</title><ul>%s</ul>" % (w, "".join(
                '<li>%s %s: <a href="%s">%s</a></li>' % (html.escape(l), html.escape(t), u_, u_) for l, t, u_ in pages)))
    for w, r in rows.items():
        os.makedirs(os.path.join(out_dir, "week-%02d" % w), exist_ok=True)
        if not r.get("exam") and not row_mats.get(w):
            problems.append("%s: syllabus week %d has no material" % (slug, w))
    index = write_index(slug, title, syl, row_mats, out_dir)
    print_pdf(index)
    print("%s: %d units, %d sessions -> %s" % (slug, len(units), len(seen), os.path.relpath(out_dir, ROOT)))
    return problems


def main(argv):
    slugs = argv[1:] or COURSES
    problems = []
    for slug in slugs:
        problems += build(slug)
    for p in problems:
        print("  PROBLEM " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
