# Restructure (plan v2): status on 2026-10-30

Branch `restructure-units` (signed commits, one per unit). Plan:
`plans/restructure-19-lectures.md`. Rules: `AUTHORING.md` and each course's
`NOTES.md` / `plan.md` / `schedule.yml` (all already updated in step 2).

## Done

- Step 1, pipeline (filters, scripts, templates, `tools/course_package.py`).
- Step 2, rules, schedules, plans for all four courses.
- **Game Math: all 15 units** (Lectures 1–19, Seminars 1–10, homework 1–14),
  `check_size.py` clean.
- **Computing Systems: all 14 units** (Lectures 1–14, Seminars 1–14, homework
  1–13; unit 14 has the project), in week-01 … week-07 and week-09 … week-15;
  `check_size.py` clean.
- Review of the finished units (2026-10-30): unclosed Try it boxes (Seminars 5, 6),
  ILOs and titles as in the syllabus, reuse notes, unit 7 figures and Stack Builder
  without HAL/ART/XNU; `game-kit.js` mixes the answer buttons (the right answer
  was always first); recordings open sims with `?fixed-order`.
- courses-private (pushed on main): `syllabus-weeks.yml` ×4; solutions of Game
  Math homework 1–14 and Computing Systems homework 1–13 match the new tasks
  (CS solutions in week-09 … week-14 since the shift).

- **Digital Media units 1–3** (Lectures 1–3, Seminars 1–3, homework 1–3); units
  8–14 already moved to week-09 … week-15 (both repos). DM keeps one running
  story per lecture (Skyward Kite, Silent Station, …): the audit flagged
  repeated case numbers only in Game Math and Computing Systems.
- Helper `conv.py` (scratchpad): renumber, fix_intro, add_whys, add_check.

## Still to do

1. **Digital Media units 4–14** (same pattern; fix: L19 reference) and **Digital Skills** (15 units: Lectures 1–10, Practice 1–5,
   Online activities 1–15 that practise their unit; see its NOTES.md).
2. Every page: `Why:` under every Try it answer, `::: {.check}` in every
   Do it / Lab task / Activity; seminars in the seminar format (templates in
   `shared/templates/seminar-*`); case studies must not repeat the numbers
   of worked examples (change the sim or the example).
3. **GIFs and posters** for changed sims: run
   `sh shared/sims/recordings/record-all.sh <name>`. First fix the stale
   paths in `record-all.sh` (many sims moved folders). Changed sims:
   game-math week-04 drone-drop, sky-lift; week-06 sky-steps, drawbridge
   (posters too); week-08 island-quest; week-10 rule-smith; week-11
   treasure-odds; week-12 loot-forge; week-13 fair-or-frustrating, bag-lab;
   week-14 pilot-check, move-lab, bounce-lab, star-dock-missions,
   problem-drill; week-15 cave-gen, generator-doctor, raft-finals;
   computing-systems week-04 phone-picker, soc-explorer; week-05 ram-rush;
   week-06 disk-doctor; week-07 stack-builder (poster too: it shows the old
   layers), two-phones (new rounds 2–3); week-09 launch-planner,
   source-check, platform-pick, fact-or-myth; week-10 launch-day; week-11
   terminal-lab, lag-detective, net-fixer; week-12 cloud-planner; week-13
   lag-lab (labels), week-15 slide-sorter. Posters of Kit games show round 1
   in the written order; the page now mixes it (only cosmetic).
   Test each sim inside its page in the browser
   (no JS syntax check was possible).
4. courses-private: renumber the remaining solutions (Digital Media,
   Digital Skills online activities) and write
   `moodle/<slug>-weeks.md` (Arabic section texts; no "مختبر" for Digital
   Skills).
5. Full `quarto render`, `python3 tools/course_package.py`, then a PR into
   main (no co-author lines; signed commits).

## Tools on this Mac (2026-10-30)

- Quarto is **not installed** locally (CI pins 1.10.19), so no `quarto render`
  or `quarto typst compile`: SVG figures were exported to PNG with headless
  Chrome at scale 200/96 (same size as before). Deno (for `record.ts`) comes
  with Quarto, so GIF recordings also need Quarto.

## Helpers (recreate if the scratchpad is gone)

- add_why.py FILE MAP: MAP lines "question start<TAB>reason"; inserts
  `    Why: reason` under each matching answer.
- add_check.py FILE MAP: MAP blocks "=== Box title" + text; adds a `.check`
  at the end of that box.
- Check sizes: `python3 _extensions/lesson/check_size.py --all | grep <path>`.
