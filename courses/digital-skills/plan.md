# Digital Skills (01101154) — unit plan

Status: plan v3 of 2026-10-31 (`plans/restructure-status.md`), after plan v2 of 2026-10-28 (`plans/restructure-19-lectures.md`). Source: the official syllabus (2026-2027, Drive) and the ILO–PLO matrix.
15 weeks: 10 units (core weeks) and 5 practice weeks (filling weeks) (AUTHORING.md, "Units and sessions", "Blended courses"). `schedule.yml` holds the same map for the site and the course package; if they differ, `schedule.yml` wins. "From" names the old lectures and sections that each session is built from.

## Course ILOs

| Code | ILO (with PLOs) | Bloom | K/S/C |
|---|---|---|---|
| A1 | Explain the main computer applications used to enhance daily productivity, including artificial intelligence tools. (PLO 3) | 2 | K |
| A2 | Explain basic concepts and terminology related to Microsoft Office applications. (PLO 3) | 2 | K |
| A3 | Describe the main features and uses of Microsoft Word, Excel and PowerPoint. (PLO 3) | 2 | K |
| B1 | Evaluate AI-generated text, data and images for accuracy, bias and suitability before using them in a document, worksheet or presentation. (PLO 3, 4) | 5 | K, C |
| C1 | Explain how Microsoft Word is used to create and format documents. (PLO 3) | 2 | K, S |
| C2 | Explain how Microsoft Excel is used to organize and present data. (PLO 3, 4) | 2 | K, S |
| C3 | Identify the basic features of Microsoft PowerPoint used to create presentations. (PLO 2, 3) | 1 | K |
| C4 | Use generative AI tools to draft, edit and improve Word documents, Excel worksheets and PowerPoint presentations. (PLO 2, 3) | 3 | S |
| D1 | Use digital and AI tools safely, responsibly and ethically: protect personal data, respect copyright and academic integrity, and state when AI was used. (PLO 3, 4) | 3 | S, C |

A1, A2, A3, C1, C2 and C3 are the six outcomes of the university description
(same text and Bloom level). B1, C4 and D1 add the use of AI.

## Weeks: 10 units and 5 practice weeks, each with a lab session and an online activity

Fully practical and blended: every week has a face-to-face lab session
(60 min) and an online activity with tasks to submit. No seminars.

| Week (syllabus) | Face-to-face (60 min, computer lab) | Online activity | From (plan v2) | ILOs |
|---|---|---|---|---|
| Unit 1 (1) | **Lecture 1** Digital Skills and the Apps That Make Us Productive | **Online activity 1** Your University Account, Cloud Storage and Files | L1, O1 | A1 |
| Unit 2 (2) | **Lecture 2** Generative AI Tools: What They Do Well and Where They Fail | **Online activity 2** Writing Clear Prompts | L2, O2 | A1 C4 |
| Unit 3 (3) | **Lecture 3** Microsoft Office: Concepts, Terms and Common Features | **Online activity 3** Office on the Computer, the Web and the Phone | L3, O3 | A2 A3 |
| Unit 4 (4) | **Lecture 4** Word (1): Formatting, Styles, Lists, Tables and Pictures | **Online activity 4** Word (2): Page Layout, Headers and a Table of Contents | L4, O4 | C1 |
| Unit 5 (5) | **Lecture 5** AI with Word: Draft, Summarize, Rewrite and Translate | **Online activity 5** A Formal Letter and a CV with AI Help | L5, O5 | C1 C4 B1 |
| Unit 6 (6) | **Lecture 6** Excel (1): Cells, Formulas, References and Basic Functions | **Online activity 6** A Monthly Budget Sheet | L6, O6 | C2 |
| Unit 7 (7) | **Lecture 7** Excel (2): Sorting, Filtering, Conditional Formatting and Charts | **Online activity 7** AI with Excel: Formulas, Clean Data and the Right Chart | L7, O7 | C2 C4 B1 |
| Practice week (8) | **Practice 1** Review of Lectures 1–7 (then the midterm) | **Online activity 8** Review Activity: Practice Questions | P1, O8 | all of 1–7 |
| Unit 8 (9) | **Lecture 8** PowerPoint: Slides, Layouts, Themes, Transitions, Animations and Notes | **Online activity 9** A Short Presentation with AI Help | L8, old O10 | C3 C4 B1 |
| Practice week (10) | **Practice 2** AI with PowerPoint: Outline, Slides and Pictures | **Online activity 10** A Five-Slide Talk | P2, old O9 | C3 C4 B1 |
| Unit 9 (11) | **Lecture 9** Checking AI Output and Using AI Responsibly | **Online activity 11** Fact-Checking an AI-Written Document | L9, O11 | B1 D1 |
| Practice week (12) | **Practice 3** Responsible AI in Practice: Personal Data, Copyright and Honesty | **Online activity 12** Safe Prompts and an AI-Use Statement | P3, O12 | D1 |
| Unit 10 (13) | **Lecture 10** Excel (3): Summarizing Data with AI Help | **Online activity 13** Analyzing a Small Dataset and Charting It | old P4 (as a lecture), O13 | C2 C4 B1 |
| Practice week (14) | **Practice 4** Working Across Office Apps with AI | **Online activity 14** Course Project (1): Plan, Data Sheet and First Draft | old P5, O14 | A1 A3 C4 |
| Practice week (15) | **Practice 5** Course Project Presentations | **Online activity 15** Course Project (2): Final Report, Data Sheet and Presentation | old L10 (practice format), O15 | B1 C1–C4 D1 |

