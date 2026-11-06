#!/usr/bin/env python3
"""Check the sessions of the face-to-face version of Digital Skills (README.md).

Run it by hand from the project root (it is not a pre-render step):

    python3 courses/digital-skills/face-to-face/check_f2f.py          # all sessions
    python3 courses/digital-skills/face-to-face/check_f2f.py 3 4      # lectures 3 and 4

For each session written so far (lesson-NN in week-WW/: Lectures 1-30; a
lecture of a practice week has `practises` in schedule.yml):

- the three files: the page, the worksheet (-sheet) and the slides (-slides),
  with the number, title and ILOs of schedule.yml;
- the worksheet: "Before you start", 3 (at most 4) experiments, each with
  "The idea:", "Aim:", a Part A and a Part B ({.part}), steps numbered on
  through the experiment, and after every step a {{< record >}}, a {.check}
  and one interactive check for the page; a "Table of results"; about 8-10
  steps and at most WORDS_MAX words without the results and the page checks;
- the page: one section with {{< experiment N >}} for each experiment, the
  table of results, Key terms, a Try it in each section (every answer with
  its "Why:") and the Summary;
- the slides: Keywords, Summary, "Your worksheet" (with {{< page-qr >}}),
  "Results of the worksheet", at most SLIDES_MAX slides, a task= and an
  answer= on every simulator slide, the answers of every Try it slide;
- no minutes for a part of the session anywhere (only "60 min" may appear):
  the teacher's rule of 2026-11-06 (README.md, "Time");
- every figure, simulator, video and start file that a file names exists;
- no wrapped line of a paragraph starts with a number and a full stop
  ("pages 1 and" / "2."): Markdown reads it as a new numbered list.

Only the Python standard library is used.
"""

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS_MAX = 1200
SLIDES_MAX = 14
STEPS = (6, 11)          # steps in all the experiments of one worksheet
CHECKS = ("choice", "order", "sort", "fill")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


def body(text):
    return re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)


def fm_value(fm, key):
    m = re.search(r"^%s:\s*(.+)$" % re.escape(key), fm, re.M)
    return m.group(1).strip().strip('"') if m else None


def sections(text, level=2):
    """[(title, text)] of the ## sections."""
    out, title, buf = [], None, []
    mark = "#" * level + " "
    for line in body(text).split("\n"):
        if line.startswith(mark) and not line.startswith(mark + "#"):
            if title is not None:
                out.append((title, "\n".join(buf)))
            title, buf = line[len(mark):].strip(), []
        elif title is not None:
            buf.append(line)
    if title is not None:
        out.append((title, "\n".join(buf)))
    return out


def schedule():
    """{3: (title, [ilos], practice?), ...} from schedule.yml (simple parse).
    A lecture of a practice week lists what it practises (`practises`)."""
    out = {}
    for line in read(os.path.join(HERE, "schedule.yml")).split("\n"):
        m = re.search(r"\{kind: lecture, n: (\d+),.*?title: \"([^\"]+)\", ilos: \[([^\]]*)\]", line)
        if m:
            out[int(m.group(1))] = (m.group(2), [x.strip() for x in m.group(3).split(",")], "practises:" in line)
    return out


def steps_of(exp_text):
    """The numbered steps of an experiment: [(number, text of the step)]."""
    out, cur, num = [], [], None
    for line in exp_text.split("\n"):
        m = re.match(r"^(\d+)\. ", line)
        if m:
            if num is not None:
                out.append((num, "\n".join(cur)))
            num, cur = int(m.group(1)), [line]
        elif num is not None:
            if re.match(r"^(:::\s*\{\.part\}|\*\*Part [AB]|\{\{< sim)", line):
                out.append((num, "\n".join(cur)))
                num, cur = None, []
            else:
                cur.append(line)
    if num is not None:
        out.append((num, "\n".join(cur)))
    return out


def strip_page_checks(text):
    """The worksheet as printed: no page checks, no results."""
    out, skip, depth = [], False, 0
    for line in text.split("\n"):
        s = line.strip()
        if not skip and re.match(r"^:::\s*\{\.(choice|order|sort|fill|check)\b", s):
            skip, depth = True, 1
            continue
        if skip:
            if re.match(r"^:::\s*\{", s):
                depth += 1
            elif s == ":::":
                depth -= 1
                if depth == 0:
                    skip = False
            continue
        out.append(line)
    return "\n".join(out)


