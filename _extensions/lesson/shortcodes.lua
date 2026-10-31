-- Lesson shortcodes, shared by all courses.
--
--   {{< glossary vector position origin >}}
--     Bilingual word table from shared/glossary.yml (EN | AR | meaning).
--
--   {{< answer-space lines=3 >}}  /  {{< answer-space box=6 >}}
--     Homework: dotted lines (or an empty box, cm) to write the answer on.
--     Shown only when the homework page is printed.
--
--   {{< sim file="sims/x.html" poster="sims/x.png" title="Move the player" height="480" kind="game" >}}
--     HTML: live simulator in an iframe + "open full screen" link. `height` is
--           the start height; sims that load sim-base.js resize the iframe.
--     PDF:  poster image + QR code to the live page.
--     PPTX: poster image + QR code to the live page (students scan it in class).
--     kind="game": a mini-game (a small playable game for one concept); the
--     label says "Mini-game" instead of "Simulator".
--     layout="qr" (slides): only the QR code, to put in a column.
--     task="Show … Ask: why …?" (slides): one or two sentences that tell the
--     teacher what to show and what to ask; shown above the recording, so the
--     slide explains itself. Every Live demo and Game challenge slide has one.
--     Slides show a recording of the game being played instead of the poster
--     when it exists: sims/<name>.gif next to sims/<name>.html, or
--     recording="sims/other.gif" (made by shared/sims/recordings/).
--
--   {{< schedule >}}
--     Course page: every week of courses/<slug>/schedule.yml (`units:`), in
--     teaching order. A core week is a unit ("Unit N": Lecture N, Seminar N
--     or Online activity N, and Homework N); a filling week (`filling: true`)
--     is a "Practice week" with no new ideas, tagged "Flexible". Every
--     session is labelled "Lecture N", "Seminar N", "Practice N" or "Online
--     activity N"; practice sessions (and a seminar with `core: false`) are
--     tagged "Flexible". A ready session (its .qmd exists, no `draft: true`)
--     is bright and links its page, PDF and slides; the others are faded
--     ("coming soon"). The review profile shows drafts as ready. Files of a
--     week are in week-WW (WW = its syllabus week): lesson-NN, seminar-NN,
--     practice-NN, online-NN and homework-UU (UU = the unit).
--     Older schedules (`lectures:`, before units) are shown in pairs.
--
--   Lecture worksheets (a practical course; AUTHORING.md, "Lecture worksheets"):
--   {{< record "D2 shows" >}}  /  {{< record "What happened?" lines=2 >}}
--     The place to record the result of one step of an experiment
--     (lesson-NN-sheet.qmd). PDF: the label and a dotted line (or lines, or
--     box=4: an empty box, cm) to write on. Page: a text field; what the
--     student types stays in this browser only. Slides: nothing.
--   {{< experiment 2 >}}  /  {{< experiment results >}}
--     Interactive lesson (lesson-NN.qmd): Experiment 2 of the worksheet next
--     to it ("## Experiment 2 · …" in lesson-NN-sheet.qmd), in a box with its
--     steps, a text field and "Check your result" after each step; or its
--     "Table of results". The experiments are written once, in the worksheet.
--   {{< start-files >}}
--     The start files of the worksheet (`start-files:` in its front matter,
--     files in week-WW/files/): download buttons on the page, names and links
--     in the PDF.

local str = pandoc.utils.stringify

-- Paths -------------------------------------------------------------------

local function project_dir()
  if quarto.project and quarto.project.directory then
    return quarto.project.directory
  end
  return pandoc.system.get_working_directory()
end

-- Folder of the current document, relative to the project root ("" at root).
local function doc_rel_dir()
  local root = pandoc.path.normalize(project_dir())
  local dir = pandoc.path.normalize(pandoc.path.directory(quarto.doc.input_file))
  local rel = pandoc.path.make_relative(dir, root)
  if rel == "." then
    return ""
  end
  return (rel:gsub("\\", "/"))
end

-- website.site-url from _quarto.yml (shortcodes do not see project metadata).
local site_url_cache = nil

local function read_yaml(path)
  local f = io.open(path, "r")
  if not f then
    error("Cannot open " .. path)
  end
  local text = f:read("a")
  f:close()
  return pandoc.read("---\n" .. text .. "\n---\n", "markdown").meta
end

