# Plan: answered interactive pages, simpler lessons, 19 lectures, study with AI

Status: approved on 2026-10-28; implementation not started. Do the work on a
new branch from `main`, in **one pull request**, as described in
"Implementation" below. This file is not published (only `.qmd` files become
pages).

## Context

1. **The interactive page teaches; the PDF tests.** The interactive page is
   the simplified study version of the notes. No question or task on it may
   stay without an immediate answer, with a short reason why the answer is
   right (or why a choice is wrong). The PDF keeps its self-test model:
   questions inside the lesson, answers at the end.
2. **Simplify to the official outcomes.** Every lecture was compared with the
   official syllabus on Drive (week topics, ILOs, Bloom level). Remove what
   goes beyond them or above their level.
3. **19 lectures per course.** Jordanian semesters lose the first 2–3 weeks,
   the midterm and the final, and 1–3 days to holidays, snow or absences. Each
   course is redistributed onto 19 lectures; lecture 19 is the last one
   (revision in Game Math, project presentations in the other courses). This
   is done by cutting and merging, never by making a lecture longer
   (90 min Game Math, 60 min the others).
4. **Study with AI.** Activities in which the student uses an AI chat to
   understand the lesson faster, only where this really helps.
5. **Moodle weeks.** Texts for the 16 platform weeks that have no new
   teaching (introduction, review, exams, catch-up).

Decisions already made:

- Redistribute **from lecture 1** (also the lectures already taught).
- **19 includes the last lecture.**
- Digital Skills: **19 in total**, still alternating (odd = face-to-face
  lesson, even = online activity).
- Graded work stays unanswered: the "Tasks to submit" of online activities and
  the homework. Their model answers stay in `courses-private`.
- Files stay in the **`week-PP` folders** and are renumbered in place.
  Old printed QR codes may open another lecture; this is accepted.

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
2. **"Check your result" in every Do it on the page.** A `.check` div inside
   every Do it / Lab task:

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
   section at the end, "Results of the Do it tasks", next to "Answers to the
   exercises". The task is in the lesson; its result is at the end.
4. **`check_size.py`**, new warnings:
   - a Do it / Lab task on a page without `.check`;
   - a Try it question without `Why:`;
   - `.check` or `Why:` inside "Tasks to submit" or a homework (graded
     answers must never be shown).

   Also let the box regexes accept extra attributes after `title=`.
5. **Templates** (`shared/templates/lesson-template.qmd`,
   `online-template.qmd`): add `Why:` and `.check`. The intro sentence
   becomes "Every question on this page has its answer: try first, then
   check."

### New rule in `AUTHORING.md` ("The page teaches, the notes test")

- The interactive page is the study version: a simplified copy of the notes in
  which every question and task has an immediate answer with a short reason.
- The PDF is the self-test: questions inside the lesson; answers (exercises
  and Do it results) at the end.
- Exception: "Tasks to submit" and homework stay unanswered; their solutions
  are in `courses-private`.

### Content

- `Why:` for every Try it question: one sentence, in the words of the lesson.
- `.check` for every Do it and Lab task on the pages, and for the online-activity
  steps that ask for a result.
- Answer every prose question on a page in the text itself.

## Part 2 · Audit against the official outcomes (simplification)

### Patterns of extra content found in all courses

1. **A second example of the same skill** (the most frequent). For example
   Example 3.2 in Game Math, Example 6.3 in Computing Systems, Example 8.2 in
   Digital Media.
2. **Calculator-level arithmetic.**
   - Game Math: √2 ≈ 1.41, 0.71, √32, interpolating between two angles.
   - Computing Systems: mAh ÷ mA with three operations, 2 million × 60.
   - Digital Media: scene doubling 1 + 2 + 4 + 8.
3. **Technical or engine asides.**
   - Game Math: `Rad2Deg`, `DeltaAngle`, `sqrMagnitude`, "Unity has no 2D
     cross".
   - Computing Systems: NPU and the SoC brand list.
   - Digital Media: Courier 12 and line IDs.