- Core: Lectures 1–10 with Online activities 1–7, 9, 11 and 13. Flexible:
  the practice weeks (Practice 1–5 with Online activities 8, 10, 12, 14 and
  15). When weeks are lost, the practice weeks go first; the course project
  (Online activities 14 and 15, Practice 5) is in the last two of them.
- Every core idea is in a unit: PivotTables are in Lecture 10, the AI outline
  turned into slides in Online activity 9, responsible AI in Lecture 9.
- AI is the main topic of Lectures 2, 5, 9 and 10 and of Online activities 2,
  5, 7, 9, 11, 12 and 13: more than the required quarter.
- The AI-use statement starts in unit 9 (Lecture 9).
- No homework (the online activities replace it).

## Lecture worksheets: real apps or simulators

Every lecture is built around a worksheet (`lesson-NN-sheet.qmd`, AUTHORING.md,
"Lecture worksheets"): one experiment per section, done on the computer in
class and checked there. The tools of each lecture, by its nature (a real
app first when the lab has it; the simulators of the page are the teacher's
demonstration and the way to do a step without the app):

| Lecture | Experiments (one per section) | Tools | Start files |
|---|---|---|---|
| 1 Productivity apps | by hand or with AutoSum · find the apps · a first prompt | mix: Excel, the Start menu and an AI assistant; Time Saver, App Launcher, AI Chat | `prices-start.xlsx` |
| 2 Generative AI tools | two good jobs · weak spots · AI, search or spreadsheet | mix: an AI assistant and a search engine; Weak Spots, Right Tool | none |
| 3 Office concepts | the parts of the window · the ribbon · Save, Save As and formats | mix: Word, Excel and PowerPoint; Window Tour, Ribbon Finder, Save Lab | `notice-start.docx` |
| 4 Word (1) | formatting · styles · a list and a table · a picture | real app: Word; Format Lab, Style Lab, List and Table Lab | `family-day-start.docx`, `park.png` |
| 5 AI with Word | a draft · a summary · a new tone · a translation | mix: an AI assistant and Word; Word AI Lab, Tone Lab | `report-start.docx` |
| 6 Excel (1) | cells and ranges · a formula · copy a formula · four functions | real app: Excel; Formula Lab and Reference Lab | `shop-start.xlsx` |
| 7 Excel (2) | sort · filter · a colour rule · two charts | real app: Excel; Table Lab, Chart Lab | `sales-start.xlsx` |
| 8 PowerPoint | slides and layouts · a theme · notes · transitions and animations | real app: PowerPoint; Slide Builder, Transition Lab | `talk-start.pptx` |
| 9 Checking AI output | claims and sources · bias · personal data · the AI-use statement | simulators and a browser: Fact-Check Lab, Bias Lab, Prompt Cleaner; Word for the statement | none |
| 10 Excel (3) | a PivotTable · weeks and averages · check an AI summary | mix: Excel and an AI assistant; Pivot Lab, Summary Check | `month-start.xlsx` |

Lecture 6 is the model (done 2026-10-31); the others follow it.

## Online activities: varied content, always tasks to submit

Each online activity has a content type (`content:` in its front matter),
so the 15 weeks do not all look the same. Every type keeps the Steps with
their self-checks and the Tasks to submit (marks, a concrete product,
uploaded to Moodle; model answers in courses-private). The practice weeks
(8, 10, 12, 14, 15) add no new content.

- **lesson** (a): an interactive lesson: the Steps explain with text,
  figures and self-checks; simulators where they help.
- **sims** (b): simulators only: every Step is a simulator with a one-line
  instruction and its self-check.
- **mix** (c): text steps and simulator steps.
- **video** (d): free official videos, linked (never copied), with title,
  source, length and the date checked; the Steps practise what they show.
- **course-video** (e): a short video made for the course (generic
  interfaces like the simulators, A2 captions, a voice-over), in the page.

