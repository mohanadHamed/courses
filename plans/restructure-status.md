# Restructure: status

Branch `restructure-units` (PR mohanadHamed/courses#25, signed commits). The
newest work is the **Digital Skills worksheets and online activities** below,
after **plan v3**; plan v2 (`plans/restructure-19-lectures.md`)
and its history follow at the end of this file.

## Digital Skills: lecture worksheets and varied online activities (2026-10-31)

The teacher's request (after plan v3, same branch and PR):

1. **Lectures 1–10 are built around a worksheet**, like the manual of a lab
   experiment: the goal (ILOs), what you need, start files (the same data
   for every student), 3–4 numbered experiments (one per section) with
   numbered steps and a place to record the result after every step, and a
   short table of results. Done and checked in class, never uploaded. The
   page shows the same experiments with "Check your result" after every
   step; the PDF has the results at the end. The notes become a short
   reference; the slides demonstrate the worksheet. Real apps, simulators or
   a mix, by lecture (`courses/digital-skills/plan.md`).
2. **Online activities 1–15 vary their content**: an interactive lesson,
   simulators only, a mix, an existing free video (official sources, linked,
   with title, source, length and the date checked) or a short video made for
   the course; every activity keeps its tasks to submit on Moodle, and its
   model answers in courses-private. The practice weeks add no new content.

### Design (decided 2026-10-31)

- `lesson-NN-sheet.qmd` (`lesson-typst`) → `digital_skills_lectureN_sheet.pdf`.
  `## Experiment N · title` with `**Aim:**` and 2–5 numbered steps; after each
  step `{{< record "label" >}}` and `::: {.check}`; `## Table of results` in
  `::: {.record-table}`; `start-files:` in the front matter (files in
  `week-WW/files/`, written by `tools/start_files.py`).
- The page reads the experiments from the worksheet (`{{< experiment N >}}`,
  `{{< experiment results >}}`, `{{< start-files >}}`): written once. Text
  fields keep what the student types in the browser (`lesson-script.html`).
- `book.lua`: results by step ("Experiment 2 · Step 3") on a new page;
  `banner.lua`: "Worksheet (PDF)" first on the page, goal card and QR card in
  the PDF; `shortcodes.lua`: course page "Worksheet" and "Notes" links;
  `download_names.py`, `course_package.py` (worksheet and start files), the
  CI output check, `check_size.py` (`check_sheet`), the templates
  (`sheet-template.qmd`), AUTHORING.md ("Lecture worksheets"), NOTES.md.
- Notes: each section ends with *In class: Experiment N of the worksheet, …*
  instead of a Lab task. Slides: Keywords, Before you start (figure
  `week-01/images/worksheet-steps.png`), Experiment N + Check N per
  experiment, Live demos, Game challenge + Try it, Table of results, Summary.

### Done

- Pipeline, rules and templates (see Design).
- Lecture 6 (model): `lesson-06-sheet.qmd` (four experiments in Excel with
  `shop-start.xlsx`; Formula Lab and Reference Lab as the demonstration),
  page, notes and slides (16) converted.
- The table of the 15 online activities in `courses/digital-skills/plan.md`
  (three of each type: lesson 5, 14, 15; sims 2, 3, 8; mix 7, 9, 12; video
  4, 10, 13; course-video 1, 6, 11) and the ten Microsoft Support videos
  (titles, pages, lengths; English captions read to check their content,
  2026-10-31). The teacher approved the design and the table (2026-10-31)
  and chose the tools for the course videos: **Mac tools, no install** (an
  HTML/SVG animation like the simulators, frames from headless Chrome, a
  voice-over with macOS `say` (Samantha), joined into an H.264/AAC MP4 by a
  Swift/AVFoundation script; A2 captions in the picture and a .vtt file).
- Lecture 1: three experiments (eight prices by hand with a stopwatch and
  with AutoSum, `prices-start.xlsx`; the apps of Microsoft 365 in the Start
  menu and at office.com; a first prompt, the same prompt twice, a question
  about made-up Sunrise Company, one tip rewritten in Word); 15 slides.
- Helper for the mechanical part of a conversion: `plans/helpers/sheet.py`
  (`page`: Lab task boxes → `{{< experiment N >}}`, Before you start, Table
  of results; `notes`: Lab task boxes → "*In class: Experiment N …*").
- Lecture 2: three experiments with an AI assistant (two good jobs: trip
  ideas and a summary of the library text printed in the worksheet, then a
  check for added facts; the weak spots: 12 pens against the calculator,
  three books searched in Bing, Weak Spots; the right tool: the library
  hours from the AI and from the university website, Right Tool); no start
  file; 14 slides.
- `shared/sims/recordings/make-video.swift`: the tested tool for the course
  videos (PNG frames + a voice-over → H.264/AAC MP4, macOS AVFoundation).

### Still to do (in this order; the next session starts here)

1. (done: the table and the video tool)
2. **Lectures 3, 4, 5, 7, 8, 9, 10** (1, 2 and 6 are done): worksheet, start
   files, page, notes, slides, one commit each, by the table "Lecture
   worksheets" in `courses/digital-skills/plan.md`. The recipe (Lectures 1,
   2 and 6 are the examples):
   a. Read the notes, the page and the slides. Write `lesson-NN-sheet.qmd`
      from `shared/templates/sheet-template.qmd`: one experiment per
      section, an Aim, 2–5 steps, a `{{< record >}}` and a `.check` after
      every step, the Table of results, the Game challenge line. Use other
      numbers than the Game challenge (its answers must not be in the
      worksheet) and fix the state between steps (undo, or say what is in
      the cells).
   b. Start files: an entry in `FILES` of `tools/start_files.py`, then run
      it (xlsx: sheets of rows; docx: plain paragraphs). Still missing in
      the tool: a `.pptx` writer for Lecture 8 (`talk-start.pptx`; for
      example `quarto pandoc` from Markdown) and a picture for Lecture 4
      (`park.png`: an SVG drawing exported to PNG, no photo).
   c. `python3 plans/helpers/sheet.py page …/lesson-NN.qmd [--files]` and
      `python3 plans/helpers/sheet.py notes …/lesson-NN-book.qmd "what
      experiment 1 does" …`; then by hand the intro paragraph of the page,
      the "You need" bullet of its Before you start, and the lead of the
      notes.
   d. Slides: Keywords; Before you start (picture
      `../week-01/images/worksheet-steps.png`); for each experiment
      "Experiment N · …" (columns: the idea in one sentence and three steps
      with their questions | the section's figure) and "Check N · …"
      (`.reveal`, one line per step); the Live demo slides of the page's
      simulators; Game challenge and its Try it (harder); Table of results
      (`.reveal`); Summary. At most 16 slides. `check_size.py` reads "work
      together" as group work: write "from one company" instead.
   e. `python3 _extensions/lesson/check_size.py --all | grep -E
      "week-WW|WARNING"`, then `quarto render courses/digital-skills/week-WW`
      and look at the worksheet PDF.
   f. One signed commit, this file updated, push.
3. **Online activities 1–15** by the table "Online activities" in
   `plan.md` (one commit each; solutions in courses-private
   `courses/digital-skills/week-WW/online-NN-solutions.md` when a task
   changes, pushed to `main`):
   - Pipeline first: `content:` in the front matter (lesson, sims, mix,
     video, course-video); `check_size.py` checks by type instead of
     `ONLINE_MIN_SIMS` (sims: a simulator in every Step; video: at least one
     `{{< watch >}}` with title, source, length and the date checked;
     course-video: the MP4, its captions and a poster exist); a
     `{{< watch >}}` shortcode in `shortcodes.lua` (an official video: a
     card that links the Microsoft Support page, never a copy; a course
     video: `<video>` with the MP4, a `.vtt` English track and a poster);
     a chip with the type in the hero (`banner.lua`); AUTHORING.md
     ("Blended courses") and NOTES.md ("Practical first: many simulators")
     say that the type decides the simulators.
   - sims (2, 3, 8): each Step one instruction, its simulator and its Try
     it; lesson (5, 14, 15) and mix (7, 9, 12): as now, with `content:`;
     video (4, 10, 13): Steps that follow the Microsoft videos of the plan
     (check each link again on the day); course-video (1, 6, 11): make the
     video, then Steps with the simulators.
   - Course videos (the teacher's choice: Mac tools, nothing to install):
     an HTML/SVG animation drawn like the simulators (generic windows, no
     logos, no screenshots), with a function that draws the picture at any
     time t, so the frames are exact; headless Chrome takes one PNG every
     1/30 s (as `record.ts` does with screenshots); the voice-over with
     `say -v Samantha -r 165` from a script in A2 English, `afconvert` to
     AAC; `shared/sims/recordings/make-video.swift` joins them (1280 × 720,
     about 1 MB a minute). A2 captions drawn in the picture and the same
     lines as a `.vtt` file. About 2 minutes each; files in
     `week-WW/videos/` (add the folder to the resources of `_quarto.yml`).
4. **Tasks with AI in all courses** (the teacher's request of 2026-10-31,
   see the next section): after steps 2 and 3, or in its own branch.
5. `check_size.py --all` and `check_figures.py` without warnings, a full
   `quarto render`, `tools/course_package.py`, the pages in the browser
   (this Mac has no Noto fonts: local PDFs use fallback fonts; CI has them).

### The teacher's request for the AI boxes (2026-10-31; not started)

The teacher checked the AI boxes of the site: they give an incomplete prompt
and ask the student to complete it. That is not right for basic students,
and many of them have never used AI to learn. In Game Math, Computing
Systems and Digital Media no ILO or PLO asks for AI: the AI boxes are an
**extra**, offered so that students meet AI as a modern way to learn. So
they must be as simple and as inviting as possible:

- **A complete prompt** in every AI box: all the details and numbers of one
  game or work situation, ready to copy and paste (the Copy prompt button
  stays). The student does not complete or design it.
- **A visual result:** the prompt asks the AI for something to look at, for
  example in a vectors lecture: "Draw a 2D grid; the player is at (2, 3) and
  the enemy at (6, 6); draw the vector from the player to the enemy as an
  arrow with its x and y parts, and label them" (a picture, a diagram, a
  chart, a small table, or a small web page that the AI makes).
- **Optional changes for the curious:** "Change the enemy to (8, 2) and ask
  the AI to draw it again. What do you notice?" (two or three changes of one
  number or one word), and the students' own ideas.
