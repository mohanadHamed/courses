-- Page header for lessons and course pages (lesson-html and lesson-typst).
--
-- Lesson (has `lesson:`) or homework (has `homework:`, `due:`, `marks:`):
--   HTML: hero header (course, title, week/lesson/time chips, PDF and slides
--         buttons) + "Today you will learn" card with the ILOs.
--   PDF:  passes theme values to the Typst template (title band) + ILO card.
-- Course page (no `lesson:`): HTML hero with course name, code and tagline.
--
-- Data: `course` (courses/<slug>/_metadata.yml), `diploma-line` and
-- `slides-public` (_quarto.yml), `week`, `lesson`, `ilos` (ILO codes such as
-- [A1, B1]) and `description` (front matter).

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

local function theme_style(course)
  return string.format("<style>:root{--accent:%s;--accent2:%s;}</style>",
    esc(str(course.accent)), esc(str(course.accent2)))
end

-- Chips under the title: lesson (week, lesson, time) or homework (week, number, due, marks).
local function page_chips(meta, course)
  local chips = {}
  if meta.week then table.insert(chips, "Week " .. str(meta.week)) end
  if meta.homework then
    table.insert(chips, "Homework " .. str(meta.homework))
    if meta.due then table.insert(chips, "Due: " .. str(meta.due)) end
    if meta.marks then table.insert(chips, str(meta.marks) .. " marks") end
  else
    if meta.lesson then table.insert(chips, "Lesson " .. str(meta.lesson)) end
    if course.minutes then table.insert(chips, "⏱ " .. str(course.minutes) .. " min") end
  end
  return chips
end

local function ilo_title(meta)
  if meta.homework then return "This homework practises" end
  return "Intended learning outcomes"
end

-- HTML --------------------------------------------------------------------

local function html_lesson(doc, course)
  local meta = doc.meta
  local stem = pandoc.path.split_extension(pandoc.path.filename(quarto.doc.input_file))
  local dir = pandoc.path.directory(quarto.doc.input_file)

  -- Lesson: the PDF is the lesson notes (lesson-NN-book.qmd), the main study text.
  -- Homework PDF is the printed page itself (homework_pdf.py), so both match.
  local buttons = {}
  if meta.homework then
    table.insert(buttons, string.format('<a class="hero-btn" href="%s.pdf" download>⬇ Download PDF</a>', esc(stem)))
  elseif file_exists(pandoc.path.join({ dir, stem .. "-book.qmd" })) then
    table.insert(buttons, string.format('<a class="hero-btn" href="%s-book.pdf">⬇ Lesson notes (PDF)</a>', esc(stem)))
  end
  if meta.homework then
    table.insert(buttons,
      '<button type="button" class="hero-btn hero-btn-ghost" onclick="window.print()">🖨 Print homework</button>')
  end
  local slides = meta["slides-public"] == true and not meta.homework
    and file_exists(pandoc.path.join({ dir, stem .. "-slides.qmd" }))
  if slides then
    table.insert(buttons, string.format(
      '<a class="hero-btn hero-btn-ghost" href="%s-slides.pptx">▶ Lecture slides</a>', esc(stem)))
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
<header class="lesson-hero theme-%s">
  <div class="hero-shapes" aria-hidden="true"><i></i><i></i><i></i></div>
  <a class="hero-course" href="../index.html">%s · %s</a>
  <h1 class="hero-title">%s</h1>
  %s
  <div class="hero-chips">%s</div>
  <div class="hero-actions">%s</div>
  %s
</header>]],
    theme_style(course), esc(str(course.theme or "arcade")),
    esc(str(course.title)), esc(str(course.code)),
    esc(str(meta.title)),
    desc ~= "" and ('<p class="hero-sub">' .. esc(desc) .. "</p>") or "",
    table.concat(chip_html, ""),
    table.concat(buttons, ""),
    slides and '<p class="hero-note">Study from the lesson notes (PDF). Practise on this page. The slides are a short summary for revision.</p>' or "")

  local blocks = { pandoc.RawBlock("html", hero) }
  if meta.homework then
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
  local chips = { "Course " .. esc(str(course.code)), "2 lessons a week" }
  if course.minutes then table.insert(chips, "⏱ " .. esc(str(course.minutes)) .. " min each") end
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
  local web = stem:match("^(.-)%-book$")
  if not web then return nil end
  local root = quarto.project and quarto.project.directory or pandoc.system.get_working_directory()
  local rel = pandoc.path.make_relative(pandoc.path.normalize(pandoc.path.directory(input)), pandoc.path.normalize(root))
  local url = site_url() .. (rel ~= "." and (rel:gsub("\\", "/") .. "/") or "") .. web .. ".html"
  return pandoc.RawBlock("typst", string.format([[
#import "@preview/tiaoma:0.3.0": qrcode
#block(width: 100%%, breakable: false, radius: 8pt, inset: 10pt, stroke: 0.6pt + accent.lighten(55%%))[
  #grid(columns: (1fr, 2.4cm), column-gutter: 12pt, align: horizon,
    [
      #text(weight: "bold", fill: accent.darken(25%%))[Interactive lesson]
      #v(1pt)
      #text(size: 9.5pt)[These notes are the main study text of the lecture. The interactive lesson
      practises the same sections with questions that give instant feedback, and runs the
      simulators and mini-games marked with a QR code in the text.]
      #v(1pt)
      #text(size: 8.5pt, fill: luma(90))[#link(%s)]
    ],
    qrcode(%s, width: 2.3cm),
  )
]
]], typst_string(url), typst_string(url)))
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
    blocks = (meta.lesson or meta.homework) and html_lesson(doc, course) or html_course(doc, course)
  elseif quarto.doc.is_format("typst") and (meta.lesson or meta.homework) then
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