4. **A topic of a later week or of another course.**
   - Game Math: the rotation rule (x, y) → (−y, x) in lecture 4, lighting
     n̂·l̂ in lecture 5, radians as a full section, and the Blender table
     (removed before, now back).
   - Computing Systems: cloud gaming and latency in lecture 2, store rules in
     lecture 1.
   - Digital Skills: how AI works (next-word probabilities), which is the
     subject of AI Applications (01101153); SUMIF/COUNTIF.
5. **Extra taxonomies and terms.**
   - Digital Skills: know/have/are authentication factors, the 3-2-1 rule,
     data classes.
   - Digital Media: logline, on-the-nose, a second name for the interest
     curve.
6. **The case study reuses a worked example's numbers.** Game Math L4–L28 and
   Computing Systems L5. The notes then contain the Game challenge answers.
   Give the story new numbers or drop the duplicate example.
7. **Whole lectures repeated in Digital Skills.** Online activity 20 copies
   lecture 19; likewise 22 ← 21, 24 ← 23 and 26 ← 25. Lecture 27 repeats
   lecture 6, and the review 15–16 repeats 1–14.

### Time freed per lecture (audit estimate)

| Course | Extra content only | Also dropping secondary sections |
|---|---|---|
| game-math (90 min) | 8–12 min | 25–35 min |
| computing-systems (60 min) | 3–14 min | 15–20 min |
| digital-media (60 min) | 2–9 min | 12–18 min |
| digital-skills (60 min) | 2–12 min; repeated lectures merge | — |

**Removing content beyond the outcomes frees only about 10–15 %.** That is
not enough for 29 → 19 (a ratio of 1.5 to 1). The merge therefore also drops
**secondary sections**: a second application of the same idea, inside the ILO
but not needed to reach it (for example 4.3, 6.4, 7.5 and 8.5 in Game Math).
Every ILO keeps at least one core section, at the same Bloom level.

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

## Part 3 · Redistribution onto 19 lectures

### Principle

- Each new lecture = the core sections of one or two old lectures, after the
  cuts above. The order of the official syllabus does not change.
- Sizes do not change: 5–7 sections in 90 min, 3–4 in 60 min. `SIZES` in
  `check_size.py` and the size table in `AUTHORING.md` stay as they are.
- Every ILO stays covered. The team activity (D1) stays in the notes of the
  lesson named in `plan.md`.
- No mid-semester revision lecture; lecture 19 is the revision or the project.

### game-math: 29 → 19 (90 min)

- Old 15 (revision of 1–14) becomes an optional self-study page before the
  midterm.
- Logic shrinks from 4 lectures to 2 (largest cuts: formal logic and
  programming). Trigonometry stays at 2.

| New | Title | From (old sections) | ILOs |
|---|---|---|---|
| 1 | Coordinates and Vectors | 1.1 (short), 1.3, 1.4, 1.5 (curl rule), 2.1 + 2.2, 2.3, 2.4 | A1 |
| 2 | Vector Operations and Distance | 3.1–3.5, 6.1 | A1 B1 |
| 3 | The Dot Product and Projection | 4.1, 4.2 (+ 4.3 in one line), 4.4, 4.5, 6.2, 6.3 (+ 6.4 as one example) | A1 B1 |
| 4 | The Cross Product, Normals and Rays | 5.1–5.4, 5.5 (culling only), 6.5 | B1 |
| 5 | Trigonometry and the Unit Circle | 7.1–7.4, 7.5 (short code box) | A2 |
| 6 | Applied Trigonometry: Angles, Rotation, Oscillation | 8.1–8.4 (+ 8.5 as one example), 12.1 | A2 B1 C1 |
| 7 | Matrices and Matrix Multiplication | 9.1, 9.3, 9.4, 10.1–10.3 | A1 C1 |
| 8 | Identity, Inverse, Translation and Scaling | 10.4, 10.5 ("undo" in words), 11.1–11.3, 11.5 | A1 C1 |
| 9 | Rotation Matrices and Homogeneous Coordinates | 12.2, 12.3, 13.1–13.4 | C1 |
| 10 | Transformation Chains and 3D Transformations | 13.5 (short), 13.6, 14.1 + 14.2, 14.3, 14.5 | C1 |
| 11 | Propositions, Operators and Truth Tables | 16.1, 16.2 + 16.3, 16.4, 16.5, 17.1 + 17.2, 17.4 | A2 B2 |
| 12 | Boolean Algebra and Game Decisions | 17.3, 18.2 (short), 18.3, 18.4, 19.1, 19.3, 19.4 | B2 |
| 13 | Probability: Events and Sample Space | 20.1–20.5, 20.6 (short) | A2 B2 |
| 14 | Conditional Probability, Expected Value and Random Numbers | 21.1, 21.2, 21.4, 21.5, 22.1 + 22.2, 22.3 | A2 B2 C2 |
| 15 | Distributions and Drop Rates | 22.4, 23.1–23.3, 24.1, 24.3, 24.4 | C2 |
| 16 | Difficulty, Fairness and the Player's Perception | 24.5, 24.6, 25.1–25.4, 25.6 | C2 |
| 17 | Case Study: Movement of a 2D Object (team activity in the notes only) | 26.1, 27.1 (+ 12.5), 27.2, 27.3, 27.5, 27.6 | B1 C1 D1 |
| 18 | Case Study: Random Level and Event Generation | 28.1–28.6 (no BFS) | B2 C2 |
| 19 | Course Revision (+ an individual presentation of a solution, D1) | 15 and 29 condensed for the whole course, 29.6 | all |

