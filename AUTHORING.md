# Authoring rules for all courses

Owner: Mohanad Hamed, Lecturer, Mobile Game Development and Design diploma,
Technical College, Al-Israa University (Jordan). Never write "Dr." anywhere.

This public repo holds the lesson materials for **all** courses I teach.
Site: <https://mohanadhamed.github.io/courses/> (Quarto website → GitHub Pages).

## Courses

Program: Mobile Game Development and Design, Intermediate University Degree
(Diploma), code L6, Technical College. Both courses are year 1, semester 1.

| Slug | Official course name | Code | Credit hours | Per week (as taught) |
|---|---|---|---|---|
| `game-math` | Mathematics and Computing for Digital Games | 13411131 | 3 | 2 lectures × **90 min** |
| `computing-systems` | Fundamentals of Computing Systems and Digital Platforms | 13411133 | 2 | 2 lectures × **60 min** |

**One lecture = one lesson. Every course has 2 lessons per week.**
16 weeks: week 8 midterm, week 16 final. Use the official course names exactly.

### Mapping the syllabus week to the 2 lessons

- `game-math`: syllabus has First Lecture + Second Lecture + Seminar.
  Lesson A = First Lecture, Lesson B = Second Lecture. Fold the seminar
  activity into the lessons as a "Class activity" (there is no separate seminar session).
- `computing-systems`: syllabus has Lecture + Seminar.
  Lesson A = Lecture topic, Lesson B = Seminar topic (hands-on, practice).
- Exam sessions (midterm, final) get no lesson. Revision sessions get a
  revision lesson. Confirm with me when a syllabus week is unclear.

### Size every lesson for its lecture time

All three outputs (interactive lesson, PDF, slides) cover exactly one lecture.

| | 60-min lesson (`computing-systems`) | 90-min lesson (`game-math`) |
|---|---|---|
| Main ideas | 2–3 | 3–5 |
| "Try it" exercises | 3–4 | 5–7 |
| Simulators / demos | 0–1 | 1–2 |
| Class activity | ~10 min | ~15–20 min |
| Slides (incl. question slides) | ~12–16 | ~18–24 |

Leave time for my Arabic explanation and questions; do not fill every minute with content.
Course-specific notes: `courses/<slug>/NOTES.md`. Topic map: `courses/<slug>/plan.md`.

## Source of truth: the Google Drive folder (private, never copy into this repo)

The Google Drive folder **الكلية التقنية** → `02-الأقسام-الأكاديمية/01-قسم-تطوير-ألعاب-الموبايل/`
is the **source of truth** for the Mobile Game Development diploma:
study plan, guidance plan, course descriptions, and
`06-خطط-المواد-ومصفوفات-مخرجات-التعلم/` (English syllabi with weekly topics,
ILO–PLO matrix). Use the newest version of each file.

- **Before creating any lesson, read the course syllabus and ILO–PLO matrix
  from Drive** (Google Drive connector). Base the lesson on that week's topics and ILOs.
- If the Drive and this repo disagree, the Drive wins: update `_metadata.yml`,
  `plan.md` or these rules, and tell me.
- Copy only ILO text into `_metadata.yml`; never commit the documents themselves.

## ILOs and PLOs

- ILO codes follow the syllabus: A1, A2 (knowledge), B1, B2 (intellectual),
  C1, C2 (subject skills), D1 (transferable).
- Official ILO text (with PLO numbers) lives in `courses/<slug>/_metadata.yml`
  under `course.ilos`. Lessons list codes only: `ilos: [A1, B1]`.
  An unknown code is a render error.
- Program PLOs: 1 game programming and development; 2 creative development,
  player experience and UI; 3 industry trends, modern technologies and
  professional development; 4 industry management and quality assurance.
- **Lessons are built from ILOs.** Pick the ILOs from the syllabus week, then
  design ideas, examples and "Try it" exercises that build exactly those ILOs.
