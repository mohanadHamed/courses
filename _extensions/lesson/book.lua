-- Lesson notes (lesson-NN-book.qmd, lesson-typst): textbook parts.
--
--   ::: {.answers}       Short answers to the end-of-chapter exercises:
--   1. …                 small text at the end of the PDF.
--   :::
--
--   ::: {.lead}          The opening paragraph of the chapter, a little larger.
--   …
--   :::

function Div(div)
  if not quarto.doc.is_format("typst") then
    return nil
  end
  if div.classes:includes("answers") then
    local blocks = pandoc.Blocks({ pandoc.RawBlock("typst", "#block(width: 100%)[#set text(size: 9pt)\n") })
    blocks:extend(div.content)
    blocks:insert(pandoc.RawBlock("typst", "]"))
    return blocks
  end
  if div.classes:includes("lead") then
    local blocks = pandoc.Blocks({ pandoc.RawBlock("typst", "#block(width: 100%, below: 1.1em)[#set text(size: 11.5pt, fill: luma(40))\n") })
    blocks:extend(div.content)
    blocks:insert(pandoc.RawBlock("typst", "]"))
    return blocks
  end
  return nil
end
