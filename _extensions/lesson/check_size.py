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
  - applied first: one "Do it" (or "Lab task") box in every section of the
    notes and of the page
lesson-NN-slides.qmd (slides)
  - slides (## headings, title slide not counted); every simulator of the page
    is on a slide ("Live demo", or the Game challenge slide for the game of
    the lesson)
  - clear slides (AUTHORING.md, "Slides explain themselves"): every question
    is a full question (a question word and "?"), its answer is on the same
    slide, an Example states its question, every simulator slide has a
    `task`, no fragments of one to three words, no group work ("Do it together")
The game of the lesson: a mini-game in the page's Game challenge must also be
in the notes (Case study, poster + QR) and on the Game challenge slide.

Seminars and practice sessions (seminar-NN*.qmd, practice-NN*.qmd; AUTHORING.md,
"What a seminar looks like") are short: two problems, with room for the
teacher's explanations. They are checked with SEMINAR_SIZES: activities
(## Activity N), Try it questions, slides and words of the worksheet; the
planned time (Recall + the "· N min" of every Activity box) against
SEMINAR_TIME; a Recall section, one "Check your result" ({.check}) in every
activity, no new glossary terms, no separate Game challenge or case study, at
most one Task with AI, and Recall / Activity / Check slides.

On every page (AUTHORING.md, "The page teaches, the notes test"): every Do it,
Lab task and Activity box has a {.check}, and every Try it question has a
"Why:" reason. Graded work (homework, "Tasks to submit") never shows them.
"Task with AI" boxes (a harder task done with an AI assistant): at most AI_MAX
per file, each with a starter {.prompt} and a check step ("Check:"); on a page
also a {.check}, in graded work the AI-use statement.

A lecture worksheet (a practical course: lesson-NN-sheet.qmd; AUTHORING.md,
"Lecture worksheets") is the main document of the session. It needs "Before
you start", one experiment per section of the notes (## Experiment N · …,
with an "Aim:"), SHEET_STEPS numbered steps in each, a {{< record >}} field
and a ::: {.check} after every step, a "Table of results" (::: {.record-table})
and its start files in files/. The page shows every experiment in its section
({{< experiment N >}}, which counts as the section's task), each section of
the notes points to its experiment, and the slides have an "Experiment N" and
a "Check N" slide for each.

An online activity (blended course: online-NN.qmd, or an older lesson-NN.qmd
with `online: true`) has no notes and no slides. It is checked for its own parts (AUTHORING.md, "Blended
courses"): "Before you start", Steps marked {.study} with one "Try it" each,
"Tasks to submit" ({.tasks}) with marks and answer space, "How to submit",
`due:` and `marks:`, and at least ONLINE_MIN_SIMS simulators.

In every file of a unit: a fenced div (`::: {...}`) needs a blank line before
it when it follows text; otherwise pandoc prints the colons as text (a
`{.check}` after "*Your result:*" then shows in the PDF and never reaches the
results).

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
        "words": (0, 3500),
        "examples": (2, None),
        "exercises": (6, 10),
        "try_its": (4, 6),
        "questions": (15, 28),
        "sims": (0, 4),
        "slides": (10, 16),
    },
    90: {
        "book_sections": (4, 7),
        "words": (0, 6000),
        "examples": (4, None),
        "exercises": (10, 16),
        "try_its": (6, 9),
        "questions": (30, 45),
        "sims": (1, 3),
        "slides": (20, 28),
    },
}
# Seminars and practice sessions (no new ideas: activities on earlier lectures).
SEMINAR_SIZES = {
    60: {"activities": (2, 3), "questions": (6, 12), "slides": (5, 9), "words": (0, 1200)},
    90: {"activities": (2, 3), "questions": (8, 15), "slides": (6, 10), "words": (0, 1600)},
}
# Planned minutes of a seminar, at most: Recall (SEMINAR_RECALL_MIN) + the
# activity times. The rest of the session is for the teacher's explanations.
SEMINAR_TIME = {60: 40, 90: 60}
SEMINAR_RECALL_MIN = 5
SEMINAR_AI_MAX = 1
SEMINAR_BOOK_REQUIRED = ["recall", "exercises", "answers to the exercises"]
SEMINAR_PAGE_REQUIRED = ["recall", "wrap-up"]
# A seminar is two short problems: no separate Game challenge or case study.
SEMINAR_FORBIDDEN = ["game challenge", "case study"]
# "Task with AI" boxes in one file, at most.
AI_MAX = 2
# Lecture worksheet: (min, max) steps in an experiment, and words at most.
SHEET_STEPS = (2, 5)
SHEET_WORDS = 1600
SHEET_REQUIRED = ["before you start", "table of results"]
# Online activity (blended course): at least this many simulators, and
# (min, max) tasks to submit.
ONLINE_MIN_SIMS = 2
ONLINE_TASKS = (2, 4)
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
    "activities": "activities",
    "minutes": "planned minutes",
    "experiments": "experiments",
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
SIM_FILE_RE = re.compile(r'\{\{< *sim [^>]*file="([^"]+)"')


def section(body, title_start):
    """The text of the first ## section whose heading starts with title_start."""
    m = re.search(r"^## " + re.escape(title_start) + r".*?$(.*?)(?=^## |\Z)", body, re.M | re.S | re.I)
    return m.group(1) if m else ""
DO_IT_RE = re.compile(r'^:::+ *\{\.callout-note[^}\n]*title="(Do it|Lab task|Activity)', re.M)
# An experiment of the lecture worksheet, shown on the page.
EXPERIMENT_RE = re.compile(r"^\{\{< *experiment (\d+) *>\}\}", re.M)
TASK_TITLES = "Do it|Lab task|Activity|Task with AI"
TRY_IT_RE = re.compile(r'^:::+ *\{\.callout-tip[^}\n]*title="Try it', re.M)


def boxes(body):
    """Every fenced div: (opening line, its text up to the closing fence)."""
    out, stack = [], []
    lines = body.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(:{3,})\s*(\S.*)?$", line)
        if not m:
            continue
        if m.group(2):
            stack.append((i, line))
        elif stack:
            start, head = stack.pop()
            out.append((head, "\n".join(lines[start + 1:i])))
    return out


def task_boxes_without_check(body):
    """Titles of Do it / Lab task / Activity / Task with AI boxes that have no {.check}."""
    out = []
    for head, text in boxes(body):
        m = re.search(r'\{\.callout-note[^}]*title="((%s)[^"]*)"' % TASK_TITLES, head)
        if m and not re.search(r"^:::+ *\{\.check\}", text, re.M):
            out.append(m.group(1))
    return out


def questions_without_why(body):
    """The answers (`:   answer`) of Try it questions that have no "Why:" reason."""
    out = []
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if not re.match(r"^:   \S", line):
            continue
        why = False
        for nxt in lines[i + 1:]:
            if nxt.strip() == "":
                continue
            if not nxt.startswith("    "):
                break
            if nxt.strip().startswith("Why:"):
                why = True
                break
        if not why:
            out.append(line[4:].strip())
    return out


def ai_task_warnings(body, graded=False):
    """Warnings for the "Task with AI" boxes of one file."""
    out = []
    ai = [(h, t) for h, t in boxes(body) if ".ai-task" in h or 'title="Task with AI' in h]
    if len(ai) > AI_MAX:
        out.append("%d Task with AI boxes, at most %d (only where AI lets students do more)" % (len(ai), AI_MAX))
    for head, text in ai:
        title = (re.search(r'title="([^"]*)"', head) or re.search(r"(.*)", head)).group(1)
        if not re.search(r"^\s*:::+ *\{\.prompt\}", text, re.M):
            out.append('Task with AI "%s" has no starter ::: {.prompt}' % title)
        if not re.search(r"\bCheck:|\*\*Check\*\*", text):
            out.append('Task with AI "%s" has no check step ("Check:"): the AI can be wrong' % title)
        if graded and "AI-use statement" not in text:
            out.append('Task with AI "%s" in graded work does not ask for the AI-use statement' % title)
    return out


def answered_warnings(body):
    """Warnings for a page: tasks without results, questions without reasons."""
    out = []
    for t in task_boxes_without_check(body):
        out.append('"%s" has no ::: {.check} (Check your result)' % t)
    missing = questions_without_why(body)
    if missing:
        out.append("%d Try it question(s) without a Why: reason (first: \"%s\")" % (len(missing), missing[0][:40]))
    return out


def graded_warnings(text):
    """Graded work (homework, Tasks to submit) never shows answers."""
    out = []
    if re.search(r"^:::+ *\{\.check\}", text, re.M):
        out.append("graded tasks show a result (::: {.check}); keep solutions in courses-private")
    if re.search(r"^\s+Why:", text, re.M):
        out.append("graded tasks show a reason (Why:); keep solutions in courses-private")
    return out


def do_its_per_section(body):
    """Number of "Do it" / "Lab task" boxes (or worksheet experiments) in each numbered section."""
    out = {}
    for part in re.split(r"^(?=## )", body, flags=re.M):
        m = SECTION_RE.match(part)
        if m:
            out[m.group(1)] = len(DO_IT_RE.findall(part)) + len(EXPERIMENT_RE.findall(part))
    return out


def sections_text(body):
    """{"6.1": text of the section, …} in order."""
    out = {}
    for part in re.split(r"^(?=## )", body, flags=re.M):
        m = SECTION_RE.match(part)
        if m:
            out[m.group(1)] = part
    return out


def check_sheet(path, rel, notes_sections, page_body, slides_body):
    """Warnings and the number of experiments of a lecture worksheet."""
    out = []
    text = read(path)
    srel = rel[:-4] + "-sheet.qmd"
    heads = headings(text)
    for part in SHEET_REQUIRED:
        if not any(h.startswith(part) for h in heads):
            out.append("%s: no \"%s\" section" % (srel, part.capitalize()))
    exps = [p for p in re.split(r"^(?=## )", text, flags=re.M) if re.match(r"## Experiment \d", p)]
    nums = [int(re.match(r"## Experiment (\d+)", p).group(1)) for p in exps]
    if nums != list(range(1, len(nums) + 1)):
        out.append("%s: experiments numbered %s; number them 1, 2, 3 …" % (srel, nums))
    if notes_sections and len(nums) != len(notes_sections):
        out.append("%s: %d experiments for %d sections of the notes (one experiment per section)"
                   % (srel, len(nums), len(notes_sections)))
    for p in exps:
        title = p.splitlines()[0][3:].strip()
        if " · " not in title:
            out.append('%s: "%s" has no short title ("## Experiment 1 · The grid")' % (srel, title))
        if not re.search(r"\bAim:", p):
            out.append('%s: "%s" has no "Aim:" (what the experiment shows)' % (srel, title))
        steps = re.split(r"^(?=\d+\. )", p, flags=re.M)[1:]
        if not (SHEET_STEPS[0] <= len(steps) <= SHEET_STEPS[1]):
            out.append('%s: "%s" has %d steps; an experiment has %d–%d' % ((srel, title, len(steps)) + SHEET_STEPS))
        for i, st in enumerate(steps, 1):
            if "{{< record" not in st:
                out.append('%s: "%s", step %d has no {{< record … >}} (a place for the result)' % (srel, title, i))
            if not re.search(r"^\s*:::+ *\{\.check\}", st, re.M):
                out.append('%s: "%s", step %d has no ::: {.check} (its result)' % (srel, title, i))
    results = section(text, "Table of results")
    if results and not re.search(r"^:::+ *\{\.record-table\}", results, re.M):
        out.append("%s: the Table of results is not in a ::: {.record-table} (room to write)" % srel)
    files = re.findall(r"^\s+- name:\s*\"?([^\"\n]+)", front_matter(path), re.M)
    for f in files:
        if not os.path.exists(os.path.join(os.path.dirname(path), "files", f.strip())):
            out.append("%s: the start file files/%s is missing" % (srel, f.strip()))
    if files and "{{< start-files" not in text:
        out.append("%s: the start files are not listed ({{< start-files >}} in Before you start)" % srel)
    main = re.split(r"^## Results", text, flags=re.M)[0]
    if count_words(main) > SHEET_WORDS:
        out.append("%s: %d words, a worksheet has at most %d" % (srel, count_words(main), SHEET_WORDS))
    # The page shows every experiment in its section; the notes point to it.
    page_secs = list(sections_text(page_body).items())
    for k, (sec, part) in enumerate(page_secs, 1):
        found = [int(n) for n in EXPERIMENT_RE.findall(part)]
        if k <= len(nums) and found != [k]:
            out.append("%s: section %s of the page does not show {{< experiment %d >}}" % (rel, sec, k))
    if files and "{{< start-files" not in page_body:
        out.append("%s: the page does not list the start files ({{< start-files >}})" % rel)
    for k, (sec, part) in enumerate(notes_sections.items(), 1):
        if not re.search(r"\bExperiment %d\b" % k, part):
            out.append("%s: section %s of the notes does not point to Experiment %d of the worksheet" % (rel, sec, k))
    if slides_body is not None:
        titles = re.findall(r"^## (.+)$", slides_body, re.M)
        for k in nums:
            if not any(re.match(r"Experiment %d\b" % k, t) for t in titles):
                out.append('%s: no "Experiment %d" slide (the teacher shows its steps)' % (rel[:-4] + "-slides.qmd", k))
            if not any(re.match(r"Check %d\b" % k, t) for t in titles):
                out.append('%s: no "Check %d" slide (the results of Experiment %d, .reveal)' % (rel[:-4] + "-slides.qmd", k, k))
        for part in re.split(r"^(?=## )", slides_body, flags=re.M):
            m = re.match(r"## (Check \d+.*)", part)
            if m and not re.search(r"^:::+ *\{\.(answer|reveal)\}", part, re.M):
                out.append('%s: slide "%s": the results are not on the slide (.reveal or .answer)'
                           % (rel[:-4] + "-slides.qmd", m.group(1).strip()))
    return out, len(nums)


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
        "do_its": do_its_per_section(body),
        "headings": headings(body),
    }


