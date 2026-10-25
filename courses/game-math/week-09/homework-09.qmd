---
title: "Homework 9: The vault of the space station"
description: "Build the truth table of a vault rule, find a bug with it, and simplify the rule with Boolean algebra. About 10 minutes."
homework: 9
due: "before lecture 19"
marks: 5
ilos: [A2, B2]
toc-title: "In this homework"
format: lesson-html   # the PDF is made by printing this page (homework_pdf.py)
---

**How to submit:** Write on paper and show your steps. Upload a clear photo to the university e-learning platform. Due: **before lecture 19**.

The vault of a space station opens with this rule:

- p: "the player has the code card"
- q: "the player is a captain"
- r: "the station is in alarm mode"

**Rule:** the vault opens when (p ∨ q) ∧ ¬r.

## Task 1 · The truth table (3 marks)

a) Build the truth table of (p ∨ q) ∧ ¬r with all 8 rows and helper
columns. (1 mark)

{{< answer-space lines=10 >}}

b) In how many cases does the vault open? Does it ever open in alarm mode?
(1 mark)

{{< answer-space lines=2 >}}

c) The programmer wrote `if (hasCard || isCaptain && !alarm)`. Find one
row where this code and the rule give different results. (1 mark)

{{< answer-space lines=3 >}}

## Task 2 · Boolean algebra (2 marks)

a) The vault stays shut when ¬((p ∨ q) ∧ ¬r). Use De Morgan's laws to write
this without a NOT in front of brackets. (1 mark)

{{< answer-space lines=3 >}}

b) Simplify (p ∧ ¬r) ∨ (q ∧ ¬r), and name the law you use. (1 mark)

{{< answer-space lines=2 >}}
