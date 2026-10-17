# Mathematics and Computing for Digital Games (13411131) — 16-week plan

Status: **approved 2026-10-17** (Phase 1). Lesson titles only, no content yet.
Source: official syllabus 13411131 (2026-2027, Drive), weekly schedule and ILOs.
ILO text is in `_metadata.yml`.

Per week (as taught): 2 lectures × 90 min → 2 lessons
(A = First Lecture, B = Second Lecture; the syllabus seminar → class activity).
Week 8: revision + midterm. Week 16: final exam.

## Course ILOs

| Code | ILO (short) | PLO |
|---|---|---|
| A1 | Vectors, matrices, 2D/3D coordinates and their role in games | 1 |
| A2 | Trigonometry, probability and logic and their use in games | 1 |
| B1 | Analyze position and motion problems with vectors and trigonometry | 1 |
| B2 | Use logic and probability for decisions and randomness | 1, 2 |
| C1 | Translate, rotate and scale with matrices | 1 |
| C2 | Use random numbers and probability for varied events and game balance | 1, 2 |
| D1 | Present math solutions and work with peers | 4 |

## Weekly map

"Week ILOs" and "PLOs" are copied from the syllabus. "Lesson ILOs" is what each
lesson puts in `ilos:` (always a part of the week ILOs).

| Week | Lesson | Title | Lesson ILOs | Week ILOs | PLOs |
|---|---|---|---|---|---|
| 01 | 01 | Math in games: where is everything? (2D and 3D coordinates) | A1 | A1 | 1 |
| | 02 | Vectors: arrows that move things | A1 | | |
| | | *Class activity:* find the math in a mobile game | | | |
| 02 | 03 | Vector math: add, scale, length and normalize | A1, B1 | A1, B1 | 1 |
| | 04 | Dot product: the angle between two vectors | A1, B1 | | |
| | | *Class activity:* vector problems in game scenes | | | |
| 03 | 05 | Cross product: direction and normals | B1 | B1 | 1 |
| | 06 | Distance, projection and direction in a game world | B1 | | |
| | | *Class activity:* movement and aiming problems | | | |
| 04 | 07 | Trigonometry: sine, cosine, tangent and the unit circle | A2 | A2, B1 | 1 |
| | 08 | Trigonometry in action: angles, turning and waves | A2, B1 | | |
| | | *Class activity:* trigonometry in game motion | | | |
| 05 | 09 | Matrices: tables of numbers | A1 | A1, C1 | 1 |
| | 10 | Matrix multiplication, identity and inverse | A1, C1 | | |
| | | *Class activity:* matrix exercises | | | |
| 06 | 11 | Move and resize: translation and scaling | C1 | C1 | 1 |
| | 12 | Turn it: rotation in 2D | C1 | | |
| | | *Class activity:* combine 2D transformations | | | |
| 07 | 13 | Homogeneous coordinates: one matrix for every change | C1 | C1 | 1 |
| | 14 | Transformations in 3D: move, turn and scale | C1 | | |
| | | *Class activity:* object, world and camera space | | | |
| 08 | 15 | Revision: weeks 1–7 | A1, A2, B1, C1 | A1, A2, B1, C1 | 1 |
| | 16 | *Midterm exam — no lesson* | | | |
| 09 | 17 | Logic: true or false, AND, OR, NOT | A2 | A2, B2 | 1, 2 |
| | 18 | Truth tables and conditions in game rules | A2, B2 | | |
| | | *Class activity:* game states and conditions | | | |
| 10 | 19 | Boolean algebra: making decisions | B2 | B2 | 1, 2 |
| | 20 | Logic for game rules and decisions | B2 | | |
| | | *Class activity:* design the rules of a simple game | | | |
| 11 | 21 | Probability: events and outcomes | A2 | A2, B2 | 1, 2 |
| | 22 | Conditional probability and expected value | A2, B2 | | |
| | | *Class activity:* loot drops and critical hits | | | |
| 12 | 23 | Random numbers: generators and seeds | C2 | C2 | 1, 2 |
| | 24 | Random distributions: uniform and weighted | C2 | | |
| | | *Class activity:* random events in a game scene | | | |
| 13 | 25 | Probability for balance: drop rates and difficulty | C2 | C2 | 1, 2 |
| | 26 | Fair randomness: what the player feels | C2 | | |
| | | *Class activity:* balance a game | | | |
| 14 | 27 | Problem set: vectors, transformations and probability | B1, C1 | B1, C1, D1 | 1, 4 |
| | 28 | Case study: moving a 2D object | B1, C1, D1 | | |
| | | *Class activity:* solve in groups and present | | | |
| 15 | 29 | Case study: random levels and events | C2 | C2, D1 | 1, 2, 4 |
| | 30 | Course revision | C2, D1 | | |
| | | *Class activity:* students present their solutions | | | |
| 16 | 31 | *Final exam — no lesson* | | All | 1, 2, 4 |
| | 32 | *Exam week — no lesson* | | | |

## ILO coverage

| ILO | Weeks (lessons) |
|---|---|
| A1 | 1–2, 5, 8 (L01–L04, L09–L10, L15) |
| A2 | 4, 8, 9, 11 (L07–L08, L15, L17–L18, L21–L22) |
| B1 | 2–4, 8, 14 (L03–L08, L15, L27–L28) |
| B2 | 9–11 (L18–L22) |
| C1 | 5–8, 14 (L10–L15, L27–L28) |
| C2 | 12, 13, 15 (L23–L26, L29–L30) |
| D1 | 14, 15 (L28, L30 — group work and presentations) |

## Notes

- Each week has one seminar activity. It goes at the end of the lesson that
  fits it best (week 1: lesson 01). The other lesson gets a shorter class
  activity on its own topic.
- D1 is built only in the group work and presentations of weeks 14–15.
  Pair work in other class activities also practises it.
- Week 8 seminar ("Midterm discussion") is not a lesson.
- Slides for every lesson are interactive: each "Try it" is a question slide,
  plus "Think" slides before new ideas; answers show on click
  (see "Interactive slides" in AUTHORING.md).
- Every "Try it" in a lesson is a matching exercise with instant feedback
  (see "Try it: match the answer" in AUTHORING.md).
