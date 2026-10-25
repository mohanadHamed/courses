---
title: "Applied Problem Set: Vectors, Transformations and Probability"
description: "Five steps for applied problems, then worked game problems from Star Dock: a shuttle's velocity and flight time, a turret's field of view and turn angle, a docking arm turned and scaled about a pivot, geometric probability and hits, and a mixed mission that needs every tool."
lesson: 26
ilos: [B1, C1]
format: lesson-html
---

This page is the interactive version of the lesson notes (PDF). Each section
has a short summary, a picture, a **Do it** task and one set of questions.
The full explanations, examples and exercises are in the notes.

## Key terms

{{< glossary applied-problem vector magnitude unit-vector velocity dot-product field-of-view atan2 rotation-matrix pivot composite-transformation geometric-probability expected-value complement-event >}}

## 26.1 Five steps for an applied problem

- **Read** (given, asked) → **draw** → **choose the tool** → **compute**
  (with units) → **check**.
- Step between points: vector. Can it see / how far to turn: dot product or
  atan2. About a point: pivot. How often: probability.

![Five steps.](images/five-steps.png){width=94%}

::: {.callout-warning title="Watch out!"}
Draw first, then choose the tool.
:::

::: {.callout-note title="Do it · Plan, do not compute"}
Write steps 1–3 for: a laser from (0, 0) to (30, 40); a guard facing (1, 0)
and a thief at (2, 5); a random point in a 10 × 10 square and a 2 × 3 box.
:::

::: {.callout-tip title="Try it 1 · Choose the tool"}
Choose the tool.

::: {.match extra="a truth table|a seed"}
how long a trip from A to B takes
:   the length of B − A

whether a guard can see a thief
:   the dot product of unit vectors

the tip of an arm turned about its base
:   a rotation about a pivot

how often a random point lands in a zone
:   area ÷ area
:::
:::

## 26.2 Problem A: the shuttle

- d = D − S; distance |d|; unit direction d / |d|.
- Velocity = speed × unit direction; per frame: × Δt.
- Time = distance ÷ speed.

![Problem A: the shuttle.](images/shuttle.png){width=94%}

::: {.callout-warning title="Watch out!"}
Never move by the whole step d every frame.
:::

::: {.callout-note title="Do it · Your shuttle"}
A pod at (−3, 2) flies to (9, 7) at 2.6 units per second, 50 fps: distance,
velocity, step per frame, time.
:::

::: {.callout-tip title="Try it 2 · The shuttle"}
S (2, 1), D (14, 10), 3 units per second, 60 fps. Choose the right answer.

::: {.match extra="(12, 9)|21"}
the distance
:   15

the unit direction
:   (0.8, 0.6)

the velocity
:   (2.4, 1.8)

the flight time
:   5 s
:::
:::

## 26.3 Problem B: the turret

- Unit vector to the target u; facing f.
- **Seen:** f · u ≥ cos(view ÷ 2) and distance ≤ range.
- **Turn:** atan2(u~y~, u~x~) − atan2(f~y~, f~x~).

![Problem B: the turret.](images/turret.png){width=94%}

::: {.callout-warning title="Watch out!"}
A 90° view compares with cos 45°, not cos 90°.
:::

::: {.callout-note title="Do it · Your turret"}
Turret at (1, 1) facing (1, 0), 60° view, range 10, target at (9, 7): seen?
How far to turn?
:::

::: {.callout-tip title="Try it 3 · The turret"}
T (4, 2), facing (0, 1), 90° view, range 6, E (7, 6). Choose the right answer.

::: {.match extra="0.6|cos 90° = 0"}
the unit vector to E
:   (0.6, 0.8)

the dot product
:   0.8

compare it with
:   cos 45° ≈ 0.707

the turn
:   about 36.9° clockwise
:::
:::

## 26.4 Problem C: the docking arm

- About a pivot P: **subtract P → rotate or scale → add P**.
- 90° counterclockwise: (x, y) → (−y, x); factor k: (kx, ky).
- One matrix: T(P) · R(θ) · T(−P).

![Problem C: the docking arm.](images/arm.png){width=94%}

