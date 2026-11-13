# Digital Skills on syllabus v3: rewrite of Units 3–10 — status

**Resume here.** Branch `claude/happy-volta-gzvzrv` in both repos
(`courses` and `courses-private`). One commit per finished unit, pushed at
once. A new session reads this file, `courses/digital-skills/plan.md` (the
map) and `schedule.yml`, then continues with the first unchecked item of
"Progress".

## The request (2026-11-13)

The teacher rebuilt the syllabus (v3, 13/11/2026) on the **official course
description** of the study plan: the concept of digital skills and the
labour market; digital devices and technologies; digital content creation;
creating a digital service; marketing digital services; with databases,
website design, data analysis and e-marketing. (v2 was Office and AI.) The
attachments were the English syllabus and its Arabic copy (the same
content); only the ILO text goes into this repo.

- **Do not change Units 1 and 2** (taught). Rewrite every unit from Unit 3
  on, so that the ILOs left are covered in the weeks left.
- **Keep the number of units (10).** Unit 3 is taught in the week of Sunday
  15/11/2026; the last teaching week is 10–14/1/2027 (Sunday to Thursday);
  the finals start the week after. So nine teaching weeks are left: Units
  3–10 (8) and one practice week.
- Store every unit as it is finished, on a feature branch, with this file.

## Decisions (plan v4, see `plan.md`)

- 10 units and **2 practice weeks** (row 8: review; row 15: the project
  presentations), 12 weeks in all; Online activities 1–12. Three pairs of
  syllabus rows are merged: 4–5 (Unit 4: Word lecture, PowerPoint online),
  9–10 (Unit 7: databases), 12–13 (Unit 9: website). The Canva graphic and
  picture copyright of row 5 go into Online activity 11 (the promotional
  post).
- Week folders: week-03 U3, week-04 U4, week-06 U5, week-07 U6, week-08 P1,
  week-09 U7, week-11 U8, week-12 U9, week-14 U10, week-15 P2. The old
  folders week-05, week-10 and week-13 go (their reusable parts move first).
- Reused from plan v3: Lecture 4 (Word), Lectures 6–7 (Excel) as Lectures 5–6,
  Online activity 6 (budget) as 5, the PowerPoint simulators of old Lecture
  8 in Online activity 4, the PivotTable of old Lecture 10 and Online
  activity 13 in Online activity 6, Share Settings (old Online activity 3)
  in Lecture 3, the review quiz (old Online activity 8) as 7.
- **The course project (D1)** is built in the core: Online activities 9, 10
  and 11 (form, website, post and plan for one of four given services), then
  Online activity 12 and Practice 2.
- Units 1–2 files are not touched. Their ILO codes stay as written (Unit 1:
  A1; Unit 2: A1, C4): the codes exist in v3, but the banner of Unit 2 now
  shows the v3 text of C4 (the digital service). **For the teacher:** if
  wanted, change `ilos:` to `[C1]` in `week-01/online-01.qmd` and to
  `[A2, C1]` in the four `week-02` files (front matter only).

## The teacher's second message (2026-11-13, same day)

