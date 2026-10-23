---
title: "Identifying Components and Reading Specifications"
subtitle: "Lecture 4 · Seminar"
format: lesson-pptx
---

## Keywords

{{< glossary motherboard graphics-card power-supply cooling-system specifications logical-processor chipset storage-capacity >}}

## 4.1 What is inside the case?

:::: {.columns}
::: {.column width="50%"}
- The motherboard connects all the parts of the computer.
- The CPU runs the instructions, and the RAM holds the running game.
- The SSD keeps the game, and the graphics card draws the images.
- **Do it:** In Parts Finder, find each part by its job. What is your score?
:::
::: {.column width="50%"}
![](images/pc-inside.png)
:::
::::

## Live demo · Parts Finder

{{< sim file="sims/parts-finder.html" poster="sims/parts-finder.png" title="Parts Finder: find the part and its job" kind="game" task="**Show:** tap the part that the game names, then the part that does the job. **Ask:** which part keeps the game when the power is off?" >}}

## Try it 1 · Parts and jobs

a) Which part holds the game while it runs?
b) A report says "Out of memory". Which part does it point to?
c) Which part is the big metal box with the fan and many cables?

::: {.answer}
a) the RAM
b) the RAM
c) the power supply
:::

## 4.2 A computer spec sheet

:::: {.columns}
::: {.column width="50%"}
- A spec sheet lists each component with a number and a unit.
- The processor line gives the cores and the GHz.
- The memory line gives the RAM, and the storage line gives the capacity.
- **Do it:** On the lab computer, open Settings → System → About. What are the processor and the RAM?
:::
::: {.column width="50%"}
![](images/spec-laptop.png)
:::
::::

## Example · Reading Laptop L1

The sheet says: 8 cores, up to 4.4 GHz; Memory 16 GB; Storage 512 GB SSD; GPU inside the processor.
**What does each line tell us?**

::: {.reveal}
1. The CPU has **8 cores**, and its fastest core works at up to 4.4 GHz.
2. The RAM is **16 GB**, and the SSD holds **512 GB**.
3. There is no separate graphics card: the GPU is inside the CPU chip.
:::

## Try it 2 · Read the laptop

The facts: Laptop L1 has 8 cores at up to 4.4 GHz, 16 GB of memory and a 512 GB SSD.

a) How much RAM does Laptop L1 have?
b) What is the storage capacity of Laptop L1?
c) Where does Windows show the number of logical processors?

::: {.answer}
a) 16 GB
b) 512 GB
c) Task Manager → Performance → CPU
:::

## 4.3 A phone spec sheet

:::: {.columns}
::: {.column width="50%"}
- On a phone sheet, the processor line is called Chipset or Chip.
- Apple does not print the RAM of an iPhone.
- The capacity is not the free space: check Settings → Storage.
- **Do it:** Open Settings → About phone (or General → About). What are the RAM and the storage?
:::
::: {.column width="50%"}
![](images/spec-phones.png)
:::
::::

## Example · Two test phones

P1 has 8 GB of RAM and 256 GB of storage with 40 GB free. P2 does not show its RAM and has 128 GB with 3 GB free.
**On which phone does a 5 GB update fit?**

::: {.reveal}
1. P1 has 40 GB free, so the update **fits**.
2. P2 has only 3 GB free, so it does **not fit**.
3. The 128 GB of P2 is its capacity, not its free space.
:::

## Try it 3 · Two test phones

The facts: P1 has 8 GB of RAM and 40 GB free. P2 does not show its RAM and has 3 GB free.

a) How much RAM does P1 have?
b) Why is the RAM of P2 not on its sheet?
c) Which line of a phone sheet holds the CPU cores?

::: {.answer}
a) 8 GB
b) Apple does not print it.
c) the Chipset (or Chip) line
:::

## Game challenge · The Byte Bay test lab

{{< sim file="sims/test-lab.html" poster="sims/test-lab.png" title="Test Lab: read the spec sheets" kind="game" task="**The story:** the testers of a small studio send requests to their test lab of three devices. **Play:** read the spec sheets and send each request to the right device." >}}

## Try it 4 · Send the request (harder)

The facts: Laptop L1 has 16 GB of RAM and 120 GB free. Phone P1 has 8 GB of RAM, 40 GB free and Android 14. Phone P2 does not show its RAM and has 3 GB free.

a) Which device has the most RAM?
b) How much more free space does P2 need for a 5 GB game?
c) Which device can take a 50 GB test build?

::: {.answer}
a) Laptop L1
b) 2 GB
c) Laptop L1
:::

## Summary

- The motherboard connects the CPU, the RAM, the storage and the other parts.
- Each part has one job, such as running, holding, keeping or drawing.
- A spec sheet lists each component with a number and a unit.
- RAM and storage both use GB, so read the name of the line.
- A phone sheet says Chipset, and its capacity is not the free space.
