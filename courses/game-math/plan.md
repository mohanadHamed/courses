# Mathematics and Computing for Digital Games (13411131) — unit plan

Status: approved on 2026-10-28 (`plans/restructure-19-lectures.md`, version 2). Source: the official syllabus (2026-2027, Drive) and the ILO–PLO matrix.
One unit = one week of the syllabus (AUTHORING.md, "Units and sessions"). `schedule.yml` holds the same map for the site and the course package; if they differ, `schedule.yml` wins. "From" names the old lectures and sections that each session is built from.

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

## Units: 15 units, 19 lectures + 10 seminars (90 min each)

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

## Tasks with AI (ideas)

a sheet of 1000 rolls of a loot table or a crit chance against the expected value; GeoGebra commands from the AI for a path of 10 points or a chain of transformations, checked at two points by hand; a rule table (truth table) for a door with four conditions, checked row by row.

## Notes

- **Independent study first.** The notes, the interactive page and the homework are enough to study alone. Pages, slides and homework never require classmates.
- **Team activity (D1): one session only.** The syllabus week-14 seminar asks for group problem solving and presentation, so the notes (PDF) of Lecture 17 contain one short team activity box, with an individual alternative. No other session has team work. In Lecture 19 each student presents one solution alone.
- In a week with two lectures, the syllabus seminar topic is the Game challenge of the second lecture. In a week with one merged lecture, the second session is a seminar.
- Homework: one per unit (13), none after units 8 and 15; it practises the lectures of its unit only.