Make the course **as easy as possible**: the students come from every
diploma, most have no IT background and weak computer skills. Cover each
ILO at the minimum. **No English writing at all** (no e-mail or text to
write): very short words; answers by choosing (multiple choice), matching,
ordering, sorting, or a letter or a number. The pipeline already says this
for Digital Skills (NOTES.md, AUTHORING.md "Answers without written
English"); every unit below follows it strictly. A task in an app may ask
the student to type a short given text (a title, a file name), never their
own sentences.

## Progress

- [x] Plan: `schedule.yml`, `_metadata.yml` (v3 ILOs and tagline), `plan.md`, this file.
- [x] Unit 3 (week-03): Lecture 3 communication (sheet, page, notes,
      slides; Mail Lab, Meeting Planner, Share Settings; game Team Desk;
      start file `agenda-start.docx`), Online activity 3 safety (Password
      Check, Phish Finder; screens of two-step sign-in, a link, Report
      phishing and app permissions in `tools/phone_screens.py`); solution;
      platform week 6. check_size clean; all four outputs and the online
      page render; the tasks print on one A4 page.
- [x] Unit 4 (week-04): Lecture 4 Word (new title, ILO C2, a Save As PDF
      step in Experiment 3; Format Lab left only in the notes and slides so
      the page is 40 minutes); Online activity 4 PowerPoint (Slide Builder
      with "Use the given text" buttons, Slide Doctor, layouts/themes/text
      figures, copied from old week-09; screens of New Slide, Design and
      Stock Images); solution; platform week 7.
- [x] Unit 5 (week-06): old Lecture 6 → Lecture 5, old Online activity 6 → 5 (still in BEFORE_SCREENS: no app screens yet); old week-05 pages removed; platform week 8.
- [x] Unit 6 (week-07): old Lecture 7 → Lecture 6; Online activity 6
      PivotTable (start file `training.xlsx`, screens, Pivot Lab and Chart
      Lab); old Online activity 7 removed; platform week 9.
- [x] Practice 1 and Online activity 7 (week-08): review of Lectures 1–6 (Activity 1 a Word notice e-mailed as a PDF; the new Review Quiz).
- [x] Unit 7 (week-09): Lecture 7 databases (Access; Field Lab, Key Lab,
      Query Lab, game Data Desk; no start file); Online activity 8 (Form Lab,
      Query Lab, Report Lab; screens of Access; tasks on the simulators,
      letters only); old PowerPoint pages of week-09 removed; platform week 10.
- [x] Unit 8 (week-11): Lecture 8 digital service (Service Sorter, Service
      Planner, Form Builder, game Service Desk; `service-plan-start.docx`);
      Online activity 9 (the four project services A-D with their form
      questions; screens of Microsoft Forms; link, two screenshots, letters);
      old week-11 pages removed; platform week 11.
- [x] Unit 9 (week-12): Lecture 9 website (Google Sites; Site Planner,
      Design Check, HTML Lab, game Web Desk; start file `files/page-start.html`
      written by hand, not by start_files.py); Online activity 10 (the given
      text of the four project sites; screens of Google Sites; the web
      address and a phone screenshot); old Practice 3 pages removed;
      platform week 12.
- [x] Unit 10 (week-14): Lecture 10 e-marketing (one AI prompt; a search;
      Canva; simulators on one engine `sims/quiz-kit.js`: Message Builder,
      Channel Mixer, Results Reader; game Market Desk); Online activity 11
      (Product Page Lab, Picture Rights, Plan Builder; screens of Canva; the
      post PNG and letters); old week-13 and week-14 pages removed;
      platform week 13.
- [x] Practice 2 and Online activity 12 (week-15): the project check and
      the three-slide talk; the final submission (Project Checker on
      quiz-kit; PowerPoint screens of week-04); old week-10 and week-15
      practice pages removed; platform week 14 and the new mapping.
- [ ] Clean-up: the hidden face-to-face version (`face-to-face/`) uses the
      old simulators and images of week-03 to week-15 (`../../week-WW/...`):
      keep those files; delete only the old blended `.qmd` files that no
      session uses any more (week-05, week-10, week-13 and the old ones in
      reused folders); `check_size.py` lists (`BEFORE_SCREENS`); NOTES.md, the course
      `index.qmd`, AUTHORING.md (the course table and "Mapping the syllabus
      week"); `glossary.yml`; `courses-private`: `syllabus-weeks.yml` (v3
      table, word for word), the solutions, the platform texts (weeks 6–14).

## How each unit is checked

- `python3 _extensions/lesson/check_size.py --all` (no warning for the unit).
- `quarto render` of the unit's files (page, notes, worksheet, slides, online
  activity), then a look at the page in Chromium (Playwright).
- Posters: `quarto typst compile` of the SVG (shared/sims/README.md).
  Recordings (GIF): `plans/helpers/record_gif.py` (Playwright and Pillow;
  the macOS pipeline in `shared/sims/recordings` needs Swift).

## Helpers written in this rewrite (`plans/helpers/`)

- `svgkit.py`: a small SVG kit for figures and posters; `figs_u3.py` draws
  the figures and posters of Unit 3 (one such script per unit).
- `export_png.py`: SVG → PNG with Liberation Sans (no Helvetica here).
- `record_gif.py`: the GIF of a simulator from its line in
  `shared/sims/recordings/record-all.sh` and its scenario (Node Playwright
  with `NODE_PATH=/opt/node22/lib/node_modules`, Pillow).
- Tasks PDF check: print the rendered online page to A4 with Playwright
  (`page.pdf`) and count the pages (one page).
- Render with `HOMEWORK_PDF=off` (its Chrome print hangs here); check the
  tasks print with Playwright instead.
- Pandoc reads `@Name` and `**@**` as citations: write `\@Omar`, `**\@**`.
