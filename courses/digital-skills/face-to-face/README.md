# Digital Skills — the face-to-face version (prepared, not published)

The blended course (one face-to-face lab lecture and one online activity
each week) is the approved course and stays on the site. The college may
turn Digital Skills into a **fully face-to-face** course, if the students
ask for it. This folder holds that version, written in advance from the
approved blended content, so that the site can be switched quickly.

- **Not on the site.** `_quarto-site.yml` (the default profile: CI,
  `quarto render`, `quarto preview`, `--profile review`) leaves this folder
  out, so nothing here is built or published. No page of the site links
  here.
- **Preview** (the teacher's check):

  ```bash
  quarto render --profile f2f
  ```

  ```bash
  quarto preview --profile f2f
  ```

  Then open `courses/digital-skills/face-to-face/index.html`: the course
  page of this version, with every session that is written.
- **Check** every session against the rules below (run it by hand, from
  the project root):

  ```bash
  python3 courses/digital-skills/face-to-face/check_f2f.py
  ```
- The rules of `AUTHORING.md` and `../NOTES.md` hold here too (A2 English,
  general examples, the page checks every task, slides that explain
  themselves), except where this file says otherwise.

## The model: two sessions in the lab every week

Study plan: 2 credit hours, fully practical (2 hours in the computer lab).
Face-to-face: **every week has two sessions of 60 minutes** (the two
lecture columns of the syllabus). Each session has three parts:

| Part | File | Output | In class |
|---|---|---|---|
| Slides | `lesson-NN-slides.qmd` | `digital_skills_lectureN_slides.pptx` | First, the teacher explains the new ideas. |
| Worksheet (the manual) | `lesson-NN-sheet.qmd` | `digital_skills_lectureN_sheet.pdf` | Then the students practise the same ideas. Printed, or read on the screen. |
| Interactive lesson | `lesson-NN.qmd` | `lesson-NN.html` | The same ideas in short points, the simulators, a check after every step. Home study. |

**Time (the teacher's rule of 2026-11-06).** A session is 60 minutes, but
a lecture rarely has the full hour: it starts late, a question or a
problem takes longer. So every session is sized for **about 20 minutes of
slides** and **a worksheet that a good student finishes in about 20
minutes**. The other 20 minutes are room for the delays and the slower
students. **The content never says this:** no page, worksheet, slide or
figure gives the minutes of a part (no "about 20 minutes", no times in the
Aim lines). Only the length of the whole session appears (the chip "60
min" on the page), so the session never looks shorter than an hour.

A practice week has two lectures with no new ideas: the same three files
(`lesson-NN…`), and in `schedule.yml` the lectures that they practise
(`practises`). Lecture 15 is the model:

- **slides:** 2–3 **Recall** slides (questions on the lectures it
  practises, with `.answer` cards), one Live demo, the Summary, Your
  worksheet and the Results; no Keywords;
- **worksheet:** 2–3 experiments, each with Part A and Part B; "**The idea
  (Lectures X–Y):**" recalls what the experiment uses;
- **page:** `## Recall` (the main ideas in short points, no Key terms),
  then one section per experiment, `## 15.1 …` (with its experiment and one
  Try it), the table of results and `## Wrap-up {.summary}`.

**No lesson notes.** The worksheet takes the place of the notes (PDF): the
course is practical, so the main document is a manual of experiments, not
a text to study for the exam. Each experiment starts with its idea in one
or two sentences, so the worksheet and the slides together hold every
concept.

### The worksheet: Part A in the app, Part B on a simulator

Every experiment has two parts:

- **Part A · In the app:** numbered steps in the real app on a computer (the
  lab computer, or any computer with Office or Office on the web): open
  Excel, type the prices, add them with AutoSum; open Word, type the
  paragraph, change the font and the size.
- **Part B · On the simulator:** one step on a simulator of the
  interactive lesson. Its box (`{{< sim >}}` in the worksheet) has the
  poster, a **QR code** (on paper: scan it with the phone) and a **link**
  (on the screen: click it). Both open the simulator on the interactive
  lesson (`lesson-NN.html#sim-name`), right above the checks of its steps.

Where a session has no simulator for an idea, Part B is one short step
on the phone (the same app or site on the phone, for example signing in
with the university account in Lecture 2).

So the worksheet works in every case:

| The student | Part A | Part B |
|---|---|---|
| reads it on the lab computer | does it in the app | clicks the link |
| has it on paper in the lab | does it in the app | scans the QR code |
| has no lab computer (the lab is not ready) | later, on any computer | scans the QR code or clicks the link, also on a phone |

The two labels are `::: {.part}` divs (book.lua keeps each one on the
page of what follows it; a small band on the page). Each step has a
`{{< record >}}` field, its closed `::: {.check}` (printed
at the end: "Results of the experiments") and one interactive check for the
page (`.choice`, `.order`, `.sort` or `.fill`), as in AUTHORING.md
("Lecture worksheets"). The steps are numbered through the experiment
(Part B goes on with the numbers of Part A: `4.`), so every result has its
own label ("Experiment 2 · Step 4").

Template of one experiment:

```markdown
## Experiment 1 · Short title

**The idea:** the concept of the slides in one or two sentences.

**Aim:** what you find out (no minutes).

::: {.part}
**Part A · In the app (Excel)**
:::

1. One action in the app, with the exact cell, button or words.

   {{< record "What you record" >}}

   ::: {.check}
   **The result**, and one line of why.
   :::

   ::: {.fill answer="150"}
   The question about the result?

   Why: one sentence.
   :::

::: {.part}
**Part B · On the simulator** (no computer? do it on your phone)
:::

{{< sim file="../../week-01/sims/time-saver.html" poster="../../week-01/sims/time-saver.png" title="Time Saver: by hand or with an app?" >}}

2. One action on the simulator, and what to look at.

   {{< record "What you see" >}}

   ::: {.check}
   The result.
   :::

   ::: {.choice}
   …
   :::
```

- **Size:** a good student finishes both parts in about 20 minutes:
  **3 experiments**, each with **2 short steps in Part A** (3 only when
  they are very short, like one click) and **1 step in Part B**; about 8–10
  steps in all, at most about 1 200 words without the results. Then the
  **Table of results** (`::: {.record-table}`, one row for each key
  result, marked "1 A", "1 B" …), which the teacher checks before the
  end. A Game challenge goes after the table, for students who finish
  early ("Finished early? Play …").
- **Before you start:** what you need, what to do without a lab
  computer, how to check, and
  `{{< start-files >}}`. The start files stay in the blended week folders:
  `start-files-dir: "../../week-WW/files"` in the front matter of the
  worksheet (`tools/start_files.py` writes them).
- A Game challenge (a mini-game) of the blended lecture stays: on the page,
  and after the table of results of the worksheet, with its QR code and
  link, for the students who finish early.

### The slides: the new ideas, for about 20 minutes

The teacher explains first, then the students do the worksheet. The deck
follows the order of the session (no minutes on any slide):

1. **Keywords** (the glossary of the lecture).
2. For each experiment of the worksheet: a **concept slide** (the idea in
   at most four sentences, with its figure, in columns), the **Live demo**
   of its simulator (the same `{{< sim >}}` with a `task` and its
   `answer`), and a **Try it** slide (2–3 questions with `.answer` cards).
   A short example (`## Example · …`, 3–4 steps in `.reveal`) may take the
   place of the Live demo where the idea needs it.
3. **Summary** (5–6 sentences): the end of the explanation.
4. **Your worksheet** (on the screen while the students work): Part A and
   Part B, the start files, and the QR code of the interactive lesson in
   the other column (`{{< page-qr >}}`), so that every student can open
   the page and its simulators on the phone.
5. **Results of the worksheet** (at the end of the session): the key
   results, one `.reveal` line for each experiment.

Where a section has no figure, its concept slide shows the poster of its
simulator, and the Live demo slide of that simulator is left out (two
pictures of the same simulator on two slides in a row): the students open
it from the worksheet. A figure made for this version goes in
`face-to-face/images/` (SVG and PNG; `check_figures.py` checks it).

About 10–13 slides (title slide not counted): 3 sections of 3 slides, the
Keywords, the Summary, the worksheet and its results. No Experiment or
Check slides: the worksheet is done after the explanation, not step by
step with the teacher. The rules of "Slides explain themselves" hold.

### The interactive lesson

The same as a blended lecture page, with the new worksheet:

- the first lines say how the session works (the slides, then the
  worksheet: Part A in the app, Part B on the simulators of this page);
- **Key terms**, **Before you start** (the start files and the figure
  `../images/how-it-works.png`);
- one section per experiment: the idea in short points, its figure, its
  simulator(s), a "Watch out!" where it helps, `{{< experiment N >}}`
  (the steps of Part A and Part B with their checks) and one **Try it**;
- `{{< experiment results >}}` (the table of results), the Game challenge
  (if the blended lecture has one) and the **Summary**.

## The 30 sessions, written from the blended sessions

`schedule.yml` holds the map (`from`: the blended session). Every session
is a lecture, and the lectures are numbered in one sequence: week w holds
Lecture 2w − 1 (from the face-to-face session of the blended week) and
Lecture 2w (from its online activity), so the number of a lecture always
gives its week. The lectures of a practice week (weeks 8, 10, 12, 14 and
15) have no new ideas: they practise the lectures before them.

| Week | Session 1 (from) | Session 2 (from) |
|---|---|---|
| 1 | Lecture 1 (Lecture 1) | Lecture 2 (Online activity 1) |
| 2 | Lecture 3 (Lecture 2) | Lecture 4 (Online activity 2) |
| 3 | Lecture 5 (Lecture 3) | Lecture 6 (Online activity 3) |
| 4 | Lecture 7 (Lecture 4) | Lecture 8 (Online activity 4) |
| 5 | Lecture 9 (Lecture 5) | Lecture 10 (Online activity 5) |
| 6 | Lecture 11 (Lecture 6) | Lecture 12 (Online activity 6) |
| 7 | Lecture 13 (Lecture 7) | Lecture 14 (Online activity 7) |
| 8 · practice | Lecture 15 (Practice 1) | Lecture 16 (Online activity 8) |
| 9 | Lecture 17 (Lecture 8) | Lecture 18 (Online activity 9) |
| 10 · practice | Lecture 19 (Practice 2) | Lecture 20 (Online activity 10) |
| 11 | Lecture 21 (Lecture 9) | Lecture 22 (Online activity 11) |
| 12 · practice | Lecture 23 (Practice 3) | Lecture 24 (Online activity 12) |
| 13 | Lecture 25 (Lecture 10) | Lecture 26 (Online activity 13) |
| 14 · practice | Lecture 27 (Practice 4) | Lecture 28 (Online activity 14) |
| 15 · practice | Lecture 29 (Practice 5) | Lecture 30 (Online activity 15) |

## Rules for writing a session

- **The approved content.** Each session is written from its blended
  session: the same ideas, ILOs, examples, figures, simulators and start
  files. Nothing beyond the ILOs of the syllabus (Drive: syllabus v2 and the
  ILO matrix v3): the students are not in technology (medical sterilization,
  supply management, renewable energy), so every session is as simple as
  the ILO allows.
- **Week 1 is a rewording only.** Lecture 1 and Online activity 1 were
  already given to the students. Lectures 1 and 2 of this version keep
  their ideas, examples and numbers; only the form changes (slides, Part A
  and Part B, a check after every step).
- **No answers to graded work.** The Tasks to submit of the online
  activities are graded and their solutions are private (`courses-private`).
  A worksheet written from an online activity uses the examples of its
  Steps and its own new examples, never the data of its Tasks to submit,
  so that this public repo gives away no answer. The course project
  (Lectures 28–30) keeps the two topics of the blended course (Canteen
  sales, My study week): its worksheets guide each student's own project
  and never show a result of the canteen data.
- **Paths.** The files of this version are in `face-to-face/week-WW/` and
  use the figures, simulators and start files of the blended week folders
  (`../../week-WW/images/…`, `../../week-WW/sims/…`). Figures made only
  for this version go in `face-to-face/images/` (`../images/…`).
- **No homework and no online activity.** The worksheet is done and
  checked in class (the coursework mark comes from the lab activities,
  quizzes and the project of the syllabus).

## Progress

Mark a session when its three files are written and render without errors
(`quarto render --profile f2f`). Commit and push after each session or each
week, so a new work session can go on from here.

| Week | Session 1 | Session 2 |
|---|---|---|
| 1 | [x] Lecture 1 | [x] Lecture 2 |
| 2 | [x] Lecture 3 | [x] Lecture 4 |
| 3 | [x] Lecture 5 | [x] Lecture 6 |
| 4 | [x] Lecture 7 | [x] Lecture 8 |
| 5 | [x] Lecture 9 | [x] Lecture 10 |
| 6 | [x] Lecture 11 | [x] Lecture 12 |
| 7 | [x] Lecture 13 | [x] Lecture 14 |
| 8 | [x] Lecture 15 | [x] Lecture 16 |
| 9 | [x] Lecture 17 | [x] Lecture 18 |
| 10 | [x] Lecture 19 | [x] Lecture 20 |
| 11 | [x] Lecture 21 | [x] Lecture 22 |
| 12 | [x] Lecture 23 | [x] Lecture 24 |
| 13 | [x] Lecture 25 | [x] Lecture 26 |
| 14 | [x] Lecture 27 | [x] Lecture 28 |
| 15 | [x] Lecture 29 | [x] Lecture 30 |

## Switching the site to face-to-face (later, when the teacher decides)

1. Move the blended files out of the way (keep them in git history, or in
   an `archive/` folder outside the render): `lesson-NN*`, `practice-NN*`,
   `online-NN.qmd` of `week-WW/`.
2. Move `face-to-face/week-WW/*.qmd` into `week-WW/`, and change the paths
   `../../week-` to `../week-` (or to `images/`, `sims/`, `files/` in the
   same week) and `../images/` to `../face-to-face-images/` (or move the
   figures into a week folder).
3. Replace `../schedule.yml` and `../index.qmd` with the files of this
   folder; set `course.blended: false` and `f2f: true` in
   `../_metadata.yml`; update `../NOTES.md`, `../plan.md` and AUTHORING.md
   (the course table, "Mapping the syllabus week").
4. Remove the exclusion from `_quarto-site.yml` (or the whole profile
   group), run `quarto render`, check every page, PDF and deck.
5. In `courses-private`: new Moodle texts for the weeks left
   (`moodle/tools/content_digital_skills.py`), and the course package
   (`syllabus-weeks.yml` from the new face-to-face syllabus on Drive).
