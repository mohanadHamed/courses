// Digital Skills · Midterm review of Units 1–4 (one PDF for the students).
// Build (from the project root):
//   quarto typst compile --root . courses/digital-skills/midterm/midterm-review.typ \
//     courses/digital-skills/week-08/files/digital_skills_midterm_review.pdf
// The key words come from shared/glossary.yml (the same words as the lessons).
#import "@preview/tiaoma:0.3.0": qrcode

#let accent = rgb("#D9480F")
#let accent2 = rgb("#FFC078")
#let soft = rgb("#FFF4E6")
#let prep-url = "https://mohanadhamed.github.io/courses/courses/digital-skills/midterm-prep.html"
#let gl = yaml("/shared/glossary.yml")
// Noto as on the site; the Mac fonts when Noto is not installed.
#let latin = ("Noto Sans", "Helvetica Neue")
#let arabic = ("Noto Naskh Arabic", "Geeza Pro")

#set document(title: "Digital Skills · Midterm Review: Units 1–4", author: "Mohanad Hamed")
#set page(paper: "a4", margin: (x: 1.8cm, top: 1.7cm, bottom: 1.6cm),
  header: context {
    if counter(page).get().first() > 1 [
      #set text(size: 8pt, fill: luma(110))
      Digital Skills (01101154) · Midterm Review: Units 1–4 #h(1fr) Mohanad Hamed
      #v(-6pt) #line(length: 100%, stroke: 0.4pt + accent2)
    ]
  },
  footer: context [
    #set text(size: 8pt, fill: luma(110))
    Technical College, Al-Israa University #h(1fr)
    #text(fill: accent, weight: "bold")[#counter(page).display("1 / 1", both: true)]
  ])
#set text(font: latin + arabic, size: 10pt, lang: "en")
#set par(justify: false, leading: 0.6em, spacing: 0.75em)
#set list(spacing: 0.55em, indent: 2pt, marker: text(fill: accent)[•])
#set enum(spacing: 0.55em)
#show strong: set text(fill: rgb("#7a2a06"))

// An Arabic box: the same points in Arabic, right to left.
#let ar(body) = block(width: 100%, fill: soft, radius: 8pt, inset: (x: 12pt, y: 10pt),
  stroke: (right: 3pt + accent), breakable: false)[
  #set text(font: arabic + latin, lang: "ar", dir: rtl, size: 10.5pt)
  #set par(justify: false, leading: 0.75em)
  #set list(marker: text(fill: accent)[•])
  #text(weight: "bold", fill: accent)[بالعربي] \
  #body
]

// A unit band.
#let unit(n, title, sessions) = {
  pagebreak(weak: true)
  block(width: 100%, fill: accent, radius: 8pt, inset: (x: 14pt, y: 10pt))[
    #text(fill: white, size: 9pt, weight: "bold")[UNIT #n · #sessions] \
    #text(fill: white, size: 15pt, weight: "bold")[#title]
  ]
  v(4pt)
}
#let part(t) = block(above: 1.0em, below: 0.5em)[#text(size: 11.5pt, weight: "bold", fill: accent.darken(20%))[#t]]
#let tip(body) = block(width: 100%, fill: rgb("#FFF9DB"), radius: 6pt, inset: 8pt, stroke: (left: 3pt + rgb("#F59F00")))[
  #text(weight: "bold", fill: rgb("#B35C00"))[Watch out! ] #body]
#let tbl(cols, ..cells) = table(columns: cols, inset: 5pt, stroke: 0.5pt + luma(215),
  fill: (_, y) => if y == 0 { soft } else { none }, ..cells)

// The key words of a unit (EN | AR | meaning), from the glossary.
#let words(..keys) = {
  part[Key words · الكلمات المهمة]
  table(columns: (24%, 26%, 50%), inset: 4pt, stroke: 0.4pt + luma(220),
    fill: (_, y) => if y == 0 { soft } else { none },
    table.header([*English*], align(right)[*العربية*], [*Meaning*]),
    ..keys.pos().map(k => {
      let t = gl.at(k)
      (text(weight: "bold", size: 9pt, t.en),
       align(right, text(font: arabic, lang: "ar", size: 9.5pt, t.ar)),
       text(size: 8.5pt, t.at("def", default: "")))
    }).flatten())
}

