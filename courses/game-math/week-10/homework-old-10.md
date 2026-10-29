---
title: "Homework 10: The trap room and the dice of the boss"
description: "Write the decision table and the else-if chain of a trap rule, and compute the probabilities of a dice attack. About 10 minutes."
homework: 10
due: "before lecture 21"
marks: 5
ilos: [B2, A2]
toc-title: "In this homework"
format: lesson-html   # the PDF is made by printing this page (homework_pdf.py)
---

**How to submit:** Write on paper and show your steps. Upload a clear photo to the university e-learning platform. Due: **before lecture 21**.

## Task 1 · The trap room (2 marks)

The designer writes: "The fire trap burns when the player steps on the
plate, unless the player wears the fire cloak. A player with low health
(less than 20) is pushed back instead."

Letters: p = steps on the plate, c = wears the cloak, h = health < 20.
Actions: **Push back**, **Burn**, **Nothing**.

a) Make the decision table with 8 rows and one action in each row. Read
"pushed back instead" as: when p and h, push back, with or without the
cloak. (1 mark)

{{< answer-space lines=10 >}}

b) Write the rules as an else-if chain in the right order, and give two
edge-case tests for "health < 20". (1 mark)

{{< answer-space lines=5 >}}

## Task 2 · The dice of the boss (3 marks)

The boss of a dungeon rolls two dice each turn.

a) The boss casts a fire ball with a sum of 10 or more. Find P(fire ball)
with the grid of 36 pairs. (1 mark)

{{< answer-space lines=3 >}}

b) The boss heals when it rolls a double. Find P(heal) and P(fire ball or
heal). (1 mark)

{{< answer-space lines=3 >}}

c) Find P(no fire ball in two turns in a row). Say why you may multiply.
(1 mark)

{{< answer-space lines=3 >}}