local function site_url()
  if site_url_cache then
    return site_url_cache
  end
  local config = read_yaml(pandoc.path.join({ project_dir(), "_quarto.yml" }))
  local url = config.website and config.website["site-url"] and str(config.website["site-url"]) or ""
  if url == "" then
    quarto.log.warning("website.site-url is not set in _quarto.yml; QR codes will use relative links")
  elseif not url:match("/$") then
    url = url .. "/"
  end
  site_url_cache = url
  return url
end

-- Escaping ----------------------------------------------------------------

local function typst_string(s)
  return '"' .. s:gsub("\\", "\\\\"):gsub('"', '\\"') .. '"'
end

local function html_attr(s)
  return (s:gsub("&", "&amp;"):gsub('"', "&quot;"):gsub("<", "&lt;"):gsub(">", "&gt;"))
end

-- QR images (for slides) ---------------------------------------------------
-- PowerPoint cannot draw a QR code itself, so we make a PNG with Quarto's
-- Typst and the same QR package as the PDF. Cached in .quarto/qr/ (not in git).

local function qr_png(url, caption, call)
  call = call or "Scan to try it"
  local dir = pandoc.path.join({ project_dir(), ".quarto", "qr" })
  pandoc.system.make_directory(dir, true)
  local base = pandoc.path.join({ dir, pandoc.utils.sha1(url .. "|" .. caption .. "|" .. call) })
  local png = base .. ".png"
  -- Image paths must be relative to the document.
  local docdir = pandoc.path.directory(quarto.doc.input_file)
  if not pandoc.path.is_absolute(docdir) then
    docdir = pandoc.path.join({ pandoc.system.get_working_directory(), docdir })
  end
  local abs = png
  if not pandoc.path.is_absolute(abs) then
    abs = pandoc.path.join({ pandoc.system.get_working_directory(), abs })
  end
  local rel = pandoc.path.make_relative(pandoc.path.normalize(abs), pandoc.path.normalize(docdir), true)
  local f = io.open(png, "r")
  if f then
    f:close()
    return rel
  end
  local typ = base .. ".typ"
  local out = io.open(typ, "w")
  out:write('#set page(width: auto, height: auto, margin: 10pt)\n',
    '#set text(font: "Noto Sans", size: 15pt, weight: "bold", fill: rgb("#24432c"))\n',
    '#import "@preview/tiaoma:0.3.0": qrcode\n',
    "#align(center)[#qrcode(", typst_string(url), ", width: 6cm)\n",
    "#v(4pt)\n", call, "\n#v(-6pt)\n#text(size: 11pt, weight: \"regular\", ", typst_string(caption), ")]\n")
  out:close()
  pandoc.pipe(quarto.config.cli_path(), { "typst", "compile", typ, png, "--ppi", "200" }, "")
  os.remove(typ)
  return rel
end

-- Glossary ----------------------------------------------------------------

local glossary_cache = nil

local function load_glossary()
  if glossary_cache then
    return glossary_cache
  end
  glossary_cache = read_yaml(pandoc.path.join({ project_dir(), "shared", "glossary.yml" }))
  return glossary_cache
end

local function arabic(text)
  if quarto.doc.is_format("html") then
    return pandoc.Span(pandoc.Str(text), { class = "ar", lang = "ar", dir = "rtl" })
  elseif quarto.doc.is_format("typst") then
    return pandoc.RawInline("typst",
      '#text(font: "Noto Naskh Arabic", lang: "ar", ' .. typst_string(text) .. ")")
  end
  return pandoc.Str(text)
end

-- HTML: one card per word (English, Arabic, meaning).
local function glossary_cards(args, terms)
  local cards = {}
  for _, arg in ipairs(args) do
    local key = str(arg)
    local t = terms[key]
    if not t then
      error("Glossary term '" .. key .. "' is missing from shared/glossary.yml")
    end
    table.insert(cards, string.format(
      '<div class="word-card"><div class="word-en">%s</div><span class="word-ar" lang="ar" dir="rtl">%s</span><div class="word-def">%s</div></div>',
      html_attr(str(t.en)), html_attr(str(t.ar)), html_attr(str(t.def or ""))))
  end
  return pandoc.RawBlock("html", '<div class="word-grid">' .. table.concat(cards, "") .. "</div>")
end

