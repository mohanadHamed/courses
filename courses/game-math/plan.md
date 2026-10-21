# Mathematics and Computing for Digital Games (13411131) — 16-week plan

Status: draft for approval, 2026-10-19. Source: official syllabus (2026-2027, Drive) and the ILO–PLO matrix v4.
The weekly map below follows the syllabus weeks; the site shows only the lecture numbers (no weeks, no exams; AUTHORING.md, "Lectures, not weeks"). If they differ, `schedule.yml` wins.

Per week (as taught): 2 lectures × 90 min → 2 lessons (A = First Lecture, B = Second Lecture; the syllabus seminar → case study and Game challenge of lesson A). Each lesson has notes (PDF), an interactive page and slides (see AUTHORING.md).

## Course ILOs

| Code | ILO (official text, with PLOs) |
|---|---|
| A1 | Explain the concepts of vectors, matrices, and two- and three-dimensional coordinates and their role in games. (PLO 1) |
| A2 | Explain the principles of trigonometry, probability, and mathematical logic and their applications in games. (PLO 1) |
| B1 | Analyze position and motion problems in games using vectors and trigonometry. (PLO 1) |
| B2 | Apply mathematical logic and probability to solve decision-making and randomness problems in games. (PLO 1, 2) |
| C1 | Apply geometric transformations (translation, rotation, and scaling) using matrices. (PLO 1) |
| C2 | Employ random numbers and probability to generate variable events and behavior that support game balance. (PLO 1, 2) |
| D1 | Present mathematical solutions and collaborate with peers in solving applied problems. (PLO 4) |

## Weekly map

| Week | Lecture | Title | Lesson ILOs | Week ILOs | PLOs |
|---|---|---|---|---|---|
| 01 | 01 | Mathematics in Game Development and Coordinate Systems | A1 | A1 | 1 |
| 01 | 02 | Vectors: Definition, Components and Basic Operations | A1 |  |  |
| 02 | 03 | Vector Operations: Addition, Scaling, Magnitude and Normalization | A1, B1 | A1, B1 | 1 |
| 02 | 04 | The Dot Product and the Angle Between Vectors | A1, B1 |  |  |
| 03 | 05 | The Cross Product: Direction and Surface Normals | B1 | B1 | 1 |
| 03 | 06 | Distance, Projection and Direction in Game Worlds | B1 |  |  |
| 04 | 07 | Trigonometry: Sine, Cosine, Tangent and the Unit Circle | A2 | A2, B1 | 1 |
| 04 | 08 | Applied Trigonometry: Angles, Rotation and Oscillating Motion | A2, B1 |  |  |
| 05 | 09 | Matrices: Definition and Basic Operations | A1 | A1, C1 | 1 |
| 05 | 10 | Matrix Multiplication, the Identity and the Inverse | A1, C1 |  |  |
| 06 | 11 | Translation and Scaling Transformations | C1 | C1 | 1 |
| 06 | 12 | Rotation in 2D | C1 |  |  |
| 07 | 13 | Homogeneous Coordinates and Transformation Matrices | C1 | C1 | 1 |
| 07 | 14 | 3D Transformations: Translation, Rotation and Scaling | C1 |  |  |
| 08 | 15 | Revision of Lectures 1–14 | A1, A2, B1, C1 | A1, A2, B1, C1 | 1 |
| 08 | — | *Midterm exam — no lesson* | |  |  |
| 09 | 16 | Mathematical Logic: Propositions and Logical Operators | A2 | A2, B2 | 1, 2 |
| 09 | 17 | Truth Tables and Logical Conditions in Game Rules | A2, B2 |  |  |
| 10 | 18 | Boolean Algebra and Decision Conditions | B2 | B2 | 1, 2 |
| 10 | 19 | Applying Logic to Game Rules and Decisions | B2 |  |  |
| 11 | 20 | Probability Basics: Events and Sample Space | A2 | A2, B2 | 1, 2 |
| 11 | 21 | Conditional Probability and Expected Value | A2, B2 |  |  |
| 12 | 22 | Random Numbers: Pseudo-Random Generators and Seeds | C2 | C2 | 1, 2 |
| 12 | 23 | Random Distributions: Uniform and Weighted | C2 |  |  |
| 13 | 24 | Probability for Game Balance: Drop Rates and Difficulty | C2 | C2 | 1, 2 |
| 13 | 25 | Randomness and Fairness: The Player's Perception | C2 |  |  |
| 14 | 26 | Applied Problem Set: Vectors, Transformations and Probability | B1, C1 | B1, C1, D1 | 1, 4 |
| 14 | 27 | Case Study: Movement of a 2D Object | B1, C1, D1 |  |  |
| 15 | 28 | Case Study: Random Level and Event Generation | C2 | C2, D1 | 1, 2, 4 |
| 15 | 29 | Course Revision | C2, D1 |  |  |
| 16 | — | *Final exam — no lesson* | | All | 1, 2, 4 |

## ILO coverage

| ILO | Lessons |
|---|---|
| A1 | L01, L02, L03, L04, L09, L10, L15 |
| A2 | L07, L08, L15, L16, L17, L20, L21 |
| B1 | L03, L04, L05, L06, L08, L15, L26, L27 |
| B2 | L17, L18, L19, L21 |
| C1 | L10, L11, L12, L13, L14, L15, L26, L27 |
| C2 | L22, L23, L24, L25, L28, L29 |
| D1 | L27, L29 |

## Notes

- **Independent study first.** The notes, the interactive page and the homework are enough to study alone. Pages, slides and homework never require classmates.
- **Team activity (D1, collaborate with peers): one lesson only.** The week-14 seminar asks for group problem solving and presentation, so the notes (PDF) of lesson 27 contain one short team activity box (solve a problem in a small team and present the solution), with an individual alternative for a student who works alone. No other lesson has team work.
- Week 15 seminar (student presentations): each student presents a solution alone.
- Week 8: revision lesson (15) and midterm exam. Week 16: final exam.
- One homework per week (`week-NN/homework-NN.qmd`), not in weeks 8 and 16: 1–2 simple tasks, under 10 minutes. Tasks are public; solutions stay private.
