---
title: "Random Numbers: Pseudo-Random Generators and Seeds"
description: "Why games need random numbers, pseudo-random numbers from a formula, a linear congruential generator by hand with modulo and its period, seeds for repeatable levels and daily challenges, turning random numbers into game values, and common bugs."
lesson: 22
ilos: [C2]
format: lesson-html
---

This page is the interactive version of the lesson notes (PDF). Each section
has a short summary, a picture, a **Do it** task and one set of questions.
The full explanations, examples and exercises are in the notes.

## Key terms

{{< glossary pseudo-random-number prng lcg modulo generator-period seed procedural-generation random-experiment >}}

## 22.1 Why games need random numbers

- Chance gives levels, loot, behaviour and critical hits.
- A computer makes **pseudo-random numbers** with a formula (a **PRNG**).
- They look random; the same start gives the same numbers.

![Real chance and pseudo-random numbers.](images/pseudo-random.png){width=94%}

::: {.callout-warning title="Watch out!"}
Good PRNGs are right for games; passwords and payments need secure ones.
:::

::: {.callout-note title="Do it · Find the chance"}
Write four things in a game you play that come from random numbers.
:::

::: {.callout-tip title="Try it 1 · Real or pseudo?"}
Choose the right answer.

::: {.match extra="a picture|the frame rate"}
a physical die
:   real chance

x = (5x + 3) mod 16
:   pseudo-random

the same start gives the same numbers
:   pseudo-random

the walls of each new cave
:   procedural generation
:::
:::

## 22.2 A generator by hand: the LCG

- **x(n+1) = (a·x(n) + c) mod m**; mod = the remainder.
- Values 0 … m − 1; the first value is the **seed**.
- The sequence repeats: the **period** is at most m.
- a = 5, c = 3, m = 16, seed 7: 7, 6, 1, 8, 11, … period 16.

![An LCG by hand.](images/lcg-steps.png){width=94%}

{{< sim file="sims/lcg-lab.html" poster="sims/lcg-lab.png" title="LCG Lab: x(n+1) = (a · x(n) + c) mod m" height="620" >}}

::: {.callout-warning title="Watch out!"}
c = 4 instead of 3 gives 7, 7, 7, …: the period is 1.
:::

::: {.callout-note title="Do it · By hand"}
a = 3, c = 1, m = 8, seed 2: compute 8 numbers and the period. Check in
**LCG Lab**.
:::

::: {.callout-tip title="Try it 2 · The LCG"}
Use LCG Lab. Choose the right answer.

::: {.match extra="16 mod 5|a"}
38 mod 16
:   6

after 7 with a = 5, c = 3, m = 16
:   6

the period with a = 5, c = 3, m = 16
:   16

the period with c = 4 and seed 7
:   1
:::
:::

## 22.3 Seeds

- **Same seed → same sequence → same level.**
- Seed from the **time**: a new game. From a **shared number**: the same
  world for friends.
- From the **date**: a daily challenge. **Saved**: exact replays and bugs
  you can repeat.

![The same seed gives the same level.](images/seeds.png){width=94%}

{{< sim file="sims/seed-lab.html" poster="sims/seed-lab.png" title="Seed Lab: the same seed, the same level" height="680" >}}

::: {.callout-warning title="Watch out!"}
Seeding from the time gives friends different worlds.
:::

::: {.callout-note title="Do it · Seeds"}
In **Seed Lab**, build seed 42 twice, then 43, then the daily challenge.
Write what stays the same.
:::

::: {.callout-tip title="Try it 3 · Seeds"}
Use Seed Lab. Choose the seed.

::: {.match extra="the player's name|a bigger font"}
a new cave every game
:   the time

the same cave for all players today
:   the date

the same world for two friends
:   a number they share

an exact replay
:   the saved seed
:::
:::

## 22.4 From random numbers to game values

- Integer: **Random.Range(min, max)** gives min … max − 1.
- Yes with probability p: **Random.value < p**.
- Between a and b: **a + r·(b − a)**.

![From a random number to a die.](images/range-map.png){width=94%}

::: {.callout-warning title="Watch out!"}
Random.Range(1, 6) never gives a 6.
:::

::: {.callout-note title="Do it · Write the call"}
Write calls for a card 0 … 51, a lane 1, 2 or 3, and a miss with p = 0.15.
:::

::: {.callout-tip title="Try it 4 · Calls"}
Choose the call.

::: {.match extra="Random.Range(1, 6)|Random.value > 1"}
a die 1 … 6
:   Random.Range(1, 7)

a card 0 … 51
:   Random.Range(0, 52)

a lane 1, 2 or 3
:   Random.Range(1, 4)

a critical hit with p = 0.2
:   Random.value < 0.2f
:::
:::

## 22.5 Common bugs with random numbers

- **Seed once**, then keep using the same generator.
- **Mind the range**: the integer max is excluded.
- **Use a good generator**; test with many counts.

![Three bugs and their fixes.](images/rng-bugs.png){width=94%}

::: {.callout-warning title="Watch out!"}
InitState(time) in Update(): every bat gets the same number.
:::

::: {.callout-note title="Do it · Find the bug"}
`Random.Range(0, items.Length - 1)`: which item never drops? Write the fix.
:::

::: {.callout-tip title="Try it 5 · Bugs"}
Choose the cause.

::: {.match extra="the graphics card|too many coins"}
all bats fly the same way
:   a new seed every frame

nobody rolls a 6
:   the max is excluded

the caves repeat after 16 levels
:   a short period

the last item never drops
:   Range(0, Length − 1)
:::
:::

## Game challenge: Seed Detective {.challenge}

Work alone. Use every section of today.

Six tester reports: **no 6** in the dice room, **bats** that fly the same
way, different **daily caves**, a wrong **replay**, caves that **repeat**,
and no coins in **lane 3**.

{{< sim file="sims/seed-detective.html" poster="sims/seed-detective.png" title="Seed Detective: fix the randomness" kind="game" height="520" >}}

::: {.callout-tip title="Try it 6 · The fixes"}
Choose the fix.

::: {.match extra="restart the computer|a faster CPU"}
no 6 in the dice room
:   Random.Range(1, 7)

all bats fly the same way
:   seed once at the start

friends get different daily caves
:   seed with today's date

the replay looks different
:   save the seed with the inputs
:::
:::

::: {.callout-tip title="Try it 7 · Compute (harder)"}
Choose the right answer.

::: {.match extra="20|9"}
(5·12 + 3) mod 16
:   15

23 mod 5
:   3

a = 3, c = 1, m = 8, seed 2: the period
:   4

a = 1, c = 0, m = 10, seed 4: the period
:   1
:::
:::

::: {.callout-tip title="Try it 8 · Seeds in design (harder)"}
Choose the right answer.

::: {.match extra="a new seed every frame|no seed at all"}
A tester finds a bug in a cave. What does the tester send?
:   the seed of the cave

Two friends want the same world.
:   they type the same seed

A speedrun must be fair for all players.
:   one fixed seed for everybody

A new surprise every time the game starts.
:   a seed from the time
:::
:::

## Summary {.summary}

- Games use pseudo-random numbers from a formula.
- An LCG: x(n+1) = (a·x(n) + c) mod m; its period is at most m.
- The same seed gives the same sequence: daily challenges, shared worlds,
  replays.
- Random.Range(min, max) with integers excludes the max.
- Seed once, mind the range, use a good generator.
