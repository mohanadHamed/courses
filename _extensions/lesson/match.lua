-- "Try it" matching questions (lesson-html and lesson-typst).
--
--   ::: {.callout-tip title="Try it 1"}
--   Position or vector?
--
--   ::: {.match extra="angle|logic"}
--   The coin is at (7, 4).
--   :   position
--
--   The car goes 3 steps right.
--   :   vector
--   :::
--   :::
--
-- Each term is a question; its definition is the right answer. `extra` adds
-- wrong answers, split by "|" (needed when there are only 1–2 questions).
-- A second paragraph of the definition that starts with "Why:" is the reason:
--
--   The magnitude of (3, −4).
--   :   5
--
--       Why: √(3² + 4²) = √25 = 5.
--
-- HTML: every answer is shown once as a button. The student taps the answer
-- for the coloured question and sees at once if it is right, with the reason
-- (lesson-script.html). After two wrong tries the right answer and its reason
-- are shown, so no student is left stuck.
-- PDF:  the questions with a blank line, the answers to choose from, and
--       the answers upside down at the bottom of the box. The reason is not
--       printed: the notes are a self-test.
--
-- Also, for the interactive page (HTML) only:
--   ::: {.check}    "Check your result" of a Do it task or a seminar activity:
--   …               a closed <details> box. In the notes (PDF) book.lua moves
--   :::             it to "Results of the Do it tasks" at the end.
--   ::: {.prompt}   The prompt of a "Task with AI" box, with a "Copy
--   …               prompt" button (lesson-script.html).
--   :::
--   ::: {.check label="What you should see"}
--                   The same closed box with another label.
--   ::: {.try-change}
--   **Try a change:** … What do you notice?
--   ::: {.check}    A change to try in a "Task with AI" box, then its
--   …               closed answer ("What you notice"); book.lua prints the
--   :::             answers at the end of the notes.
--   :::

local str = pandoc.utils.stringify

local function letter(i)
  return string.char(string.byte("a") + i - 1)
end

local function html_inlines(inlines)
  local out = pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), "html")
  return (out:gsub("%s+$", ""))
end

local function answer_inlines(defs)
  local first = defs[1] and defs[1][1]
  if first and (first.t == "Plain" or first.t == "Para") then
    return first.content
  end
  return pandoc.Inlines({ pandoc.Str(str(defs[1] or "")) })
end

-- The reason ("Why: …" paragraph after the answer), without "Why:"; or nil.
local function why_inlines(defs)
  for _, b in ipairs(defs[1] or {}) do
    if (b.t == "Para" or b.t == "Plain") and b.content[1] and b.content[1].t == "Str"
        and b.content[1].text:match("^Why:") then
      local out = pandoc.Inlines({})
      out:extend(b.content)
      local rest = out[1].text:gsub("^Why:", "")
      if rest == "" then
        out:remove(1)
        if out[1] and out[1].t == "Space" then out:remove(1) end
      else
        out[1] = pandoc.Str(rest)
      end
      return out
    end
  end
  return nil
end

-- Read a .match div: questions, answers and the list of options.
local function read_match(div)
  local intro, items = {}, nil
  for _, b in ipairs(div.content) do
    if b.t == "DefinitionList" and not items then
      items = b.content
    else
      table.insert(intro, b)
    end
  end
  if not items then
    error("A ::: {.match} block needs a definition list (question, then ':   answer').")
  end
  local qs, opts, index = {}, {}, {}
  local function add_option(inlines)
    local key = str(inlines)
    if not index[key] then
      table.insert(opts, inlines)
      index[key] = #opts
    end
    return index[key]
  end
  local reuse = false
  local seen = {}
  for _, item in ipairs(items) do
    local ans = answer_inlines(item[2])
    local key = str(ans)
    if seen[key] then reuse = true end
    seen[key] = true
    table.insert(qs, { q = item[1], a = ans, o = add_option(ans), why = why_inlines(item[2]) })
  end
  local extra = div.attributes["extra"]
  if extra then
    for part in extra:gmatch("[^|]+") do
      add_option(pandoc.Inlines({ pandoc.Str((part:gsub("^%s+", ""):gsub("%s+$", ""))) }))
    end
  end
  return intro, qs, opts, reuse
end

local function html_widget(qs, opts, reuse)
  local li, buttons = {}, {}
  for i, q in ipairs(qs) do
    table.insert(li, string.format(
      '<li class="match-q" data-a="%d" tabindex="0"><span class="match-label">%s)</span>'
        .. '<span class="match-text">%s</span><span class="match-slot">?</span>%s</li>',
      q.o, letter(i), html_inlines(q.q),
      q.why and ('<span class="match-why" hidden>' .. html_inlines(q.why) .. "</span>") or ""))
  end
  for i, o in ipairs(opts) do
    table.insert(buttons, string.format('<button type="button" class="match-opt" data-o="%d">%s</button>',
      i, html_inlines(o)))
  end
  return pandoc.RawBlock("html", string.format([[
<div class="match" data-reuse="%s">
  <ol class="match-list">%s</ol>
  <p class="match-help">Tap the right answer for the question in colour. After two wrong tries, the answer is shown.</p>
  <div class="match-opts" role="group" aria-label="Answers">%s</div>
  <p class="match-feedback" aria-live="polite"></p>
  <div class="match-foot"><span class="match-score"></span><button type="button" class="match-reset" hidden>Start again</button></div>
</div>]], reuse and "1" or "0", table.concat(li, ""), table.concat(buttons, "")))
end