local function glossary(args)
  local terms = load_glossary()
  if quarto.doc.is_format("html") then
    return glossary_cards(args, terms)
  end
  -- Slides show keywords only (EN | AR); lessons add the meaning.
  local slides = quarto.doc.is_format("pptx")
  local header = {
    { pandoc.Plain("English") },
    { pandoc.Plain({ arabic("العربية") }) },
  }
  if not slides then
    table.insert(header, { pandoc.Plain("Meaning") })
  end
  local rows = {}
  for _, arg in ipairs(args) do
    local key = str(arg)
    local t = terms[key]
    if not t then
      error("Glossary term '" .. key .. "' is missing from shared/glossary.yml")
    end
    local row = {
      { pandoc.Plain({ pandoc.Strong(str(t.en)) }) },
      { pandoc.Plain({ arabic(str(t.ar)) }) },
    }
    if not slides then
      table.insert(row, { pandoc.Plain(str(t.def or "")) })
    end
    table.insert(rows, row)
  end
  local aligns = { pandoc.AlignLeft, pandoc.AlignRight, pandoc.AlignLeft }
  local widths = { 0.25, 0.25, 0.5 }
  if slides then
    aligns, widths = { pandoc.AlignLeft, pandoc.AlignRight }, { 0.5, 0.5 }
  end
  local tbl = pandoc.utils.from_simple_table(pandoc.SimpleTable({}, aligns, widths, header, rows))
  if slides then
    return tbl -- the pptx writer drops tables inside a Div
  end
  return pandoc.Div({ tbl }, { class = "glossary" })
end

-- Simulator ---------------------------------------------------------------

local function sim(kwargs)
  local file = str(kwargs.file)
  local poster = str(kwargs.poster)
  local title = str(kwargs.title)
  local height = str(kwargs.height)
  if file == "" or poster == "" then
    error("sim shortcode needs file= and poster=")
  end
  local game = str(kwargs.kind) == "game"
  local label = game and "Mini-game" or "Simulator"
  if title == "" then title = label end
  if height == "" then height = "480" end

  local rel = doc_rel_dir()
  local url = site_url() .. (rel ~= "" and (rel .. "/") or "") .. file
  local qr_only = str(kwargs.layout) == "qr"

  if qr_only and not quarto.doc.is_format("html") and not quarto.doc.is_format("typst") then
    return pandoc.Para({ pandoc.Image({}, qr_png(url, title, game and "Scan to play" or "Scan to try it")) })
  end

  if quarto.doc.is_format("html") then
    return pandoc.RawBlock("html", string.format([[
<figure class="sim">
  <iframe src="%s" title="%s" loading="lazy" style="height:%spx"></iframe>
  <figcaption><span class="sim-label">%s %s: %s</span><a href="%s" target="_blank" rel="noopener">Open full screen ↗</a></figcaption>
</figure>]], html_attr(file), html_attr(title), html_attr(height), game and "🕹" or "🎮", label, html_attr(title), html_attr(file)))

  elseif quarto.doc.is_format("typst") then
    return pandoc.RawBlock("typst", string.format([[
#import "@preview/tiaoma:0.3.0": qrcode
#block(width: 100%%, breakable: false, stroke: 0.6pt + rgb("#9aa5ae"), radius: 4pt, inset: 10pt)[
  #grid(
    columns: (1fr, 3.6cm),
    column-gutter: 12pt,
    align: horizon,
    align(center, image(%s, width: 80%%)),
    align(center)[
      #qrcode(%s, width: 3.2cm)
      #v(2pt)
      #text(size: 8pt)[Scan to %s]
    ],
  )
  #v(4pt)
  #text(size: 9pt)[*%s:* #%s — scan the QR code or open #link(%s)]
]
]], typst_string(poster), typst_string(url), game and "play" or "try it", label, typst_string(title), typst_string(url)))

  else
    -- pptx: the recording (or the poster) on the left, QR code on the right,
    -- so students see the game move and can scan it in class
    local picture = poster
    local rec = str(kwargs.recording)
    if rec == "" then rec = file:gsub("%.html$", ".gif") end
    local docdir = pandoc.path.directory(quarto.doc.input_file)
    local fh = io.open(pandoc.path.join({ docdir, rec }), "rb")
    if fh then fh:close(); picture = rec end
    local left = { pandoc.Para({ pandoc.Image({}, picture) }) }
    local right = { pandoc.Para({ pandoc.Image({}, qr_png(url, title, game and "Scan to play" or "Scan to try it")) }) }
    -- With a task, text comes before each picture: the writer then uses the
    -- "Comparison" layout (a line of text above each picture).
    local task = str(kwargs.task)
    if task ~= "" then
      table.insert(left, 1, pandoc.Para(pandoc.read(task, "markdown").blocks[1].content))
      table.insert(right, 1, pandoc.Para({ pandoc.Str(game and "Scan the QR code to play on your phone."
        or "Scan the QR code to try it on your phone.") }))
    end
    return pandoc.Div({
      pandoc.Div(left, { class = "column", width = "55%" }),
      pandoc.Div(right, { class = "column", width = "45%" }),
    }, { class = "columns" })
  end
