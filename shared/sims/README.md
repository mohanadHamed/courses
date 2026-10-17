# Simulators

- `sim-base.css` — shared look. Every simulator links it with a relative path.
- `sim-base.js` — every simulator loads it. It resizes the lesson iframe to fit.
- Reusable simulators (used by more than one course) go in this folder.
  Lesson-specific ones go in `courses/<slug>/week-NN/sims/`.

## Rules

- One HTML file, plain JavaScript. No CDN libraries, no external APIs, no paid services.
- Works on a phone: touch input (`pointerdown`), fits a narrow screen.
- Has a poster: `<name>.svg` (source) and `<name>.png` (used in PDF and slides).
  The poster shows the simulator's start state.

## Export a poster

```bash
quarto typst compile --root . --input svg=/courses/game-math/week-01/sims/grid-position.svg shared/sims/export-poster.typ courses/game-math/week-01/sims/grid-position.png --ppi 200
```
