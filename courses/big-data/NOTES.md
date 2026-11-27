# Big Data and Data Analysis (02053116) — the lab part: course notes

Course-specific rules only. Global rules are in the root `AUTHORING.md`;
where this file differs, it wins for this course.

## Whose course, and what part

- A course of the **Faculty of Business** (Bachelor in Management
  Information Systems, year 3, blended, 3 credit hours), not of the
  Technical College. Its coordinator and teacher of the theory is another
  member of staff; the official course plan (2026-10-07) is a university
  document: never copy it here (only the text of C1 and C3 is in
  `_metadata.yml`).
- The teacher gives **only the lab part**: one hour every Sunday in the
  computer lab (Windows, Internet), from 22/11/2026 to 10/1/2027 (8 labs),
  for two outcomes, **one after the other**:
  - **C1** (Labs 1–3): use big data platforms to collect, store, process and
    analyse big data. Platform: **Google BigQuery** and **Looker Studio**.
    Lab 1 used the real BigQuery sandbox with a personal Google account;
    **from Lab 2 there is no Google account** (below, "The BigQuery Lab").
    Hadoop and Spark are shown only as ideas on simulators (too heavy for
    one hour).
  - **C3** (Labs 4–8): solve a real big data problem in **R** (RStudio,
    installed on the lab computers before Lab 4). One problem through all
    five labs: the transactions of a real online shop (Online Retail II,
    UCI, CC BY 4.0).
- **No marks on the worksheets** (the teacher's decision of 2026-11-27:
  the labs do not focus on marks now). A task heading is `## Task N ·
  title`, with no marks; no marks in the first lines, no "(1 mark)" on
  *Finished early?*, and no "Your mark" box. The worksheet ends with *Show
  your teacher* and the *Finished early?* box. `check_size.py` warns about
  marks in a Big Data worksheet (it replaced the rule of 2026-11-21: 10
  marks for each lab).

## Business students: simple, and only what the outcome needs (2026-11-27)

The teacher's request after Lab 2 was first written: the students study
**accounting, MIS and business administration**, not IT, and most are weak
with computers. The course is a **service course**: the students use data
platforms and R to help their work, not to learn programming.

- **Assume no IT course before.** Every idea in everyday words, with a
  business example (a return, a country, a big order), never a technical
  one for its own sake.
- **SQL is only `SELECT … FROM … WHERE`** (columns, a table, a filter with
  `=`, `<`, `>`, `>=`, `AND`, `IS NULL`, text in quotes) **and `CREATE TABLE`
  with its column names and types**. Nothing more: no `CREATE TABLE … AS
  SELECT`, no `GROUP BY` or `COUNT` for the student to type, no joins, no
  backticks when `dataset.table` is enough. A bigger idea (totals per
  country, a dashboard) is shown **ready, with one click**, on the big
  picture simulator, not typed.
- **The lab in one hour, at the pace of the slowest student** (the size of
  Lab 1: about 20 minutes of the page by `check_size.py`, 3 tasks):
  1. **The big picture** (the teacher, 5–10 minutes): a simulator that does
     the whole lab in a few clicks, with the data and the queries ready
     (`week-WW/sims/big-picture.html`), so the class sees what the lab is
     for before any detail.
  2. **Step by step, together** (about 30 minutes): the teacher goes
     through the page and the class does each step on the simulator of the
     page at the same time. The worksheet holds the same steps (for the lab
     and for home).
- The prep video is sent before the lab on the e-learning platform; it is
  not shown in class.

## The model: the lab model of Digital Skills, and nothing else

Every lab is a lecture in the **lab model** (`lab: true`;
`courses/digital-skills/NOTES.md`, "The lab model"): about 15 minutes on
the interactive page (paged, simulators that look like the real app, one
Try it per section, Key terms, Summary), then the printed **worksheet**, a
guide with numbered steps, a box to tick and the drawn screen of every
step (`tools/bq_screens.py` for the BigQuery screens). No notes (PDF), no
slides, no homework, no online activities, no Game challenge, no course
package and no platform texts.

