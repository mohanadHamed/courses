# Restructure (plan v2): status on 2026-10-29

Branch `restructure-units` (signed commits, one per unit). Plan:
`plans/restructure-19-lectures.md`. Rules: `AUTHORING.md` and each course's
`NOTES.md` / `plan.md` / `schedule.yml` (all already updated in step 2).

## Done

- Step 1, pipeline (filters, scripts, templates, `tools/course_package.py`).
- Step 2, rules, schedules, plans for all four courses.
- **Game Math: all 15 units** (Lectures 1–19, Seminars 1–10, homework 1–14),
  `check_size.py` clean.
- **Computing Systems units 1–6** (Lectures 1–6, Seminars 1–6, homework 1–6).
- courses-private (pushed on main): `syllabus-weeks.yml` ×4; solutions of Game
  Math homework 1–14 and Computing Systems homework 1–6 match the new tasks.

## In progress: Computing Systems unit 7 (week-07)

- Done: `lesson-07.qmd` and `lesson-07-book.qmd` (from old 13: HAL, ART, XNU
  and Unity callbacks removed; the life-cycle example changed so it does not
  repeat the Pause, Please! challenge).
- To do: `lesson-07-slides.qmd` (from `lesson-13-slides.qmd`: subtitle
  "Lecture 7", sections 13.x → 7.x, remove the HAL/ART/Core OS bullets and
  the HAL and OnApplicationPause answers, replace "Example · A call in level 3"
  with Sara's message in level 2); Seminar 7 (`seminar-07.qmd`, `-book`,
  `-slides`) from old lecture 14 (fix the Do it "Compare with a classmate" →
  "check the maker's update page"); homework 7 (due "before lecture 8", AI
  line, Lecture 7 only); then delete `lesson-13*` and `lesson-14*` in week-07.

## Still to do

1. **Computing Systems units 8–14.** First shift the folders: units 8–14 live
   in syllabus weeks 9–15, so `git mv week-14 week-15`, … , `week-08 week-09`
   (from the top down). Old `lesson-02-old*.md` (old 2.3 cloud gaming, Lag Lab)
   is stashed in week-13 for Lecture 12 (it moves to week-14 with the shift;
   Lecture 12 belongs in week-13; also fix "cloud gaming adds about 50 ms" to
   match Lag Lab +120/+220 ms). Lag Lab sim files are still in week-01/sims.
   Per unit k: old lecture 2k−1 → Lecture k (plus the parts the plan names),
   old 2k → Seminar k; cuts and fixes are listed in `plan.md` and in the plan
   (L15 "Ask a classmate"). Unit 14: no homework (project).
2. **Digital Media** (14 units, same pattern; fixes: L2 diegetic rule, L19
   reference) and **Digital Skills** (15 units: Lectures 1–10, Practice 1–5,
   Online activities 1–15 that practise their unit; see its NOTES.md).
3. Every page: `Why:` under every Try it answer, `::: {.check}` in every
   Do it / Lab task / Activity; seminars in the seminar format (templates in
   `shared/templates/seminar-*`); case studies must not repeat the numbers
   of worked examples (change the sim or the example).
4. **GIFs and posters** for changed sims: run
   `sh shared/sims/recordings/record-all.sh <name>`. First fix the stale
   paths in `record-all.sh` (many sims moved folders). Changed sims:
   game-math week-04 drone-drop, sky-lift; week-06 sky-steps, drawbridge
   (posters too); week-08 island-quest; week-10 rule-smith; week-11
   treasure-odds; week-12 loot-forge; week-13 fair-or-frustrating, bag-lab;
   week-14 pilot-check, move-lab, bounce-lab, star-dock-missions,
   problem-drill; week-15 cave-gen, generator-doctor, raft-finals;
   computing-systems week-04 phone-picker, soc-explorer; week-05 ram-rush;
   week-06 disk-doctor. Test each sim inside its page in the browser
   (no JS syntax check was possible).
5. courses-private: renumber the remaining solutions (Computing Systems 7–13,
   Digital Media, Digital Skills online activities) and write
   `moodle/<slug>-weeks.md` (Arabic section texts; no "مختبر" for Digital
   Skills).
6. Full `quarto render`, `python3 tools/course_package.py`, then a PR into
   main (no co-author lines; signed commits).

## Helpers (recreate if the scratchpad is gone)

- add_why.py FILE MAP: MAP lines "question start<TAB>reason"; inserts
  `    Why: reason` under each matching answer.
- add_check.py FILE MAP: MAP blocks "=== Box title" + text; adds a `.check`
  at the end of that box.
- Check sizes: `python3 _extensions/lesson/check_size.py --all | grep <path>`.