::: {.callout-warning title="Watch out!"}
Rotating about the origin moves the arm away from its pivot.
:::

::: {.callout-note title="Do it · Your arm"}
Pivot (−1, 2), tip (2, 6): rotate 90° counterclockwise, then scale by 0.5
about the pivot.
:::

::: {.callout-tip title="Try it 4 · The arm"}
P (3, 2), A (7, 2). Choose the right answer.

::: {.match extra="(7, 6)|(0, 0)"}
A − P
:   (4, 0)

A after 90° counterclockwise about P
:   (3, 6)

then scaled by 1.5 about P
:   (3, 8)

A rotated about the origin (wrong)
:   (−2, 7)
:::
:::

## 26.5 Problem D: asteroids and shots

- **Geometric probability:** area of the part ÷ area of the region.
- At least one in n: 1 − (1 − p)^n^. Expected: n · p.

![Problem D: asteroids.](images/spawn.png){width=94%}

::: {.callout-warning title="Watch out!"}
Compare areas, not lengths.
:::

::: {.callout-note title="Do it · Your probabilities"}
A 30 × 20 map, a 6 × 5 trap: P(on the trap)? Of 40 enemies, how many on the
trap on average?
:::

::: {.callout-tip title="Try it 5 · Asteroids and shots"}
Choose the right answer.

::: {.match extra="0.3|0.216"}
P(inside the shield), radius 3, 20 × 10
:   about 0.14

asteroids inside the shield, of 50
:   about 7

P(at least one hit), 3 shots, p = 0.6
:   0.936

expected hits, 3 shots, p = 0.6
:   1.8
:::
:::

## 26.6 Problem E: a mixed mission

- Split into parts; one tool per part; write each result.
- Keep 2–3 decimals until the end.

{{< sim file="sims/problem-drill.html" poster="sims/problem-drill.png" title="Problem Drill: Star Dock" height="560" >}}

::: {.callout-warning title="Watch out!"}
Rounding early makes every later part a little wrong.
:::

::: {.callout-note title="Do it · Your mission"}
Drone at (2, 1) facing (0, 1), asteroid at (−3, 13), 2.6 units per second,
p = 0.2: time, turn angle, P(at least one crystal in 5).
:::

::: {.callout-tip title="Try it 6 · The mining drone"}
Dock (0, 0), facing (1, 0), asteroid (6, 8), 2 units per second, p = 0.25.
Choose the right answer.

::: {.match extra="14 s|0.25"}
the flight time
:   5 s

the turn angle
:   about 53.1°

P(at least one crystal in 4 asteroids)
:   about 0.68

crystals in 20 asteroids, on average
:   5
:::
:::

## Game challenge: Star Dock Missions {.challenge}

Work alone. Use every section of today.

Six missions: the **flight time**, the **velocity**, the **turret**, the
**arm**, the **shield** and **three shots**.

{{< sim file="sims/star-dock-missions.html" poster="sims/star-dock-missions.png" title="Star Dock Missions: one tool for each problem" kind="game" height="440" >}}

::: {.callout-tip title="Try it 7 · The missions"}
Choose the right answer.

::: {.match extra="7 s|(7, 6)"}
the shuttle's flight time
:   5 s

the turret sees the target because
:   0.8 ≥ 0.707 and 5 ≤ 6

the new tip of the arm
:   (3, 6)

1 − 0.4³
:   0.936
:::
:::

::: {.callout-tip title="Try it 8 · Compute (harder)"}
Choose the right answer.

::: {.match extra="(5, 1)|0.49"}
rotate (5, 1) by 90° about (2, 1)
:   (2, 4)

scale (5, 1) by 2 about (2, 1)
:   (8, 1)

P(at least one hit in 2), p = 0.7
:   0.91

P(in a circle r = 2), 10 × 10 square
:   about 0.126
:::
:::

## Summary {.summary}

- Read, draw, choose the tool, compute, check.
- Motion: step, length, unit direction, velocity, Δt.
- Seeing: dot product with cos(view ÷ 2); turning: atan2.
- About a pivot: subtract, transform, add back.
- Probability: area ratios, 1 − (1 − p)^n^, n · p.
