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
| 5–7 sections | ~60 | definition, figure, 1–2 worked examples, common mistake, code where useful | summary, figure, one Try it (4–6 varied questions), simulator / mini-game | Think → concept (picture) → Example → Try it |
| Case study / Game challenge | ~20 | case study + illustration | 2 Try it on the whole lesson | story + one slide per Try it |
| Summary | 5 | exercises + answers | Summary | Summary |

Ways to go deeper into the same topic (never into next week's topic):
the reverse question, negative numbers, precision (floats), different
screens and conventions (screen space, handedness, Blender ↔ Unity),
discrete grids, reading short game code, several frames in one question.

Mathematics: LaTeX math (`$…$`) in the notes; plain text with
`x~s~` subscripts on the page and slides (no MathJax needed).

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
