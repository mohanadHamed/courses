-- Every table of a web page in its own box (div.table-scroll, lesson.css).
-- On a phone, a table wider than the screen scrolls sideways inside this box,
-- so the page itself never becomes wider than the screen. A table that fits
-- looks the same as before. Web pages only (lesson-html): the notes (PDF) and
-- the slides keep their tables as they are.

function Table(tbl)
  return pandoc.Div({ tbl }, pandoc.Attr("", { "table-scroll" }))
end