- **Collapsed expected answers:** after each "What do you notice?", a
  closed box with what the student should see (like "Check your result"), so
  the page still answers everything.
- No heavy check step before the student sees the result; keep it fun. A
  short reminder that AI can be wrong may stay, with the expected answer to
  compare.
- **Scope:** every AI box in every course: 19 boxes today (Game Math 12:
  Lecture 1 notes and page, Seminars 1, 5, 6, 7, 8, 9, 11, 12, Practice 2,
  and Homework 1; Computing Systems 4: Seminars 3, 7, 8, 12; Digital Media 3:
  Seminars 3, 4, 12). Digital Skills has no "Task with AI" box: there AI
  **is** in the ILOs (A1, B1, C4, D1), so its AI experiments and online
  tasks stay as they are (ask the teacher before changing them). Graded
  work (Homework 1 of Game Math, tasks to submit) keeps no answers: ask the
  teacher whether its AI box becomes the same kind of optional extra.
- **Pipeline to change** (then every box): AUTHORING.md ("Tasks with AI":
  the new model, the example box, "0–2 per session"); `check_size.py`
  (`ai_task_warnings`: a complete `.prompt`, the changes, a collapsed
  answer after each "What do you notice?"; no "Check:" step required
  outside graded work); a class for the changes and their answers (for
  example `::: {.try-change}` with a `.check` inside each change), rendered
  on the page as closed boxes (`match.lua`, `lesson.css`) and in the PDF at
  the end like the other results (`book.lua`); the templates; each course's
  NOTES.md ("Tasks with AI fit here when …").

