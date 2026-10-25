---
title: "Probability Basics: Events and Sample Space"
description: "Random experiments and sample spaces, the probability of an event with equally likely outcomes, the complement, two-step experiments with grids and tree diagrams, the rules for OR and AND, and relative frequency in many trials."
lesson: 20
ilos: [A2]
format: lesson-html
---

This page is the interactive version of the lesson notes (PDF). Each section
has a short summary, a picture, a **Do it** task and one set of questions.
The full explanations, examples and exercises are in the notes.

## Key terms

{{< glossary random-experiment outcome sample-space event probability equally-likely-outcomes complement-event mutually-exclusive-events independent-events tree-diagram relative-frequency law-of-large-numbers >}}

## 20.1 Random experiments and sample spaces

- A **random experiment**: a die, a coin, a loot crate.
- An **outcome** is one result; the **sample space** S is the set of all
  outcomes.
- One die: S = {1, …, 6}. Two coins: S = {HH, HT, TH, TT}.
- List the outcomes so that each one is equally likely.

![Three experiments and their sample spaces.](images/sample-spaces.png){width=94%}

::: {.callout-warning title="Watch out!"}
HT and TH are two different outcomes.
:::

::: {.callout-note title="Do it · Sample spaces"}
Write S and |S| for three coins, a spinner with four colours, and 12 event
cards.
:::

::: {.callout-tip title="Try it 1 · Sample spaces"}
Choose |S|.

::: {.match extra="3|7"}
one die
:   6

two coins
:   4

three coins
:   8

two dice
:   36
:::
:::

## 20.2 The probability of an event

- An **event** A is a set of outcomes.
- Equally likely outcomes: **P(A) = |A| / |S|**.
- 0 = impossible, 1 = certain; fraction, decimal or %.
- The raft needs a 5 or a 6: P = 2/6 = 1/3.

![An event and the probability scale.](images/event-prob.png){width=94%}

{{< sim file="sims/sample-space-lab.html" poster="sims/sample-space-lab.png" title="Sample Space Lab: count the outcomes" height="760" >}}

::: {.callout-warning title="Watch out!"}
A probability is never more than 1.
:::

::: {.callout-note title="Do it · Count"}
One die: P(odd), P(less than 3), P(a 7). Check one in **Sample Space
Lab**.
:::

::: {.callout-tip title="Try it 2 · One die and a crate"}
Choose the probability.

::: {.match extra="6/10|2/3"}
P(an even number)
:   1/2

P(a 5 or a 6)
:   1/3

P(gold), 1 gold of 10 items
:   1/10

P(a 7)
:   0
:::
:::

## 20.3 The complement: "not A"

- **not A**: all outcomes that are not in A.
- **P(not A) = 1 − P(A)**.
- At least one 6 with two dice: no 6 = 25 cells, so P = 1 − 25/36 = 11/36.

![At least one 6, counted with the complement.](images/complement.png){width=94%}

::: {.callout-warning title="Watch out!"}
1/6 + 1/6 counts the cell (6, 6) twice.
:::

::: {.callout-note title="Do it · The complement"}
P(not a 6); P(at least one head) with two coins; P(not a storm) with 3
storms in 12 cards.
:::

::: {.callout-tip title="Try it 3 · Not A"}
Use Sample Space Lab. Choose the probability.

::: {.match extra="1/36|12/36"}
P(not a 6), one die
:   5/6

P(not wood), 6 wood of 10 items
:   4/10

P(at least one 6), two dice
:   11/36

P(at least one head), two coins
:   3/4
:::
:::

## 20.4 Two-step experiments: grids and trees

- m and k outcomes → **m × k** equally likely pairs.
- A **grid** for two dice: 36 cells. A **tree diagram**: one branch per
  outcome.
- Along a branch: **multiply**. All leaves add up to 1.
- P(sum 7) = 6/36 = 1/6.

![Two dice: the sums.](images/dice-sums.png){width=94%}

![A coin, then a spinner with three colours.](images/tree.png){width=94%}

::: {.callout-warning title="Watch out!"}
There are 11 sums, but they are not equally likely.
:::

