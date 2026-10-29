# Plan: answered pages, simpler lessons, lectures and seminars in a 15-week plan, tasks with AI

Status: approved on 2026-10-28 and revised the same day (version 2, see
"Why version 2"; Part 4 revised the same day). Implementation started
on 2026-10-28 (branch `restructure-units`). Do the work on a new branch
from `main`, in **one pull request**, as described in "Implementation"
below. This file is not published (only `.qmd` files become pages).

## Context

1. **The interactive page teaches; the PDF tests.** The interactive page is
   the simplified study version of the notes. No question or task on it may
   stay without an immediate answer, with a short reason why the answer is
   right (or why a choice is wrong). The PDF keeps its self-test model:
   questions inside the lesson, answers at the end.
2. **Simplify to the official outcomes.** Every lecture was compared with the
   official syllabus on Drive (week topics, ILOs, Bloom level). Remove what
   goes beyond them or above their level.
3. **A margin for lost time, inside the official 15-week plan.** Jordanian
   semesters lose the first 2–3 weeks, the midterm and the final, and days to
   holidays, snow or absences. About **19 sessions per course are "core"**
   (always taught). The other sessions are seminars or practice sessions that
   are taught when time allows and otherwise studied at home. Lecture length
   does not grow (90 min Game Math, 60 min the others).
4. **Tasks with AI.** Lessons built for students who have AI assistants:
   some tasks are set at a higher level, with guidance on how to reach it
   with AI and how to check the AI's work (Part 4).
5. **Moodle weeks.** Texts for the platform weeks without new teaching
   (introduction, review, exams, catch-up).

### Why version 2

The dean asks every semester for the complete course materials, organised by
the official 15-week plan. So the materials must cover **every row of each
syllabus's weekly table**, and must not look like 10–12 weeks plus fillers.
Version 1 cut each course to 19 lectures. Version 2 keeps the same 19 core
sessions and the same cuts, but organises everything in **units = syllabus
weeks**, with each syllabus slot filled:

- **Lecture slots** hold the lectures (always core).
- **Seminar slots** (Game Math, Computing Systems, Digital Media: the
  syllabi say "theory + seminar") hold **seminars**: activity sessions in
  which students apply the lectures they already had. A few seminars are core
  (an ILO needs them); the others are flexible.
- **Digital Skills** has no seminars: the syllabus says "practical" and
  "blended" (one face-to-face lecture and one online activity per week). Its
  flexible face-to-face sessions are **practice sessions** (hands-on work on
  earlier lectures). Its online activities are asynchronous and are not lost
  to holidays, so all 15 stay.

The material that version 1 deleted as "secondary" (a second application of
the same idea, inside the ILO) is **moved into the seminars**, not deleted.
Content beyond the ILOs stays cut.

### Decisions already made

- Redistribute **from lecture 1** (also the sessions already taught).
- Graded work stays unanswered: the "Tasks to submit" of online activities and
  the homework. Their model answers stay in `courses-private`.
- Folders stay `week-WW` and files are renamed in place; old printed QR codes
  may open another session. This is accepted. In version 2, **WW is the
  syllabus week of the unit**, which makes the 15-week package simple.
- Seminars must be **visible as seminars**: in their title, label, grouping
  and slides, so a teacher knows at once that the session is activity-based.

### Changed from version 1 (check before implementing)

- Digital Skills keeps **all 15 online activities** (version 1 had 9). Each one
  is rewritten to practise its unit instead of repeating the face-to-face
  lecture, which fixes the duplication the audit found. The margin is on the
  face-to-face side: 10 core lectures and 5 flexible practice sessions.
- Homework stays **one per unit**, as now (13 in Computing Systems and Digital
  Media, where the syllabus has "HW" every teaching week, and 13 in Game
  Math). It practises the lectures of its unit only, never a flexible seminar.

## Part 1 · No unanswered point on the interactive page

### What the audit found

- Every "Try it" is interactive (`match.lua`, `lesson-script.html`), but the
  feedback is generic: "✓ Right!" or "✗ Not this one. Try again."
  (`lesson-script.html` around lines 93 and 99). There is no reason why, and
  no way out for a student who is stuck.