// ----------------------------------------------------------------- page 1
#block(width: 100%, fill: soft, radius: 12pt, inset: 16pt, stroke: 0.6pt + accent2)[
  #text(size: 9pt, fill: accent, weight: "bold")[DIGITAL SKILLS · 01101154 · ALL DIPLOMA PROGRAMMES]
  #v(2pt)
  #text(size: 22pt, weight: "bold", fill: rgb("#7a2a06"))[Midterm Review: Units 1–4]
  #v(-4pt)
  #text(size: 11pt)[The main points, the key words, and how to prepare]
]

#grid(columns: (1fr, 3.4cm), column-gutter: 14pt, align: horizon,
  [
    #part[What is in the exam?]
    - *Units 1–4:* Lectures 1–4 and Online activities 1–4.
    - *Multiple choice:* each question has 4 answers; one is right.
    - *1 mark* for each question.

    #part[How to study]
    + Read this PDF: one unit at a time, in English and Arabic.
    + Do the *practice exam* on the course website (the QR code): 30 random
      questions in one hour. It marks each answer at once and says why.
      Do it again and again: every exam has new questions.
    + Missed a question? Read its unit here again.
  ],
  align(center)[
    #qrcode(prep-url, width: 3.2cm)
    #v(-2pt)
    #text(size: 8.5pt, weight: "bold")[Practice exam]
  ])

#ar[
  - الامتحان النصفي يشمل #strong[الوحدات من 1 إلى 4]: المحاضرات من 1 إلى 4 والأنشطة الإلكترونية من 1 إلى 4.
  - الأسئلة #strong[اختيار من متعدد]: لكل سؤال 4 خيارات، واحد منها فقط صحيح، ولكل سؤال علامة واحدة.
  - #strong[طريقة الدراسة:] اقرأ هذا الملف وحدة وحدة، ثم حلّ #strong[الامتحان التجريبي] على موقع المادة (رمز QR أعلاه):
    30 سؤالاً عشوائياً خلال ساعة، تظهر لك صحة كل إجابة مع السبب بالعربية والإنجليزية. كرّره أكثر من مرة، ففي كل مرة أسئلة جديدة.
]

#part[Exam tips · نصائح للامتحان]
#tbl((1fr, 1fr),
  [*In English*], align(right)[*بالعربي*],
  [Read the whole question and *all four* answers.], align(right, text(lang: "ar", dir: rtl)[اقرأ السؤال كاملاً والخيارات الأربعة كلها.]),
  [Look for the key word: *To / Cc*, *Save / Save As*, *Font / Paragraph*.], align(right, text(lang: "ar", dir: rtl)[ابحث عن الكلمة المفتاحية في السؤال.]),
  [Not sure? Cross out the answers that are surely wrong.], align(right, text(lang: "ar", dir: rtl)[غير متأكد؟ استبعد الخيارات الخاطئة بالتأكيد أولاً.]),
  [Answer every question: there is no minus mark.], align(right, text(lang: "ar", dir: rtl)[أجب عن كل الأسئلة، فلا توجد علامة سالبة.]),
)

// ----------------------------------------------------------------- Unit 1
#unit(1, "Digital Skills, Apps, Accounts and Files", "Lecture 1 · Online activity 1")

#part[1. Digital skills and productivity]
- *Digital skills:* what you can do with a computer, a phone and apps (write a letter, add up prices, send a file). Almost every job needs them.
- *Productivity:* more useful work in less time. The computer does the simple, repeated work; you plan and check.
- Example: Excel adds 8 prices at once (*AutoSum*). When a price changes, Excel shows the new total by itself.

