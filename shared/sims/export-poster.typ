// Export a simulator poster SVG to PNG (for the PDF and the slides).
// Run from the project root:
//   quarto typst compile --root . --input svg=/courses/<slug>/week-NN/sims/<name>.svg \
//     shared/sims/export-poster.typ courses/<slug>/week-NN/sims/<name>.png --ppi 200
#set page(width: auto, height: auto, margin: 0pt)
#image(sys.inputs.at("svg"))
