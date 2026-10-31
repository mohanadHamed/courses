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
| `game-math` | Mathematics and Computing for Digital Games | 13411131 | 3 | 2 × **90 min** (lecture + seminar) | Dunn & Parberry, *3D Math Primer for Graphics and Game Development*, 2nd ed. |
| `computing-systems` | Fundamentals of Computing Systems and Digital Platforms | 13411133 | 2 | 2 × **60 min** (lecture + seminar) | Tanenbaum & Austin, *Structured Computer Organization*, 6th ed. |
| `digital-media` | Digital Media Technologies and Creative Production for Games | 13411134 | 2 | 2 × **60 min** (lecture + seminar) | Schell, *The Art of Game Design*, 3rd ed. |
| `digital-skills` | Digital Skills | 01101154 | 2 | **blended**: 1 × **60 min** lab lecture + 1 online activity | Evans, Martin & Poatsy, *Technology in Action*, 18th ed. (+ Microsoft Office and AI references) |

`digital-skills` is taught to the diploma students of the whole college,
most of them not in technology: it is simpler than the other courses (A2
English) and uses general examples, never the games industry. Its
`NOTES.md` has the details and overrides "Level and language" below.
Since 2026-10-23 it teaches Microsoft Office and AI tools (syllabus v2). It
is **fully practical** (2 hours in the computer lab in the study plan) and
**blended**: each week one face-to-face lab session and one online activity
(see "Blended courses: the online activity" below). It has no seminars.

**Core weeks and practice weeks.** The syllabus has 16 weeks: week 8
midterm, week 16 final. The e-learning platform has a 15-week plan. Each
course has **10–12 core weeks** (units, with all the new ideas) and fills
the rest of the 15 weeks with **practice weeks** (filling weeks: revision,
an applied problem set, a case study, a lab practice, project
presentations; no new content) and the midterm week. The materials still
cover every row of each syllabus's weekly table: every semester the dean
asks for them in the official 15-week format (see "The course package").
Use the official course names exactly.
The textbook is in `course.textbook` (`_metadata.yml`). Follow its topics and
level; never copy its text, figures or exercises.

### Units and sessions (what students see)

Jordanian semesters lose the first two or three weeks, the exams and days to
holidays, snow or absences. So each course has **10–12 core weeks** (always
taught) and **practice weeks** (taught when time allows; when a week is
lost, a practice week goes first, and nothing is missing for the students).
Lecture length does not change (90 min Game Math, 60 min the others).

- A **unit** is a core week: **Lecture N and Seminar N** (Game Math,
  Computing Systems, Digital Media: the seminar practises the lecture of the
  same week) or **Lecture N and its online activity** (Digital Skills), and
  **Homework N** (not in Digital Skills). Units are numbered 1, 2, 3 … in
  teaching order, so "Unit 5" holds Lecture 5 and Seminar 5.
- A **practice week** (a filling week) has **no new ideas**: one or two
  Practice sessions (revision, an applied problem set, a case study, project
  presentations; Digital Skills: a lab practice with an online practice
  activity). It is flexible: taught when time allows, else studied at home
  (every answer is on its page). The 15-week plan on the platform is the
  units, the practice weeks and the midterm week.
- **Session types:**

  | Type | Label | Content | Core? |
  |---|---|---|---|
  | Lecture | "Lecture N" | New ideas: the lesson model below. | Always. |
  | Seminar | "Seminar N" | **No new ideas.** Students apply the lecture of the same unit, through activities (see "What a seminar looks like"). Game Math, Computing Systems, Digital Media. | Always. |
  | Practice | "Practice N" | **No new ideas.** A practice week: revision, problems, a case study, presentations; Digital Skills: hands-on lab work. Seminar format. | Flexible. |
  | Online activity | "Online activity N" | Digital Skills: practises its unit, never repeats the lecture. Numbered 1–15 in teaching order. | Core in a unit; flexible in a practice week. |

- Lectures, seminars, practice sessions and online activities are numbered
  separately, each in teaching order; Lecture N and Seminar N are always in
  the same unit. "Which lecture did we reach?" still works.
- Every ILO keeps at least one core section at its Bloom level: no ILO
  depends on a practice week. A second application of the same idea goes to
  the seminar of the unit.