- PLOs connect to lessons **through** the ILOs (ILO → PLO in the matrix).
  Do not target PLOs directly, but do not ignore them: choose examples that
  serve the PLO behind each ILO (e.g. PLO 1 → real game programming and
  engine situations; PLO 2 → player experience; PLO 4 → testing and quality).

## Students

- Diploma students, weak English, weak math (Tawjihi ~50–60%).
- I explain in Arabic in class. All written material is in **very simple English**.
- Simple and practical, never academic.
- No programming yet: *Programming Fundamentals (1)* (C#) is in semester 2.
  In semester-1 courses, code is a short C# "just read it" example,
  never a task. The program uses C#, Unity and mobile (Android/iOS).
- **Do not assume students know a game engine.** Unity has its own course in
  semester 3. Do not teach engine parts (Inspector, Transform, GameObject, …).
  Connect math to **game programming / game code** in general words, and name
  Unity only as an example in brackets: "C#, the language of many games
  (for example, games made with Unity)". Explain every code word you show
  (e.g. "`Vector3` means three numbers together").

## Writing rules (always enforce)

- English CEFR A2–B1: short sentences, one idea per sentence, active voice.
- Simple verbs: use, find, move, show, change — not utilize, determine, obtain.
- **Picture before formula**: game example → diagram → then math or code.
- Short graded exercises ("Try it") **after each idea**, easy → harder.
  Every "Try it" is a matching exercise (see "Try it: match the answer").
- Every lesson starts with a bilingual glossary of 5–10 terms.
- Every lesson lists the course ILOs it covers (`ilos:` codes, from the syllabus week).
- Each lesson ends with a short "Class activity" sized for the lecture time.
  In `game-math`, take it from the syllabus seminar of that week.
- Slides: keywords and visuals only. No long sentences. Question slides may
  have one short question (see "Interactive slides").

## Glossary

- Master list: `shared/glossary.yml` (`key: {en, ar, def}`).
- Insert with `{{< glossary key1 key2 ... >}}`. A missing key is a render error
  — add the term to `glossary.yml` first, never inline.
- Same English term and same Arabic translation for a concept everywhere.
  Check `glossary.yml` before adding; reuse existing keys.

## Three outputs per lesson

Folder: `courses/<slug>/week-NN/`. Two lessons per week; lesson numbers run
across the course (week 1 → lessons 01–02, week 2 → 03–04, …).
Static diagrams go in `week-NN/images/`.

| File | Format | Output |
|---|---|---|
| `lesson-NN.qmd` | `lesson-html` + `lesson-typst` | Interactive HTML page + printable PDF |
| `lesson-NN-slides.qmd` | `lesson-pptx` | Teacher slides (.pptx) |
| `homework-NN.qmd` (NN = week) | `lesson-html` | Take-home task page with a Print button (no PDF) |

- Start from `shared/templates/lesson-template.qmd`, `slides-template.qmd`
  and `homework-template.qmd`.
- Formats, styles and filters live in the Quarto extension `_extensions/lesson/`
  (Quarto requires `_extensions/` at the project root). Change look and
  behaviour there, once, for every course.
- The `lesson-html`/`lesson-typst` formats add the course banner (course name,
  diploma line, week, lesson, ILOs) automatically from metadata. Course name and
  code come from `courses/<slug>/_metadata.yml`.
- PDF engine: Typst. Main font Noto Sans; Arabic font Noto Naskh Arabic
  (installed in CI from `fonts-noto-core`).

## Design

- One design system for all courses; each course has its own colour theme.
  Light look: near-white backgrounds, the course colour only as accents.
  Never a blue theme. Readable dark text everywhere.
- Course colours: `course.accent` / `course.accent2` / `course.theme` in
  `courses/<slug>/_metadata.yml` (PDF + lesson pages). Keep `.theme-*` colours
  in `shared/templates/site.scss` and `shared/sims/sim-base.css` the same.
  game-math: green `#2F9E44` / lime `#A9E34B` (`arcade`);
  computing-systems: gold `#A86700` / yellow `#FFD43B` (`circuit`).
- Web: `_extensions/lesson/lesson.css` (hero, word cards, "Try it" cards,
  summary) + `lesson-script.html` (progress bar, "I did it" buttons).
  Site theme and fonts: `shared/templates/site.scss`, fonts in `shared/fonts/`.
- PDF: `_extensions/lesson/typst-template.typ` (title band, header, footer),
  `typst-show.typ`, `typst-body.typ` (callout style).
- Slides: `_extensions/lesson/pptx_finish.py` (project post-render) gives every
  `.pptx` the course look: colours from `_metadata.yml`, fonts, background shapes,
  footer, a coloured title slide, a fade between slides, and the click animations.
  Never style slides by hand in PowerPoint; change the script once for all courses.
- Mark the last two sections: `## Class activity {.activity}` and `## Summary {.summary}`.

## Try it: match the answer

Every "Try it" box in a lesson is interactive. Do not write static answers.

```markdown
::: {.callout-tip title="Try it 1"}
Position or vector?

::: {.match}
The coin is at (7, 4).
:   position

The car goes 3 steps right.
:   vector
:::
:::
```

- Each question (the term) is followed by its right answer (`:   answer`).
- **Web:** the questions get labels a), b), …; every different answer is shown
  **once** as a button, in a random order. The student taps the answer for the
  question in colour and sees at once "Right!" or "Not this one. Try again."
  When all are right, the box shows the score and its "I did it" button is ticked.
