---
title: "Probability Basics: Events and Sample Space"
description: "Lesson notes · Random experiments and sample spaces, the probability of an event with equally likely outcomes, the complement, two-step experiments with grids and tree diagrams, the rules for OR and AND, and relative frequency in many trials."
lesson: 20
ilos: [A2]
format: lesson-typst
---

::: {.lead}
*Lucky Raft* is a board game for two to four players. Each turn, a player
rolls dice to move the raft between islands, opens loot crates, and draws
event cards: sunshine or storm. The designer wants the game to feel
exciting but fair: how often should a player reach the island in one turn?
How rare is the gold item? To answer, we need **probability**: a number
from 0 to 1 that says how likely something is. In this lesson you describe
a random experiment with its **sample space**, compute the probability of
an **event** by counting, use the **complement**, count two-step
experiments with grids and trees, combine events with OR and AND, and
compare the theory with many rolls in a simulator. Every section ends with
a short task.
:::

## Key terms

{{< glossary random-experiment outcome sample-space event probability equally-likely-outcomes complement-event mutually-exclusive-events independent-events tree-diagram relative-frequency law-of-large-numbers >}}

## 20.1 Random experiments and sample spaces

A game uses chance whenever the result of an action is not known in
advance (@fig-spaces).

::: {.callout-important title="Definition 20.1 — Experiment, outcome, sample space"}
A **random experiment** is an action whose result we cannot know in
advance. Each possible result is an **outcome**. The set of all outcomes is
the **sample space** S, and |S| is the number of outcomes in it.
:::

