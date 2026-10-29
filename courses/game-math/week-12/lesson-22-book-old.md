---
title: "Random Numbers: Pseudo-Random Generators and Seeds"
description: "Lesson notes · Why games need random numbers, pseudo-random numbers from a formula, a linear congruential generator by hand with modulo and its period, seeds for repeatable levels and daily challenges, turning random numbers into game values, and common bugs."
lesson: 22
ilos: [C2]
format: lesson-typst
---

::: {.lead}
Every cave of *Torch Hall* is different: the walls, the coins and the bats
come from random numbers. But the testers report strange things: nobody
ever rolls a 6 in the dice room, all five bats fly the same way, and the
"daily challenge" is different for two friends on the same day. A computer
cannot roll a real die: it **computes** numbers that only look random. In
lectures 20 and 21 you computed probabilities. In this lesson you look
inside the machine: how a **pseudo-random generator** works, what a
**seed** is, how random numbers become dice, lanes and loot, and how to
avoid the common bugs. Every section ends with a short task.
:::

## Key terms

{{< glossary pseudo-random-number prng lcg modulo generator-period seed procedural-generation random-experiment >}}

## 22.1 Why games need random numbers

Chance makes games surprising and replayable: different levels, loot,
enemy behaviour and critical hits (@fig-pseudo).

::: {.callout-important title="Definition 22.1 — Pseudo-random numbers"}
**Real chance** comes from the physical world: a die, noise, the exact time
between key presses. A computer usually makes **pseudo-random numbers**
with a fixed formula, a **pseudo-random number generator (PRNG)**: each
number is computed from the one before. They look random and pass
statistical tests, but the same start always gives the same numbers.
:::