def count_words(text):
    t = re.sub(r"\{\{<.*?>\}\}", " ", text)
    t = re.sub(r"^:::.*$", " ", t, flags=re.M)
    t = re.sub(r"[*`#|>]", " ", t)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.\-]*", t))


def paths_named(text):
    """Relative paths of figures, simulators, posters, videos and start files."""
    out = re.findall(r"\]\(([^)\s]+\.(?:png|jpg|svg|gif))\)", text)
    out += re.findall(r'(?:file|poster|captions|script|recording)="([^"]+)"', text)
    # captions="English" names the language of an official video, not a file
    return [p for p in out if "/" in p or re.search(r"\.\w+$", p)]


def check_minutes(text, rel, warn):
    # The time of a part of the session ("about 20 minutes", "10 min",
    # "**Time:**"); minutes in a story (Mona's jobs take 120 minutes) are fine.
    pats = (r"\babout\s+\d+\s*(?:minutes?|mins?)\b", r"\b\d+\s*mins?\b", r"\*\*Time:\*\*",
            r"\b\d+\s*(?:minutes?)\s+(?:of|for)\s+(?:the\s+)?(?:slides|worksheet|experiments?|explanation)")
    for pat in pats:
        for m in re.finditer(pat, text, re.I):
            if re.match(r"60\s*min", m.group(0)):
                continue
            line = text[:m.start()].count("\n") + 1
            warn("%s:%d: a time for a part of the session (\"%s\"): the content never gives minutes"
                 % (rel, line, m.group(0)))


def check_wrapped_numbers(text, rel, warn):
    # "look at pages 1 and\n   2." makes "2." a new list: rewrap the line.
    item = re.compile(r"^(\s*)(\d+[.)]|[-*+]|:)(\s|$)")
    lines = text.split("\n")
    for i in range(1, len(lines)):
        cur, prev = lines[i], lines[i - 1]
        m = re.match(r"^(\s*)\d+[.)](\s|$)", cur)
        if not m or not prev.strip() or prev.strip().startswith((":::", "|", "{{<")) \
                or prev.rstrip().endswith(":"):  # a list that a sentence introduces
            continue
        p = item.match(prev)
        # the text of a line of a list item starts after its marker
        indent = len(p.group(0)) if p else len(prev) - len(prev.lstrip())
        if p and not p.group(3):
            continue
        if indent == len(m.group(1)):
            warn("%s:%d: a wrapped line starts with \"%s\": rewrap it, or Markdown starts a list"
                 % (rel, i + 1, cur.strip()[:12]))


def check_choice_blocks(text, rel, warn):
    for m in re.finditer(r"::: \{\.choice[^}]*\}\n(.*?)\n\s*:::", text, re.S):
        block = m.group(1)
        right = len(re.findall(r"^\s*- \[x\]", block, re.M))
        opts = len(re.findall(r"^\s*- \[[ x]\]", block, re.M))
        whys = len(re.findall(r"^\s*Why:", block, re.M))
        line = text[:m.start()].count("\n") + 1
        if right != 1:
            warn("%s:%d: a choice needs exactly one right option ([x]), has %d" % (rel, line, right))
        if whys < opts:
            warn("%s:%d: a choice needs a Why: for every option (%d options, %d reasons)" % (rel, line, opts, whys))


