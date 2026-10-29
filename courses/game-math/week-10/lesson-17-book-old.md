---
title: "Truth Tables and Logical Conditions in Game Rules"
description: "Lesson notes · Building a truth table with 2^n rows, computing a compound proposition column by column, tautologies, contradictions and equivalent propositions, game rules as truth tables, going from a table back to a condition, and using the rows as test cases."
lesson: 17
ilos: [A2, B2]
format: lesson-typst
---

::: {.lead}
In the space game *Star Dock*, the dock door opens when a ship has the pass,
and its shields are up or an officer is on board. Is that the rule the
designer wanted? Will the door ever open by mistake? With three conditions
there are eight possible situations, and a bug can hide in any of them. A
**truth table** lists every situation and the value of the rule in each one.
In lecture 16 you met the logical operators. In this lesson you build truth
tables, read game rules from them, find equivalent rules, write a condition
from a table, and use every row as a test. Every section ends with a short
task.
:::

## Key terms

{{< glossary truth-table compound-proposition truth-value tautology contradiction logical-equivalence test-case conjunction disjunction implication >}}

## 17.1 Building a truth table

A game rule with two conditions has four possible situations: both true,
only the first, only the second, none. A truth table writes all of them
down, in a fixed order (@fig-rows).

::: {.callout-important title="Definition 17.1 — Truth table"}
A **truth table** has one column for each variable and one row for each
combination of truth values. With **n** variables there are $2^n$ rows: 2
variables give 4 rows, 3 give 8, 4 give 16. The usual order: in the first
column half the rows are T, half F; in each next column T and F change
twice as often.
:::