## Plan v3 (teacher's request of 2026-10-31): core weeks and practice weeks

The teacher's notes:

1. **Every week is one lecture and one seminar** in Game Math, Computing
   Systems and Digital Media (the study plan: Game Math 2 theory + 1
   seminar, taught as 90 min + 90 min; the other two 1 theory + 1 seminar,
   60 + 60). Order: Lecture 1, Seminar 1, Lecture 2, Seminar 2, … The
   seminar of a week practises the lecture of the same week.
2. **Digital Skills is fully practical and blended** (study plan: 2 hours
   computer lab): every week a face-to-face lab lecture and a practical
   online activity (an interactive lesson or video with tasks submitted on
   the e-learning platform). It has no seminars.
3. **10–12 core weeks** with new lectures and seminars, so that holidays and
   absences leave room. The other weeks of the 15-week plan on the
   e-learning platform are **filling weeks** (on the site: *practice
   weeks*): revision, exams, an applied problem set, a case study, a
   practical lab, project presentations. They have **no new content**, so
   they can be skipped and nothing is missing for the students.

### Design (decided 2026-10-31)

- `schedule.yml`: `units:` lists the 15 weeks in teaching order. A core week
  is a unit (`unit: N`: Lecture N, Seminar N or Online activity N, Homework
  N). A filling week has `filling: true` and Practice N sessions (always
  flexible); exam-only weeks are not listed. `covers:` lists the other
  syllabus weeks of a merged unit (course package). Seminars are core.
