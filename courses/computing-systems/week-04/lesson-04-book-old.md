---
title: "Identifying Components and Reading Specifications"
description: "Lesson notes · The parts inside a computer and what each one does, and how to read the specification sheet of a computer and of a phone."
lesson: 4
ilos: [A1]
format: lesson-typst
---

::: {.lead}
A small game studio, *Byte Bay*, sets up a test lab. It buys a new desktop
computer, a laptop and two phones. Before the testers can use them, someone
must answer simple questions. What is inside the computer? Which part do we
change if the game runs out of memory? How much space is free for the new
build? The answers are on two places: inside the case, and on the
**specification sheet** of each device. In lecture 3 you learned what the
CPU, the memory and the storage do. In this lesson you find these parts
yourself and read their numbers. Every section ends with a short task: in a
simulator, on the lab computer or on your phone.
:::

## Key terms

{{< glossary hardware motherboard cpu memory storage ssd graphics-card power-supply cooling-system specifications logical-processor chipset storage-capacity >}}

## 4.1 What is inside the case?

A tester at Byte Bay opens the side of the new desktop computer. Inside are
boards, cables, fans and small cards. Which part is the CPU? Where is the
memory? A game developer does not build computers, but must know the parts
and their jobs. Then a problem report such as "not enough memory" or "the
disk is full" points to the right part.

Most of the parts sit on one big board, the **motherboard** (@fig-case).

