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
    `task`, no fragments of one to three words, no group work ("Do it together");
    no unsolved work: a "Do it:" question has its result on the slide
    (::: {.reveal}, "Result:"), and a `task` that asks something has its
    answer= (shown on click)
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

On every page (AUTHORING.md, "The page teaches, the notes test", and "The page
checks every task"): every Do it, Lab task and Activity box ends with an
interactive check (::: {.choice}, {.order}, {.sort} or {.fill}, interact.lua)
and never with a closed {.check}; each check is complete (one right option and
a reason for every option; 3-8 cards in order with a reason; 2-4 groups and a
reason for every card; an answer= and a reason). Every Try it question has a
"Why:" reason. Graded work (homework, "Tasks to submit") never shows them.
In the notes and the worksheets (PDF) every task box keeps its {.check}: the
results are printed at the end (a self-test).
"Task with AI" boxes (an extra for the curious; AUTHORING.md, "Tasks with
AI"): at most AI_MAX per file, each with a complete {.prompt} that asks for a
visual result, what the student should see and 2-3 changes to try: on the
page as interactive checks, in the notes as closed answers. AI is never part
of graded work: in a homework a box belongs in an optional section
"## Optional · Task with AI {.extra}".

FROZEN files were sent to students and keep an older model this semester
(AUTHORING.md, "Frozen sessions"): they are listed and not checked against
the newest rules. Rewrite them at the start of the next semester.

A lecture worksheet (a practical course: lesson-NN-sheet.qmd; AUTHORING.md,
"Lecture worksheets") is the main document of the session. It needs "Before
you start", one experiment per section of the notes (## Experiment N · …,
with an "Aim:"), SHEET_STEPS numbered steps in each, a {{< record >}} field
and a ::: {.check} after every step, a "Table of results" (::: {.record-table})
and its start files in files/. The page shows every experiment in its section
({{< experiment N >}}, which counts as the section's task), each section of
the notes points to its experiment, and the slides have a "Your worksheet" and
a "Results of the worksheet" slide. An experiment with Part A ({.part}, in the
app) has a Part B (on a simulator or the phone), and no part gives minutes.

A lecture page is taught in class on the smart screen (since 2026-11-08):
page_minutes() estimates its class time (PAGE_TIME_COST), at most PAGE_TIME;
the pages of HOME_PAGES (taught before the screens) keep the older sizes.

An online activity (blended course: online-NN.qmd, or an older lesson-NN.qmd
with `online: true`) has no notes and no slides. It is checked for its own parts (AUTHORING.md, "Blended
courses"): "Before you start", Steps marked {.study} with one "Try it" each,
"Tasks to submit" ({.tasks}) with answer space, "How to submit", `due:` (no
marks anywhere) and a content type (`content:`), which decides what the Steps
need: sims, a simulator in every Step; mix, at least one simulator; video, a
{{< watch >}} of an official video with its source, length and the date the
link was checked; course-video, the video made for the course with its
captions, poster and script, the captions the same words as the script.

Answers without written English (AUTHORING.md): homework, tasks to submit
and worksheet records never ask for English text (ESSAY_RE: "explain",
"why?", "give the reason", "write a sentence", …; a record "because …" or
lines=3+), and homework and online activities name no marks (MARKS_RE).

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
# The page sizes (try_its, questions) are for a page taught in class (PAGE_TIME).
SIZES = {
    60: {
        "book_sections": (3, 4),
        "words": (0, 3500),
        "examples": (2, None),
        "exercises": (6, 10),
        "try_its": (4, 6),
        "questions": (8, 16),
        "sims": (0, 4),
        "slides": (10, 16),
    },
    90: {
        "book_sections": (4, 7),
        "words": (0, 6000),
        "examples": (4, None),
        "exercises": (10, 16),
        "try_its": (6, 9),
        "questions": (18, 28),
        "sims": (1, 3),
        "slides": (20, 28),
    },
}
# The page is taught in class (AUTHORING.md, "The page is taught in class"):
# since 2026-11-08 the teacher teaches from the interactive page on the smart
# screen of the classroom, so a lecture page fits about 40 minutes of a 60-min
# lecture and about 65 of a 90-min lecture; the rest of the lecture is for the
# students' questions and the delays of a real class. The planned minutes are
# estimated from what the page shows (PAGE_TIME_COST): the explanation is read
# on the screen and explained in Arabic, the class answers every check and
# every Try it question, and the teacher shows every simulator and runs every
# AI prompt. A Task with AI box is an extra (shown when time is left): not
# counted.
PAGE_TIME = {60: 40, 90: 65}
PAGE_TIME_COST = {
    "start": 2,        # open the page, its first lines and the summary
    "term": 0.2,       # each term of the glossary
    "wpm": 40,         # words of explanation per minute (on the screen, explained in Arabic)
    "check": 1,        # each interactive check of a task (choice, order, sort, fill)
    "question": 1,     # each Try it question
    "sim": 2,          # each simulator or mini-game shown on the screen
    "prompt": 2,       # each AI prompt run on the screen (copy, paste, read the answer)
}
# Lectures taught before the smart screens keep their home-study page this
# semester: the older page sizes (HOME_SIZES) and no class time. Rewrite them
# for class at the start of the next semester, then empty this set.
HOME_PAGES = {
    "courses/game-math/week-01/lesson-01.qmd",
    "courses/game-math/week-02/lesson-02.qmd",
    "courses/computing-systems/week-01/lesson-01.qmd",
    "courses/computing-systems/week-02/lesson-02.qmd",
    "courses/computing-systems/week-03/lesson-03.qmd",
    "courses/digital-media/week-01/lesson-01.qmd",
    "courses/digital-media/week-02/lesson-02.qmd",
}
HOME_SIZES = {
    60: {"try_its": (4, 6), "questions": (15, 28)},
    90: {"try_its": (6, 9), "questions": (30, 45)},
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
# Try it questions on the page of a lecture with a worksheet: its experiments
# have a check after every step, so one or two questions per section are enough.
SHEET_QUESTIONS = (4, 12)
# Online activity (blended course): at least this many simulators, and
# (min, max) tasks to submit.
ONLINE_CONTENT = ("lesson", "sims", "mix", "video", "course-video")
WATCH_RE = re.compile(r"\{\{<\s*watch\s+(.*?)>\}\}", re.S)
ONLINE_TASKS = (2, 4)
# Sessions sent to students before a rule changed keep their older model this
# semester (AUTHORING.md, "Frozen sessions"): they are listed, not checked.
# Rewrite them with the newest rules at the start of the next semester, then
# empty this set.
FROZEN = {
    # Digital Skills, fall 2026: Lecture 1 and Online activity 1 (with its
    # tasks PDF) were sent to the students before the page checked every task.
    "courses/digital-skills/week-01/lesson-01.qmd",
    "courses/digital-skills/week-01/online-01.qmd",
    # The homework of the units taught before 2026-11-08 was given with
    # written answers ("Why?", "Give the reason"); it keeps them this semester.
    "courses/game-math/week-01/homework-01.qmd",
    "courses/game-math/week-02/homework-02.qmd",
    "courses/computing-systems/week-01/homework-01.qmd",
    "courses/computing-systems/week-02/homework-02.qmd",
    "courses/computing-systems/week-03/homework-03.qmd",
    "courses/digital-media/week-01/homework-01.qmd",
    "courses/digital-media/week-02/homework-02.qmd",
}
# Interactive checks of the page (interact.lua): (min, max) options of a
# choice, cards of an order, groups and cards of a sort.
IC_RE = re.compile(r"^\s*:{3,}\s*\{[^}\n]*\.(choice|order|sort|fill)\b", re.M)
# A whole page check (no nested divs inside): its fence, its text and its
# closing fence at the same indentation.
# The start of a list item ("1. ", "b) ", "(a) ", "- "): a line of a check
# that starts like this is read as a list, not as text.
LIST_START_RE = re.compile(r"^\s*(\d+[.)]|[a-zA-Z][.)]|\([a-zA-Z0-9]+\)|[-*+])\s")
IC_BLOCK_RE = re.compile(r"^([ \t]*):{3,}\s*\{[^}\n]*\.(choice|order|sort|fill)\b[^\n]*\n.*?^\1:{3,}[ \t]*$",
                         re.M | re.S)
# Answers without written English (AUTHORING.md, "Answers without written
# English"): graded tasks and worksheet records ask for a choice, an order, a
# number, a name or a few words, never for English text to write.
ESSAY_RE = re.compile(r"\b(explain|describe|discuss|justify|in your own words|in (?:one|a|two) (?:short )?sentences?"
                      r"|write (?:a|one|two|three|your|some) (?:short )?(?:sentences?|paragraphs?|e-?mails?|texts?"
                      r"|reasons?|prompts?|stor(?:y|ies)|advice)|write (?:a|one|your) (?:short |formal )?letter\b"
                      r"|give (?:a|the|one|your) reasons?|and why\b|why\?|\bwhy (?:do|does|did|is|are|was|were|must|should|can|not)\b)", re.I)
# No marks or grades on homework and online activities (the teacher's request
# of 2026-11-08): the e-learning platform keeps the grades.
MARKS_RE = re.compile(r"\b\d+(?:\.\d+)?\s+marks?\b|\bmarks? (?:them|each|per)\b|\(no marks\)|\bno marks\b", re.I)
CHOICE_OPTIONS = (2, 4)
ORDER_CARDS = (3, 8)
SORT_GROUPS = (2, 4)
SORT_CARDS = (3, 8)
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
GLOSSARY_RE = re.compile(r"\{\{<\s*glossary\s+([^>]*?)\s*>\}\}")


def drop_divs(text, classes):
    """The text without the fenced divs ({.check}, …) of the given classes,
    at any indentation (the closing fence has the indentation of the opening one)."""
    out, skip = [], None
    for line in text.split("\n"):
        if skip is not None:
            m = re.match(r"^(\s*):{3,}\s*$", line)
            if m and len(m.group(1)) == skip:
                skip = None
            continue
        m = re.match(r"^(\s*):{3,}\s*\{\.(%s)\b" % "|".join(classes), line)
        if m:
            skip = len(m.group(1))
            continue
        out.append(line)
    return "\n".join(out)


def experiment_on_page(sheet_body, n):
    """What {{< experiment n >}} shows on the page (shortcodes.lua): the steps
    and their checks, without "The idea:", the record fields, the closed
    results and the simulators (they are in the section of the page)."""
    m = re.search(r"^## Experiment %s\b[^\n]*\n(.*?)(?=^## |\Z)" % n, sheet_body, re.M | re.S)
    if not m:
        return ""
    t = re.sub(r"^\*\*The idea[^\n]*(\n[^\n]+)*", " ", m.group(1), flags=re.M)
    t = re.sub(r"\{\{<\s*(record|sim)\b.*?>\}\}", " ", t, flags=re.S)
    return drop_divs(t, ["check"])


def page_minutes(path, page_body):
    """The planned class minutes of a lecture page (PAGE_TIME_COST)."""
    c = PAGE_TIME_COST
    body = page_body
    sheet = path[:-4] + "-sheet.qmd"
    if os.path.exists(sheet):
        st = read(sheet)
        body = re.sub(r"^\{\{< *experiment (\d+) *>\}\}", lambda m: experiment_on_page(st, m.group(1)),
                      body, flags=re.M)
    # A Task with AI box is an extra, shown only when time is left.
    for head, text in boxes(body):
        if ".ai-task" in head or 'title="Task with AI' in head:
            body = body.replace(text, " ")
    terms = sum(len(g.split()) for g in GLOSSARY_RE.findall(body))
    questions = count_questions(body)
    checks = len(IC_RE.findall(body))
    sims = len(re.findall(r"\{\{< *sim ", body))
    prompts = len(re.findall(r"^\s*:{3,} *\{\.prompt\}", body, re.M))
    # The first lines and the summary are in "start".
    parts = re.split(r"^(?=## )", body, flags=re.M)
    explained = "".join(p for p in parts if p.startswith("## ") and not re.match(r"## Summary\b", p))
    explained = IC_BLOCK_RE.sub(" ", explained)
    # The words of a prompt are in its "prompt" minutes (copied, not explained).
    explained = drop_divs(explained, ["prompt"])
    words = max(0, count_words(explained) - count_words(try_it_text(explained)))
    minutes = (c["start"] + c["term"] * terms + words / c["wpm"] + c["check"] * checks
               + c["question"] * questions + c["sim"] * sims + c["prompt"] * prompts)
    return int(round(minutes))


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
    """Every fenced div: (opening line, its text up to the closing fence).

    Divs may be indented (inside a numbered step of a worksheet); the text
    then loses the indentation of its opening line."""
    out, stack = [], []
    lines = body.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(\s*)(:{3,})\s*(\S.*)?$", line)
        if not m:
            continue
        if m.group(3):
            stack.append((i, line, len(m.group(1))))
        elif stack:
            start, head, ind = stack.pop()
            text = [l[ind:] if l[:ind].strip() == "" else l for l in lines[start + 1:i]]
            out.append((head, "\n".join(text)))
    return out


def task_boxes_without_check(body):
    """Titles of Do it / Lab task / Activity / Task with AI boxes that have no {.check}."""
    out = []
    for head, text in boxes(body):
        m = re.search(r'\{\.callout-note[^}]*title="((%s)[^"]*)"' % TASK_TITLES, head)
        if m and not re.search(r"^\s*:::+ *\{\.check\}", text, re.M):
            out.append(m.group(1))
    return out


def task_boxes_without_ic(body):
    """Titles of Do it / Lab task / Activity / Task with AI boxes without an interactive check."""
    out = []
    for head, text in boxes(body):
        m = re.search(r'\{\.callout-note[^}]*title="((%s)[^"]*)"' % TASK_TITLES, head)
        if m and not IC_RE.search(text):
            out.append(m.group(1))
    return out


def try_it_text(body):
    """The text of the "Try it" boxes only (their questions and answers)."""
    return "\n".join(text for head, text in boxes(body)
                     if re.search(r'\{\.callout-tip[^}]*title="Try it', head))


def count_questions(body):
    """Questions in the Try it boxes (`:   answer` lines)."""
    return len(re.findall(r"^:   \S", try_it_text(body), re.M))


def ic_warnings(body):
    """Warnings for the interactive checks of a page (interact.lua), one string each."""
    out = []
    for head, text in boxes(body):
        m = re.match(r"^\s*:{3,}\s*\{[^}\n]*\.(choice|order|sort|fill)\b", head)
        if not m:
            continue
        kind = m.group(1)
        lines = text.splitlines()
        first = next((l.strip() for l in lines if l.strip()), "")
        name = '%s check "%s"' % (kind, first[:45])
        if kind == "choice":
            items = re.split(r"^- \[[ xX]\] ", text, flags=re.M)
            marks = re.findall(r"^- \[([ xX])\] ", text, re.M)
            if not CHOICE_OPTIONS[0] <= len(marks) <= CHOICE_OPTIONS[1]:
                out.append("%s: %d options; give %d–%d (- [x] right, - [ ] wrong)" % ((name, len(marks)) + CHOICE_OPTIONS))
            if sum(1 for x in marks if x in "xX") != 1:
                out.append("%s: needs exactly one right option (- [x])" % name)
            missing = sum(1 for it in items[1:] if not re.search(r"^\s+Why:", it, re.M))
            if missing:
                out.append("%s: %d option(s) without a Why: (why it is right, or why it is wrong)" % (name, missing))
        elif kind == "order":
            cards = re.findall(r"^\d+\. \S", text, re.M)
            if not ORDER_CARDS[0] <= len(cards) <= ORDER_CARDS[1]:
                out.append("%s: %d cards; give %d–%d in the right order (1. … 2. …)" % ((name, len(cards)) + ORDER_CARDS))
            if not re.search(r"^Why:", text, re.M):
                out.append("%s: no Why: after the list (why this is the order)" % name)
        elif kind == "sort":
            groups, cards, why = 0, 0, 0
            for k, l in enumerate(lines):
                if l.startswith(":   "):
                    cards += 1
                    nxt = []
                    for l2 in lines[k + 1:]:
                        if l2.startswith(":") or (l2.strip() and not l2.startswith(" ")):
                            break
                        nxt.append(l2)
                    if any(x.strip().startswith("Why:") for x in nxt):
                        why += 1
                elif l.strip() and not l.startswith(" ") and k + 1 < len(lines) and lines[k + 1].startswith(":   "):
                    groups += 1
                    if LIST_START_RE.match(l):
                        out.append('%s: the group "%s" starts like a list item, so it is read as a list; '
                                   'write it as "Question 1 · …"' % (name, l.strip()[:40]))
            if not SORT_GROUPS[0] <= groups <= SORT_GROUPS[1]:
                out.append("%s: %d groups; give %d–%d" % ((name, groups) + SORT_GROUPS))
            if not SORT_CARDS[0] <= cards <= SORT_CARDS[1]:
                out.append("%s: %d cards; give %d–%d" % ((name, cards) + SORT_CARDS))
            if why < cards:
                out.append("%s: %d card(s) without a Why:" % (name, cards - why))
        else:
            if not re.search(r'answer="[^"]+"', head):
                out.append('%s: no answer="…" (the right answers, split by "|")' % name)
            if not re.search(r"^Why:", text, re.M):
                out.append("%s: no Why: (the reason, shown with the answer)" % name)
    return out


def questions_without_why(body):
    """The answers (`:   answer`) of Try it questions that have no "Why:" reason."""
    out = []
    lines = try_it_text(body).splitlines()
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


def ai_task_warnings(body, graded=False, page=False):
    """Warnings for the "Task with AI" boxes of one file.

    On a page (page=True) what the student should see and every change to try
    are interactive checks; in the notes they are closed answers ({.check})."""
    out = []
    ai = [(h, t) for h, t in boxes(body) if ".ai-task" in h or 'title="Task with AI' in h]
    if len(ai) > AI_MAX:
        out.append("%d Task with AI boxes, at most %d (only where AI lets students do more)" % (len(ai), AI_MAX))
    for head, text in ai:
        title = (re.search(r'title="([^"]*)"', head) or re.search(r"(.*)", head)).group(1)
        if graded:
            # AI is always an extra: never in graded tasks.
            out.append('Task with AI "%s" is in graded work; put it after the tasks, in an optional '
                       '"## Optional · Task with AI {.extra}" section' % title)
            continue
        prompt = re.search(r"^\s*:::+ *\{\.prompt\}\n(.*?)^\s*:::+\s*$", text, re.M | re.S)
        if not prompt:
            out.append('Task with AI "%s" has no ::: {.prompt}' % title)
        # An extra for the curious (AUTHORING.md, "Tasks with AI"): a complete
        # prompt with a visual result, what you should see, and changes to try,
        # each with its closed answer.
        if prompt:
            words = prompt.group(1)
            if re.search(r"\[[^\]]*\]|…|\.\.\.|:\s*$|\badd your\b|\byour (premise|points|rule|notes)\b", words, re.I):
                out.append('Task with AI "%s": the prompt is not complete (no brackets, "…" or "add your …": '
                           'give every detail, ready to copy)' % title)
            if not re.search(r"\b(draw|picture|diagram|chart|graph|grid|map|table|plot|web page|timeline)\b", words, re.I):
                out.append('Task with AI "%s": the prompt asks for no visual result (a picture, diagram, chart, '
                           'table or small web page)' % title)
        changes = re.findall(r"^\s*:::+ *\{\.try-change\}(.*?)(?=^\s*:::+ *\{\.try-change\}|\Z)", text, re.M | re.S)
        if not 2 <= len(changes) <= 3:
            out.append('Task with AI "%s" has %d changes to try (::: {.try-change}); give 2 or 3' % (title, len(changes)))
        answer = IC_RE if page else re.compile(r"^\s*:::+ *\{\.check", re.M)
        for c in changes:
            if not answer.search(c):
                out.append('Task with AI "%s": a change to try has no %s' % (title, "interactive check (::: {.choice} inside it)"
                                                                            if page else "closed answer (::: {.check} inside it)"))
        before = re.split(r"^\s*:::+ *\{\.try-change\}", text, flags=re.M)[0]
        if not answer.search(before):
            out.append('Task with AI "%s" does not say what the student should see (%s after the prompt)'
                       % (title, "::: {.choice}: which result is right" if page
                          else '::: {.check label="What you should see"}'))
    return out


def answered_warnings(body):
    """Warnings for a page: tasks the page does not check, closed self-checks,
    incomplete interactive checks, questions without reasons."""
    out = []
    for t in task_boxes_without_ic(body):
        out.append('"%s" has no interactive check (::: {.choice}, {.order}, {.sort} or {.fill}): '
                   "the page checks every task at once" % t)
    closed = len(re.findall(r"^\s*:::+ *\{\.check\b", body, re.M))
    if closed:
        out.append('%d closed "Check your result" box(es) (::: {.check}); on the page every task is checked '
                   "at once with an interactive check (the notes keep {.check})" % closed)
    out.extend(ic_warnings(body))
    missing = questions_without_why(body)
    if missing:
        out.append("%d Try it question(s) without a Why: reason (first: \"%s\")" % (len(missing), missing[0][:40]))
    return out


def graded_warnings(text):
    """Graded work (homework, Tasks to submit) never shows answers."""
    out = []
    if re.search(r"^:::+ *\{\.check\}", text, re.M):
        out.append("graded tasks show a result (::: {.check}); keep solutions in courses-private")
    if IC_RE.search(text):
        out.append("graded tasks have an interactive check (it shows the answer); keep solutions in courses-private")
    if re.search(r"^\s+Why:", text, re.M):
        out.append("graded tasks show a reason (Why:); keep solutions in courses-private")
    m = MARKS_RE.search(text)
    if m:
        out.append('the tasks name marks ("%s"); homework and online tasks show no marks' % m.group(0))
    # A ready prompt ({.prompt}) is copied, not written: its words do not count;
    # neither does a question answered with a letter ("Write A or B. (A) …").
    plain_text = drop_divs(re.sub(r"<!--.*?-->", " ", text, flags=re.S), ["prompt"])
    plain_text = "\n\n".join(p for p in re.split(r"\n\s*\n", plain_text)
                             if not re.search(r"\(A\)|\*\*A\.\*\*|Choose A, B", p))
    for m in ESSAY_RE.finditer(plain_text):
        out.append('a task asks for written English ("%s"): ask for a choice, an order, a number, '
                   "a name or a few words" % m.group(0))
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
            for label, more in re.findall(r'\{\{<\s*record\s+"([^"]*)"([^>]*)>\}\}', st):
                lines = re.search(r"lines=(\d+)", more)
                if re.search(r"\bbecause\b|\bin my (own )?words\b|\bwhy\b", label, re.I) or (lines and int(lines.group(1)) >= 3):
                    out.append('%s: "%s", step %d records a sentence ("%s"): record a value, a name, a word '
                               "or a tick (AUTHORING.md, \"Answers without written English\")" % (srel, title, i, label))
            if "{{< record" not in st:
                out.append('%s: "%s", step %d has no {{< record … >}} (a place for the result)' % (srel, title, i))
            if not re.search(r"^\s*:::+ *\{\.check\}", st, re.M):
                out.append('%s: "%s", step %d has no ::: {.check} (its result)' % (srel, title, i))
            if not IC_RE.search(st):
                out.append('%s: "%s", step %d has no interactive check for the page (::: {.choice}, '
                           "{.order}, {.sort} or {.fill} after its {.check})" % (srel, title, i))
        for w in ic_warnings(p):
            out.append("%s: %s" % (srel, w))
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
    main = IC_BLOCK_RE.sub(" ", main)   # the page checks are not in the PDF
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
    for p in exps:
        title = p.splitlines()[0][3:].strip()
        if re.search(r"\b\d+\s*(min|minutes)\b", p.split("\n1. ")[0]):
            out.append('%s: "%s" gives the minutes of a part; only the whole session has a length' % (srel, title))
        if "{.part}" in p and not re.search(r"Part B", p):
            out.append('%s: "%s" has Part A but no Part B (a step on a simulator or the phone)' % (srel, title))
    if slides_body is not None:
        # The slides are a reference of the lecture (AUTHORING.md, "Lecture
        # worksheets"): the worksheet and its results are on two slides.
        srel_s = rel[:-4] + "-slides.qmd"
        titles = re.findall(r"^## (.+)$", slides_body, re.M)
        if not any(t.startswith("Your worksheet") for t in titles):
            out.append('%s: no "Your worksheet" slide (Part A, Part B, the start files and {{< page-qr >}})' % srel_s)
        if not any(t.startswith("Results of the worksheet") for t in titles):
            out.append('%s: no "Results of the worksheet" slide (one .reveal line for each experiment)' % srel_s)
        for part in re.split(r"^(?=## )", slides_body, flags=re.M):
            m = re.match(r"## (Results of the worksheet.*)", part)
            if m and not re.search(r"^:::+ *\{\.(answer|reveal)\}", part, re.M):
                out.append('%s: slide "%s": the results are not on the slide (.reveal or .answer)'
                           % (srel_s, m.group(1).strip()))
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
        "questions": count_questions(body),
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
        # No unsolved work on a slide: a Do it question shows its result on a
        # click (a seminar's Activity slide and a worksheet's Experiment slide
        # have their results on the Check slide after them).
        if (re.search(r"^\s*- \*\*Do it:\*\*", outside, re.M) and not has_answer
                and not re.match(r"(Activity|Experiment) \d", title)):
            out.append('slide %s: the Do it task has no result on the slide (::: {.reveal} with '
                       '"**Result:** …" or "**Example:** …" under it, in the same column)' % name)
        for sim in re.findall(r"\{\{< *sim [^>]*>\}\}", text):
            if 'layout="qr"' not in sim and "task=" not in sim:
                out.append('slide %s: the simulator has no task="…" (what to show, what to ask)' % name)
            if re.search(r"\*\*Ask:\*\*|\?", re.search(r'task="([^"]*)"', sim).group(1) if "task=" in sim else "") \
                    and "answer=" not in sim:
                out.append('slide %s: the simulator task asks something but has no answer="…" (shown on a click)' % name)
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
    if not re.search(r"^due:", fm, re.M):
        out.append("%s: online activity without `due:` in the front matter" % rel)
    if re.search(r"^marks:", fm, re.M):
        out.append("%s: `marks:` in the front matter; online activities show no marks" % rel)
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
    for w in answered_warnings(study) + ai_task_warnings(body, page=True):
        out.append("%s: %s" % (rel, w))
    m = re.search(r"^content:\s*\"?([\w-]+)", fm, re.M)
    content = m.group(1) if m else ""
    if content not in ONLINE_CONTENT:
        out.append("%s: online activity without a content type (`content:` %s)" % (rel, ", ".join(ONLINE_CONTENT)))
    sims = len(re.findall(r"\{\{< *sim ", body))
    watches = [dict(re.findall(r'(\w+)="([^"]*)"', a)) for a in WATCH_RE.findall(body)]
    if content == "sims":
        for p in steps:
            if not re.search(r"\{\{< *sim ", p):
                out.append('%s: "%s" has no simulator; every Step of a sims activity has one' % (rel, p.splitlines()[0][3:]))
    elif content == "mix" and sims == 0:
        out.append("%s: a mix activity has no simulator (text steps and simulator steps)" % rel)
    elif content == "video":
        links = [w for w in watches if w.get("url")]
        if not links:
            out.append("%s: a video activity without an official video ({{< watch url=… >}})" % rel)
        for w in links:
            for key in ("title", "source", "length", "checked"):
                if not w.get(key):
                    out.append('%s: the video "%s" has no %s= (title, source, length and the date checked)'
                               % (rel, w.get("title", w["url"]), key))
    elif content == "course-video":
        videos = [w for w in watches if w.get("file")]
        if not videos:
            out.append("%s: a course-video activity without its video ({{< watch file=… >}})" % rel)
        here = os.path.dirname(path)
        for w in videos:
            for key in ("file", "captions", "poster", "script"):
                if not w.get(key):
                    out.append('%s: the course video "%s" has no %s=' % (rel, w.get("title", w["file"]), key))
                elif not os.path.exists(os.path.join(here, w[key])):
                    out.append("%s: the %s %s of the course video is missing" % (rel, key, w[key]))
            vtt, script = os.path.join(here, w.get("captions", "")), os.path.join(here, w.get("script", ""))
            if w.get("captions") and w.get("script") and os.path.exists(vtt) and os.path.exists(script):
                cues = [l.strip() for l in read(vtt).splitlines()
                        if l.strip() and l.strip() != "WEBVTT" and "-->" not in l and not l.strip().isdigit()]
                lines = [l.strip() for l in read(script).splitlines() if l.strip()]
                if cues != lines:
                    out.append("%s: the captions %s are not the words of the script %s (the voice reads the script)"
                               % (rel, w["captions"], w["script"]))
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
    n["questions"] = count_questions(body)
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
    for w in answered_warnings(body) + ai_task_warnings(body, page=True):
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


def is_frozen(rel):
    return rel.replace(os.sep, "/") in FROZEN


def check(project_dir):
    rows, warnings = [], []
    week = os.path.join(project_dir, "courses", "*", "week-*")
    for name in ("seminar-[0-9][0-9].qmd", "practice-[0-9][0-9].qmd"):
        for path in sorted(glob.glob(os.path.join(week, name))):
            minutes = course_minutes(project_dir, path.split(os.sep)[-3])
            if minutes not in SEMINAR_SIZES:
                continue
            rel = os.path.relpath(path, project_dir)
            if is_frozen(rel):
                continue
            w, n = check_seminar(path, rel, minutes)
            warnings.extend(w)
            rows.append((rel, minutes, n))
    for path in sorted(glob.glob(os.path.join(week, "online-[0-9][0-9].qmd"))):
        rel = os.path.relpath(path, project_dir)
        if not is_frozen(rel):
            warnings.extend(check_online(path, rel))
    for path in sorted(glob.glob(os.path.join(week, "homework-[0-9][0-9].qmd"))):
        rel = os.path.relpath(path, project_dir)
        if is_frozen(rel):
            continue
        hw = read(path)
        # An optional section {.extra} (a Task with AI, not graded) is not graded work.
        parts = re.split(r"^(?=## )", hw, flags=re.M)
        extra = "".join(p for p in parts if re.match(r"## .*\{\.extra\}", p))
        graded = "".join(p for p in parts if not re.match(r"## .*\{\.extra\}", p))
        warnings.extend("%s: %s" % (rel, w) for w in graded_warnings(graded) + ai_task_warnings(graded, graded=True)
                        + ai_task_warnings(extra, page=True) + ic_warnings(extra))
        if re.search(r"^marks:", front_matter(path), re.M):
            warnings.append("%s: `marks:` in the front matter; homework shows no marks" % rel)
    pattern = os.path.join(project_dir, "courses", "*", "week-*", "lesson-[0-9][0-9].qmd")
    for path in sorted(glob.glob(pattern)):
        slug = path.split(os.sep)[-3]
        minutes = course_minutes(project_dir, slug)
        rel = os.path.relpath(path, project_dir)
        if minutes not in SIZES or is_frozen(rel):
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
        for w in answered_warnings(page_body) + ai_task_warnings(page_body, page=True):
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

        sizes = dict(SIZES[minutes])
        if has_sheet:
            # The checks of the experiments practise the ideas too: fewer Try it questions.
            sizes["questions"] = SHEET_QUESTIONS
        home = rel.replace(os.sep, "/") in HOME_PAGES
        if home:
            # Taught before the smart screens: the older home-study page.
            sizes.update(HOME_SIZES[minutes])
        else:
            n["minutes"] = page_minutes(path, page_body)
            if n["minutes"] > PAGE_TIME[minutes]:
                warnings.append("%s: about %d minutes in class (the page is taught on the screen); a %d-min "
                                "lecture plans at most %d, the rest is for questions and delays (AUTHORING.md, "
                                "\"The page is taught in class\")" % (rel, n["minutes"], minutes, PAGE_TIME[minutes]))
        for key, (lo, hi) in sizes.items():
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
    if FROZEN:
        print("Frozen this semester, not checked (AUTHORING.md, \"Frozen sessions\"; rewrite them next semester): "
              + ", ".join(sorted(FROZEN)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
