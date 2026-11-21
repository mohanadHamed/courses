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
    analyse big data. Platform: **Google BigQuery** (the free sandbox, a
    personal Google account; no card) and **Looker Studio**. Hadoop and
    Spark are shown only as ideas on simulators (too heavy for one hour).
  - **C3** (Labs 4–8): solve a real big data problem in **R** (RStudio,
    installed on the lab computers before Lab 4). One problem through all
    five labs: the transactions of a real online shop (Online Retail II,
    UCI, CC BY 4.0).
- No marks on the pages. The teacher ticks each student's finished lab on
  a checklist (private, not in this repo) and agrees the marks with the
  coordinator.

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
  preparation videos are in Arabic: the teacher records the screen while
  doing the worksheet (a one-page recording card per lab, private).
- **Examples:** business and everyday data (taxi trips, an online shop,
  sales, customers), never games.
- **Labels:** every session is labelled "Lab N" (`course.lecture-label`).
  The folders `week-WW` count the labs (WW = N), not syllabus rows.
- **Google accounts:** the students use their personal Google accounts
  (the university accounts are Microsoft). Every worksheet of Labs 1–3 ends
  with **Sign out**.
- **Recording on a Mac, labs on Windows:** BigQuery and Looker Studio are
  the same in the browser. In RStudio the videos click **Run** instead of a
  shortcut, the worksheets read files by name inside an RStudio Project (no
  paths), and the installation of R has its own Windows video.
- **Numbers on the simulators** are examples close to the real tables
  (the page says so); the worksheet never asks the student to write a
  result.