- Course page: "Unit N" cards and "Practice week" cards (dashed, tagged
  Flexible). Banner: a practice session shows "Practice N · practises …" and
  "Flexible". Course package: a merged unit is listed in every syllabus row
  it covers; practice weeks fill their rows.
- **Game Math: 12 core weeks.** The two lectures of syllabus weeks 2, 3, 4
  and 11 are merged into one 90-min lecture (7 sections); the second
  application moves to the seminar of the week. Practice weeks: 8
  (Practice 1, revision of Lectures 1–7, before the midterm), 14 (Practice 2
  applied problem set, Practice 3 case study: movement of a 2D object) and
  15 (Practice 4 case study: random levels, Practice 5 course revision).
  Old → new lectures: 1→1, 2+3→2, 4+5→3, 6+7→4, 8→5, 9→6, 10→7, 11→8,
  12→9, 13+14→10, 15→11, 16→12, 17→Practice 3, 18→Practice 4, 19→Practice 5.
  Old → new seminars: 1→1, 2→5, 3→6, 4→7, 5→Practice 1, 6→8, 7→9, 8→11,
  9→12, 10→Practice 2; new Seminars 2, 3, 4 and 10. Homework 1–12 (old
  9–13 → 8–12; old 14 removed: no homework in a practice week).
- **Computing Systems: 12 core weeks.** Lectures 5 and 6 are merged
  (operating systems: processes, memory, files and devices; unit 5 covers
  syllabus weeks 5 and 6), Seminars 5 and 6 become one seminar with two
  activities. Old 7–13 → 6–12. Practice weeks: the midterm week (no
  session), Practice 1 (old Lecture 14: performance and compatibility case
  studies) and Practice 2 (old Seminar 14: project presentations).
  Homework 5 + 6 → 5; old 7–13 → 6–12.
- **Digital Media: 12 core weeks.** Lectures 12 and 13 are merged
  (intellectual property, licences, credits; unit 12 covers syllabus weeks
  13 and 14), Seminars 12 and 13 become one seminar with two activities.
  Practice weeks: the midterm week, Practice 1 (old Lecture 14: team
  workshop) and Practice 2 (old Seminar 14: team presentation). Homework
  12 + 13 → 12. D1 (team work) keeps a core part in the IP lecture and
  seminar.
- **Digital Skills: 10 core weeks** (Lectures 1–10, each with its online
  activity) and 5 practice weeks (Practice 1–5, lab practice with no new
  ideas, each with an online practice activity). Online activities keep
  their numbers 1–15 (one per week of the platform). Changes: Online
  activities 9 and 10 swap (the AI-with-PowerPoint activity goes to the
  PowerPoint unit; the five-slide talk to the practice week); a new
  Lecture 10 "Excel (3): Summarizing Data with AI Help" in week 13 from
  Practice 4 and Online activity 13 (PivotTables are new content, so they
  need a core lecture); old Lecture 10 (project presentations) becomes
  Practice 5; old Practice 5 becomes Practice 4.
- Helpers: `plans/helpers/qmd.py` (split a .qmd into level-2 blocks and
  join them again; used for the merges) and `plans/helpers/renum.py`
  (rename sessions with `git mv` and map "Lecture N", "Seminar N",
  "Homework N" references). The files as they were before plan v3 are at
  commit `0ae7d8d` (`git show 0ae7d8d:courses/…`).

### Done

- Pipeline: `shortcodes.lua` (course page: practice weeks), `banner.lua`
  (practice sessions flexible), `lesson.css`, `tools/course_package.py`
  (`filling`, `covers`).
- Game Math renumbering: lectures, seminars, practice sessions and homework
  renamed and every reference mapped; `schedule.yml` rewritten (15 weeks:
  12 units + 3 practice weeks).
