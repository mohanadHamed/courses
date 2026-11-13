# Rewrite of next week's units with the newest rules: status

Branch `claude/lucid-cannon-yooru2` in both repos (`courses` and
`courses-private`). The teacher's request (2026-11-13): the pipeline changed
at least twice in the last week (2026-11-08/09: smart screens, answers
without written English, PDFs to fill in; 2026-11-10: the picture is in the
activity that asks about it, screens of every app step, a task asks only for
what the device can do, a fix for one session is a rule for all). Rewrite
the units taught next week with the newest AUTHORING.md and `check_size.py`:

| Course | Unit | Folder | Sessions |
|---|---|---|---|
| Game Math | 4 | `courses/game-math/week-04` | Lecture 4, Seminar 4, Homework 4 |
| Computing Systems | 5 | `courses/computing-systems/week-05` | Lecture 5, Seminar 5, Homework 5 |
| Digital Media | 4 | `courses/digital-media/week-04` | Lecture 4, Seminar 4, Homework 4 |
| Digital Skills | 3 | `courses/digital-skills/week-03` | Lecture 3 (worksheet), Online activity 3 |

One commit per finished unit (and its solution in `courses-private`), pushed
at once, so a new session can continue from here.

## What each unit needs (found 2026-11-13)

All four units were last changed on 2026-11-09 (PR #32), before the rules of
2026-11-10.

- Every seminar: the picture of each activity inside its task box, with
  exactly the objects, names and numbers of its questions (not a lecture
  figure); no step or exercise that asks for English text.
- Every lecture: no Do it or exercise that asks for a sentence; the Game
  challenge in one Try it box of 3–4 questions (the last one harder); a
  picture for every task that names objects.
- Homework: no "Give the reason" (a choice instead); private solution
  changed with it.
- Digital Skills Online activity 3: drawn screens for every app step
  (`tools/phone_screens.py`, a tab per device), taken out of
  `BEFORE_SCREENS`; tasks ask only for what the device can do.

## Progress

- [x] Game Math Unit 4: Seminar 4 pictures inside the activity boxes (`aim-drones`, `orb-lift`, drones named A, B, C); Lecture 4: a figure for the targets of 4.5 (`targets`), the Game challenge in one box of four questions, a tick instead of a sentence in the 4.3 Do it of the notes, exercise 16 new; Homework 4 Task 1b a short answer instead of "Give the reason" (solution changed).
- [x] Computing Systems Unit 5: Lecture 5: the Game challenge in one box of four questions; the Do it of 5.1 in the notes asks for a tick, not a sentence; exercises 3, 7, 9, 10 are choices. Seminar 5: the pictures inside the activity boxes (Test Day after the box), Activity 2 Step 2 a yes or no and a tick, Try it 3 has three questions, exercise 5 a choice. Homework 5 already met the rules (no change).
- [x] Digital Media Unit 4: Lecture 4: the Game challenge in one box of three questions (the last one harder), the 4.1 Do it shorter (40 planned minutes); exercises 1, 3, 4, 5, 6, 7, 8, 9, 10 of the notes are choices or a word. Seminar 4: the scene card and the line table inside the box of Activity 1; a new picture of Nour's two barks and the three triggers inside the box of Activity 2 (`barks-back`, also on the slide; `revise` removed); Try it 3 has three questions. Homework 4 already met the rules (no change).
- [x] Digital Skills Unit 3: Online activity 3: the drawn screens of every
  app step (`tools/phone_screens.py`, `@window`): Save As PDF in Word on a
  computer and Download as PDF in Word on the web (two tabs), Ctrl + C in
  Excel and the Paste Options in Word, the Share button and dialog; taken
  out of `BEFORE_SCREENS`. Its tasks now say where they work (Task 1: Word
  on a computer or on the web; Task 2: the desktop apps); the platform text
  says the same. Lecture 3: the Game challenge in one box of three
  questions (the last one harder), the page trimmed to 40 planned minutes;
  the exercises of the notes ask for a name, a choice or yes or no; the
  record of Experiment 3, Step 3 asks for task numbers.

## For the teacher to check

- The screens of Online activity 3 are drawn after the current Windows and
  web layouts of Word and Excel (File › Save As › PDF (*.pdf); File ›
  Export › Download as PDF on the web; the Paste Options under a pasted
  table; Share › Specific people › Can view). The official help pages could
  not be read from here: look at them once in the real apps.
- Online activity 3 no longer offers the phone apps for its tasks: the
  Paste Options are not in the Word phone app. If the students must be able
  to do every task on a phone, Task 2 needs another product.