end

-- Answer space (homework) -------------------------------------------------
-- {{< answer-space lines=3 >}}   dotted lines to write the answer on
-- {{< answer-space box=6 >}}     an empty box, 6 cm high (for a drawing)
-- Hidden on screen, shown when the homework page is printed (web only).

local function answer_space(kwargs)
  local lines = tonumber(str(kwargs.lines)) or 0
  local box = tonumber(str(kwargs.box)) or 0
  if lines == 0 and box == 0 then lines = 3 end
  if quarto.doc.is_format("html") then
    if box > 0 then
      return pandoc.RawBlock("html", string.format(
        '<div class="answer-space answer-box" style="height:%gcm" aria-hidden="true"></div>', box))
    end
    return pandoc.RawBlock("html",
      '<div class="answer-space" aria-hidden="true">' .. string.rep('<div class="answer-line"></div>', lines) .. "</div>")
  end
  return pandoc.Null()
end

-- Course schedule (course page) ---------------------------------------------

local function read_text(path)
  local f = io.open(path, "r")
  if not f then return nil end
  local text = f:read("a")
  f:close()
  return text
end

-- Front matter of a .qmd as pandoc meta (nil if the file is missing).
local function front_matter(path)
  local text = read_text(path)
  if not text then return nil end
  local fm = text:match("^%-%-%-\n(.-)\n%-%-%-")
  if not fm then return {} end
  return pandoc.read("---\n" .. fm .. "\n---\n", "markdown").meta
end

local function review_profile()
  local prof = quarto.project and quarto.project.profile
  if type(prof) == "table" then
    for _, p in ipairs(prof) do if str(p) == "review" then return true end end
  end
  return (os.getenv("QUARTO_PROFILE") or ""):find("review") ~= nil
end

-- A page is ready when its file exists and it is not a draft (drafts count in review).
local function ready(meta)
  if not meta then return false end
  if meta.draft == true or str(meta.draft or "") == "true" then
    return review_profile()
  end
  return true
end

local function file_exists(path)
  local f = io.open(path, "r")
  if f then f:close() return true end
  return false
end

-- Prefix of the downloaded file names (math_lecture5.pdf): course.file-prefix,
-- the same names as banner.lua and download_names.py.
local function file_prefix(meta)
  local course = meta and meta.course or {}
  if course["file-prefix"] then return str(course["file-prefix"]) end
  return (str(course.slug or "course"):gsub("%-", "_"))
end

-- Folder of a unit: week-WW, WW = its syllabus week (older schedules: the
-- pair of lectures). The name is internal and never shown.
local function pair_dir(pair)
  return string.format("week-%02d", pair)
end

-- One session of a unit: { stem, link text, file names, label }.
local SESSION = {
  lecture = { stem = "lesson", go = "Open lecture →", label = "Lecture", file = "lecture", pdf = "PDF" },
  seminar = { stem = "seminar", go = "Open seminar →", label = "Seminar", file = "seminar", pdf = "Worksheet" },
  practice = { stem = "practice", go = "Open practice →", label = "Practice", file = "practice", pdf = "Worksheet" },
  online = { stem = "online", go = "Open activity →", label = "Online activity", file = "online" },
}

-- Practice sessions (filling weeks) are flexible unless `core: true`; a
-- seminar is core unless `core: false`; lectures and online activities are core.
local function is_flexible(kind, x)
  local core = x.core
  if core ~= nil then core = core == true or str(core) == "true" end
  if kind == "practice" then return core ~= true end
  if kind == "seminar" then return core == false end
  return false
end

