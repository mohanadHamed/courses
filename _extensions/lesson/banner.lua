-- Page header for lessons and course pages (lesson-html and lesson-typst).
--
-- A session page (AUTHORING.md, "Units and sessions"): lecture (`lesson: N`),
-- seminar (`seminar: N`), practice session (`practice: N`, Digital Skills),
-- online activity (`online: N`, with `due:` and `marks:`; blended courses;
-- older pages: `lesson: N` and `online: true`) or homework (`homework: U`,
-- the unit, with `due:` and `marks:`):
--   HTML: hero header (course, title, lecture/time chips, PDF and slides
--         buttons) + "Today you will learn" card with the ILOs.
--   PDF:  passes theme values to the Typst template (title band) + ILO card.
-- A lecture of a practical course can have a worksheet (lesson-NN-sheet.qmd;
-- AUTHORING.md, "Lecture worksheets"): the page shows a "Worksheet (PDF)"
-- button first, and the worksheet PDF has a goal card (the ILOs) and a QR
-- card to the page, where every step has its result.
-- Course page (no `lesson:`): HTML hero with course name, code and tagline.
--
-- Data: `course` (courses/<slug>/_metadata.yml), `diploma-line` and
-- `slides-public` (_quarto.yml), the session number, `ilos` (ILO codes such as
-- [A1, B1]) and `description` (front matter). What a seminar practises, whether
-- it is core or flexible, and the lectures of a homework's unit come from
-- courses/<slug>/schedule.yml.

local str = pandoc.utils.stringify