| # | Online activity | Week | Type | Content |
|---|---|---|---|---|
| 1 | Your University Account, Cloud Storage and Files | Unit 1 | course-video | video *Folders, paths and good file names* (about 2 min, to be made); Path Finder, Folder Lab, Sync Lab |
| 2 | Writing Clear Prompts | Unit 2 | sims | Prompt Builder, Follow-up Chat, Prompt Doctor |
| 3 | Office on the Computer, the Web and the Phone | Unit 3 | sims | PDF Export, Paste Lab, Share Settings |
| 4 | Word (2): Page Layout, Headers and a Table of Contents | Unit 4 | video | Microsoft Support: *Change margins* (0:31), *Insert or remove a page break* (0:45), *Insert a header or footer* (0:56), *Insert page numbers* (0:57), *Add a Table of Contents in Word* (0:38) |
| 5 | A Formal Letter and a CV with AI Help | Unit 5 | lesson | the parts of a letter and a CV, checking what the AI wrote; Letter Builder, Profile Picker, CV Checker |
| 6 | A Monthly Budget Sheet | Unit 6 | course-video | video *A monthly budget in Excel* (about 2 min, to be made); Budget Builder, Number Format Lab |
| 7 | AI with Excel: Formulas, Clean Data and the Right Chart | Unit 7 | mix | AI Formula Lab, Clean Data Lab, Chart Lab |
| 8 | Review Activity: Practice Questions | Practice week | sims | Practice Quiz, Contents Builder, Reference Lab |
| 9 | A Short Presentation with AI Help | Unit 8 | mix | Outline Lab, Image Prompt Lab, a check before presenting |
| 10 | A Five-Slide Talk | Practice week | video | Microsoft Support: *Add speaker notes* (0:32), *Add animations to slides* (1:18), *Use Presenter View* (1:36); Talk Planner, Rehearsal Lab |
| 11 | Fact-Checking an AI-Written Document | Unit 9 | course-video | video *Check an AI answer: claims, sources and fair words* (about 2 min, to be made); Claim Finder, Claim Court |
| 12 | Safe Prompts and an AI-Use Statement | Practice week | mix | Prompt Cleaner, a tool and copyright check, Statement Builder |
| 13 | Analyzing a Small Dataset and Charting It | Unit 10 | video | Microsoft Support: *Create a PivotTable* (0:45), *Create charts* (0:52); Pivot Lab |
| 14 | Course Project (1): Plan, Data Sheet and First Draft | Practice week | lesson | the plan, the data sheet and the first draft; Plan Checker |
| 15 | Course Project (2): Final Report, Data Sheet and Presentation | Practice week | lesson | the final files, the checks and the AI-use statement |

Three activities of each type. The official videos (all with English
captions, checked 2026-10-31 by their pages and captions):

| Video (title on the page) | Page (Microsoft Support) | Length |
|---|---|---|
| Change margins | support.microsoft.com/en-us/word/training/change-margins | 0:31 |
| Insert or remove a page break | support.microsoft.com/en-us/word/training/insert-a-page-break | 0:45 |
| Insert a header or footer | support.microsoft.com/en-us/word/training/insert-a-header-or-footer | 0:56 |
| Insert page numbers | support.microsoft.com/en-us/word/training/insert-page-numbers | 0:57 |
| Add a Table of Contents in Word | support.microsoft.com/en-us/word/training/insert-a-table-of-contents | 0:38 |
| Add speaker notes | support.microsoft.com/en-us/powerpoint/training/add-speaker-notes-to-your-slides | 0:32 |
| Add animations to slides | support.microsoft.com/en-us/powerpoint/training/animate-text-or-objects | 1:18 |
| Use Presenter View | support.microsoft.com/en-us/powerpoint/training/use-presenter-view-in-powerpoint | 1:36 |
| Create a PivotTable | support.microsoft.com/en-us/excel/get-started/create-a-pivottable-to-analyze-worksheet-data | 0:45 |
| Create charts | support.microsoft.com/en-us/excel/get-started/create-a-chart-from-start-to-finish | 0:52 |

Check the links every semester: Microsoft moves its pages.

## Tasks with AI (ideas)

AI is already the subject of many sessions; the Tasks with AI there are the Office tasks done with AI help at a higher level (a formatted report, a budget with formulas and a chart), always with checking and, from unit 9, the AI-use statement.

## Notes

- **Independent study first.** Pages, slides and online activities never require classmates (the course project has no peer feedback).
- The margin: the five practice weeks (Practice 1–5 and their online activities) are flexible: taught when time allows, studied at home otherwise. Lectures 1–10 and their online activities are core.
- No homework: the online activities replace it. Their model answers are in `courses-private` (`week-WW/online-NN-solutions.md`).
- The AI-use statement starts in unit 9 (Lecture 9).