![Truth tables with 2 and 3 variables.](images/tt-rows.png){#fig-rows width=94%}

::: {.callout-note title="Example 17.1 — Two conditions of a door"}
p: "the ship has the pass", q: "the shields are up".

1. 2 variables: $2^2 = 4$ rows.
2. Rows: (T, T), (T, F), (F, T), (F, F).
3. With a third variable r ("an officer is on board"), each row splits in
   two: $2^3 = 8$ rows.
:::

::: {.callout-warning title="Common mistake"}
Writing the rows in a random order. It is easy to miss a case or write one
twice. Follow the halving pattern, and count: 2, 4, 8 or 16 rows.
:::

::: {.callout-note title="Do it · How many cases?"}
1. How many rows does a truth table with 4 variables have? And with 5?
2. Write the 8 rows of p, q, r in the usual order.

*Your result:* two numbers and an 8-row table.
:::

## 17.2 A compound proposition, column by column

For a longer proposition, add one column for each part, from the inside out
(@fig-steps). The last column is the value of the whole proposition.

::: {.callout-important title="Definition 17.2 — Helper columns"}
To build the truth table of a compound proposition, add a **helper
column** for each operator, in the order of computing (brackets, NOT, AND,
OR, IF–THEN). Each helper column uses only the columns before it.
:::

![¬(p ∧ ¬q), one column at a time.](images/tt-steps.png){#fig-steps width=94%}

::: {.callout-note title="Example 17.2 — The table of ¬(p ∧ ¬q)"}
1. Column ¬q: F, T, F, T.
2. Column p ∧ ¬q: only the row p = T, q = F gives T.
3. Column ¬(p ∧ ¬q): T, F, T, T. It is false only when p = T and q = F —
   the same as p → q.
:::

{{< sim file="sims/truth-table-lab.html" poster="sims/truth-table-lab.png" title="Truth Table Lab: every case of a condition" height="700" >}}

::: {.callout-warning title="Common mistake"}
Computing the NOT of a whole bracket as the NOT of each part: ¬(p ∧ q) is
not ¬p ∧ ¬q. Compute the bracket first, then turn the whole column round
(lecture 18 gives the right law).
:::

::: {.callout-note title="Do it · Predict, then check"}
1. On paper, build the table of (p ∨ q) ∧ ¬p with helper columns.
2. In **Truth Table Lab**, switch to Quiz mode, type the same condition and
   enter your answers. Press Check.

*Your result:* a table and your check.
:::

## 17.3 Tautologies, contradictions and equivalence

Some propositions have the same value in every row. And two different
propositions can have the same table (@fig-te).

::: {.callout-important title="Definition 17.3 — Tautology, contradiction, equivalence"}
A **tautology** is true in every row (p ∨ ¬p). A **contradiction** is false
in every row (p ∧ ¬p). Two propositions are **equivalent** (≡) when their
last columns are the same in every row; then one can replace the other.
:::

![A tautology, a contradiction, and two equivalent propositions.](images/taut-equiv.png){#fig-te width=94%}

::: {.callout-note title="Example 17.3 — A door that never opens"}
A designer writes: "open when the alarm is on and the alarm is off":
alarm ∧ ¬alarm. Its column is F, F: a contradiction. The door never opens.
The truth table finds this bug before any player does.
:::

::: {.callout-note title="Example 17.4 — Two ways to write a rule"}
"If the ship is docked, the engine is off" is docked → ¬engine. The table
gives F only for docked = T, engine = T. So it is equivalent to
¬docked ∨ ¬engine, and also to ¬(docked ∧ engine).
:::

::: {.callout-warning title="Common mistake"}
Calling two propositions equivalent because they agree in some rows. They
must agree in **every** row.
:::

::: {.callout-note title="Do it · Same or not?"}
Build the tables of p → q and q → p. Are they equivalent? Which row shows
it?

*Your result:* two columns and one row.
:::

## 17.4 A game rule as a truth table

A truth table shows a designer exactly when a rule fires. Here is the dock
door of Star Dock with three conditions (@fig-door).

::: {.callout-important title="Definition 17.4 — Reading a rule from its table"}
The **true rows** of a rule are the situations in which it fires (the door
opens, the trap triggers). Reading them answers two questions: does it fire
in every case it should, and in no case it should not?
:::

![The dock door p ∧ (q ∨ r): it opens in 3 of 8 cases.](images/door-table.png){#fig-door width=94%}

::: {.callout-note title="Example 17.5 — Checking the dock door"}
p: pass, q: shields up, r: officer on board. Rule: p ∧ (q ∨ r).

1. True rows: (T, T, T), (T, T, F), (T, F, T): 3 of 8.
2. Without the pass the door never opens: rows 5–8 are all F. Good.
3. With the pass but neither shields nor officer, it stays shut: row 4. The
   designer agrees: no bug.
:::

::: {.callout-warning title="Common mistake"}
Checking only the "normal" case (everything true). Bugs hide in unusual
rows, such as the pass without shields.
:::

::: {.callout-note title="Do it · The repair bay"}
The repair bay opens when the ship is docked (d) and the engine is off (¬e),
or when an officer is on board (o): (d ∧ ¬e) ∨ o. Build its 8-row table. In
how many cases does it open?

*Your result:* a table and a number.
:::

## 17.5 From a truth table back to a condition

Sometimes the designer gives a table ("open in these cases"), and the
programmer must write the condition (@fig-back).

::: {.callout-important title="Definition 17.5 — One AND per true row"}
For each **true row**, write an AND of the variables, with ¬ in front of
each variable that is F in that row. Join these ANDs with OR. The result has
the same table (then simplify it, lecture 18).
:::

![Two true rows give (p ∧ ¬q) ∨ (¬p ∧ q).](images/table-to-rule.png){#fig-back width=94%}

::: {.callout-note title="Example 17.6 — The two-key lock"}
The lock opens when exactly one of two keys is turned: rows (T, F) and
(F, T).

1. Row (T, F): p ∧ ¬q. Row (F, T): ¬p ∧ q.
2. Condition: (p ∧ ¬q) ∨ (¬p ∧ q).
3. This is p XOR q: in C#, `p ^ q`.
:::

::: {.callout-warning title="Common mistake"}
Forgetting the ¬ of the false variables: "p ∧ q" for the row (T, F) is
wrong; that is the row (T, T).
:::

::: {.callout-note title="Do it · Write the condition"}
A door opens only in the rows (T, T) and (F, F) of p, q. Write the
condition with one AND per row. What does the door check in words?

*Your result:* one condition and one sentence.
:::

## 17.6 Every row is a test case

A truth table is also a test plan: each row is a situation a tester sets
up in the game, with the result the table predicts (@fig-tests).

::: {.callout-important title="Definition 17.6 — Test cases from a truth table"}
A **test case** is one set of inputs with the expected result. Each row of
the truth table of a rule gives one test case. Testing all rows tests the
rule completely; with many variables, test at least each true row and the
false rows next to them (one variable changed).
:::

![Test cases from the table of the dock door.](images/test-cases.png){#fig-tests width=94%}

::: {.callout-note title="Example 17.7 — A bug found"}
The code of the dock door is `if (hasPass && shieldsUp || officer)`.

1. Test row 7 of the table: no pass, no shields, officer (F, F, T). The
   table says **shut**.
2. The game opens the door: && is computed first, so `… || officer` is
   true.
3. Fix: `if (hasPass && (shieldsUp || officer))`. The row passes now.
:::

::: {.callout-warning title="Common mistake"}
Testing only the true rows. The false rows check that the door does **not**
open when it should not.
:::

::: {.callout-note title="Do it · A test plan"}
Write four test cases (inputs and expected result) for the repair bay of
17.4: two true rows and two false rows.

*Your result:* four test cases.
:::

## Case study: Rule Detective

*Star Dock* is a made-up space game. Its designer lost the conditions of
six doors, but the test logs are left: one truth table per door. Door A
opens only with the pass and the shields up; door B is false in one row
only; door C is true exactly when p and q differ; door D is false only for
p = T, q = F; door E has three inputs; and in the cargo bay, q does not
matter. The Game challenge of the interactive lesson uses these logs. In
the mini-game below you find each condition.

{{< sim file="sims/rule-detective.html" poster="sims/rule-detective.png" title="Rule Detective: find the condition from the log" kind="game" height="760" >}}

## Further reading

Rosen, *Discrete Mathematics and Its Applications*, 8th ed., Sections 1.1
(truth tables) and 1.3 (propositional equivalences).

## Exercises

1. How many rows has the truth table of a proposition with 4 variables?
2. Build the truth table of p ∧ ¬q.
3. Build the truth table of ¬p ∨ q.
4. Build the truth table of (p ∨ q) ∧ ¬(p ∧ q). Which operator is it?
5. Is p → (q → p) a tautology? Show the table.
6. Is p ∧ ¬p ∧ q a contradiction?
7. Are p → q and ¬q → ¬p equivalent? Show the tables.
8. Are p → q and q → p equivalent?
9. The dock door is p ∧ (q ∨ r). In which rows is it true?
10. A trap fires in the rows (T, F) and (F, F) of p, q. Write its
    condition and simplify it in words.
11. Write the condition with one AND per row for the true rows (T, T, F)
    and (F, T, T) of p, q, r.
12. How many test cases test a rule with 3 variables completely?
13. The code `if (a || b && c)` should mean "(a or b) and c". Which row
    shows the bug?
14. Why should a tester also test the false rows?

## Answers to the exercises

::: {.answers}
1. 16.
2. F, T, F, F.
3. T, F, T, T.
4. F, T, T, F: XOR.
5. Yes: all four rows are T.
6. Yes: every row is F (p ∧ ¬p is already F).
7. Yes: both are T, F, T, T.
8. No: they differ in the rows (T, F) and (F, T).
9. (T, T, T), (T, T, F), (T, F, T).
10. (p ∧ ¬q) ∨ (¬p ∧ ¬q): it fires when q is false, ¬q.
11. (p ∧ q ∧ ¬r) ∨ (¬p ∧ q ∧ r).
12. 8.
13. For example a = T, b = F, c = F: the code gives T, the rule gives F.
14. To check that the rule does not fire when it should not.
:::
