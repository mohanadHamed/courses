# Pages taught on the smart screen: status

Branch `claude/vigilant-lamport-8o58y7` in both repos (`courses` and
`courses-private`). The teacher's request of 2026-11-08 and the rules are
in AUTHORING.md ("The page is taught in class", "Lecture worksheets",
"Tasks with AI", "Blended courses", Lessons learned 2026-11-08).

## The request (2026-11-08)

1. The classrooms have smart screens; the teacher teaches from the
   interactive page instead of the slides. The pages were too long for a
   lecture. Untaught lecture pages are sized for class: about 40 minutes of
   a 60-min lecture, 60–70 (at most 65 planned) of a 90-min lecture.
2. Rewrite only what is not taught yet: Game Math from Lecture 3,
   Computing Systems from Lecture 4, Digital Media from Lecture 3, Digital
   Skills from Lecture 2 (unit 2).
3. Every deck stays on the site as a reference (not deleted).
4. Digital Skills stays blended; the face-to-face version stays hidden.
   It must work with and without a computer lab: the page is the lesson
   without a lab (simulators of Office tasks, AI prompts to copy into an
   assistant in another tab), the worksheet (Part A in the app, Part B on a
   simulator) is the lab manual. AI content must be practical and joined
   to Office work, never AI alone. Online activities teach every task in
   their Steps with a model, and their tasks are simple enough to do alone.

## Done (one signed commit per unit, pushed)

- Rules and checker: `check_size.py` estimates the class minutes of a page
  (PAGE_TIME_COST, PAGE_TIME = 40 / 65; HOME_PAGES = the lectures taught
  before); the worksheet slides rule ("Your worksheet", "Results of the
  worksheet"); a Part A needs a Part B; no minutes for a part.
  `shortcodes.lua`: the page leaves out "The idea:" of an experiment.
- Game Math Lectures 3–12: 53–62 planned minutes.
- Computing Systems Lectures 4–12: 34–40.
- Digital Media Lectures 3–12: 35–40.
- Digital Skills Lectures 2–10 (39–40): worksheets, pages and slides taken
  from the face-to-face version (Part A / Part B), merged to three
  experiments where needed (Lectures 4, 5, 9; the notes of Lectures 4, 5,
  6, 8 and 9 merged two sections the same way), copy-ready prompts on every
  AI step, the Game challenge slides kept. Lecture 2 was redesigned (a
  draft checked in Word, a total checked in a spreadsheet: new simulator
  `week-02/sims/bill-check.html` with poster, GIF and scenario).
- Online activities 2–7, 9, 11, 13: a model in each Step; tasks simpler
  (2 unchanged: it may be open already). Solutions and platform texts in
  `courses-private` (`online-NN-solutions.md`,
  `moodle/tools/content_digital_skills.py`).

## Still to do (in this order)

1. Render check with Quarto 1.10.19 (the Typst package `tiaoma` 0.3.0 must
   be in `.quarto/typst/packages/preview/` when packages.typst.org is not
   reachable): every changed week, then look at a few pages, PDFs and
   decks.
2. `courses/digital-skills/NOTES.md` and `plan.md`: the two-case model,
   the experiments of each lecture, the face-to-face version left as it was
   on 2026-11-06 (align it if the course is switched).
3. Rebuild `moodle/digital-skills-weeks.md` in courses-private
   (`moodle/tools/build.py`).
4. Online activities 14 and 15 (the course project) and Practice 4–5: look
   at their size; Online activities 8, 10 and 12 are not given this
   semester.
5. Open the pull requests when the teacher asks.