![Real chance and pseudo-random numbers.](images/pseudo-random.png){#fig-pseudo width=94%}

::: {.callout-note title="Example 22.1 — Chance in Torch Hall"}
1. **Procedural generation:** the walls and coins of each cave.
2. **Loot:** the item in each chest (the crates of lecture 21).
3. **Behaviour:** the direction in which a bat flies next.
4. **Combat:** a critical hit with probability 0.2.
:::

::: {.callout-warning title="Common mistake"}
Thinking that pseudo-random means "not random enough for games". For
games, a good PRNG is ideal: fast, and repeatable when you need it. (For
passwords and online money, special secure generators are used.)
:::

::: {.callout-note title="Do it · Find the chance"}
Choose a game you play. Write four things in it that come from random
numbers.

*Your result:* a list of four.
:::

## 22.2 A generator by hand: the LCG

One of the oldest generators fits in one line (@fig-lcg).

::: {.callout-important title="Definition 22.2 — Linear congruential generator"}
An **LCG** computes
$$x_{n+1} = (a \cdot x_n + c) \bmod m.$$
**mod** (modulo) is the remainder of a division: 38 mod 16 = 6. All values
are between 0 and m − 1. The first value x₀ is the **seed**. Because there
are only m values, the sequence repeats; the number of values before the
repeat is the **period**, at most m.
:::

![An LCG by hand with a = 5, c = 3, m = 16 and seed 7.](images/lcg-steps.png){#fig-lcg width=94%}

::: {.callout-note title="Example 22.2 — Seed 7"}
a = 5, c = 3, m = 16, x₀ = 7:

1. x₁ = (5·7 + 3) mod 16 = 38 mod 16 = **6**.
2. x₂ = (5·6 + 3) mod 16 = 33 mod 16 = **1**; x₃ = 8 mod 16 = **8**.
3. The sequence 7, 6, 1, 8, 11, 10, 5, 12, 15, 14, 9, 0, 3, 2, 13, 4 uses
   all 16 values; then 7 comes again. The period is **16**, the full
   period.
:::

::: {.callout-note title="Example 22.3 — A bad choice"}
With c = 4 instead of 3: x₁ = (35 + 4) mod 16 = 39 mod 16 = 7. The
generator gives 7, 7, 7, … for ever: the period is 1. The numbers a, c and m
must be chosen with care.
:::

{{< sim file="sims/lcg-lab.html" poster="sims/lcg-lab.png" title="LCG Lab: x(n+1) = (a · x(n) + c) mod m" height="620" >}}

::: {.callout-warning title="Common mistake"}
Writing your own generator "for fun" in a real game. Small m gives short
periods and patterns. Use the generator of the engine or of the language.
:::

::: {.callout-note title="Do it · By hand"}
With a = 3, c = 1, m = 8 and seed 2, compute 8 numbers. What is the period?
Check it in **LCG Lab**.

*Your result:* eight numbers and a period.
:::

## 22.3 Seeds: the same start, the same numbers

The seed is the key to repeatable randomness (@fig-seeds).

::: {.callout-important title="Definition 22.3 — Seed"}
The **seed** is the start value of a PRNG. The **same seed gives the same
sequence**, and so the same level, loot and events. A game chooses the
seed:

- from the **time** or the system: a new game every time;
- from a **number** the player types or shares: the same world for friends;
- from the **date**: a daily challenge, the same for all players today;
- **saved** with the inputs: an exact replay, and bugs that can be repeated.
:::

![The same seed gives the same level.](images/seeds.png){#fig-seeds width=94%}

::: {.callout-note title="Example 22.4 — The daily cave"}
1. The seed is the date as a number: 25 October 2026 → **20261025**.
2. Every player who opens the daily cave today builds it with this seed:
   the same walls, coins and bats for all.
3. Tomorrow the seed is 20261026: a new cave for everybody.
:::

{{< sim file="sims/seed-lab.html" poster="sims/seed-lab.png" title="Seed Lab: the same seed, the same level" height="680" >}}

::: {.callout-caution title="In game code"}
```csharp
// Unity: one generator for the level, seeded once.
var rng = new System.Random(seed);          // seed = 20261025 for the daily cave
for (int i = 0; i < cells.Length; i++)
    cells[i] = rng.NextDouble() < 0.22 ? Cell.Wall : Cell.Floor;
```
:::

::: {.callout-warning title="Common mistake"}
Seeding from the time when players should share a world. Two friends start a
second apart and get different caves. Use a shared number or the date.
:::

::: {.callout-note title="Do it · Seeds"}
In **Seed Lab**, build seed 42 twice, then 43. Then press Daily challenge.
Write what stays the same and what changes.

*Your result:* three short notes.
:::

## 22.4 From random numbers to game values

A PRNG gives numbers in a fixed range. The game needs dice, lanes, items
and yes/no decisions (@fig-range).

::: {.callout-important title="Definition 22.4 — Scaling random numbers"}
From a number r with 0 ≤ r < 1:

- an integer from **min** to **max − 1**: floor(r · (max − min)) + min;
- yes with probability p: **r < p**;
- a value between a and b: a + r · (b − a).

In Unity, **Random.Range(min, max)** with integers gives min … max − 1 (the
max is **not** included); with floats, the max can be included.
**Random.value** gives a float from 0 to 1.
:::

![From a random number to a die.](images/range-map.png){#fig-range width=94%}

::: {.callout-note title="Example 22.5 — Dice, lanes and critical hits"}
1. A die: `Random.Range(1, 7)` → 1 … 6.
2. Three lanes numbered 0, 1, 2: `Random.Range(0, 3)`.
3. A critical hit with p = 0.2: `if (Random.value < 0.2f) Crit();`.
4. A coin bonus between 5 and 15 (float): `5 + Random.value * 10`.
:::

::: {.callout-warning title="Common mistake"}
`Random.Range(1, 6)` for a die: the 6 never comes, because the max of the
integer version is not included.
:::

::: {.callout-note title="Do it · Write the call"}
Write the call for: (a) a card from 52 cards (0 … 51); (b) a lane 1, 2 or 3;
(c) a miss with probability 0.15.

*Your result:* three lines of code.
:::

## 22.5 Common bugs with random numbers

Most "strange randomness" in games comes from a few bugs (@fig-bugs).

::: {.callout-important title="Definition 22.5 — Three rules"}
1. **Seed once:** make one generator at the start and keep using it.
   Seeding again and again (for example every frame with the time) gives the
   same numbers many times.
2. **Mind the range:** for integers the max is excluded.
3. **Use a good generator** with a long period; test the results with
   counts (lecture 20).
:::

![Three bugs and their fixes.](images/rng-bugs.png){#fig-bugs width=94%}

::: {.callout-note title="Example 22.6 — The five bats"}
The code calls `Random.InitState((int)Time.time)` in `Update()` of every
bat.

1. In one frame, `Time.time` is the same for all bats: every bat gets the
   same seed.
2. The same seed gives the same first number: all bats choose the same
   direction.
3. Fix: seed once when the level starts; each bat just asks the generator
   for its next number.
:::

::: {.callout-warning title="Common mistake"}
Testing the drop chance with 10 tries and calling it a bug. Count 1000 or
more tries before you decide (the law of large numbers, lecture 20).
:::

::: {.callout-note title="Do it · Find the bug"}
The code is `int item = Random.Range(0, items.Length - 1);`. Which item can
never drop? Write the fix.

*Your result:* the item and one line of code.
:::

## Case study: Seed Detective

The testers of *Torch Hall* report six problems: nobody rolls a 6 in the dice
room; all bats fly the same way; two friends get different daily caves; the
replay of a best run looks different; the caves repeat after 16 levels; and
coins never appear in lane 3. The Game challenge of the interactive lesson
uses these reports. In the mini-game below you choose the fix for each
one.

{{< sim file="sims/seed-detective.html" poster="sims/seed-detective.png" title="Seed Detective: fix the randomness" kind="game" height="520" >}}

## Further reading

Knuth, *The Art of Computer Programming*, Vol. 2, 3rd ed., Chapter 3
(random numbers, the LCG). Unity Manual, "Random" and "Random.Range"
(docs.unity3d.com). Shaker, Togelius and Nelson, *Procedural Content
Generation in Games* (2016), Chapter 1.

## Exercises

1. What is the difference between real chance and pseudo-random numbers?
2. Compute 23 mod 5 and 40 mod 8.
3. With a = 5, c = 3, m = 16, what follows x = 12?
4. What is the largest possible period of an LCG with m = 16?
5. With a = 1, c = 0, m = 10 and seed 4, what is the sequence?
6. What does the seed decide?
7. Why does a daily challenge use the date as the seed?
8. What must a replay save, besides the inputs?
9. Which numbers does Random.Range(0, 10) give?
10. Write a call for a die with 8 faces (1 … 8).
11. How do you make a yes with probability 0.3 from Random.value?
12. Why should the generator be seeded only once?
13. A level generator with seed 99 gives a bug. How do you show it to a
    teammate?
14. Name one use of real (secure) random numbers that games do not do with a
    PRNG.

## Answers to the exercises

::: {.answers}
1. Real chance cannot be repeated; pseudo-random numbers come from a formula
   and the same seed repeats them.
2. 3; 0.
3. (5·12 + 3) mod 16 = 63 mod 16 = 15.
4. 16.
5. 4, 4, 4, … (period 1).
6. Where the sequence starts, and so all the numbers that follow.
7. All players get the same level today, and a new one tomorrow.
8. The seed.
9. 0 … 9.
10. Random.Range(1, 9).
11. Random.value < 0.3f.
12. Seeding again, for example with the same time, repeats the same numbers.
13. Send the seed: the teammate builds the same level.
14. For example passwords, keys or online payments.
:::
