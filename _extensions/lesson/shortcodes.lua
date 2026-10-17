-- Lesson shortcodes, shared by all courses.
--
--   {{< glossary vector position origin >}}
--     Bilingual word table from shared/glossary.yml (EN | AR | meaning).
--
--   {{< sim file="sims/x.html" poster="sims/x.png" title="Move the player" height="480" >}}
--     HTML: live simulator in an iframe + "open full screen" link. `height` is
--           the start height; sims that load sim-base.js resize the iframe.
--     PDF:  poster image + QR code to the live page.
--     PPTX: poster image + link.

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

local function glossary(args)
  local terms = load_glossary()
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
  if title == "" then title = "Simulator" end
  if height == "" then height = "480" end

  local rel = doc_rel_dir()
  local url = site_url() .. (rel ~= "" and (rel .. "/") or "") .. file

  if quarto.doc.is_format("html") then
    return pandoc.RawBlock("html", string.format([[
<figure class="sim">
  <iframe src="%s" title="%s" loading="lazy" style="height:%spx"></iframe>
  <figcaption><strong>Simulator:</strong> %s · <a href="%s" target="_blank" rel="noopener">Open full screen ↗</a></figcaption>
</figure>]], html_attr(file), html_attr(title), html_attr(height), html_attr(title), html_attr(file)))

  elseif quarto.doc.is_format("typst") then
    return pandoc.RawBlock("typst", string.format([[
#import "@preview/tiaoma:0.3.0": qrcode
#block(width: 100%%, breakable: false, stroke: 0.6pt + rgb("#9aa5ae"), radius: 4pt, inset: 10pt)[
  #grid(
    columns: (1fr, 3.6cm),
    column-gutter: 12pt,
    align: horizon,
    image(%s, width: 100%%),
    align(center)[
      #qrcode(%s, width: 3.2cm)
      #v(2pt)
      #text(size: 8pt)[Scan to try it]
    ],
  )
  #v(4pt)
  #text(size: 9pt)[*Simulator:* #%s — scan the QR code or open #link(%s)]
]
]], typst_string(poster), typst_string(url), typst_string(title), typst_string(url)))

  else
    -- pptx: poster and link side by side on one slide
    return pandoc.Div({
      pandoc.Div({ pandoc.Para({ pandoc.Image({}, poster) }) }, { class = "column", width = "60%" }),
      pandoc.Div({
        pandoc.Para({ pandoc.Strong(title) }),
        pandoc.Para({ pandoc.Link(url, url) }),
      }, { class = "column", width = "40%" }),
    }, { class = "columns" })
  end
end

return {
  ["glossary"] = function(args) return glossary(args) end,
  ["sim"] = function(_, kwargs) return sim(kwargs) end,
}
