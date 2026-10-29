---
title: "Case Study: Random Level and Event Generation"
description: "Lesson notes · A case study of a level generator for Torch Hall: seeds that repeat a level, random-walk caves, placing items by rejection sampling, flood fill to check that a level is connected, weighted event tables and shuffle bags for the rooms, and testing a generator with many seeds."
lesson: 28
ilos: [C2]
format: lesson-typst
---

::: {.lead}
*Torch Hall* gets an endless mode: every floor is new, built by a
**level generator** from random numbers. The first tests are exciting and
worrying at the same time. One tester finds a floor where the exit cannot
be reached. Another finds a bug but cannot show it again, because the next
floor is different. Some floors have three golden torches, others no chest
at all. In lectures 20–25 you learned probability, random numbers and
seeds, weighted choices, balance and fair randomness. In this case study
you **combine** them into one generator: seeds, a random-walk cave,
placing items by rules, checking the level, random events, and testing the
generator with many seeds. Every section ends with a short task.
:::

## Key terms

{{< glossary procedural-generation level-generator seed prng random-walk rejection-sampling flood-fill event-table weighted-random shuffle-bag expected-value generator-test >}}

## 28.1 Seeds: the same seed, the same level

A generator uses a pseudo-random number generator (PRNG). Its **seed**
decides every number that follows (lecture 22; @fig-seeds).

::: {.callout-important title="Definition 28.1 — Seeded generation"}
A **level generator** builds a level from a PRNG and rules. With the same
**seed** and the same code, it builds the **same level** again. Save the
seed of every level; show it in bug reports; use a new seed (for example
from the time) for a new level, or a shared seed for a "daily challenge"
that all players play.
:::

