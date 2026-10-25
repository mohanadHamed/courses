---
title: "Truth Tables and Logical Conditions in Game Rules"
subtitle: "Lecture 17"
format: lesson-pptx
---

## Keywords

{{< glossary truth-table compound-proposition tautology contradiction logical-equivalence test-case implication >}}

## 17.1 Building a truth table

:::: {.columns}
::: {.column width="50%"}
- A truth table has one row for every combination of values.
- With n variables, the table has 2^n rows.
- In the first column, half the rows are T and half are F.
- **Do it:** Write the 8 rows of p, q and r in the usual order.
:::
::: {.column width="50%"}
![](images/tt-rows.png)
:::
::::

## Try it 1 · Rows

a) How many rows has a table with 3 variables?
b) How many rows has a table with 5 variables?
c) What is the first row of p, q and r in the usual order?

::: {.answer}
a) 8
b) 32
c) T, T, T
:::

## 17.2 Column by column

:::: {.columns}
::: {.column width="50%"}
- A helper column holds the value of one part of the proposition.
- We compute the columns from the inside out.
- The last column gives the value of the whole proposition.
- **Do it:** Build the table of (p ∨ q) ∧ ¬p. Does the lab agree?
:::
::: {.column width="50%"}
![](images/tt-steps.png)
:::
::::

## Example · The table of ¬(p ∧ ¬q)

We build the truth table of ¬(p ∧ ¬q) with helper columns.
**What is its last column, and which operator does it match?**

::: {.reveal}
1. The column ¬q is F, T, F, T.
2. The column p ∧ ¬q is F, T, F, F.
3. The last column is **T, F, T, T**, the same as **p → q**.
:::

## Live demo · Truth Table Lab

{{< sim file="sims/truth-table-lab.html" poster="sims/truth-table-lab.png" title="Truth Table Lab: every case of a condition" task="**Show:** make the tables of p -> q and p && (q || r), then fill one table in Quiz mode with one mistake. **Ask:** which helper column would have found the mistake?" >}}

## Try it 2 · Compute the columns

Give each last column from the row (T, T) to the row (F, F).

a) What is the column of p ∧ ¬q?
b) What is the column of ¬p ∨ q?
c) What is the column of (p ∨ q) ∧ ¬p?

::: {.answer}
a) F, T, F, F
b) T, F, T, T
c) F, F, T, F
:::

## 17.3 Always, never and the same

:::: {.columns}
::: {.column width="50%"}
- A tautology is true in every row, such as p ∨ ¬p.
- A contradiction is false in every row, such as p ∧ ¬p.
- Two propositions with the same last column are equivalent.
- **Do it:** Compare the tables of p → q and q → p. Are they the same?
:::
::: {.column width="50%"}
![](images/taut-equiv.png)
:::
::::

## Try it 3 · Always, never, same

a) What is the proposition p ∨ ¬p called?
b) What happens to a door with the rule alarm ∧ ¬alarm?
c) Are p → q and q → p equivalent?

::: {.answer}
a) a tautology
b) It never opens, because the rule is a contradiction.
c) No, they differ in the rows (T, F) and (F, T).
:::

## 17.4 A game rule as a table

:::: {.columns}
::: {.column width="50%"}
- The true rows show when a rule fires.
- The dock door p ∧ (q ∨ r) opens in 3 of 8 cases.
- Without the pass, the dock door never opens.
- **Do it:** In how many cases does the repair bay (d ∧ ¬e) ∨ o open?
:::
::: {.column width="50%"}
![](images/door-table.png)
:::
::::

## Try it 4 · Read the rule

a) In how many rows is p ∧ (q ∨ r) true?
b) In how many rows is p ∨ q ∨ r true?
c) In how many rows is (d ∧ ¬e) ∨ o true?

::: {.answer}
a) 3
b) 7
c) 5
:::

## 17.5 From a table to a condition

:::: {.columns}
::: {.column width="50%"}
- Each true row becomes an AND of the variables.
- A variable that is F in that row gets a NOT.
- The ANDs of all true rows are joined with OR.
- **Do it:** A door opens in the rows (T, T) and (F, F). Which condition is it?
:::
::: {.column width="50%"}
![](images/table-to-rule.png)
:::
::::

## Example · The two-key lock

The lock opens when exactly one of two keys is turned: the rows (T, F) and (F, T).
**Which condition does the programmer write?**

::: {.reveal}
1. The row (T, F) gives p ∧ ¬q.
2. The row (F, T) gives ¬p ∧ q.
3. The condition is **(p ∧ ¬q) ∨ (¬p ∧ q)**, which is p XOR q.
:::

## Try it 5 · Back to a condition

a) Which condition is true only in the row (T, F)?
b) Which condition is true only in the row (F, F)?
c) Which condition is true in the rows (T, T) and (F, F)?

::: {.answer}
a) p ∧ ¬q
b) ¬p ∧ ¬q
c) (p ∧ q) ∨ (¬p ∧ ¬q)
:::

## 17.6 Every row is a test case

:::: {.columns}
::: {.column width="50%"}
- Each row of the table is one test case with its expected result.
- Testing all the rows tests the rule completely.
- The false rows check that the rule does not fire by mistake.
- **Do it:** Write four test cases for the repair bay. Which rows did you pick?
:::
::: {.column width="50%"}
![](images/test-cases.png)
:::
::::

## Example · A bug found

The code of the dock door is hasPass && shieldsUp || officer.
**Which test finds the bug, and how do we fix it?**

::: {.reveal}
1. The row (F, F, T) has an officer but no pass, and the table says **shut**.
2. The game **opens** the door, because && is computed before ||.
3. The fix is **hasPass && (shieldsUp || officer)**.
:::

## Try it 6 · Testing

a) How many test cases test a rule with 3 variables completely?
b) The code opens a door that the table keeps shut. What is it?
c) Why do we also test the false rows?

::: {.answer}
a) 8
b) a bug
c) to see that the door stays shut
:::

## Game challenge · Rule Detective

{{< sim file="sims/rule-detective.html" poster="sims/rule-detective.png" title="Rule Detective: find the condition from the log" kind="game" task="**The story:** in Star Dock, the conditions of six doors are lost, and only their test logs are left. **Play:** find the condition that gives exactly each truth table." >}}

## Try it 7 · Three inputs (harder)

a) In how many of 8 rows is (p ∧ q) ∨ r true?
b) Which variable does not matter in the cargo bay rule p ∧ ¬r?
c) Which condition is true in only one row of three variables?

::: {.answer}
a) 5
b) q
c) p ∧ q ∧ r
:::

## Summary

- A truth table lists all 2^n cases of a rule.
- Helper columns compute a proposition from the inside out.
- Equivalent propositions have the same last column in every row.
- One AND for each true row, joined with OR, rebuilds a condition.
- Every row of the table is a test case for the game.