def count_page(body):
    parts = re.split(r"^(?=## )", body, flags=re.M)
    per_section = {}
    for part in parts:
        m = SECTION_RE.match(part)
        if m:
            per_section[m.group(1)] = len(TRY_IT_RE.findall(part))
    return {
        "sections": SECTION_RE.findall(body),
        "per_section": per_section,
        "try_its": len(TRY_IT_RE.findall(body)),
        "questions": len(re.findall(r"^:   \S", body, re.M)),
        "sims": len(re.findall(r"\{\{< *sim ", body)),
        "sim_files": set(SIM_FILE_RE.findall(body)),
        "challenge_sims": set(SIM_FILE_RE.findall(section(body, "Game challenge"))),
        "do_its": do_its_per_section(body),
        "headings": headings(body),
    }


def count_slides(body):
    titles = re.findall(r"^## (.+)$", body, re.M)
    return {
        "slides": len(titles),
        "sim_files": set(SIM_FILE_RE.findall(body)),
        "challenge_sims": set(SIM_FILE_RE.findall(section(body, "Game challenge"))),
    }


QUESTION_WORDS = {"what", "which", "who", "whose", "where", "when", "why", "how", "is", "are",
                  "was", "were", "do", "does", "did", "can", "could", "should", "would", "will",
                  "has", "have", "had", "must", "may"}


