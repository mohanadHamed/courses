# Authoring rules for all courses

Owner: Mohanad Hamed, Lecturer, Mobile Game Development and Design diploma,
Technical College, Al-Israa University (Jordan). Never write "Dr." anywhere.

This public repo holds the lesson materials for **all** courses I teach.
Site: <https://mohanadhamed.github.io/courses/> (Quarto website → GitHub Pages).

## Courses

Program: Mobile Game Development and Design, Intermediate University Degree
(Diploma), code L6, Technical College. All four courses are year 1, semester 1
(2026-2027 syllabi).

| Slug | Official course name | Code | Credit hours | Per week (as taught) | Textbook |
|---|---|---|---|---|---|
| `game-math` | Mathematics and Computing for Digital Games | 13411131 | 3 | 2 lectures × **90 min** | Dunn & Parberry, *3D Math Primer for Graphics and Game Development*, 2nd ed. |
| `computing-systems` | Fundamentals of Computing Systems and Digital Platforms | 13411133 | 2 | 2 × **60 min** (lecture + seminar) | Tanenbaum & Austin, *Structured Computer Organization*, 6th ed. |
| `digital-media` | Digital Media Technologies and Creative Production for Games | 13411134 | 2 | 2 × **60 min** (lecture + seminar) | Schell, *The Art of Game Design*, 3rd ed. |
| `digital-skills` | Digital Skills | 01101154 | 2 | 2 × **60 min** (lab sessions) | Evans, Martin & Poatsy, *Technology in Action*, 18th ed. (+ DigComp 2.2) |

`digital-skills` is taught to the diploma students of the whole college,
most of them not in technology: it is simpler than the other courses (A2
English) and uses general examples, never the games industry. Its
`NOTES.md` has the details and overrides "Level and language" below.

**One lecture = one lesson. Every course has 2 lessons per week.**
16 weeks: week 8 midterm, week 16 final. Use the official course names exactly.

### Lectures, not weeks (what students see)

The syllabus plans by week, but the site never shows a week. Absences and
delays move each course differently (one course may reach week 5 while
another is in week 3), so everything students and the teacher see counts
**lectures**: "Which lecture did we reach?"

- Lectures are numbered 1, 2, 3 … in teaching order, with no gap for exams.
  The course page lists them in pairs ("Lectures 1–2"), each pair followed
  by its homework.
- **Homework k follows lectures 2k−1 and 2k** and is due "before lecture
  2k+1". There is no homework after a revision lecture or the project.
- **Exams are not on the site.** The university sets the midterm and the
  final exam in its own week; the site does not tie them to a lecture. A
  revision lecture is an ordinary lecture ("Revision of Lectures 1–14").