- Game Math unit 2: Lecture 2 "Vector Operations and the Dot Product" (old
  2 + 3; 7 sections; old 2.5 speed folded into 2.4, the vision cone left to
  the Game challenge story and the seminar), new Seminar 2 "Vector Exercises
  in Game Scenarios" (Raft Rush crossing; a guard's vision cone with Dot
  Lab), Homework 2 unchanged.
- Game Math unit 3: Lecture 3 "The Cross Product, Distance and Projection"
  (old 4.1–4.4 and 5.1–5.3 with the wall slide; culling and rays cut from
  the lecture), new Seminar 3 "Solving Movement and Aiming Problems"
  (Asteroid Beam with along and across; a floor normal and the slide with
  Normal Lab), Homework 3 unchanged.
- Game Math unit 4: Lecture 4 "Trigonometry: the Unit Circle, Rotation and
  Oscillation" (old 6.1–6.4 and 7.1, 7.3, 7.4; Turn Lab replaced by a paper
  task in 4.5; the short turn cut), new Seminar 4 "Trigonometry in Game
  Motion" (aim with atan2 in Turn Lab; an orb and Sky Lift), Homework 4
  unchanged.
- Game Math unit 10: Lecture 10 "Probability: Events, Conditional
  Probability and Expected Value" (old 13.1–13.5 with independence, 14.1
  with the multiplication rule, 14.3 with fair games and 1/p; Treasure Odds
  as the Game challenge), new Seminar 10 "Probability in Loot Drops and
  Critical Hits" (three short activities: theory and many rolls in Roll Lab,
  the old 13.6; a critical hit with a known first die and a chest, with
  Conditional Lab; a crate's expected value and fair price in Crate Lab),
  Homework 10 unchanged. Raft Odds and the figure `large-numbers` removed;
  Lecture 11 refers to Seminar 10 for many tries.

- Game Math practice weeks and the rest of the course: Seminar 12 has a
  D1 part (a reply to a player, presented alone, 18 min; 56 planned
  minutes); Practices 1 and 2 relabelled; Practices 3, 4 and 5 (old
  Lectures 17–19) rewritten in the practice format (three short activities
  each, 59–60 planned minutes, worksheets made with `mkbook.py`, the team
  activity in the worksheet of Practice 3); the course maps (`course-map`,
  `course-map-all`) and the matrix figure show the new lecture numbers;
  Fair Speed and the figures no session uses removed; `index.qmd`,
  `plan.md` and `NOTES.md` describe the 12 units and 3 practice weeks.
  `check_size.py` gives no warning for Game Math.

- Computing Systems (plan v3 done): Lecture 5 "Operating Systems:
  Processes, Memory, Files and Devices" (old 5.1–5.3, old 6.1 with the
  essentials of 6.2; Pocket Quest and RAM Rush as the Game challenge; 4
  sections, 16 slides), Seminar 5 "Operating-System Tour and File and
  Resource Management" (the Windows tour of old Seminar 5 and the device
  check of old Seminar 6 with Test Day), Homework 5 (old 5 task 1 and old 6
  task 1); old 7–13 renamed 6–12 with all references; Lecture 14 rewritten
  as Practice 1 (two case studies with Performance Detective and
  Compatibility Lab), Seminar 14 relabelled Practice 2; week-06 removed
  (its figures and Test Day moved to week-05); Settings Explorer, Name
  Checker, Disk Doctor and four unused figures removed; `schedule.yml`,
  `plan.md`, `NOTES.md`, `index.qmd`. `check_size.py`: no warning.

- Digital Media (plan v3 done): Lecture 12 "Intellectual Property:
  Copyright, Licences, Fair Use and Credits" (old 12.1 with 12.2, 12.3 with
  13.2, 12.4, and 13.1 + 13.3 + 13.4 as section 12.4; Can We Use It? as the
  Game challenge; 4 sections, 27 questions, 15 slides), Seminar 12
  "Intellectual-Property Issues and a Licence Audit" (the rights check of
  old Seminar 12 and the audit of old Seminar 13, with the AI audit at
  home), Homework 12 kept (due one week after Lecture 12; old Homework 13
  dropped); week-14 removed (its figures, Credit Builder and Audit Board
  moved to week-13); Lecture 14 rewritten as Practice 1 (the Storm Night
  package planned and checked; the team activity in the worksheet),
  Seminar 14 relabelled Practice 2; Asset Shopping, IP Desk, Audit Fixes,
  Workshop Day and unused figures removed; `schedule.yml`, `plan.md`,
  `NOTES.md`, `index.qmd`. `check_size.py`: no warning.