- **Cut (main items):**
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
- **Games and simulators dropped:** Harbor Guard, Gem Grid, one of Asteroid Beam
  and Turret Turn, one of Lighthouse and Cannon Cove, Code Cleaner, Rule
  Detective, LCG Lab, Seed Detective, Shape Lab, Balance Board, Problem Drill,
  Star Dock Missions, and one of the two revision games.
- **Homework:** 9 (after 1–2 … 17–18) instead of 14.
- **New lecture 1** takes 8 old sections; condense to 7 (2.1 and 2.2 become
  one section).

### computing-systems: 28 → 19 (60 min)

| New | From (old) | Title | ILOs |
|---|---|---|---|
| 1 | 1 + 2.4 | Computing Systems, Platforms and the Devices We Play On | A1 |
| 2 | 3 + 2.1 | CPU, Memory and Storage | A1 |
| 3 | 4 (4.1, 4.2) | Identifying Components and Reading Specifications | A1 |
| 4 | 5 + 2.2 | Input/Output, the GPU and Graphics Hardware | A1 |
| 5 | 6 + settings table of 5 | Comparing Device Specifications for Gaming | A1 B2 |
| 6 | 7 | Smartphone Architecture: SoC, Sensors, Touch Screen and Battery | A1 |
| 7 | 8 + 4.3 | Analyzing a Smartphone Specification Sheet | A1 B2 |
| 8 | 9 + 10 | Operating Systems: Functions, Processes, Memory, and a Tour | A2 |
| 9 | 11 (11.1, 11.3) + 12 | Files, Devices and a Ready Test Device | A2 C1 |
| 10 | 13 + 14 | Android and iOS: Architecture and Features | A2 B1 |
| 11 | 15 (15.1, 15.2, 15.4) + 16 | Android vs iOS with Reliable Sources (team activity) | B1 D1 |
| 12 | 17 + 18 + 15.3 | Publishing on the App Stores | C2 |
| 13 | 19 + 20 (20.1, 20.2) | Networking Concepts and Tools | A2 |
| 14 | 21 + 22 | Cloud Computing and Cloud Services for Games | A2 C2 |
| 15 | 23 + 24 (24.1, 24.3) | Gaming Platforms Compared | B1 B2 |
| 16 | 25 (+ developer options from 14) | Test Environments: Emulators and Real Devices | C1 |
| 17 | 26 | Hands-on: A Sample App on an Emulator | C1 |
| 18 | 27 | Platform Performance and Compatibility: Case Studies | B2 C1 D1 |
| 19 | 28 | Student Presentations (Project) | B2 C1 D1 |

