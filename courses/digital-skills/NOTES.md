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
  and answered in one line. With the worksheet they are a short reference.
- **Lab tasks and experiments** use only the lab computer, a browser and the
  student's own phone, with steps written as a numbered list.
- The ILOs and the lecture titles follow the course syllabus v2 (Drive,
  2026-10-23): Microsoft Office and AI tools, built on the university course
  description *Smart Digital Skills*. Ask the teacher before a syllabus title
  is changed.

## Timing and textbook: a blended course

- 2 credit hours, **fully practical** (the study plan: 2 hours in the
  computer lab) and **blended**: every week has one face-to-face lab session
  (60 min) and one online activity (asynchronous, about 60 min of work, on
  the university e-learning platform: an interactive lesson with
  simulators, or a video, and practical tasks to submit). No seminars.
  `course.blended: true` in `_metadata.yml`; `schedule.yml` has 15 weeks:
  10 units (core: Lecture N and its online activity) and 5 practice weeks
  (flexible: Practice N in the lab and an online practice activity, no new
  ideas). Online activities are numbered 1–15 in teaching order.
- **Face-to-face lecture: a worksheet first** (AUTHORING.md, "Lecture
  worksheets"). The worksheet (`lesson-NN-sheet.qmd`, PDF) is the main
  document of the session, like the manual of a lab experiment: the goal
  (the ILOs), what you need, the start files, 3–4 experiments (one per
  section) with numbered steps, a place to record the result after every
  step, and a table of results. Students do it on the computer during the
  lecture and the teacher checks it there; it is never uploaded. The notes
  (PDF) are a short reference, the interactive page shows the same
  experiments with "Check your result" after every step, and the slides are
  the teacher's demonstration of the worksheet. Size for **60 minutes**
  (3–4 sections, about 40 minutes of experiments) and a ~10-min Game
  challenge set in an ordinary workplace or a student's study work.
- **Real apps or simulators** in the worksheet, by the nature of the
  lecture (the choice of each lecture is in `plan.md`): Word, Excel,
  PowerPoint or an AI tool when the lab has it, the simulators of the page
  as the teacher's demonstration and the way to do a step without the app.
- **Practice session** (`practice-NN*`, flexible, in a practice week):
  hands-on work on earlier lectures in Word, Excel, PowerPoint or an AI
  tool, in the seminar format (AUTHORING.md, "What a seminar looks like");
  no new ideas; every answer on its page.
- **Online activity:** `online-NN.qmd` with `online: N`, `due:` ("before
  lecture N", the next face-to-face lecture) and `marks:`; no notes and no
  slides. It **practises its unit** and never repeats the face-to-face
  lecture; in a unit it may add a skill of the unit's syllabus row (Online
  activity 9: an AI outline turned into slides); in a practice week it adds
  nothing new. Start from `shared/templates/online-template.qmd`. It has:
  1. "Before you start": what you need, about how long, what you submit;
  2. two or three short **Steps** (`{.study}`): plain explanation, a figure,
     a simulator to try at once, one "Try it" self-check with `Why:`
     reasons, and a `.check` where a step asks for a result;
     where the teacher has a video, the e-learning platform links it;
  3. **Tasks to submit** (`{.tasks}`): 2–4 tasks with marks, each with a
     concrete product (a file with a given name, a screenshot, a short
     answer) and answer space for the printed copy;
  4. **How to submit**: one short line (the e-learning platform, file names).
  The Steps are hidden on paper: "Print tasks" and "Download tasks (PDF)"
  give only the tasks (`homework_pdf.py` prints the page).
- The online activity **replaces the homework**: no `homework-UU.qmd` in
  this course. Model answers and marking notes go to `courses-private`
  (`courses/digital-skills/week-WW/online-NN-solutions.md`).
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
- Every task done with AI ends with checking the output and, from unit 9 (Lecture 9) on, an AI-use statement.
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
- 2026-10-28 (plan v2, `plans/restructure-19-lectures.md`): 15 units with
  10 core lectures, 5 flexible practice sessions and all 15 online
  activities. Each online activity now practises its unit instead of
  copying the lecture (old 20, 22, 24 and 26 copied 19, 21, 23 and 25), old
  lecture 27 no longer repeats lecture 6, and the course project has no peer
  feedback (it needed classmates). Cut: how AI works (next-word
  probabilities; *AI Applications* teaches it), SUMIF/COUNTIF, the
  know/have/are factors, the 3-2-1 rule and data classes. Lecture 8 adds the
  animations that the syllabus names. The AI-use statement starts in unit 11.
- 2026-10-30 (plan v2 applied to all 15 units): Lectures 1–10, Practice 1–5
  in the short seminar format (two problems, at most 40 planned minutes,
  every answer on the page) and Online activities 1–15 (`online-NN.qmd`,
  due "before lecture N"; Online activity 15 after Lecture 10). Every
  question has a reason and every Lab task a result. The online activities
  practise their unit with their own examples and simulators; Practice 2–5
  and Online activities 10–14 overlap a little because a flexible practice
  may be skipped. Removed: the DigComp self-check, Hiring Desk, Next Word,
  The Right Tool (SUMIF/COUNTIF) and Link Lab, and the figures of how AI works, why AI
  is wrong, summary formulas, the AI workflow, e-mail sharing and peer
  feedback. New: Claim Finder (Online activity 11), Rehearsal Lab (Online
  activity 9 and Lecture 10) and the figures "what AI does well" and
  "animations step by step". Changed: Transition Lab (Appear, Fade, Spin),
  Prompt Cleaner (two prompts for Online activity 12), AI Formula Lab (SUM,
  MAX, AVERAGE), Office Relay (no link round), Presentation Day (no link or
  peer-feedback round). Cut: SUMIF, COUNTIF and AVERAGEIF, linked tables and
  charts (Paste Link, Update Link), sharing with classmates, peer feedback.
  The course project runs through Online activity 14 (plan, data sheet,
  first draft), Lecture 10 (five slides, four checks, a three-minute talk)
  and Online activity 15 (the final files with a table of contents, page
  numbers and one AI-use statement).
- 2026-10-31 (plan v3): the teacher confirmed that the course is fully
  practical and blended, without seminars, with 10–12 core weeks and
  filling weeks without new content. Now 10 units (Lectures 1–10 with their
  online activities) and 5 practice weeks (Practice 1–5 with Online
  activities 8, 10, 12, 14 and 15). Old Practice 4 (PivotTables, new
  content in a flexible session) became Lecture 10 "Excel (3): Summarizing
  Data with AI Help" (week 13: a PivotTable, other questions, an AI summary
  checked number by number); Online activities 9 and 10 swapped places (the
  AI outline in the PowerPoint unit, the five-slide talk in the practice
  week); old Lecture 10 (project presentations) became Practice 5 and old
  Practice 5 became Practice 4. Online activity 13 is due one week after
  Lecture 10, Online activity 14 before Practice 5. Removed: Presentation
  Day and one unused figure.
- 2026-10-31 (teacher's request, lecture worksheets): every lecture is now
  built around a worksheet that students fill in during the lecture, like
  the manual of a lab experiment, with start files (`tools/start_files.py`)
  so that every student has the same data. Lecture 6 (Excel 1) was the
  model: four experiments in Excel with `shop-start.xlsx`, Formula Lab and
  Reference Lab as the teacher's demonstration.