- Digital Skills (plan v3 done): new Lecture 10 "Excel (3): Summarizing
  Data with AI Help" in week-13 (three sections: totals by group with a
  PivotTable, other questions with weeks, averages and a chart, an AI
  summary checked number by number; Pivot Lab and Summary Check; Huda's
  April meeting as the Game challenge; notes, page and 14 slides); old
  Practice 4 removed (its content is Lecture 10); Online activities 9 and
  10 swapped with their sims and figures (Outline Lab and Image Prompt Lab
  to week-09, Talk Planner and Rehearsal Lab to week-10; Rehearsal Lab loads
  `slide-kit.js` from week-09); old Lecture 10 rewritten as Practice 5 (five
  slides and four checks with Deck Checker; rehearse with Rehearsal Lab);
  old Practice 5 renamed Practice 4; dues of Online activities 13–15 and
  the project figure updated; Presentation Day and one figure removed;
  `schedule.yml` (10 units, 5 practice weeks), `plan.md`, `NOTES.md`,
  `index.qmd`. `check_size.py --all`: no warning in any course.

- Rules: `AUTHORING.md` ("Courses", "Units and sessions", "Mapping the
  syllabus week", "What a seminar looks like", "Blended courses",
  "Homework", "Course pages and the schedule", "The course package", a
  lessons-learned entry of 2026-10-31) and the seminar and homework
  templates describe core weeks and practice weeks.

- courses-private (pushed to `main`, commit 9d91bfb): homework solutions
  renamed, merged and removed to match the new homework; the online
  solutions 9 and 10 swapped; dues of the online activities 13–15; the
  Moodle week maps of the four courses show the 15-week plan (units,
  practice weeks, midterm) and have an Arabic text for a practice week.

- Build and check (2026-10-31, on the Mac, Quarto 1.10.20): a full
  `quarto render` (one error fixed: two figures labelled `fig-tree` in the
  merged Game Math Lecture 10 notes), then 147 session pages, 147 PDFs and
  96 slide decks with their download names; no notes PDF or worksheet shows
  `Why:` or `:::`. `tools/course_package.py`: the four packages with every
  syllabus row filled (merged units in both rows, practice weeks in theirs),
  no session left over. Browser (local server on port 4321): the four course
  pages show the units and the practice weeks, every session ready; 147
  pages, 231 embedded simulators and 1,219 links and files load; the moved
  simulators load all their scripts; two wrong tries show the answer with
  its reason. Fixes found by the check: Seminar 2's list of wrong answers,
  and the practised lectures of Game Math Practices 3 and 4. The Mac has no
  Noto fonts, so local PDFs use fallback fonts (CI installs Noto).

### Still to do (in this order)

1. **Game Math:** done (see above).
2. **Computing Systems:** done (see above).
3. **Digital Media:** done (see above).
4. **Digital Skills:** done (see above).
5. **Rules:** done (see above).
6. **courses-private:** done (see above).
7. **GIF recordings:** none needed: the new seminars and practice sessions
   reuse simulators that already have GIFs, and no simulator changed its
   look (`check_size.py` reports no slide without a recording).
8. **Build and check:** done (see above).
9. **The teacher's review** on localhost (`quarto render`, then `quarto
   preview`, or `python3 -m http.server 4321 --directory _site`), then the
   merge of PR #25.

---

## History: plan v2, status on 2026-10-30 (end of the fourth session)

Branch `restructure-units` (signed commits, one per unit). Plan:
`plans/restructure-19-lectures.md`. Rules: `AUTHORING.md` and each course's
`NOTES.md` / `plan.md` / `schedule.yml`.

### The teacher's notes of 2026-10-30 (now rules in AUTHORING.md)

1. **Lessons as simple as the outcomes allow**: the estimated limit (about
   30 % simpler than October 2026), only the simplest concepts that reach
   every ILO at its Bloom level; A2–B1 English in the notes, A2 on pages and
   slides. Applied to all work done since; lectures finished before
   2026-10-30 (Game Math, Computing Systems, Digital Media 1–4) were not
   simplified again (a possible later pass).
2. **Seminars short**: two short problems (three at most) that together use
   every concept of the lecture they practise; planned time (Recall 5 min +
   the "· N min" of the activity boxes) at most 40 of 60 min and 60 of 90
   min, the rest for the teacher's explanations; no Game challenge or case
   study in a seminar (a game is the tool of an activity); a Task with AI
   only as an optional `## At home · Task with AI`; worksheet = Recall, the
   activities, 3–5 exercises. `check_size.py` checks all of this
   (`SEMINAR_SIZES`, `SEMINAR_TIME`, `SEMINAR_FORBIDDEN`). Templates in
   `shared/templates/seminar-*` follow it.