def check_sheet(path, rel, warn, practice=False):
    text = read(path)
    secs = sections(text)
    titles = [t for t, _ in secs]
    if "Before you start" not in titles:
        warn("%s: no \"## Before you start\"" % rel)
    exps = [(t, s) for t, s in secs if re.match(r"^Experiment \d+ · ", t)]
    lo = 2 if practice else 3
    if not lo <= len(exps) <= 4:
        warn("%s: %d experiments (%d, at most 4)" % (rel, len(exps), lo))
    total = 0
    for t, s in exps:
        n = re.match(r"^Experiment (\d+)", t).group(1)
        if not re.search(r"\*\*The idea( \([^)]*\))?:\*\*", s):
            warn("%s: Experiment %s has no \"**The idea:**\"" % (rel, n))
        if "**Aim:**" not in s:
            warn("%s: Experiment %s has no \"**Aim:**\"" % (rel, n))
        parts = re.findall(r"\*\*Part ([AB]) ·", s)
        if parts != ["A", "B"]:
            warn("%s: Experiment %s needs a Part A and then a Part B (found %s)" % (rel, n, parts or "none"))
        if s.count("::: {.part}") != len(parts):
            warn("%s: Experiment %s: put each Part label in a ::: {.part} div" % (rel, n))
        st = steps_of(s)
        nums = [k for k, _ in st]
        if nums != list(range(1, len(nums) + 1)):
            warn("%s: Experiment %s: number the steps on through the experiment (found %s)" % (rel, n, nums))
        for k, step in st:
            if "{{< record" not in step:
                warn("%s: Experiment %s · Step %d has no {{< record >}}" % (rel, n, k))
            if "::: {.check}" not in step:
                warn("%s: Experiment %s · Step %d has no ::: {.check} (the result in the PDF)" % (rel, n, k))
            ics = len(re.findall(r"::: \{\.(?:%s)\b" % "|".join(CHECKS), step))
            if ics != 1:
                warn("%s: Experiment %s · Step %d needs one check for the page (has %d)" % (rel, n, k, ics))
        b_part = s.split("**Part B ·", 1)[1] if "**Part B ·" in s else ""
        if b_part and "{{< sim" not in b_part and "phone" not in b_part.split("\n", 1)[0]:
            warn("%s: Experiment %s: Part B has no simulator (or a task on the phone)" % (rel, n))
        total += len(st)
    if not (5 if practice else STEPS[0]) <= total <= STEPS[1]:
        warn("%s: %d steps in all (about 8-10: a good student finishes the worksheet quickly)" % (rel, total))
    if "## Table of results" not in text or "{.record-table}" not in text:
        warn("%s: no \"## Table of results\" with a ::: {.record-table}" % rel)
    printed = strip_page_checks(body(text))
    printed = printed.split("## Table of results")[0]
    words = count_words(printed)
    if words > WORDS_MAX:
        warn("%s: %d words without the results (at most %d)" % (rel, words, WORDS_MAX))
    check_choice_blocks(text, rel, warn)
    return [re.match(r"^Experiment (\d+)", t).group(1) for t, _ in exps], total, words


def check_page(path, rel, exps, warn, practice=False):
    text = read(path)
    secs = sections(text)
    titles = [t for t, _ in secs]
    # a practice session has no new terms: a Recall instead of Key terms
    for need in (("Recall",) if practice else ("Key terms",)) + ("Before you start", "Table of results"):
        if need not in titles:
            warn("%s: no \"## %s\"" % (rel, need))
    if not any(t.startswith("Summary") or t.startswith("Wrap-up") for t in titles):
        warn("%s: no \"## Summary {.summary}\" (a practice session: Wrap-up)" % rel)
    for n in exps:
        if "{{< experiment %s >}}" % n not in text:
            warn("%s: Experiment %s of the worksheet is not on the page ({{< experiment %s >}})" % (rel, n, n))
    if "{{< experiment results >}}" not in text:
        warn("%s: no {{< experiment results >}}" % rel)
    for t, s in secs:
        if re.match(r"^\d+\.\d+ ", t):
            boxes = s.count('title="Try it')
            if boxes != 1:
                warn("%s: section \"%s\" has %d Try it boxes (one)" % (rel, t, boxes))
            if "{{< experiment" not in s:
                warn("%s: section \"%s\" shows no experiment" % (rel, t))
    answers = len(re.findall(r"^:   ", text, re.M))
    whys = len(re.findall(r"^    Why:", text, re.M))
    if whys < answers:
        warn("%s: %d Try it answers but %d reasons (Why:)" % (rel, answers, whys))