def plain(text):
    """Slide text without Markdown marks."""
    text = re.sub(r"\{\{<.*?>\}\}", " ", text)
    text = re.sub(r"[*_`]|~([^~]*)~", lambda m: m.group(1) or "", text)
    return text.strip()


def is_question(line):
    """A full question: ends with "?", and its last sentence has a question word."""
    line = plain(line)
    if not line.endswith("?") or re.search(r"(…|\.\.\.)\s*\?$", line):
        return False
    last = re.split(r"(?<=[.!;])\s+", line)[-1]
    for part in (last, last.split(":")[-1]):
        if any(w in QUESTION_WORDS for w in re.findall(r"[A-Za-z']+", part.lower())[:3]):
            return True
    return False


# Group work on a slide ("Do it together", "discuss with a classmate").
GROUP_RE = re.compile(r"\b(do|try|work|discuss|play|answer) (it |this )?together\b|classmate|\bin (pairs|groups)\b"
                      r"|\b(your (group|partner)|a partner)\b", re.I)


def check_slides(body):
    """Warnings for slides that do not explain themselves (one string each)."""
    out = []
    for part in re.split(r"^(?=## )", body, flags=re.M):
        m = re.match(r"## (.+)", part)
        if not m:
            continue
        title = m.group(1).strip()
        name = '"%s"' % title
        text = part[m.end():]
        outside = re.sub(r"^:::+ *\{\.(answer|reveal)\}.*?^:::+ *$", "", text, flags=re.M | re.S)
        has_answer = re.search(r"^:::+ *\{\.(answer|reveal)\}", text, re.M) is not None
        if len(plain(title).replace(" · ", "  ")) > 44:
            out.append("slide %s: the title is too long for one line (44 characters at most)" % name)
        if GROUP_RE.search(part):
            out.append("slide %s: group work (each student works alone; write only \"Do it:\")" % name)
        if re.search(r"(…|\.\.\.)\s*\??\s*$", outside, re.M):
            out.append("slide %s: an unfinished sentence (…)" % name)
        if title.startswith("Think"):
            out.append("slide %s: no Think slides (a question with no visible answer)" % name)
        if title.startswith("Try it"):
            if not has_answer:
                out.append("slide %s: the answer is not on the slide (::: {.answer})" % name)
            items = re.findall(r"^[a-h]\) (.+)$", outside, re.M)
            for q in items:
                if not is_question(q):
                    out.append('slide %s: not a full question: "%s"' % (name, plain(q)[:60]))
            if not items and not any(is_question(l) for l in outside.splitlines()):
                out.append("slide %s: no full question (a question word and \"?\")" % name)
        if title.startswith("Example") and "?" not in outside:
            out.append("slide %s: say what the example asks (a question before the steps)" % name)
        for sim in re.findall(r"\{\{< *sim [^>]*>\}\}", text):
            if 'layout="qr"' not in sim and "task=" not in sim:
                out.append('slide %s: the simulator has no task="…" (what to show, what to ask)' % name)
        if title.startswith("Keywords"):
            continue
        for b in re.findall(r"^\s*- (.+)$", outside, re.M):
            t = plain(b)
            if " · " in t or len(re.findall(r"[A-Za-z0-9]+", t)) < 4:
                out.append('slide %s: a fragment, write a short sentence: "%s"' % (name, t[:60]))
    return out