![Three experiments and their sample spaces.](images/sample-spaces.png){#fig-spaces width=94%}

::: {.callout-note title="Example 20.1 — The experiments of Lucky Raft"}
1. Roll one die: S = {1, 2, 3, 4, 5, 6}, |S| = 6.
2. Flip two coins: S = {HH, HT, TH, TT}, |S| = 4. HT and TH are different
   outcomes: the first coin is heads in one, tails in the other.
3. Open a crate with 10 items (1 gold, 3 silver, 6 wood): |S| = 10, one
   outcome for each item.
:::

::: {.callout-warning title="Common mistake"}
Writing S = {two heads, one head, no head} for two coins. These three
results are not equally likely: "one head" happens in two ways, HT and TH.
List the outcomes so that each one is equally likely.
:::

::: {.callout-note title="Do it · Sample spaces"}
Write the sample space and |S|: (a) flip three coins; (b) spin a spinner
with the colours red, blue, green and yellow; (c) draw one card from 12
event cards.

*Your result:* three sample spaces.
:::

## 20.2 The probability of an event

An **event** is a question about the result, such as "the raft reaches the
island" (@fig-prob).

::: {.callout-important title="Definition 20.2 — Event and probability"}
An **event** A is a set of outcomes, a part of S. When all outcomes are
**equally likely**,
$$P(A) = \frac{|A|}{|S|} = \frac{\text{number of outcomes in } A}{\text{number of outcomes in } S}.$$
Always 0 ≤ P(A) ≤ 1: P = 0 is **impossible**, P = 1 is **certain**. A
probability can be written as a fraction, a decimal or a percentage.
:::

![An event and the probability scale.](images/event-prob.png){#fig-prob width=94%}

::: {.callout-note title="Example 20.2 — Reaching the island"}
The raft reaches the island with a 5 or a 6.

1. A = {5, 6}, |A| = 2, |S| = 6.
2. P(A) = 2/6 = 1/3 ≈ 0.33 ≈ 33 %.
3. So about one turn in three reaches the island.
:::

::: {.callout-note title="Example 20.3 — The gold item"}
A crate has 1 gold, 3 silver and 6 wood items. P(gold) = 1/10 = 10 %,
P(silver) = 3/10, P(wood) = 6/10. Together: 1/10 + 3/10 + 6/10 = 1, because
some item always comes out.
:::

{{< sim file="sims/sample-space-lab.html" poster="sims/sample-space-lab.png" title="Sample Space Lab: count the outcomes" height="760" >}}

::: {.callout-warning title="Common mistake"}
A probability greater than 1, such as 7/6. Check that the event is part of
S and that you divide by |S|.
:::

::: {.callout-note title="Do it · Count"}
One die. Find P(an odd number), P(less than 3) and P(a 7). Check one of
them in **Sample Space Lab**.

*Your result:* three probabilities.
:::

## 20.3 The complement: "not A"

Sometimes it is easier to count the outcomes that are **not** in the event
(@fig-comp).

::: {.callout-important title="Definition 20.3 — Complement"}
The **complement** of A, written "not A" (or A′), has all outcomes of S
that are not in A. Since A and not A together fill S,
$$P(\text{not } A) = 1 - P(A).$$
:::

![At least one 6 with two dice, counted with the complement.](images/complement.png){#fig-comp width=94%}

::: {.callout-note title="Example 20.4 — Not wood"}
P(not wood) = 1 − P(wood) = 1 − 6/10 = 4/10. Check: the gold and the silver
items, 1 + 3 = 4 of 10.
:::

::: {.callout-note title="Example 20.5 — At least one 6"}
Two dice: a 6 on either die gives a bonus.

1. A = "at least one 6" is hard to count. Not A = "no 6 at all".
2. No 6: 5 choices for the first die, 5 for the second: 25 of 36.
3. P(A) = 1 − 25/36 = **11/36** ≈ 0.31.
:::

::: {.callout-warning title="Common mistake"}
1/6 + 1/6 = 12/36 for "at least one 6". The outcome (6, 6) is then counted
twice. The complement avoids the problem.
:::

::: {.callout-note title="Do it · The complement"}
Use the complement: (a) P(not a 6) with one die; (b) P(at least one head)
with two coins; (c) P(not a storm) when 3 of 12 cards are storms.

*Your result:* three probabilities.
:::

## 20.4 Two-step experiments: grids and trees

When an experiment has two steps, we list the pairs of outcomes in a
**grid** or a **tree diagram** (@fig-sums, @fig-tree).

::: {.callout-important title="Definition 20.4 — Grids and tree diagrams"}
For two steps with m and k equally likely outcomes, there are **m × k**
equally likely pairs. A **grid** shows them as a table; a **tree diagram**
shows one branch for each outcome of each step. Along a branch, the
probabilities are **multiplied**.
:::

![Two dice: 36 cells and the number of ways to make each sum.](images/dice-sums.png){#fig-sums width=94%}

::: {.callout-note title="Example 20.6 — The sum 7"}
In *Lucky Raft*, a sum of 7 calls the sea eagle.

1. Two dice: 6 × 6 = 36 equally likely pairs.
2. Sum 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1): 6 pairs.
3. P(sum 7) = 6/36 = 1/6. The sums 2 and 12 have only 1/36 each.
:::

![A coin, then a spinner with three equal colours.](images/tree.png){#fig-tree width=94%}

::: {.callout-note title="Example 20.7 — A coin and a spinner"}
A player flips a coin, then spins a spinner with three equal colours.

1. 2 × 3 = 6 leaves: H-red, H-blue, H-green, T-red, T-blue, T-green.
2. P(H and red) = 1/2 × 1/3 = 1/6.
3. The six leaves add up to 6 × 1/6 = 1.
:::

::: {.callout-warning title="Common mistake"}
Saying P(sum 7) = 1/11 because there are 11 sums (2 to 12). The sums are not
equally likely; the 36 pairs are.
:::

::: {.callout-note title="Do it · Two dice"}
Use the grid of @fig-sums: P(sum 12), P(a double) and P(sum more than 9).

*Your result:* three probabilities.
:::

## 20.5 Combining events: OR and AND

Game rules often combine events: "a 6 **or** an even number", "a storm
**and** another storm" (@fig-or).

::: {.callout-important title="Definition 20.5 — The rules for OR and AND"}
- **OR (addition rule):** P(A or B) = P(A) + P(B) − P(A and B). When A and
  B are **mutually exclusive** (no common outcome), P(A or B) = P(A) + P(B).
- **AND for independent events:** A and B are **independent** when one does
  not change the chance of the other; then P(A and B) = P(A) × P(B).
:::

![A or B: add, then take away the overlap.](images/or-and.png){#fig-or width=94%}

::: {.callout-note title="Example 20.8 — Even or more than 4"}
One die. A = even = {2, 4, 6}, B = more than 4 = {5, 6}.

1. A and B = {6}: one common outcome.
2. P(A or B) = 3/6 + 2/6 − 1/6 = 4/6. Check: {2, 4, 5, 6}.
3. A = {1} and B = {6} are mutually exclusive: P = 1/6 + 1/6 = 2/6.
:::

::: {.callout-note title="Example 20.9 — Two storms in a row"}
12 event cards, 3 storms. A player draws a card, puts it back, shuffles
and draws again.

1. The two draws are independent: the first card is back in the deck.
2. P(storm) = 3/12 = 1/4 each time.
3. P(storm and storm) = 1/4 × 1/4 = 1/16.
:::

::: {.callout-caution title="In game code"}
```csharp
int a = Random.Range(1, 7);   // first die, 1..6
int b = Random.Range(1, 7);   // second die, independent of the first
bool bonus = (a == 6) || (b == 6);   // P = 11/36
bool eagle = (a + b == 7);           // P = 6/36
```
:::

::: {.callout-warning title="Common mistake"}
Adding the probabilities when both events must happen: 1/4 + 1/4 = 1/2 for
two storms. "And" needs multiplication; two storms are rarer than one.
:::

::: {.callout-note title="Do it · OR and AND"}
(a) One die: P(less than 3 or a 6). (b) One die: P(odd or less than 3).
(c) A coin and a die: P(heads and a 6).

*Your result:* three probabilities.
:::

## 20.6 Theory and experiment

Counting gives the probability in theory. A game test, or a simulator,
gives the **relative frequency** (@fig-lln).

::: {.callout-important title="Definition 20.6 — Relative frequency"}
After n trials in which the event happened k times, the **relative
frequency** is k/n. By the **law of large numbers**, the relative frequency
comes closer to the probability as n grows. With few trials it can be far
away.
:::

![The share of 6s in 1000 rolls.](images/large-numbers.png){#fig-lln width=94%}

::: {.callout-note title="Example 20.10 — Testing the bonus"}
The designer rolls two dice 1000 times in a script and counts 312 bonus
rolls (at least one 6).

1. Relative frequency: 312/1000 = 0.312.
2. Theory: 11/36 ≈ 0.306. The values are close.
3. A result such as 0.333 would point to a mistake: the 1/6 + 1/6 bug in the
   code.
:::

{{< sim file="sims/roll-lab.html" poster="sims/roll-lab.png" title="Roll Lab: theory and experiment" height="760" >}}

::: {.callout-warning title="Common mistake"}
"I rolled a die 6 times and never got a 6, so the die is broken." With so
few trials this happens often: P(no 6 in 6 rolls) = (5/6)⁶ ≈ 0.33.
:::

::: {.callout-note title="Do it · Roll"}
1. In **Roll Lab**, roll 10 times and write the relative frequency of a 6.
2. Roll to 1000. Write the new value and its difference from 1/6.

*Your result:* two relative frequencies.
:::

## Case study: Raft Odds

A turn of *Lucky Raft*: the raft needs a 5 or a 6; a crate gives an item
that is not wood; the sea eagle comes with a sum of 7; a bonus comes with
at least one 6; a move rule says "even or more than 4"; and two storm cards
can come in a row. The Game challenge of the interactive lesson uses this
turn. In the mini-game below you find each probability before the move.

{{< sim file="sims/raft-odds.html" poster="sims/raft-odds.png" title="Raft Odds: the probability before each move" kind="game" height="600" >}}

## Further reading

Rosen, *Discrete Mathematics and Its Applications*, 8th ed., Sections 7.1
and 7.2 (discrete probability). Schell, *The Art of Game Design*, 3rd ed.,
Chapter 12 (chance in game mechanics).

## Exercises

1. Write the sample space of flipping one coin and rolling one die. What
   is |S|?
2. Why are "two heads, one head, no head" not good outcomes for two coins?
3. One die: P(more than 2)?
4. A crate has 2 gold and 8 wood items. P(gold)?
5. What is the probability of an impossible event? Of a certain one?
6. P(A) = 0.35. What is P(not A)?
7. Two coins: P(at least one tail), with the complement.
8. How many outcomes have three dice?
9. Two dice: P(sum 4)?
10. Two dice: P(a double)?
11. One die: P(even or a 3)? Are the events mutually exclusive?
12. One die: P(even or more than 3)?
13. Two coins: P(heads and heads), with the AND rule.
14. A spinner has 4 equal colours. Spin twice: P(red both times)?
15. A die is rolled 600 times. About how many 6s do you expect?
16. A designer counts 250 sums of 7 in 1000 rolls of two dice. Is the code
    probably right? Explain.

## Answers to the exercises

::: {.answers}
1. {H1, H2, …, H6, T1, …, T6}; |S| = 12.
2. They are not equally likely: one head happens in two ways.
3. 4/6 = 2/3.
4. 2/10 = 1/5.
5. 0; 1.
6. 0.65.
7. 1 − 1/4 = 3/4.
8. 6 × 6 × 6 = 216.
9. 3/36 = 1/12.
10. 6/36 = 1/6.
11. 3/6 + 1/6 = 4/6; yes, they have no common outcome.
12. 3/6 + 3/6 − 2/6 = 4/6 (the outcomes 2, 4, 5, 6).
13. 1/2 × 1/2 = 1/4.
14. 1/4 × 1/4 = 1/16.
15. About 100.
16. Probably not: 250/1000 = 0.25, far from 1/6 ≈ 0.167 with so many rolls.
:::
