-- Interactive checks: the page checks every task at once (AUTHORING.md,
-- "The page teaches, the notes test"). They take the place of a closed
-- "Check your result" on the interactive page: the student taps, puts cards
-- in order, sorts cards or types a number, and sees at once if it is right,
-- with the reason. A wrong answer says why it is wrong; after two wrong tries
-- the right answer is shown with its reason, so no student is left stuck.
-- They are for the page only: the notes, the worksheets and the slides leave
-- them out (the notes keep their {.check} results at the end).
--
--   ::: {.choice}                 One question, 2–4 options, one right ([x]).
--   Where does u + v end?         Each option has its reason: why it is right,
--                                 or why it is wrong. The page mixes the
--   - [x] at (4, 3)               options (.fixed keeps the written order,
--                                 for A, B, C or a scale).
--     Why: 3 + 1 = 4, 1 + 2 = 3.
--
--   - [ ] at (3, 4)
--
--     Why: x comes first: 3 + 1 = 4.
--   :::
--
--   ::: {.order}                  Put the cards in order: the list is the
--   Put the steps in order.       right order, the page mixes it. The student
--                                 swaps two cards with two taps (or moves one
--   1. Fetch                      with ▲ ▼), then taps "Check the order".
--   2. Decode                     The reason is shown when the order is right.
--   3. Execute
--
--   Why: The CPU fetches, decodes, then executes.
--   :::
--
--   ::: {.sort}                   Sort the cards into groups: each term is a
--   Story or gameplay?            group, each of its definitions one card
--                                 (with its own "Why:"). The student taps a
--   Story                         group for the card in colour.
--   :   She saved the fisherman.
--
--       Why: The next scene changes.
--
--   Gameplay
--   :   She picked a blue boat.
--
--       Why: Only the look changes.
--   :::
--
--   ::: {.fill answer="10" unit="cm" hint="Square each part first."}
--   How long is the vector (6, 8)?     Type a number or a short answer.
--                                      answer: the right answers, split by
--   Why: √(36 + 64) = √100 = 10.       "|"; tol: how far a number may be off
--   :::                                (default 0.001); unit: shown after the
--                                      field and allowed in the answer; hint:
--                                      shown after the first wrong try.
--
-- Behaviour and look: lesson-script.html and lesson.css (".ic"). Every check
-- sends "ic:done" when it is solved (the progress of the page listens).
-- check_size.py checks the parts (one right option, a reason for every
-- option, 3–6 cards in order, 2–3 groups).

local str = pandoc.utils.stringify

local KINDS = { "choice", "order", "sort", "fill" }

local function kind_of(div)
  for _, k in ipairs(KINDS) do
    if div.classes:includes(k) then return k end
  end
  return nil
end

local function esc(s)
  return (s:gsub("&", "&amp;"):gsub('"', "&quot;"):gsub("<", "&lt;"):gsub(">", "&gt;"))
end

local function html_inlines(inlines)
  local out = pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), "html")
  return (out:gsub("%s+$", ""))
end

local function html_blocks(blocks)
  local out = pandoc.write(pandoc.Pandoc(blocks), "html")
  return (out:gsub("%s+$", ""))
end

-- A "Why: …" paragraph: its inlines without "Why:" (or nil).
local function why_of(block)
  if not block or (block.t ~= "Para" and block.t ~= "Plain") then return nil end
  local first = block.content[1]
  if not (first and first.t == "Str" and first.text:match("^Why:")) then return nil end
  local out = pandoc.Inlines({})
  out:extend(block.content)
  local rest = out[1].text:gsub("^Why:", "")
  if rest == "" then
    out:remove(1)
    if out[1] and (out[1].t == "Space" or out[1].t == "SoftBreak") then out:remove(1) end
  else
    out[1] = pandoc.Str(rest)
  end
  return out
end

-- The first block of a list item, as inlines.
local function item_inlines(item)
  local first = item[1]
  if first and (first.t == "Plain" or first.t == "Para") then return pandoc.Inlines(first.content) end
  return pandoc.Inlines({ pandoc.Str(str(first or "")) })
