# Digital Skills (01101154) — course notes

Course-specific rules only. Global rules are in the root `AUTHORING.md`.

## Audience: every diploma student, not only technology students

This course is taught to the diploma students of the whole Technical
College. Most of them do not study technology (for example supply
management, medical sterilization, facility assessment). So this course is
**simpler than every other course**, and its examples are **general**.

- **Examples everyone knows:** daily life (a phone, a message, a photo, an
  online form, a bill), study (homework, the e-learning platform, a class
  report) and common jobs (an office, a shop, a bank, a school). Never the
  games industry, and never one specialization (no supply chains, no
  hospitals as the main setting). Made-up workplaces are ordinary ones
  (Sunrise Company, a small office).
- **English: A2** in the notes, the page and the slides. Sentences of about
  12 words at most, one idea each; the 1000 most common English words where
  possible; no idioms, no passive voice. Every computer word is explained in
  plain words the first time (an "app" is a program on a phone).
- **Less theory than the other courses:** one short definition per section
  at most, one worked example per section, small steps. Leave out names,
  dates and numbers that no task needs.
- **Notes:** at most about 2 000 words without exercises; exercises are short
  and answered in one line.
- **Lab tasks** use only the lab computer, a browser and the student's own
  phone, with steps written as a numbered list.
- The ILOs and the lecture titles follow the course syllabus v2 (Drive,
  2026-10-23): Microsoft Office and AI tools, built on the university course
  description *Smart Digital Skills*. Ask the teacher before a syllabus title
  is changed.

## Timing and textbook: a blended course

- 2 credit hours, **blended**: each week one face-to-face lecture (60 min,
  computer lab) and one online activity (asynchronous, about 60 min of work,
  on the university e-learning platform). `course.blended: true` in
  `_metadata.yml`; the online lectures have `online: true` in
  `schedule.yml`.
- **Face-to-face lecture (odd number):** a full lesson like the other
  courses: notes (PDF), interactive page, slides; size for **60 minutes**
  (3–4 sections), a Lab task in every section, a ~10-min Game challenge set
  in an ordinary workplace or a student's study work.
- **Online activity (even number):** `lesson-NN.qmd` with `online: true`,
  `due:` ("before lecture 2k+1") and `marks:`; no notes and no slides. Start
  from `shared/templates/online-template.qmd`. It has:
  1. "Before you start": what you need, about how long, what you submit;
  2. two or three short **Steps** (`{.study}`): plain explanation, a figure,
     a simulator to try at once, one "Try it" self-check (instant feedback);
     where the teacher has a video, the e-learning platform links it;
  3. **Tasks to submit** (`{.tasks}`): 2–4 tasks with marks, each with a
     concrete product (a file with a given name, a screenshot, a short
     answer) and answer space for the printed copy;
  4. **How to submit**: one short line (the e-learning platform, file names).
  The Steps are hidden on paper: "Print tasks" and "Download tasks (PDF)"
  give only the tasks (`homework_pdf.py` prints the page).
- The online activity **replaces the homework**: no `homework-KK.qmd` in
  this course. Model answers and marking notes go to `courses-private`
  (`courses/digital-skills/week-PP/lesson-NN-solutions.md`).
- Textbook: Evans, Martin and Poatsy, *Technology in Action*, Global Edition,
  18th ed. References: Lambert and Frye, *Microsoft Office Step by Step
  (Office 2021 and Microsoft 365)*, 2022; Microsoft 365 Training
  (support.microsoft.com/training); UNESCO, *Guidance for Generative AI in
  Education and Research*, 2023; *DigComp 2.2*, 2022.

## Practical first: many simulators

The teacher wants every lesson and every online activity to be practical and
interactive: students try each idea at once on something that works like the
real tool.

- **2–4 simulators or mini-games** in every face-to-face lesson, and **at
  least 2** in every online activity. Prefer simulators of the real tools:
  a folder window, a Word page with a ribbon, an Excel grid that computes, a
  slide editor, an AI chat with fixed answers. Draw them as simple generic
  interfaces (no Microsoft logos, no screenshots).