### Done

- Steps 1–2 of the plan (pipeline, rules, schedules, plans).
- **Game Math: all 15 units**; **Computing Systems: all 14 units**
  (lectures, seminars, homework); all their seminars **shortened** to the
  new model (CS 35–38 min planned, GM 50–59 min).
- **Digital Media: all 14 units** (Lectures 1–14, Seminars 1–14, homework
  1–13; unit 14 has the project instead of homework), in week-01 … week-07
  and week-09 … week-15. Seminars 1–3 were shortened; 4–14 written short.
  Unit 14: Lecture 14 from old 27 with the quality criteria of old 28.1 in
  section 14.4 (the brief as pass or fail, five criteria scored 1–4 with
  evidence, the fails fixed first by their owners); core Seminar 14 from
  old 28 as two short problems (Package Review of Team Blue; a six-minute
  talk plan in Package Talk Planner); the team activity (D1) with its
  individual alternative only in the notes of Lecture 14 and the worksheet
  of Seminar 14; the action-list priorities (must, should, could) cut;
  feedback in three parts refers to Lecture 9. Cut as planned: channels and
  inside/outside the world (Seminar 1 had added them), the 180-degree rule
  and camera map, 65 536 levels and file-size sums, the BPM formula, Unity
  code and the Audio Mixer, 370 MB/s and the bitrate formula, patents,
  trade secrets and "life + 70" sums, code licences (MIT/GPL). Moved: the
  editing basics of old 20 (tracks, split, trim, ripple delete) into
  Lecture 11.1; the rights check of old 24.2 into Lecture 13.4; feedback in
  three parts into Lecture 9.4; owners and "inspired or copied" into
  Lecture 12. Homework 7, 8, 10, 11 and 13 rewritten so that they practise
  their lecture only (solutions updated and pushed in courses-private).
  The L19 reference (raster images = Lecture 1) is fixed.
- Seminar-only games removed (their Game challenge is gone): CS Test Lab,
  Spec Match, Phone Picker, Help Ticket, Power Lab, Two Phones, Port
  Planner, Report Doctor, Talk Doctor; GM Harbor Guard, Sky Steps, Cannon
  Cove, Island Quest, Difficulty Tuner, Problem Drill, Star Dock Missions;
  DM Sound Stage, Ember Trail, Curve Builder, Premise Doctor, Voice Match,
  Board Builder, Panel Composer, Clean Take, Critic's Choice, Editor Tour,
  Promo Judge, Public Domain Clock, Feedback Desk; and the figures no
  session uses. GM
  Seminar 9 no longer adds expected attacks or input/output randomness
  (not in Lecture 16). Old lecture numbers removed from several sims.
- `record-all.sh`: stale paths fixed, deleted sims and their scenarios
  removed.
- **Digital Skills: all 15 units** (Lectures 1–10, Practice 1–5 in the short
  seminar format, Online activities 1–15 as `online-NN.qmd`), one commit per
  unit. Details and the lists of removed and new simulators, cut concepts and
  the course project: the lessons-learned entry of 2026-10-30 in
  `courses/digital-skills/NOTES.md`. Unused sims and figures removed (also
  `pictures` of week 9 and `format-table` of week 13).
- **Course pages** (`index.qmd` of the four courses) describe units, not
  weeks or pairs of lectures; the CI output check knows the new file names
  (seminar, practice and online PDFs).
- **GIFs and posters (step 2):** all 43 sims of the old list and the changed
  Digital Skills sims recorded again (Rehearsal Lab got a scenario; Link Lab's
  was removed); posters of Drawbridge and Stack Builder made again. Recorded
  in the cloud with Playwright and PIL, the same scenarios and settings as
  `record-all.sh` (600 px, `?fixed-order`, 560 px GIF); running
  `record-all.sh` on the Mac makes them again the usual way (Deno, Swift).
