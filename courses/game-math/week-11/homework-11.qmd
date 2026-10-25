---
title: "Homework 11: The bonus wheel and the seed"
description: "Compute a conditional probability and the expected value of a bonus wheel, then run a small random number generator by hand and find a bug with a seed. About 10 minutes."
homework: 11
due: "before lecture 23"
marks: 5
ilos: [A2, B2, C2]
toc-title: "In this homework"
format: lesson-html   # the PDF is made by printing this page (homework_pdf.py)
---

**How to submit:** Write on paper and show your steps. Upload a clear photo to the university e-learning platform. Due: **before lecture 23**.

## Task 1 · The bonus wheel (3 marks)

A bonus wheel has 10 equal parts: 1 part gives 50 coins, 2 parts give 20
coins, 3 parts give 5 coins and 4 parts give 0 coins. A spin costs 10 coins.

a) Compute the expected value of one spin and the expected gain. Is the
wheel fair? (1 mark)

{{< answer-space lines=4 >}}

b) The wheel stopped on a part that gives at least 5 coins. What is the
probability that it gives 50 coins? (1 mark)

{{< answer-space lines=3 >}}

c) A player spins two times. What is the probability of 0 coins both times?
Are the two spins independent? (1 mark)

{{< answer-space lines=3 >}}

## Task 2 · A generator by hand (2 marks)

a) Compute the first 8 numbers of x(n+1) = (5·x(n) + 1) mod 8 with the
seed 3. What is the period? (1 mark)

{{< answer-space lines=3 >}}

b) A game computes a prize lane with `int lane = Random.Range(1, 3);` and the
level has lanes 1, 2 and 3. Which lane never gets a prize? Write the fix,
and say why a tester should note the seed of a level with a bug. (1 mark)

{{< answer-space lines=3 >}}