- The same answer may fit several questions (input / output / …); say so in the
  instruction: "You can use an answer more than once."
- With only 1–2 questions, or few different answers, add wrong answers:
  `::: {.match extra="2 frames|4 frames"}` (split by `|`).
- Keep answers short (a word, a number, a short phrase).
- Answers must be fixed. Never ask about what a simulator shows now: the
  student can change it at any time (and "Challenge" places things at random).
  Ask about a fixed picture, and put that picture **inside** the "Try it" box.
  A simulator can be used only for questions with one fixed answer
  ("Move the player to (0, 0). What is this point called?").
- **Check every "Try it" before you commit:**
  1. *Self-contained.* The student can answer from the box alone. A picture it
     needs is inside the box, or directly above it and called "the picture above".
  2. *No changing state.* Nothing depends on a simulator, the time, or the
     student's own phone (menus and brands differ).
  3. *One right answer.* Every question has exactly one right option. Every
     wrong option (`extra`) is clearly wrong, never "also right sometimes"
     (e.g. phone vs tablet "on the bus").
  4. *Same words.* The answer matches what the question asks, and uses the
     words of the lesson.
  5. *Tried.* In `quarto preview --profile review`, tap one wrong and then all
     right answers in each box.
- **PDF:** the questions with a blank line, "Choose from:" (A to Z), and the
  answers upside down at the bottom of the box.
- Open tasks (fill a table, talk with a partner) stay as text in the same box,
  next to a small matching check.
- No "Check your answers" boxes for "Try it" any more. Filter: `_extensions/lesson/match.lua`;
  behaviour in `lesson-script.html`, look in `lesson.css`.

## Interactive slides

Slides are for a conversation with the class, not a one-way talk.
The teacher asks, the students answer aloud, then one click shows the answer.

- **Every "Try it" of the lesson is a slide**: `## Try it N · short title`,
  the questions, then the answers in `::: {.answer}`.
- **Add "Think" slides** before a new idea: `## Think · short title`, one
  question ("What do you think…?"), then `::: {.answer}` or `::: {.reveal}`.
  Use as many as fit the lecture.
- `::: {.answer}`: each list item or paragraph becomes an answer card at the
  bottom of the slide. Each card pops in on its own click (elastic zoom).
  Use the same labels as the questions (`a)`, `1.`) so the cards show them.