#part[2. The main productivity apps (Microsoft 365)]
An *office suite* is a set of apps that work together: *Microsoft 365* (or Google Workspace).
#tbl((22%, 28%, 50%),
  [*App*], [*Kind of app*], [*Main job*],
  [Word], [word processor], [letters, reports, CVs],
  [Excel], [spreadsheet], [numbers, lists, totals, charts],
  [PowerPoint], [presentation app], [slides for a talk],
  [Outlook], [e-mail and calendar], [messages, files to send, meetings],
  [OneDrive], [cloud storage], [your files on every device],
  [Teams], [chat and online meetings], [talk to people who are far away],
  [Copilot], [AI assistant], [ask in normal words; it writes and sums up],
)
#tip[A table of numbers goes to *Excel*, not Word: Excel calculates with no mistakes.]

#part[3. AI assistants]
- An *AI assistant* (Copilot, ChatGPT, Gemini) answers your request in normal words. Your request is a *prompt*.
- *Generative AI* makes new text or pictures. Good jobs: a *first draft*, a *summary*, *ideas*, a *translation*.
- AI makes mistakes (wrong facts, wrong numbers) and *sounds sure*. *Check every answer*; you are responsible.
- *Never* type personal data into an AI tool: an ID number, a card number, a phone number.

#part[4. Your account (Online activity 1)]
- *Authentication:* you prove the account is yours (a password, often a code on your phone).
- *Single sign-on (SSO):* one sign-in opens e-mail, the e-learning platform, Microsoft 365 and OneDrive. Risk: a stolen password opens everything.
- On a shared computer: never save your password; *Sign out* at the end (closing the browser is not enough); *Windows + L* locks the screen.

#part[5. Files, folders, paths and names]
- A *folder* keeps files and other folders. The *path* is the full address of a file: `C:\Users\Sara\Documents\Courses\cv.docx`. Two files can have the same name, never the same path.
- *Extensions:* `.docx` Word · `.xlsx` Excel · `.pptx` PowerPoint · `.jpg` photo · `.pdf` PDF · `.exe` program. The *last* extension is the real type: `photo.jpg.exe` is a program!
- *Good file names:* say what it is · no spaces (use `-` or `_`) · date as year-month-day · versions `v01`, `v02` (never "final final"). Example: `2026-11-12_english-talk_v03.pptx`.

#part[6. Cloud storage, sync and backup]
- *Cloud storage* (OneDrive, Google Drive): your files on the Internet; open them on any device after you sign in.
- *Sync* copies every change to all your devices, a *delete* too. The cloud *recycle bin* keeps deleted files for some days.
- A *backup* is an extra copy in a separate place (a USB stick). A mistake does not reach it.

#ar[
  - #strong[المهارات الرقمية:] ما تستطيع فعله بالحاسوب والهاتف والتطبيقات. #strong[الإنتاجية:] عمل مفيد أكثر في وقت أقل.
  - #strong[Word] للرسائل والتقارير، #strong[Excel] للأرقام والمجاميع، #strong[PowerPoint] للشرائح، #strong[Outlook] للبريد والتقويم، #strong[OneDrive] للتخزين السحابي، #strong[Teams] للمحادثة والاجتماعات.
  - #strong[المساعد الذكي] يكتب مسودات وملخصات وأفكاراً، لكنه يخطئ ويبدو واثقاً: تحقق من كل معلومة، ولا تكتب له بيانات شخصية أبداً.
  - #strong[المصادقة:] إثبات أن الحساب لك. #strong[الدخول الموحد:] تسجيل دخول واحد يفتح كل الخدمات (وخطره: كلمة مرور مسروقة تفتح كل شيء).
  - على حاسوب مشترك (في الجامعة): اضغط #strong[Sign out] في النهاية، و#strong[Windows + L] لقفل الشاشة.
  - #strong[المسار] هو العنوان الكامل للملف. #strong[الامتداد] يحدد نوع الملف، والامتداد الأخير هو الحقيقي (‎.exe برنامج).
  - الاسم الجيد للملف: يوضح المحتوى، بدون فراغات، التاريخ سنة-شهر-يوم، ورقم الإصدار v01.
  - #strong[المزامنة] تنسخ كل تغيير إلى كل الأجهزة حتى الحذف، أما #strong[النسخة الاحتياطية] فهي نسخة منفصلة لا يصلها الخطأ.
]

