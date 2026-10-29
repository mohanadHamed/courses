---
title: "Applied Problem Set: Vectors, Transformations and Probability"
subtitle: "Lecture 26"
format: lesson-pptx
---

## Keywords

{{< glossary applied-problem unit-vector velocity dot-product atan2 pivot composite-transformation geometric-probability expected-value >}}

## 26.1 Five steps

:::: {.columns}
::: {.column width="50%"}
- We read what is given and what is asked.
- We draw a sketch and choose the tool.
- We compute with units and check the answer.
- **Do it:** Write a plan for a laser from (0, 0) to (30, 40). Which tool do you choose?
:::
::: {.column width="50%"}
![](images/five-steps.png)
:::
::::

## Example · The cargo drone

A cargo drone at (1, 1) must reach a crate at (4, 5) in 2 seconds.
**How fast must it fly?**

::: {.reveal}
1. The step is (4, 5) − (1, 1) = **(3, 4)**, with length **5**.
2. The speed is 5 ÷ 2 = **2.5 units per second**.
3. Check: 2.5 units per second for 2 seconds gives 5 units.
:::

## Try it 1 · Choose the tool

a) Which tool tells whether a guard can see a thief?
b) Which tool gives the tip of an arm turned about its base?
c) Which tool gives how often a random point lands in a zone?

::: {.answer}
a) the dot product of unit vectors
b) a rotation about a pivot
c) area ÷ area
:::

## 26.2 Problem A: the shuttle

:::: {.columns}
::: {.column width="50%"}
- The step is D − S, and its length is the distance.
- The velocity is the speed times the unit direction.
- The time is the distance divided by the speed.
- **Do it:** Find the flight time of a pod from (−3, 2) to (9, 7) at 2.6 units per second. What is it?
:::
::: {.column width="50%"}
![](images/shuttle.png)
:::
::::

## Example · The shuttle

The shuttle flies from S (2, 1) to D (14, 10) at 3 units per second, at 60 fps.
**What are the velocity and the flight time?**

::: {.reveal}
1. D − S = **(12, 9)**, with length √225 = **15**.
2. The velocity is 3 × (0.8, 0.6) = **(2.4, 1.8)**, so each frame moves (0.04, 0.03).
3. The flight takes 15 ÷ 3 = **5 s**, which is 300 frames.
:::

## Try it 2 · The shuttle

a) What is the unit direction of (12, 9)?
b) What is the step per frame at 60 fps for the velocity (2.4, 1.8)?
c) Why must the shuttle not move by (12, 9) every frame?

::: {.answer}
a) (0.8, 0.6)
b) (0.04, 0.03)
c) It would jump past the dock at once.
:::

## 26.3 Problem B: the turret

:::: {.columns}
::: {.column width="50%"}
- We find the unit vector to the target.
- A target is seen when the dot product is at least cos(view ÷ 2).
- The turn angle comes from atan2.
- **Do it:** Decide if a turret at (1, 1) facing (1, 0) with a 60° view sees (9, 7). Does it?
:::
::: {.column width="50%"}
![](images/turret.png)
:::
::::

## Example · The turret

The turret at T (4, 2) faces (0, 1), with a 90° view and range 6.
**Can it see a target at E (7, 6), and how far must it turn?**

::: {.reveal}
1. E − T = (3, 4), with distance **5** and unit vector **(0.6, 0.8)**.
2. The dot product is **0.8 ≥ 0.707** and 5 ≤ 6, so the target is seen.
3. atan2 gives 53.1°, so the turret turns **36.9° clockwise** from 90°.
:::

## Try it 3 · The turret

a) Which value do we compare with for a 90° field of view?
b) Is a target with dot product 0.6 inside a 90° view?
c) How far must a guard facing (1, 0) turn towards (3, 4)?

::: {.answer}
a) cos 45° ≈ 0.707
b) No, because 0.6 < 0.707.
c) about 53.1° counterclockwise
:::

## 26.4 Problem C: the docking arm

:::: {.columns}
::: {.column width="50%"}
- We subtract the pivot, then rotate or scale.
- Then we add the pivot back.
- The composite matrix is T(P) R(θ) T(−P).
- **Do it:** Rotate the tip (2, 6) about the pivot (−1, 2) by 90°. Where is it now?
:::
::: {.column width="50%"}
![](images/arm.png)
:::
::::

