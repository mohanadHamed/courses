---
title: "Case Study: Random Level and Event Generation"
subtitle: "Lecture 28"
format: lesson-pptx
---

## Keywords

{{< glossary level-generator seed random-walk rejection-sampling flood-fill event-table shuffle-bag generator-test >}}

## 28.1 Seeds

:::: {.columns}
::: {.column width="50%"}
- The same seed and the same code give the same level.
- We save the seed and show it in bug reports.
- The level gets its own PRNG.
- **Do it:** Go to seed 43 and back to 42 in Cave Generator. What stays the same?
:::
::: {.column width="50%"}
![](images/seeds.png)
:::
::::

## Example · The bug on floor 3

A tester finds a wall without collision on floor 3 of endless mode.
**How can the developer see it too?**

::: {.reveal}
1. The pause menu shows the seed **48213**.
2. The tester writes the seed in the **bug report**.
3. The developer starts floor 3 with that seed and sees **the same wall**.
:::

## 28.2 A random-walk cave

:::: {.columns}
::: {.column width="50%"}
- A walker moves one random step at a time and digs floor.
- More steps give a bigger cave.
- The cave is always connected.
- **Do it:** Dig a cave on paper with 12 die rolls. How many tiles are floor?
:::
::: {.column width="50%"}
![](images/random-walk.png)
:::
::::

## Live demo · Cave Generator

{{< sim file="sims/cave-gen.html" poster="sims/cave-gen.png" title="Cave Generator: one seed, one level" task="**Show:** seeds 42, 43 and 42 again, then random tiles and a test of 100 seeds. **Ask:** why are all walk caves valid, but not all tile caves?" >}}

## Try it 1 · Seeds and walks

a) What does a tester need to repeat a floor?
b) Why is a random-walk cave always connected?
c) Why do 160 steps not give 160 floor tiles?

::: {.answer}
a) the seed of the floor
b) The walker only moves to neighbours.
c) The walker steps on many tiles twice.
:::

## 28.3 Rejection sampling

:::: {.columns}
::: {.column width="50%"}
- We draw a random place and check the rules.
- A place that breaks a rule is drawn again.
- The expected number of draws is 1/p.
- **Do it:** Compute the expected draws for p = 0.25. How many are they?
:::
::: {.column width="50%"}
![](images/rejection.png)
:::
::::

## Example · The chest

The chest must be at least 6 steps from the start, and 40 % of the tiles are allowed.
**How many draws does the generator need?**

::: {.reveal}
1. Each draw succeeds with **p = 0.4**.
2. On average it needs 1 ÷ 0.4 = **2.5** draws.
3. A maximum of **200** draws stops an endless loop.
:::

## Try it 2 · Draws

a) How many draws are expected for p = 0.8?
b) How many draws are expected for p = 0.05?
c) Why does a rejection loop need a maximum?

::: {.answer}
a) 1.25
b) 20
c) If no place fits, the loop never ends.
:::

## 28.4 Flood fill

:::: {.columns}
::: {.column width="50%"}
- Flood fill visits every tile reachable from the start.
- An exit that is not reached makes the level invalid.
- With a valid share q we try 1/q seeds on average.
- **Do it:** Find a random-tiles seed with an unreachable exit. Which seed is it?
:::
::: {.column width="50%"}
![](images/flood-fill.png)
:::
::::

## Example · Random tiles

Each tile is floor with 55 % probability.
**What does the generator do with the islands?**

::: {.reveal}
1. Flood fill marks the reachable tiles from the start.
2. On some seeds the exit is **not reached**, so the seed is rejected.
3. With 60 % valid seeds, the game tries about **1.7** seeds per floor.
:::

## 28.5 Events

:::: {.columns}
::: {.column width="50%"}
- An event table gives each event a weight.
- The expected coins per floor are the coins per room times the rooms.
- A shuffle bag spreads the events more evenly.
- **Do it:** Test 1000 floors with each method in Event Deck. Which has fewer floors without a chest?
:::
::: {.column width="50%"}
![](images/event-table.png)
:::
::::

## Live demo · Event Deck

{{< sim file="sims/event-deck.html" poster="sims/event-deck.png" title="Event Deck: what is in each room?" task="**Show:** two floors rolled room by room, then 1000 floors with each method. **Ask:** why is the average the same but the unlucky floors fewer?" >}}

## Example · Coins on a floor

A room gives a chest with 25 % (20 coins) or a torch with 5 % (100 coins).
**What does a floor of 8 rooms give?**

::: {.reveal}
1. Each room gives 0.25 × 20 + 0.05 × 100 = **10** coins on average.
2. A floor gives **80** coins on average.
3. P(no chest) = 0.75⁸ ≈ **10 %**, so one floor in ten has none.
:::

## Try it 3 · Events

a) What are the expected coins for a floor of 8 rooms?
b) What is P(at least one torch in 8 rooms) with p = 0.05?
c) What does a shuffle bag keep the same?

::: {.answer}
a) 80
b) about 34 %
c) the shares of the events
:::

## 28.6 Testing the generator

:::: {.columns}
::: {.column width="50%"}
- We run the generator with 1000 seeds or more.
- We measure the valid share, the paths and the rewards.
- We change one rule and test again.
- **Do it:** Write a test plan with three numbers to measure. Which number matters most?
:::
::: {.column width="50%"}
![](images/generator-test.png)
:::
::::

## Example · Fewer steps

The designers try 120 walk steps instead of 160 for shorter floors.
**What does a test of 1000 seeds show?**

::: {.reveal}
1. The average path falls from 34 to **27** tiles.
2. But **4 %** of the floors have a path under 10 tiles.
3. A new rule asks for an exit at least **15 steps** away.
:::

## Game challenge · Generator Doctor

{{< sim file="sims/generator-doctor.html" poster="sims/generator-doctor.png" title="Generator Doctor: six reports about the generator" kind="game" task="**The story:** the testers of Torch Hall report six problems with the generator. **Play:** choose the fix or the number for each report." >}}

## Try it 4 · Compute (harder)

a) What are the coins per room for chest 30 % (+10) and torch 10 % (+50)?
b) What is P(no chest in 6 rooms) with p = 0.3?
c) How often does a 0.5 % problem appear in 1000 seeds?

::: {.answer}
a) 8
b) about 0.118
c) about 5 times
:::

## Summary

- A seed repeats a level, so the level gets its own PRNG.
- A random walk digs a connected cave.
- Rejection sampling needs 1/p draws on average.
- Flood fill rejects levels with an unreachable exit.
- Event tables and shuffle bags plan the rewards.
- Many seeds test the generator.
