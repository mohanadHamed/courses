# Pages taught on the smart screen: status

Branch `claude/vigilant-lamport-8o58y7` in both repos (`courses` and
`courses-private`). The teacher's requests of 2026-11-08 and the rules are
in AUTHORING.md ("The page is taught in class", "Answers without written
English", "Lecture worksheets", "Tasks with AI", "Blended courses",
"Homework", "Way of working", Lessons learned 2026-11-08).

## The requests (2026-11-08)

1. The classrooms have smart screens; the teacher teaches from the
   interactive page instead of the slides. The pages were too long for a
   lecture. Untaught lecture pages are sized for class: about 40 minutes of
   a 60-min lecture, 60–70 (at most 65 planned) of a 90-min lecture.
2. Rewrite only what is not taught yet: Game Math from Lecture 3,
   Computing Systems from Lecture 4, Digital Media from Lecture 3, Digital
   Skills from Lecture 2 (unit 2). Every deck stays on the site.
3. Digital Skills stays blended; the face-to-face version stays hidden. It
   works with and without a lab; the teacher chooses for each experiment the
   simulator on the page or the real app on the laptop (HDMI).
4. Later the same day: lectures hold only their ILOs; no question asks for
   English text (choices, orders, numbers, names, a few words); homework and
   online tasks have short answers and show no marks; in Digital Skills AI
   is a quarter to a third of a session and students never write a prompt;
   Unit 2 practises everyday skills on the phone; the newest rules are the
   standard for every rewrite (the taught sessions are rewritten next
   semester).
5. In the evening: the homework and tasks PDFs are forms that students type
   their answers in.

## Done (one signed commit per step, pushed)

- Rules and checker: `check_size.py` estimates the class minutes of a page,
  warns about marks, essay words in graded tasks and worksheet records that
  ask for a reason; the homework of the taught units is frozen (`FROZEN`).
- Game Math Lectures 3–12 (53–62 planned minutes), Computing Systems 4–12
  (34–40), Digital Media 3–12 (35–40): pages for class.
- Digital Skills Lectures 2–10 (39–40 minutes): Part A in the app, Part B
  on a simulator or the phone; the page offers the simulator or the real
  app (first lines, part labels). Unit 2 is new (search, screenshots, AI as
  one third; Search Lab; Online activity 2: a calendar reminder, a scan, the
  missing part of a prompt). Lecture 5 is Word with AI (one AI experiment;
  Word's spelling check and Find and Replace with Check Lab; Translate and
  the tone). Lecture 9 is Check Information and Share Safely, with AI Too
  (a claim in two sources; a free picture, a source line and app
  permissions; a safe prompt and an AI-use statement).
- Online activities 2–15: short answers, ready prompts, given AI-use
  statements; Online activity 7 is Excel first (AI in one Step).
- Homework of Game Math 3–12, Computing Systems 4–12 and Digital Media 3–12:
  short answers (letters of choices, numbers, words, yes or no); marks
  removed from every homework and online activity.
- Fillable PDFs: every answer line (and the Name and Student number line,
  and the answer cells of a table) is a field to type in
  (`homework_pdf.py` with pypdf; CI installs pypdf and checks the fields).
- Solutions and platform texts in `courses-private` for every change.
- Scope: the sections of the untaught lectures were checked against the
  syllabus weeks and ILOs (Drive copy of 2026-11-08); none is outside them.

## Checked (2026-11-08)

- `check_size.py` (no warnings), `check_figures.py` (no cross shapes),
  `face-to-face/check_f2f.py` (0 warnings).
- Rendered with Quarto 1.10.19: the changed Digital Skills weeks (pages,
  notes, worksheets, slides) and every homework and online page; the
  homework and tasks PDFs printed with Chrome's headless shell and checked
  for their form fields and pages.

## Still to do

1. Next semester: rewrite the lectures taught before the screens
   (`HOME_PAGES` in `check_size.py`), Digital Skills Lecture 1 and Online
   activity 1, and the frozen homework (`FROZEN`) with the newest rules,
   then empty both sets. Seminars and practice sessions get the rule
   "Answers without written English" at the same time.
2. If Online activity 2 is already open on the platform, replace its page
   and tasks PDF there: its tasks changed completely.
3. The exercises of the lesson notes (PDF, self-study with answers) of the
   untaught lectures still have 49 "Why …?" or "Explain …" items in 26
   files (Computing Systems 4–12, Digital Media 3–12, Game Math 5–12,
   Digital Skills 4, 6, 8). Turn each into a choice ("Which reason is
   right? A … B …") with its answer, then let `check_size.py` check the
   notes exercises too. The pages, worksheets, homework and online tasks
   are done.
