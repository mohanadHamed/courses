---
title: "How Games Run on the Devices We Use"
description: "Lesson notes · From the store to the first frame, the frame on real hardware, where the game is computed, and device classes for gaming."
lesson: 2
ilos: [A1]
format: lesson-typst
---

::: {.lead}
A first-year class wants one game to run on all the devices of its students:
cheap and expensive Android phones, iPhones, laptops, a console, and a phone
that plays through a cloud gaming service. Why does the game load slowly on
one phone? Why does it feel late on another? In the previous lesson you met
the parts of a computing system. In this lesson you follow one game on real
devices: from the store to the first frame, through every frame, and across
the network. You also compare the devices that students play on. Every
section ends with a short task on your phone, on the lab computer or in a
mini-game.
:::

## Key terms

{{< glossary app-package install process loading gpu frame-rate refresh-rate resolution thermal-throttling latency cloud-gaming >}}

## 2.1 From the store to the first frame

A mobile game comes as one file, an **app package**. It holds the game's code
and its **assets**: pictures, 3D models, sounds and levels. On Android, the
package that the phone downloads is called an APK. On iPhone, it is called
an IPA.

**Installing** copies the package into the phone's storage. The game does not
run yet: it uses storage, but no memory.

When the player taps the icon, the operating system **launches** the game
(@fig-launch):

1. it creates a **process**: a running program with its own part of memory;
2. it **loads** the game's code from storage into memory (RAM);
3. the game loads the assets of the first scene;
4. the game starts, and the first frame appears.