#words("digital-skills", "productivity", "office-suite", "cloud-storage", "ai-assistant", "generative-ai", "prompt",
  "authentication", "single-sign-on", "file-path", "file-extension", "synchronization", "backup")

// ----------------------------------------------------------------- Unit 2
#unit(2, "Search, Screenshots, AI and Your Phone", "Lecture 2 · Online activity 2")

#part[1. Search for a fact: the official source]
+ Type *2–4 keywords*, not a long sentence: _Israa University calendar_.
+ Read the *web address*: `.edu.jo` a university in Jordan · `.gov.jo` the government of Jordan · `microsoft.com` the company Microsoft.
+ Open the *official website*: the website of the organization that owns the fact (the university for exam dates).
+ Skip *Ad / Sponsored* results (paid), forums (opinions) and old pages: check the year.
#tip[The first result is not always right: it is often an ad. Read the web address first.]

#part[2. Screenshots]
#tbl((22%, 40%, 38%),
  [*Device*], [*Keys*], [*Where it goes*],
  [Windows], [*Windows + Shift + S* (Snipping Tool): drag a box], [the clipboard: *Ctrl + V* pastes it, *Ctrl + S* saves it],
  [Android], [*Power + Volume down*, together], [Photos / Gallery › Screenshots],
  [iPhone], [*Side button + Volume up*, together], [Photos › Screenshots],
)
- *Crop* it (keep only the part that matters) · *cover personal data* of other people · give it a *good name*: `exam-dates.png`.

#part[3. AI: check its facts and numbers]
- AI writes *likely* words: good for a *draft, summary, ideas, rewrite, translation*.
- Weak spots: *invented facts* (a *hallucination*: sounds sure but is wrong), *old information* (it learned up to a date), *wrong numbers*.
- The right tool: facts and dates → *search engine* and the official website · exact sums → *spreadsheet* · drafts → *AI assistant*.
- Five steps with AI: *ask → read → check → edit → use*.
- Example: AI says 12 pens × 0.25 JD = 3.50 JD. In Excel, `=12*0.25` gives *3.00 JD*: the AI was wrong.

#part[4. Your phone for study (Online activity 2)]
- *Calendar:* add the lecture with its date and time, and a *reminder* (Alert / Notification), for example 1 hour before; then *Save* (iPhone: ✓).
- *Scan* a paper homework into *one PDF*: Android → *Google Drive* (the camera button); iPhone → *Files* (••• › Scan Documents) or Notes. Name it well: `math-homework3.pdf`.

#part[5. A clear prompt: task, context, format]
#tbl((22%, 33%, 45%),
  [*Part*], [*It says …*], [*Example*],
  [*Task*], [what the AI must do], [_Write a short message to my club leader._],
  [*Context*], [the facts of your situation], [_I cannot come on Monday; I have an exam._],
  [*Format*], [how the answer must look], [_3 polite sentences._],
)
- Not right? Send a *follow-up prompt* in the same chat: _Make it shorter._ · _Write it in Arabic._

