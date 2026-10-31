// The pictures of a course video (AUTHORING.md, "Blended courses"), drawn
// like the simulators: generic windows, no logos, no screenshots.
//
// A video page (courses/<slug>/week-WW/videos/<name>.html) loads this kit and
// sets VIDEO = { label, title, scenes: [scene, …] }, one scene for each
// scene of the script (<name>-script.txt; scenes are split by a blank line).
// A scene is a function (g, k, p): it draws into the SVG group g; k is the
// line of the scene that the voice is reading (0, 1, 2 …) and p the seconds
// since that line started, so a picture can appear with its line:
//   if (k >= 2) folder(g, 300, 200, { o: show(k, 2, p) });
//
// window.drawAt(t) (record-video.ts) draws the picture at time t from
// window.TIMING (make-voice.swift): the scene whose first line has started,
// and the words of the line in the caption band, the same words as the voice.
// It returns a key that changes only when the picture changes.
(() => {
  const W = 1280, H = 720, NS = "http://www.w3.org/2000/svg";
  const C = {
    accent: "#D9480F", accent2: "#FFC078", soft: "#FFF4E6", paper: "#FFFFFF", page: "#FFF9F2",
    ink: "#3B2A1E", grey: "#7A6E66", line: "#E8D5C2", green: "#2B8A3E", red: "#C92A2A",
    blue: "#1C7ED6", purple: "#7048E8", yellow: "#FAB005", teal: "#0CA678",
  };
  const FONT = '"Nunito", "Helvetica Neue", Arial, sans-serif';
  const MONO = '"Menlo", "Consolas", monospace';

  const style = document.createElement("style");
  style.textContent = `
    @font-face { font-family: "Nunito"; font-weight: 400; src: url("../../../../shared/fonts/nunito-latin-400-normal.woff2") format("woff2"); }
    @font-face { font-family: "Nunito"; font-weight: 700; src: url("../../../../shared/fonts/nunito-latin-700-normal.woff2") format("woff2"); }
    @font-face { font-family: "Nunito"; font-weight: 800; src: url("../../../../shared/fonts/nunito-latin-800-normal.woff2") format("woff2"); }
    html, body { margin: 0; width: ${W}px; height: ${H}px; overflow: hidden; background: ${C.page}; font-family: ${FONT}; }
    #stage { position: absolute; left: 0; top: 0; }
    #caption { position: absolute; left: 60px; right: 60px; bottom: 26px; min-height: 0; text-align: center;
      font: 700 34px/1.25 ${FONT}; color: #fff; }
    #caption span { display: inline-block; background: rgba(32, 24, 18, 0.88); border-radius: 14px; padding: 10px 22px; }
    #caption:empty { display: none; }`;
  document.head.appendChild(style);

  // ---- drawing helpers (SVG) ----
  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs || {})) if (v !== undefined && v !== null) e.setAttribute(k, v);
    if (parent) parent.appendChild(e);
    return e;
  }
  function group(parent, o = {}) {
    return el("g", { opacity: o.o ?? 1, transform: o.dx || o.dy ? `translate(${o.dx || 0} ${o.dy || 0})` : null }, parent);
  }
  function text(parent, x, y, s, o = {}) {
    const t = el("text", {
      x, y, "font-size": o.size || 28, "font-weight": o.weight || 700, fill: o.fill || C.ink,
      "text-anchor": o.anchor || "start", "font-family": o.mono ? MONO : FONT, opacity: o.o ?? 1,
    }, parent);
    t.textContent = s;
    return t;
  }
  function rect(parent, x, y, w, h, o = {}) {
    return el("rect", { x, y, width: w, height: h, rx: o.r ?? 10, fill: o.fill || C.paper,
      stroke: o.stroke || "none", "stroke-width": o.sw || 2, opacity: o.o ?? 1 }, parent);
  }
  // A generic window: a title bar with the title and three dots; the content
  // area starts 44 px below the top.
  function win(parent, x, y, w, h, title, o = {}) {
    const g = group(parent, o);
    rect(g, x + 6, y + 8, w, h, { fill: "rgba(80,50,20,0.10)", r: 16 });
    rect(g, x, y, w, h, { fill: C.paper, stroke: C.line, r: 16 });
    el("path", { d: `M${x} ${y + 16}a16 16 0 0 1 16 -16h${w - 32}a16 16 0 0 1 16 16v28h${-w}z`, fill: o.bar || C.soft }, g);
    text(g, x + 20, y + 30, title, { size: 20, weight: 800, fill: C.ink });
    for (let i = 0; i < 3; i++) el("circle", { cx: x + w - 26 - i * 22, cy: y + 22, r: 6, fill: ["#E8B4A0", "#F2CF8B", "#B7D7A8"][i] }, g);
    return g;
  }
  function folder(parent, x, y, o = {}) {
    const s = o.s || 1, c = o.color || C.yellow;
    const g = group(parent, o);
    el("path", { d: `M${x} ${y + 8 * s}q0 -8 8 -8h${22 * s}l${8 * s} ${8 * s}h${30 * s}q8 0 8 8v${36 * s}q0 8 -8 8h${-62 * s}q-8 0 -8 -8z`, fill: c }, g);
    el("rect", { x, y: y + 16 * s, width: 76 * s, height: 36 * s, rx: 6, fill: o.front || "#FFD43B" }, g);
    if (o.label) text(g, x + 38 * s, y + 52 * s + 26, o.label, { size: o.size || 22, anchor: "middle", weight: 700 });
    return g;
  }
  function file(parent, x, y, o = {}) {
    const g = group(parent, o), c = o.color || C.blue, s = o.s || 1, w = 56 * s, h = 70 * s, f = 16 * s;
    el("path", { d: `M${x} ${y}h${w - f}l${f} ${f}v${h - f}h${-w}z`, fill: "#fff", stroke: c, "stroke-width": 3 }, g);
    el("path", { d: `M${x + w - f} ${y}v${f}h${f}`, fill: "none", stroke: c, "stroke-width": 3 }, g);
    rect(g, x + 6 * s, y + 36 * s, w - 12 * s, 20 * s, { fill: c, r: 4 });
    if (o.ext) text(g, x + w / 2, y + 51 * s, o.ext, { size: 13 * s, anchor: "middle", fill: "#fff", weight: 800 });
    if (o.label) text(g, x + w / 2, y + h + 26, o.label, { size: o.size || 20, anchor: "middle", mono: o.mono });
    return g;
  }
  // One line of text in parts of other colours: [[text, colour], …].
  function spans(parent, x, y, parts, o = {}) {
    const t = text(parent, x, y, "", o);
    for (const [s, c] of parts) {
      const sp = el("tspan", { fill: c || o.fill || C.ink }, t);
      sp.textContent = s;
    }
    return t;
  }
  function pill(parent, x, y, s, o = {}) {
    const g = group(parent, o), size = o.size || 24, w = o.w || s.length * size * 0.56 + 36;
    rect(g, x, y, w, size + 22, { fill: o.fill || C.soft, stroke: o.stroke || "none", r: (size + 22) / 2 });
    text(g, x + w / 2, y + size + 4, s, { size, anchor: "middle", fill: o.ink || C.ink, mono: o.mono, weight: o.weight || 800 });
    return g;
  }
  function arrow(parent, x1, y1, x2, y2, o = {}) {
    const g = group(parent, o), c = o.color || C.accent, a = Math.atan2(y2 - y1, x2 - x1), L = 18;
    el("line", { x1, y1, x2: x2 - Math.cos(a) * L * 0.8, y2: y2 - Math.sin(a) * L * 0.8, stroke: c, "stroke-width": o.sw || 5, "stroke-linecap": "round" }, g);
    el("path", { d: `M${x2} ${y2}L${x2 - L * Math.cos(a - 0.5)} ${y2 - L * Math.sin(a - 0.5)}L${x2 - L * Math.cos(a + 0.5)} ${y2 - L * Math.sin(a + 0.5)}z`, fill: c }, g);
    return g;
  }
  // A round mark: ok (a tick) or not ok (a short bar).
  function mark(parent, x, y, ok, o = {}) {
    const g = group(parent, o);
    el("circle", { cx: x, cy: y, r: o.r || 18, fill: ok ? C.green : C.red }, g);
    el("path", { d: ok ? `M${x - 8} ${y}l6 7l11 -13` : `M${x - 9} ${y}h18`, stroke: "#fff", "stroke-width": 4.5,
      fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, g);
    return g;
  }
  // A big title card (the first scene of a video).
  function titleCard(g, k, p, title, sub) {
    rect(g, 140, 150, 1000, 300, { fill: C.paper, stroke: C.line, r: 28, o: show(k, 0, p) });
    rect(g, 140, 150, 18, 300, { fill: C.accent, r: 9, o: show(k, 0, p) });
    text(g, 200, 260, title, { size: 52, weight: 800, fill: C.accent, o: show(k, 0, p) });
    if (sub) text(g, 200, 330, sub, { size: 30, weight: 700, fill: C.ink, o: show(k, 1, p) });
  }

  // Opacity of a part that appears with line n of the scene.
  function fade(p, d = 0.45) { return Math.max(0, Math.min(1, p / d)); }
  function show(k, n, p) { return k > n ? 1 : k === n ? fade(p) : 0; }

  window.VK = { W, H, C, el, group, text, spans, rect, win, folder, file, pill, arrow, mark, titleCard, fade, show };

  // ---- the stage and drawAt(t) ----
  let svg, cap, last = "";
  function setup() {
    svg = el("svg", { id: "stage", width: W, height: H, viewBox: `0 0 ${W} ${H}` });
    document.body.appendChild(svg);
    cap = document.createElement("div");
    cap.id = "caption";
    document.body.appendChild(cap);
  }
  // drawAt(t, true): the picture without the caption (the poster).
  window.drawAt = (t, poster) => {
    if (!svg) setup();
    const T = window.TIMING, V = window.VIDEO;
    let si = 0;
    T.scenes.forEach((s, i) => { if (t >= s.start) si = i; });
    const scene = T.scenes[si];
    let k = 0;
    scene.lines.forEach((l, j) => { if (t >= l.start) k = j; });
    const line = scene.lines[k], p = Math.max(0, t - line.start);
    const words = !poster && t >= line.start && t <= line.end + 0.3 ? line.text : "";
    const key = `${si}|${k}|${p < 0.5 ? Math.floor(p * 30) : "s"}|${words ? 1 : 0}|${poster ? 1 : 0}`;
    if (key === last) return key;
    last = key;
    svg.textContent = "";
    rect(svg, 0, 0, W, H, { fill: C.page, r: 0 });
    rect(svg, 0, 0, W, 6, { fill: C.accent, r: 0 });
    text(svg, 40, 46, V.label, { size: 20, weight: 800, fill: C.accent });
    text(svg, W - 40, 46, V.title, { size: 20, weight: 700, fill: C.grey, anchor: "end" });
    const g = group(svg);
    V.scenes[si](g, k, p);
    cap.innerHTML = words ? `<span>${words.replace(/&/g, "&amp;").replace(/</g, "&lt;")}</span>` : "";
    return key;
  };
})();
