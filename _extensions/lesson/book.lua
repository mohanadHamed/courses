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
--   ::: {.prompt}        The prompt of a "Task with AI" box: a dashed box.
--   …
--   :::
--
--   ::: {.try-change}    A change to try in a "Task with AI" box: its text
--   … ::: {.check} …     stays, and its answer goes to the results at the
--   :::                  end ("… · Change 1").
--
-- A lecture worksheet (lesson-NN-sheet.qmd; AUTHORING.md, "Lecture
-- worksheets"): under "## Experiment N · …" the steps are a numbered list,
-- each step with a {{< record >}} field and a {.check}. The results go to
-- "Results of the experiments", labelled "Experiment N · Step M".
--
--   ::: {.record-table}  A table with empty cells to fill in (the "Table of
--   | … |   |          results"): taller rows, room to write.
--   :::

local str = pandoc.utils.stringify

local results = {}      -- { label = "1.2 · Do it · Add two arrows", blocks = {...} }
local section = nil     -- "1.2" of the current ## heading
local experiment = nil  -- "Experiment 2" of the current ## heading (worksheet)
local steps = false     -- a result of a step of an experiment
local box = nil         -- title of the current callout
local changes = 0       -- the changes to try in the current callout
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

local function take_check(div, step_label)
  if step_label then
    steps = true
    table.insert(results, { label = step_label, blocks = div.content })
    return {}
  end
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
      experiment = str(h.content):match("^(Experiment %d+)")
      box = nil
    end
  end,
  -- The steps of an experiment: each result is labelled with its step.
  OrderedList = function(list)
    if not is_typst() or not experiment then return nil end
    local start = list.listAttributes and list.listAttributes.start or list.start or 1
    for i, item in ipairs(list.content) do
      local kept = pandoc.Blocks({})
      for _, b in ipairs(item) do
        if b.t == "Div" and b.classes:includes("check") then
          take_check(b, string.format("%s · Step %d", experiment, start + i - 1))
        else
          kept:insert(b)
        end
      end
      list.content[i] = kept
    end
    return list, false
  end,
  Callout = function(c)
    box = callout_title(c)
    changes = 0
  end,
  Div = function(div)
    if not is_typst() then return nil end
    for _, c in ipairs(div.classes) do
      if c:match("^callout%-") then box = callout_title(div); changes = 0 end
    end
    if div.classes:includes("try-change") then
      changes = changes + 1
      local kept = pandoc.Blocks({})
      for _, b in ipairs(div.content) do
        if b.t == "Div" and b.classes:includes("check") then
          local label = (box or "Task") .. " · Change " .. changes
          if section then label = section .. " · " .. label end
          table.insert(results, { label = label, blocks = b.content })
        else
          kept:insert(b)
        end
      end
      return wrap("#block(width: 100%, inset: (left: 8pt, y: 3pt), stroke: (left: 2pt + rgb(\"#b197fc\")))[\n", kept), false
    end
    if div.classes:includes("check") then
      return take_check(div, experiment), false
    end
    if div.classes:includes("record-table") then
      return wrap("#block(width: 100%)[#set table(inset: (x: 6pt, y: 11pt))\n", div.content)
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
        .. 'fill: rgb("#5f3dc4"))[Prompt to copy] \\\n#set text(size: 9.5pt)\n', div.content)
    end
    return nil
  end,
}

-- A worksheet: the "Table of results" (its title, its line and the table)
-- stays on one page, so the teacher checks it on one sheet.
local keep = {
  Pandoc = function(doc)
    if not is_typst() then return nil end
    local out, i, n, changed = pandoc.Blocks({}), 1, #doc.blocks, false
    while i <= n do
      local b = doc.blocks[i]
      if b.t == "Header" and b.level == 2 and str(b.content):match("^Table of results") then
        local j = i + 1
        while j <= n and not (doc.blocks[j].t == "Header" and doc.blocks[j].level <= 2) do j = j + 1 end
        out:insert(pandoc.RawBlock("typst", "#block(width: 100%, breakable: false)["))
        for k = i, j - 1 do out:insert(doc.blocks[k]) end
        out:insert(pandoc.RawBlock("typst", "]"))
        i, changed = j, true
      else
        out:insert(b)
        i = i + 1
      end
    end
    if changed then
      doc.blocks = out
      return doc
    end
  end,
}

local append = {
  Pandoc = function(doc)
    if not is_typst() or #results == 0 then return nil end
    local m = doc.meta
    local seminar = m.seminar or m.practice
    -- A worksheet is printed: its results start on a new page.
    if steps then doc.blocks:insert(pandoc.RawBlock("typst", "#pagebreak(weak: true)")) end
    doc.blocks:insert(pandoc.Header(2, steps and "Results of the experiments"
      or (seminar and "Results of the activities"
      or (lab and "Results of the Lab tasks" or "Results of the Do it tasks"))))
    doc.blocks:insert(pandoc.Para({ pandoc.Emph({ pandoc.Str(steps
      and "Do each step first and record your result. Then compare it with the one here."
      or (seminar and "Do each activity first. Then compare your result with the one here."
      or "Do each task first. Then compare your result with the one here.")) }) }))
    local body = pandoc.Blocks({})
    for _, r in ipairs(results) do
      body:insert(pandoc.Para({ pandoc.Strong({ pandoc.Str(r.label) }) }))
      body:extend(r.blocks)
    end
    doc.blocks:extend(wrap("#block(width: 100%)[#set text(size: 9.5pt)\n", body))
    return doc
  end,
}

return { collect, keep, append }