local function session_row(dir, wdir, prefix, slides_public, x, in_filling)
  local kind = str(x.kind or "lecture")
  local s = SESSION[kind]
  if not s then error("schedule.yml: unknown kind '" .. kind .. "' (lecture, seminar, practice, online)") end
  local n = tonumber(str(x.n))
  local stem = string.format("%s-%02d", s.stem, n)
  local base = pandoc.path.join({ dir, wdir, stem })
  local fm = front_matter(base .. ".qmd")
  local ok = ready(fm)
  local flexible = is_flexible(kind, x) and not in_filling
  local file = string.format("%s/%s_%s%d", wdir, prefix, s.file, n)
  local links
  if ok then
    local parts = { string.format('<a class="sl-go" href="%s/%s.html">%s</a>', wdir, stem, s.go) }
    if kind == "online" then
      table.insert(parts, string.format('<a class="sl-file" href="%s_tasks.pdf">Tasks PDF</a>', file))
      local bits = {}
      if fm.marks then table.insert(bits, str(fm.marks) .. " marks") end
      if fm.due then table.insert(bits, "due " .. str(fm.due)) end
      if #bits > 0 then
        table.insert(parts, '<span class="sl-due">' .. html_attr(table.concat(bits, " · ")) .. "</span>")
      end
    else
      -- A lecture with a worksheet (lesson-NN-sheet.qmd): the worksheet is the
      -- main document of the session, the notes are a short reference.
      local sheet = file_exists(base .. "-sheet.qmd")
      if sheet then
        table.insert(parts, string.format('<a class="sl-file" href="%s_sheet.pdf">Worksheet</a>', file))
      end
      if file_exists(base .. "-book.qmd") then
        table.insert(parts, string.format('<a class="sl-file" href="%s.pdf">%s</a>', file, sheet and "Notes" or s.pdf))
      end
      if slides_public and file_exists(base .. "-slides.qmd") then
        table.insert(parts, string.format('<a class="sl-file" href="%s_slides.pptx">Slides</a>', file))
      end
    end
    links = '<span class="sl-links">' .. table.concat(parts, "") .. "</span>"
  else
    links = '<span class="sl-soon">Coming soon</span>'
  end
  local tags = ""
  if flexible then tags = tags .. ' <span class="sl-tag sl-flex">Flexible</span>' end
  if kind == "online" then tags = tags .. ' <span class="sl-tag">💻 Online</span>' end
  return string.format(
    '<div class="sl sl-%s %s"><span class="sl-kind">%s %d</span><span class="sl-title">%s%s</span>%s</div>',
    kind, ok and "is-ready" or "is-soon", s.label, n, html_attr(str(x.title)), tags, links), ok
end