end

-- The reason of a list item or a definition: its "Why:" paragraph.
local function item_why(blocks)
  for i = 2, #blocks do
    local w = why_of(blocks[i])
    if w then return w end
  end
  return nil
end

local function reason_html(w)
  return w and html_inlines(w) or ""
end

-- Split the content of a check into (intro blocks, the list, blocks after it).
local function split(div, list_types)
  local intro, list, after = pandoc.Blocks({}), nil, pandoc.Blocks({})
  for _, b in ipairs(div.content) do
    if not list and list_types[b.t] then
      list = b
    elseif list then
      after:insert(b)
    else
      intro:insert(b)
    end
  end
  return intro, list, after
end

-- The reason after the list ("Why: …"), and any other blocks after it.
local function trailing_why(after)
  local why, rest = nil, pandoc.Blocks({})
  for _, b in ipairs(after) do
    local w = why_of(b)
    if w and not why then why = w else rest:insert(b) end
  end
  return why, rest
end

local function open_tag(kind, div, extra)
  local cls = "ic ic-" .. kind
  if div.classes:includes("fixed") then cls = cls .. " ic-fixed" end
  return pandoc.RawBlock("html", string.format('<div class="%s"%s>', cls, extra or "")
    .. '<div class="ic-q">')
end

local function fail(kind, msg)
  error("A ::: {." .. kind .. "} check " .. msg .. " (see the top of _extensions/lesson/interact.lua).")
end

-- One question, several options (a task list), one of them right.
local function choice(div)
  local intro, list, after = split(div, { BulletList = true, OrderedList = true })
  if not list then fail("choice", "needs a list of options (- [x] right, - [ ] wrong)") end
  local rows, right = {}, 0
  for _, item in ipairs(list.content) do
    local inl = item_inlines(item)
    local mark = inl[1] and inl[1].t == "Str" and inl[1].text or ""
    local ok = mark == "☒"
    if mark == "☒" or mark == "☐" then
      inl:remove(1)
      if inl[1] and inl[1].t == "Space" then inl:remove(1) end
    elseif mark:match("^%[x%]$") then
      ok = true
    end
    if ok then right = right + 1 end
    table.insert(rows, string.format(
      '<div class="ic-opt-row"><button type="button" class="ic-opt" data-right="%s">'
        .. '<span class="ic-mark" aria-hidden="true"></span><span class="ic-opt-text">%s</span></button>'
        .. '<div class="ic-reason" hidden>%s</div></div>',
      ok and "1" or "0", html_inlines(inl), reason_html(item_why(item))))
  end
  if right ~= 1 then fail("choice", "needs exactly one right option (- [x])") end
  local blocks = pandoc.Blocks({ open_tag("choice", div) })
  blocks:extend(intro)
  blocks:insert(pandoc.RawBlock("html", '</div><div class="ic-opts" role="group" aria-label="Answers">'
    .. table.concat(rows, "") .. '</div><p class="ic-help">Tap the right answer.</p>'
    .. '<p class="ic-feedback" aria-live="polite"></p></div>'))
  blocks:extend(after)
  return blocks
end

-- Cards to put in order: the list is the right order.
local function order(div)
  local intro, list, after = split(div, { OrderedList = true, BulletList = true })
  if not list then fail("order", "needs a list in the right order (1. first, 2. second …)") end
  local cards = {}
  for i, item in ipairs(list.content) do
    table.insert(cards, string.format(
      '<li class="ic-card" data-pos="%d"><span class="ic-num" aria-hidden="true"></span>'
        .. '<span class="ic-card-text">%s</span><span class="ic-move">'
        .. '<button type="button" class="ic-up" aria-label="Move up">▲</button>'
        .. '<button type="button" class="ic-down" aria-label="Move down">▼</button></span></li>',
      i, html_inlines(item_inlines(item))))
  end
  local why, rest = trailing_why(after)
  local blocks = pandoc.Blocks({ open_tag("order", div) })
  blocks:extend(intro)
  blocks:insert(pandoc.RawBlock("html", '</div><ol class="ic-cards">' .. table.concat(cards, "") .. "</ol>"
    .. '<p class="ic-help">Tap two cards to swap them, or move a card with ▲ ▼. Then check.</p>'
    .. '<div class="ic-actions"><button type="button" class="ic-check">Check the order</button></div>'
    .. '<p class="ic-feedback" aria-live="polite"></p>'
    .. '<div class="ic-why" hidden>' .. reason_html(why) .. "</div></div>"))
  blocks:extend(rest)
  return blocks
