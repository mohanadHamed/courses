-- Adds the "About this lesson" box at the top of every lesson (HTML + PDF):
-- course name and code, diploma line, week/lesson and the ILOs covered.
-- Data comes from metadata: `course` (courses/<slug>/_metadata.yml),
-- `diploma-line` (_quarto.yml), and `week`, `lesson`, `ilos` (ILO codes such
-- as [A1, B1], front matter).
-- In HTML it also links the printable PDF (same file name, .pdf).

local str = pandoc.utils.stringify

local function line(label, value)
  return pandoc.Plain({ pandoc.Strong(label .. ": "), pandoc.Str(value) })
end

function Pandoc(doc)
  local meta = doc.meta
  if not meta.course then
    return nil
  end

  local course = meta.course
  local items = {
    line("Course", str(course.title) .. " (" .. str(course.code) .. ")"),
  }
  if meta["diploma-line"] then
    table.insert(items, line("Program", str(meta["diploma-line"])))
  end
  if meta.week and meta.lesson then
    table.insert(items, line("Week", str(meta.week) .. " · Lesson " .. str(meta.lesson)))
  end

  if quarto.doc.is_format("html") then
    local stem = pandoc.path.split_extension(pandoc.path.filename(quarto.doc.input_file))
    table.insert(items, pandoc.Plain({
      pandoc.Strong("Print: "),
      pandoc.Link("Download PDF", stem .. ".pdf"),
    }))
  end

  local content = { pandoc.BulletList(pandoc.List(items):map(function(b) return { b } end)) }

  if meta.ilos and #meta.ilos > 0 then
    table.insert(content, pandoc.Para({ pandoc.Strong("Course ILOs in this lesson:") }))
    -- `ilos: [A1, B1]` are codes; the official text is in course.ilos.
    local known = course.ilos or {}
    local ilos = pandoc.List(meta.ilos):map(function(ilo)
      local code = str(ilo)
      if not known[code] then
        error("ILO '" .. code .. "' is not in course.ilos (courses/<slug>/_metadata.yml)")
      end
      return { pandoc.Plain({ pandoc.Strong(code), pandoc.Str(" — " .. str(known[code])) }) }
    end)
    table.insert(content, pandoc.BulletList(ilos))
  else
    quarto.log.warning("Lesson has no `ilos:` in front matter: " .. quarto.doc.input_file)
  end

  local box = quarto.Callout({
    type = "note",
    title = "About this lesson",
    content = pandoc.Blocks(content),
    appearance = "simple",
    icon = false,
  })
  doc.blocks:insert(1, box)
  return doc
end
