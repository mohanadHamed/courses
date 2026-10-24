# Simulators

- `sim-base.css` — shared look. Every simulator links it with a relative path.
- `sim-base.js` — every simulator loads it, before its own script. It gives every
  animation frame `performance.now()` (one clock, also inside the lesson page),
  resizes the lesson iframe to fit, and keeps game keys and `focus()` from
  scrolling the lesson page.
- `viewer3d.js` — 3D helper for 3D simulators (uses `vendor/three.module.min.js`).
- `vendor/` — copied third-party libraries with their licenses. Never load from a CDN.
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

## Recordings for the slides

The slides show a short GIF of each simulator or mini-game being played, next
to its QR code (`sims/<name>.gif` next to `sims/<name>.html`).

1. Write `recordings/scenarios/<name>.js`: plain JavaScript that plays the
   game in the page (`wait(ms)`, `click(selector)`, `tap(element, x, y)`).
2. Add one line to `recordings/record-all.sh` (page, seconds, output GIF;
   `window` for 3D scenes).
3. Start a server for the repository: `python3 -m http.server 4323`.
4. Run `sh shared/sims/recordings/record-all.sh <name>`.

`record.ts` (Deno, comes with Quarto) drives Google Chrome and takes the
frames; `make-gif.swift` (macOS) joins them into a looping GIF.
