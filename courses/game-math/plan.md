# Mathematics and Computing for Digital Games (13411131) — unit plan

Status: plan v3 of 2026-10-31 (`plans/restructure-status.md`), after plan v2 of 2026-10-28 (`plans/restructure-19-lectures.md`). Source: the official syllabus (2026-2027, Drive) and the ILO–PLO matrix.
15 weeks: 12 units (core weeks) and 3 practice weeks (filling weeks) (AUTHORING.md, "Units and sessions"). `schedule.yml` holds the same map for the site and the course package; if they differ, `schedule.yml` wins. "From" names the old lectures and sections that each session is built from.

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

## Weeks: 12 units (Lecture N + Seminar N, 90 min each) and 3 practice weeks

Every week is one lecture and one seminar. The lecture of a unit covers both
lecture columns of its syllabus week; the seminar does the syllabus seminar
topic and practises that lecture.

| Week (syllabus) | Sessions | From (plan v2) | ILOs |
|---|---|---|---|
| Unit 1 (1) | **Lecture 1** Coordinates and Vectors | Lecture 1 | A1 |
| | **Seminar 1** Where Mathematics Appears in a Mobile Game | Seminar 1 | A1 |
| Unit 2 (2) | **Lecture 2** Vector Operations and the Dot Product | Lectures 2 (2.1–2.4, 2.5 as an example) + 3 (3.1–3.3) | A1 B1 |
| | **Seminar 2** Vector Exercises in Game Scenarios | Raft Rush; 3.4 vision cone | A1 B1 |
| Unit 3 (3) | **Lecture 3** The Cross Product, Distance and Projection | Lectures 4 (4.1–4.4) + 5 (5.1–5.3) | B1 |
| | **Seminar 3** Solving Movement and Aiming Problems | 5.4 Asteroid Beam; 4.4 normal and the slide | B1 |
| Unit 4 (4) | **Lecture 4** Trigonometry: the Unit Circle, Rotation and Oscillation | Lectures 6 (6.1–6.4) + 7 (7.1, 7.3, 7.4) | A2 B1 |
| | **Seminar 4** Trigonometry in Game Motion | Turn Lab; Sky Lift | A2 B1 |
| Unit 5 (5) | **Lecture 5** Matrices: Operations, Multiplication, Identity and Inverse | Lecture 8 | A1 C1 |
| | **Seminar 5** Matrix Exercises | Seminar 2 | A1 C1 |
| Unit 6 (6) | **Lecture 6** Translation, Scaling and Rotation in 2D | Lecture 9 | C1 |
| | **Seminar 6** Composing 2D Transformations | Seminar 3 | C1 |
| Unit 7 (7) | **Lecture 7** Homogeneous Coordinates and 3D Transformations | Lecture 10 | C1 |
| | **Seminar 7** Transformation Chains: Object, World and Camera Space | Seminar 4 | C1 |
| Practice week (8) | **Practice 1** Revision of Lectures 1–7 (then the midterm) | Seminar 5 | A1 A2 B1 C1 |
| Unit 8 (9) | **Lecture 8** Propositions, Logical Operators and Truth Tables | Lecture 11 | A2 B2 |
| | **Seminar 8** Logic Exercises: Game States and Conditions | Seminar 6 | A2 B2 |
| Unit 9 (10) | **Lecture 9** Boolean Algebra and Decision Conditions | Lecture 12 | B2 |
| | **Seminar 9** Designing a Rule Set for a Simple Game | Seminar 7 | B2 |
| Unit 10 (11) | **Lecture 10** Probability: Events, Conditional Probability and Expected Value | Lectures 13 (13.1–13.5) + 14 (14.1 with 14.2, 14.3 with 14.4) | A2 B2 |
| | **Seminar 10** Probability in Loot Drops and Critical Hits | 13.6 Roll Lab; Conditional Lab; Crate Lab | A2 B2 |
| Unit 11 (12) | **Lecture 11** Random Numbers: Generators, Seeds and Distributions | Lecture 15 | C2 |
| | **Seminar 11** Generating Random Events in a Game Scenario | Seminar 8 | C2 |
| Unit 12 (13) | **Lecture 12** Probability for Game Balance and Fairness | Lecture 16 | C2 |
| | **Seminar 12** Game Balancing Exercise (with a reply presented alone: D1) | Seminar 9 | C2 D1 |
| Practice week (14) | **Practice 2** Applied Problem Set: Vectors, Transformations and Probability | Seminar 10 | B1 C1 C2 |
| | **Practice 3** Case Study: Movement of a 2D Object (team activity in the worksheet) | Lecture 17 | B1 C1 D1 |
| Practice week (15) | **Practice 4** Case Study: Random Level and Event Generation | Lecture 18 | B2 C2 |
| | **Practice 5** Course Revision (present one solution alone) | Lecture 19 | all |

- Core: Lectures 1–12 and Seminars 1–12. Flexible: Practice 1–5 (no new
  ideas; studied at home when not held).
- The 15-week plan on the e-learning platform: units 1–7, practice week 8
  (with the midterm), units 8–12, practice weeks 14 and 15; the final exam
  follows in the university's exam week. When weeks are lost, the practice
  weeks are dropped first.
- **Cut (plan v3):** the vision cone as a section, back-face culling, the ray
  test as a lecture section, turning the short way; theory and experiment
  moved to Seminar 10. Earlier cuts (plan v2) stay cut: transpose and the
  engine's 4 × 4 matrix, the general inverse formula, reflection as a
  section, Rᵀ = R⁻¹, formal logic (contrapositive, iff), the state machine,
  short-circuit evaluation, bell-shaped distributions, logarithms in drop
  rates, PRD, flood fill, acceleration and damping, geometric probability,
  Unity code that no task needs.
- **Homework:** 12, one per unit (due before the next lecture; Homework 12
  one week after Lecture 12); none in a practice week.

## Tasks with AI (ideas)

a sheet of 1000 rolls of a loot table or a crit chance against the expected value; GeoGebra commands from the AI for a path of 10 points or a chain of transformations, checked at two points by hand; a rule table (truth table) for a door with four conditions, checked row by row.

## Notes

- **Independent study first.** The notes, the interactive page and the homework are enough to study alone. Pages, slides and homework never require classmates.
- **Team activity (D1): one session only.** The syllabus week-14 seminar asks for group problem solving and presentation, so the worksheet of Practice 3 contains one short team activity box, with an individual alternative. No other session has team work. Seminar 12 (core) has a reply presented alone; in Practice 5 each student presents one solution alone.
- Homework: one per unit (12), none in a practice week; it practises the lecture of its unit only.