## Example · Turn, then grow

The arm turns 90° counterclockwise about P (3, 2), then grows by 1.5.
**Where is the tip A (7, 2) at the end?**

::: {.reveal}
1. A − P = (4, 0), and the rotation gives **(0, 4)**, so A' = **(3, 6)**.
2. Scaling gives 1.5 × (0, 4) = (0, 6), so A'' = **(3, 8)**.
3. Check: the arm is 4 long before and **6** long after.
:::

## Try it 4 · The arm

a) Where does (5, 1) go after 90° counterclockwise about (2, 1)?
b) Where does (5, 1) go when scaled by 2 about (2, 1)?
c) Why must we subtract the pivot first?

::: {.answer}
a) (2, 4)
b) (8, 1)
c) Otherwise the arm turns about the origin and leaves its pivot.
:::

## 26.5 Problem D: asteroids and shots

:::: {.columns}
::: {.column width="50%"}
- A geometric probability is an area divided by an area.
- At least one success in n tries is 1 − (1 − p)^n^.
- The expected number of successes is n times p.
- **Do it:** Find P(on a 6 × 5 trap) on a 30 × 20 map. What is it?
:::
::: {.column width="50%"}
![](images/spawn.png)
:::
::::

## Example · The shield and the turret

Asteroids appear in a 20 × 10 rectangle, and the shield has radius 3.
**How often is an asteroid inside, and what does the turret hit?**

::: {.reveal}
1. P(inside) = π × 9 ÷ 200 ≈ **0.14**, so about 7 of 50 asteroids.
2. Three shots at p = 0.6 give P(at least one hit) = 1 − 0.4³ = **0.936**.
3. The expected number of hits is 3 × 0.6 = **1.8**.
:::

## Try it 5 · Probabilities

a) What is P(a point lies in a circle of radius 2) in a 10 × 10 square?
b) What is P(at least one hit in 2 shots) with p = 0.7?
c) How many hits do we expect in 10 shots with p = 0.7?

::: {.answer}
a) about 0.126
b) 0.91
c) 7
:::

## 26.6 Problem E: a mixed mission

:::: {.columns}
::: {.column width="50%"}
- We split a mixed problem into parts.
- Each part uses one tool and gives one result.
- We keep two or three decimals until the end.
- **Do it:** Solve two problems of each topic in Problem Drill. Which topic was hardest?
:::
::: {.column width="50%"}
![](images/five-steps.png)
:::
::::

## Live demo · Problem Drill

{{< sim file="sims/problem-drill.html" poster="sims/problem-drill.png" title="Problem Drill: Star Dock" task="**Show:** solve one vector problem with the class, then one probability problem. **Ask:** which of the five steps did you use?" >}}

## Example · The mining drone

A drone at (0, 0) faces (1, 0), and an asteroid is at (6, 8). The drone flies at 2 units per second, and p = 0.25.
**What are the time, the turn and the crystal chances?**

::: {.reveal}
1. The step (6, 8) has length 10, so the flight takes **5 s**.
2. cos θ = 0.6, so the drone turns about **53.1°** counterclockwise.
3. P(at least one crystal in 4) = 1 − 0.75⁴ ≈ **0.68**, and 20 asteroids give 5 on average.
:::

## Game challenge · Star Dock Missions

{{< sim file="sims/star-dock-missions.html" poster="sims/star-dock-missions.png" title="Star Dock Missions: one tool for each problem" kind="game" task="**The story:** the control room of Star Dock sends six missions. **Play:** find the right tool and choose the right result for each mission." >}}

## Try it 6 · Missions (harder)

a) What is the velocity of a ship from (1, 2) to (9, 8) at 5 units per second?
b) Is a thief at (3, 4) inside the 90° view of a guard at (0, 0) facing (1, 0)?
c) Why should we not round in the middle of a mixed problem?

::: {.answer}
a) (4, 3)
b) No, because 0.6 < 0.707.
c) Small errors grow in the later parts.
:::

## Summary

- We read, draw, choose the tool, compute and check.
- Motion uses the step, the unit direction and the speed.
- Seeing uses the dot product, and turning uses atan2.
- Turning about a pivot needs subtract, transform and add back.
- Probability uses area ratios, 1 − (1 − p)^n^ and n times p.