def front_matter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end]
    return ""


def is_online(path):
    return re.search(r"^online:\s*true\b", front_matter(path), re.M) is not None


def check_online(path, rel):
    """Warnings for an online activity (one string each)."""
    out = []
    fm = front_matter(path)
    body = read(path)
    for key in ("due", "marks"):
        if not re.search(r"^%s:" % key, fm, re.M):
            out.append("%s: online activity without `%s:` in the front matter" % (rel, key))
    heads = headings(body)
    for part in ("before you start", "tasks to submit", "how to submit"):
        if not any(h.startswith(part) for h in heads):
            out.append("%s: online activity without a \"%s\" section" % (rel, part.capitalize()))
    steps = [p for p in re.split(r"^(?=## )", body, flags=re.M) if re.match(r"## Step \d", p)]
    if not steps:
        out.append("%s: online activity without Steps (## Step 1 · … {.study})" % rel)
    for p in steps:
        title = p.splitlines()[0][3:]
        if "{.study}" not in title:
            out.append('%s: "%s" is not marked {.study} (it would be printed)' % (rel, title))
        k = len(TRY_IT_RE.findall(p))
        if k != 1:
            out.append('%s: "%s" has %d Try it boxes; give each step one self-check' % (rel, title, k))
    tasks = section(body, "Tasks to submit")
    n_tasks = len(re.findall(r"^### Task \d", tasks, re.M))
    if not (ONLINE_TASKS[0] <= n_tasks <= ONLINE_TASKS[1]):
        out.append("%s: %d tasks to submit, an online activity needs %d–%d (### Task 1 · …)" % ((rel, n_tasks) + ONLINE_TASKS))
    if "answer-space" not in tasks:
        out.append("%s: the tasks have no {{< answer-space >}} for the printed copy" % rel)
    if ".match" in tasks:
        out.append("%s: the tasks to submit show answers (.match); keep self-checks in the Steps" % rel)
    for w in graded_warnings(tasks) + ai_task_warnings(tasks, graded=True):
        out.append("%s: Tasks to submit: %s" % (rel, w))
    study = "".join(steps)
    for w in answered_warnings(study) + ai_task_warnings(body):
        out.append("%s: %s" % (rel, w))
    sims = len(re.findall(r"\{\{< *sim ", body))
    if sims < ONLINE_MIN_SIMS:
        out.append("%s: %d simulators, an online activity needs %d or more" % (rel, sims, ONLINE_MIN_SIMS))
    return out


