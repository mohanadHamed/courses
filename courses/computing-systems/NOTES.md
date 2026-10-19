# Fundamentals of Computing Systems and Digital Platforms (13411133) — course notes

Course-specific rules only. Global rules are in the root `AUTHORING.md`.

## Timing and textbook

- 2 × 60 min (2 credit hours). Lesson A = syllabus Lecture topic, Lesson B =
  syllabus Seminar topic (applied: devices, specs, case studies).
- Textbook: Tanenbaum and Austin, *Structured Computer Organization*, 6th ed.
  (the computer as a multilevel machine, the computer zoo); reference:
  Silberschatz et al., *Operating System Concepts*, 10th ed., and the official
  Android and Apple developer documentation.
- Size for **60 minutes** (3–4 sections). `check_size.py` warns at every render.
- Every lesson ends with a ~10-min Game challenge that each student does alone.
- Numbers about hardware and markets change quickly: give orders of
  magnitude ("about half of game revenue", "100 MB/s to over 1 GB/s") and
  check them each semester.
- File and memory sizes count in steps of **1024**, as Windows does and as
  Digital Skills does: 1 KB = 1024 bytes, 1 MB = 1024 KB, 1 GB = 1024 MB,
  1 TB = 1024 GB. Drive makers count in 1000s, so a "1 TB" drive shows about
  931 GB in Windows.

## Lessons learned

- Week 1 (2026-10-17): group work and physical activities are not always
  possible. The pair activity and the group device survey became solo Game
  challenges.
- Week 1 (2026-10-19, after teaching): input–processing–output alone was too
  simple. Rebuilt with the stored-program model, the instruction cycle, the
  multilevel machine and ISAs, classes of computers and digital platforms
  (lesson 1), and launching, CPU/GPU frames, latency and cloud gaming
  (lesson 2), with the mini-games Tap Runner and Lag Lab.
- Week 1 (2026-10-19, applied first): simpler level and English; Do it tasks
  on the lab PC (Settings → About for the ISA, display settings, Task
  Manager), on the phone (timing a game start) and in the mini-games. Left
  out: the six-level machine table, translation vs interpretation, Moore's
  law. Lesson 3 (week 2) was the model lesson for this approach.
- Week 1 (2026-10-19, level check, about 20 % simpler): ticks-per-frame,
  frame-rate, pixel and input-lag calculations, the ISA and compiler section
  and bandwidth were removed; one sentence on builds per platform (ARM, x86)
  stays.
- Week 2 (2026-10-20, teacher review): lesson 3 now counts sizes in 1024
  instead of 1000, like Digital Skills, so students of both courses learn one
  rule. 1024 × 1024 bytes = 1 MB makes the texture example exact (4 MB);
  the Try it asks 2 GB = 2048 MB.