#ar[
  - للبحث: اكتب #strong[2–4 كلمات مفتاحية]، واقرأ عنوان الموقع، وافتح #strong[الموقع الرسمي] لصاحب المعلومة. ‎.edu.jo جامعة أردنية، ‎.gov.jo حكومة الأردن. تجاهل الإعلانات (Ad) والمنتديات والصفحات القديمة.
  - #strong[لقطة الشاشة:] في ويندوز #strong[Windows + Shift + S] (تذهب للحافظة)، في أندرويد #strong[Power + خفض الصوت#strong[، في الآيفون ]الزر الجانبي + رفع الصوت#strong[. ثم ]اقتصّها]، وغطِّ بيانات الآخرين، وأعطها اسماً جيداً.
  - الذكاء الاصطناعي قد #strong[يهلوس] (يخترع معلومات بثقة)، ومعلوماته قد تكون قديمة، ويخطئ في الأرقام. المواعيد من الموقع الرسمي، والمجاميع من إكسل، والمسودات من الذكاء الاصطناعي.
  - الخطوات الخمس: #strong[اسأل ← اقرأ ← تحقق ← عدّل ← استخدم].
  - على الهاتف: أضف المحاضرة إلى #strong[التقويم] مع #strong[تذكير]، وامسح الواجب الورقي إلى #strong[ملف PDF واحد] (Google Drive في أندرويد، Files في الآيفون).
  - الموجّه الواضح فيه: #strong[المهمة] (ماذا يفعل)، #strong[السياق] (معلومات موقفك)، #strong[الشكل] (كيف يبدو الجواب). وللتعديل أرسل #strong[موجّهاً متابعاً] في المحادثة نفسها.
]

#words("search-engine", "official-website", "screenshot", "snipping-tool", "crop", "hallucination",
  "reminder", "scan", "prompt-task", "prompt-context", "prompt-format", "follow-up-prompt")

// ----------------------------------------------------------------- Unit 3
#unit(3, "Office, E-mail, Meetings and Safety", "Lecture 3 · Online activity 3")

#part[1. The Office window and the ribbon]
- *Word* makes a *document* · *Excel* a *workbook* (one box is a *cell*: *B3* = column B, row 3) · *PowerPoint* a *presentation* of slides.
- *Title bar* (the file name) at the top · *ribbon* under it · *status bar* (the page, the zoom) at the bottom.
- The ribbon: *tabs* › *groups* › *commands*. Example: *Home › Font › Bold*.
#tbl((50%, 50%),
  [*You want to …*], [*Go to …*],
  [make text bold], [Home › Font › Bold],
  [center a title], [Home › Paragraph › Center],
  [add a table or a picture], [Insert › Tables / Pictures],
  [turn the page sideways], [Layout › Orientation],
  [save, print, share], [the *File* tab],
  [start from a ready design (*template*)], [File › New],
)

#part[2. Save, Save As, PDF and one shared file]
- *Save* (*Ctrl + S*) keeps the same file. *Save As* makes a *new copy* with a new name, place or format.
- *PDF* keeps its look on every device: for reading and printing (nobody changes it). `.docx .xlsx .pptx` can be changed.
- *AutoSave* saves every change, but *only for files in OneDrive*. On a USB stick or the desktop, press Ctrl + S often.
- Team work: keep *one file* in OneDrive and *Share* it: *Specific people · Can edit*. People change it at the same time (*co-editing*).
- A *comment* (Review › New Comment) is a note next to the text. *Version History* (File › Info) brings back older versions.
#tip[*Anyone with the link · Can edit* is a risk: the link can reach strangers, and they can change the file.]

#part[3. E-mail and meetings]
#tbl((24%, 76%),
  [*Part / button*], [*Use it for …*],
  [*To*], [the people who must *act*],
  [*Cc*], [the people who *only need to know*],
  [*Subject*], [a short title: _Agenda: staff meeting on Sunday_],
  [*Attachment*], [a file (the Inbox shows a *paperclip*). A big file (a 2 GB video) → a *OneDrive link*],
  [*Reply* / *Reply all*], [answer the sender only / everyone in To and Cc],
  [*Forward*], [send the e-mail *and its file* to a new person],
)
- A *meeting invitation*: a title, the time, the attendees and a room or an *online meeting* link (Teams, Meet, Zoom). Answers: *Accept · Tentative · Decline*. At the time: *Join*.

