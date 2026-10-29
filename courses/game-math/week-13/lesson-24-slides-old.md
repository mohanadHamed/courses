---
title: "Probability for Game Balance: Drop Rates and Difficulty"
subtitle: "Lecture 24"
format: lesson-pptx
---

## Keywords

{{< glossary game-balance drop-rate pity-timer expected-value hit-chance >}}

## 24.1 Drop rates

:::: {.columns}
::: {.column width="50%"}
- A drop rate is the chance of the item in one try.
- P(at least one in n) = 1 − (1 − p)ⁿ.
- The average is 1/p, but some players wait much longer.
- **Do it:** Compute the chance after 10 tries with p = 0.1. What is it?
:::
::: {.column width="50%"}
![](images/at-least-one.png)
:::
::::

## Example · The golden torch

The golden torch drops from bats with p = 5 %.
**How many players have it after 20 and after 45 bats?**

::: {.reveal}
1. After 20 bats: 1 − 0.95²⁰ ≈ **64 %**, not 100 %.
2. After 45 bats: 1 − 0.95⁴⁵ ≈ **90 %**.
3. The average is **20 bats**, but 10 % of the players need more than 45.
:::

## Try it 1 · At least once

a) What is P(at least one in 20 tries) with p = 5 %?
b) What is P(none in 20 tries) with p = 5 %?
c) What is P(at least one in 3 tries) with p = 0.2?

::: {.answer}
a) about 64 %
b) about 36 %
c) about 49 %
:::

## 24.2 Tries for most players

:::: {.columns}
::: {.column width="50%"}
- 90 % of players need n ≥ ln 0.1 / ln(1 − p) tries.
- For 90 % within 20 tries, p must be about 11 %.
- A simulator finds the same answer by trying.
- **Do it:** Find the rate for 90 % within 20 bats. Which rate did you find?
:::
::: {.column width="50%"}
![](images/at-least-one.png)
:::
::::

## Live demo · Drop Rate Lab

{{< sim file="sims/drop-rate-lab.html" poster="sims/drop-rate-lab.png" title="Drop Rate Lab: how long do players wait?" task="**Show:** simulate 5 %, then set 11 %, then 5 % with a pity timer at 40. **Ask:** what happens to the longest wait with the pity timer?" >}}

## Try it 2 · Tries

a) How many tries do 90 % of the players need with p = 5 %?
b) How many tries do 90 % need with p = 0.1?
c) Which rate gives 90 % within 20 tries?

::: {.answer}
a) 45
b) 22
c) about 11 %
:::

## 24.3 Pity timers

:::: {.columns}
::: {.column width="50%"}
- A pity timer guarantees the item after N misses.
- It can also raise the chance after each miss.
- The longest wait is limited, and the average falls a little.
- **Do it:** Switch on pity at 40 in the lab. What is the longest wait?
:::
::: {.column width="50%"}
![](images/pity-timer.png)
:::
::::

## Example · A guarantee at 40

The torch has p = 5 %, and the team adds a guarantee at bat 40.
**What changes for the players?**

::: {.reveal}
1. Without the timer, about **13 %** still wait after 39 bats.
2. With it, **every player** has the torch at bat 40.
3. The average falls from 20 to about **17 bats**.
:::

## Try it 3 · Pity

a) What is the longest wait with a pity timer at 40?
b) What is the average with p = 5 % and no pity?
c) Why does the average fall a little with pity?

::: {.answer}
a) 40 bats
b) 20 bats
c) It cuts off the very long waits.
:::

## 24.4 Rewards and the economy

:::: {.columns}
::: {.column width="50%"}
- The expected reward is the sum of value times probability.
- Chests needed ≈ price ÷ E.
- The plain average of the values gives too much.
- **Do it:** Compute E for 70 % 10, 25 % 40 and 5 % 200 coins. What is it?
:::
::: {.column width="50%"}
![](images/difficulty.png)
:::
::::

## Example · The chest and the shop

A chest gives 5 coins (60 %), 20 coins (30 %) or 60 coins (10 %), and a sword costs 300 coins.
**How many chests does a player need?**

::: {.reveal}
1. E = 0.6·5 + 0.3·20 + 0.1·60 = **15 coins**.
2. The sword needs about 300 ÷ 15 = **20 chests**.
3. With 30 coins for rare, E = 18 and about **17 chests**.
:::

## Try it 4 · Rewards

a) What is E for 80 % 10 coins and 20 % 50 coins?
b) How many chests with E = 18 buy a hat for 180 coins?
c) What is E for 70 % 10, 25 % 40 and 5 % 200 coins?

::: {.answer}
a) 18
b) 10
c) 27
:::

## 24.5 Difficulty

:::: {.columns}
::: {.column width="50%"}
- Hits needed are health divided by damage, rounded up.
- Expected attacks are hits divided by the hit chance.
- A simulation of many fights gives the win rate.
- **Do it:** Make the skeleton a normal enemy. Which value did you change?
:::
::: {.column width="50%"}
![](images/difficulty.png)
:::
::::

## Live demo · Difficulty Tuner

{{< sim file="sims/difficulty-tuner.html" poster="sims/difficulty-tuner.png" title="Difficulty Tuner: how hard is the skeleton?" task="**Show:** simulate the first skeleton, then raise its damage to 16, then make a boss. **Ask:** why do we change only one number at a time?" >}}

## Try it 5 · Difficulty

a) How many hits does 40 health need with 10 damage?
b) How many attacks does the player expect with 4 hits and hit chance 0.8?
c) Which win rate is the target for a normal enemy here?

::: {.answer}
a) 4
b) 5
c) 70–85 % for the player
:::

## 24.6 Simulations

:::: {.columns}
::: {.column width="50%"}
- We code the rule and run it 1000 times or more.
- We look at the average and at the unlucky players.
- We change one number and run it again.
- **Do it:** Simulate p = 3 % with and without pity at 50. What changes?
:::
::: {.column width="50%"}
![](images/pity-timer.png)
:::
::::

## Game challenge · Balance Board

{{< sim file="sims/balance-board.html" poster="sims/balance-board.png" title="Balance Board: numbers for the update" kind="game" task="**The story:** before the update of Torch Hall, the balance team checks six cards. **Play:** use drop rates, expected values and hit chances to answer each card." >}}

## Try it 6 · Compute (harder)

a) What is P(none in 10 tries) with p = 0.05?
b) What is 1 − 0.8³?
c) What does a simulation show that the average does not?

::: {.answer}
a) about 0.60
b) 0.488
c) the unlucky players and the longest waits
:::

## Summary

- P(at least one in n) = 1 − (1 − p)ⁿ, and the average is 1/p.
- We choose p so that most players get the item in time.
- Pity timers limit the longest wait.
- Expected rewards are compared with the prices.
- Expected attacks and simulations set the difficulty.
