-- Lesson notes (lesson-NN-book.qmd, seminar-NN-book.qmd; lesson-typst): textbook parts.
--
--   ::: {.answers}       Short answers to the end-of-chapter exercises:
--   1. …                 small text at the end of the PDF.
--   :::
--
--   ::: {.lead}          The opening paragraph of the chapter, a little larger.
--   …
--   :::
--
--   ::: {.check}         The result of a Do it task or a seminar activity. The
--   …                    notes are a self-test: the result is taken out of the
--   :::                  lesson and printed at the end, in "Results of the Do it
--                        tasks" (Digital Skills: "Results of the Lab tasks"; a
--                        seminar or practice session: "Results of the
--                        activities"), under the title of its box.
--
--   ::: {.prompt}        A starter prompt of a "Task with AI" box: a dashed box.
--   …
--   :::

local str = pandoc.utils.stringify

local results = {}      -- { label = "1.2 · Do it · Add two arrows", blocks = {...} }
local section = nil     -- "1.2" of the current ## heading
local box = nil         -- title of the current callout
local lab = false       -- a result of a "Lab task" box (Digital Skills)

local function is_typst()
  return quarto.doc.is_format("typst")
end

local function wrap(prefix, content)
  local blocks = pandoc.Blocks({ pandoc.RawBlock("typst", prefix) })
  blocks:extend(content)
  blocks:insert(pandoc.RawBlock("typst", "]"))
  return blocks
end

local function take_check(div)
  local label = (box or "Task"):gsub(" · %d+ min$", "")
  if label:match("^Lab task") then lab = true end
  if section and not label:match("^Activity") then label = section .. " · " .. label end
  table.insert(results, { label = label, blocks = div.content })
  return {}
end

local function callout_title(el)
  if el.title then return str(el.title) end
  if el.attributes and el.attributes.title then return el.attributes.title end
  return nil
end

local collect = {
  traverse = "topdown",
  Header = function(h)
    if h.level == 2 then
      section = str(h.content):match("^(%d+%.%d+)")
      box = nil
    end
  end,
  Callout = function(c)
    box = callout_title(c)
  end,
  Div = function(div)
    if not is_typst() then return nil end
    for _, c in ipairs(div.classes) do
      if c:match("^callout%-") then box = callout_title(div) end
    end
    if div.classes:includes("check") then
      return take_check(div), false
    end
    if div.classes:includes("answers") then
      return wrap("#block(width: 100%)[#set text(size: 9pt)\n", div.content)
    end
    if div.classes:includes("lead") then
      return wrap("#block(width: 100%, below: 1.1em)[#set text(size: 11.5pt, fill: luma(40))\n", div.content)
    end
    if div.classes:includes("prompt") then
      return wrap('#block(width: 100%, breakable: false, fill: white, radius: 6pt, inset: (x: 9pt, y: 7pt), '
        .. 'stroke: (paint: rgb("#b197fc"), thickness: 0.8pt, dash: "dashed"))[#text(size: 8.5pt, weight: "bold", '
        .. 'fill: rgb("#5f3dc4"))[Starter prompt] \\\n#set text(size: 9.5pt)\n', div.content)
    end
    return nil
  end,
}

local append = {
  Pandoc = function(doc)
    if not is_typst() or #results == 0 then return nil end
    local m = doc.meta
    local seminar = m.seminar or m.practice
    doc.blocks:insert(pandoc.Header(2, seminar and "Results of the activities"
      or (lab and "Results of the Lab tasks" or "Results of the Do it tasks")))
    doc.blocks:insert(pandoc.Para({ pandoc.Emph({ pandoc.Str(seminar
      and "Do each activity first. Then compare your result with the one here."
      or "Do each task first. Then compare your result with the one here.") }) }))
    local body = pandoc.Blocks({})
    for _, r in ipairs(results) do
      body:insert(pandoc.Para({ pandoc.Strong({ pandoc.Str(r.label) }) }))
      body:extend(r.blocks)
    end
    doc.blocks:extend(wrap("#block(width: 100%)[#set text(size: 9.5pt)\n", body))
    return doc
  end,
}

return { collect, append }
