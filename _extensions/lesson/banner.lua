-- Page header for lessons and course pages (lesson-html and lesson-typst).
--
-- Lesson (has `lesson:`):
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

-- HTML --------------------------------------------------------------------

local function html_lesson(doc, course)
  local meta = doc.meta
  local stem = pandoc.path.split_extension(pandoc.path.filename(quarto.doc.input_file))
  local dir = pandoc.path.directory(quarto.doc.input_file)

  local buttons = { string.format(
    '<a class="hero-btn" href="%s.pdf">⬇ Download PDF</a>', esc(stem)) }
  local slides_public = meta["slides-public"] == true
  if slides_public and file_exists(pandoc.path.join({ dir, stem .. "-slides.qmd" })) then
    table.insert(buttons, string.format(
      '<a class="hero-btn hero-btn-ghost" href="%s-slides.pptx">▶ Lecture slides</a>', esc(stem)))
  end

  local chips = {}
  if meta.week then table.insert(chips, "Week " .. esc(str(meta.week))) end
  if meta.lesson then table.insert(chips, "Lesson " .. esc(str(meta.lesson))) end
  if course.minutes then table.insert(chips, "⏱ " .. esc(str(course.minutes)) .. " min") end
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
    slides_public and '<p class="hero-note">Slides are a short summary for class. Study from this page or the PDF.</p>' or "")

  local blocks = { pandoc.RawBlock("html", hero) }

  local ilos = lesson_ilos(meta, course)
  if #ilos > 0 then
    local items = {}
    for _, i in ipairs(ilos) do
      table.insert(items, string.format('<li><span class="ilo-code">%s</span> %s</li>', esc(i[1]), esc(i[2])))
    end
    table.insert(blocks, pandoc.RawBlock("html", string.format([[
<div class="ilo-card">
  <div class="ilo-title">🎯 Today you will learn</div>
  <ul>%s</ul>
  <div class="ilo-foot">Course ILOs · %s</div>
</div>]], table.concat(items, ""), esc(str(meta["diploma-line"] or "")))))
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

local function typst_lesson(doc, course)
  local meta = doc.meta
  -- Values for the title band in typst-template.typ (via typst-show.typ).
  meta.lessontheme = {
    accent = raw('rgb(' .. typst_string(str(course.accent)) .. ')'),
    accent2 = raw('rgb(' .. typst_string(str(course.accent2)) .. ')'),
    course = raw(typst_string(str(course.title) .. " · " .. str(course.code))),
    chips = raw("(" .. typst_string("Week " .. str(meta.week or "")) .. ", "
      .. typst_string("Lesson " .. str(meta.lesson or "")) .. ", "
      .. typst_string(str(course.minutes or "") .. " min") .. ",)"),
    program = raw(typst_string(str(meta["diploma-line"] or ""))),
  }

  local ilos = lesson_ilos(meta, course)
  if #ilos == 0 then return {} end
  local rows = {}
  for _, i in ipairs(ilos) do
    table.insert(rows, string.format(
      '  #box(fill: accent, radius: 3pt, inset: (x: 4pt, y: 2pt))[#text(fill: white, weight: "bold", size: 9pt, %s)] #h(4pt) #%s\n',
      typst_string(i[1]), typst_string(i[2])))
  end
  return { pandoc.RawBlock("typst", string.format([[
#block(width: 100%%, fill: accent.lighten(96%%), radius: 8pt, inset: 12pt, stroke: (left: 3pt + accent))[
  #text(weight: "bold", fill: accent.darken(15%%))[Today you will learn]
  #v(2pt)
%s]
]], table.concat(rows, "  #v(2pt)\n"))) }
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
    blocks = meta.lesson and html_lesson(doc, course) or html_course(doc, course)
  elseif quarto.doc.is_format("typst") and meta.lesson then
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