::: {.callout-note title="Do it · Two dice"}
From the grid: P(sum 12), P(a double), P(sum more than 9).
:::

::: {.callout-tip title="Try it 4 · Two dice"}
Choose the probability.

::: {.match extra="1/11|2/36"}
P(sum 7)
:   6/36

P(sum 12)
:   1/36

P(a double)
:   1/6

P(heads and red), coin and 3-colour spinner
:   1/2 × 1/3
:::
:::

## 20.5 Combining events: OR and AND

- **OR:** P(A) + P(B) − P(A and B). Mutually exclusive: just add.
- **AND, independent:** P(A) × P(B).
- Even or more than 4: 3/6 + 2/6 − 1/6 = 4/6.
- Two storms (card put back): 1/4 × 1/4 = 1/16.

![A or B: add, then take away the overlap.](images/or-and.png){width=94%}

::: {.callout-warning title="Watch out!"}
"And" multiplies: two storms are rarer than one.
:::

::: {.callout-note title="Do it · OR and AND"}
P(less than 3 or a 6); P(odd or less than 3); P(heads and a 6).
:::

::: {.callout-tip title="Try it 5 · OR and AND"}
Choose the probability.

::: {.match extra="5/6|1/2 + 1/6"}
P(even or more than 4), one die
:   4/6

P(a 1 or a 6), one die
:   2/6

P(two storms), 3 storms in 12, put back
:   1/16

P(heads and a 6)
:   1/12
:::
:::

## 20.6 Theory and experiment

- **Relative frequency** = hits ÷ trials.
- **Law of large numbers:** with many trials it comes close to P.
- With few trials, big differences are normal.
- A far result after 1000 trials can show a bug.

![The share of 6s in 1000 rolls.](images/large-numbers.png){width=94%}

{{< sim file="sims/roll-lab.html" poster="sims/roll-lab.png" title="Roll Lab: theory and experiment" height="760" >}}

::: {.callout-warning title="Watch out!"}
No 6 in 6 rolls happens about one time in three.
:::

::: {.callout-note title="Do it · Roll"}
In **Roll Lab**, roll 10 times, then 1000 times. Write both relative
frequencies of a 6.
:::

::: {.callout-tip title="Try it 6 · Experiments"}
Use Roll Lab. Choose the right answer.

::: {.match extra="exactly 1/6 every time|always 0"}
312 bonus rolls in 1000: the relative frequency?
:   0.312

Rolls of a die: about how many 6s in 600?
:   about 100

After 10 rolls, the frequency of a 6 is 0.4. Is that strange?
:   no, few trials jump a lot

After 1000 rolls, 0.333 for at least one 6?
:   probably a bug in the code
:::
:::

## Game challenge: Raft Odds {.challenge}

Work alone. Use every section of today.

A turn of *Lucky Raft*: a **5 or a 6**, a crate item that is **not wood**,
a **sum of 7**, **at least one 6**, **even or more than 4**, and **two
storms** in a row.

{{< sim file="sims/raft-odds.html" poster="sims/raft-odds.png" title="Raft Odds: the probability before each move" kind="game" height="600" >}}

::: {.callout-tip title="Try it 7 · The turn"}
Choose the probability.

::: {.match extra="7/36|1/8"}
the raft reaches the island
:   1/3

the sea eagle comes (sum 7)
:   1/6

the bonus (at least one 6)
:   11/36

two storms in a row
:   1/16
:::
:::

::: {.callout-tip title="Try it 8 · Three dice (harder)"}
Choose the right answer.

::: {.match extra="18|1/18"}
How many outcomes have three dice?
:   216

P(three 6s)
:   1/216

P(no 6 with three dice)
:   125/216

P(at least one 6 with three dice)
:   91/216
:::
:::

## Summary {.summary}

- A random experiment has a sample space S of outcomes.
- With equally likely outcomes, P(A) = |A| / |S|, from 0 to 1.
- P(not A) = 1 − P(A): often easier to count.
- Two steps: a grid or a tree; multiply along a branch.
- OR: add and take away the overlap. AND (independent): multiply.
- Many trials bring the relative frequency close to the probability.