def check_slides_seminar(body):
    """Seminar decks: a Recall slide, and a Check slide after every Activity slide."""
    out = []
    titles = re.findall(r"^## (.+)$", body, re.M)
    if not any(t.startswith("Recall") for t in titles):
        out.append("no Recall slide (questions on the earlier lectures, with .answer)")
    acts = [re.match(r"Activity (\d+)", t).group(1) for t in titles if re.match(r"Activity \d+", t)]
    checks = {re.match(r"Check (\d+)", t).group(1) for t in titles if re.match(r"Check \d+", t)}
    for a in acts:
        if a not in checks:
            out.append("Activity %s has no Check %s slide (the result, with .reveal)" % (a, a))
    for part in re.split(r"^(?=## )", body, flags=re.M):
        m = re.match(r"## (Recall|Check \d+)(.*)", part)
        if m and not re.search(r"^:::+ *\{\.(answer|reveal)\}", part, re.M):
            out.append('slide "%s%s": the answers are not on the slide (.answer or .reveal)' % (m.group(1), m.group(2)))
    return out


def check_seminar(path, rel, minutes):
    """Warnings and counts for a seminar or practice session."""
    out, n = [], {}
    body = read(path)
    heads = headings(body)
    n["activities"] = len(re.findall(r"^## Activity \d", body, re.M))
    n["questions"] = len(re.findall(r"^:   \S", body, re.M))
    n["try_its"] = len(TRY_IT_RE.findall(body))
    n["sims"] = len(re.findall(r"\{\{< *sim ", body))
    for part in SEMINAR_PAGE_REQUIRED:
        if not any(h.startswith(part) for h in heads):
            out.append("%s: no \"%s\" section" % (rel, part.capitalize()))
    for part in SEMINAR_FORBIDDEN:
        if any(h.startswith(part) for h in heads):
            out.append("%s: a seminar has no \"%s\" (two short problems; a game is the tool of an activity)" % (rel, part.capitalize()))
    times = []
    for title in re.findall(r'^:::+ *\{\.callout-note[^}\n]*title="(Activity [^"]*)"', body, re.M):
        m = re.search(r"·\s*(\d+)\s*min\b", title)
        if m:
            times.append(int(m.group(1)))
        else:
            out.append('%s: "%s" has no time ("· 15 min")' % (rel, title))
    n["minutes"] = SEMINAR_RECALL_MIN + sum(times)
    if n["minutes"] > SEMINAR_TIME[minutes]:
        out.append("%s: %d planned minutes (Recall %d + activities %s); a %d-min seminar plans at most %d, "
                   "the rest is for explaining" % (rel, n["minutes"], SEMINAR_RECALL_MIN,
                                                    " + ".join(map(str, times)), minutes, SEMINAR_TIME[minutes]))
    n_ai = sum(1 for h, _ in boxes(body) if ".ai-task" in h or 'title="Task with AI' in h)
    if n_ai > SEMINAR_AI_MAX:
        out.append("%s: %d Task with AI boxes, a seminar has at most %d (in \"At home\")" % (rel, n_ai, SEMINAR_AI_MAX))
    if "{{< glossary" in body:
        out.append("%s: a seminar adds no new terms (no glossary; reuse the lectures' words)" % rel)
    acts = [p for p in re.split(r"^(?=## )", body, flags=re.M) if re.match(r"## Activity \d", p)]
    for p in acts:
        title = p.splitlines()[0][3:]
        if not DO_IT_RE.search(p):
            out.append('%s: "%s" has no Activity box (::: {.callout-note title="Activity …"})' % (rel, title))
        k = len(TRY_IT_RE.findall(p))
        if k > 1:
            out.append('%s: "%s" has %d Try it boxes; give each activity one' % (rel, title, k))
    for w in answered_warnings(body) + ai_task_warnings(body):
        out.append("%s: %s" % (rel, w))

    book_path = path[:-4] + "-book.qmd"
    if os.path.exists(book_path):
        book = read(book_path)
        main = re.split(r"^## Answers", book, flags=re.M)[0]
        n["words"] = count_words(main)
        bheads = headings(book)
        for part in SEMINAR_BOOK_REQUIRED:
            if not any(h.startswith(part) for h in bheads):
                out.append("%s: no \"%s\" section in the worksheet" % (rel, part.capitalize()))
        for t in task_boxes_without_check(book):
            out.append('%s: worksheet: "%s" has no ::: {.check} (its result at the end)' % (rel, t))
        for w in ai_task_warnings(book):
            out.append("%s: worksheet: %s" % (rel, w))
    else:
        out.append("%s: no worksheet (%s)" % (rel, os.path.basename(book_path)))

    slides_path = path[:-4] + "-slides.qmd"
    if os.path.exists(slides_path):
        sb = read(slides_path)
        n["slides"] = count_slides(sb)["slides"]
        srel = rel[:-4] + "-slides.qmd"
        for w in check_slides(sb) + check_slides_seminar(sb):
            out.append("%s: %s" % (srel, w))
    else:
        out.append("%s: no slides file (%s)" % (rel, os.path.basename(slides_path)))

    for key, (lo, hi) in SEMINAR_SIZES[minutes].items():
        v = n.get(key)
        if v is None:
            continue
        if v < lo or (hi is not None and v > hi):
            out.append("%s: %d %s, a %d-min seminar needs %d–%d" % (rel, v, NAMES[key], minutes, lo, hi))
    return out, n