#part[4. Safety (Online activity 3)]
- *Strong password:* long (12+ characters), random words with a number and a symbol: `Blue-Camel-Rain-47`. Never a name, a birthday or `qwerty`. *One password for one account.*
- *Two-step verification:* after the password, a code or number on your phone. A sign-in that is not you → tap *No, it's not me*, then change the password.
- *Phishing:* a fake message that wants your password, a code or money. Signs: a strange sender, it *hurries* you ("in 24 hours"), a strange link, it asks for a password/PIN/code or offers a prize. → Do not tap; *touch and hold* a link to see its real address; *report it and delete it*.
- *App permissions:* give only what the app needs. A map: *Allow only while using the app*. A calculator or flashlight: *Don't allow*.
- *AI tools:* never a password, ID number, phone number, address or grades. Use made-up names: _Customer 1_.

#ar[
  - وورد يصنع #strong[مستنداً]، وإكسل #strong[مصنفاً] (الخلية B3 = العمود B والصف 3)، وباوربوينت #strong[عرضاً تقديمياً].
  - #strong[الشريط:] تبويبات ← مجموعات ← أوامر. الخط العريض في Home › Font، والإدراج (جدول أو صورة) في Insert، واتجاه الصفحة في Layout، والحفظ والطباعة والمشاركة في File، و#strong[القوالب] (ملفات جاهزة) في File › New.
  - #strong[Save] يحفظ الملف نفسه، و#strong[Save As] يصنع نسخة جديدة. #strong[PDF] يحافظ على شكله ولا يُعدَّل. #strong[الحفظ التلقائي] فقط لملفات OneDrive.
  - للعمل الجماعي: ملف واحد في OneDrive مشارك مع #strong[أشخاص محددين] بصلاحية #strong[Can edit]. #strong[التعليق] ملاحظة بجانب النص، و#strong[سجل الإصدارات] يعيد النسخ القديمة.
  - البريد: #strong[To] لمن سيقوم بالعمل، #strong[Cc] لمن يحتاج أن يعرف فقط، #strong[Reply all] للجميع، #strong[Forward] لإرسال الرسالة وملفها لشخص جديد، والملف الكبير يُرسل كرابط OneDrive.
  - دعوة الاجتماع: قبول (Accept) أو ربما (Tentative) أو رفض (Decline)، وفي الموعد اضغط #strong[Join].
  - كلمة مرور #strong[قوية وطويلة]، وكلمة مرور لكل حساب، و#strong[التحقق بخطوتين]. #strong[التصيّد:] رسالة مزيفة تستعجلك وتطلب كلمة المرور أو رمزاً أو مالاً: لا تضغط الرابط، أبلغ عنها واحذفها.
  - أذونات التطبيقات: أعطِ التطبيق ما يحتاجه فقط. ولا تكتب بيانات شخصية حقيقية في أدوات الذكاء الاصطناعي.
]

#words("workbook", "template", "ribbon", "save-as", "autosave", "co-editing", "doc-comment", "email-cc", "attachment",
  "email-forward", "meeting-invitation", "two-step-verification", "phishing", "app-permission")

// ----------------------------------------------------------------- Unit 4
#unit(4, "Word Documents", "Lecture 4 · Online activity 4")

#part[1. Text and paragraph formatting]
- *Text formatting* (*Home › Font*): font, size, *bold*, _italic_, underline, colour. It changes letters and words.
- *Paragraph formatting* (*Home › Paragraph*): *alignment* (left, center, right, *justified* = straight on both sides), *line spacing*, space after.
- First *select* the text, then click the command. For a paragraph, clicking inside it is enough.
#tip[If every line is bold, nothing stands out. Bold only one or two important words.]

#part[2. Styles and the Navigation Pane]
- A *style* is a saved set of formatting with a name. Change the style once → *all* the text with that style changes.
- *Title* (the name of the document, once) · *Heading 1* (main headings) · *Heading 2* (smaller headings under them) · *Normal* (the text).
- *View › Navigation Pane* shows a map of the headings; click one to jump to it.
#tip[A heading made "by hand" (bold and big) is normal text for Word: it is not in the Navigation Pane or the table of contents.]