- **One short activity per lab** (the teacher's rule of 2026-11-21): a
  quick explanation of at most 15 minutes on the page, then a worksheet
  with **one** small activity (3 tasks, about 10–12 steps) that a student
  finishes in less than 30 minutes, a strong student in about 20, so that
  every student finishes something in the hour. More practice goes into a
  "Finished early?" box at the end, never into a fourth required task.
- **Only screens that match the real app** (the teacher's request of
  2026-11-21: Task 2 of Lab 1 sent the students to **+ Add data** and the
  Marketplace, which did not match BigQuery). A step gets a drawn screen
  only when its screen is checked against the real app (by the teacher, or
  from the official help page of the current version). Where the screens
  change often or were not checked, the step is **general**: the name of
  the box or button and what to type or click, with the names the student
  will see (the search box of BigQuery Studio, *chicago taxi*, the dataset
  *chicago_taxi_trips*, the table *taxi_trips*), and no picture. The
  simulator of the page follows the same general steps.
- **Code is explained** (the teacher's request of 2026-11-21, after Lab 1:
  the query was given without saying what `EXTRACT` or `GROUP BY` do).
  Every line of code that a student types (SQL in Labs 1–3, R in Labs 4–8)
  is explained, and every word that is not plain English (`SELECT`,
  `EXTRACT`, `AS`, `*`, `GROUP BY`, `DESC`, backticks, `;`, `<-`, `%>%`, …):
  - on the page, a part `### The <code>, line by line` before the app box:
    the code, then a `::: {.code-explain}` table (Line | What it does, one
    row for every line), then a **Code Steps** simulator
    (`shared/sims/code-steps.js`, `window.CODE_STEPS`) that runs the code
    step by step on a small example table, in the order the computer runs
    it (SQL: `FROM` first, `ORDER BY` last);
  - in the worksheet, an `#explain(...)` table under the code box (the
    meaning of each line in one short sentence);
  - a code of the "Finished early?" box says in one sentence what changed.
  `check_size.py` warns about a SQL or R block on a lab page without its
  `{.code-explain}` table (or with fewer rows than lines), and about a
  worksheet with code to type and no `explain(...)` table.
- **Language:** the worksheets and the pages are in clear English (B1:
  third-year business students; short sentences, every term explained). The
  prep video is read in Arabic (below, "The prep video").
- **Examples:** business and everyday data (taxi trips, an online shop,
  sales, customers), never games.
- **Labels:** every session is labelled "Lab N" (`course.lecture-label`).
  The folders `week-WW` count the labs (WW = N), not syllabus rows.
- **Google accounts:** only in Lab 1 (taught as it is, with **Sign out** at
  the end). Labs 2–3 need no account: their worksheets are done on the
  BigQuery Lab (below).
- **Labs on Windows:** BigQuery and Looker Studio are the same in the
  browser on every computer. In RStudio the worksheets read files by name
  inside an RStudio Project (no paths), and the installation of R has its
  own Windows guide.
- **Numbers on the simulators** are examples close to the real tables
  (the page says so); the worksheet never asks the student to write a
  result.

## The BigQuery Lab: no sign-in (since Lab 2, 2026-11-27)

In Lab 1 most students could not sign in to their personal Gmail on the
lab computers, and the coordinator asked for the easiest way, with no
sign-in. So from Lab 2 **the worksheet of every C1 lab is done on a
simulator of the page**, and the page and the worksheet show the same
screens. The R labs (C3) stay on the real RStudio of the lab computers.

- **A real SQL engine.** `shared/sims/bq-engine.js` runs SQL on SQLite
  (sql.js, `shared/sims/vendor/sql-wasm.*`, MIT) with the rules of
  BigQuery: `project.dataset.table` names in backticks (a dataset is an
  attached database), EXTRACT, COUNTIF, FORMAT_DATE, DATE_TRUNC,
  SAFE_DIVIDE, `"text"` as a string, `/` as FLOAT; the errors of BigQuery
  (Unrecognized name … Did you mean …?, Not found: Table …, Syntax error
  at [line:col], a column neither grouped nor aggregated, Already Exists,
  no DML in the sandbox); **rows in any order without ORDER BY** (shuffled
  on every run); and the bytes before the run (the columns that the query
  reads; 0 B for COUNT(*) alone). Any query a student types runs.
- **The app of the lab:** `week-WW/sims/bq-labN.js` draws BigQuery Studio
  (the Explorer and its ⋮ menus, Create dataset, Create table › Upload,
  Schema/Details/Preview, the editor, Results, Job information). One page
  holds the whole worksheet (`bq-labN.html`, opened on a full page from the
  lab page), and it remembers the student's work in the browser
  (`localStorage`, replayed on load; *Start again* empties it). The page
  embeds the same app in parts (`bq-labN-<part>.html`).
- **Steps a student can do alone** (the teacher's request of 2026-11-27):
  the list of steps under the simulator gives each step a short title
  (*Task 1 · Create the dataset shop*) and, in brackets, the details:
  where to click and what to type, with the names on the screen (*In the
  Explorer on the left, click ⋮ next to big-data-lab, then Create dataset.
  Type shop in Dataset ID, then click Create dataset.*). A student who did
  not follow the teacher can do the step from the list alone. One step for
  each screen or panel (open Create table, then fill it in).
- **Try a change** (the teacher's request of 2026-11-27: "what if I remove
  ORDER BY?"): under the editor, 6–10 changes of the queries of the lab
  that a student often wants to try (another value in WHERE, no quotes,
  remove the WHERE line, AND, a name spelled wrong …), each with one
  sentence on what it shows. The engine gives the real answer; the sentence
  explains it.
- **The data:** the same file in Labs 2–8, Online Retail II (UCI, CC BY
  4.0), the sheet of 2009–2010 (525,461 rows). The simulator uses
  `week-02/sims/online_retail_2010.csv`, **1 row in every 25** (21,019
  rows, 1.9 MB); the pages and the worksheets say so. The numbers of the
  worksheet are the real answers on that file (sales 21,019 rows; the
  returns, Quantity < 0, 514 rows).
- **The screens of the worksheet** are the simulator itself, with its
  orange numbers: `bq-labN.html?shot=<name>` (the list `SHOTS` in the app),
  taken by `tools/bq_sim_shots.sh` (headless Chrome, a local server).
  `?shot=<name>&poster=1` gives a poster without numbers.
- **The prep video** shows the simulator and its screens; no sign-in.

## The prep video (since 2026-11-21)

The course is blended: the coordinator's lectures, this lab, and offline
activities on the e-learning platform. The **prep video** of each lab is
one of those activities, so it teaches: it explains the ideas of the lab
in order (the teacher's request of 2026-11-21: a screen recording of the
worksheet only repeats the lab), and it is the **introduction of the
interactive page** of the same lab. Students watch it before the lab, and
absent students study with it.

- **The script comes first:** `week-WW/videos/labN-intro-script.txt`, in
  **Arabic** (the teacher reads it), with the English terms of the lab
  inside the sentences (BigQuery, query, GROUP BY). One line for each
  sentence and a blank line between scenes: **10–14 scenes of 3–6 short
  lines**. **450–1 000 words** (about 7–10 minutes): short enough to read
  without many repeats. Symbols are said in words ("COUNT مع النجمة").
- **The pictures are in English**, the words of the page and the
  worksheet: `videos/labN-intro.html` with `video-kit.js`, one scene for
  each scene of the script (`VIDEO.captions: false`: no words burned into
  the picture). Each line of the script shows its part of the picture. The
  scenes reuse the drawn screens (`../images/…`) and the simulator posters
  (`../sims/…`) with `image()`, and show code with `code()` (the line that
  the voice explains is lit, in the order the computer runs it).
- **Its order:** the question of the lab → the ideas of the page, one
  scene or two for each section, with the code line by line → what the
  student does in the lab (the tasks of the worksheet, sign out) → "try the
  simulators before the lab".
- **The teacher's voice, in one file or more.** The teacher reads the
  whole script in one recording (QuickTime or Voice Memos), silent about
  **3 seconds between scenes**: the scene breaks are the pauses that fit
  best (each scene about as long as its text, the longer pauses first), so
  a shorter pause between scenes or a longer one inside a scene is fine. After a mistake, stop and start a new
  file at the beginning of the same scene. The first number of a file's
  name is the scene where it starts (`scene-01.m4a`, then `scene-07.m4a`);
  what the earlier file holds after the end of scene 6 is left out. One
  file for each scene works too. The recordings stay private
  (`lab-materials/LabN_voice/`). The reading sheet (`LabN_Video_Script.pdf`,
  private) shows each scene's number, its words and its last picture.
- **Clean the recording first** (the teacher's request of 2026-11-21: the
  generated voices made mistakes no person makes, so the teacher's voice
  stays, without its slips). `python3 tools/clean_voice.py find <recording>`
  hears the recording on the Mac (macOS speech recognition, on-device;
  macOS asks once to allow it) and prints its words with their times and
  the words said twice in a row. Check each place against the script (some
  words are twice on purpose: "FROM. FROM"), then
  `python3 tools/clean_voice.py cut <recording> LabN_voice/scene-01.wav a-b …`
  removes each first, wrong reading (from its start to the start of the
  right one). Run `find` on the result to see that the places read right.
  The long pauses are shortened when the video is made: a pause inside a
  scene longer than 0.8 seconds becomes 0.8 (`MAX_PAUSE`).
- **Make it:**
  `sh shared/sims/recordings/make-course-video.sh courses/big-data/week-WW/videos labN-intro <recordings-dir>`.
  Without a recordings dir (or for a scene without its file), macOS `say`
  (Majed) reads the scene: a draft to check the pictures and the timing
  before the teacher records. The silence before and after each recording
  is cut, and the time of every line is found from the pauses of the
  speaker. `SCENE_SHOTS=<dir>` saves the last picture of every scene for
  the reading sheet.
- **On the page:** the first section, `## Before the lab: the video`, a
  `::: {.prep-video}` box with `{{< watch file=… captions=… poster=…
  script=… length=… lang="ar" >}}` (Arabic captions in CC, the script as a
  right-to-left transcript). It is not counted in the 15 minutes of class.
- `check_size.py` warns about a lab page without its prep video, a missing
  file, a script outside 450–1 000 words, and captions that are not the
  lines of the script.