- Pages, PDFs, slides and download names say "Lecture N" and "Homework k",
  never "Week N"; slide subtitles are "Lecture N" (or "Lecture N ·
  Seminar", "Lecture N · Lab session").
- The folders keep the name `week-PP` (PP = the pair: lectures 1–2 and
  homework 1 in `week-01`, lectures 3–4 and homework 2 in `week-02`). The
  name is internal: it keeps the links and QR codes of printed notes
  working, and it is never shown.
The textbook is in `course.textbook` (`_metadata.yml`). Follow its topics and
level; never copy its text, figures or exercises.

### Mapping the syllabus week to the 2 lessons

- `game-math`: syllabus has First Lecture + Second Lecture + Seminar.
  Lesson A = First Lecture, Lesson B = Second Lecture. The seminar topic
  becomes the case study / Game challenge of lesson A.
- `computing-systems`, `digital-media`: Lecture + Seminar.
  Lesson A = Lecture topic, Lesson B = Seminar topic (applied, analysis, practice).
- `digital-skills`: Lab Session 1 + Lab Session 2 (computer lab). Both lessons
  have notes like the others, plus "Lab task" boxes on the page.
- Exam sessions (midterm, final) get no lesson and no number. Revision
  sessions get a revision lesson. Confirm with me when a syllabus week is
  unclear.

## The lesson model: the notes come first

Students turned out to be stronger than expected: the first lessons were too
simple and repeated the same idea many times. Every lesson is now built in
this order.

1. **Lesson notes (PDF)** — `lesson-NN-book.qmd` → `<prefix>_lectureN.pdf`.
   The main study text, written like an applied chapter of a technical
   textbook: simple, clear English (see "Level and language"), numbered
   sections (`## 1.1 …`), precise definitions, worked examples and common
   mistakes, "Do it" tasks (see "Applied first"), figures, tables, short C#
   reading examples where useful, a case study, further reading (textbook
   chapter), exercises and short answers. It is never long on theory.
2. **Interactive lesson (HTML)** — `lesson-NN.qmd`, derived from the notes.
   The same sections (`## 1.1 …`), each with a short, clear summary (plainer
   English than the notes, but not childish), its figures, its simulator or
   mini-game, and **one** "Try it" set. Then the Game challenge and a summary.
3. **Slides (PPTX)** — `lesson-NN-slides.qmd`, derived from the notes: a
   visual summary for class and for revision.

The PDF links to the web lesson (QR card under the ILOs, added by
`banner.lua`) and to every simulator and mini-game (QR in the `{{< sim >}}`
box). The web lesson's main button is "Lesson notes (PDF)".

### Applied first (a diploma, not a bachelor's degree)

The program is an applied diploma (Intermediate University Degree, JNQF;
the syllabi describe every ILO as Knowledge, Skill or Competency). Graduates
are expected to *do* things in a game studio, so students learn mainly by
doing. Theory is taught as far as a task needs it, and every concept ends in
something the student does. This holds for the notes, the page and the
slides.

- **The outcomes come first, the tasks serve them.** Every applied task
  builds the ILO of that week (the course ILOs in the syllabus and the
  ILO–PLO matrix on Drive) at its Bloom level and descriptor, and serves the
  PLO behind it. A "describe" ILO (A, level 1–2, K) still ends with the
  student describing or explaining; the task gives the description a real
  object (their phone, a spec sheet, a game screen). Never add a skill
  that belongs to an ILO of a later week (for example setting up an emulator,
  C1, before week 14 of `computing-systems`), and never drop the knowledge an
  ILO asks for: the midterm and final still test it.
- **Situation → concept → task.** Every section opens with a concrete game
  development situation (a problem a developer meets), gives the concept
  needed to handle it, and ends with the student handling it. Never open a
  section with a definition. Prefer section titles that name the problem or
  the action ("Why the game loads slowly: storage") over abstract ones.
- **One "Do it" task per section** (notes and page:
  `::: {.callout-note title="Do it · short title"}`; in `digital-skills` the
  same box is called "Lab task"). Short (2–5 minutes), done alone, on things
  every student has: their phone, the lab computer, a browser, a simulator or
  mini-game of the lesson, a free tool that runs in the lab, or paper. It
  has a concrete product: a number, a filled table, a file, a sketch, a
  decision with a reason. It works on Android and iOS, and on Windows lab
  computers; if a step differs, say how. No programming and no game-engine
  interface (see "Students").
- **Theory budget.** About one third of a lesson explains; two thirds apply
  (game-based worked examples, Do it tasks, Try it, Game challenge).
  At most one formal definition per section, only for terms the tasks use.
  History, taxonomies and background that no task or ILO needs are left out
  or go to "Further reading".
- **Questions ask students to use the idea.** In every "Try it" set and in
  the exercises, at least two thirds of the questions put the idea into a
  game situation: choose, classify, decide, find the error, or (where the
  ILO needs it) calculate; the rest may check a term or a definition. See
  "Level and language" for the level of thinking.
- **Worked examples are game cases with real numbers** (a load time, a frame
  budget, a sound level, a file name), never abstract ones.
- **Slides teach by showing.** In class, each section is a short concept and
  a live demonstration on the projector (phone settings, the lab computer, a
  simulator); then each student does the Do it task alone, on their own
  phone or lab computer. Never "do it together": no group or class activity.

### No repetition (most important)

- Each concept gets **one** section. Explain it once, give it one set of
  questions, then move on to a clearly *different* concept
  (2D coordinates → 3D coordinates → …). Never ask again about something a
  previous section already practised.
- **One "Try it" box per section** (the Game challenge may have 1–3). Inside
  a box, every question tests something different: no lists of near-identical
  questions. `check_size.py` warns when a section has more than one box.
- Do not repeat the same picture on consecutive slides, and do not repeat
  the whole lesson in the summary (5–6 short lines).
- Go deeper, never wider: new cases, the reverse question, precision,
  practical consequences — never the next week's topic.

### Rich and visual

- Every section of the notes and of the page has at least one figure,
  diagram or illustration; every concept slide has a picture.
- Draw figures as SVG (keep the `.svg`, export a `.png` for PDF and slides:
  see `shared/sims/README.md`). Illustrated "game screens" of the made-up
  case-study games are welcome. Never use screenshots of commercial games or
  copyrighted images.
- No emoji or special symbols inside SVG figures (the PDF engine cannot draw
  them); draw icons as shapes.

### Mini-games

When a concept is tied to an event in a game (a tap to jump, a hit, a sound
that changes with distance, a velocity applied every frame), build a small
playable **mini-game** for it in `week-NN/sims/`, embed it on the page and
link it from the notes and the slides:
`{{< sim file="sims/x.html" poster="sims/x.png" title="…" kind="game" >}}`
(label "Mini-game", QR text "Scan to play"). Same rules as simulators.

### The game of the lesson (playable case study)

When the Case study and the Game challenge of a lesson use a made-up game
(*Harbor Guard*, *Comet Courier*, *Pocket Pets*, …), build its core as a
mini-game: only the part that the lesson teaches (placing objects by their
coordinates, one velocity per frame, sorting player messages by component,
switching the tetrad on and off), with the numbers of the story in its first
round. Then:

- **Page:** the Game challenge embeds it after the story and before the Try
  it boxes (`{{< sim … kind="game" >}}`); it replaces the static illustration.
- **Notes (PDF):** the Case study embeds the same shortcode (poster + QR,
  "Scan to play").
- **Slides:** the Game challenge slide shows the game, its recording and
  QR code, with a `task` line that tells the story in one sentence and what
  to do (`{{< sim … kind="game" task="…" >}}`). The Try it slide after it
  starts with the facts of the story in full sentences.
- If the lesson's mini-game already *is* that game (Tap Runner), reuse it:
  the notes and the page point to it, the slide shows its QR code.
- A story about a studio, a class or a person, not a game, needs no game of
  its own.

`check_size.py` warns when a game of the page's Game challenge is missing in
the notes or on the Game challenge slide.

### Size every lesson for its lecture time

| | 60-min lesson | 90-min lesson (`game-math`) |
|---|---|---|
| Notes: numbered sections (`## 1.1`) | 3–4 | 5–7 |
| Notes: words (without exercises and answers), at most | 3 500 | 6 000 |
| Notes: worked examples | 2+ | 4+ |
| Notes: exercises (with short answers at the end) | 6–10 | 10–16 |
| Page: "Try it" boxes (one per section + Game challenge) | 4–6 | 6–9 |
| Page: questions in all "Try it" boxes | 15–28 | 30–45 |
| Simulators / mini-games | 0–2 | 1–3 |
| Slides (title slide not counted) | 10–16 | 20–28 |

**Class time and home time.** The notes and the interactive page are studied
at home, without a time limit, so they keep their full size. The **slides**
are what is taught in the lecture, and they are kept short so that the
teacher has time to explain the hard concepts in Arabic and answer
questions: one concept slide per section, the key worked examples, one
"Try it" slide per section with **2–3** of the page's questions, one Game
challenge story slide and **one** challenge "Try it" slide. Everything else
(the other questions, the second challenge box, extra examples, the
exercises) is for home.

**Time plan (90 min):** key terms 5 · sections ~65 (about 10 per section,
mostly explanation) · Game challenge ~10 · summary and questions 10.
**Time plan (60 min):** key terms 3 · sections ~42 · Game challenge ~8 ·
summary 7.

`_extensions/lesson/check_size.py` (project pre-render) checks these numbers,
that every section of the notes is on the page, the one-box-per-section rule,
one "Do it" (or "Lab task") box in every section of the notes and the page,
the required parts (notes: Key terms, Exercises, Answers to the exercises;
page: Key terms, Game challenge, Summary) and one "Live demo" slide per
simulator. Fix every warning before you open a PR. Full table:
`python3 _extensions/lesson/check_size.py --all`. Keep `SIZES` and this table
the same.

**Independent study first; team work only where the syllabus asks for it.**
Every student must be able to learn from the notes and the page alone.
Interactive pages, slides, lab tasks and homework never need classmates.
A team activity appears **only in the notes (PDF)**, and only in the one or
two lessons where the syllabus or a course ILO names team work (the D1
weeks): one short `::: {.callout-note title="Team activity"}` box with roles,
a product and a presentation, followed by an individual alternative for a
student who works alone. No other lesson has group or pair work or
discussions with classmates. Each course's `plan.md` names these lessons.

**Game challenge (every course; no class activities).** No groups, no paper:
every student works alone on the page, and the teacher shows one part on
the slides. `## Game challenge: <name> {.challenge}`, a short story of one
made-up game or studio (3–5 sentences with fixed numbers), then the game
itself as a playable mini-game when the story is about a game (see "The game
of the lesson"), then "Try it" boxes that combine the sections of the day (the
last one "(harder)"). The notes contain the same story as a "Case study"
section.

Course-specific notes: `courses/<slug>/NOTES.md`. Week map:
`courses/<slug>/schedule.yml` (titles, ILOs) and `courses/<slug>/plan.md`.

## Source of truth: the Google Drive folder (private, never copy into this repo)

The Google Drive folder **الكلية التقنية** → `02-الأقسام-الأكاديمية/01-قسم-تطوير-ألعاب-الموبايل/`
is the **source of truth** for the Mobile Game Development diploma:
study plan, guidance plan, course descriptions, and
`06-خطط-المواد-ومصفوفات-مخرجات-التعلم/` (English syllabi with weekly topics,
ILO–PLO matrix). Use the newest version of each file.

- **Before creating any lesson, read the course syllabus and ILO–PLO matrix
  from Drive** (Google Drive connector). Base the lesson on that week's topics and ILOs.
- If the Drive and this repo disagree, the Drive wins: update `_metadata.yml`,
  `schedule.yml`, `plan.md` or these rules, and tell me.
- Copy only ILO text into `_metadata.yml`; never commit the documents themselves.

## ILOs and PLOs

- ILO codes follow the syllabus: A1, A2 (knowledge), B1, B2 (intellectual),
  C1, C2, C3 (subject skills), D1 (transferable).
- Official ILO text (with PLO numbers) lives in `courses/<slug>/_metadata.yml`
  under `course.ilos`. Lessons list codes only: `ilos: [A1, B1]`.
  An unknown code is a render error.
- Program PLOs: 1 game programming and development; 2 creative development,
  player experience and UI; 3 industry trends, modern technologies and
  professional development; 4 industry management and quality assurance.
- **Lessons are built from ILOs.** Pick the ILOs from the syllabus week, then
  design sections, examples and exercises that build exactly those ILOs.
- PLOs connect to lessons **through** the ILOs. Do not target PLOs directly,
  but choose examples that serve the PLO behind each ILO (PLO 1 → game
  programming and engines; PLO 2 → player experience; PLO 3 → tools and
  industry; PLO 4 → testing, quality, production).

## Students

- Diploma students, first year. They cope with real concepts when the
  text is simple and clear, but English is their second language.
- I explain in Arabic in class; the bilingual glossary supports them.

### Level and language

The students' starting level is very basic. The level is about 20 %
simpler than the first applied version of the lessons (October 2026), which
was already slightly easier than a first-year bachelor's course; the English
is simple. The ILOs and PLOs stay exactly the same: a lesson is easier in
*how* it teaches, never in *what* the ILO asks for. (The estimated limit is
about 30 % simpler: beyond it, syllabus topics, the ILO verb or the practical
tasks would be lost.)

- **Scope: only what the outcomes need.** A topic goes into a lesson only if
  the syllabus week names it, an ILO of the week asks for it, or an ILO of a
  later week builds on it (for example handedness, needed by the cross
  product in week 3). Everything else is left out, even when it is useful in
  practice (for example screen ↔ world conversion formulas, the index of a
  tile grid, Blender ↔ Unity conversion, evaluation criteria before the
  evaluation ILO). Spend the time in class on the Do it tasks and questions,
  not on more examples of the same idea: short notes are better than
  repeated ones.
- **Match the thinking to the ILO.** For a knowledge ILO (describe, explain;
  K), questions ask students to recognise, describe, classify or explain a
  game example. Calculations appear only where the ILO or a later ILO needs
  them.
- **Numbers:** small, round numbers (1024 × 1024, 100 reads, 10 ms + 6 ms).
  One step per calculation, no calculator needed. No conversion that needs
  a calculator (1024³ and the like) unless an ILO asks for it.
- **Depth:** one idea at a time; the main idea of a section fits in two
  sentences. Leave out details that the ILO and the tasks do not need
  (cache levels, standards, exceptions); one short sentence is enough when
  a student may meet the detail in practice.
- **English (notes):** CEFR B1. Short sentences (about 20 words at most,
  one idea each), common words, active voice ("the CPU reads the value",
  not "the value is read"), no idioms. Explain every technical word in plain
  words the first time it appears, then use the same word every time.
- **English (page and slides):** A2–B1: even shorter sentences and lists.
- Definitions stay precise, but in the same simple English.
- No programming yet: *Programming Fundamentals (1)* (C#) is in semester 2.
  Code in semester-1 courses is a short C# example to read, never a task,
  and every code word is explained.
- Do not teach a game engine's interface (Inspector, GameObject, …): Unity
  has its own course. Engine conventions (axes, handedness, `Vector3`) are fine
  as examples.

## Writing rules (always enforce)

- **Notes:** simple English (B1, see "Level and language"): short
  paragraphs, direct steps. Precise
  definitions (`::: {.callout-important title="Definition 1.2 — …"}`), worked
  examples with numbered steps (`::: {.callout-note title="Example 1.3 — …"}`),
  common mistakes (`::: {.callout-warning title="Common mistake"}`), code
  (`::: {.callout-caution title="In game code"}`), figures with captions and
  `@fig-` references, tables with captions, `::: {.lead}` opening paragraph,
  `::: {.answers}` for the short answers.
- **Page:** the same content, shorter and plainer (A2–B1): one idea per
  sentence, but no baby talk. "Watch out!" boxes for common mistakes.
- **Slides:** short, complete sentences and pictures; no paragraphs. See
  "Slides explain themselves".
- Picture before formula: game situation → figure → definition → example →
  Do it.
- Every rule or formula gets a worked example in the notes.
- Every lesson starts with a bilingual "Key terms" glossary (8–14 terms).
- Facts must be correct and current (conventions of engines, standards,
  numbers). When unsure, leave it out.

## Glossary

- Master list: `shared/glossary.yml` (`key: {en, ar, def}`); `def` is one
  precise textbook sentence.
- Insert with `{{< glossary key1 key2 ... >}}`. A missing key is a render error
  — add the term to `glossary.yml` first, never inline.
- Same English term and same Arabic translation for a concept everywhere.
  Check `glossary.yml` before adding; reuse existing keys. No `: ` inside a
  value (YAML).

## Three outputs per lesson

Folder: `courses/<slug>/week-PP/`, one folder for each pair of lectures
(see "Lectures, not weeks"): lectures 1–2 in `week-01`, 3–4 in `week-02`, ….
NN in the file names is the lecture number. Figures in `week-PP/images/`,
simulators and mini-games in `week-PP/sims/`.

| File | Format | Output |
|---|---|---|
| `lesson-NN-book.qmd` | `lesson-typst` | Lesson notes, PDF (the main text) |
| `lesson-NN.qmd` | `lesson-html` | Interactive lesson page |
| `lesson-NN-slides.qmd` | `lesson-pptx` | Slides (.pptx), public summary |
| `homework-KK.qmd` (KK = pair) | `lesson-html` | Take-home task page with Print and Download PDF buttons |

- **Download names.** Files students download have meaningful, unique
  names: `math_lecture5.pdf` (notes), `math_lecture5_slides.pptx` (slides),
  `math_homework1.pdf` (homework). N is the lecture or homework number
  without a leading zero; the prefix is `course.file-prefix` in
  `_metadata.yml` (`math`, `computing_systems`, `digital_media`,
  `digital_skills`). `download_names.py` (post-render) renames the rendered
  files; `banner.lua` and `{{< schedule >}}` link the same names. Keep the
  source names (`lesson-NN-book.qmd`) as they are.
- Start from `shared/templates/book-template.qmd`, `lesson-template.qmd`,
  `slides-template.qmd` and `homework-template.qmd`.
- Formats, styles and filters live in the Quarto extension `_extensions/lesson/`
  (Quarto requires `_extensions/` at the project root). Change look and
  behaviour there, once, for every course.
- The formats add the course banner (course name, diploma line, lecture
  number, ILOs) automatically from metadata.
- PDF engine: Typst. Main font Noto Sans; Arabic font Noto Naskh Arabic
  (installed in CI from `fonts-noto-core`). Book filter: `book.lua`
  (`.lead`, `.answers`); callout styles: `typst-body.typ`.

## Design

- One design system for all courses; each course has its own colour theme.
  Light look: near-white backgrounds, the course colour only as accents.
  Never a blue theme. Readable dark text everywhere.
- Course colours: `course.accent` / `course.accent2` / `course.theme` in
  `courses/<slug>/_metadata.yml`. Keep `.theme-*` colours in
  `shared/templates/site.scss` and `shared/sims/sim-base.css` the same.
  game-math: green `#2F9E44` / lime `#A9E34B` (`arcade`);
  computing-systems: gold `#A86700` / yellow `#FFD43B` (`circuit`);
  digital-media: grape `#9C36B5` / pink `#F783AC` (`studio`);
  digital-skills: orange `#D9480F` / peach `#FFC078` (`workshop`).
- Web: `_extensions/lesson/lesson.css` + `lesson-script.html`.
  Site theme and fonts: `shared/templates/site.scss`, fonts in `shared/fonts/`.
- PDF: `typst-template.typ` (title band, header, footer, justified text),
  `typst-show.typ`, `typst-body.typ`.
- Slides: `_extensions/lesson/pptx_finish.py` (project post-render) gives every
  `.pptx` the course look. Never style slides by hand in PowerPoint.
- Mark the last two sections of the page: `## Game challenge: … {.challenge}`
  and `## Summary {.summary}`.

## Try it: match the answer

Every "Try it" box on the page is interactive. Do not write static answers.

```markdown
::: {.callout-tip title="Try it 1 · Short title"}
One instruction.

::: {.match extra="wrong answer|another wrong answer"}
First question.
:   its answer

Second question.
:   its answer
:::
:::
```

- Each question is followed by its right answer (`:   answer`). The page shows
  every different answer once as a button, in random order.
- The same answer may fit several questions; say so: "You can use an answer
  more than once." With few different answers, add wrong ones in `extra`.
- Keep answers short. Escape a backslash as `\\`.
- Answers must be fixed (never about what a simulator shows now).
- **Check every "Try it" before you commit:** self-contained (the picture or
  numbers are in the box or the section above), no changing state, exactly one
  right option per question, the words of the lesson, varied questions (no
  near-duplicates), tried in `quarto preview --profile review`.
- **Every fact a question needs is on the page.** If a question uses a fact
  from the notes (an example, a table, a name such as "Alpha" or "the Switch"),
  the page section shows it too, in a bullet or a figure. When notes or pages
  are shortened, check the questions again.
- **No question depends on another one.** Repeat the numbers in each question
  ("The same enemy E = (2, 7) and player P = (6, 4) …"); the student may answer
  in any order.
- **The Game challenge box repeats the key facts** of the story in its first
  line (names, coordinates, sizes), so the box can be answered without
  scrolling back. Names in the questions also appear in the game and its
  poster (Alpha and Beta are labelled on the map).
- **Every slide question can be answered from the slides** (the concept slide
  bullets, a table slide, the Game challenge slide or the facts at the top of
  the Try it slide).
- Filter: `_extensions/lesson/match.lua`; behaviour in `lesson-script.html`.

## Interactive slides

Slides are for a conversation with the class.

### Slides explain themselves (most important for slides)

A teacher who did not prepare the lesson, or a student who missed it, must
understand every slide from the slide alone: what it says, what it asks and
what the class does with it. Short is good; unclear is not.

- **Sentences, not fragments.** Every bullet is a short, complete sentence
  with a verb ("Installing copies the game into storage."), not a fragment
  ("install → storage", "APK · IPA", "CPU: logic"). A formula, a menu path
  (Settings → About) or a file name may stand inside a sentence.
- **A question looks like a question.** It is a complete question with a
  question word (What, Which, Why, How, Where, Who, When, Is, Does, Can …)
  and a "?": "Which part of the phone fills up when you install a game?",
  never "installing fills…?" or "a painted forest background". Give the
  numbers and the situation inside the question, even if it gets longer.
- **The answer is on the same slide**, hidden until the teacher clicks
  (`::: {.answer}` cards or `::: {.reveal}` steps). A slide never asks a
  question that a later slide answers.
- **A statement never hides a question.** A slide that tells a story or
  gives facts says so ("The story: …", "The facts: …"), and a slide that asks
  something asks it in a full question. If the questions about a story come
  on the next slide, that slide repeats the facts it needs.
- **Every slide says what to do.** A Do it bullet is a full instruction for
  one student, labelled only "Do it:" (never "together"; each student works
  alone without being told so), for example "**Do it:** Open Task Manager
  (Ctrl + Shift + Esc). How many logical processors does the CPU have?". Every Live demo and Game
  challenge slide has a `task` in its `{{< sim >}}` shortcode: what the
  teacher shows and what the class is asked ("Show: jump with +0 ms, then
  with +220 ms. Ask: why does the jump feel late?").
- **Examples state their question** before the steps ("How long does the
  level load on each phone?"); each step is a short sentence that ends with
  the result.
- **Summary lines are sentences** (5–6), one per main idea.
- **Titles fit on one line** (44 characters at most, with the "Try it N"
  label); a second line runs into the text below.
- **Nothing overlaps.** Longer sentences need care: at most four sentences
  and the Do it bullet on a concept slide, 2–3 questions on a Try it slide
  (the answer cards take the lower part of the slide), 3–4 steps in an
  Example. Look at every slide, with all answers shown, before a PR.
- `check_size.py` warns about fragments of one to three words, bullets with
  " · " between keywords, questions without a question word or "?", "…",
  Try it slides without an answer on the slide, Examples without a
  question, simulator slides without a `task`, and group work ("Do it
  together", "with a classmate").

### Slide types

- **One "Try it" slide per section**: `## Try it N · short title`, **2–3**
  questions chosen from the page's set, then the answers in `::: {.answer}`.
  Two short sections may share one slide (`## Try it 3–4 · …`).
- **No "Think" slides** (a question before the idea): in class, a question
  without a visible answer leaves the class waiting for one. Every question
  is on a Try it slide or in an Example, with its answer.
- **Key worked examples only** (about one per section in 90 min, fewer in
  60 min): `## Example · short title`, 3–4 steps in `::: {.reveal}`. Common
  mistakes go in a bullet of the concept slide, not on their own slide.
- **Pictures:** every concept slide has a figure. A picture together with
  text must be in columns, or the slide is split in two:
  `:::: {.columns}` / `::: {.column width="50%"}` text / `::: {.column width="50%"}` picture.
  Text in a column with a picture is lost: keep them in separate columns.
  At most four sentences and the Do it bullet; `pptx_finish.py` makes long
  text smaller, but a smaller font is not a reason to write more.
  A table slide has no other text (put a short note in the title).
  Never put `.reveal` or `.answer` inside columns.
- One "Live demo · …" slide per simulator or mini-game (same `{{< sim >}}`
  shortcode with a `task`: the task line above the recording of the game
  being played, and a large QR code).
- Game challenge: one slide with the game itself (its recording + QR code,
  `{{< sim … kind="game" task="…" >}}`; the task gives the story in one
  sentence and says what to do), then one "Try it" slide (harder, 2–3
  questions) whose first lines give the key facts of the story in full
  sentences. A story without a game gets one story slide in full sentences
  (columns: text and a picture) that ends with the task.
- Filter: `_extensions/lesson/slides.lua`. Look and animations: `pptx_finish.py`.
  Check a deck in PowerPoint's Slide Show before class.

## Slides for students

- `slides-public: true` in `_quarto.yml` shows a "Lecture slides" button on each
  lesson and a "Slides" link on the course page. Slides are a summary, not
  study material. Set it to `false` to keep slides teacher-only.

## Simulators

- **A recording on every slide with a QR code.** Every simulator and
  mini-game that appears on a slide has a short GIF of it being played,
  `sims/<name>.gif` next to `sims/<name>.html`; the slides show it next to the
  QR code instead of the poster (`recording="sims/x.gif"` chooses another
  one). Make it with `shared/sims/recordings/`: a scenario that plays the game
  (`scenarios/<name>.js`), one line in `record-all.sh`, then
  `sh shared/sims/recordings/record-all.sh <name>`. Keep it 7–11 s and under
  about 500 KB. `check_size.py` warns when a slide's simulator has no
  recording. Record again when the simulator changes.
- **Robust game loops.** `requestAnimationFrame` first, then draw inside
  `try/catch`, so one failed frame never stops the game. Clamp times computed
  from the frame time (`Math.max(0, now − start)`): the frame time can be a
  little *before* the click that started an animation. Never decide a result
  only while drawing (a hidden tab draws nothing): use a timer as well. Never
  ignore a click silently: a button that cannot act now says why.
- Plain HTML + JavaScript. No paid services, no external APIs, nothing loaded
  from the internet. Third-party libraries are copied into `shared/sims/vendor/`
  with their license (three.js r170, MIT). Must work on a phone (pointer
  events, narrow screens). Sound only with Web Audio, after a tap.
- 3D: `shared/sims/viewer3d.js`. Lesson-specific: `courses/<slug>/week-NN/sims/<name>.html`.
  Reusable: `shared/sims/<name>.html`.
- Link `shared/sims/sim-base.css`, load `shared/sims/sim-base.js` (relative
  paths), and put the course theme class on `<body>`.
- Every simulator needs a poster `<name>.png` (keep the `.svg` next to it).
- Embed with `{{< sim … >}}` (see Mini-games). HTML → live iframe; PDF →
  poster + QR; PPTX → poster + large QR. Never hand-write this per format.
- Per-viewer state (a best score, a self-check) may use `localStorage`,
  always inside `try/catch`.

## Course pages and the schedule

- `courses/<slug>/schedule.yml` lists every lecture in teaching order
  (number, title, ILOs); no weeks and no exams. The course page shows it with
  `{{< schedule >}}` in pairs, each with its homework: a lecture whose
  `lesson-NN.qmd` exists and is not a draft is bright, with links (lecture,
  PDF, slides); the others are faded ("Coming soon"). Released homework
  appears after its two lectures.
- Titles in `schedule.yml` follow the syllabus weekly table. Change a title
  there, and in the lesson's front matter, together.

## Build number and fresh pages

- `_extensions/lesson/build_stamp.py` (post-render, last) writes
  `version.json`, adds `?v=<build>` to every local link and file, and puts a
  small "Build N · date · commit" line at the bottom of every page. In CI the
  build number is the GitHub Actions run number.
- Every page checks `version.json` (never cached) when it opens and when the
  tab becomes visible again; if a newer build is online, it reloads once with
  the new build in its address. Students therefore never study an old page.

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
the same paths: `courses/<slug>/week-KK/homework-KK-solutions.md`. Change a
homework and its solution together.

- One homework after every two lectures: homework k follows lectures 2k−1
  and 2k (`courses/<slug>/week-KK/homework-KK.qmd`), from
  `shared/templates/homework-template.qmd`. None after a revision lecture;
  computing-systems, digital-media and digital-skills: the project instead
  of the last homework (syllabus).
- Built from the ILOs of its two lectures (`ilos:`): practise exactly what
  the two lessons taught, in the same words. No new content.
- Size: **1–2 short, simple tasks, under 10 minutes**, in all courses. A
  student who has read the notes or gone through the interactive page must be
  able to answer at once; no research, no long calculations. Short homework that students finish is better than long homework
  they skip. I may make it longer later in the course, if the students do it well;
  then I will change this rule. Marks per task in the heading; total in `marks:`.
- At least one task in a real game situation (the PLO behind the ILO).
- Written answers only (semester 1: no programming). Code may be read, never written.
- **Fixed numbers only** ("3 steps up", "(8, 4)"): no variables like *n* in a
  task. Classes are small, so copying is not a risk now.
- **Change the numbers and situations every semester.** Old versions stay in
  the git history, and old answers go around.
- `due:` names a lecture ("before lecture 3"), never a week or a date, so
  the page works every semester and after any delay. Exact dates go on the
  e-learning platform.
- Submission: the university e-learning platform (syllabus). The page says how.
- Release: keep `draft: true` until its second lecture is taught; then remove it.
  Earlier homework stays online.
- No answers on the page: no `.match` boxes, no "Check your answers".
- **A web page that prints well.** Homework belongs to two lectures, not to
  one lesson, so it is never in a lesson PDF. The page has "⬇ Download PDF" and
  "🖨 Print homework" buttons. The PDF is the printed page itself:
  `_extensions/lesson/homework_pdf.py` (post-render) prints each homework page
  with headless Chrome, so the download and the printout are the same one A4
  page. Only `format: lesson-html`; no Typst version.
- **Answer space:** after every question, add space to write the answer:
  `{{< answer-space lines=2 >}}` (dotted lines; as many as a good answer needs)
  or `{{< answer-space box=6 >}}` (an empty box, height in cm, for a drawing).
  They appear only on paper, with a Name / Student number line at the top.
- **One A4 page:** the printed page must fit on one page.
  "How to submit" is one short line; the print layout is tight.
  If it does not fit, cut a question or use fewer lines, never a smaller font.
- The course page lists released homework after its two lectures (number, due, marks).
- Check every task like a "Try it": self-contained, one clear answer
  (or a clear marking rule), no changing state, tried before release.

## Public repo — never commit

Assignment solutions and marking notes, exam questions, question banks, grades,
student data, official internal university documents. Those live elsewhere,
privately. Homework *tasks* are public (see "Homework").
Lessons or homework not ready for students: `draft: true` (not published).

## Way of working

- Build two lectures at a time. Never generate all lessons up front.
- Phase 1: `schedule.yml` + `plan.md` per course (16-week map → ILOs, same weeks as the syllabus), approved by me first.
- Phase 2: **a typical session = the next two lectures of each course**
  (the syllabus week that holds them), each with all 3 outputs, plus one
  homework per course. Start every session by reading that week in the
  Drive syllabus.
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

- 2026-10-17: the first week 1 `game-math` lessons were too short for 90 min
  (12–21 "Try it" questions, fewer than the 60-min lessons). Size by the
  number of questions and worked examples, not only by the number of ideas.
  The size table and `check_size.py` now enforce this.
- 2026-10-17: group work and physical class activities are not always
  possible. Every lesson (both courses) ends with a "Game challenge" that each
  student does alone on the page and slides, instead of a class activity.
- 2026-10-19 (after teaching week 1): the lessons were too simple and
  repeated the same idea (2D/3D coordinates asked again and again), which
  bored teacher and students. New model: the PDF is a textbook-style chapter
  written first, the page and the slides are derived from it; one section and
  one question set per concept; figures and illustrations everywhere,
  including the slides; mini-games for concepts tied to game events. Rules
  above ("The lesson model"). The size table changed accordingly.
- 2026-10-19: a slide with a picture and text outside columns is split into
  two slides by the PPTX writer. Use columns.
- 2026-10-19: the decks were too long for the lecture once the teacher's
  Arabic explanation is counted. Slides are now the class part only (12–16
  for 60 min, 22–28 for 90 min, 2–3 questions per "Try it" slide); the notes
  and the page keep everything for home study.
- 2026-10-19: group activities are rarely done (few students, no time) and
  only look good on paper. Team work stays only where the official outcomes
  require it: one team-activity box in the notes (PDF) of one or two lessons
  per course, with an individual alternative (see each course's `plan.md`).
- 2026-10-19: the week 1 lessons followed a bachelor's model (textbook
  chapter, formal definitions first, recognition questions). The program is
  an applied diploma: lessons are now "applied first" (situation → concept →
  task, one Do it task per section, a theory budget), always within the
  official ILOs and PLOs. Rules above ("Applied first"). Tried first on one
  model lesson before it is applied to all courses.
- 2026-10-19 (model lesson review): the model was right in approach but a
  little too hard, and its English too formal. The level is now slightly
  easier (small numbers, fewer details) and the English simple (B1 in the
  notes, A2–B1 on the page and slides), with the same ILOs and PLOs. Rules
  above ("Level and language").
- 2026-10-19: the made-up game of each case study is now playable: a
  mini-game of its core part in the page's Game challenge, with its QR code
  in the notes and on the Game challenge slide (rule "The game of the
  lesson").
- 2026-10-20: the slides now show a GIF recording of each game or simulator
  being played next to its QR code, so the whole class sees the
  demonstration (rule "A recording on every slide with a QR code").
- 2026-10-20 (after release): Comet Courier sometimes did not animate (a
  negative frame index stopped its draw loop), and some questions used facts
  that the shortened pages no longer showed (Alpha and Beta, the console
  example, typical file sizes). Rules added under "Try it" and "Simulators".
- 2026-10-21: the site counts lectures, not weeks. Absences and delays move
  the courses differently, so a week number confused students and teacher.
  Lectures are numbered without gaps, homework follows every two lectures
  (due "before lecture 2k+1"), and exams are not on the site. Rules above
  ("Lectures, not weeks").
- 2026-10-21 (teacher review of the slides): some slides were keyword
  fragments that hid a question (the Game challenge story of computing
  systems lesson 2 looked like questions whose answers were on the next
  slide), and the "Do it together" bullets suggested group work. All slides
  were rewritten: complete sentences, complete questions with a question
  word and "?", the answer on the same slide, a `task` line on every
  simulator slide, Do it tasks for each student alone. The "Think" slides
  were removed (a question with no visible answer), and the slides stay
  short, so the lecture takes no longer: at most four short sentences on a
  concept slide. Rules above ("Slides explain themselves"); `check_size.py`
  checks them.
- 2026-10-19 (level check): the students' level is very basic. The most the
  lessons can be simplified without losing the ILOs and PLOs was estimated at
  about 30 %; the lessons are now about 20 % simpler, and topics that no
  syllabus week or ILO asks for are left out (rule "Scope: only what the
  outcomes need"). The notes no longer have a minimum word count: short
  notes are better than a second example of the same idea (see "No
  repetition"); only the maximum stays.
