-- PDF (lesson-typst): keep each question on the same page as its answer space.
-- The answer-space shortcode (shortcodes.lua) writes a raw Typst block that
-- starts with "// answer-space". This filter puts the question just before it
-- and the answer space in one block that does not break across pages.

local function is_space(b)
  return b and b.t == "RawBlock" and b.format == "typst" and b.text:match("^// answer%-space")
end

function Blocks(blocks)
  if not quarto.doc.is_format("typst") then return nil end
  local out = pandoc.Blocks({})
  local i = 1
  while i <= #blocks do
    local b = blocks[i]
    -- "a) question" is read as a one-item list, so lists count as questions too.
    local question = b.t == "Para" or b.t == "Plain" or b.t == "OrderedList" or b.t == "BulletList"
    if question and is_space(blocks[i + 1]) then
      out:insert(pandoc.RawBlock("typst", "#block(breakable: false, width: 100%)["))
      out:insert(b)
      out:insert(blocks[i + 1])
      out:insert(pandoc.RawBlock("typst", "]"))
      i = i + 2
    else
      out:insert(b)
      i = i + 1
    end
  end
  return out
end
