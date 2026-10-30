# Mathematics and Computing for Digital Games (13411131) — course notes

Course-specific rules only. Global rules are in the root `AUTHORING.md`.

## Timing and textbook

- 2 lectures × 90 min (3 credit hours). Lesson A = syllabus First Lecture,
  Lesson B = Second Lecture; the syllabus seminar becomes the case study and
  Game challenge of lesson A.
- Textbook: Dunn and Parberry, *3D Math Primer for Graphics and Game
  Development*, 2nd ed. (ch. 1 coordinate systems, ch. 2 vectors, …). Follow
  its order and rigour; never copy it.

## Shape of a 90-min lesson

| Part | Minutes | Notes (PDF) | Page | Slides |
|---|---|---|---|---|
| Key terms | 5 | glossary 10–14 terms | glossary | Keywords |
| 5–7 sections | ~60 | definition, figure, 1–2 worked examples, common mistake, code where useful | summary, figure, one Try it (4–6 varied questions, each with `Why:`), simulator / mini-game | concept (picture) → Example → Try it |
| Case study / Game challenge | ~20 | case study + illustration | 2 Try it on the whole lesson | story + one slide per Try it |
| Summary | 5 | exercises + answers | Summary | Summary |

Ways to go deeper into the same topic (never into next week's topic):
the reverse question, negative numbers, precision (floats), different
screens and conventions (screen space, handedness, Blender ↔ Unity),
discrete grids, reading short game code, several frames in one question.

Mathematics: LaTeX math (`$…$`) in the notes; plain text with
`x~s~` subscripts on the page and slides (no MathJax needed).

## Units and seminars (2026-10-28)

- 15 units = syllabus weeks 1–15: 19 lectures (core) and 10 seminars
  (flexible). In a week with two lectures (units 2, 3, 4, 11, 15) the
  syllabus seminar topic is the Game challenge of the second lecture; in a
  week with one merged lecture the second 90-min session is a seminar with
  the syllabus seminar title. Unit 8 is the revision seminar (Seminar 5).
- A 90-min seminar (since 2026-10-30): Recall, two short problems (three
  at most) that together use every concept of the lecture, about 60 of the
  90 minutes planned (the rest for explaining), a Wrap-up; no separate Game
  challenge. A game that the merged lectures gave up (Multiply Lab, Asteroid
  Beam, Lighthouse, Problem Drill, Star Dock Missions) is the tool of an
  activity when it fits.
- Tasks with AI fit here when the AI does the long part and the student
  checks it: a sheet of 1000 loot rolls against the expected value,
  GeoGebra commands for a path or a chain of transformations checked at two
  points by hand, a truth table for a door with four conditions. Never trust
  AI arithmetic without a check.

## Lessons learned

- Week 1 (2026-10-17): the first lessons had 12 and 21 "Try it" questions and no
  worked examples: too short for 90 min. Rebuilt with 45–49 questions.
- Week 1 (2026-10-19, after teaching): those 45–49 questions were mostly the
  same question again (axes, moving points, 2D and 3D coordinates), and the
  English was too simple. Rebuilt as textbook-style notes with six distinct
  sections per lesson (game loop, 1D, 2D, screen space, tile grids, 3D;
  scalars, arrows, components, displacement, motion per frame, 3D vectors),
  one question set per section, and mini-games (Grid Strike, Vector Dash).
- Week 1 (2026-10-19, applied first): rebuilt again at a slightly easier
  level in simple English, with a Do it task in every section: GeoGebra
  (points, vectors), a spreadsheet (board index), paper (number line) and the
  mini-games (Grid Strike, Vector Dash, the 3D viewer). Simplifying cut the
  notes below 2 500 words; extra game-based worked examples (not theory)
  brought them back. Left out: float precision, screen fitting, basis
  vectors, n-dimensional vectors.
- Week 1 (2026-10-19, level check, about 20 % simpler): screen space and
  world space with their conversion formulas, the tile-grid index and the
  Blender ↔ Unity conversion were removed (no syllabus week or ILO asks for
  them). Handedness stays, because the cross product (week 3) needs it.
- Week 1 (2026-10-21, teacher review): the hand rule no longer names single
  fingers (the middle finger is not a polite gesture to ask for in class).
  It is the curl rule: the fingers point along +x and bend towards +y; the
  thumb shows +z. Use this wording in every lesson.
- 2026-10-28 (plan v2): 29 lectures became 19 lectures and 10 seminars.
  Cut as beyond the ILOs: transpose and the engine's 4 × 4 matrix, the
  general inverse formula, reflection, Rᵀ = R⁻¹ and the determinant proof,
  formal logic (contrapositive, iff), the state machine and its code,
  short-circuit evaluation, bell-shaped distributions, logarithms in drop
  rates, PRD, flood fill (BFS), acceleration and damping, geometric
  probability, √2 ≈ 1.41-style arithmetic, `Rad2Deg`, `DeltaAngle`,
  `sqrMagnitude`, and Unity code that no task needs. Case studies get new
  numbers (they reused the worked examples, so the notes held the Game
  challenge answers). Fix: Turn Lab's target (6, 1) is at 9.5°, not 10°.
