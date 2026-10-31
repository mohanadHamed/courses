# Fundamentals of Computing Systems and Digital Platforms (13411133) — course notes

Course-specific rules only. Global rules are in the root `AUTHORING.md`.

## Timing and textbook

- 2 credit hours (1 theory + 1 seminar), taught every week as one lecture
  of 60 min and one seminar of 60 min; the seminar practises the lecture of
  the same week (applied: devices, specs, case studies).
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
- 2026-10-28 (plan v2): 14 units (weeks 1–7 and 9–15), each with a core
  lecture and a seminar; Seminars 2, 3, 4, 13 and 14 are core, the others
  flexible. Two earlier decisions were reversed as the plan proposed: cloud
  gaming and latency (Lag Lab) left unit 1 and stay, short, in Lecture 12;
  the texture-memory sums are cut (sizes still count in 1024). Also cut:
  process states, time-slice sums, virtual memory, block details, HAL / ART
  / XNU (generic layers stay), exact store limits, signing keys, IPv6, MAC,
  the four-layer model, nslookup, tracert, price sums, the weighted decision
  matrix, the NPU and brand lists. Fixes: the cloud-gaming delay matches Lag
  Lab, Parts Finder's table has 7 rows, "Ask a classmate" became "check the
  maker's update page". Tasks with AI: an AI-drafted comparison table of five
  devices with three numbers checked on the makers' pages, a test plan for
  four devices, a store-listing checklist checked against the official
  guidelines.
- 2026-10-31 (plan v3): every week is one lecture and one seminar; 12 core
  weeks and 2 practice weeks (with the midterm week, 15 weeks on the
  platform). Lectures 5 and 6 were merged into Lecture 5 "Operating Systems:
  Processes, Memory, Files and Devices" (unit 5 covers syllabus weeks 5 and
  6); the device check (old 6.3) is now a problem of Seminar 5, which joins
  the OS tour and the device check. Old Lectures and Seminars 7–13 became
  6–12; Lecture 14 became Practice 1 (two case studies: frames and a hot
  phone with Performance Detective; one build for every device with
  Compatibility Lab and a reliable source) and Seminar 14 Practice 2 (the
  project presentations). Homework 5 joins old 5 and 6. Removed: Settings
  Explorer, Name Checker, Disk Doctor and four unused figures.
- 2026-10-31 (teacher's review of the AI boxes): the four "Task with AI"
  boxes (Seminars 3, 7, 8 and 12) became extras with a complete prompt and a
  coloured table to look at, built from given facts so that the answers do
  not change: five made-up test phones by level, Android and iOS for a
  studio with one Windows laptop, a checklist before the stores, and a test
  table of four setups; each has two or three changes to try with closed
  answers.