def check_slides(path, rel, warn, practice=False):
    text = read(path)
    secs = sections(text)
    titles = [t for t, _ in secs]
    if len(titles) > SLIDES_MAX:
        warn("%s: %d slides (at most %d)" % (rel, len(titles), SLIDES_MAX))
    if practice and not any(t.startswith("Recall") for t in titles):
        warn("%s: a practice session starts with Recall slides" % rel)
    for need in (() if practice else ("Keywords",)) + ("Summary", "Your worksheet", "Results of the worksheet"):
        if need not in titles:
            warn("%s: no \"## %s\" slide" % (rel, need))
    for t, s in secs:
        if t == "Your worksheet" and "{{< page-qr >}}" not in s:
            warn("%s: the \"Your worksheet\" slide has no {{< page-qr >}}" % rel)
        if t.startswith("Try it") and "{.answer}" not in s:
            warn("%s: \"%s\" has no ::: {.answer}" % (rel, t))
        for m in re.finditer(r"\{\{< sim (.*?)>\}\}", s):
            a = m.group(1)
            if "task=" not in a:
                warn("%s: \"%s\": a simulator slide needs task=" % (rel, t))
            elif "?" in a.split("task=", 1)[1].split('"')[1] and "answer=" not in a:
                warn("%s: \"%s\": the question of the task needs answer=" % (rel, t))
        if t not in ("Keywords",) and not t.startswith("Try it") and "{{< sim" not in s:
            for line in s.split("\n"):
                if line.startswith("- ") and len(line.split()) <= 4 and "?" not in line:
                    warn("%s: \"%s\": a fragment, not a sentence: %s" % (rel, t, line.strip()))


def check_paths(path, rel, warn):
    text = read(path)
    base = os.path.dirname(path)
    for p in paths_named(text):
        if p.startswith("http"):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(base, p))):
            warn("%s: missing file %s" % (rel, p))
    fm = front_matter(text)
    d = fm_value(fm, "start-files-dir")
    for name in re.findall(r"^\s+- name: (\S+)", fm, re.M):
        if not os.path.exists(os.path.normpath(os.path.join(base, d or "files", name))):
            warn("%s: missing start file %s" % (rel, name))


def main(argv):
    project = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
    sched = schedule()
    wanted = set(a.lower() for a in argv[1:])
    warnings = []
    done = []
    for page in sorted(glob.glob(os.path.join(HERE, "week-*", "*.qmd"))):
        name = os.path.basename(page)
        m = re.match(r"^lesson-(\d+)\.qmd$", name)
        if not m:
            continue
        n = int(m.group(1))
        if wanted and str(n) not in wanted:
            continue
        stem = page[:-4]
        rel = os.path.relpath(stem, project)
        warn = warnings.append
        for suffix in ("", "-sheet", "-slides"):
            if not os.path.exists(stem + suffix + ".qmd"):
                warn("%s%s.qmd is missing" % (rel, suffix))
        if not all(os.path.exists(stem + s + ".qmd") for s in ("-sheet", "-slides")):
            continue
        title, ilos, pr = sched.get(n, (None, None, False))
        week = int(re.search(r"week-(\d+)", stem).group(1))
        if n not in (2 * week - 1, 2 * week):
            warn("%s: Lecture %d is not a lecture of week %d (Lectures %d and %d)" % (rel, n, week, 2 * week - 1, 2 * week))
        for suffix in ("", "-sheet", "-slides"):
            text = read(stem + suffix + ".qmd")
            fm = front_matter(text)
            r = rel + suffix + ".qmd"
            if title and fm_value(fm, "title") != title:
                warn("%s: the title is not the one of schedule.yml (\"%s\")" % (r, title))
            if suffix != "-slides":
                num = fm_value(fm, "lesson")
                if num is None or int(num) != n:
                    warn("%s: `lesson: %d` is missing" % (r, n))
                got = fm_value(fm, "ilos")
                if ilos and got and [x.strip() for x in got.strip("[]").split(",")] != ilos:
                    warn("%s: ilos %s, schedule.yml has %s" % (r, got, ilos))
            check_minutes(text, r, warn)
            check_wrapped_numbers(text, r, warn)
            check_paths(stem + suffix + ".qmd", r, warn)
        exps, steps, words = check_sheet(stem + "-sheet.qmd", rel + "-sheet.qmd", warn, pr)
        check_page(stem + ".qmd", rel + ".qmd", exps, warn, pr)
        check_slides(stem + "-slides.qmd", rel + "-slides.qmd", warn, pr)
        slides = len(sections(read(stem + "-slides.qmd")))
        done.append("Lecture %d%s: %d experiments, %d steps, %d words, %d slides"
                    % (n, " (practice)" if pr else "", len(exps), steps, words, slides))
    for d in done:
        print(d)
    for w in warnings:
        print("WARN " + w)
    print("Face-to-face check: %d session(s), %d warning(s)." % (len(done), len(warnings)))
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