- **The AI chat simulator gives fixed, prepared answers** (no AI service, no
  Internet): the student picks a prompt and sees what a typical assistant
  answers, including typical mistakes to find.
- Simulators check the student's work and say what is right or wrong
  (a path, a file name, a formula, a prompt with task, context and format).
- Everything works on a phone: many students do the online activity at home
  on a phone.

## AI tools

- Name the idea and two or three common free tools (Microsoft Copilot with
  the university account, ChatGPT, Gemini), never one product only. No task
  needs a paid plan. Copilot inside Word, Excel or PowerPoint is "if your
  account has it"; the tasks also work by copying from an AI chat.
- Never ask students to type real personal data (ID numbers, phone numbers,
  addresses, grades) into an AI tool: use made-up details.
- Every task done with AI ends with checking the output and, from lecture
  23 on, an AI-use statement.
- AI is a tool for documents, data and presentations here; how AI works is
  the subject of *AI Applications* (01101153). Keep to what a user needs.

## Lab sessions

- Keep lab tasks independent of one product's menus where possible: name the
  concept (version history, sharing permission) and the common tools
  (Microsoft 365 / Google Workspace), because the lab software may change.
- Never ask students to enter real passwords or personal data into a page of
  this site. Self-assessments stay in the student's browser.
- In the guidance plan of the diploma the course is in semester 2; the
  2026-2027 syllabus and the timetable put it in semester 1.
- File sizes count in steps of **1024**, as Windows on the lab computers
  does: 1 KB = 1024 bytes, 1 MB = 1024 KB, 1 GB = 1024 MB. One-step
  conversions (2 GB = 2048 MB) are fine; 1024 is not hard for the students.

## Lessons learned

- Week 1 (2026-10-19): course started with the new lesson model. Interactive
  parts: DigComp self-check (simulator) and Path Finder (mini-game on paths).
- Week 1 (2026-10-19, applied first): simpler level and English; a Lab task
  in every section instead of one block at the end (DigComp self-check, a
  real job advertisement, single sign-on, extensions and Copy as path,
  course folders, version history and restore). Left out: the 1000 vs 1024
  conversion.
- Week 1 (2026-10-19, level check, about 20 % simpler): the table of 21
  competences (now five areas in simple words), the EU-targets figure,
  relative paths and file-size calculations were removed.
- Week 1 (2026-10-20, teacher review): the slides of lesson 1 felt
  theoretical. The Game challenge is now a mini-game, Hiring Desk (sort the
  tasks of Pixel Harbor's job adverts into DigComp areas, read the
  candidates' levels, hire), played on the projector and on the phones.
  File sizes in lesson 2 now count in 1024 instead of 1000, with one worked
  example (2 GB = 2048 MB) and one exercise.
- Week 1 (2026-10-21, teacher review): the course is for all diploma
  students of the college, most of them not in technology. Both lessons,
  the slides, the homework and the mini-games were rewritten in A2 English
  with general examples: Pixel Harbor (a game studio) became Sunrise Company
  (an office and a shop), game files and trailers became class reports and
  family videos, and the course folders are general ones (English, Arabic).
  Paths are Windows paths (as on the lab computers). The DigComp self-check
  and the figures use plain words ("I check if information is true"), and
  the diploma line of this course is "All diploma programmes" (an override
  of `diploma-line` in `_metadata.yml`).
- 2026-10-23 (new plan): the course was rebuilt on the university course
  description *Smart Digital Skills* (Office and AI), keeping its name,
  number and 2 credit hours. Databases, websites and digital marketing were
  dropped; AI tools take more than a third of the lectures. The course is
  blended: one face-to-face lesson and one online activity per week (no
  separate homework), with many simulators of the real tools in both.
  Lecture 1 is now about the apps that make us productive (AI assistants
  included) and lecture 2 (accounts, files, cloud) became the first online
  activity.