#part[3. Lists, tables and pictures]
- *Bullets* for a list of things (water, a hat …); *Numbering* for steps in order.
- *Table* (*Insert › Table*) for information in rows and columns. The *header row* (the first row) names the columns. Rows = *1 header row + 1 row for each item*: a price list of 6 items → *7 rows, 2 columns*. *Tab* in the last cell adds a row; *Table Design* gives it a style.
- *Picture* (*Insert › Pictures*: This Device, Stock Images, Online Pictures). Resize from a *corner* (the shape stays right).
- *Text wrapping:* *In Line with Text* (a line of its own) · *Square* (the text flows around it).
- *Alt text* (right-click › View Alt Text): a short description that a screen reader reads aloud.
- Use your own photos or *Stock Images*: many pictures on the Internet belong to someone.

#part[4. A Word report (Online activity 4)]
#tbl((50%, 50%),
  [*You want …*], [*Do this*],
  [a table of contents], [Heading 1 for every heading, then *References › Table of Contents › Automatic Table 1*],
  [a header on every page], [*Insert › Header › Blank*: type it once, it is on *every page*],
  [page numbers], [*Insert › Page Number › Bottom of Page*: Word counts the pages (3 pages → the last is 3)],
  [the report as a PDF], [*File › Save As* › Save as type: *PDF (\*.pdf)* › Save],
)

#ar[
  - #strong[تنسيق النص] (Home › Font): الخط والحجم والعريض والمائل واللون. #strong[تنسيق الفقرة] (Home › Paragraph): المحاذاة وتباعد الأسطر. حدّد النص أولاً ثم اضغط الأمر.
  - #strong[النمط] تنسيق محفوظ باسم: #strong[Title] لاسم المستند، #strong[Heading 1] للعناوين الرئيسية، #strong[Heading 2] للفرعية، #strong[Normal] للنص. غيّر النمط مرة فيتغير كل نص يحمله.
  - #strong[جزء التنقل] (View › Navigation Pane) خريطة العناوين. العنوان المصنوع يدوياً بالعريض والحجم لا يظهر فيه ولا في الفهرس.
  - #strong[القائمة النقطية] للأشياء، و#strong[المرقّمة] للخطوات. #strong[الجدول] للمعلومات في صفوف وأعمدة، و#strong[صف العناوين] هو الصف الأول؛ عدد الصفوف = صف العناوين + صف لكل عنصر. Tab في آخر خلية يضيف صفاً.
  - #strong[الصورة] من Insert › Pictures، وتصغيرها من #strong[الزاوية]. #strong[Square] يجعل النص يلتف حولها، و#strong[النص البديل] وصف يقرؤه قارئ الشاشة. استخدم صورك أو Stock Images.
  - #strong[الفهرس] من تبويب #strong[References] ويعتمد على أنماط العناوين. #strong[الترويسة] و#strong[رقم الصفحة] من تبويب #strong[Insert] وتظهر في كل صفحة. #strong[PDF] من File › Save As.
]

#words("text-formatting", "paragraph-formatting", "alignment", "line-spacing", "style", "heading-style", "navigation-pane",
  "bulleted-list", "numbered-list", "word-table", "header-row", "text-wrapping", "alt-text", "table-of-contents",
  "header-footer", "page-number", "pdf")

#v(10pt)
#align(center)[
  #block(fill: soft, radius: 10pt, inset: 12pt, stroke: 0.6pt + accent2)[
    #grid(columns: (auto, 2.6cm), column-gutter: 14pt, align: horizon,
      [#text(weight: "bold", fill: accent)[Now practise!] \
       30 random questions, one hour, each answer with its reason. \
       #text(font: arabic, lang: "ar", dir: rtl)[تدرّب الآن: امتحان تجريبي من 30 سؤالاً خلال ساعة.] \
       #text(size: 8pt, fill: luma(90))[#link(prep-url)]],
      qrcode(prep-url, width: 2.6cm))
  ]
  #text(size: 10pt, weight: "bold")[Good luck! · بالتوفيق]
]
