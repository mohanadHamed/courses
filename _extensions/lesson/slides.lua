-- Slides (lesson-pptx): click-to-show parts.
--
--   ::: {.answer}          Answer cards. Each list item or paragraph becomes one
--   - a) position          card at the bottom of the slide. Each card pops in on
--   - b) vector            its own click (elastic zoom), so the teacher can ask
--   :::                    first and show the answer after the students reply.
--
--   ::: {.reveal}          Each list item or paragraph fades in from the left
--   - next idea            on its own click ("think first, then see").
--   :::
--
-- PowerPoint has no Markdown for animations, so this filter only leaves
-- invisible marker paragraphs around the content. pptx_finish.py (project
-- post-render) finds the markers, builds the cards and adds the animations.

local MARK = {
  answer = "\u{E000}",
  reveal = "\u{E001}",
  stop = "\u{E00F}",
}

local function marker(ch)
  return pandoc.Para({ pandoc.Str(ch) })
end

-- Results ({.check}) and AI prompts ({.prompt}) are for the page and the
-- notes; the slides show results with .answer and .reveal instead.

function Div(div)
  if not quarto.doc.is_format("pptx") then
    return nil
  end
  if div.classes:includes("check") or div.classes:includes("prompt") then
    return {}
  end
  for _, kind in ipairs({ "answer", "reveal" }) do
    if div.classes:includes(kind) then
      local blocks = { marker(MARK[kind]) }
      for _, b in ipairs(div.content) do
        table.insert(blocks, b)
      end
      table.insert(blocks, marker(MARK.stop))
      return blocks
    end
  end
  return nil
end
