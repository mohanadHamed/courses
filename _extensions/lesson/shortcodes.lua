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
--
--   {{< schedule >}}
--     Course page: all 16 weeks from courses/<slug>/schedule.yml, two lessons
--     a week. A ready lesson (its .qmd exists, no `draft: true`) is bright and
--     links its page, PDF and slides; the others are faded ("coming soon").
--     The review profile shows drafts as ready.

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
    -- pptx: poster on the left, QR code on the right, so students can scan it in class
    return pandoc.Div({
      pandoc.Div({ pandoc.Para({ pandoc.Image({}, poster) }) }, { class = "column", width = "55%" }),
      pandoc.Div({
        pandoc.Para({ pandoc.Image({}, qr_png(url, title, game and "Scan to play" or "Scan to try it")) }),
      }, { class = "column", width = "45%" }),
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

local function schedule()
  if not quarto.doc.is_format("html") then return pandoc.Null() end
  local dir = pandoc.path.directory(quarto.doc.input_file)
  local data = read_yaml(pandoc.path.join({ dir, "schedule.yml" }))
  local config = read_yaml(pandoc.path.join({ project_dir(), "_quarto.yml" }))
  local slides_public = config["slides-public"] == true
  local out = { '<div class="schedule">' }
  local ready_count = 0
  for _, w in ipairs(data.weeks or {}) do
    local week = tonumber(str(w.week))
    local wdir = string.format("week-%02d", week)
    local rows = {}
    for _, l in ipairs(w.lessons or {}) do
      local n = tonumber(str(l.n))
      local stem = string.format("lesson-%02d", n)
      local base = pandoc.path.join({ dir, wdir, stem })
      local ok = ready(front_matter(base .. ".qmd"))
      local links = ""
      if ok then
        ready_count = ready_count + 1
        local href = wdir .. "/" .. stem
        local parts = { string.format('<a class="sl-go" href="%s.html">Open lesson →</a>', href) }
        if file_exists(base .. "-book.qmd") then
          table.insert(parts, string.format('<a class="sl-file" href="%s-book.pdf">PDF</a>', href))
        end
        if slides_public and file_exists(base .. "-slides.qmd") then
          table.insert(parts, string.format('<a class="sl-file" href="%s-slides.pptx">Slides</a>', href))
        end
        links = '<span class="sl-links">' .. table.concat(parts, "") .. "</span>"
      else
        links = '<span class="sl-soon">Coming soon</span>'
      end
      table.insert(rows, string.format(
        '<div class="sl %s"><span class="sl-num">%02d</span><span class="sl-title">%s</span>%s</div>',
        ok and "is-ready" or "is-soon", n, html_attr(str(l.title)), links))
    end
    if w.exam then
      table.insert(rows, string.format('<div class="sl is-exam"><span class="sl-num">✎</span><span class="sl-title">%s</span></div>',
        html_attr(str(w.exam))))
    end
    local hw = front_matter(pandoc.path.join({ dir, wdir, string.format("homework-%02d.qmd", week) }))
    local hw_html = ""
    if ready(hw) then
      local bits = {}
      if hw.marks then table.insert(bits, str(hw.marks) .. " marks") end
      if hw.due then table.insert(bits, "due " .. str(hw.due)) end
      hw_html = string.format('<a class="sw-hw" href="%s/homework-%02d.html">📝 Homework %d%s</a>',
        wdir, week, week, #bits > 0 and (" · " .. html_attr(table.concat(bits, " · "))) or "")
    end
    local any_ready = false
    for _, r in ipairs(rows) do if r:find("is%-ready") then any_ready = true end end
    table.insert(out, string.format(
      '<section class="sw %s"><header class="sw-head"><span class="sw-week">Week %d</span>%s</header>%s</section>',
      any_ready and "has-ready" or "", week, hw_html, table.concat(rows, "")))
  end
  table.insert(out, "</div>")
  return pandoc.RawBlock("html", table.concat(out, "\n"))
end

return {
  ["schedule"] = function() return schedule() end,
  ["answer-space"] = function(_, kwargs) return answer_space(kwargs) end,
  ["glossary"] = function(args) return glossary(args) end,
  ["sim"] = function(_, kwargs) return sim(kwargs) end,
}