local function esc(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

local function typst_string(s)
  return '"' .. s:gsub("\\", "\\\\"):gsub('"', '\\"') .. '"'
end

local function file_exists(path)
  local f = io.open(path, "r")
  if f then f:close() return true end
  return false
end

-- { {code, text}, ... } from `ilos:` codes, checked against course.ilos.
local function lesson_ilos(meta, course)
  local out = {}
  if not meta.ilos or #meta.ilos == 0 then
    quarto.log.warning("Lesson has no `ilos:` in front matter: " .. quarto.doc.input_file)
    return out
  end
  local known = course.ilos or {}
  for _, ilo in ipairs(meta.ilos) do
    local code = str(ilo)
    if not known[code] then
      error("ILO '" .. code .. "' is not in course.ilos (courses/<slug>/_metadata.yml)")
    end
    table.insert(out, { code, str(known[code]) })
  end
  return out
end

-- File names that students download (download_names.py renames the rendered
-- files to match): math_lecture5.pdf, math_lecture5_slides.pptx,
-- math_seminar2.pdf, math_seminar2_slides.pptx, math_homework1.pdf,
-- digital_skills_practice3.pdf, digital_skills_online4_tasks.pdf (the printed
-- online activity), digital_skills_lecture6_sheet.pdf (the worksheet of a
-- lecture). The prefix is course.file-prefix.
local STEM_NAMES = { lesson = "lecture", seminar = "seminar", practice = "practice", online = "online" }

local function download_names(course, stem)
  local prefix = course["file-prefix"] and str(course["file-prefix"])
    or (str(course.slug or "course"):gsub("%-", "_"))
  local hw = stem:match("^homework%-(%d+)$")
  local kind, n = stem:match("^(%a+)%-(%d+)$")
  local name = kind and STEM_NAMES[kind]
  local base = name and string.format("%s_%s%d", prefix, name, tonumber(n))
  return {
    homework = hw and string.format("%s_homework%d.pdf", prefix, tonumber(hw)) or (stem .. ".pdf"),
    notes = base and (base .. ".pdf") or (stem .. "-book.pdf"),
    slides = base and (base .. "_slides.pptx") or (stem .. "-slides.pptx"),
    tasks = base and (base .. "_tasks.pdf") or (stem .. ".pdf"),
    sheet = base and (base .. "_sheet.pdf") or (stem .. "-sheet.pdf"),
  }
end

local function number(v)
  return v ~= nil and tonumber(str(v)) or nil
end

-- The worksheet of a lecture (lesson-NN-sheet.qmd) rather than its notes.
local function is_sheet()
  local stem = pandoc.path.split_extension(pandoc.path.filename(quarto.doc.input_file))
  return stem:match("%-sheet$") ~= nil
end

-- An online activity of a blended course: one page with digital content and
-- tasks to submit, printed like a homework (homework_pdf.py).
local function is_online(meta)
  if meta.online == nil or meta.online == false then return false end
  return number(meta.online) ~= nil or meta.online == true or str(meta.online) == "true"
end

-- The session of a page: { kind = "lecture" | "seminar" | "practice" |
-- "online" | "homework", n = its number, label = "Seminar 2" }, or nil.
local LABELS = { lecture = "Lecture", seminar = "Seminar", practice = "Practice", online = "Online activity", homework = "Homework" }

local function session_of(meta)
  local kind, n
  if meta.homework then kind, n = "homework", number(meta.homework)
  elseif meta.seminar then kind, n = "seminar", number(meta.seminar)
  elseif meta.practice then kind, n = "practice", number(meta.practice)
  elseif is_online(meta) and number(meta.online) then kind, n = "online", number(meta.online)
  elseif is_online(meta) then kind, n = "online", number(meta.lesson)   -- older pages
  elseif meta.lesson then kind, n = "lecture", number(meta.lesson)
  else return nil end
  local label = LABELS[kind] .. (n and (" " .. n) or "")
  if kind == "online" and not number(meta.online) then label = "Lecture " .. (n or "") end
  return { kind = kind, n = n, label = label }
end

-- courses/<slug>/schedule.yml (next to the course page, or the folder above
-- week-WW), or nil.
local function read_schedule()
  local dir = pandoc.path.directory(quarto.doc.input_file)
  local f = io.open(pandoc.path.join({ dir, "schedule.yml" }), "r")
    or io.open(pandoc.path.join({ pandoc.path.directory(dir), "schedule.yml" }), "r")
  if not f then return nil end
  local text = f:read("a")
  f:close()
  return pandoc.read("---\n" .. text .. "\n---\n", "markdown").meta
end

-- "Lecture 4", "Lectures 4–5", "Lectures 1, 3 and 6".
local function lectures_text(ns)
  if #ns == 0 then return nil end
  if #ns == 1 then return "Lecture " .. ns[1] end
  local run = true
  for i = 2, #ns do if ns[i] ~= ns[i - 1] + 1 then run = false end end
  if run then return string.format("Lectures %d–%d", ns[1], ns[#ns]) end
  local head = {}
  for i = 1, #ns - 1 do table.insert(head, tostring(ns[i])) end
  return "Lectures " .. table.concat(head, ", ") .. " and " .. ns[#ns]
end

-- From schedule.yml: the unit of the session, what it practises, core or not.
-- Returns { unit = 3, practises = "Lectures 4–5", core = true, lectures = "…" }.
local function schedule_info(sess)
  local out = { core = true }
  local data = sess and read_schedule()
  if not data or not data.units then return out end
  for _, u in ipairs(data.units) do
    local lectures = {}
    local found = false
    for _, x in ipairs(u.sessions or {}) do
      local kind = str(x.kind or "lecture")
      if kind == "lecture" then table.insert(lectures, number(x.n)) end
      if kind == sess.kind and number(x.n) == sess.n then
        found = true
        -- A practice session (a filling week) is flexible unless `core: true`;
        -- a seminar is core unless `core: false`.
        if kind == "practice" then
          out.core = x.core == true or str(x.core or "") == "true"
        else
          out.core = not (x.core == false or str(x.core or "") == "false")
        end
        local ps = {}
        for _, p in ipairs(x.practises or {}) do table.insert(ps, number(p)) end
        out.practises = lectures_text(ps)
      end
    end
    if sess.kind == "homework" and number(u.unit) == sess.n then found = true end
    if found then
      out.unit = number(u.unit)
      out.lectures = lectures_text(lectures)
      return out
    end
  end
  return out
end

-- Pages that print as tasks with answer space: homework and online activities.
local function is_printed(meta)
  return meta.homework or is_online(meta)
end

local function theme_style(course)
  return string.format("<style>:root{--accent:%s;--accent2:%s;}</style>",
    esc(str(course.accent)), esc(str(course.accent2)))
end

-- Chips under the title: the session (number, what it practises, time) or
-- homework (number, the lectures of its unit, due, marks). Never a week:
-- courses count sessions.
local function page_chips(meta, course)
  local chips = {}
  local sess = session_of(meta)
  if not sess then return chips end
  local info = schedule_info(sess)
  if sess.kind == "homework" then
    table.insert(chips, sess.label)
    if info.lectures then
      table.insert(chips, "After " .. info.lectures)
    elseif sess.n then
      table.insert(chips, string.format("After lectures %d–%d", 2 * sess.n - 1, 2 * sess.n))
    end
    if meta.due then table.insert(chips, "Due: " .. str(meta.due)) end
    if meta.marks then table.insert(chips, str(meta.marks) .. " marks") end
  elseif sess.kind == "online" then
    table.insert(chips, sess.label)
    table.insert(chips, "💻 Online")
    if meta.due then table.insert(chips, "Due: " .. str(meta.due)) end
    if meta.marks then table.insert(chips, str(meta.marks) .. " marks") end
  else
    if (sess.kind == "seminar" or sess.kind == "practice") and info.practises then
      table.insert(chips, sess.label .. " · practises " .. info.practises)
    else
      table.insert(chips, sess.label)
    end
    if sess.kind ~= "lecture" and not info.core then table.insert(chips, "Flexible") end
    if course.blended then table.insert(chips, "🏫 Face-to-face") end
    if course.minutes then table.insert(chips, "⏱ " .. str(course.minutes) .. " min") end
    if sess.kind == "lecture" and is_sheet() then table.insert(chips, "Worksheet") end
  end
  return chips
end

-- A flexible seminar or practice session is held when time allows.
local function flexible_note(meta)
  local sess = session_of(meta)
  if not sess or (sess.kind ~= "seminar" and sess.kind ~= "practice") then return nil end
  if schedule_info(sess).core then return nil end
  local what = sess.kind == "seminar" and "seminar" or "practice session"
  return string.format("This %s is held in class when time allows. If it is not held, study it at home: every answer is on this page.", what)
end

local function ilo_title(meta)
  if meta.homework then return "This homework practises" end
  if is_sheet() then return "Goal of this worksheet" end
  if is_online(meta) then return "This online activity practises" end
  if meta.seminar then return "This seminar practises" end
  if meta.practice then return "This practice session practises" end
  return "Intended learning outcomes"
end

-- HTML --------------------------------------------------------------------

local function hero_note(meta, slides, online, sheet)
  local lines = {}
  if sheet then
    table.insert(lines, "In class, follow the worksheet (PDF): do each experiment on the computer and record your results. "
      .. "On this page every step has its result. The lesson notes (PDF) are a short reference.")
  elseif online then
    table.insert(lines, "Work through the steps on this page, then do the tasks and submit them on the university e-learning platform.")
  elseif meta.seminar or meta.practice then
    table.insert(lines, "No new ideas today: you apply the lectures you had. Do each activity alone, then open \"Check your result\".")
  elseif slides then
    table.insert(lines, "Study from the lesson notes (PDF). Practise on this page. The slides are a short summary for revision.")
  end
  local flex = flexible_note(meta)
  if flex then table.insert(lines, flex) end
  if #lines == 0 then return "" end
  return '<p class="hero-note">' .. esc(table.concat(lines, " ")) .. "</p>"
end

local function html_lesson(doc, course)
  local meta = doc.meta
  local stem = pandoc.path.split_extension(pandoc.path.filename(quarto.doc.input_file))
  local dir = pandoc.path.directory(quarto.doc.input_file)
  local names = download_names(course, stem)

  -- Lesson: the PDF is the lesson notes (lesson-NN-book.qmd), the main study text.
  -- Homework PDF is the printed page itself (homework_pdf.py), so both match.
  local buttons = {}
  local online = is_online(meta)
  -- A lecture with a worksheet: the worksheet is the main document of the session.
  local sheet = meta.lesson and not online and file_exists(pandoc.path.join({ dir, stem .. "-sheet.qmd" }))
  if meta.homework then
    table.insert(buttons, string.format('<a class="hero-btn" href="%s" download>⬇ Download PDF</a>', esc(names.homework)))
  elseif online then
    table.insert(buttons, string.format('<a class="hero-btn" href="%s" download>⬇ Download tasks (PDF)</a>', esc(names.tasks)))
  elseif file_exists(pandoc.path.join({ dir, stem .. "-book.qmd" })) then
    if sheet then
      table.insert(buttons, string.format('<a class="hero-btn" href="%s">⬇ Worksheet (PDF)</a>', esc(names.sheet)))
    end
    table.insert(buttons, string.format('<a class="hero-btn%s" href="%s">⬇ %s (PDF)</a>', sheet and " hero-btn-ghost" or "",
      esc(names.notes), (meta.seminar or meta.practice) and "Worksheet" or "Lesson notes"))
  end
  if meta.homework then
    table.insert(buttons,
      '<button type="button" class="hero-btn hero-btn-ghost" onclick="window.print()">🖨 Print homework</button>')
  elseif online then
    table.insert(buttons,
      '<button type="button" class="hero-btn hero-btn-ghost" onclick="window.print()">🖨 Print tasks</button>')
  end
  local slides = meta["slides-public"] == true and not is_printed(meta)
    and file_exists(pandoc.path.join({ dir, stem .. "-slides.qmd" }))
  if slides then
    local kind = meta.seminar and "Seminar" or (meta.practice and "Practice" or "Lecture")
    table.insert(buttons, string.format(
      '<a class="hero-btn hero-btn-ghost" href="%s">▶ %s slides</a>', esc(names.slides), kind))
  end

  local chips = {}
  for _, c in ipairs(page_chips(meta, course)) do table.insert(chips, esc(c)) end
  local chip_html = {}
  for _, c in ipairs(chips) do
    table.insert(chip_html, '<span class="hero-chip">' .. c .. "</span>")
  end
  table.insert(chip_html, '<span class="hero-chip hero-progress" id="lesson-progress" hidden></span>')

  local desc = meta.description and str(meta.description) or ""
  local hero = string.format([[
%s
<header class="lesson-hero theme-%s%s">
  <div class="hero-shapes" aria-hidden="true"><i></i><i></i><i></i></div>
  <a class="hero-course" href="../index.html">%s · %s</a>
  <h1 class="hero-title">%s</h1>
  %s
  <div class="hero-chips">%s</div>
  <div class="hero-actions">%s</div>
  %s
</header>]],
    theme_style(course), esc(str(course.theme or "arcade")), online and " online-activity" or "",
    esc(str(course.title)), esc(str(course.code)),
    esc(str(meta.title)),
    desc ~= "" and ('<p class="hero-sub">' .. esc(desc) .. "</p>") or "",
    table.concat(chip_html, ""),
    table.concat(buttons, ""),
    hero_note(meta, slides, online, sheet))

  local blocks = { pandoc.RawBlock("html", hero) }
  if is_printed(meta) then
    -- Only on paper: a line for the name and the student number.
    table.insert(blocks, pandoc.RawBlock("html",
      '<div class="print-only hw-name"><span>Name:</span><i></i><span>Student number:</span><i></i></div>'))
  end

  local ilos = lesson_ilos(meta, course)
  if #ilos > 0 then
    local items = {}
    for _, i in ipairs(ilos) do
      table.insert(items, string.format('<li><span class="ilo-code">%s</span> %s</li>', esc(i[1]), esc(i[2])))
    end
    table.insert(blocks, pandoc.RawBlock("html", string.format([[
<div class="ilo-card">
  <div class="ilo-title">🎯 %s</div>
  <ul>%s</ul>
  <div class="ilo-foot">Course ILOs · %s</div>
</div>]], ilo_title(meta), table.concat(items, ""), esc(str(meta["diploma-line"] or "")))))
  end
  return blocks
end

local function html_course(doc, course)
  local meta = doc.meta
  local chips = { "Course " .. esc(str(course.code)) }
  local units = (read_schedule() or {}).units ~= nil
  if course.blended then
    table.insert(chips, units and "Blended: a lecture or practice session + an online activity in each unit"
      or "Blended: 1 lab lecture + 1 online activity each week")
  else
    table.insert(chips, units and "Lectures, seminars and one homework in each unit" or "Homework after every 2 lectures")
  end
  if course.minutes then
    table.insert(chips, "⏱ " .. esc(str(course.minutes)) .. (course.blended and " min lab lecture" or " min each"))
  end
  local chip_html = {}
  for _, c in ipairs(chips) do
    table.insert(chip_html, '<span class="hero-chip">' .. c .. "</span>")
  end
  return { pandoc.RawBlock("html", string.format([[
%s
<header class="lesson-hero course-hero theme-%s">
  <div class="hero-shapes" aria-hidden="true"><i></i><i></i><i></i></div>
  <span class="hero-course">%s</span>
  <h1 class="hero-title">%s</h1>
  <div class="hero-chips">%s</div>
</header>]],
    theme_style(course), esc(str(course.theme or "arcade")),
    esc(str(meta["diploma-line"] or "")),
    esc(str(course.title)),
    table.concat(chip_html, ""))) }
end

-- Typst -------------------------------------------------------------------

local function raw(s) return pandoc.RawInline("typst", s) end

-- website.site-url from _quarto.yml, with a final "/".
local function site_url()
  local root = quarto.project and quarto.project.directory or pandoc.system.get_working_directory()
  local f = io.open(pandoc.path.join({ root, "_quarto.yml" }), "r")
  if not f then return "" end
  local text = f:read("a")
  f:close()
  local url = text:match('site%-url:%s*"([^"]+)"') or ""
  if url ~= "" and not url:match("/$") then url = url .. "/" end
  return url
end

-- Lesson notes (lesson-NN-book.qmd): a card with a QR code to the interactive lesson.
local function web_lesson_card(meta)
  local input = quarto.doc.input_file
  local stem = pandoc.path.split_extension(pandoc.path.filename(input))
  local web = stem:match("^(.-)%-book$") or stem:match("^(.-)%-sheet$")
  if not web then return nil end
  local sheet = stem:match("%-sheet$") ~= nil
  local root = quarto.project and quarto.project.directory or pandoc.system.get_working_directory()
  local rel = pandoc.path.make_relative(pandoc.path.normalize(pandoc.path.directory(input)), pandoc.path.normalize(root))
  local url = site_url() .. (rel ~= "." and (rel:gsub("\\", "/") .. "/") or "") .. web .. ".html"
  local seminar = meta.seminar or meta.practice
  local head = seminar and "Interactive page" or "Interactive lesson"
  local text = sheet
    and "Do each experiment on the computer and write your result after each step. The interactive lesson has the start files and the same experiments, with a field for each result and \"Check your result\" after every step. The results are also at the end of this worksheet: look only after you try."
    or seminar
    and "This worksheet is a self-test: the results of the activities are at the end. The interactive page has the same activities with \"Check your result\" and questions that give instant feedback."
    or "These notes are the main study text of the lecture and a self-test: the results are at the end. The interactive lesson practises the same sections with questions that give instant feedback and their reasons, and runs the simulators and mini-games marked with a QR code in the text."
  return pandoc.RawBlock("typst", string.format([[
#import "@preview/tiaoma:0.3.0": qrcode
#block(width: 100%%, breakable: false, radius: 8pt, inset: 10pt, stroke: 0.6pt + accent.lighten(55%%))[
  #grid(columns: (1fr, 2.4cm), column-gutter: 12pt, align: horizon,
    [
      #text(weight: "bold", fill: accent.darken(25%%))[%s]
      #v(1pt)
      #text(size: 9.5pt)[%s]
      #v(1pt)
      #text(size: 8.5pt, fill: luma(90))[#link(%s)]
    ],
    qrcode(%s, width: 2.3cm),
  )
]
]], head, text, typst_string(url), typst_string(url)))
end

local function typst_lesson(doc, course)
  local meta = doc.meta
  -- Values for the title band in typst-template.typ (via typst-show.typ).
  meta.lessontheme = {
    accent = raw('rgb(' .. typst_string(str(course.accent)) .. ')'),
    accent2 = raw('rgb(' .. typst_string(str(course.accent2)) .. ')'),
    course = raw(typst_string(str(course.title) .. " · " .. str(course.code))),
    chips = raw("(" .. table.concat((function()
      local out = {}
      for _, c in ipairs(page_chips(meta, course)) do table.insert(out, typst_string(c)) end
      return out
    end)(), ", ") .. ",)"),
    program = raw(typst_string(str(meta["diploma-line"] or ""))),
  }

  local ilos = lesson_ilos(meta, course)
  local card = web_lesson_card(meta)
  if #ilos == 0 then return card and { card } or {} end
  local rows = {}
  for _, i in ipairs(ilos) do
    table.insert(rows, string.format(
      '  #box(fill: accent, radius: 3pt, inset: (x: 4pt, y: 2pt))[#text(fill: white, weight: "bold", size: 9pt, %s)] #h(4pt) #%s\n',
      typst_string(i[1]), typst_string(i[2])))
  end
  return { pandoc.RawBlock("typst", string.format([[
#block(width: 100%%, fill: accent.lighten(96%%), radius: 8pt, inset: 12pt, stroke: (left: 3pt + accent))[
  #text(weight: "bold", fill: accent.darken(15%%))[%s]
  #v(2pt)
%s]
]], ilo_title(meta), table.concat(rows, "  #v(2pt)\n"))), card }
end

-- Main --------------------------------------------------------------------

function Pandoc(doc)
  local meta = doc.meta
  local course = meta.course
  if not course then
    return nil
  end

  local blocks
  if quarto.doc.is_format("html") then
    blocks = session_of(meta) and html_lesson(doc, course) or html_course(doc, course)
  elseif quarto.doc.is_format("typst") and session_of(meta) then
    blocks = typst_lesson(doc, course)
  else
    return nil
  end

  for i = #blocks, 1, -1 do
    doc.blocks:insert(1, blocks[i])
  end
  doc.meta = meta
  return doc
end