![The same seed gives the same level.](images/seeds.png){#fig-seeds width=94%}

::: {.callout-note title="Example 28.1 — The bug on floor 3"}
1. A tester finds a wall without collision on floor 3 of endless mode.
2. The game shows "seed 48213" in the pause menu; the tester writes it in
   the report.
3. The developer starts floor 3 with seed 48213 and sees the same wall.
:::

::: {.callout-caution title="In game code"}
```csharp
var rng = new System.Random(seed);       // one PRNG per level
int roomType = rng.Next(0, 4);           // the same numbers for the same seed
```
:::

::: {.callout-warning title="Common mistake"}
Using the same PRNG for the level and for things that change while
playing (particles, enemy hits). Then the level changes when the player
does something different. Use a separate PRNG for the level.
:::

::: {.callout-note title="Do it · Same seed"}
In **Cave Generator**, go to seed 43 and back to 42. Write what stays the
same. Why is that useful for a daily challenge?

*Your result:* two sentences.
:::

## 28.2 A random-walk cave

A simple way to dig a cave is a **random walk** (@fig-walk).

::: {.callout-important title="Definition 28.2 — Random walk"}
Start with a grid of walls. A walker starts in the middle; in each step it
moves one tile in a random direction (up, down, left or right, inside the
border) and makes that tile floor. More steps give a bigger cave. Because
the walker only moves to neighbours, **every floor tile is connected** to
the start.
:::

![A random walk digs a cave.](images/random-walk.png){#fig-walk width=94%}

::: {.callout-note title="Example 28.2 — Size of the cave"}
1. A 24 × 14 grid has 336 tiles.
2. With 160 steps the walker visits many tiles more than once; the cave is
   about a quarter of the grid.
3. The exit is placed on the reachable tile farthest from the start
   (found with flood fill, section 28.4).
:::

{{< sim file="sims/cave-gen.html" poster="sims/cave-gen.png" title="Cave Generator: one seed, one level" height="760" >}}

::: {.callout-warning title="Common mistake"}
Expecting 160 steps to give 160 floor tiles. The walker often steps on
tiles that are already floor; measure the fill on many seeds.
:::

::: {.callout-note title="Do it · Walk on paper"}
On a 7 × 7 grid, start in the middle. Roll a die 12 times: 1–2 right,
3 left, 4 up, 5–6 down (stay inside). Colour each tile you visit.

*Your result:* a small cave and its number of floor tiles.
:::

## 28.3 Placing items by rejection sampling

Items need rules: a chest not next to the start, a monster not on the exit
(@fig-reject).

::: {.callout-important title="Definition 28.3 — Rejection sampling"}
Draw a random candidate; if it breaks a rule, **reject** it and draw
again. If a share $p$ of all candidates is allowed, each draw succeeds
with probability $p$, and the **expected number of draws** is
$$E[\text{draws}] = \frac{1}{p}$$
(the waiting time of lecture 21). Always set a maximum number of draws.
:::

![Place the chest by drawing again.](images/rejection.png){#fig-reject width=94%}

::: {.callout-note title="Example 28.3 — The chest"}
1. Rule: the chest is on floor and at least 6 steps from the start.
2. 40 % of the tiles are allowed: $E[\text{draws}] = 1/0.4 = 2.5$.
3. If only 2 % are allowed: $1/0.02 = 50$ draws on average; the maximum of
   200 draws protects the game from an endless loop.
:::

::: {.callout-warning title="Common mistake"}
A `while` loop with no maximum. If no tile meets the rules, the game
freezes. Stop after a maximum and use a fallback (the farthest tile).
:::

::: {.callout-note title="Do it · Expected draws"}
Compute the expected number of draws for $p = 0.8$, $0.25$ and $0.05$.
Which rule would you change if $p$ is 0.05?

*Your result:* three numbers and one idea.
:::

## 28.4 Checking a level with flood fill

Not every generator connects everything. A level must be **checked**
before it is played (@fig-flood).

::: {.callout-important title="Definition 28.4 — Flood fill check"}
**Flood fill** starts at the start tile and visits every floor tile it can
reach through neighbours, keeping a queue (breadth first). It gives the
number of steps to each tile. If the exit is not reached, the level is
**invalid**: reject the seed and try the next one, or dig a tunnel. If a
share $q$ of seeds is valid, the expected number of seeds to try is
$1/q$.
:::

![Flood fill: can the player reach the exit?](images/flood-fill.png){#fig-flood width=94%}

::: {.callout-note title="Example 28.4 — Random tiles"}
1. A second method makes each tile floor with 55 % probability. Many
   floors are cut into islands.
2. Flood fill marks the reachable tiles; on some seeds the exit is pink:
   rejected.
3. If 60 % of the seeds are valid, the game needs $1/0.6 \approx 1.7$ seeds
   on average to find a good floor.
:::

::: {.callout-warning title="Common mistake"}
Checking by eye. A level that looks open can still have a wall between the
start and the exit. Let the code check every seed.
:::

::: {.callout-note title="Do it · Find a broken seed"}
In **Cave Generator**, switch to "random tiles" and find a seed whose exit
cannot be reached. Then test 100 seeds with both methods.

*Your result:* one seed and two valid shares.
:::

## 28.5 Random events: tables and bags

Each room of a floor gets an event from an **event table** (lecture 23;
@fig-events).

::: {.callout-important title="Definition 28.5 — Events per room"}
- An **event table** is a weighted random choice: probability = weight ÷
  sum of the weights.
- The **expected reward** per room is $\sum$ value × probability
  (lecture 24); per floor, multiply by the number of rooms.
- Rolling each room alone can give unlucky floors; a **shuffle bag** of
  cards (lecture 25) keeps the shares and spreads them more evenly.
:::

![An event table.](images/event-table.png){#fig-events width=94%}

::: {.callout-note title="Example 28.5 — Coins on a floor"}
1. Per room: $0.25 \cdot 20 + 0.05 \cdot 100 = 10$ coins; per floor of 8
   rooms: 80 coins.
2. $P(\text{no chest on a floor}) = 0.75^8 \approx 0.10$: one floor in ten
   has no chest.
3. $P(\text{at least one torch}) = 1 - 0.95^8 \approx 0.34$.
4. With a bag of 20 cards (5 chests, 1 torch), the average stays 80 coins,
   and floors without a chest become about half as frequent (Event Deck).
:::

{{< sim file="sims/event-deck.html" poster="sims/event-deck.png" title="Event Deck: what is in each room?" height="560" >}}

::: {.callout-warning title="Common mistake"}
Giving every event the same probability "to be fair". Fair for the game
means a planned share of rewards and dangers, set with weights.
:::

::: {.callout-note title="Do it · A floor of events"}
1. In **Event Deck**, test 1000 floors with each method and compare.
2. Compute the expected coins per floor if the chest gives 30 coins.

*Your result:* a comparison and one number.
:::

## 28.6 Testing the generator with many seeds

One good floor proves nothing. A **generator test** runs many seeds
(@fig-test).

::: {.callout-important title="Definition 28.6 — Generator test"}
Run the generator for many seeds (for example 1000) and measure: the
share of **valid** levels, the **path length** from start to exit, the
number of chests and enemies, the **coins** per floor. Look at the
average and at the extremes, as in lecture 24. Change one rule, test
again, compare.
:::

![Testing the generator with 1000 seeds.](images/generator-test.png){#fig-test width=94%}

::: {.callout-note title="Example 28.6 — Fewer steps"}
1. With 160 walk steps: 100 % valid, average path 34 tiles.
2. The designers want shorter floors and try 120 steps.
3. The test of 1000 seeds shows: average path 27 tiles, but 4 % of the
   floors have a path under 10 tiles: too easy. They add a rule: "exit at
   least 15 steps away, else next seed".
:::

::: {.callout-warning title="Common mistake"}
Testing with seed 1, 2 and 3 only. Rare problems need many seeds; a 1 %
problem appears about 10 times in 1000 seeds.
:::

::: {.callout-note title="Do it · Test plan"}
Write a test plan for the generator: three numbers to measure, the number
of seeds, and one rule you would change if a number is bad.

*Your result:* a short test plan.
:::

## Case study: Generator Doctor

The testers of *Torch Hall* report six problems: a bug that cannot be
repeated, an exit that cannot be reached, the draws needed for the chest,
the expected coins per room, floors without a chest, and a change of the
walk steps. The Game challenge of the interactive lesson uses these
reports. In the mini-game below you choose the fix or the number that
answers each report.

{{< sim file="sims/generator-doctor.html" poster="sims/generator-doctor.png" title="Generator Doctor: six reports about the generator" kind="game" height="460" >}}

## Further reading

Shaker, Togelius and Nelson, *Procedural Content Generation in Games*
(2016), Chapters 1–3 (free online). Short, "Procedural Generation in Game
Design" (2017), the chapters on dungeons and on testing generators.

## Exercises

1. Why does the same seed give the same level?
2. Why should the level have its own PRNG?
3. Describe one step of a random walk.
4. Why is a random-walk cave always connected?
5. A rule allows 25 % of the tiles. Expected draws?
6. Why does a rejection loop need a maximum?
7. What does flood fill compute?
8. 80 % of the seeds give a valid level. Expected seeds to try?
9. An event table: empty 60, chest 30 (+10 coins), torch 10 (+50 coins).
   Expected coins per room?
10. In exercise 9, expected coins for a floor of 6 rooms?
11. $P(\text{no chest in 6 rooms})$ with $p = 0.3$ per room?
12. What does a shuffle bag change for the events of a floor?
13. Name three numbers a generator test can measure.
14. A problem happens on 0.5 % of the seeds. About how often in 1000
    seeds?

## Answers to the exercises

::: {.answers}
1. The PRNG gives the same sequence of numbers for the same seed.
2. So that the actions of the player do not change the level.
3. Move one tile in a random direction (inside the border) and make it
   floor.
4. The walker only moves to neighbouring tiles.
5. $1/0.25 = 4$.
6. If no candidate meets the rules, the loop never ends.
7. Every tile that can be reached from the start, and the steps to each.
8. $1/0.8 = 1.25$.
9. $0.3 \cdot 10 + 0.1 \cdot 50 = 8$.
10. 48.
11. $0.7^6 \approx 0.118$.
12. The shares stay, but unlucky floors (no chest) become rarer.
13. For example the valid share, the path length, the chests, the coins.
14. About 5 times.
:::
