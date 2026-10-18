// Restyle Quarto callouts for lessons (same structure as Quarto's version).
// The callout type is read from Quarto's icon colour:
//   tip       (green)  "Try it" boxes (web lesson and homework)
//   important (red)    Definition / Key idea   — accent band, the core of a section
//   note      (blue)   Example                 — worked example with numbered steps
//   warning   (orange) Common mistake          — "Watch out" in the web lesson
//   caution            In game code            — a short C# reading example
#let callout(body: [], title: "Callout", background_color: rgb("#dddddd"), icon: none, icon_color: black, body_background_color: white) = {
  let kind = if icon_color == rgb("#00A047") { "try" }
    else if icon_color == rgb("#CC1914") { "key" }
    else if icon_color == rgb("#EB9113") { "warn" }
    else if icon_color == rgb("#FC5300") { "code" }
    else { "note" }
  let head-fill = if kind == "try" { gradient.linear(accent.lighten(93%), accent2.lighten(85%)) }
    else if kind == "key" { accent.lighten(88%) }
    else if kind == "warn" { rgb("#fff4e6") }
    else { luma(244) }
  let body-fill = if kind == "key" { accent.lighten(96%) } else if kind == "warn" { rgb("#fffaf3") } else { white }
  let line-paint = if kind == "try" { accent.lighten(70%) }
    else if kind == "key" { accent.lighten(45%) }
    else if kind == "warn" { rgb("#f0b37a") }
    else { luma(205) }
  let title-fill = if kind == "warn" { rgb("#a3500b") } else if kind == "note" or kind == "code" { luma(60) } else { accent.darken(40%) }
  block(
    breakable: false,
    fill: body-fill,
    stroke: if kind == "key" { (left: 3pt + accent, rest: 0.6pt + line-paint) } else { (paint: line-paint, thickness: 0.6pt, dash: if kind == "note" { "dashed" } else { "solid" }) },
    width: 100%,
    radius: 6pt,
    clip: true,
    block(
      inset: 0pt,
      width: 100%,
      below: 0pt,
      block(fill: head-fill, width: 100%, inset: (x: 10pt, y: 5pt))[
        #set text(weight: "bold", fill: title-fill, size: if kind == "try" { 10.5pt } else { 9.8pt })
        #title
      ]) +
      if (body != []) {
        block(inset: 0pt, width: 100%,
          block(fill: body-fill, width: 100%, inset: (x: 10pt, y: 7pt), body))
      }
  )
}
