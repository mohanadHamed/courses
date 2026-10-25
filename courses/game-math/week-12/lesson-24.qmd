---
title: "Probability for Game Balance: Drop Rates and Difficulty"
description: "Drop rates and the chance of at least one drop, how many tries most players need, pity timers, the expected value of rewards, difficulty from hit chances and expected attacks, and checking a balance with simulations."
lesson: 24
ilos: [C2]
format: lesson-html
---

This page is the interactive version of the lesson notes (PDF). Each section
has a short summary, a picture, a **Do it** task and one set of questions.
The full explanations, examples and exercises are in the notes.

## Key terms

{{< glossary game-balance drop-rate pity-timer expected-value hit-chance probability-distribution complement-event >}}

## 24.1 Drop rates and "at least once"

- **P(at least one in n) = 1 − (1 − p)ⁿ.**
- p = 5 %: after 20 tries 64 %, after 45 tries 90 %.
- The average is 1/p, but some players wait much longer.

![Drop rate 5 %.](images/at-least-one.png){width=94%}

::: {.callout-warning title="Watch out!"}
5 % × 20 is not 100 %: chances of tries do not add up.
:::

::: {.callout-note title="Do it · Chances of a drop"}
p = 0.1: compute the chance after 5, 10 and 30 tries.
:::

::: {.callout-tip title="Try it 1 · At least once"}
Choose the probability.

::: {.match extra="100 %|20 %"}
p = 5 %, at least one in 20 tries
:   about 64 %

p = 5 %, none in 20 tries
:   about 36 %

p = 0.2, at least one in 3 tries
:   about 49 %

p = 0.1, at least one in 10 tries
:   about 65 %
:::
:::

## 24.2 How many tries do most players need?

- 90 % of players: **n ≥ ln 0.1 / ln(1 − p)**.
- 90 % within 20 tries: p ≈ 11 %.
- Or try values in a table or a simulator.

{{< sim file="sims/drop-rate-lab.html" poster="sims/drop-rate-lab.png" title="Drop Rate Lab: how long do players wait?" height="680" >}}

::: {.callout-warning title="Watch out!"}
Players remember the long waits, not the average.
:::

::: {.callout-note title="Do it · Find the rate"}
In **Drop Rate Lab**, find the rate for 90 % within 20 bats; check it with the
formula.
:::

::: {.callout-tip title="Try it 2 · Tries"}
Use Drop Rate Lab. Choose the right answer.

::: {.match extra="1 try|200 tries"}
p = 5 %: tries for 90 % of the players
:   45

p = 5 %: tries for 50 % of the players
:   14

the rate for 90 % within 20 tries
:   about 11 %

p = 0.1: tries for 90 % (ln 0.1 / ln 0.9)
:   22
:::
:::

## 24.3 Pity timers

- A **pity timer** guarantees the item after N misses, or raises the chance.
- The longest wait is limited; the average falls a little.

![A pity timer.](images/pity-timer.png){width=94%}

::: {.callout-warning title="Watch out!"}
Be honest about drop chances; stores ask for shown odds on paid random items.
:::

::: {.callout-note title="Do it · Pity"}
Switch on the pity timer at 40 in **Drop Rate Lab**. Longest wait? Average?
:::

::: {.callout-tip title="Try it 3 · Pity"}
Use Drop Rate Lab. Choose the right answer.

::: {.match extra="100|0"}
the longest wait with pity at 40
:   40

the average with p = 5 % and pity at 40
:   about 17

the average with p = 5 % and no pity
:   20

players still waiting after 39 misses without pity
:   about 13 %
:::
:::

## 24.4 Rewards: expected value and the economy

- **E = Σ value × weight ÷ Σ weights.**
- Compare E with the shop prices: chests needed ≈ price ÷ E.

::: {.callout-warning title="Watch out!"}
The plain average of the values overestimates the rewards.
:::

::: {.callout-note title="Do it · The economy"}
70 % 10 coins, 25 % 40 coins, 5 % 200 coins: E? Chests for a 400-coin
shield?
:::

::: {.callout-tip title="Try it 4 · Rewards"}
Choose the right answer.

::: {.match extra="28|85"}
E: 60 % 5, 30 % 20, 10 % 60
:   15

chests for a 300-coin sword at E = 15
:   20

E: 70 % 10, 25 % 40, 5 % 200
:   27

E: 80 % 10, 20 % 50
:   18
:::
:::

## 24.5 Difficulty from probability

- Hits = ⌈health ÷ damage⌉; **expected attacks = hits ÷ hit chance**.
- Compare both sides; simulate the win rate.
- Target here: a normal enemy loses 70–85 % of fights.

![Expected attacks.](images/difficulty.png){width=94%}

{{< sim file="sims/difficulty-tuner.html" poster="sims/difficulty-tuner.png" title="Difficulty Tuner: how hard is the skeleton?" height="560" >}}

::: {.callout-warning title="Watch out!"}
Change one number at a time.
:::

::: {.callout-note title="Do it · Tune an enemy"}
In **Difficulty Tuner**, make a normal skeleton (70–85 %) and a boss
(30–45 %).
:::

::: {.callout-tip title="Try it 5 · Difficulty"}
Use Difficulty Tuner. Choose the right answer.

::: {.match extra="0.7|50"}
hits for 40 health with 10 damage
:   4

expected attacks: 4 hits, hit chance 0.8
:   5

expected attacks: 3 hits, hit chance 0.75
:   4

the player's win rate against the first skeleton
:   about 88 %
:::
:::

## 24.6 Testing a balance with simulations

- Code the rule, run it 1000+ times, look at the **average and the
  extremes**.
- Change one number and run again.

::: {.callout-warning title="Watch out!"}
A few play sessions show only your own luck.
:::

::: {.callout-note title="Do it · Simulate"}
p = 3 %, with and without pity at 50: compare the average and the longest
wait.
:::

::: {.callout-tip title="Try it 6 · Simulations"}
Choose the right answer.

::: {.match extra="your own luck|a single fight"}
what a simulation shows beyond the average
:   the unlucky players

how many simulated tries
:   1000 or more

after a change of one number
:   run it again

the longest wait without pity at p = 5 %
:   often over 100
:::
:::

## Game challenge: Balance Board {.challenge}

Work alone. Use every section of today.

Six cards: a **torch in 20 bats**, a rate for **10 kills on average**,
players who **quit**, **expected attacks**, the **chest's E**, and a skeleton
that **wins too often**.

{{< sim file="sims/balance-board.html" poster="sims/balance-board.png" title="Balance Board: numbers for the update" kind="game" height="440" >}}

::: {.callout-tip title="Try it 7 · The cards"}
Choose the right answer.

::: {.match extra="100 %|1 %"}
P(at least one torch in 20 bats, p = 5 %)
:   about 64 %

the rate for 10 kills on average
:   10 %

players quit after 200 misses
:   add a pity timer

the skeleton wins too often
:   lower one number a little
:::
:::

::: {.callout-tip title="Try it 8 · Compute (harder)"}
Choose the right answer.

::: {.match extra="0.5|2"}
P(none in 10 tries), p = 0.05
:   about 0.60

hat 180 coins, E = 18: chests
:   10

1 − 0.8³
:   0.488

tries for 90 % with p = 0.1
:   22
:::
:::

## Summary {.summary}

- P(at least one in n) = 1 − (1 − p)ⁿ; the average is 1/p.
- Choose p for the share of players: n ≥ ln(1 − q) / ln(1 − p).
- Pity timers limit the longest wait.
- Rewards: compare E with prices.
- Difficulty: expected attacks = hits ÷ hit chance; simulate the win rate.