- When a syllabus week has more content than one lecture can hold, merge
  two lectures into one (at most the size of one lecture: see "Size every
  lesson") and move the second applications to the seminar; never move new
  content to a practice week.
- **The site never shows a week.** Absences move each course differently, so
  everything students see counts sessions. The course page lists the units
  ("Unit 3") and the practice weeks ("Practice week", tagged Flexible), each
  with its sessions and, for a unit, its homework.
- **Exams are not on the site.** The university sets them in its own week.
  A revision session is a practice session ("Revision of Lectures 1–7").
- **Homework U** belongs to unit U, practises Lecture U only (never a
  seminar or a practice session), and is due "before lecture N" (the next
  lecture); the last homework is due "one week after lecture N". No
  homework in a practice week.
- Pages, PDFs, slides and download names say "Lecture N", "Seminar N",
  "Practice N", "Online activity N" and "Homework U", never "Week N". Slide
  subtitles: "Lecture N", "Seminar N · practises Lecture N", "Practice N ·
  practises Lectures X–Y".
- **Folders:** `week-WW`, WW = the syllabus week whose row the unit or the
  practice week covers (the first one for a merged unit). The name is
  internal and never shown.
- `courses/<slug>/schedule.yml` lists the weeks in teaching order: units
  (`unit: N`) and practice weeks (`filling: true`), each with `week`
  (folder and syllabus row), `covers` (more syllabus rows of a merged unit)
  and its sessions (`kind`, `n`, `slot` = the syllabus column, `title`,
  `ilos`, `practises`). It is the source for the course page, the banners
  and the course package.

### Mapping the syllabus week to the sessions

- `game-math`: the syllabus has First Lecture + Second Lecture + Seminar;
  taught as one lecture (90 min) and one seminar (90 min) per week. The
  lecture of a unit covers both lecture columns of its syllabus week (two
  old lectures merged into 7 sections where needed); the seminar does the
  syllabus seminar topic. 12 units (syllabus weeks 1–7 and 9–13) and 3
  practice weeks (8: revision; 14 and 15: problem set, case studies, course
  revision).
- `computing-systems`, `digital-media`: Lecture + Seminar per week. 12 units
  (one merged unit covers two syllabus weeks: Computing Systems 5–6, Digital
  Media 13–14) and 2 practice weeks (syllabus week 15: case studies or the
  team workshop, and the presentations), with the midterm week.
- `digital-skills` (blended, fully practical): Lecture 1 of the syllabus is
  the face-to-face lab session (a lecture in a unit, a practice session in a
  practice week); Lecture 2 is the online activity. 10 units and 5 practice
  weeks (8, 10, 12, 14, 15).
- Exam sessions get no session. Confirm with me when a syllabus week is
  unclear. The maps are in each course's `plan.md`.

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

In a fully practical course (now `digital-skills`) every lecture also has a
**worksheet** (`lesson-NN-sheet.qmd`), the main document of the session,
like the manual of a lab experiment; its notes are then a short reference
and its main button is "Worksheet (PDF)" (see "Lecture worksheets").

### The page teaches, the notes test

- **The interactive page is the study version:** a simplified copy of the
  notes in which every question and task has an immediate answer with a
  short reason. No student is left stuck.
  - Every Try it question has a `Why:` reason (see "Try it"). After two
    wrong tries the page shows the right answer with its reason.
  - Every Do it, Lab task, Activity and Task with AI box has a
    `::: {.check}`: "Check your result", closed until the student opens it.
    A fixed task: the result and one line of why. A personal task (their
    phone, their premise): "A good answer looks like …" and a 2–3 point
    self-check list.
  - A prose question on the page is answered in the text itself.
- **The PDF is the self-test:** questions inside the lesson, answers at the
  end. `book.lua` moves every `.check` of the notes to "Results of the Do it
  tasks" ("Results of the activities" in a seminar), next to "Answers to the
  exercises"; `Why:` is not printed.
- **Graded work stays unanswered:** the homework and the "Tasks to submit"
  of online activities have no `.check` and no `Why:`. Their solutions are
  in `courses-private`.
- `check_size.py` warns about a task without `.check`, a Try it question
  without `Why:`, and answers in graded work.

### What a seminar looks like

A seminar (and a practice session, in the same format) has **no new
ideas**: students apply the lectures they already had. A seminar practises
the lecture of its unit; a practice session (a practice week) revises or
applies several lectures. It must look like a seminar or a practice session
in its title, label, grouping and slides, so a teacher knows at once that it
is activity-based. Templates: `seminar-template.qmd`,
`seminar-book-template.qmd`, `seminar-slides-template.qmd`.

- **Files:** `seminar-NN.qmd` (page), `seminar-NN-book.qmd` (worksheet,
  PDF), `seminar-NN-slides.qmd`; a practice session `practice-NN*`. Front
  matter `seminar: N` (or `practice: N`); what it practises comes from
  `schedule.yml`. The banner shows "Seminar 2 · practises Lecture 2", or
  "Practice 1 · practises Lectures 1–7" and "Flexible"; a practice page says
  in one line that it is studied at home when it is not held.
- **Short, with room to explain.** Most students cannot solve a seminar
  problem alone, even with its answer on the page: the teacher explains
  almost every problem before and after the students try it. So a seminar
  is **two short problems** (three only when two cannot hold the concepts),
  each with little effort and little time, that **together use every
  concept of the lecture(s) it practises**. The planned time (Recall and the
  activity times) is about **40 minutes of a 60-min seminar** and about
  **60 minutes of a 90-min seminar**; the rest is for the teacher's
  explanations. A problem is short when it has one situation, two to four
  steps and one small product; never a second problem on the same concept.
- **Structure:**
  1. **Recall** (about 5 min): 3 key ideas of the lectures it practises
     and one Try it with 2–3 questions. No new terms and no glossary.
  2. **Activities** (`## Activity N · title`): 2 (at most 3). Each has a
     short game (or workplace) situation, an
     `::: {.callout-note title="Activity N · title · 15 min"}` box with a
     task for each student alone and a concrete product, its `.check`, and
     one Try it with 2–3 questions (with `Why:`). Seminars are where the
     syllabus seminar titles are done ("Matrix exercises", "Drawing a
     storyboard from a scene"). The unit's mini-game, when it fits, is the
     tool of an activity; a seminar has no separate Game challenge.
  3. **At home** (optional, `## At home · Task with AI`): at most one Task
     with AI, outside the planned time.
  4. **Wrap-up** (`## Wrap-up {.summary}`): 2–3 lines, "what you can now do".
- **Worksheet (PDF):** Recall, the activities, 3–5 short exercises;
  "Answers to the exercises" and "Results of the activities" at the end.
  No case study.
- **Slides teach by asking:** a Recall slide (questions on the earlier
  lectures, `.answer` cards); per activity a Task slide ("Activity 2 · …
  · 15 min": the situation, the instruction, the product) and a Check slide
  (the result, `.reveal` step by step); a Live demo slide for a simulator
  the activities use; a Wrap-up. `pptx_finish.py` puts a "SEMINAR" (or
  "PRACTICE") mark on every slide.
- **Team work** stays only in the notes or the worksheet of the session that
  `plan.md` names, with an individual alternative.

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
  same box is called "Lab task", and in a lecture with a worksheet it is the
  experiment of the section). Short (2–5 minutes), done alone, on things
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
- No religious symbols, and nothing that looks like one. Above all, never a
  cross shape: an upright stroke with a crossbar. An antenna is a tower (two
  legs meeting at the top, a light and radio waves), not a mast with bars;
  a kite has two coloured halves, not two sticks; a gamepad's direction pad
  is four small arrows; first aid is a box with a heart or the words "first
  aid", never a red cross. `_extensions/lesson/check_figures.py` (project
  pre-render) warns about cross shapes in every figure, poster and
  simulator; fix every warning before a PR.

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
| Notes: numbered sections (`## 1.1`) | 3–4 | 4–7 |
| Notes: words (without exercises and answers), at most | 3 500 | 6 000 |
| Notes: worked examples | 2+ | 4+ |
| Notes: exercises (with short answers at the end) | 6–10 | 10–16 |
| Page: "Try it" boxes (one per section + Game challenge) | 4–6 | 6–9 |
| Page: questions in all "Try it" boxes | 15–28 | 30–45 |
| Simulators / mini-games | 0–4 | 1–3 |
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

**Seminars and practice sessions** (short, with room for the teacher's
explanations; see "What a seminar looks like"):

| | 60 min | 90 min |
|---|---|---|
| Activities (`## Activity N`) | 2–3 | 2–3 |
| Planned time: Recall 5 min + the activity times, at most | 40 min | 60 min |
| Try it questions | 6–12 | 8–15 |
| Slides (title slide not counted) | 5–9 | 6–10 |
| Worksheet words, at most | 1 200 | 1 600 |

**Lecture worksheets** (a practical course, 60 min): one experiment per
section (3–4), 2–5 steps in each, about 40 minutes of experiments, at most
1 600 words without the results. The slides stay within 10–16.

`_extensions/lesson/check_size.py` (project pre-render) checks these numbers,
that every section of the notes is on the page, the one-box-per-section rule,
one "Do it" (or "Lab task") box in every section of the notes and the page,
the required parts (notes: Key terms, Exercises, Answers to the exercises;
page: Key terms, Game challenge, Summary) and one "Live demo" slide per
simulator. Fix every warning before you open a PR. Full table:
`python3 _extensions/lesson/check_size.py --all`. Keep `SIZES` and this table
the same.

### Lecture worksheets (a practical course)

A lecture of a fully practical course (now `digital-skills`) is built
around a **worksheet**, like the manual of a lab experiment. It is the main
document of the session: students follow it during the lecture, do each
step on the computer and record what they see, as they would record
measurements. Template: `shared/templates/sheet-template.qmd`.

- **File:** `lesson-NN-sheet.qmd` (`format: lesson-typst`, the same
  `lesson:` and `ilos:` as the lecture) → `<prefix>_lectureN_sheet.pdf`.
  The page shows "Worksheet (PDF)" as its first button, and the course page
  a "Worksheet" link (the notes link is then "Notes").
- **Parts:** the goal (the ILO card, added by `banner.lua`, with a QR card
  to the page); `## Before you start` (what you need, the time, how to
  check, and `{{< start-files >}}`); then **one experiment per section** of
  the notes, `## Experiment N · short title`, with an `**Aim:**` line (the
  section of the notes and the minutes) and **2–5 numbered steps**. After
  each step: a place to record the result, `{{< record "D2 shows" >}}` (a
  value, a formula, an observation, a file name; `lines=2` for a sentence,
  `box=4` for a sketch), and its `::: {.check}`. At the end
  `## Table of results`: a short table in `::: {.record-table}` (what to
  record, an empty "Your result" column) that the teacher checks before the
  end of the lecture; then one line pointing to the Game challenge.
- **Start files:** when the steps need data, every student gets the same
  file. List it in the front matter (`start-files:` with `name` and
  `about`); the file is in `week-WW/files/`, written by
  `tools/start_files.py` (change the numbers there and in the worksheet
  together, then run it).
- **Real apps or simulators,** chosen by the nature of the lecture and
  written in `plan.md`: the steps run in Word, Excel, PowerPoint or an AI
  tool, on the simulators of the interactive lesson, or a mix. A real app
  comes first when the lab has it; a simulator is the teacher's
  demonstration and the way to do the step without the app.
- **The page teaches, the worksheet tests.** The interactive lesson shows
  each experiment in its section with `{{< experiment N >}}`, read from the
  worksheet (written once): a text field after each step (kept in the
  student's browser only) and "Check your result". `{{< experiment results >}}`
  shows the table of results. In the PDF, `book.lua` moves every result to
  "Results of the experiments" ("Experiment 2 · Step 3"), on a new page.
- **Done and checked in class, never uploaded.** The worksheet is not
  homework and has no marks; the online activity is the graded work of
  the unit.
- **The notes are a short reference:** definitions, worked examples, common
  mistakes, the case study, the exercises. Each section ends with one line
  that points to its experiment (*In class: Experiment 2 of the worksheet,
  …*) instead of a Lab task.
- **The slides are the teacher's demonstration of the worksheet:**
  Keywords; "Before you start" (the start files, the figure
  `week-01/images/worksheet-steps.png`); for each experiment an
  "Experiment N · …" slide (the idea in one sentence and the steps, each
  with its question; a picture in the other column) and a "Check N · …"
  slide (the results, step by step, in `.reveal`); a Live demo slide for
  each simulator; the Game challenge and its Try it slide; a "Table of
  results" slide; the Summary. The Try it questions of the sections stay on
  the page (home study).
- `check_size.py` checks it: an experiment for every section of the notes,
  an Aim and 2–5 steps in each, a record field and a check after every
  step, the table of results, the start files, the experiments on the page
  and in the notes, an Experiment and a Check slide for each, and at most
  1 600 words (without the results).

### Blended courses: the online activity

A blended course (`course.blended: true`; now `digital-skills`) is fully
practical and has one face-to-face lab session and one online activity in
every week. In a unit the face-to-face session is a lecture (a full lesson
with all three outputs); in a practice week it is a practice session
(seminar format, no new ideas). The online activity (`kind: online` in
`schedule.yml`) is **one page**, `online-NN.qmd` with `online: N`, `due:` and
`marks:` in the front matter (template: `shared/templates/online-template.qmd`).
It **practises its unit** and never repeats the face-to-face lecture; in a
unit it may add a skill of the unit's syllabus row, in a practice week it
adds nothing new:

- "Before you start" (what you need, about how long, what you submit);
- 2–3 short **Steps** marked `{.study}`: a plain explanation, a figure, a
  simulator to try at once, one "Try it" self-check each, with `Why:`, and
  a `.check` where a step asks for a result (a video, if the teacher has
  one, is linked on the e-learning platform);
- **Tasks to submit** (`{.tasks}`): 2–4 practical tasks with marks and a
  concrete product (a named file, a screenshot, a short answer), with
  `{{< answer-space >}}` for the printed copy; then "How to submit".

The page has "Download tasks (PDF)" and "Print tasks" buttons; on paper only
the tasks are printed (`homework_pdf.py` prints it as
`<prefix>_onlineN_tasks.pdf`). The online activity **replaces the
homework** of that course. Its model answers stay private in
`courses-private` (`week-WW/online-NN-solutions.md`). `check_size.py` checks
its parts and that it has at least two simulators.

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

Course-specific notes: `courses/<slug>/NOTES.md`. Unit map:
`courses/<slug>/schedule.yml` (sessions, titles, ILOs) and
`courses/<slug>/plan.md`.

## Tasks with AI

Students have AI assistants. A lesson that only asks simple questions lets a
student paste them into an AI and learn nothing, and asking an AI to explain
the lesson needs no lesson. So lessons are built **for a world with AI**:
some tasks are set at a **higher level than a student could reach alone in
the time**, with guidance on how to reach it with an AI assistant and how
to check its work. The student uses AI to do more, not to do the work for
them, and learns to use AI well.

```markdown
::: {.callout-note .ai-task title="Task with AI · Simulate 1000 loot drops"}
**Goal:** a sheet that rolls 1000 drops of the loot table and compares them
with the expected numbers.

1. **Ask the AI:** start with this prompt and add your table.

   ::: {.prompt}
   Write spreadsheet formulas that roll one loot drop per row …
   :::

2. **Do it yourself:** paste the formulas, fill 1000 rows, count each item.
3. **Check:** work out by hand the expected number of rare drops
   (1000 × 5 % = 50). Your sheet must give about 50. If not, find the
   mistake in the AI's formulas.

*Your product:* the sheet, and one sentence on what the AI got wrong or what
you changed.

::: {.check}
A good sheet … (2–3 point self-check list)
:::
:::
```

- **A product beyond the usual level, inside the ILOs of the session**
  (never a topic of a later week): long or hard by hand, for example 1000
  random rolls, a five-phone comparison table, a story with three endings
  and its storyboard, a licence audit of 20 assets.
- **A starter prompt** (`::: {.prompt}`; the page adds "Copy prompt").
- **The student's own part:** they build, change, choose or decide.
- **A check with the tools of the lesson:** a value worked by hand, a
  simulator, GeoGebra, the maker's page, the official source. The AI can be
  wrong; finding where is part of the task.
- **A product**, and one sentence on what the AI got wrong or what the
  student changed.
- On the page and in the notes the box has a `.check`. In graded work
  (homework, Tasks to submit) it has none and asks for the **AI-use
  statement** (which tool, what was asked, what the student changed).
- **0–2 per session**, only where AI really lets students do more: often
  the Game challenge of a lecture, the "At home" part of a seminar (at most
  one there) or a homework task. Not on the slides.
- Free tools named generally (Microsoft Copilot with the university
  account, ChatGPT, Gemini); no task needs a paid plan. No personal data in
  a prompt.
- Never AI images, sound or video as a student's media product in Digital
  Media (unclear rights, and it skips the production ILOs); they are a case
  in the IP sessions.
- The rule "no tool or assistant names" (Site identity) is about how the
  lessons are made, not about the tools students use.
- `check_size.py` warns above 2 per file and about a box without `.prompt`
  or a check step (and, in graded work, without the AI-use statement).

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

The students' starting level is very basic. Since 2026-10-30 the lessons
are **as simple as the outcomes allow**: the estimated limit, about 30 %
simpler than the first applied version of the lessons (October 2026), which
was already slightly easier than a first-year bachelor's course. Beyond it,
syllabus topics, the ILO verb or the practical tasks would be lost. The ILOs
and PLOs stay exactly the same: a lesson is easier in *how* it teaches,
never in *what* the ILO asks for. Explain each idea in the simplest way, and
teach only the simplest concepts that still reach every ILO at its Bloom
level and serve the PLO behind it.

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
- **English (notes):** CEFR A2–B1. Short sentences (about 15 words at most,
  one idea each), the most common words, active voice ("the CPU reads the
  value", not "the value is read"), no idioms. Explain every technical word
  in plain words the first time it appears, then use the same word every
  time.
- **English (page and slides):** A2: even shorter sentences (about 12
  words) and lists.
- Definitions stay precise, but in the same simple English.
- No programming yet: *Programming Fundamentals (1)* (C#) is in semester 2.
  Code in semester-1 courses is a short C# example to read, never a task,
  and every code word is explained.
- Do not teach a game engine's interface (Inspector, GameObject, …): Unity
  has its own course. Engine conventions (axes, handedness, `Vector3`) are fine
  as examples.

## Writing rules (always enforce)

- **Notes:** simple English (A2–B1, see "Level and language"): short
  paragraphs, direct steps. Precise
  definitions (`::: {.callout-important title="Definition 1.2 — …"}`), worked
  examples with numbered steps (`::: {.callout-note title="Example 1.3 — …"}`),
  common mistakes (`::: {.callout-warning title="Common mistake"}`), code
  (`::: {.callout-caution title="In game code"}`), figures with captions and
  `@fig-` references, tables with captions, `::: {.lead}` opening paragraph,
  `::: {.answers}` for the short answers.
- **Page:** the same content, shorter and plainer (A2): one idea per
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

## Three outputs per session

Folder: `courses/<slug>/week-WW/`, one folder for each unit, WW = its
syllabus week (see "Units and sessions"). NN in the file names is the number
of the session within its kind. Figures in `week-WW/images/`, simulators and
mini-games in `week-WW/sims/`. Images and simulators move with their session.

| File | Format | Output |
|---|---|---|
| `lesson-NN-book.qmd` | `lesson-typst` | Lesson notes, PDF (the main text) |
| `lesson-NN.qmd` | `lesson-html` | Interactive lesson page |
| `lesson-NN-slides.qmd` | `lesson-pptx` | Slides (.pptx), public summary |
| `seminar-NN-book.qmd`, `seminar-NN.qmd`, `seminar-NN-slides.qmd` | the same | Seminar worksheet, page and slides (Digital Skills: `practice-NN*`) |
| `lesson-NN-sheet.qmd` | `lesson-typst` | Lecture worksheet, PDF (Digital Skills: the main document of the session) |
| `online-NN.qmd` | `lesson-html` | Online activity (Digital Skills) |
| `homework-UU.qmd` (UU = unit) | `lesson-html` | Take-home task page with Print and Download PDF buttons |

- **Download names.** Files students download have meaningful, unique
  names: `math_lecture5.pdf` (notes), `math_lecture5_slides.pptx` (slides),
  `math_seminar2.pdf`, `math_seminar2_slides.pptx`, `math_homework1.pdf`,
  `digital_skills_practice3.pdf`, `digital_skills_online4_tasks.pdf`,
  `digital_skills_lecture6_sheet.pdf` (a lecture worksheet). N is
  the number without a leading zero; the prefix is `course.file-prefix` in
  `_metadata.yml` (`math`, `computing_systems`, `digital_media`,
  `digital_skills`). `download_names.py` (post-render) renames the rendered
  files; `banner.lua` and `{{< schedule >}}` link the same names. Keep the
  source names (`lesson-NN-book.qmd`) as they are.
- Start from `shared/templates/book-template.qmd`, `lesson-template.qmd`,
  `slides-template.qmd`, the three `seminar-*` templates,
  `online-template.qmd` and `homework-template.qmd`.
- Formats, styles and filters live in the Quarto extension `_extensions/lesson/`
  (Quarto requires `_extensions/` at the project root). Change look and
  behaviour there, once, for every course.
- The formats add the course banner (course name, diploma line, lecture
  number, ILOs) automatically from metadata.
- PDF engine: Typst. Main font Noto Sans; Arabic font Noto Naskh Arabic
  (installed in CI from `fonts-noto-core`). Book filter: `book.lua`
  (`.lead`, `.answers`, `.check` results, `.prompt`); callout styles:
  `typst-body.typ`.

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

    Why: one sentence, in the words of the lesson.

Second question.
:   its answer

    Why: one sentence.
:::
:::
```

- Each question is followed by its right answer (`:   answer`). The page shows
  every different answer once as a button, in random order.
- **Every question has a reason** (`Why:`, indented under the answer): one
  sentence in the words of the lesson, why the answer is right (or why a
  tempting answer is wrong). The page shows it after the right answer, or
  after two wrong tries together with the right answer. The notes do not
  print it.
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
  `try/catch`, so one failed frame never stops the game. Use one clock:
  `performance.now()` for the start of an animation and for the frame time.
  In a lesson page the browser can give `requestAnimationFrame` a time many
  seconds behind `performance.now()`, so `sim-base.js` (loaded before the
  simulator's own script) passes `performance.now()` to every frame. Still
  clamp times (`Math.max(0, now − start)`). Never decide a result
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

- `courses/<slug>/schedule.yml` lists every week in teaching order: units
  and practice weeks (see "Units and sessions"); no exams. The course page
  shows it with `{{< schedule >}}`: one card per unit ("Unit 3") with its
  homework, and one dashed card per practice week ("Practice week", tagged
  Flexible). Each session is labelled "Lecture N", "Seminar N", "Practice N"
  or "Online activity N"; a session whose `.qmd` exists and is not a draft
  is bright, with links (page, PDF, slides); the others are faded ("Coming
  soon").
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
the same paths: `courses/<slug>/week-WW/homework-UU-solutions.md`. Change a
homework and its solution together.

- **One homework per unit** (not in a blended course: there the online
  activity takes its place): homework U belongs to unit U
  (`courses/<slug>/week-WW/homework-UU.qmd`), from
  `shared/templates/homework-template.qmd`. None in a practice week;
  computing-systems and digital-media: the project in the practice weeks
  (syllabus).
- Built from the ILOs of the lecture of its unit (`ilos:`): practise exactly
  what it taught, in the same words, never a seminar or a practice session.
  No new content.
- **With AI in mind** (see "Tasks with AI"): where a short question could be
  pasted into an AI and answered without learning, prefer one Task with AI
  at a higher level, which asks for the AI-use statement. The page says:
  "You may use AI where a task says so. Check its work and say how you used
  it." The homework stays light: students who finish it quickly do it.
- Size: **1–2 short, simple tasks, about 10 minutes, never more than 15**,
  in all courses, a Task with AI included (at most one per homework, small).
  Shorter is better: never make a homework longer than it is. A
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
- `due:` names a lecture ("before lecture 3": the lecture of the next unit;
  the last one "one week after lecture 12"), never a week or a date, so
  the page works every semester and after any delay. Exact dates go on the
  e-learning platform.
- Submission: the university e-learning platform (syllabus). The page says how.
- Release: homework is published together with its unit, when the
  PR is merged (see "Release: no drafts"). Earlier homework stays online.
- No answers on the page: no `.match` boxes, no "Check your answers".
- **A web page that prints well.** Homework belongs to a unit, not to one
  lesson, so it is never in a lesson PDF. The page has "⬇ Download PDF" and
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
- The course page lists released homework in its unit card (number, due, marks).
- Check every task like a "Try it": self-contained, one clear answer
  (or a clear marking rule), no changing state, tried before release.

## The course package (for the dean, every semester)

The college asks every semester for the complete materials of each course,
organised by the official weekly plan of its syllabus.

- The weekly table of each syllabus is copied **word for word** into
  `courses-private/courses/<slug>/syllabus-weeks.yml` (private; this repo
  keeps only titles and ILO codes).
- After a full `quarto render`, `python3 tools/course_package.py` writes
  `_package/<slug>/` (not in git): one folder per syllabus week with its
  PDFs, slides, homework and the addresses of its pages, and `index.html` /
  `index.pdf`: the syllabus table exactly as approved, with one added
  **Materials** column (Lecture 8, Seminar 8, Practice 1 (flexible),
  Online activity 5, Homework 5). A merged unit is listed in every row it
  covers; the practice weeks fill the rows of the case studies, revisions
  and presentations.
- The script checks that every teaching row has its material and that every
  session belongs to exactly one row. Fix every problem before sending it.

## Public repo — never commit

Assignment solutions and marking notes, exam questions, question banks, grades,
student data, official internal university documents (also the syllabus
tables of the course package). Those live elsewhere, privately. Homework *tasks* are public (see "Homework").
Nothing unfinished goes to `main`: the PR review is the check (see "Release:
no drafts").

## Way of working

- Build one unit at a time. Never generate all lessons up front.
- Phase 1: `schedule.yml` + `plan.md` per course (the units of the 16-week
  syllabus → sessions → ILOs), approved by me first.
- Phase 2: **a typical work session = the next unit of each course**, each
  session with all its outputs, plus its homework. Start by reading that
  week in the Drive syllabus.
- I review every lesson in its PR before I merge it; merging is the release.
  Ask before big structural decisions.

### Release: no drafts

New lectures, online activities and homework are written **without**
`draft: true` and are published when I merge their PR. The course page then
shows them at once (homework in its unit), so students can study
ahead. Use `draft: true` only when I ask for it for one file; the templates
do not add it. The draft mechanism still works (a draft lecture is faded,
"Coming soon", and `--profile review` shows it).
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
- Review a PR before merging it: check out the PR branch, run
  `quarto render` once (the preview alone does not build the PDFs), then
  `quarto preview`. Add `--profile review` to both only if a file has
  `draft: true` (`_quarto-review.yml` shows drafts).
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
- 2026-10-23: Digital Skills became a blended course built on the
  university description *Smart Digital Skills* (Office and AI, at least a
  quarter AI). New page type: the online activity (rules above, "Blended
  courses"), which replaces the homework there. The teacher asked for as
  many simulators as possible, so a 60-min lesson may now have up to four.
- 2026-10-23: no drafts. Lectures and homework are published when their PR is
  merged; the PR review is the check before release. Homework no longer waits
  until its second lecture is taught (rule "Release: no drafts").
- 2026-10-24 (teacher review): most mini-games did not work inside the
  lesson page, only with "Open full screen". In an embedded (lazy) iframe,
  Chrome gave the game loop a frame time about 17 s behind
  `performance.now()`, so animations that started at a click stood still.
  `sim-base.js` now gives every frame `performance.now()`, stops Space and
  the arrow keys from scrolling the page, and keeps `focus()` from scrolling
  the page; on a phone, a simulator takes the whole width of the screen.
  Test every new simulator inside the page, not only on its own.
- 2026-10-28 (plan `plans/restructure-19-lectures.md`): semesters lose two
  or three weeks plus holidays, the students are weaker than expected, and
  the dean checks the materials against the 15-week syllabus. The courses
  are now organised in units (one per syllabus week) with about 19 core
  sessions and flexible seminars or practice sessions; the interactive page
  answers every question and task (`Why:`, `.check`), while the PDF stays a
  self-test; content beyond the ILOs was cut and second applications moved
  to the seminars. Students have AI assistants, so some tasks are now set at
  a higher level and done with AI, with a check step (not "explain it to
  me" prompts, which every student can do alone). Rules above ("Units and
  sessions", "The page teaches, the notes test", "What a seminar looks
  like", "Tasks with AI", "The course package").
- 2026-10-30 (teacher review of the first seminars): the seminars were too
  long for the class. Most students cannot solve a seminar problem alone, so
  the teacher explains almost every problem, and that takes time. A seminar
  is now two short problems (three at most) that together use every concept
  of the lecture it practises, planned for about 40 of 60 minutes (60 of 90),
  with no separate Game challenge or case study; a Task with AI is an
  optional "At home" part. The lessons are now as simple as the outcomes
  allow (the estimated limit, about 30 % simpler than October 2026), with
  A2–B1 English in the notes and A2 on the pages and slides. Rules above
  ("What a seminar looks like", "Level and language").
- 2026-10-31 (Digital Skills, lecture worksheets): the course is fully
  practical, so every lecture is now built around a worksheet, like the
  manual of a lab experiment: 3–4 experiments (one per section), numbered
  steps done on the computer (a real app, a simulator or both), a place to
  record the result of every step, start files with the same data for
  every student, and a table of results that the teacher checks in class.
  The page shows the same experiments with a check after every step; the
  notes became a short reference; the slides demonstrate the worksheet.
  Rules above ("Lecture worksheets").
- 2026-10-31 (teacher's review of the order, plan v3): the seminars were
  scattered (Game Math went Lecture 1, Seminar 1, Lectures 2–7, then a
  seminar), and the 15 units mixed core and flexible sessions. Now every
  week is one lecture and one seminar that practises it (Game Math, Computing
  Systems, Digital Media) or one lab lecture and one online activity
  (Digital Skills, fully practical, no seminars). Each course has 10–12 core
  weeks (units) and practice weeks without new content that fill the
  15-week plan of the platform and are dropped first when weeks are lost.
  Game Math merged the two lectures of four syllabus weeks; Computing
  Systems and Digital Media merged one pair each; Digital Skills turned the
  PivotTable practice into Lecture 10. Rules above ("Units and sessions",
  "Mapping the syllabus week", "What a seminar looks like", "Blended
  courses", "Homework", "Course pages and the schedule").