- **Browser check:** all 154 session pages of the rendered site opened in
  Chromium (phone width) with their 240 simulators loaded: two problems,
  both fixed (Digital Media Cut Lab and Effects Lab loaded `scene.js` from
  week 10, where it no longer is; a `$` on Online activity 8 started a
  formula). On six pages of the four courses: two wrong tries show the
  right answer with its reason, a right answer shows its reason, and "Check
  your result" opens.
- **courses-private (step 3):** `online-NN-solutions.md` for Online activities
  1–15 (old `lesson-2W-solutions.md` renamed and updated where the tasks
  changed: 7, 8, 9, 11, 14, 15; the stale homework-1 solution removed) and
  `moodle/<slug>-weeks.md` for the four courses (the official map and the
  Arabic texts: introduction, review before the midterm, midterm, catch-up
  week, final review, final exam; no "lab" word in Digital Skills).
  **Committed in the session's clone, not pushed yet** (pushing to `main`
  of courses-private needs the teacher's permission in this environment).
- **Render and package (step 4):** a full `quarto render` (Quarto 1.10.19,
  cloud session): 360 files, 100 slide decks, 54 homework and online-task
  PDFs, 254 renamed downloads, no errors. It showed 19 results in the Game
  Math notes of Lectures 9–12 printed as text (no blank line before
  `{.check}`; Lecture 9 had no results section): fixed, and `check_size.py`
  now warns about a fenced div right after text. `tools/course_package.py`:
  the four packages (week-01 … week-16, `index.html`, `index.pdf`), every
  syllabus row with its material, no session left over. The task PDFs show
  only the tasks, and no notes PDF or worksheet shows `Why:` or `:::`.
- `check_size.py --all`: no warnings in any course. `check_figures.py`: no
  warnings.

### Still to do

1. Push the two courses-private commits to its `main` (they exist only in
   the cloud session's clone).
2. The pull request into `main` (signed commits, no co-author lines); its
   description lists the removed games and the cut concepts for the
   teacher's review.
3. The teacher's review: one unit of each course in the browser
   (`quarto preview`), the open decisions of the plan, and the GIFs.

### How a unit was converted (Digital Media; use the same way)

For a team or project unit (D1), write the team activity box only in the
notes of the lecture and in the worksheet of the seminar (add it by hand
after `mkbook.py`, before "## Exercises"), each with an individual
alternative and a `.check`.

1. `git mv` the old files: the first old lesson → `lesson-NN*` (Lecture
   N), the second → `seminar-NN*`.
2. `python3 plans/helpers/conv.py renumber FILE OLD NEW` on the three
   lecture files; `conv.py intro PAGE` on the page.
3. Cut what the plan lists; fix old lecture numbers; put the essentials of
   the second old lesson into the lecture where the homework or the next
   lecture needs them.
4. Reasons: `conv.py whys PAGE REASONS` (one line per `:   answer`, in
   order); results: `conv.py checks FILE CHECKS` ("=== Do it · title" then
   the text) on the page and on the notes.
5. Seminar: write the page by hand (template), then
   `python3 plans/helpers/mkbook.py PAGE SPEC` makes the worksheet (SPEC:
   the lead, a line "===", then "1. exercise | answer" lines); write the
   slides by hand.
6. Homework: due "before lecture N+1", the line "You may use AI where a
   task says so…", only the lecture of its unit; update the solution in
   courses-private (commit on main, push).
7. `python3 _extensions/lesson/check_size.py --all | grep week-WW`: no
   warnings; check for missing figures; remove sims and figures that no
   session uses (and their lines in `record-all.sh` and their scenarios).
8. One unit per commit (signed; the message describes the change).

### Tools

- Mac: Quarto is not installed locally (CI pins 1.10.19).
- Cloud session of 2026-10-30: Quarto 1.10.19 from the GitHub release;
  packages.typst.org is blocked there, so the Typst package
  `@preview/tiaoma:0.3.0` (QR codes) was copied from the typst/packages
  repository into `~/.cache/typst/packages/preview/tiaoma/0.3.0`; Chrome for
  the task PDFs and the package index: Playwright's `chrome-headless-shell`
  (`CHROME=…`), because the full Chromium hangs on Google services there;
  fonts: `fonts-noto-core`, as in CI.
