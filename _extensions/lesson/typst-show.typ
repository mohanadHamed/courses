// Course colours and title-band values come from banner.lua (meta.lessontheme).
#let accent = $if(lessontheme.accent)$$lessontheme.accent$$else$rgb("#2F9E44")$endif$
#let accent2 = $if(lessontheme.accent2)$$lessontheme.accent2$$else$rgb("#A9E34B")$endif$

#show: doc => article(
$if(title)$
  title: [$title$],
$endif$
$if(description)$
  subtitle: [$description$],
$endif$
$if(lang)$
  lang: "$lang$",
$endif$
$if(region)$
  region: "$region$",
$endif$
$if(mainfont)$
  font: ("$mainfont$", "Noto Naskh Arabic"),
$endif$
$if(fontsize)$
  fontsize: $fontsize$,
$endif$
$if(codefont)$
  codefont: ($for(codefont)$"$codefont$",$endfor$),
$endif$
$if(linestretch)$
  linestretch: $linestretch$,
$endif$
  accent: accent,
  accent2: accent2,
$if(lessontheme.course)$
  course: $lessontheme.course$,
$endif$
$if(lessontheme.chips)$
  chips: $lessontheme.chips$,
$endif$
$if(lessontheme.program)$
  program: $lessontheme.program$,
$endif$
$if(lessontheme.compact)$
  compact: $lessontheme.compact$,
$endif$
  doc,
)
