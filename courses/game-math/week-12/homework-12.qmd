---
title: "Homework 12: The fishing pond"
description: "Build a weighted loot table for a fishing pond, compute its expected value, and choose a drop rate and a pity timer for a rare fish. About 10 minutes."
homework: 12
due: "before lecture 25"
marks: 5
ilos: [C2]
toc-title: "In this homework"
format: lesson-html   # the PDF is made by printing this page (homework_pdf.py)
---

**How to submit:** Write on paper and show your steps. Upload a clear photo to the university e-learning platform. Due: **before lecture 25**.

In a small game, a player fishes in a pond. Each cast gives one of these:

| catch | weight | coins |
|---|---|---|
| old boot | 50 | 0 |
| small fish | 35 | 4 |
| big fish | 14 | 15 |
| golden fish | 1 | 200 |

## Task 1 · The loot table (3 marks)

a) Write the probability of each catch and the cumulative weights. (1 mark)

{{< answer-space lines=4 >}}

b) Which catch does the random number r = 97.5 (from 0 to 100) give? And
r = 99.2? (1 mark)

{{< answer-space lines=2 >}}

c) Compute the expected coins per cast. How many casts does a player need on
average for a fishing rod of 300 coins? (1 mark)

{{< answer-space lines=3 >}}

## Task 2 · The golden fish (2 marks)

a) The golden fish has p = 0.01. What is the chance to catch at least one in
100 casts? (Use 0.99¹⁰⁰ ≈ 0.37.) (1 mark)

{{< answer-space lines=2 >}}

b) Players complain. Propose a pity timer (after how many casts?) and say in
one sentence what it changes for the players. (1 mark)

{{< answer-space lines=3 >}}