def check(project_dir):
    rows, warnings = [], []
    week = os.path.join(project_dir, "courses", "*", "week-*")
    for name in ("seminar-[0-9][0-9].qmd", "practice-[0-9][0-9].qmd"):
        for path in sorted(glob.glob(os.path.join(week, name))):
            minutes = course_minutes(project_dir, path.split(os.sep)[-3])
            if minutes not in SEMINAR_SIZES:
                continue
            rel = os.path.relpath(path, project_dir)
            w, n = check_seminar(path, rel, minutes)
            warnings.extend(w)
            rows.append((rel, minutes, n))
    for path in sorted(glob.glob(os.path.join(week, "online-[0-9][0-9].qmd"))):
        warnings.extend(check_online(path, os.path.relpath(path, project_dir)))
    for path in sorted(glob.glob(os.path.join(week, "homework-[0-9][0-9].qmd"))):
        rel = os.path.relpath(path, project_dir)
        hw = read(path)
        warnings.extend("%s: %s" % (rel, w) for w in graded_warnings(hw) + ai_task_warnings(hw, graded=True))
    pattern = os.path.join(project_dir, "courses", "*", "week-*", "lesson-[0-9][0-9].qmd")
    for path in sorted(glob.glob(pattern)):
        slug = path.split(os.sep)[-3]
        minutes = course_minutes(project_dir, slug)
        rel = os.path.relpath(path, project_dir)
        if minutes not in SIZES:
            continue
        if is_online(path):
            warnings.extend(check_online(path, rel))
            continue
        n = {}
        page = count_page(read(path))
        n.update({k: page[k] for k in ("try_its", "questions", "sims")})

        book_path = path[:-4] + "-book.qmd"
        sheet_path = path[:-4] + "-sheet.qmd"
        has_sheet = os.path.exists(sheet_path)
        if os.path.exists(book_path):
            book = count_book(read(book_path))
            n.update({"book_sections": len(book["sections"]), "words": book["words"],
                      "examples": book["examples"], "exercises": book["exercises"]})
            for part in BOOK_REQUIRED:
                if not any(h.startswith(part) for h in book["headings"]):
                    warnings.append("%s: no \"%s\" section in the notes" % (rel, part.capitalize()))
            book_sims = set(SIM_FILE_RE.findall(read(book_path)))
            for f in sorted(page["challenge_sims"] - book_sims):
                warnings.append("%s: the game %s is not in the notes (Case study)" % (rel, f))
            for sec, k in book["do_its"].items():
                if k == 0 and not has_sheet:
                    warnings.append("%s: section %s of the notes has no Do it task" % (rel, sec))
            missing = [s for s in book["sections"] if s not in page["sections"]]
            if missing:
                warnings.append("%s: sections %s of the notes are not on the page" % (rel, ", ".join(missing)))
        else:
            warnings.append("%s: no lesson notes (%s)" % (rel, os.path.basename(book_path)))

        for sec, k in page["do_its"].items():
            if k == 0:
                warnings.append("%s: section %s of the page has no Do it task" % (rel, sec))
        page_body = read(path)
        for w in answered_warnings(page_body) + ai_task_warnings(page_body):
            warnings.append("%s: %s" % (rel, w))
        if os.path.exists(book_path):
            for w in ai_task_warnings(read(book_path)):
                warnings.append("%s: notes: %s" % (rel, w))
        for sec, k in page["per_section"].items():
            if k > 1:
                warnings.append("%s: section %s has %d Try it boxes; use one question set per concept" % (rel, sec, k))

        slides_path = path[:-4] + "-slides.qmd"
        if has_sheet:
            notes_secs = sections_text(read(book_path)) if os.path.exists(book_path) else {}
            slides_body = read(slides_path) if os.path.exists(slides_path) else None
            w, n["experiments"] = check_sheet(sheet_path, rel, notes_secs, page_body, slides_body)
            warnings.extend(w)
        if os.path.exists(slides_path):
            s = count_slides(read(slides_path))
            n["slides"] = s["slides"]
            for f in sorted(page["sim_files"] - s["sim_files"]):
                warnings.append("%s: %s is on no slide (\"Live demo\" or Game challenge)" % (rel, f))
            lesson_dir = os.path.dirname(path)
            for f in sorted(s["sim_files"]):
                if not os.path.exists(os.path.join(lesson_dir, re.sub(r"\.html$", ".gif", f))):
                    warnings.append("%s: %s has no recording for the slides (shared/sims/recordings)" % (rel, f))
            for f in sorted(page["challenge_sims"] - s["challenge_sims"]):
                warnings.append("%s: the game %s is not on the Game challenge slide" % (rel, f))
            for w in check_slides(read(slides_path)):
                warnings.append("%s: %s" % (os.path.relpath(slides_path, project_dir), w))
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
    for path in sorted(glob.glob(os.path.join(week, "*.qmd"))):
        lines = read(path).split("\n")
        for i in range(1, len(lines)):
            prev = lines[i - 1].strip()
            if re.match(r"\s*:{3,}\s*\{", lines[i]) and prev and not prev.startswith(":::"):
                warnings.append("%s: a blank line is missing before \"%s\" (pandoc shows it as text)"
                                % (os.path.relpath(path, project_dir), lines[i].strip()))
    return rows, warnings


def main():
    project_dir = os.environ.get("QUARTO_PROJECT_DIR") or os.getcwd()
    rows, warnings = check(project_dir)
    if "--all" in sys.argv:
        cols = ["book_sections", "activities", "minutes", "experiments", "words", "examples", "exercises", "try_its",
                "questions", "sims", "slides"]
        short = ["sect", "activ", "plan", "exper", "words", "exmpl", "exer", "try", "quest", "sims", "slides"]
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