- `::: {.reveal}`: each item fades in from the left on its own click.
  Use it for "think first, then see" lists. Normal slides show everything at once.
- Keep questions short (about 5 lines), so the cards fit under them.
- A picture can go next to the questions with `:::: {.columns}`;
  the cards still go at the bottom.
- The "Try it" / "Think" title label gets the course colour and a big faint "?".
- Filter: `_extensions/lesson/slides.lua`. Look and animations: `pptx_finish.py`.
- Check a deck in PowerPoint's Slide Show before class: every click must show
  the next answer.

## Slides for students

- `slides-public: true` in `_quarto.yml` shows a "Lecture slides" button on each
  lesson with a note that slides are a summary, not study material.
  Set it to `false` to keep slides teacher-only (they are still built).

## Simulators

- Plain HTML + JavaScript. No paid services, no external APIs, nothing loaded
  from the internet. Third-party libraries are copied into `shared/sims/vendor/`
  with their license (three.js r170, MIT). Must work on a phone.
- 3D: use `shared/sims/viewer3d.js` (Unity axes: x right, y up, z forward;
  axes, ground grid, labels, arrows for vectors, dashed paths, animation).
  Example: `courses/game-math/week-01/sims/position-3d.html`.
- Lesson-specific: `courses/<slug>/week-NN/sims/<name>.html`.
  Reusable across courses: `shared/sims/<name>.html`.
- Shared look and auto-resize: link `shared/sims/sim-base.css`, load
  `shared/sims/sim-base.js` (relative paths), and put the course theme class
  on `<body>` (`theme-arcade` / `theme-circuit`).
- Every simulator needs a static poster image `<name>.png` (keep the `.svg`
  source next to it). Export: `quarto typst compile` via `shared/sims/export-poster.typ`
  (see `shared/sims/README.md`).
- Embed with `{{< sim file="sims/<name>.html" poster="sims/<name>.png" title="..." >}}`.
  HTML → live iframe + "open full screen" link. PDF → poster + QR code to the
  live page. PPTX → poster + large QR code ("Scan to try it") so students open
  the simulator on their phones during the lecture. Never hand-write this per format.
- **Every slides file must have one "Live demo" slide per simulator in the lesson**,
  using the same `{{< sim >}}` shortcode, so each interactive part has a QR code in class.

## Site identity

- Title: **Mohanad Hamed — Courses**.
- Subtitle: *Lecturer, Mobile Game Development and Design — Technical College, Al-Israa University*.
- Every lesson page shows its course name and the diploma/university line.
- `about.qmd` ends with one small muted credit line (`.credit-note`). Keep it
  exactly as it is. Never add a similar line anywhere else.
- No tool or assistant names anywhere: not in pages, source code, comments,
  file names or commit messages. The credit line on the About page is the only exception.

## Homework (take-home assignments)

Homework **tasks are public**, like the lessons (common practice: MIT
OpenCourseWare, Stanford and Harvard CS50 publish their problem sets). Students
can prepare, and the homework is take-home anyway. **Solutions, model answers
and marking notes stay private**, never in this repo: they go in the private
repo `courses-private` (folder `../courses-private`, next to this one), with
the same paths: `courses/<slug>/week-NN/homework-NN-solutions.md`. Change a
homework and its solution together.

- One homework per week and course: `courses/<slug>/week-NN/homework-NN.qmd`,
  from `shared/templates/homework-template.qmd`. No homework in exam weeks
  (8, 16). computing-systems week 15: the project instead (syllabus).
- Built from the week's ILOs (`ilos:`), like the lessons: practise exactly
  what the two lessons taught, in the same words. No new content.
- Size (start of the semester): **1–2 short tasks, about 15 minutes**, in both
  courses. Short homework that students finish is better than long homework
  they skip. I may make it longer in later weeks, if the students do it well;
  then I will change this rule. Marks per task in the heading; total in `marks:`.