end

-- Cards to sort into groups: each term of the definition list is a group.
local function sort(div)
  local intro, list, after = split(div, { DefinitionList = true })
  if not list then fail("sort", "needs a definition list (a group, then ':   a card' for each card)") end
  local bins, cards = {}, {}
  for g, item in ipairs(list.content) do
    table.insert(bins, string.format(
      '<button type="button" class="ic-bin" data-g="%d"><span class="ic-bin-name">%s</span>'
        .. '<span class="ic-bin-count"></span></button>', g, html_inlines(item[1])))
    for _, def in ipairs(item[2]) do
      table.insert(cards, string.format(
        '<li class="ic-sort-card" data-g="%d" tabindex="0"><span class="ic-sort-text">%s</span>'
          .. '<span class="ic-sort-group" hidden></span><span class="ic-reason" hidden>%s</span></li>',
        g, html_inlines(item_inlines(def)), reason_html(item_why(def))))
    end
  end
  local blocks = pandoc.Blocks({ open_tag("sort", div) })
  blocks:extend(intro)
  blocks:insert(pandoc.RawBlock("html", '</div><ol class="ic-sort-cards">' .. table.concat(cards, "") .. "</ol>"
    .. '<p class="ic-help">Tap the right group for the card in colour.</p>'
    .. '<div class="ic-bins" role="group" aria-label="Groups">' .. table.concat(bins, "") .. "</div>"
    .. '<p class="ic-feedback" aria-live="polite"></p></div>'))
  blocks:extend(after)
  return blocks
end

-- A number or a short answer, typed and checked at once.
local function fill(div)
  local answer = div.attributes.answer
  if not answer or answer == "" then fail("fill", 'needs answer="…" (the right answers, split by "|")') end
  local intro, why, rest = pandoc.Blocks({}), nil, pandoc.Blocks({})
  for _, b in ipairs(div.content) do
    local w = why_of(b)
    if w and not why then why = w
    elseif why then rest:insert(b)
    else intro:insert(b) end
  end
  local numeric = true
  for part in answer:gmatch("[^|]+") do
    if not part:gsub(",", "."):match("^%s*[%-−]?%d+%.?%d*%s*$") then numeric = false end
  end
  local unit = div.attributes.unit or ""
  local attrs = string.format(' data-answer="%s" data-tol="%s" data-unit="%s" data-hint="%s"',
    esc(answer), esc(div.attributes.tol or ""), esc(unit), esc(div.attributes.hint or ""))
  local blocks = pandoc.Blocks({ open_tag("fill", div, attrs) })
  blocks:extend(intro)
  blocks:insert(pandoc.RawBlock("html", string.format(
    '</div><div class="ic-fill-row"><input class="ic-input" type="text" inputmode="%s" autocomplete="off" '
      .. 'autocapitalize="off" spellcheck="false" aria-label="Your answer">%s'
      .. '<button type="button" class="ic-check">Check</button></div>'
      .. '<p class="ic-feedback" aria-live="polite"></p><div class="ic-why" hidden>%s</div></div>',
    numeric and "decimal" or "text", unit ~= "" and ('<span class="ic-unit">' .. esc(unit) .. "</span>") or "",
    reason_html(why))))
  blocks:extend(rest)
  return blocks
end

local BUILD = { choice = choice, order = order, sort = sort, fill = fill }

return {
  {
    Div = function(div)
      local kind = kind_of(div)
      if not kind then return nil end
      if not quarto.doc.is_format("html") then
        return {}       -- the notes, worksheets and slides leave the page checks out
      end
      return BUILD[kind](div)
    end,
  },
}