- **Every "Do it" / "Lab task" box on the pages has no answer**: 4–6 per
  lesson. The audit sorted them into:
  - **fixed** tasks, with one result (for example "(4, 3)", or "the triangle
    disappears from below: back-face culling");
  - **personal** tasks, whose result depends on the student's phone, game or
    writing (a premise, the specs of their device).
- A few prose questions have no answer (for example "Does the wind help a
  boat?" in Game Math lecture 4).
- In the PDF, the Do it boxes have no answers either; only the exercises have
  "Answers to the exercises".

### Pipeline changes (`_extensions/lesson/`)

1. **A reason for every Try it question.** An optional second paragraph in the
   definition, starting with `Why:`:

   ```markdown
   The magnitude of (3, −4).
   :   5

       Why: √(3² + 4²) = √25 = 5. The minus sign disappears when you square it.
   ```

   - `match.lua` reads this paragraph. Today `answer_inlines` takes only the
     first paragraph and silently drops the rest. In HTML it puts the reason
     on each question (`data-why`). In Typst it is not printed: the PDF stays
     a self-test.
   - `lesson-script.html`: a right answer shows "✓ Right!" and the reason.
     After two wrong tries, the right answer is shown with its reason, and
     the question does not count as "right at the first try". No student is
     left stuck.
   - `lesson.css`: style of the reason line.
2. **"Check your result" in every Do it and every seminar activity on the
   page.** A `.check` div inside the box:

   ```markdown
   ::: {.check}
   u + v = (4, 3). It ends where w ends: head to tail gives the same arrow.
   :::
   ```

   - HTML: `<details><summary>Check your result</summary>…</details>`,
     closed until the student opens it.
   - Fixed task: the result and one line of why.
   - Personal task: "A good answer looks like …" (a model answer) and a
     2–3 point self-check list.
3. **PDF:** `book.lua` collects the `.check` divs of the notes into a new
   section at the end, "Results of the Do it tasks" (in a seminar: "Results
   of the activities"), next to "Answers to the exercises". The task is in
   the lesson; its result is at the end.
4. **`check_size.py`**, new warnings:
   - a Do it / Lab task / activity on a page without `.check`;
   - a Try it question without `Why:`;
   - `.check` or `Why:` inside "Tasks to submit" or a homework (graded
     answers must never be shown).

   Also let the box regexes accept extra attributes after `title=`.
5. **Templates:** add `Why:` and `.check`. The intro sentence of a page
   becomes "Every question on this page has its answer: try first, then
   check."

### New rule in `AUTHORING.md` ("The page teaches, the notes test")

- The interactive page is the study version: a simplified copy of the notes in
  which every question and task has an immediate answer with a short reason.
- The PDF is the self-test: questions inside the lesson; answers (exercises,
  Do it and activity results) at the end.
- Exception: "Tasks to submit" and homework stay unanswered; their solutions
  are in `courses-private`.

### Content

- `Why:` for every Try it question: one sentence, in the words of the lesson.
- `.check` for every Do it, Lab task and seminar activity on the pages, and for
  the online-activity steps that ask for a result.
- Answer every prose question on a page in the text itself.

## Part 2 · Audit against the official outcomes (simplification)

### Patterns of extra content found in all courses

1. **A second example of the same skill** (the most frequent). For example
   Example 3.2 in Game Math, Example 6.3 in Computing Systems, Example 8.2 in
   Digital Media. In version 2 a good second example moves to the seminar of
   the unit; a weak one is cut.
2. **Calculator-level arithmetic.** Cut.
   - Game Math: √2 ≈ 1.41, 0.71, √32, interpolating between two angles.
   - Computing Systems: mAh ÷ mA with three operations, 2 million × 60.
   - Digital Media: scene doubling 1 + 2 + 4 + 8.
3. **Technical or engine asides.** Cut.
   - Game Math: `Rad2Deg`, `DeltaAngle`, `sqrMagnitude`, "Unity has no 2D
     cross".
   - Computing Systems: NPU and the SoC brand list.
   - Digital Media: Courier 12 and line IDs.
4. **A topic of a later week or of another course.** Cut.
   - Game Math: the rotation rule (x, y) → (−y, x) in lecture 4, lighting
     n̂·l̂ in lecture 5, radians as a full section, and the Blender table
     (removed before, now back).
   - Computing Systems: cloud gaming and latency in lecture 2, store rules in
     lecture 1.
   - Digital Skills: how AI works (next-word probabilities), which is the
     subject of AI Applications (01101153); SUMIF/COUNTIF.
5. **Extra taxonomies and terms.** Cut.
   - Digital Skills: know/have/are authentication factors, the 3-2-1 rule,
     data classes.
   - Digital Media: logline, on-the-nose, a second name for the interest
     curve.
6. **The case study reuses a worked example's numbers.** Game Math L4–L28 and
   Computing Systems L5. The notes then contain the Game challenge answers.
   Give the story new numbers or drop the duplicate example.
7. **Whole sessions repeated in Digital Skills.** Online activity 20 copies
   lecture 19; likewise 22 ← 21, 24 ← 23 and 26 ← 25. Lecture 27 repeats
   lecture 6, and the review 15–16 repeats 1–14. In version 2 each online
   activity practises its unit instead (see Part 3).

### Time freed per lecture (audit estimate)

| Course | Extra content only | Also moving secondary sections to the seminar |
|---|---|---|
| game-math (90 min) | 8–12 min | 25–35 min |
| computing-systems (60 min) | 3–14 min | 15–20 min |
| digital-media (60 min) | 2–9 min | 12–18 min |
| digital-skills (60 min) | 2–12 min | — |

Removing content beyond the outcomes frees only about 10–15 %. Merging two
syllabus lectures into one core lecture therefore also moves the **secondary
sections** (a second application of the same idea) into the seminar of the
same unit. Every ILO keeps at least one core section, at the same Bloom
level, so no ILO depends on a flexible session.

### Content errors found (fix them in the same PR)

- **game-math L8, Do it 8.2:** the target (6, 1) is at 9.5°, not 10°. Turn Lab
  shows 19°; the text says 20°.
- **computing-systems L2:** the text says cloud gaming adds about 50 ms;
  Lag Lab uses +120 and +220 ms.
- **computing-systems L3:** the examples go 3.2, then 3.4.
- **computing-systems L4:** the task asks for a table of 6 rows; Parts Finder
  has 7 parts.
- **computing-systems L14 and L15:** a Do it says "Ask a classmate". Replace it
  with "check the maker's update page".
- **digital-media L2:** wind is diegetic but does not change, so the rule
  "what changes is diegetic" that the task leads to is wrong.
- **digital-media L19:** wrong reference; raster images were lecture 1, not 2.
- **digital-skills L29–30:** peer feedback needs classmates (against the
  rules). L18 lacks the animations that the syllabus names.
- **game-math L29 (revision):** covers only lectures 16–28 and still revises
  PRD, which is cut.

### Open decisions (the plan cuts them; the teacher may keep any of them)

Each reverses an earlier decision recorded in a course `NOTES.md`:

- computing-systems L2: cloud gaming and latency (2.3, Lag Lab);
- computing-systems L3: the texture-memory sums in 1024;
- digital-media L1: raster vs vector with the Paint and PowerPoint task.

## Part 3 · Units, lectures and seminars

### Session types

| Type | Label on the site and slides | Content | Core? |
|---|---|---|---|
| Lecture | "Lecture N" | New ideas: situation → concept → Do it → Try it → Game challenge (the current lesson model). | Always core. |
| Seminar | "Seminar N" | **No new ideas.** Students apply the lectures they already had, through activities. | Core or flexible (see the maps). |
| Practice (Digital Skills) | "Practice N" | Hands-on work on earlier lectures in Word, Excel, PowerPoint or an AI tool; same format as a seminar. | Flexible. |
| Online activity (Digital Skills) | "Online activity N" | As now (Steps with Try it, Tasks to submit), practising its unit. | Always kept (asynchronous). |

- A **unit** is one week of the official syllabus: its lecture(s), its
  seminar or online activity, and its homework. Units are numbered in
  teaching order, without gaps for exam weeks, and are never called weeks on
  the site. The folder of a unit is `week-WW`, where WW is its syllabus week
  (internal).
- Lectures and seminars are numbered separately, each in teaching order.
  "Which lecture did we reach?" still works: the teacher must reach the last
  lecture and the core seminars.
- A flexible seminar has every answer on its page. If it is not held in
  class, students study it at home; the page says so in one line.

### What a seminar looks like

- **Title and label:** `## Seminar N · <the syllabus seminar title>`;
  banner chip "Seminar · practises Lectures X–Y". Slide subtitle "Seminar N ·
  practises Lecture X". Download names `math_seminar3.pdf`,
  `math_seminar3_slides.pptx` (Digital Skills: `digital_skills_practice2.pdf`).
- **Three outputs, like a lecture:**
  - Notes (PDF) as a worksheet: Recall, then the activities, then "Results of
    the activities" and the exercises' answers at the end.
  - Interactive page: Recall, then each activity with its "Check your result"
    and one Try it (with `Why:`).
  - Slides (see below).
- **Structure:**
  1. **Recall** (about 5 min): 3–5 key ideas from the lectures it practises,
     and 2–3 recall questions with answers. No new terms; the glossary keys
     are reused, so there is no "Key terms" section.
  2. **Activities:** 3–4 in 60 min, 4–6 in 90 min. Each one has a game (or
     workplace) situation, a task for each student alone, a time, and a
     concrete product (a filled table, a sketch, a short decision with a
     reason, a file). Seminars are where the syllabus seminar titles are
     done: "Matrix exercises", "Operating-system tour on PC and mobile",
     "Drawing a storyboard from a scene".
  3. **Game challenge** as now (the unit's game, harder questions).
  4. **Wrap-up:** 3–4 lines, "what you can now do".
- **Slides of a seminar** teach by asking:
  - a Recall slide whose questions refer to the earlier lectures, with the
    answers on the same slide (`.answer` cards);
  - per activity, a **Task slide** ("Activity 2 · 10 min": the situation, the
    instruction for each student, the product) and a **Check slide** with the
    result revealed step by step (`.reveal`);
  - one Game challenge slide, a wrap-up slide.
  - About 8–12 slides in 60 min, 12–18 in 90 min.
  - `pptx_finish.py` gives seminar decks a visible "Seminar" mark on every
    slide.
- **Team work:** activities are individual, as now. The team activity (D1)
  stays only in the notes of the session that `plan.md` names, with an
  individual alternative.

### game-math: 15 units, 19 lectures + 10 seminars (90 min each)

As taught, 2 × 90 min per week. In a week with two lectures, the syllabus
seminar topic is the Game challenge of the first lecture (as now). In a week
with one lecture, the second session is a seminar with the syllabus seminar
title.

| Unit (week) | Sessions | From (old lectures / sections) | ILOs |
|---|---|---|---|
| 1 (1) | **Lecture 1** Coordinates and Vectors | 1.1 (short), 1.3, 1.4, 1.5 (curl rule), 2.1 + 2.2, 2.3, 2.4 | A1 |
| | **Seminar 1** Where Mathematics Appears in a Mobile Game | old 1–2 activities, 2.5 (3D moves) as practice | A1 |
| 2 (2) | **Lecture 2** Vector Operations: Addition, Scaling, Magnitude and Normalization | 3.1–3.5 | A1 B1 |
| | **Lecture 3** The Dot Product and the Angle Between Vectors (Game challenge = "Vector exercises in game scenarios") | 4.1, 4.2 (+ 4.3 in one line), 4.4, 4.5 | A1 B1 |
| 3 (3) | **Lecture 4** The Cross Product: Direction and Surface Normals | 5.1–5.4, 5.5 (culling only) | B1 |
| | **Lecture 5** Distance, Projection and Direction (Game challenge = "Solving movement and aiming problems") | 6.1, 6.2, 6.3 (+ 6.4 as one example), 6.5 | B1 |
| 4 (4) | **Lecture 6** Trigonometry: Sine, Cosine, Tangent and the Unit Circle | 7.1–7.4, 7.5 (short code box) | A2 |
| | **Lecture 7** Applied Trigonometry: Angles, Rotation and Oscillation (Game challenge = "Trigonometry in game motion") | 8.1–8.4 (+ 8.5 as one example) | A2 B1 |
| 5 (5) | **Lecture 8** Matrices: Operations, Multiplication, Identity and Inverse | 9.1, 9.3 + 9.4, 10.1 + 10.2, 10.3, 10.4, 10.5 ("undo" in words) | A1 C1 |
| | **Seminar 2** Matrix Exercises | second examples of 9–10, Multiply Lab | A1 C1 |
| 6 (6) | **Lecture 9** Translation, Scaling and Rotation in 2D | 11.1–11.3, 12.1 + 12.2, 12.3 (undo) | C1 |
| | **Seminar 3** Composing 2D Transformations | 11.5, second examples of 11–12 | C1 |
| 7 (7) | **Lecture 10** Homogeneous Coordinates and 3D Transformations | 13.1–13.4, 14.1 + 14.2, 14.3 (short) | C1 |
| | **Seminar 4** Transformation Chains: Object, World and Camera Space | 13.5 (short), 13.6, 14.5 | C1 |
| 8 (8) | **Seminar 5** Revision of Lectures 1–10 (by activities; old 15 condensed) | old 15 | A1 A2 B1 C1 |
| 9 (9) | **Lecture 11** Propositions, Logical Operators and Truth Tables | 16.1, 16.2 + 16.3, 16.4, 16.5, 17.1 + 17.2, 17.4 | A2 B2 |
| | **Seminar 6** Logic Exercises: Game States and Conditions | old 16–17 activities | A2 B2 |
| 10 (10) | **Lecture 12** Boolean Algebra and Decision Conditions | 17.3, 18.2 (short), 18.3, 18.4, 19.1, 19.3, 19.4 | B2 |
| | **Seminar 7** Designing a Rule Set for a Simple Game | Rule Smith, 19.6 example | B2 |
| 11 (11) | **Lecture 13** Probability Basics: Events and Sample Space | 20.1–20.5, 20.6 (short) | A2 B2 |
| | **Lecture 14** Conditional Probability and Expected Value (Game challenge = "Probability in loot drops and critical hits") | 21.1, 21.2 (+ 21.3 in one line), 21.4, 21.5 | A2 B2 |
| 12 (12) | **Lecture 15** Random Numbers: Generators, Seeds and Distributions | 22.1 + 22.2 (one LCG step), 22.3 ("seed once"), 22.4, 23.1–23.3 | C2 |
| | **Seminar 8** Generating Random Events in a Game Scenario | Loot Table Lab, second examples | C2 |
| 13 (13) | **Lecture 16** Probability for Game Balance and Fairness | 24.1, 24.3, 24.4, 25.1–25.4 | C2 |
| | **Seminar 9** Game Balancing Exercise | 24.5, 24.6, 25.6 | C2 |
| 14 (14) | **Seminar 10** Applied Problem Set: Vectors, Transformations and Probability | old 26 (no geometric probability) | B1 C1 C2 |
| | **Lecture 17** Case Study: Movement of a 2D Object (team activity in the notes only = "Group problem solving and presentation") | 27.1 (+ 12.5), 27.2, 27.3, 27.5 (e = 1), 27.6 | B1 C1 D1 |
| 15 (15) | **Lecture 18** Case Study: Random Level and Event Generation | 28.1–28.6 (no BFS) | B2 C2 |
| | **Lecture 19** Course Revision (+ an individual presentation of a solution = "Student presentations of solutions") | old 29 condensed for the whole course, 29.6 | all |

- Core: the 19 lectures. Flexible: Seminars 1–10.
- **Cut (beyond the ILOs):**
  - transpose and the engine's 4 × 4 matrix in lecture 9;
  - the general inverse formula (ad − bc);
  - reflection as a section;
  - Rᵀ = R⁻¹ and the det proof;
  - formal logic (contrapositive, iff), the state machine and its `switch`
    code;
  - short-circuit evaluation;
  - bell-shaped distributions and uniform points in a circle;
  - logarithms in drop rates;
  - PRD;
  - flood fill (BFS);
  - acceleration and damping;
  - geometric probability;
  - all Unity code that no task needs.
- **Games and simulators dropped:** Harbor Guard, Gem Grid, Code Cleaner, Rule
  Detective, LCG Lab, Seed Detective, Shape Lab, Balance Board, one of the
  two revision games. Games of cut lectures that fit a seminar (Asteroid
  Beam, Lighthouse, Problem Drill, Star Dock Missions) move to that seminar.
- **Homework:** 13, one per unit (none after units 8 and 15).

### computing-systems: 14 units, 14 lectures + 14 seminars (60 min each)

| Unit (week) | Lecture (core) | From | Seminar | From | Seminar core? | ILOs |
|---|---|---|---|---|---|---|
| 1 (1) | **Lecture 1** Computing Systems and Digital Platforms in the Games Industry | 1 + 2.4 | **Seminar 1** The Devices Students Use and How Games Run on Them | old 2 activities (time a game start, your screen, right device) | flexible | A1 |
| 2 (2) | **Lecture 2** Computer Components: CPU, Memory and Storage | 3 + 2.1 | **Seminar 2** Identifying Components and Reading Specifications | 4.1, 4.2 | core | A1 |
| 3 (3) | **Lecture 3** Input/Output Devices, the GPU and Graphics Hardware | 5 + 2.2 | **Seminar 3** Comparing Device Specifications for Gaming | 6 + settings table of 5 | core | A1 B2 |
| 4 (4) | **Lecture 4** Smartphone Architecture: SoC, Sensors, Touch Screen and Battery | 7 | **Seminar 4** Analyzing a Smartphone Specification Sheet | 8 + 4.3 | core | A1 B2 |
| 5 (5) | **Lecture 5** Operating Systems: Functions, Processes and Memory Management | 9 + essentials of 10 | **Seminar 5** Operating-System Tour on PC and Mobile | 10 | flexible | A2 |
| 6 (6) | **Lecture 6** File Systems, Resources and Device Management | 11.1, 11.3 + essentials of 12 | **Seminar 6** Hands-on: File and Resource Management | 12 | flexible | A2 C1 |
| 7 (7) | **Lecture 7** Mobile Operating Systems: Android and iOS Architecture | 13 + essentials of 14 | **Seminar 7** Exploring Android and iOS Features | 14 | flexible | A2 B1 |
| 8 (9) | **Lecture 8** Mobile Platforms Compared: Android vs iOS (team activity in the notes) | 15.1, 15.2, 15.4 + reliable sources of 16 | **Seminar 8** Platform Comparison Activity | 16 | flexible | B1 D1 |
| 9 (10) | **Lecture 9** App Stores and Publishing Requirements | 17 + 15.3 + essentials of 18 | **Seminar 9** Reviewing App-Store Guidelines | 18 | flexible | C2 |
| 10 (11) | **Lecture 10** Networking Concepts: LAN, the Internet and Protocols | 19 + 20.1–20.2 essentials | **Seminar 10** Networking Tools Demonstration | 20 | flexible | A2 |
| 11 (12) | **Lecture 11** Cloud Computing: Models and Services | 21 + essentials of 22 | **Seminar 11** Cloud Services for Games: Storage and Hosting | 22 | flexible | A2 C2 |
| 12 (13) | **Lecture 12** Gaming Platforms: Consoles, PC, Mobile and Cloud Gaming | 23 + 24.1, 24.3 | **Seminar 12** Case Study: Comparing Gaming Platforms | 24 | flexible | B1 B2 |
| 13 (14) | **Lecture 13** Setting Up Test Environments: Emulators and Real Devices | 25 (+ developer options from 14) | **Seminar 13** Hands-on: Running a Sample App on an Emulator | 26 | core | C1 |
| 14 (15) | **Lecture 14** Platform Performance and Compatibility: Case Studies | 27 | **Seminar 14** Student Presentations (Project) | 28 | core | B2 C1 D1 |

- Core: 14 lectures + Seminars 2, 3, 4, 13, 14 = **19**. Flexible: 9 seminars.
- "Essentials of …" means the lecture keeps the one idea of that seminar that
  an ILO or the exam needs; the activities stay in the seminar.
- **Cut (beyond the ILOs):**
  - 2.3 (cloud gaming, Lag Lab) in unit 1; it stays, short, in Lecture 12;
  - process states, time-slice sums, virtual memory;
  - block details and the file-system format table (keep "FAT32 cannot hold
    a 4 GB file" as a common mistake);
  - HAL / ART / XNU (keep generic layers: kernel, libraries, framework, apps);
  - exact store limits, signing keys, staged-rollout percentages;
  - IPv6, MAC, the four-layer model, nslookup, tracert;
  - egress and price sums;
  - the weighted decision matrix (keep a 3-criterion table);
  - the fourth repetition of throttling.
- **Homework:** 13, one per unit; the project instead of homework in unit 14.

### digital-media: 14 units, 14 lectures + 14 seminars (60 min each)

| Unit (week) | Lecture (core) | From | Seminar | From | Seminar core? | ILOs |
|---|---|---|---|---|---|---|
| 1 (1) | **Lecture 1** Digital Media and Creative Production in Games | 1 + essentials of 2 | **Seminar 1** Analyzing the Media of a Favorite Game | 2 | flexible | A1 |
| 2 (2) | **Lecture 2** Story Fundamentals: Character, Setting, Conflict and Structure | 3 | **Seminar 2** Analyzing the Story Structure of a Mobile Game | 4 | core | A1 B1 |
| 3 (3) | **Lecture 3** Narrative in Games: Linear, Branching and Environmental Storytelling | 5 | **Seminar 3** Drafting a Story Premise | 6 | core | A1 B1 |
| 4 (4) | **Lecture 4** Screenwriting: Format, Scenes and Dialogue | 7 + essentials of 8 | **Seminar 4** Writing a Scene and Its Dialogue | 8 | flexible | A1 B1 |
| 5 (5) | **Lecture 5** Storyboarding: Shots, Composition and Flow | 9 + essentials of 10 | **Seminar 5** Drawing a Storyboard from a Scene | 10 | flexible | C1 |
| 6 (6) | **Lecture 6** Storyboards for Gameplay and Cutscenes; Storyboard Tools | 11 + essentials of 12 | **Seminar 6** Storyboard Workshop | 12 | flexible | C1 |
| 7 (7) | **Lecture 7** Digital Audio Basics: Sound, Formats and Recording | 13.1–13.4 + essentials of 14 | **Seminar 7** Recording and Editing a Sound Sample | 14 | flexible | C2 |
| 8 (9) | **Lecture 8** Music and Sound-Effects Production for Games | 15 | **Seminar 8** Producing a Short Music or Sound-Effect Loop | 16 | core | C2 |
| 9 (10) | **Lecture 9** Audio Design: Mixing, Implementation and Quality Evaluation | 17 + essentials of 18 | **Seminar 9** Mixing and Critique Session | 18 | flexible | B2 C2 |
| 10 (11) | **Lecture 10** Digital Video Basics: Formats, Resolution and Codecs | 19 + essentials of 20 | **Seminar 10** Video-Editing Tool Tour | 20 | flexible | C3 |
| 11 (12) | **Lecture 11** Video Processing: Editing, Transitions, Effects and Export | 21 | **Seminar 11** Editing a Promotional Clip | 22 | core | C3 |
| 12 (13) | **Lecture 12** Intellectual Property: Copyright, Licensing and Fair Use | 23 + 24.1, 24.3 | **Seminar 12** Case Study: Intellectual-Property Issues in Game Content | 24 | flexible | A2 D1 |
| 13 (14) | **Lecture 13** Using Licensed and Open Assets; Credits and Attribution | 25.1–25.3 + 24.2 | **Seminar 13** Auditing the Licenses of a Game's Assets | 26 | flexible | A2 D1 |
| 14 (15) | **Lecture 14** Integrated Media Production: Team Workshop (team activity) | 27 | **Seminar 14** Team Presentation of a Media Package (team activity) | 28 | core | B2 C1 C2 C3 D1 |

- Core: 14 lectures + Seminars 2, 3, 8, 11, 14 = **19**. Flexible: 9 seminars.
- **Cut (beyond the ILOs):**
  - raster/vector and the formats-and-tools table in lecture 1 (open decision;
    the plan keeps one line);
  - the spatial/meta classification;
  - scene-doubling sums;
  - Courier and line IDs;
  - the 180-degree rule with a camera map;
  - 65,536 levels and file-size sums;
  - the BPM formula;
  - the Unity Audio Mixer interface and code (`AUTHORING.md` forbids engine
    interfaces);
  - 370 MB/s and the bitrate formula;
  - patents, trade secrets and "life + 70" sums;
  - code licences (MIT/BSD/GPL).
- **Homework:** 13, one per unit; the project instead of homework in unit 14.
  `plan.md`: the team activity is in Lecture 14 and Seminar 14.

### digital-skills: 15 units, 10 lectures + 5 practice sessions + 15 online activities

Practical and blended. Holidays cancel face-to-face sessions only, so the
margin is on the face-to-face side.

| Unit (week) | Face-to-face (60 min) | From | Online activity | From | ILOs |
|---|---|---|---|---|---|
| 1 (1) | **Lecture 1** Digital Skills and the Apps That Make Us Productive | 1 | **Online activity 1** Your University Account, Cloud Storage and Files | 2 | A1 |
| 2 (2) | **Lecture 2** Generative AI Tools: What They Do Well and Where They Fail | 3 | **Online activity 2** Writing Clear Prompts | 4 | A1 C4 |
| 3 (3) | **Lecture 3** Microsoft Office: Concepts, Terms and Common Features | 5 | **Online activity 3** Office on the Computer, the Web and the Phone | 6 | A2 A3 |
| 4 (4) | **Lecture 4** Word (1): Formatting, Styles, Lists, Tables and Pictures | 7 | **Online activity 4** Word (2): Page Layout, Headers and a Table of Contents | 8 | C1 |
| 5 (5) | **Lecture 5** AI with Word: Draft, Summarize, Rewrite and Translate | 9 | **Online activity 5** A Formal Letter and a CV with AI Help | 10 | C1 C4 B1 |
| 6 (6) | **Lecture 6** Excel (1): Cells, Formulas, References and Basic Functions | 11 | **Online activity 6** A Monthly Budget Sheet | 12 | C2 |
| 7 (7) | **Lecture 7** Excel (2): Sorting, Filtering, Conditional Formatting and Charts | 13 | **Online activity 7** AI with Excel: Formulas, Clean Data and the Right Chart | 14 | C2 C4 B1 |
| 8 (8) | **Practice 1** Review of Lectures 1–7 (by tasks) | 15 | **Online activity 8** Review Activity: Practice Questions | 16 | all of 1–7 |
| 9 (9) | **Lecture 8** PowerPoint: Slides, Layouts, Themes, Transitions, Animations and Notes | 17 + essentials of 18 (animations added) | **Online activity 9** A Five-Slide Talk | 18 | C3 |
| 10 (10) | **Practice 2** AI with PowerPoint: Outline, Slides and Pictures | 19 | **Online activity 10** A Short Presentation with AI Help (carries the unit's core content) | 20 | C3 C4 B1 |
| 11 (11) | **Lecture 9** Checking AI Output and Using AI Responsibly | 21 (§2–4) + 23 (§1–3) | **Online activity 11** Fact-Checking an AI-Written Document | 22 | B1 D1 |
| 12 (12) | **Practice 3** Responsible AI in Practice: Personal Data, Copyright and Honesty | 23 activities | **Online activity 12** Safe Prompts and an AI-Use Statement | 24 | D1 |
| 13 (13) | **Practice 4** Excel (3): Summarizing Data with AI Help | 25 (no SUMIF/COUNTIF) | **Online activity 13** Analyzing a Small Dataset and Charting It | 26 | C2 C4 B1 |
| 14 (14) | **Practice 5** Working Across Office Apps with AI | 27 (no linked tables, no classmates) | **Online activity 14** Course Project (1): Plan, Data Sheet and First Draft | 28 | A1 A3 C4 |
| 15 (15) | **Lecture 10** Course Project Presentations | 29 (§29.1–29.3, no peer feedback) | **Online activity 15** Course Project (2): Final Report, Data Sheet and Presentation | 30 (no peer feedback) | B1 C1–C4 D1 |

- Core: Lectures 1–10 and all 15 online activities. Flexible: Practice 1–5.
- Each online activity practises its unit and never repeats the lecture
  (fixes pattern 7). In units 10 and 12, where the face-to-face session is a
  flexible practice, the online activity carries the core idea.
- AI is the main topic of units 2, 5, 7, 10, 11, 12 and part of 13–15: more
  than the required quarter.
- The AI-use statement starts in unit 11; update `NOTES.md` (today: "from
  lecture 23").
- Old lecture 1: replace the job-advert Lab task with a short AutoSum task.
  Old lecture 3: shrink "how AI works" to two bullets and teach "what AI does
  well", which the syllabus names.
- No homework (the online activities replace it).

### Files, names and links

- Folder of a unit: `week-WW`, WW = its syllabus week. Game Math and Digital
  Skills use `week-01 … week-15`. Computing Systems and Digital Media have no
  unit in week 8 (midterm), so they use `week-01 … week-07` and
  `week-09 … week-15`.
- File names in a unit folder:
  - `lesson-NN.qmd`, `lesson-NN-book.qmd` and `lesson-NN-slides.qmd` for
    Lecture NN;
  - `seminar-NN*` for Seminar NN, and `practice-NN*` for Practice NN
    (Digital Skills);
  - `online-NN.qmd` for Online activity NN (Digital Skills);
  - `homework-UU.qmd` for the homework of unit UU.
- Download names: `math_lecture8.pdf`, `math_seminar2.pdf`,
  `math_seminar2_slides.pptx`, `math_homework5.pdf`,
  `digital_skills_practice3.pdf`, `digital_skills_online4_tasks.pdf`.
- Images and simulators move with their session. Old printed QR codes may
  open another session (accepted).

## Part 4 · Tasks with AI (revised 2026-10-28)

### The idea (the teacher's clarification)

Students have AI assistants. A lesson that only asks simple questions lets a
student paste them into an AI and learn nothing. Asking an AI to explain the
lesson is something every student can do alone; it needs no lesson. Instead,
the lessons are built **for a world with AI**: some tasks are set at a
**higher level than students could reach alone in the time**, with guidance
on how to use an AI assistant to reach it. The student uses AI to do more,
not to do the homework for them, and learns to use AI well. This replaces
the "Study with AI" boxes of the first version of this plan (explain it,
quiz me, review my work, find the mistake).

### What a Task with AI looks like

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
A good sheet … (on the page; in the PDF at the end)
:::
:::
```

- **A product beyond the usual level**, inside the ILOs of the session (never
  a topic of a later week): something that is long or hard by hand, such as
  1000 random rolls, a five-phone comparison table, a story with three
  endings and its storyboard, a licence audit of 20 assets.
- **A starter prompt** (`.prompt`, with a "Copy prompt" button on the page).
- **The student's own part**: they build, change, choose or decide.
- **A check with the tools of the lesson**: a value worked by hand, a
  simulator, GeoGebra, the maker's page, the official source. The AI can be
  wrong, and finding where it is wrong is part of the task.
- **A product** to keep or hand in, and one sentence on what the AI got
  wrong or what the student changed.
- On the page and in the notes the box has a `.check` (a model product and a
  self-check list). In graded work (homework, Tasks to submit) it has no
  `.check` and asks for the AI-use statement.

### Where

- 0–2 per session, only where AI really lets students do more: often a
  seminar activity, the Game challenge, or a homework task. Not on the
  slides (home or seminar work).
- Homework: where a short question could be pasted into an AI, prefer one
  small Task with AI, with the AI-use statement. The whole homework takes
  about 10 minutes, never more than 15, and never gets longer than it is
  (the teacher's rule, 2026-10-29). The homework
  page says: "You may use AI where a task says so. Check its work and say
  how you used it."
- Ideas per course:
  - **game-math:** a sheet of 1000 rolls of a loot table or a crit chance
    against the expected value; GeoGebra commands from the AI for a path of
    10 points or a chain of transformations, checked at two points by hand;
    a rule table (truth table) for a door with four conditions, checked row
    by row.
  - **computing-systems:** a comparison table of five phones or consoles
    from an AI draft, three numbers checked on the makers' pages; a test
    plan for a game on four devices; a store-listing checklist checked
    against the official store guidelines (D1, reliable sources).
  - **digital-media:** a branching story with three endings, edited by the
    student and drawn as a storyboard; a scene drafted with AI and rewritten
    in screenplay format; a credits list and licence audit of 20 assets,
    each licence checked at its source. Never AI images, sound or video as
    the student's media product (unclear rights; it skips the production
    ILOs); it is a case in the IP sessions.
  - **digital-skills:** AI is already the subject of many sessions; the
    Tasks with AI there are the Office tasks done with AI help at a higher
    level (a formatted report, a budget with formulas and a chart), always
    with checking and, from unit 11, the AI-use statement.
- Fixed rules (new `AUTHORING.md` section "Tasks with AI"):
  - free tools named generally (Microsoft Copilot with the university
    account, ChatGPT, Gemini); no task needs a paid plan;
  - no personal data in a prompt;
  - every task has a check step;
  - the rule "no tool or assistant names" keeps applying to how the lessons
    are made, not to the tools students use.
- `check_size.py`: at most 2 per session; a box without `.prompt` or without
  a check step is a warning; on a page it needs a `.check`; in graded work
  it must ask for the AI-use statement and show no `.check`.

## Part 5 · The 15-week course package and the Moodle weeks

### The course package (for the dean, every semester)

- The weekly table of each syllabus is copied **word for word** (week, the
  columns Lecture / Seminar, or First Lecture / Second Lecture / Seminar, or
  Lecture 1 / Lecture 2 online, ILOs, PLOs, descriptors) into
  `courses-private/courses/<slug>/syllabus-weeks.yml`. It stays private;
  the public repo keeps only titles and ILO codes, as now.
- A new script, `tools/course_package.py`, run after `quarto render`:
  - reads `schedule.yml` (sessions with their unit, syllabus week and slot)
    and the private `syllabus-weeks.yml`;
  - writes `_package/<slug>/` (git-ignored): one folder per syllabus week
    (`week-01 … week-16`) with the rendered notes PDF, slides and homework of
    that week, and the address of each interactive page;
  - writes `index.html` and `index.pdf` (headless Chrome, as in
    `homework_pdf.py`): the syllabus weekly table exactly as approved, with
    one added **Materials** column naming the session that covers each row
    (Lecture 8, Seminar 2, Online activity 5, homework 5). Week 8 and week 16
    show the exams as the syllabus does.
- The script checks that every row of the syllabus table has its material, and
  that every session belongs to exactly one row.

### Moodle weeks

These texts go in `courses-private`, not on the site: the site counts
sessions, not weeks.

- One file per course: `courses-private/moodle/<slug>-weeks.md` (pushed to
  `main` of `courses-private` directly, as usual), with:
  1. **The official map** (the same as the package): week w holds unit w's
     sessions; week 8 the midterm (and the revision seminar in Game Math, the
     review in Digital Skills); week 16 the final. A note says the real week
     follows the last session taught.
  2. **Ready Arabic texts for weeks without new teaching**, in the
     university's section template ("الأسبوع … (التاريخ): …", "في هذا الأسبوع
     سوف نعمل على", "في نهاية هذا الأسبوع ستكون قادراً على", "المطلوب من
     الطالب"): introduction, review before the midterm, midterm, catch-up week
     (pointing to the answered pages of earlier sessions, including the
     flexible seminars), final review, final exam. In Digital Skills, never
     the word "مختبر".
- The texts of actual teaching weeks (which session in which week, with
  links) are written on request, when the real pace is known.

## Implementation

Branch from `main`, one pull request, one commit per step below.

1. **Pipeline:**
   - `match.lua` (`Why:`, `.check`, `.prompt` of the Tasks with AI);
   - `lesson-script.html` (reason, reveal after two wrong tries, copy button);
   - `lesson.css`, `typst-body.typ`;
   - `book.lua` ("Results of the Do it tasks" / "Results of the activities");
   - **session types**:
     - `schedule.yml` entries get `kind` (lecture, seminar, practice, online),
       `n`, `unit`, `week` (syllabus week), `slot` (syllabus column) and
       `core`;
     - `shortcodes.lua` (`{{< schedule >}}` grouped by unit, with "Lecture N"
       and "Seminar N" labels, and the folder function by syllabus week);
     - `banner.lua` (seminar and practice chips: "Seminar · practises
       Lectures X–Y");
     - `download_names.py` and `homework_pdf.py` (new file names);
     - `slides.lua` and `pptx_finish.py` (the seminar look and its "Seminar"
       mark);
   - `check_size.py`: the new warnings, and new `SIZES` rows for seminars and
     practice sessions:

     | | 60 min | 90 min |
     |---|---|---|
     | Activities | 3–4 | 4–6 |
     | Try it questions | 10–20 | 15–30 |
     | Slides | 8–12 | 12–18 |
     | Notes words, at most | 2 000 | 3 000 |

     Also: one `.check` per activity, a Recall section, no new glossary
     terms;
   - new templates `seminar-template.qmd`, `seminar-book-template.qmd` and
     `seminar-slides-template.qmd` (also used for Digital Skills practice);
     the other templates get `Why:` and `.check`;
   - `tools/course_package.py` and the `_package/` line in `.gitignore`.
   - Try everything on one unit of one course first.
2. **Rules:** in `AUTHORING.md`:
   - "The page teaches, the notes test";
   - units, lectures, seminars, practice and online sessions; core and
     flexible sessions; numbering and names;
   - "What a seminar looks like";
   - "Tasks with AI";
   - the course package;
   - homework one per unit;
   - a lessons-learned entry for 2026-10-28.

   Also `NOTES.md`, `plan.md` and `schedule.yml` of the four courses.
3. **Content, one commit per course** (game-math, computing-systems,
   digital-media, digital-skills):
   - lectures merged and cut by the maps;
   - seminars and practice sessions built in the seminar format from the old
     seminar lessons and the moved secondary sections;
   - Digital Skills online activities rewritten to practise their unit;
   - new case-study numbers;
   - the error fixes;
   - `Why:` and `.check` everywhere;
   - the Tasks with AI;
   - slides derived again from the notes (seminar decks in the seminar style);
   - homework renumbered by unit;
   - new GIF recordings only for changed simulators
     (`sh shared/sims/recordings/record-all.sh <name>`).
4. **`courses-private`** (`main`, pushed directly):
   - homework and online-activity solutions renumbered;
   - `courses/<slug>/syllabus-weeks.yml` for the four courses (from the Drive
     syllabi);
   - the `moodle/<slug>-weeks.md` files.
5. **Pull request** into `main`, reviewed and merged by the teacher.

## Verification

- `python3 _extensions/lesson/check_size.py --all`: no warnings, including the
  new ones (no Do it or activity without `.check`, no question without
  `Why:`, seminar sizes).
- `python3 _extensions/lesson/check_figures.py`: no warnings.
- A full `quarto render`: no errors; the new download names exist
  (`math_lecture19.pdf`, `math_seminar10.pdf`), and no old name is left
  (`math_lecture20.pdf` does not exist).
- `python3 tools/course_package.py`: for each course,
  - a package with week folders 1–16;
  - an index whose rows match the syllabus table word for word;
  - every row with its material, and no session left over.
- In the browser (`quarto preview`), one unit of each course:
  - the course page groups sessions by unit, with "Lecture N" and "Seminar N"
    labels;
  - two wrong answers, then the right answer is shown with its reason;
  - "Check your result" opens;
  - "Copy prompt" works;
  - the simulators work inside the page and at phone width.
- One PDF of each course: the results section at the end, and no `Why:` text
  inside the lesson.
- One lecture deck and one seminar deck of each course in PowerPoint:
  - nothing overlaps;
  - the seminar deck shows its "Seminar" mark, its Recall slide and its Task
    and Check slides.
- Print one online activity and one homework: one A4 page, no answers.