local function typst_widget(qs, opts)
  local items = {}
  for _, q in ipairs(qs) do
    local line = pandoc.Inlines({})
    line:extend(q.q)
    line:extend({ pandoc.Space(), pandoc.Str("→"), pandoc.Space(), pandoc.Str("__________") })
    table.insert(items, { pandoc.Plain(line) })
  end
  local choose = pandoc.Inlines({ pandoc.Emph({ pandoc.Str("Choose from:") }), pandoc.Space() })
  -- A to Z, so the order of the options does not give away the answers.
  local sorted = {}
  for _, o in ipairs(opts) do table.insert(sorted, o) end
  table.sort(sorted, function(x, y) return str(x):lower() < str(y):lower() end)
  for i, o in ipairs(sorted) do
    if i > 1 then choose:extend({ pandoc.Space(), pandoc.Str("·"), pandoc.Space() }) end
    choose:insert(pandoc.Strong(o))
  end
  return {
    pandoc.OrderedList(items, pandoc.ListAttributes(1, "LowerAlpha", "OneParen")),
    pandoc.Para(choose),
  }
end

-- Answers printed upside down at the bottom of the box, like in a workbook:
-- close to the questions, but not read by accident.
local function typst_key(qs)
  local parts = {}
  for i, q in ipairs(qs) do
    local a = pandoc.write(pandoc.Pandoc({ pandoc.Plain(q.a) }), "typst"):gsub("%s+$", "")
    table.insert(parts, letter(i) .. ") " .. a)
  end
  return pandoc.RawBlock("typst", string.format(
    "#align(right)[#rotate(180deg, reflow: true)[#text(size: 8pt, fill: luma(115))[*Answers:* %s]]]",
    table.concat(parts, " · ")))
end

-- Returns the blocks that replace the .match div, and the answer key (PDF).
local function build(div)
  local intro, qs, opts, reuse = read_match(div)
  local blocks = {}
  for _, b in ipairs(intro) do table.insert(blocks, b) end
  if quarto.doc.is_format("html") then
    table.insert(blocks, html_widget(qs, opts, reuse))
    return blocks, nil
  end
  for _, b in ipairs(typst_widget(qs, opts)) do table.insert(blocks, b) end
  table.insert(blocks, typst_key(qs))
  return blocks, nil
end

local function active()
  return quarto.doc.is_format("html") or quarto.doc.is_format("typst")
end

-- HTML: "Check your result" (closed until the student opens it), or the
-- label of the box (label="…").
local function check_box(div, label)
  label = div.attributes.label or label or "Check your result"
  local blocks = pandoc.Blocks({ pandoc.RawBlock("html",
    '<details class="check"><summary>' .. label:gsub("&", "&amp;"):gsub("<", "&lt;") .. '</summary><div class="check-body">') })
  blocks:extend(div.content)
  blocks:insert(pandoc.RawBlock("html", "</div></details>"))
  return blocks
end

-- HTML: a change to try in a "Task with AI" box, with its closed answer.
local function try_change(div)
  local blocks = pandoc.Blocks({ pandoc.RawBlock("html", '<div class="try-change">') })
  for _, b in ipairs(div.content) do
    if b.t == "Div" and b.classes:includes("check") then
      blocks:extend(check_box(b, "What you notice"))
    else
      blocks:insert(b)
    end
  end
  blocks:insert(pandoc.RawBlock("html", "</div>"))
  return blocks
end

return {
  {
    traverse = "topdown",
    Div = function(div)
      if div.classes:includes("try-change") and quarto.doc.is_format("html") then
        return try_change(div), false
      end
      if div.classes:includes("check") and quarto.doc.is_format("html") then
        return check_box(div)
      end
      if not active() then return nil end
      if div.classes:includes("match") then
        local blocks, key = build(div)
        if key then table.insert(blocks, key) end
        return blocks, false
      end
      local pos
      for i, b in ipairs(div.content) do
        if b.t == "Div" and b.classes:includes("match") then pos = i break end
      end
      if not pos then return nil end
      local blocks, key = build(div.content[pos])
      local content = {}
      for i, b in ipairs(div.content) do
        if i == pos then
          for _, nb in ipairs(blocks) do table.insert(content, nb) end
        else
          table.insert(content, b)
        end
      end
      div.content = content
      if key then return { div, key }, false end
      return div, false
    end,
  },
}
