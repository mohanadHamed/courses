// Lesson PDF layout: colour title band, running header and footer,
// accent headings and tables. Colours are per course (typst-show.typ).

#let article(
  title: none,
  subtitle: none,
  lang: "en",
  region: "US",
  font: none,
  fontsize: 11pt,
  codefont: none,
  linestretch: 1,
  accent: rgb("#2F9E44"),
  accent2: rgb("#A9E34B"),
  course: none,
  chips: (),
  program: none,
  compact: false,   // homework: tighter, so it fits on one A4 page
  doc,
) = {
  let gap = if compact { 0.9em } else { 1.6em }
  let title-text = if title != none { title } else { [] }
  set document(title: title)
  set text(lang: lang, region: region, size: fontsize)
  set text(font: font) if font != none
  set par(justify: false, leading: linestretch * 0.7em)
  show raw: set text(font: codefont) if codefont != none

  set page(
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: 8pt, fill: luma(110))
        grid(columns: (1fr, auto),
          if course != none { course } else { [] },
          text(fill: accent, weight: "bold", title-text))
        v(-4pt)
        line(length: 100%, stroke: 0.6pt + accent.lighten(60%))
      }
    },
    footer: context {
      set text(size: 8pt, fill: luma(120))
      line(length: 100%, stroke: 0.6pt + luma(220))
      v(-4pt)
      grid(columns: (1fr, auto),
        if program != none { program } else { [] },
        text(weight: "bold", fill: accent)[#counter(page).display("1 / 1", both: true)])
    },
  )

  // Headings: accent bar + accent colour.
  show heading: set text(fill: accent.darken(25%), weight: "bold")
  show heading.where(level: 1): it => block(above: gap, below: 0.6em)[
    #box(fill: gradient.linear(accent, accent2), width: 5pt, height: 0.95em, radius: 2pt, baseline: 0.1em)
    #h(6pt)#text(size: 1.35em, it.body)
  ]
  show heading.where(level: 2): it => block(above: gap, below: if compact { 0.5em } else { 0.8em })[
    #box(fill: gradient.linear(accent, accent2), width: 5pt, height: 0.95em, radius: 2pt, baseline: 0.1em)
    #h(6pt)#text(size: if compact { 1.15em } else { 1.3em }, it.body)
  ]
  show heading.where(level: 3): it => block(above: 1.2em, below: 0.6em, text(size: 1.1em, it.body))

  // Tables: soft accent header row.
  set table(
    inset: 6pt,
    stroke: (x, y) => if y == 0 { (bottom: 1pt + accent) } else { (bottom: 0.4pt + luma(225)) },
    fill: (x, y) => if y == 0 { accent.lighten(94%) },
  )
  show table.cell.where(y: 0): set text(weight: "bold", fill: accent.darken(30%))

  // Code and figures.
  show raw.where(block: true): it => block(width: 100%, fill: luma(246), radius: 6pt, inset: 10pt, it)
  show figure.caption: set text(size: 9pt, fill: luma(90))

  // Title band.
  block(
    width: 100%,
    radius: 12pt,
    clip: true,
    fill: gradient.linear(white, accent.lighten(95%), accent2.lighten(85%), angle: 20deg),
    stroke: 0.6pt + accent.lighten(75%),
    inset: if compact { (x: 14pt, y: 9pt) } else { (x: 18pt, y: 16pt) },
  )[
    #place(right + top, dx: 40pt, dy: -50pt, circle(radius: 55pt, fill: accent2.transparentize(85%)))
    #place(right + bottom, dx: -60pt, dy: 30pt, circle(radius: 22pt, fill: accent.transparentize(92%)))
    #set text(fill: accent.darken(50%))
    #if course != none { text(size: 9pt, weight: "bold", fill: accent.darken(10%), course) }
    #v(2pt)
    #text(size: if compact { 17pt } else { 22pt }, weight: "bold", title-text)
    #if subtitle != none and not compact { v(-4pt); text(size: 11pt, subtitle) }
    #v(4pt)
    #for c in chips {
      box(fill: white, stroke: 0.6pt + accent.lighten(40%),
        radius: 8pt, inset: (x: 7pt, y: 3pt), text(size: 9pt, weight: "bold", c))
      h(5pt)
    }
  ]
  v(6pt)

  doc
}