- **Cut (main items):**
  - all of 2.3 (cloud gaming, Lag Lab in lecture 2); it stays, short, in 15;
  - process states, time-slice sums, virtual memory;
  - block details and the file-system format table (keep "FAT32 cannot hold
    a 4 GB file" as a common mistake);
  - HAL / ART / XNU (keep generic layers: kernel, libraries, framework, apps);
  - exact store limits, signing keys, staged-rollout percentages;
  - IPv6, MAC, the four-layer model, nslookup, tracert;
  - egress and price sums;
  - the weighted decision matrix (keep a 3-criterion table);
  - the fourth repetition of throttling.
- **Homework:** 8, then the project instead of the last one.

### digital-media: 28 → 19 (60 min)

| New | From (old) | Title | ILOs |
|---|---|---|---|
| 1 | 1 + 2 | Digital Media in Games and How to Analyze Them | A1 |
| 2 | 3 | Story Fundamentals: Character, Setting, Conflict and Structure | A1 |
| 3 | 4 | Analyzing the Story Structure of a Mobile Game | A1 B1 |
| 4 | 5 | Narrative in Games: Linear, Branching and Environmental | A1 |
| 5 | 6 | Drafting a Story Premise | A1 B1 |
| 6 | 7 + 8 | Screenwriting: Writing a Scene and Its Dialogue | A1 B1 |
| 7 | 9 + 10 | Storyboarding: From Shots to a Timed Board | C1 |
| 8 | 11 + 12 | Storyboards for Gameplay and Cutscenes; Animatic and Workshop | C1 |
| 9 | 13 (13.1–13.4) + 14 | Digital Audio: Recording and Editing a Sample | C2 |
| 10 | 15 | Music and Sound Effects for Games | C2 |
| 11 | 16 | Producing a Short Loop | C2 |
| 12 | 17 + 18 | Audio Mixing, Quality Evaluation and Critique | B2 C2 |
| 13 | 19 + 20 | Digital Video Basics and the Editing Tool | C3 |
| 14 | 21 | Video Processing: Cuts, Transitions, Effects and Export | C3 |
| 15 | 22 | Editing a Promotional Clip | C3 |
| 16 | 23 + 24 (24.1, 24.3, 24.4) | Intellectual Property and Its Issues in Game Content | A2 D1 |
| 17 | 25 (25.1–25.3) + 24.2 + 26 | Licensed and Open Assets, Credits and a License Audit | A2 D1 |
| 18 | 27 | Integrated Media Production: Team Workshop (team activity) | B2 C1 C2 C3 D1 |
| 19 | 28 | Team Presentation of a Media Package (team activity) | B2 D1 |

- **Cut (main items):**
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
- **Homework:** 8, then the project instead of the last one. `plan.md`: the
  team activity moves to lectures 18–19.

### digital-skills: 30 → 19 (10 face-to-face + 9 online)

Lectures **1–13 keep their numbers and files** (simplified only). The merges
start at 14:

| New | Mode | From (old) | Title | ILOs |
|---|---|---|---|---|
| 14 | online | 14 + 25 (§25.1, 25.3, 25.4) + 26 | AI with Excel: Clean Data, PivotTables, Checked Insights | C2 C4 B1 |
| 15 | F2F | 17 + 18 | PowerPoint: Slides, Themes, Transitions and Animations, Notes | C3 |
| 16 | online | 19 + 20 | A Short Presentation with AI Help | C3 C4 B1 |
| 17 | F2F | 21 (§2–4) + 23 (§1–3) | Checking AI Output and Using AI Responsibly | B1 D1 |
| 18 | online | 28 + 30 + tasks of 22 and 24 | Course Project: Report, Slides and AI-Use Statement | B1 C1–C4 D1 |
| 19 | F2F | 29 (§29.1–29.3, no peer feedback) | Course Project Presentations | C3 C4 B1 |

- Dropped: 15–16 (review) and 27; merged: 20, 22, 24, 26, 28.
- AI share: 8 of 19 lectures (42 %); the minimum is a quarter.
- The AI-use statement starts in lecture 17; update `NOTES.md` (today: "from
  lecture 23").
- Old lecture 1: replace the job-advert Lab task with a short AutoSum task.
  Old lecture 3: shrink "how AI works" to two bullets and teach "what AI does
  well", which the syllabus names.

### Files and links

- Renumber in place: lecture n in `week-PP/lesson-NN*` with
  PP = (n + 1) ÷ 2 rounded down; images and simulators move with their
  lesson; delete the empty `week-11 … week-15` folders.
- Download names follow the new numbers automatically (`download_names.py`).
- **Homework** is renumbered: homework k after lectures 2k − 1 and 2k. Keep
  the best tasks of the old homework, and update the solutions in
  `courses-private` with the same numbers.
- Moodle links that point to lectures by number must be updated after the
  merge (see Part 5).

## Part 4 · Study with AI

### Four kinds of activity, chosen because they speed up understanding

Each one ends with a check, because the AI can be wrong.

| Kind | What the student does | Best for | Check |
|---|---|---|---|
| 1. Explain it another way | Copies a ready prompt: "Explain X in Arabic with a game example, in 5 sentences." | The hardest idea of the lesson; students whose English is weak. | Compare with the lesson's definition: the given key words must appear. |
| 2. Quiz me | "Ask me 3 questions about X, one at a time; give me a hint, not the answer." | Ideas that need more practice, after the Try it. | Answers come from the lesson; compare with the notes. |
| 3. Review my work | Pastes their own Do it result and the lesson's checklist: "What is missing by this checklist?" | Writing and analysis: premise, scene, storyboard, spec comparison, a Word or Excel file. | The student decides which comments to accept and writes one line why. |
| 4. Find the mistake | The page shows a prepared AI answer (fixed text) with one or two planted mistakes; the student finds them. | Every course; especially arithmetic in Game Math and made-up specs in Computing Systems. | A `match` question with `Why:`: answered at once, no AI account needed. |

Left out on purpose:

- "Write the solution for me": it replaces the learning.
- "Generate new problems": AI arithmetic is not reliable. Use it rarely, and
  only when the student verifies in GeoGebra or a simulator.
- AI-generated images, sound or video in Digital Media: unclear rights, and it
  skips the production ILOs. Mention it only as a case in the IP lessons.

### Form and place

- A new box, in the notes (PDF) and on the page:

  ```markdown
  ::: {.callout-note .ai-study title="Study with AI · Explain the dot product in Arabic"}
  Goal: …
  ::: {.prompt}
  Explain the dot product to a first-year student in Arabic … in 5 sentences.
  :::
  Check: the answer must say … If it says …, it is wrong.
  :::
  ```

  - HTML: a "Copy prompt" button (`lesson-script.html`) and its own colour
    (`lesson.css`).
  - PDF: the same box with the prompt printed (`typst-body.typ`).
- 1–2 boxes per lesson, in the hardest section, not one per section ("No
  repetition"). Home study: not counted in the lecture time, not on the
  slides.
- Where (audit judgement per new lecture):
  - game-math: 1, 2, 3, 5, 8, 11, 12, 13, 14 (find the mistake only), 16, 19.
    None in 10 and 18 (unreliable arithmetic; the simulator does it better).
  - computing-systems: 2, 3, 5, 6, 7, 11 (best fit: check AI claims about
    Android and iOS against official sources, the D1 skill), 12, 15, 18.
  - digital-media: 2, 3, 5 (best fit: feedback on the premise against the six
    questions, without the AI rewriting it), 6, 16 (find the mistake: "under
    10 seconds is fair use"), 17. None in the audio and video production
    lessons.
  - digital-skills: 2, 5, 7, 11 (strongest: relative and absolute
    references), 13, 15. None in lessons whose topic is AI. Not before the
    prompts lecture.
- Fixed rules (new `AUTHORING.md` section "Study with AI"):
  - free tools named generally, as in `digital-skills/NOTES.md` (Microsoft
    Copilot with the university account, ChatGPT, Gemini);
  - no personal data;
  - every activity ends with a check;
  - AI is for understanding the lesson, not for writing graded work. Every
    homework page gets one line: "You may use AI to understand the lesson.
    Write the answers yourself.";
  - the rule "no tool or assistant names" keeps applying to how the lessons
    are made, not to the tools students use.
- `check_size.py` counts `.ai-study` boxes: warn above 2 per lesson, and when a
  box has no `.prompt` or no "Check:" line.

## Part 5 · Moodle weeks (16 platform weeks)

These texts go in `courses-private`, not on the site: the site counts
lectures, not weeks, and an "introduction" or "catch-up" week would confuse
students.

- One file per course: `courses-private/moodle/<slug>-weeks.md` (pushed to
  `main` of `courses-private` directly, as usual), with:
  1. **A default map** of platform weeks (week 1 = 11/10/2026) to lectures:

     | Platform week | Content |
     |---|---|
     | 1–2 | Introduction (already filled) |
     | 3 | Lectures 1–2 |
     | 4 | 3–4 |
     | 5 | 5–6 |
     | 6 | 7–8 |
     | 7 | 9–10 |
     | 8 | Midterm exam |
     | 9 | 11–12 |
     | 10 | 13–14 |
     | 11 | 15–16 |
     | 12 | 17–18 |
     | 13 | 19 |
     | 14 | Catch-up and spare |
     | 15 | Final review |
     | 16 | Final exam |

     with the note "the real week follows the last lecture taught".
  2. **Ready Arabic texts for weeks without new teaching**, in the
     university's section template ("الأسبوع … (التاريخ): …", "في هذا الأسبوع
     سوف نعمل على", "في نهاية هذا الأسبوع ستكون قادراً على", "المطلوب من
     الطالب"): introduction, review before the midterm, midterm, catch-up week
     (pointing to the answered pages of earlier lectures), final review, final
     exam. In Digital Skills, never the word "مختبر".
- The texts of actual teaching weeks (which lecture in which week, with links)
  are written on request, when the real pace is known.

## Implementation

Branch from `main`, one pull request, one commit per step below.

1. **Pipeline:** `match.lua` (`Why:`, `.check`, `.ai-study` / `.prompt`),
   `lesson-script.html` (reason, reveal after two wrong tries, copy button),
   `lesson.css`, `typst-body.typ`, `book.lua` ("Results of the Do it tasks"),
   `check_size.py` (new warnings), the two templates. Try it on one lesson
   first.
2. **Rules:** `AUTHORING.md` ("The page teaches, the notes test", "Study with
   AI", 19 lectures and why, a lessons-learned entry for 2026-10-28), and
   `NOTES.md`, `plan.md` and `schedule.yml` of the four courses.
3. **Content, one commit per course** (game-math, computing-systems,
   digital-media, digital-skills):
   - merges and cuts by the maps;
   - new case-study numbers;
   - the error fixes;
   - `Why:` and `.check` on every page;
   - the Study with AI boxes;
   - the slides derived again from the notes;
   - homework renumbered;
   - new GIF recordings only for changed simulators
     (`sh shared/sims/recordings/record-all.sh <name>`).
4. **`courses-private`** (`main`, pushed directly): homework and
   online-activity solutions renumbered; the `moodle/<slug>-weeks.md` files.
5. **Pull request** into `main`, reviewed and merged by the teacher.

## Verification

- `python3 _extensions/lesson/check_size.py --all`: no warnings, including the
  new ones (no Do it without `.check`, no question without `Why:`).
- `python3 _extensions/lesson/check_figures.py`: no warnings.
- A full `quarto render`: no errors; the new download names
  (`math_lecture19.pdf` exists, `math_lecture20.pdf` does not).
- In the browser (`quarto preview`), one lesson of each course:
  - two wrong answers, then the right answer is shown with its reason;
  - "Check your result" opens;
  - "Copy prompt" works;
  - the simulators work inside the page and at phone width;
  - the course page lists 19 lectures and the homework in place.
- One PDF of each course: "Results of the Do it tasks" at the end, no `Why:`
  text inside the lesson.
- One deck of each course in PowerPoint: nothing overlaps.
- Print one online activity and one homework: one A4 page, no answers.