- At least one task in a real game situation (the PLO behind the ILO).
- Written answers only (semester 1: no programming). Code may be read, never written.
- **Fixed numbers only** ("3 steps up", "(8, 4)"): no variables like *n* in a
  task. Classes are small, so copying is not a risk now.
- **Change the numbers and situations every semester.** Old versions stay in
  the git history, and old answers go around.
- `due:` is relative ("Week 3, before the first lecture"), so the page works
  every semester. Exact dates go on the e-learning platform.
- Submission: the university e-learning platform (syllabus). The page says how.
- Release: keep `draft: true` until the week opens; then remove it.
  Earlier homework stays online.
- No answers on the page: no `.match` boxes, no "Check your answers".
- **Web page only, printed by the student.** Homework belongs to the week, not
  to a lesson, so it is not in any lesson PDF and has no PDF of its own
  (`format: lesson-html`). The page has a "🖨 Print homework" button.
- **Answer space:** after every question, add space to write the answer:
  `{{< answer-space lines=2 >}}` (dotted lines; as many as a good answer needs)
  or `{{< answer-space box=6 >}}` (an empty box, height in cm, for a drawing).
  They appear only on paper, with a Name / Student number line at the top.
- **One A4 page:** the printed page must fit on one page.
  "How to submit" is one short line; the print layout is tight.
  If it does not fit, cut a question or use fewer lines, never a smaller font.
- The course page lists released homework (week, title, due, marks).
- Check every task like a "Try it": self-contained, one clear answer
  (or a clear marking rule), no changing state, tried before release.

## Public repo — never commit

Assignment solutions and marking notes, exam questions, question banks, grades,
student data, official internal university documents. Those live elsewhere,
privately. Homework *tasks* are public (see "Homework").
Lessons or homework not ready for students: `draft: true` (not published).

## Way of working

- Build week by week. Never generate all lessons up front.
- Phase 1: `plan.md` per course (16-week map → ILOs, same weeks as the syllabus), approved by me first.
- Phase 2: **a typical session = one week**: 2 lessons for `game-math` +
  2 lessons for `computing-systems`, each with all 3 outputs (4 lessons total),
  plus one homework per course.
  Start every session by reading that week in the Drive syllabus.
- I review every lesson before release. Ask before big structural decisions.
- After each week I write `courses/<slug>/retro/week-NN.md`. Turn general lessons
  learned into rules here; course-specific ones into the course `NOTES.md`.
- Semesters: improve lessons in place, never copy a course. Tag each finished
  semester (e.g. `git tag 2026-fall`).

## Git

- Commit locally as me: author and committer come from my git config
  (`Mohanad Hamed <mohanad_subhi@yahoo.com>`). Never pass `--author`, never set
  another `user.name`/`user.email`.
- Commit messages describe the change only. No tool names, no co-author
  trailers, no "generated by" lines.
- Every commit is signed with my SSH key (global git config:
  `gpg.format ssh`, `commit.gpgsign true`), so GitHub shows it as **Verified**.
  Never pass `--no-gpg-sign`.
- Check with `git log -1 --format='%an <%ae> / %cn <%ce> / sig %G?'` after
  committing. `sig G` means a good signature.
- Never commit or push to `main`. Put every change on a feature branch
  (for example `week-02-lessons`), commit there, push the branch and open a
  pull request into `main`. I review and merge the PR myself.
- PR title and description follow the commit message rules (no tool names,
  no "generated by" lines).

## Build

- Local: `quarto preview` (HTML) or `quarto render` (all outputs → `_site/`).
- Review drafts before merging a PR: check out the PR branch, run
  `quarto render --profile review` once (the preview alone does not build the
  PDFs), then `quarto preview --profile review` (`_quarto-review.yml` shows
  `draft: true` lessons).
- CI: `.github/workflows/publish.yml` renders on push to `main` and deploys to Pages.
- Quarto version is pinned in the workflow; keep local Quarto the same.

## Lessons learned

<!-- Add general rules from weekly retros here, newest first. -->
