# Restructure (plan v2): status on 2026-10-30 (end of the third session)

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
- `check_size.py --all`: no warnings outside Digital Skills (87 warnings
  there, all from the old structure). `check_figures.py`: no warnings.

## Still to do (in this order)

1. **Digital Skills, 15 units** (all still old `lesson-01 … lesson-30`):
   map in the plan, Part 3 (Lectures 1–10 core, Practice 1–5 flexible in
   the short seminar format `practice-NN*`, Online activities 1–15 as
   `online-NN.qmd` that practise their unit and never repeat the lecture;
   at least 2 sims each; AI-use statement from unit 11; the course's
   NOTES.md: A2 English, general examples, never games). Model answers of
   the online activities go to courses-private
   (`courses/digital-skills/week-WW/online-NN-solutions.md`). Fix the sims
   `office-relay.html` ("(lecture 23)") and `presentation-day.html`
   ("lecture 30"). `schedule.yml` is already in the new format. Each
   `week-WW` holds old `lesson-(2W−1)*` (the face-to-face lesson, three
   files) and old `lesson-2W.qmd` (the online activity, `online: true`):
   the first becomes `lesson-NN*` or `practice-NN*`, the second
   `online-WW.qmd` (templates in `shared/templates/`).
2. **GIFs and posters** for changed sims (`sh shared/sims/recordings/record-all.sh
   <name>`; needs Quarto's Deno, not installed here): game-math week-04
   drone-drop, sky-lift; week-06 drawbridge (poster too); week-10
   rule-smith; week-11 treasure-odds; week-12 loot-forge; week-13
   fair-or-frustrating, bag-lab; week-14 pilot-check, move-lab, bounce-lab;
   week-15 cave-gen, generator-doctor, raft-finals; computing-systems
   week-04 soc-explorer (text); week-05 ram-rush; week-06 disk-doctor,
   test-day (text); week-07 stack-builder (poster too), pause-please
   (text); week-09 launch-planner, source-check, platform-pick,
   fact-or-myth; week-10 launch-day, review-board (text); week-11
   terminal-lab, lag-detective, net-fixer; week-12 cloud-planner; week-13
   lag-lab (labels); week-15 slide-sorter; digital-media week-05
   shot-caller (last round); week-07 waveform-lab (readout); week-09
   score-the-scene (tempo round), loop-doctor (text); week-11 export-desk
   (bitrate round), video-settings-lab (readout), timeline-lab (end
   message); week-14 asset-shopping, audit-board, audit-fixes (one round
   or row each); week-15 workshop-day (the loop explanation). Test each
   sim inside its page in the browser (no JS check was possible here).
3. **courses-private**: the online-activity solutions of Digital Skills,
   and `moodle/<slug>-weeks.md` (Arabic section texts; no "مختبر" for
   Digital Skills).
4. Full `quarto render`, `python3 tools/course_package.py`, then a PR into
   main (signed commits, no co-author lines). In the PR description, list
   the removed games and the cut concepts above for the teacher's review.

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

## Tools on this Mac (2026-10-30)

- Quarto is **not installed** locally (CI pins 1.10.19), so no render and
  no GIF recordings. SVG figures can be exported to PNG with headless
  Chrome (installed) at scale 200/96.
