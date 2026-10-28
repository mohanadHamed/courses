# Fundamentals of Computing Systems and Digital Platforms (13411133) — unit plan

Status: approved on 2026-10-28 (`plans/restructure-19-lectures.md`, version 2). Source: the official syllabus (2026-2027, Drive) and the ILO–PLO matrix.
One unit = one week of the syllabus (AUTHORING.md, "Units and sessions"). `schedule.yml` holds the same map for the site and the course package; if they differ, `schedule.yml` wins. "From" names the old lectures and sections that each session is built from.

## Course ILOs

| Code | ILO (official text, with PLOs) |
|---|---|
| A1 | Describe the components of computers and smartphones and the function of each. (PLO 1) |
| A2 | Explain the functions of operating systems and the concepts of networking and cloud computing. (PLO 1) |
| B1 | Compare mobile platforms (Android and iOS) and gaming platforms in terms of capabilities and limitations. (PLO 1, 3) |
| B2 | Analyze the impact of device and platform specifications on game performance and compatibility. (PLO 1, 4) |
| C1 | Set up testing environments for games using emulators and real devices. (PLO 1, 3) |
| C2 | Describe the requirements for publishing games on app stores and cloud services. (PLO 3, 4) |
| D1 | Use reliable sources for self-learning and follow developments in digital platforms. (PLO 3) |

## Units: 14 units, 14 lectures + 14 seminars (60 min each)

| Unit (week) | Lecture (core) | From | Seminar | From | Seminar core? | ILOs |
|---|---|---|---|---|---|---|
| 1 (1) | **Lecture 1** Computing Systems and Digital Platforms in the Games Industry | 1 + 2.4 | **Seminar 1** The Devices Students Use and How Games Run on Them | old 2 activities (time a game start, your screen, right device) | flexible | A1 |
| 2 (2) | **Lecture 2** Computer Components: CPU, Memory and Storage | 3 + 2.1 | **Seminar 2** Identifying Components and Reading Specifications | 4.1, 4.2 | core | A1 |
| 3 (3) | **Lecture 3** Input/Output Devices, the GPU and Graphics Hardware | 5 + 2.2 | **Seminar 3** Comparing Device Specifications for Gaming | 6 + settings table of 5 | core | A1 B2 |
| 4 (4) | **Lecture 4** Smartphone Architecture: SoC, Sensors, Touch Screen and Battery | 7 | **Seminar 4** Analyzing a Smartphone Specification Sheet | 8 + 4.3 | core | A1 B2 |
| 5 (5) | **Lecture 5** Operating Systems: Functions, Processes and Memory Management | 9 + essentials of 10 | **Seminar 5** Operating-System Tour on PC and Mobile | 10 | flexible | A2 |
| 6 (6) | **Lecture 6** File Systems, Resources and Device Management | 11.1, 11.3 + essentials of 12 | **Seminar 6** Hands-on: File and Resource Management | 12 | flexible | A2 C1 |
| 7 (7) | **Lecture 7** Mobile Operating Systems: Android and iOS Architecture | 13 + essentials of 14 | **Seminar 7** Exploring Android and iOS Features | 14 | flexible | A2 B1 |
| 8 (9) | **Lecture 8** Mobile Platforms Compared: Android vs iOS (team activity in the notes) | 15.1, 15.2, 15.4 + reliable sources of 16 | **Seminar 8** Platform Comparison Activity | 16 | flexible | B1 D1 |
| 9 (10) | **Lecture 9** App Stores and Publishing Requirements | 17 + 15.3 + essentials of 18 | **Seminar 9** Reviewing App-Store Guidelines | 18 | flexible | C2 |
| 10 (11) | **Lecture 10** Networking Concepts: LAN, the Internet and Protocols | 19 + 20.1–20.2 essentials | **Seminar 10** Networking Tools Demonstration | 20 | flexible | A2 |
| 11 (12) | **Lecture 11** Cloud Computing: Models and Services | 21 + essentials of 22 | **Seminar 11** Cloud Services for Games: Storage and Hosting | 22 | flexible | A2 C2 |
| 12 (13) | **Lecture 12** Gaming Platforms: Consoles, PC, Mobile and Cloud Gaming | 23 + 24.1, 24.3 | **Seminar 12** Case Study: Comparing Gaming Platforms | 24 | flexible | B1 B2 |
| 13 (14) | **Lecture 13** Setting Up Test Environments: Emulators and Real Devices | 25 (+ developer options from 14) | **Seminar 13** Hands-on: Running a Sample App on an Emulator | 26 | core | C1 |
| 14 (15) | **Lecture 14** Platform Performance and Compatibility: Case Studies | 27 | **Seminar 14** Student Presentations (Project) | 28 | core | B2 C1 D1 |

- Core: 14 lectures + Seminars 2, 3, 4, 13, 14 = **19**. Flexible: 9 seminars.
- "Essentials of …" means the lecture keeps the one idea of that seminar that
  an ILO or the exam needs; the activities stay in the seminar.
- **Cut (beyond the ILOs):**
  - 2.3 (cloud gaming, Lag Lab) in unit 1; it stays, short, in Lecture 12;
  - process states, time-slice sums, virtual memory;
  - block details and the file-system format table (keep "FAT32 cannot hold
    a 4 GB file" as a common mistake);
  - HAL / ART / XNU (keep generic layers: kernel, libraries, framework, apps);
  - exact store limits, signing keys, staged-rollout percentages;
  - IPv6, MAC, the four-layer model, nslookup, tracert;
  - egress and price sums;
  - the weighted decision matrix (keep a 3-criterion table);
  - the fourth repetition of throttling.
- **Homework:** 13, one per unit; the project instead of homework in unit 14.

## Tasks with AI (ideas)

a comparison table of five phones or consoles from an AI draft, three numbers checked on the makers' pages; a test plan for a game on four devices; a store-listing checklist checked against the official store guidelines (D1, reliable sources).

## Notes

- **Independent study first.** Pages, slides and homework never require classmates.
- No ILO of this course asks for team work (D1 is self-learning with reliable sources). The notes of Lecture 8 have the team activity that version 2 of the plan names, with an individual alternative; the unit-14 presentations are individual project presentations.
- Reversed earlier decisions (plan, "Open decisions"; cut as planned): cloud gaming and latency (old 2.3, Lag Lab) leave unit 1 and stay, short, in Lecture 12; the texture-memory sums in 1024 are cut (file sizes still count in 1024).
- Homework: one per unit (13); unit 14: the project instead (syllabus).