![Launching a game: the operating system creates a process and copies code and assets from storage into memory.](images/launch.png){#fig-launch width=88%}

Why is there a loading screen? Because storage is much slower than memory.
Phone storage reads from about 100 MB per second in cheap phones to more than
1000 MB per second in expensive phones.

::: {.callout-note title="Example 2.1 — Why loading is slower on a cheap phone"}
The first level of a game needs 1500 MB of assets. Phone A reads 1500 MB per
second. Phone B reads 150 MB per second.

1. Phone A: $1500 / 1500 = 1$ second.
2. Phone B: $1500 / 150 = 10$ seconds.
3. Same game, same level: ten times slower, only because of the storage
   speed.
:::

Memory is limited too. When the player switches to another app, the game
waits in the background. If memory gets full, the operating system closes
background games to free memory. This is why a game sometimes starts again
from its title screen when the player comes back. Good games save the
player's progress when they go to the background.

::: {.callout-warning title="Common mistake"}
"A phone with more storage starts games faster." No: the *size* of storage
decides how many games fit. The *speed* of storage decides how fast they load.
The size of *memory* decides how much can stay loaded at once.
:::

::: {.callout-note title="Do it · Time a game start"}
Use a game on your phone and a stopwatch (the clock of the lab computer, a
watch, or count the seconds).

1. Close the game fully (swipe it away in the recent apps). Start it, and time
   it until the main menu appears.
2. Go to the home screen, wait ten seconds, and open the game again from the
   recent apps. Time it again.

*Your result:* the two times, and one sentence: why is the second start
faster? Use the words *storage* and *memory*.
:::

## 2.2 The frame on real hardware

Every frame needs work from two processors. The **CPU** runs the game logic:
input, rules, movement and the list of things to draw. The **GPU** (graphics
processor) draws the picture: it computes the colour of every pixel. The two
work like an assembly line: while the GPU draws one frame, the CPU already
prepares the next one. So the slower of the two decides the time of each
frame (@fig-pipeline).

![The CPU and the GPU work on two frames at the same time. The slower one sets the pace.](images/cpu-gpu-pipeline.png){#fig-pipeline width=94%}

::: {.callout-important title="Definition 2.1 — Frame rate, refresh rate and resolution"}
The **frame rate** is the number of new pictures that the game makes per
second (frames per second, fps). The **refresh rate** is the number of times
per second that the screen redraws its picture (60, 90 or 120 Hz). The
**resolution** is the number of pixels: width × height. More pixels mean more
work for the GPU. The player never sees more new pictures than the slower of
the two rates allows: a game at 70 fps on a 60 Hz screen shows 60 new pictures
per second.
:::

A phone has no fan. After some minutes of heavy play, the chip gets hot. To
protect itself, the phone slows the processor down. This is called **thermal
throttling**. A game that runs at 60 fps in the first minute may drop to 40
fps after twenty minutes. So developers test games for a long time, not only
for one minute.

::: {.callout-note title="Do it · Your screen in numbers"}
On a lab computer (Windows): open Settings → System → Display.

1. Write the **display resolution** (for example 1920 × 1080).
2. Open **Advanced display** and write the **refresh rate**.
*Your result:* the resolution, the refresh rate, and the highest frame rate a
player can *see* on this screen.
:::

## 2.3 Where the game is computed

A game is not always computed only on the player's device. There are three
common ways (@fig-where):

- **local:** everything happens on the device;
- **online (client–server):** each device runs the game, and a server keeps
  the shared data of the match, such as positions and scores;
- **cloud gaming:** the game runs on a server in a data centre. The device only
  sends the player's touches and shows the video that comes back.

![Three ways to run a game: local, client–server and cloud gaming.](images/where-game-runs.png){#fig-where width=94%}

::: {.callout-important title="Definition 2.2 — Latency"}
**Latency** is the delay between an action and its result on the screen,
measured in milliseconds (ms). In games it is also called *input lag*.
:::

Cloud gaming lets a cheap phone play big games. But it needs a fast Internet
connection, and it adds latency: every touch travels to the data centre, and
every frame travels back.

::: {.callout-note title="Example 2.2 — Which games can be streamed?"}
A cloud gaming service adds about 50 ms of delay to every tap.

1. A fighting game or a rhythm game needs fast reactions: 50 ms more is easy
   to feel, and the player loses.
2. A card game or a puzzle game does not need fast reactions: the delay does
   not matter.
3. So cloud gaming suits slow games best.
:::

{{< sim file="sims/lag-lab.html" poster="sims/lag-lab.png" title="Lag Lab: play with input lag" kind="game" height="560" >}}

::: {.callout-note title="Do it · Feel the lag"}
Open the **Lag Lab** mini-game above (or scan its QR code).

1. Play 10 blocks in each mode: local, online, cloud with a good network, and
   cloud with a poor network.
2. Write the percentage of blocks you cleared in each mode.

*Your result:* the four results, and one sentence: from which mode does the
lag start to make the game hard?
:::

## 2.4 Device classes for gaming

Students play on very different devices (@fig-devices). @tbl-devices compares
them on the things that matter for a game designer.

![The five device classes on which students play.](images/devices.png){#fig-devices width=92%}

| Property | Smartphone | Tablet | PC / laptop | Console | Cloud gaming |
|---|---|---|---|---|---|
| Input | touch, sensors | touch, sensors | keyboard, mouse, gamepad | gamepad | depends on the device |
| Screen | small | medium | large | TV | any |
| Power | battery, no fan | battery, no fan | mains, fans | mains, fans | the server |
| Play time | short, anywhere | short to medium | long, at a desk | long, at home | needs a fast network |

: Device classes compared for gaming. {#tbl-devices}

A game made for one class must change for another. A touch interface does not
work with a gamepad. A long open-world game does not fit a five-minute bus
ride. A game that needs a fan cannot keep its frame rate on a phone. So the
first question in planning a game, and in testing it, is: *on which devices
will people play it?*

::: {.callout-warning title="Common mistake"}
"A fast phone can run any PC game." Even a fast phone has a small touch
screen, a battery and no fan. The game must still be changed for the phone.
:::

::: {.callout-note title="Do it · The right device for a game"}
Choose one game that you know well.

1. Write the input it needs (touch, buttons, keyboard…), the screen it needs
   (small or large) and the length of one session (minutes).
2. Choose the device class where it works best, and give one reason.

*Your result:* the three facts, the device class and the reason.
:::

## Case study: the class survey

A first-year class lists the devices it plays on. Most students use Android
phones of different prices; the cheapest phone reads its storage at 120 MB per
second. A few students use iPhones, and some use laptops. One student owns a
console. Two students play through a cloud gaming service; one of them has a
slow connection. The class wants one game that runs on all of these devices.
The Game challenge of the interactive lesson uses this survey.

## Further reading

Tanenbaum and Austin, *Structured Computer Organization*, 6th ed., Chapter 1,
the part on the "computer zoo"; Silberschatz, Galvin and Gagne, *Operating
System Concepts*, 10th ed., Chapter 3 ("Processes").

## Exercises

1. What is the difference between installing and launching a game? Use the
   words storage and memory.
2. Write the four steps between the tap on a game's icon and the first frame.
3. A level needs 900 MB of assets. How long does it load at 300 MB per second?
4. A player comes back to a game after a long video, and the game starts again
   from the title screen. Why?
5. What does the CPU do in a frame, and what does the GPU do?
6. A screen refreshes at 90 Hz, and the game makes 70 fps. How many new
   pictures does the player see per second?
7. Why must a phone game be tested for twenty minutes, not only for one?
8. Name the three ways to run a game, and say where the game runs in each.
9. Why is cloud gaming better for a card game than for a fighting game?

## Answers to the exercises

::: {.answers}
1. Installing copies the game into storage (no memory used). Launching creates a process and loads the code and assets into memory.
2. Create a process; load the code into memory; load the first scene's assets; start the game.
3. 900 / 300 = 3 seconds.
4. Memory got full, so the operating system closed the game in the background. It had to load again from storage.
5. The CPU runs the game logic (input, rules, movement); the GPU draws the picture (the colour of every pixel).
6. 70 (the game is slower than the screen).
7. The phone gets hot and slows down (thermal throttling). A one-minute test does not show this.
8. Local: on the device. Client–server: on each device, with shared data on a server. Cloud gaming: on a server in a data centre.
9. Cloud gaming adds latency. A card game does not need fast reactions; a fighting game does.
:::