![The parts inside a desktop computer. Each part has one main job.](images/pc-inside.png){#fig-case width=92%}

::: {.callout-important title="Definition 4.1 — Motherboard"}
The **motherboard** is the main circuit board of a computer. It connects the
CPU, the memory, the storage and the other parts, so that they can send data
to each other.
:::

@tbl-parts gives the job of each part and what you see on the outside.

| Part | What it looks like | Its job |
|---|---|---|
| CPU (processor) | a square chip under a metal block and a fan | runs the instructions of the game |
| memory (RAM) | long, thin cards in slots next to the CPU | holds the game while it runs |
| storage (SSD) | a small card or a flat box | keeps the game and the saves when the power is off |
| graphics card | a big card with fans, near the bottom | draws the images of the game (it holds the GPU) |
| power supply | a metal box with a fan and many cables | turns wall power into the voltages the parts need |
| cooling system | fans and metal blocks with thin plates | carries heat away from the chips |

: The parts of a desktop computer and their jobs. {#tbl-parts}

A laptop has the same parts, but they are smaller and packed tightly. In
many laptops, the RAM is fixed on the motherboard, and the GPU is inside the
CPU chip. A laptop has a battery instead of a power-supply box. A phone packs
almost everything into one chip; lecture 7 looks inside it.

::: {.callout-note title="Example 4.1 — Which part does the report point to?"}
Three testers send problem reports about the new desktop computer.

1. "The game stops with the message *Out of memory*." The game needs more
   **RAM**.
2. "I cannot install the new build: *Not enough space*." The **storage** is
   full.
3. "The fans are very loud, and after 10 minutes the game gets slow." The
   **cooling system** cannot carry the heat away fast enough.
:::

::: {.callout-warning title="Common mistake"}
Thinking that the big box with the fan and the cables is the processor. That
box is the **power supply**. The CPU is a small chip, hidden under its own
cooler in the middle of the motherboard.
:::

{{< sim file="sims/parts-finder.html" poster="sims/parts-finder.png" title="Parts Finder: find the part and its job" kind="game" height="640" >}}

::: {.callout-note title="Do it · Parts Finder"}
Open the **Parts Finder** mini-game above (or scan its QR code).

1. Play round 1: tap each part that the game names.
2. Play round 2: tap the part that does the job that the game describes.

*Your result:* your score, and a table with six rows: part and job.
:::

## 4.2 Reading the specification sheet of a computer

Byte Bay must choose a laptop for its testers. The shop shows a
**specification sheet** for each model: a list of the technical values of
the device, in short lines. Each line names a component and gives a number
with a unit (@fig-laptop-sheet).

![The specification sheet of Laptop L1, with the component of each line.](images/spec-laptop.png){#fig-laptop-sheet width=90%}

::: {.callout-important title="Definition 4.2 — Specification sheet"}
A **specification sheet** (spec sheet) lists the main technical values of a
device: its processor, its memory, its storage, its graphics and its display.
Each line names a component and gives a number with a unit.
:::

Most lines use only a few units (@tbl-units).

| Line | Component | Unit | Example | What it tells you |
|---|---|---|---|---|
| Processor | CPU | cores, GHz | 8 cores, up to 4.4 GHz | how much work it can do at the same time, and how fast one core is |
| Memory | RAM | GB | 16 GB | how much the computer can hold while programs run |
| Storage | SSD or hard disk | GB, TB | 512 GB SSD | how much it can keep when it is off (its **capacity**) |
| Graphics | GPU | — | inside the processor | if there is a separate graphics card |
| Display | screen | inches, pixels | 15.6", 1920 × 1080 | the size and the sharpness of the screen |

: Common lines of a computer spec sheet. {#tbl-units}

On the lab computer, Windows shows the same values. **Settings → System →
About** shows the processor and the installed RAM. **Task Manager →
Performance** shows more. Under **CPU**, it shows the number of cores and of
**logical processors** (the threads that the CPU can run at the same time).
Under **Memory**, it shows the RAM, and under **Disk**, the storage.

::: {.callout-note title="Example 4.2 — Reading Laptop L1"}
Laptop L1 has this sheet: *Processor: 8 cores (4 performance + 4
efficiency), up to 4.4 GHz · Memory: 16 GB · Storage: 512 GB SSD · Graphics:
GPU inside the processor · Display: 15.6", 1920 × 1080*.

1. Number of cores: 8. Four are fast cores, four save energy (lecture 3).
2. The fastest core works at up to 4.4 GHz.
3. RAM: 16 GB. Storage: 512 GB on an SSD. Both use GB, but they are
   different parts.
4. There is no separate graphics card: the GPU is inside the CPU chip.
:::

::: {.callout-warning title="Common mistake"}
Mixing up RAM and storage because both use GB. "16 GB" next to "Memory" is
RAM. "512 GB" next to "Storage" is the SSD. A shop advert that says "a
laptop with 512 GB" means the storage, not the RAM.
:::

::: {.callout-note title="Do it · The spec sheet of the lab computer"}
On a lab computer (Windows):

1. Open **Settings → System → About**. Write the processor and the installed
   RAM.
2. Open **Task Manager** (Ctrl + Shift + Esc) **→ Performance**. Under **CPU**,
   write the cores and the logical processors. Under **Disk 0**, write the
   type (SSD or HDD) and the capacity.

*Your result:* a spec sheet of the lab computer with four lines: processor,
memory, storage, graphics.
:::

## 4.3 Reading the specification sheet of a phone

Byte Bay also needs two test phones. A phone spec sheet has the same main
lines, but some names are different (@fig-phone-sheets). The processor line
is often called **Chipset** or **Chip**: one chip that holds the CPU, the
GPU and more. The storage line gives the capacity, but the phone itself
shows how much of it is still free.

![The spec sheets of two test phones, P1 (Android) and P2 (iOS).](images/spec-phones.png){#fig-phone-sheets width=92%}

| Line on a phone sheet | Component | Example |
|---|---|---|
| Chipset (or Chip) | the main chip: CPU cores, GPU and more | 8 cores, up to 3.0 GHz |
| RAM | memory | 8 GB |
| Storage | flash storage | 256 GB |
| OS | operating system and its version | Android 14 |

: The main lines of a phone spec sheet. {#tbl-phone}

The display and the battery are also on the sheet. Lectures 5 and 7 explain
them.

::: {.callout-note title="Example 4.3 — Two test phones"}
Phone P1: *Chipset: 8 cores, up to 3.0 GHz · RAM: 8 GB · Storage: 256 GB
(40 GB free) · OS: Android 14*. Phone P2: *Chip: 6 cores (2 performance + 4
efficiency) · RAM: not given · Storage: 128 GB (3 GB free) · OS: iOS 17*.

1. More RAM: P1. The maker of P2 does not print the RAM; Apple does not list
   it for its iPhones.
2. A 5 GB update fits on P1 (40 GB free), but not on P2 (only 3 GB free).
3. P2 has 128 GB of capacity, but only 3 GB is free: the photos and apps of
   its owner fill the rest.
:::

::: {.callout-warning title="Common mistake"}
Reading the capacity as the free space. "Storage: 128 GB" is the size of the
whole storage. To know if a game fits, look at the free space on the phone
itself (Settings → Storage).
:::

::: {.callout-note title="Do it · The spec sheet of your phone"}
On your phone:

- **Android:** open **Settings → About phone**. Write the model, the Android
  version and (if it is shown) the RAM. Then open **Settings → Storage**:
  write the capacity and the free space. (The names can be a little different
  on some phones.)
- **iPhone:** open **Settings → General → About**. Write the model name, the
  capacity, the available space and the iOS version. The RAM is not shown.

*Your result:* a spec sheet of your phone with four lines: chipset (or model),
RAM, storage (capacity and free), OS.
:::

## Case study: the Byte Bay test lab

*Byte Bay* is a made-up game studio. Its test lab has three devices:

- **Laptop L1:** processor 8 cores (4 performance + 4 efficiency), up to
  4.4 GHz; RAM 16 GB; storage 512 GB SSD (120 GB free); GPU inside the
  processor; Windows 11.
- **Phone P1:** chipset 8 cores, up to 3.0 GHz; RAM 8 GB; storage 256 GB
  (40 GB free); Android 14.
- **Phone P2:** chip 6 cores (2 performance + 4 efficiency); RAM not given;
  storage 128 GB (3 GB free); iOS 17.

The testers send requests to the lab: "Which device has the most RAM?",
"On which phone does the 5 GB update fit?", "Which sheet does not show the
RAM?". In the mini-game below, you read the sheets and send each request to
the right device.

{{< sim file="sims/test-lab.html" poster="sims/test-lab.png" title="Test Lab: read the spec sheets" kind="game" height="640" >}}

## Further reading

Tanenbaum and Austin, *Structured Computer Organization*, 6th ed., Chapter 2
("Computer Systems Organization": processors, primary memory, secondary
memory and input/output). For your own devices: the "About" pages of
Windows, Android and iOS, and the makers' official spec sheets.

## Exercises

1. Name the part that (a) keeps the saves when the power is off; (b) holds the
   game while it runs; (c) connects all the parts.
2. A tester says: "The big box with the fan at the back is the processor."
   What is wrong?
3. "The game stops with *Out of memory*." Which part does this report point
   to?
4. Name two differences between the parts of a desktop computer and the
   parts of a laptop.
5. A sheet says *Processor: 6 cores, up to 4.0 GHz · Memory: 8 GB · Storage:
   1 TB*. How many cores? How much RAM? How much storage?
6. Where does Windows show the number of logical processors?
7. A phone sheet says *Storage: 128 GB*. A game needs 4 GB. Is it sure that
   the game fits? Why?
8. Which line of a phone sheet holds the CPU cores?
9. Byte Bay: which device has the most RAM? On which phone does a 5 GB update
   fit?

## Answers to the exercises

::: {.answers}
1. (a) storage (SSD); (b) memory (RAM); (c) the motherboard.
2. That box is the power supply. The CPU is a small chip under its own cooler, on the motherboard.
3. The memory (RAM).
4. For example: in many laptops the RAM is fixed on the motherboard; the GPU is often inside the CPU; a laptop has a battery instead of a power-supply box; the parts are smaller.
5. 6 cores; 8 GB of RAM; 1 TB of storage.
6. Task Manager → Performance → CPU.
7. No. 128 GB is the capacity. The game fits only if 4 GB or more is free (Settings → Storage).
8. The Chipset (or Chip) line.
9. Laptop L1 (16 GB). Phone P1 (40 GB free; P2 has only 3 GB free).
:::
