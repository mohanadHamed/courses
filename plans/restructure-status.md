# Restructure (plan v2): status on 2026-10-30 (end of the fourth session)

Branch `restructure-units` (signed commits, one per unit). Plan:
`plans/restructure-19-lectures.md`. Rules: `AUTHORING.md` and each course's
`NOTES.md` / `plan.md` / `schedule.yml`.

## The teacher's notes of 2026-10-30 (now rules in AUTHORING.md)

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

## Done

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

## Still to do

1. Push the two courses-private commits to its `main` (they exist only in
   the cloud session's clone).
2. The pull request into `main` (signed commits, no co-author lines); its
   description lists the removed games and the cut concepts for the
   teacher's review.
3. The teacher's review: one unit of each course in the browser
   (`quarto preview`), the open decisions of the plan, and the GIFs.

## How a unit was converted (Digital Media; use the same way)

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

## Tools

- Mac: Quarto is not installed locally (CI pins 1.10.19).
- Cloud session of 2026-10-30: Quarto 1.10.19 from the GitHub release;
  packages.typst.org is blocked there, so the Typst package
  `@preview/tiaoma:0.3.0` (QR codes) was copied from the typst/packages
  repository into `~/.cache/typst/packages/preview/tiaoma/0.3.0`; Chrome for
  the task PDFs and the package index: Playwright's `chrome-headless-shell`
  (`CHROME=…`), because the full Chromium hangs on Google services there;
  fonts: `fonts-noto-core`, as in CI.
