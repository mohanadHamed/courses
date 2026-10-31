# Mathematics and Computing for Digital Games (13411131) — course notes

Course-specific rules only. Global rules are in the root `AUTHORING.md`.

## Timing and textbook

- 3 credit hours (2 theory + 1 seminar), taught every week as one lecture
  of 90 min and one seminar of 90 min. The lecture of a unit covers both
  lecture columns of its syllabus week (First Lecture and Second Lecture);
  the seminar does the syllabus seminar topic and practises that lecture.
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

## Units, seminars and practice weeks (plan v3, 2026-10-31)

- 15 weeks: 12 units (core: Lecture N, Seminar N, Homework N; syllabus
  weeks 1–7 and 9–13) and 3 practice weeks (flexible: week 8, Practice 1,
  revision of Lectures 1–7; week 14, Practice 2 applied problem set and
  Practice 3 case study: movement of a 2D object; week 15, Practice 4 case
  study: random levels and Practice 5 course revision). The syllabus weeks
  with two lectures (2, 3, 4, 11) have one merged lecture of 7 sections; the
  second application of each idea is in the seminar of the week.
- D1 (present solutions, team work) has a core part in Seminar 12 (a reply
  of three sentences, presented alone); the team activity is in the
  worksheet of Practice 3, with an individual alternative, and Practice 5
  presents a solution in five parts.
- A 90-min seminar (since 2026-10-30): Recall, two short problems (three
  at most) that together use every concept of the lecture, about 60 of the
  90 minutes planned (the rest for explaining), a Wrap-up; no separate Game
  challenge. A game that the merged lectures gave up (Multiply Lab, Asteroid
  Beam, Raft Rush, Sky Lift, Turn Lab, Roll Lab, Crate Lab) is the tool of an
  activity when it fits.
- Tasks with AI (an extra for the curious; AUTHORING.md): the AI draws
  what the lesson computes, from a complete prompt with every number: the
  frames of a ship on a grid, a level with its quadrants, a sprite before
  and after a matrix, transformed blocks, a planet and its moon, a coloured
  truth table or decision table, a chart of 1000 draws or 1000 hunters. The
  changes to try change one number or one word (a velocity, the order of
  two rules, a chance), and their closed answers say what changes and why.
  No graded task needs AI: Homework 1 does the patrol by hand and ends with
  an optional Task with AI (no marks) about another robot.

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
- 2026-10-31 (plan v3): every week is one lecture and one seminar, and the
  course has 12 core weeks and 3 practice weeks. Old Lectures 2+3, 4+5, 6+7
  and 13+14 were merged (7 sections each). Cut from the lectures: the vision
  cone as a section (it is in the Game challenge story and Seminar 2),
  back-face culling and the ray test (the beam is a problem of Seminar 3),
  turning the short way, and theory and experiment (now Seminar 10). Removed:
  Fair Speed and Raft Odds. Old Lectures 17–19 became Practices 3–5 in the
  practice format; Homework 14 was removed.
- 2026-10-31 (teacher's review of the AI boxes): the eleven "Task with AI"
  boxes (Lecture 1 notes and page, Seminars 1, 5, 6, 7, 8, 9, 11, 12 and
  Practice 2) became extras with a complete prompt, a picture or a coloured
  table to look at, and two or three changes to try with closed answers.
- 2026-10-31 (teacher's decision): AI is always an optional extra, also in
  homework. Homework 1, Task 2 (3 marks) is done by hand (the velocity, the
  positions, a drawing); the AI box became an optional section with no
  marks, about another robot, hidden on paper.