local function schedule_units(dir, prefix, slides_public, units)
  local out = { '<div class="schedule">' }
  for _, u in ipairs(units) do
    local filling = u.filling == true or str(u.filling or "") == "true"
    local unit = tonumber(str(u.unit or ""))
    local wdir = pair_dir(tonumber(str(u.week)))
    local rows, any_ready = {}, false
    for _, x in ipairs(u.sessions or {}) do
      local row, ok = session_row(dir, wdir, prefix, slides_public, x, filling)
      table.insert(rows, row)
      any_ready = any_ready or ok
    end
    local hw_html = ""
    if unit and not filling then
      local hw = front_matter(pandoc.path.join({ dir, wdir, string.format("homework-%02d.qmd", unit) }))
      if ready(hw) then
        local bits = {}
        if hw.marks then table.insert(bits, str(hw.marks) .. " marks") end
        if hw.due then table.insert(bits, "due " .. str(hw.due)) end
        hw_html = string.format('<a class="sw-hw" href="%s/homework-%02d.html">📝 Homework %d%s</a>',
          wdir, unit, unit, #bits > 0 and (" · " .. html_attr(table.concat(bits, " · "))) or "")
      end
    end
    local head
    if filling then
      head = '<span class="sw-week">Practice week</span><span class="sl-tag sl-flex">Flexible</span>'
    else
      head = string.format('<span class="sw-week">Unit %d</span>', unit or 0)
    end
    table.insert(out, string.format(
      '<section class="sw sw-unit%s %s"><header class="sw-head">%s%s</header>%s</section>',
      filling and " sw-filling" or "", any_ready and "has-ready" or "", head, hw_html, table.concat(rows, "")))
  end
  table.insert(out, "</div>")
  return pandoc.RawBlock("html", table.concat(out, "\n"))
end

local function schedule(meta)
  if not quarto.doc.is_format("html") then return pandoc.Null() end
  local dir = pandoc.path.directory(quarto.doc.input_file)
  local prefix = file_prefix(meta)
  local data = read_yaml(pandoc.path.join({ dir, "schedule.yml" }))
  local config = read_yaml(pandoc.path.join({ project_dir(), "_quarto.yml" }))
  local slides_public = config["slides-public"] == true
  if data.units then return schedule_units(dir, prefix, slides_public, data.units) end
  local lectures = data.lectures or {}
  local out = { '<div class="schedule">' }
  -- Two lectures, then their homework: one section per pair.
  for first = 1, #lectures, 2 do
    local pair = (first + 1) // 2
    local wdir = pair_dir(pair)
    local rows, nums = {}, {}
    for idx = first, math.min(first + 1, #lectures) do
      local l = lectures[idx]
      local n = tonumber(str(l.n))
      table.insert(nums, n)
      local stem = string.format("lesson-%02d", n)
      local base = pandoc.path.join({ dir, wdir, stem })
      local fm = front_matter(base .. ".qmd")
      local ok = ready(fm)
      local online = l.online == true or str(l.online or "") == "true"
        or (fm and (fm.online == true or str(fm.online or "") == "true"))
      local links
      if ok and online then
        local href = wdir .. "/" .. stem
        local bits = {}
        if fm.marks then table.insert(bits, str(fm.marks) .. " marks") end
        if fm.due then table.insert(bits, "due " .. str(fm.due)) end
        local parts = {
          string.format('<a class="sl-go" href="%s.html">Open activity →</a>', href),
          string.format('<a class="sl-file" href="%s/%s_lecture%d_tasks.pdf">Tasks PDF</a>', wdir, prefix, n),
        }
        if #bits > 0 then
          table.insert(parts, '<span class="sl-due">' .. html_attr(table.concat(bits, " · ")) .. "</span>")
        end
        links = '<span class="sl-links">' .. table.concat(parts, "") .. "</span>"
      elseif ok then
        local href = wdir .. "/" .. stem
        local parts = { string.format('<a class="sl-go" href="%s.html">Open lecture →</a>', href) }
        if file_exists(base .. "-book.qmd") then
          table.insert(parts, string.format('<a class="sl-file" href="%s/%s_lecture%d.pdf">PDF</a>', wdir, prefix, n))
        end
        if slides_public and file_exists(base .. "-slides.qmd") then
          table.insert(parts, string.format('<a class="sl-file" href="%s/%s_lecture%d_slides.pptx">Slides</a>', wdir, prefix, n))
        end
        links = '<span class="sl-links">' .. table.concat(parts, "") .. "</span>"
      else
        links = '<span class="sl-soon">Coming soon</span>'
      end
      table.insert(rows, string.format(
        '<div class="sl %s%s"><span class="sl-num">%02d</span><span class="sl-title">%s%s</span>%s</div>',
        ok and "is-ready" or "is-soon", online and " is-online" or "", n, html_attr(str(l.title)),
        online and ' <span class="sl-tag">💻 Online</span>' or "", links))
    end
    local hw = front_matter(pandoc.path.join({ dir, wdir, string.format("homework-%02d.qmd", pair) }))
    local hw_html = ""
    if ready(hw) then
      local bits = {}
      if hw.marks then table.insert(bits, str(hw.marks) .. " marks") end
      if hw.due then table.insert(bits, "due " .. str(hw.due)) end
      hw_html = string.format('<a class="sw-hw" href="%s/homework-%02d.html">📝 Homework %d%s</a>',
        wdir, pair, pair, #bits > 0 and (" · " .. html_attr(table.concat(bits, " · "))) or "")
    end
    local any_ready = false
    for _, r in ipairs(rows) do if r:find("is%-ready") then any_ready = true end end
    local label = #nums > 1 and string.format("Lectures %d–%d", nums[1], nums[#nums])
      or string.format("Lecture %d", nums[1])
    table.insert(out, string.format(
      '<section class="sw %s"><header class="sw-head"><span class="sw-week">%s</span>%s</header>%s</section>',
      any_ready and "has-ready" or "", label, hw_html, table.concat(rows, "")))
  end
  table.insert(out, "</div>")
  return pandoc.RawBlock("html", table.concat(out, "\n"))
end

-- Lecture worksheets ------------------------------------------------------
-- The worksheet of a lecture (lesson-NN-sheet.qmd, a PDF) is the main document
-- of a face-to-face session in a practical course: numbered experiments, each
-- with numbered steps, a place to record the result of every step, and a
-- short table of results. The interactive lesson shows the same experiments,
-- read from the worksheet when the page is rendered.

-- The worksheet of this page: lesson-NN.qmd (or lesson-NN-sheet.qmd itself).
local function sheet_path()
  local input = quarto.doc.input_file
  local stem = pandoc.path.split_extension(pandoc.path.filename(input))
  stem = stem:gsub("%-sheet$", "")
  return pandoc.path.join({ pandoc.path.directory(input), stem .. "-sheet.qmd" })
end

-- The arguments of a shortcode written in a text: '"D2 shows" lines=2'.
local function parse_args(s)
  local label = s:match('^%s*"(.-)"') or s:match("^%s*'(.-)'")
  local kw = {}
  for k, v in s:gmatch('(%w+)="(.-)"') do kw[k] = v end
  for k, v in s:gmatch("(%w+)=(%d+%.?%d*)") do kw[k] = v end
  return label, kw
end

local function record_html(label, lines, box)
  local field
  if box > 0 then
    field = string.format('<textarea class="record-input" style="height:%gcm" aria-label="%s"></textarea>',
      box, html_attr(label))
  elseif lines > 1 then
    field = string.format('<textarea class="record-input" rows="%d" aria-label="%s"></textarea>',
      lines, html_attr(label))
  else
    field = string.format('<input class="record-input" type="text" autocomplete="off" spellcheck="false" aria-label="%s">',
      html_attr(label))
  end
  return string.format('<div class="record"><span class="record-label">%s</span>%s</div>', html_attr(label), field)
end

local function record_typst(label, lines, box)
  local head = string.format('box(fill: accent2.lighten(62%%), radius: 3pt, inset: (x: 5pt, y: 2.5pt), '
    .. 'text(size: 8pt, weight: "bold", fill: accent.darken(45%%), %s))', typst_string(label))
  local dots = 'line(length: 100%, stroke: (paint: luma(140), thickness: 0.7pt, dash: "dotted"))'
  local out = { '#block(width: 100%, breakable: false, above: 6pt, below: 10pt)[' }
  if box > 0 then
    table.insert(out, "#" .. head)
    table.insert(out, string.format('#v(3pt)#rect(width: 100%%, height: %gcm, radius: 4pt, '
      .. 'stroke: (paint: luma(160), thickness: 0.7pt, dash: "dashed"))', box))
  else
    table.insert(out, string.format("#grid(columns: (auto, 1fr), column-gutter: 6pt, align: bottom, %s, %s)", head, dots))
    for _ = 2, lines do table.insert(out, "#v(0.55cm)#" .. dots) end
  end
  return table.concat(out, "") .. "]"
end

local function record(args, kwargs)
  local label = str(args[1] or "")
  if label == "" then label = str(kwargs.label or "") end
  if label == "" then label = "Your result" end
  local lines = tonumber(str(kwargs.lines)) or 1
  local box = tonumber(str(kwargs.box)) or 0
  if quarto.doc.is_format("html") then
    return pandoc.RawBlock("html", record_html(label, lines, box))
  elseif quarto.doc.is_format("typst") then
    return pandoc.RawBlock("typst", record_typst(label, lines, box))
  end
  return pandoc.Null()
end

-- The "## …" section of a .qmd text whose title matches `pattern`: its title
-- and its text up to the next "## " heading (or nil).
local function md_section(text, pattern)
  text = (text:gsub("^%-%-%-\n.-\n%-%-%-\n", "", 1))
  local title, body = nil, {}
  for line in (text .. "\n"):gmatch("([^\n]*)\n") do
    local h = line:match("^## (.-)%s*$")
    if h then
      if title then break end
      if h:match(pattern) then title = h end
    elseif title then
      table.insert(body, line)
    end
  end
  return title, title and table.concat(body, "\n") or nil
end

local function check_details(div)
  local blocks = pandoc.Blocks({ pandoc.RawBlock("html",
    '<details class="check"><summary>Check your result</summary><div class="check-body">') })
  blocks:extend(div.content)
  blocks:insert(pandoc.RawBlock("html", "</div></details>"))
  return blocks
end

local function experiment(args)
  if not quarto.doc.is_format("html") then return pandoc.Null() end
  local which = str(args[1] or "")
  local path = sheet_path()
  local text = read_text(path)
  if not text then error("experiment shortcode: the worksheet " .. path .. " is missing") end
  local results = which == "results"
  local title, body = md_section(text, results and "^Table of results" or ("^Experiment " .. which .. "%f[^%d]"))
  if not body then
    error("experiment shortcode: no \"## " .. (results and "Table of results" or ("Experiment " .. which))
      .. "\" in " .. path)
  end
  title = (title:gsub("%s*%b{}%s*$", ""))
  -- A record field becomes its text field (with the indentation of its step);
  -- the simulators are already in the section of the page.
  body = body:gsub("([ \t]*){{<%s*record%s+(.-)%s*>}}", function(indent, a)
    local label, kw = parse_args(a)
    local html = record_html(label or "Your result", tonumber(kw.lines) or 1, tonumber(kw.box) or 0)
    return indent .. "```{=html}\n" .. indent .. html .. "\n" .. indent .. "```"
  end)
  body = body:gsub("{{<%s*sim%s.-%s*>}}", "")
  local doc = pandoc.read(body, "markdown")
  doc = doc:walk({ Div = function(d) if d.classes:includes("check") then return check_details(d) end end })
  local head
  if results then
    head = '<span class="exp-title">Table of results</span>'
  else
    local num, rest = title:match("^(Experiment %d+)%s*·%s*(.*)$")
    head = string.format('<span class="exp-num">%s</span><span class="exp-title">%s</span>',
      html_attr(num or title), html_attr(rest or ""))
  end
  local blocks = pandoc.Blocks({ pandoc.RawBlock("html", string.format(
    '<div class="experiment%s" id="%s"><div class="exp-head">%s</div><div class="exp-body">',
    results and " exp-results" or "", results and "experiment-results" or ("experiment-" .. which), head)) })
  blocks:extend(doc.blocks)
  blocks:insert(pandoc.RawBlock("html", "</div></div>"))
  return blocks
end

-- The start files: `start-files:` (name, about) in the worksheet's front
-- matter; the files are in the folder files/ next to it.
local function start_files(meta)
  local files = meta and meta["start-files"]
  if not files then
    local fm = front_matter(sheet_path())
    files = fm and fm["start-files"]
  end
  if not files or #files == 0 then return pandoc.Null() end
  if quarto.doc.is_format("html") then
    local items = {}
    for _, f in ipairs(files) do
      local name = str(f.name or f)
      table.insert(items, string.format(
        '<li><a class="sf-file" href="files/%s" download>⬇ %s</a><span class="sf-about">%s</span></li>',
        html_attr(name), html_attr(name), html_attr(str(f.about or ""))))
    end
    return pandoc.RawBlock("html", '<div class="start-files"><div class="sf-title">📂 Start files</div><ul>'
      .. table.concat(items, "") .. '</ul><p class="sf-note">The same data for every student. '
      .. "Download each file, then open it in its app.</p></div>")
  elseif quarto.doc.is_format("typst") then
    local rel = doc_rel_dir()
    local items = {}
    for _, f in ipairs(files) do
      local name = str(f.name or f)
      local url = site_url() .. (rel ~= "" and (rel .. "/") or "") .. "files/" .. name
      table.insert(items, string.format("- #link(%s)[#strong(%s)]: #%s", typst_string(url), typst_string(name),
        typst_string(str(f.about or ""))))
    end
    return pandoc.RawBlock("typst", string.format([[
#block(width: 100%%, breakable: false, fill: accent2.lighten(88%%), radius: 6pt, inset: (x: 10pt, y: 8pt), stroke: 0.6pt + accent2.darken(5%%))[
#text(weight: "bold", fill: accent.darken(35%%))[Start files] #h(4pt) #text(size: 8.5pt, fill: luma(80))[The same data for every student. Download them from the interactive lesson (QR code above).]
%s
]
]], table.concat(items, "\n")))
  end
  return pandoc.Null()
end

return {
  ["schedule"] = function(_, _, meta) return schedule(meta) end,
  ["answer-space"] = function(_, kwargs) return answer_space(kwargs) end,
  ["glossary"] = function(args) return glossary(args) end,
  ["sim"] = function(_, kwargs) return sim(kwargs) end,
  ["record"] = function(args, kwargs) return record(args, kwargs) end,
  ["experiment"] = function(args) return experiment(args) end,
  ["start-files"] = function(_, _, meta) return start_files(meta) end,
}
