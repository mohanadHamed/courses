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
      if file_exists(base .. "-book.qmd") then
        table.insert(parts, string.format('<a class="sl-file" href="%s.pdf">%s</a>', file, s.pdf))
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

return {
  ["schedule"] = function(_, _, meta) return schedule(meta) end,
  ["answer-space"] = function(_, kwargs) return answer_space(kwargs) end,
  ["glossary"] = function(args) return glossary(args) end,
  ["sim"] = function(_, kwargs) return sim(kwargs) end,
}
