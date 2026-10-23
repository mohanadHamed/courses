---
title: "Identifying Components and Reading Specifications"
description: "The parts inside a computer and what each one does, and how to read the specification sheet of a computer and of a phone."
lesson: 4
ilos: [A1]
format: lesson-html
---

This page is the interactive version of the lesson notes (PDF). Each section
starts with a problem in a game studio. Then it explains the part of the
device behind it. It ends with a **Do it** task (in a simulator, on the lab
computer or on your phone) and one set of questions. The full explanations,
examples and exercises are in the notes.

## Key terms

{{< glossary hardware motherboard cpu memory storage ssd graphics-card power-supply cooling-system specifications logical-processor chipset storage-capacity >}}

## 4.1 What is inside the case?

- Most parts sit on the **motherboard**. It connects all the parts.
- **CPU**: a square chip under a metal block and a fan. It runs the
  instructions.
- **RAM**: long, thin cards next to the CPU. It holds the game while it
  runs.
- **SSD**: a small card or a flat box. It keeps the game when the power is
  off.
- **Graphics card**: a big card with fans. It draws the images (it holds the
  GPU).
- **Power supply**: a metal box with cables. **Cooling system**: fans and
  metal blocks.
- A laptop has the same parts, smaller. Its GPU is often inside the CPU, and
  it has a battery.

![The parts inside a desktop computer.](images/pc-inside.png){width=90%}

::: {.callout-warning title="Watch out!"}
The big box with the fan and the cables is the **power supply**, not the
processor. The CPU is a small chip under its own cooler.
:::

{{< sim file="sims/parts-finder.html" poster="sims/parts-finder.png" title="Parts Finder: find the part and its job" kind="game" height="640" >}}

::: {.callout-note title="Do it · Parts Finder"}
In **Parts Finder**, play round 1 (find the part by its name) and round 2
(find the part by its job). Write your score and a table with six rows:
part and job.
:::

::: {.callout-tip title="Try it 1 · Parts and jobs"}
Choose the right part.

::: {.match extra="the keyboard|the display"}
It holds the game while it runs.
:   the RAM

It keeps the saves when the power is off.
:   the SSD

It connects the CPU, the memory and the storage.
:   the motherboard

The report says "Out of memory". Which part does it point to?
:   the RAM

The fans are very loud, and the game gets slow after 10 minutes. Which part cannot keep up?
:   the cooling system
:::
:::

## 4.2 Reading the specification sheet of a computer

- A **specification sheet** lists the technical values of a device, line by
  line.
- **Processor**: cores and GHz (8 cores, up to 4.4 GHz).
- **Memory**: the RAM in GB (16 GB).
- **Storage**: the **capacity** in GB or TB (512 GB SSD).
- **Graphics**: a separate graphics card, or a GPU inside the processor.
- Windows: **Settings → System → About** (processor, RAM) and **Task Manager →
  Performance** (cores, **logical processors**, memory, disk).

![The spec sheet of Laptop L1.](images/spec-laptop.png){width=86%}

::: {.callout-warning title="Watch out!"}
RAM and storage both use GB. "16 GB" next to **Memory** is RAM; "512 GB" next
to **Storage** is the SSD.
:::

::: {.callout-note title="Do it · The spec sheet of the lab computer"}
On a lab computer, open **Settings → System → About**: write the processor
and the installed RAM. Then open **Task Manager → Performance**: write the
cores and logical processors (**CPU**) and the type and capacity of
**Disk 0**. Make a spec sheet with four lines.
:::

::: {.callout-tip title="Try it 2 · Read the laptop"}
Laptop L1: *Processor: 8 cores (4 performance + 4 efficiency), up to 4.4 GHz ·
Memory: 16 GB · Storage: 512 GB SSD · Graphics: GPU inside the processor*.
Choose the right answer.

::: {.match extra="4 GB|4 cores|1024 GB"}
How many cores does it have?
:   8

How much RAM does it have?
:   16 GB

What is the storage capacity?
:   512 GB

Does it have a separate graphics card?
:   no, the GPU is inside the processor

Where does Windows show the logical processors?
:   Task Manager → Performance → CPU
:::
:::

## 4.3 Reading the specification sheet of a phone

