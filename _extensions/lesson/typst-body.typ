// Restyle Quarto callouts for lessons (same structure as Quarto's version).
// Green "tip" callouts are "Try it" boxes; the others are answer boxes.
#let callout(body: [], title: "Callout", background_color: rgb("#dddddd"), icon: none, icon_color: black, body_background_color: white) = {
  let is-try = icon_color == rgb("#00A047")
  let head-fill = if is-try { gradient.linear(accent.lighten(93%), accent2.lighten(85%)) } else { luma(242) }
  let body-fill = if is-try { white } else { luma(251) }
  let line-paint = if is-try { accent.lighten(70%) } else { luma(215) }
  block(
    breakable: false,
    fill: body-fill,
    stroke: (paint: line-paint, thickness: 0.6pt, dash: if is-try { "solid" } else { "dashed" }),
    width: 100%,
    radius: 8pt,
    clip: true,
    block(
      inset: 0pt,
      width: 100%,
      below: 0pt,
      block(fill: head-fill, width: 100%, inset: (x: 10pt, y: 6pt))[
        #set text(weight: "bold", fill: if is-try { accent.darken(45%) } else { luma(80) }, size: if is-try { 10.5pt } else { 9.5pt })
        #title
      ]) +
      if (body != []) {
        block(inset: 0pt, width: 100%,
          block(fill: body-fill, width: 100%, inset: (x: 10pt, y: 8pt), body))
      }
  )
}
