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
- The ILOs and the lecture titles follow the course syllabus **v3**
  (2026-11-13): the official course description of the study plan
  (digital skills and the labour market, devices and technologies, digital
  content, data analysis, databases, a digital service, website design,
  e-marketing). Ask the teacher before a syllabus title is changed.
- **As easy as possible** (the teacher's request of 2026-11-13): the
  students come from every diploma, most with no IT background and weak
  computer skills, and their English is very weak. Each ILO is covered at
  its minimum; every text is very short; no task asks for English writing
  (no e-mail, no text of their own): the student chooses, matches, orders,
  sorts, or types a letter, a number or a given text. Graded online tasks
  give all the facts (the four project services) and ask for letters,
  numbers, links, files or screenshots.

## Timing and textbook: a blended course

- 2 credit hours, **fully practical** (the study plan: 2 hours in the
  computer lab) and **blended**: every week has one face-to-face lab session
  (60 min) and one online activity (asynchronous, about 60 min of work, on
  the university e-learning platform: an interactive lesson with
  simulators, or a video, and practical tasks to submit). No seminars.
  `course.blended: true` in `_metadata.yml`; `schedule.yml` has 12 weeks
  (plan v4): 10 units (core: Lecture N and its online activity) and 2
  practice weeks (flexible: Practice N and an online practice activity, no
  new ideas; row 8 the review, row 15 the project). Online activities are
  numbered 1–12 in teaching order.
- **Face-to-face lecture: two cases, one lesson** (since 2026-11-08;
  AUTHORING.md, "The page is taught in class" and "Lecture worksheets").
  The computer labs of the college are not ready yet, and the classrooms
  have smart screens. So every lecture works in both cases:
  - *Without a lab* (now): the teacher teaches from the **interactive
    page** on the smart screen, about **40 minutes**. Each section is the
    idea in a few points, its simulator, its experiment and one applied Try
    it question. The teacher does Part A of the experiment on the
    simulator of the section (it holds the data of the start file) or in
    the app on the teacher's laptop, runs each AI prompt (**Copy prompt**)
    in an AI assistant in another tab, and the class answers the check of
    every step. Students can open the page on their phones and do Part B.
  - *In the lab* (later): the students follow the **worksheet** (PDF, the
    manual): Part A in Word, Excel, PowerPoint or an AI assistant, Part B
    on a simulator; they write each result, and the teacher checks the
    table of results.
  The worksheet has 3 experiments (`## Experiment N · …`: "The idea:",
  "Aim:", Part A and Part B as `{.part}` labels, 2–3 steps in Part A and 1
  in Part B), taken from the face-to-face version; the page leaves out
  "The idea:". The notes (PDF) are a short reference with one section per
  experiment; the slides are a reference of the lecture in the
  face-to-face model (concepts, Live demos, Try it, Summary, Your
  worksheet, Results of the worksheet, the Game challenge).
- **Real apps and simulators:** Part A in Word, Excel, PowerPoint or an AI
  tool, Part B on the simulators of the page. A simulator of an Office task
  is the lab of a class without computers, so give it the data of the
  start file (Formula Lab and `shop-start.xlsx`, Bill Check and the bill of
  Lecture 2).
- **Practice session** (`practice-NN*`, flexible, in a practice week):
  hands-on work on earlier lectures in Word, Excel, PowerPoint or an AI
  tool, in the seminar format (AUTHORING.md, "What a seminar looks like");
  no new ideas; every answer on its page.
- **Online activity:** `online-NN.qmd` with `online: N`, `due:` ("before
  lecture N", the next face-to-face lecture) and `marks:`; no notes and no
  slides. It **practises its unit** and never repeats the face-to-face
  lecture; in a unit it may add a skill of the unit's syllabus row (Online
  activity 4: PowerPoint, row 5 of a merged unit); in a practice week it
  adds nothing new. Start from `shared/templates/online-template.qmd`. It has:
  1. "Before you start": what you need, about how long, what you submit;
  2. two or three short **Steps** (`{.study}`): plain explanation, a figure,
     a simulator to try at once, one "Try it" check with `Why:`
     reasons, and an interactive check (`.choice`, `.order`, `.sort` or
     `.fill`) where a step asks for a result: it answers at once;
     where the teacher has a video, the e-learning platform links it;
  3. **Tasks to submit** (`{.tasks}`): 2–4 tasks with marks, each with a
     concrete product (a file with a given name, a screenshot, a short
     answer) and answer space for the printed copy;
  4. **How to submit**: one short line (the e-learning platform, file names).
  The Steps are hidden on paper: "Print tasks" and "Tasks PDF to fill in"
  give only the tasks (`homework_pdf.py` prints the page).
- The online activity **replaces the homework**: no `homework-UU.qmd` in
  this course. Model answers and marking notes go to `courses-private`
  (`courses/digital-skills/week-WW/online-NN-solutions.md`).
- Textbook: Evans, Martin and Poatsy, *Technology in Action*, Global Edition,
  18th ed. References (syllabus v3): Lambert and Frye, *Microsoft Office Step
  by Step (Office 2021 and Microsoft 365)*, 2022; Chaffey and
  Ellis-Chadwick, *Digital Marketing*, 8th ed., 2022; Duckett, *HTML and
  CSS*, 2011; *DigComp 2.2*, 2022; Microsoft 365 Training
  (support.microsoft.com/training).
- **The course project (D1)** is built in the core: Online activity 9 (the
  student chooses one of four given services, A–D, and builds its form),
  10 (its website), 11 (its post and marketing plan), then Practice 2 (the
  talk) and Online activity 12 (the final submission).

## A face-to-face version (prepared, not published)

The course may become fully face-to-face if the students ask for it. That
version is written in advance in `face-to-face/` (two sessions of 60
minutes in the lab each week, each with slides, a worksheet and an
interactive lesson; no online activities and no notes), numbered in one
sequence: Lectures 1–30, two in each week. It is never built
for the site (`_quarto-site.yml`); preview it with `--profile f2f`. Its
`README.md` has the model, the rules, the progress and the steps to switch
the site. On 2026-11-08 the teacher decided that the course stays blended
and that this version stays hidden as it is. The blended Lectures 2–10 then
took its worksheets, pages and slides (Part A and Part B) and were sized
for a class on the smart screen, with three experiments each and prompts to
copy, so they now differ from it. Leave the face-to-face version as it was
on 2026-11-06; if the course is ever switched, first bring it in line with
the blended lectures (`face-to-face/schedule.yml`, `from`).

## Practical first: many simulators

The teacher wants every lesson and every online activity to be practical and
interactive: students try each idea at once on something that works like the
real tool.

- **2–4 simulators or mini-games** in every face-to-face lesson. In an
  online activity the content type decides (AUTHORING.md, "Blended
  courses"; the table in `plan.md`): a simulator in every Step of a `sims`
  activity, at least one in a `mix`, and simulators where they help in a
  `lesson`, a `video` or a `course-video` activity. Prefer simulators of the real tools:
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
- **The screens of the real apps** (AUTHORING.md, "Screens of every app
  step"): an online activity is done alone, so every Step that has the
  student work in an app shows its screens, one drawn picture per step,
  with Android and iPhone in two tabs for a phone app (Online activity 2:
  Google Calendar and Calendar, Google Drive and Files). A simulator lets
  the student try the idea; the screens show where the buttons of the real
  app are. The other online activities get their screens when they are
  next written or rewritten.

## AI tools

- Name the idea and two or three common free tools (Microsoft Copilot with
  the university account, ChatGPT, Gemini), never one product only. No task
  needs a paid plan. Copilot inside Word, Excel or PowerPoint is "if your
  account has it"; the tasks also work by copying from an AI chat.
- Never ask students to type real personal data (ID numbers, phone numbers,
  addresses, grades) into an AI tool: use made-up details.
- Every task done with AI ends with checking the output; the final project
  (Online activity 12) has the AI-use line where AI helped. Since syllabus
  v3, AI is a tool of C1 (Units 1–2) and a small helper in later lectures
  (one prompt in Lecture 10), never the topic of a session.
- AI is a tool for documents, data and presentations here; how AI works is
  the subject of *AI Applications* (01101153). Keep to what a user needs.
- **Practical, never AI alone** (the teacher's request of 2026-11-08: the
  students know AI already, and Lecture 2 felt theoretical in class). Every
  AI step of a worksheet gives its complete prompt in `::: {.prompt}` (the
  page adds "Copy prompt"; a prompt that needs a text holds the text, so it
  works without the start file), and its result goes into an Office task: a
  draft corrected in Word, a total checked in a spreadsheet, a fair advert
  with an AI-use statement in Word, an AI summary checked against a
  PivotTable. No more than three prompts in a lecture: each one takes about
  two minutes in class.

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

## On the e-learning platform (Moodle)

The teacher fills one section of the university e-learning platform for
every calendar week, by hand, with the university's template.

- **Language:** the section text is in Arabic (the platform is in Arabic);
  the linked pages and the files stay in English, as on this site. Never
  write "مختبر": the face-to-face lecture may be in an ordinary classroom.
- **The template, part by part:**
  1. Title: "الأسبوع … (date): topic".
  2. "في هذا الأسبوع سوف نعمل على": a short paragraph.
  3. "في نهاية هذا الأسبوع ستكون قادرا على": the outcomes, numbered.
  4. "المطلوب من الطالب القيام به خلال الأسبوع": numbered steps.
  5. "الأنشطة غير المتزامنة": the links and the submission.
- **Parts 1–3 describe the whole week,** the face-to-face lecture
  included: they are descriptions and ask nothing of the student.
- **Parts 4–5 are only the online (blended) lecture** ("المحاضرة المدمجة"):
  its steps (the Steps of the online activity, its videos and simulators,
  then the tasks to submit), the link to its page and its submission.
  Never the face-to-face lecture: students get its instructions in class,
  and a second list of work would confuse them.
- **No marks and no due dates in the text.** The due date is set as an
  option of the Moodle assignment, and the platform reminds the students.
- A lost week stays on the platform as a real week with a role of its own
  (for example "getting ready": accounts, tools, how the course works),
  never as a copy of the next week. Its activities are moved to the week in
  which they are done, not deleted, so that submissions are kept.
- **The weeks of fall 2026-2027.** Lecture 1 was given in platform week 4
  (1/11/2026) and Lecture 2 in week 5. From week 6 (15/11/2026, plan v4)
  each platform week holds one unit: Units 3–10 in weeks 6–13; week 14
  (10–14/1/2027, the last teaching week) holds Practice 2 and Online
  activity 12 (the project); week 15 is the final exams. Practice 1 and
  Online activity 7 (review) are linked for self-study before the midterm.
  The texts of weeks 5–14, with their links, are in `courses-private`
  (`moodle/digital-skills-weeks.md`).

## Lessons learned

- 2026-11-13 (syllabus v3, the teacher's request): the syllabus was rebuilt
  on the official course description (devices, communication and safety,
  content, data analysis, databases, a digital service, website design,
  e-marketing). Units 1–2 (taught) stay; Units 3–10 were rewritten for the
  nine teaching weeks left (plan v4, `plan.md`; progress in
  `plans/digital-skills-v3-status.md`): three pairs of syllabus rows are
  merged (4–5, 9–10, 12–13), and the course has 10 units and 2 practice
  weeks. New lectures: communication and collaboration (3), databases in
  Access (7), a digital service with Microsoft Forms (8), a website in Google
  Sites with a look at HTML and CSS (9), e-marketing with Canva (10); Word
  (4) and Excel (5–6) were kept. The course project (D1) runs through Online
  activities 9–12. The same day the teacher asked for the simplest possible
  course with no English writing (rule above, "As easy as possible").

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
- 2026-11-03 (the platform): the college was not ready in platform week 3
  (25/10/2026), so Lecture 1 was given on 1/11/2026, in platform week 4.
  Week 3 became a "getting ready" week; Lecture 1 and Online activity 1,
  with its submission, moved to week 4. The practice weeks absorb the lost
  weeks. The teacher set the rules for the weekly platform text (above,
  "On the e-learning platform").
- 2026-11-08 (teacher's request, later the same day): Unit 2 was all AI,
  which the students do not like, and writing prompts needs more English
  than they have. Unit 2 is now everyday skills that work on a phone, with
  AI as one third: Lecture 2 finds a fact on its official website (Search
  Lab, new), keeps the part of a screen that matters (Windows + Shift + S,
  the phone's keys, crop) and checks an AI draft and an AI total (Bill
  Check); Online activity 2 adds a reminder in the phone's calendar and a
  page scanned into a PDF, and the prompt step only asks the student to
  choose the missing part (Prompt Doctor). Its answers are files and single
  words. Weak Spots, Right Tool, Prompt Builder and Follow-up Chat stay in
  `week-02/sims/`, unused this semester. In every lecture, AI is a quarter
  to a third of the session, and no task asks for English text.
- 2026-11-08 (teacher's request): the labs are
  not ready, the classrooms have smart screens, and Lecture 2 felt
  theoretical and boring on the page. The course stays blended (the
  face-to-face version stays hidden). Lectures 2–10 now work with and
  without a lab: the page is taught on the screen in about 40 minutes
  (simulators of the Office tasks, prompts to copy into an AI assistant in
  another tab, one applied Try it per section), and the worksheet has Part A
  in the app and Part B on a simulator. Lectures 4, 5 and 9 joined two
  experiments (formatting and styles; rewrite and translate; safe prompts
  and the AI-use statement), and the notes of Lectures 4, 5, 6, 8 and 9
  joined the same sections. Online activities 3–13 got a model in each Step and simpler
  tasks (fixed data, fewer steps, one product each); Online activity 2,
  maybe open already, got the models only.
- 2026-11-10 (teacher's request): Online activity 2 is studied alone at
  home, and its Steps 1 and 2 are done on the phone, but they gave only
  text and one generic figure each. They now show the screens of the apps
  in two tabs, three drawn pictures in each (Android: Google Calendar and
  Google Drive; iPhone: Calendar and Files), with the data of the models
  (Huda's study group, Omar's math homework 3); the two generic figures
  were removed. The screens follow the official help pages and the iOS
  Simulator (iOS 26): the new event has the buttons ✓ and ×, no longer
  Add and Cancel; Drive scans from the camera button at the bottom right
  and asks for the name and for .pdf or .jpg; Files scans from its •••
  button and names the file Scanned Document, which the student renames.
  The other online activities get their screens when they are next written
  or rewritten (AUTHORING.md, "Screens of every app step"). Task 1 now asks
  for the screenshot only, with no file name: an iPhone cannot rename a
  screenshot in Photos (AUTHORING.md, "A task asks only for what the device
  can do").