- The processor line is often called **Chipset** or **Chip**: one chip with
  the CPU cores, the GPU and more.
- **RAM** and **Storage** are in GB. Apple does not print the RAM of an
  iPhone.
- **OS**: the operating system and its version (Android 14, iOS 17).
- The capacity is not the free space. The phone shows the free space in
  **Settings → Storage**.
- Phone P1: chipset 8 cores, up to 3.0 GHz; RAM 8 GB; storage 256 GB
  (40 GB free); Android 14.
- Phone P2: chip 6 cores; RAM not given; storage 128 GB (3 GB free); iOS 17.

![The spec sheets of the test phones P1 and P2.](images/spec-phones.png){width=90%}

::: {.callout-note title="Do it · The spec sheet of your phone"}
**Android:** Settings → About phone (model, Android version, RAM if shown),
then Settings → Storage (capacity and free space). **iPhone:** Settings →
General → About (model name, capacity, available, iOS version). Make a spec
sheet of your phone with four lines.
:::

::: {.callout-tip title="Try it 3 · Two test phones"}
Use the sheets of P1 and P2 above. Choose the right answer.

::: {.match extra="P2, because it has 128 GB|4 GB"}
How much RAM does P1 have?
:   8 GB

A 5 GB update must be installed. On which phone does it fit?
:   P1, it has 40 GB free

Why is the RAM of P2 not on its sheet?
:   Apple does not print it

P2 has 128 GB of storage. How much of it is free?
:   3 GB

Which line of a phone sheet holds the CPU cores?
:   Chipset (or Chip)
:::
:::

## Game challenge: the Byte Bay test lab {.challenge}

Work alone. Use every section of today.

*Byte Bay* is a made-up game studio. Its test lab has three devices:

- **Laptop L1:** 8 cores (4 performance + 4 efficiency), up to 4.4 GHz; RAM
  16 GB; storage 512 GB SSD (120 GB free); GPU inside the processor;
  Windows 11.
- **Phone P1:** 8 cores, up to 3.0 GHz; RAM 8 GB; storage 256 GB (40 GB free);
  Android 14.
- **Phone P2:** 6 cores (2 performance + 4 efficiency); RAM not given;
  storage 128 GB (3 GB free); iOS 17.

{{< sim file="sims/test-lab.html" poster="sims/test-lab.png" title="Test Lab: read the spec sheets" kind="game" height="640" >}}

::: {.callout-tip title="Try it 4 · Send the request"}
Byte Bay: L1 (16 GB RAM, 120 GB free, Windows 11), P1 (8 GB RAM, 40 GB free,
Android 14), P2 (RAM not given, 3 GB free, iOS 17). Choose the device. You
can use an answer more than once.

::: {.match}
Which device has the most RAM?
:   Laptop L1

A tester needs an Android phone. Which one?
:   Phone P1

Which device has the least free storage?
:   Phone P2

A 50 GB test build must be copied. Which device has room for it?
:   Laptop L1
:::
:::

::: {.callout-tip title="Try it 5 · Read between the lines (harder)"}
Byte Bay: L1 (8 cores, up to 4.4 GHz, 16 GB RAM, 512 GB SSD, 120 GB free,
GPU inside the processor), P1 (8 cores, up to 3.0 GHz, 8 GB RAM, 256 GB,
40 GB free), P2 (6 cores, RAM not given, 128 GB, 3 GB free). Choose the right
answer.

::: {.match extra="the power supply|1.4 GHz|128 GB"}
L1 and P1 both have 8 cores. Which one has the faster core?
:   L1, up to 4.4 GHz

P2 shows "128 GB". Why can a 5 GB game still not be installed?
:   only 3 GB is free

L1 has no graphics card. Which part draws its images?
:   the GPU inside the processor

How much more free space does P2 need for a 5 GB game?
:   2 GB

A tester opens a desktop and sees long, thin cards next to the CPU. What are they?
:   the RAM
:::
:::

## Summary {.summary}

- The motherboard connects the CPU, the RAM, the storage and the other parts.
- Each part has one job: run, hold, keep, draw, power or cool.
- A spec sheet lists each component with a number and a unit.
- RAM and storage both use GB: read the name of the line.
- Phones say "Chipset"; the capacity is not the free space.
