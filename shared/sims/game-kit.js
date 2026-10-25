// Shared helper for mini-games and simulators. Load it after sim-base.js:
//   <script src="<relative path>/shared/sims/sim-base.js"></script>
//   <script src="<relative path>/shared/sims/game-kit.js"></script>
//
// Kit.game({...}) builds the usual round-based mini-game inside <main class="sim">:
// a line with the round, the goal and the stars, an optional canvas, one button
// per answer, a message line, "Next round" and "Sound". The game only gives its
// rounds, how to draw a round and how to judge an answer. Results are decided
// with a timer, never while drawing (a hidden tab draws nothing), and the draw
// loop keeps running when one frame fails (AUTHORING.md, "Robust game loops").
//
// Kit.canvas(), Kit.loop(), Kit.slider(), Kit.buttons() and Kit.beep() help the
// simulators that are not round-based (labs with sliders).
(() => {
  const Kit = {};
  let audio = null;
  Kit.sound = true;

  Kit.beep = (f, d = 0.15, type = "triangle", vol = 0.07) => {
    if (!Kit.sound) return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      const o = audio.createOscillator(), g = audio.createGain();
      o.type = type; o.frequency.value = f; g.gain.value = vol;
      o.connect(g); g.connect(audio.destination);
      g.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + d);
      o.start(); o.stop(audio.currentTime + d);
    } catch (_) { /* no sound on this device */ }
  };
  Kit.good = () => [660, 880, 1320].forEach((f, i) => setTimeout(() => Kit.beep(f, 0.13), i * 110));
  Kit.bad = () => Kit.beep(200, 0.3, "sawtooth");

  // A number with a real minus sign, rounded to d decimals.
  Kit.fmt = (v, d = 1) => {
    const k = Math.pow(10, d), r = Math.round(v * k) / k;
    return (r < 0 ? "−" : "") + Math.abs(r === 0 ? 0 : r);
  };

  Kit.el = (tag, attrs = {}, html = "") => {
    const e = document.createElement(tag);
    Object.entries(attrs).forEach(([k, v]) => (k === "class" ? (e.className = v) : e.setAttribute(k, v)));
    if (html) e.innerHTML = html;
    return e;
  };

  // A canvas that fills the width of its box. height(W) gives its height in CSS pixels.
  Kit.canvas = (el, height) => {
    const c = { el, ctx: el.getContext("2d"), W: 0, H: 0 };
    c.resize = () => {
      c.W = el.clientWidth || 300;
      c.H = Math.round(typeof height === "function" ? height(c.W) : height || c.W * 0.6);
      const dpr = window.devicePixelRatio || 1;
      el.width = Math.round(c.W * dpr); el.height = Math.round(c.H * dpr); el.style.height = c.H + "px";
      c.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    window.addEventListener("resize", c.resize);
    c.resize();
    return c;
  };

  // requestAnimationFrame first, then draw inside try/catch: one failed frame never stops the loop.
  Kit.loop = (draw) => {
    const step = (now) => { requestAnimationFrame(step); try { draw(now); } catch (e) { /* keep the loop alive */ } };
    requestAnimationFrame(step);
  };

  // A labelled slider with its value; returns the <input>.
  Kit.slider = (parent, label, min, max, step, value, onInput, show = (v) => v) => {
    const wrap = Kit.el("label");
    const span = Kit.el("span", {}, label);
    const input = Kit.el("input", { type: "range", min, max, step, value });
    const out = Kit.el("span", { class: "readout" });
    const upd = () => { out.textContent = show(+input.value); onInput && onInput(+input.value); };
    input.addEventListener("input", upd);
    wrap.append(span, input, out);
    parent.appendChild(wrap);
    upd();
    return input;
  };

  // A row of buttons; onPick(key) gets the key of the pressed one.
  Kit.buttons = (parent, items, onPick, cls = "ghost") => {
    parent.innerHTML = "";
    items.forEach((it) => {
      const b = Kit.el("button", { type: "button", class: cls, "data-k": it.k }, it.label);
      b.addEventListener("click", () => onPick(it.k, b));
      parent.appendChild(b);
    });
  };

  Kit.style = (css) => document.head.appendChild(Kit.el("style", {}, css));
  Kit.style(`
    .sim .hud { display: flex; flex-wrap: wrap; gap: 4px 14px; align-items: baseline; margin: 0 0 8px; font-weight: 800; font-variant-numeric: tabular-nums; }
    .sim .hud .lvl { color: var(--sim-accent); }
    .sim .hud .goal b { color: #e8590c; }
    .sim .hud .stars { margin-left: auto; }
    .sim .pad { display: grid; grid-template-columns: repeat(var(--cols, 3), minmax(0, 1fr)); gap: 6px; margin-top: 10px; }
    .sim .pad button { padding: 8px 6px; line-height: 1.25; }
    .sim .pad button.picked { background: var(--sim-accent); color: #fff; }
    .sim .row { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: center; margin-top: 10px; }
    .sim .calc { margin-top: 8px; font-weight: 700; font-variant-numeric: tabular-nums; min-height: 1.2em; }
    .sim .message.bad { color: #c92a2a; }
    .sim .panel { border: 1px solid var(--sim-border); border-radius: 12px; padding: 10px 12px; background: #fff; }
    @media (max-width: 520px) { .sim .pad { grid-template-columns: repeat(var(--cols-phone, 2), minmax(0, 1fr)); } }
  `);

  // Round-based mini-game.
  //   rounds:   [{ goal, choices: [{k, label}], answer, why: {k: text}, good, ... }]
  //   canvas:   height(W) of a canvas, or 0 for no canvas
  //   draw(ctx, W, H, now, round, state): draws the round (state.pick, state.t0, state.done, state.ok)
  //   judge(k, round): { ok, msg } (default: k === round.answer, round.why[k], round.good)
  //   calc(k, round): one line under the buttons when a choice is made (optional)
  //   animMs: time between the choice and the result (the animation), default 900
  //   cols, colsPhone: buttons per row
  //   intro: the message of round 1 (the story of the lesson)
  Kit.game = (o) => {
    const main = document.querySelector("main.sim");
    const hud = Kit.el("div", { class: "hud" }, '<span class="lvl" id="lvl"></span><span class="goal" id="goal"></span><span class="stars" id="stars">★ 0</span>');
    main.appendChild(hud);
    let cv = null;
    if (o.canvas) {
      const c = Kit.el("canvas", { id: "c", "aria-label": o.alt || "The game" });
      main.appendChild(c);
      cv = Kit.canvas(c, o.canvas);
    }
    const pad = Kit.el("div", { class: "pad", id: "choices" });
    pad.style.setProperty("--cols", o.cols || 3);
    pad.style.setProperty("--cols-phone", o.colsPhone || Math.min(o.cols || 3, 2));
    const calc = Kit.el("p", { class: "calc", id: "calc" });
    const msg = Kit.el("p", { class: "message", id: "msg" });
    const row = Kit.el("div", { class: "row" });
    const next = Kit.el("button", { type: "button", id: "next" }, "Next round ▶");
    const snd = Kit.el("button", { type: "button", id: "sound", class: "ghost" }, "Sound: on");
    row.append(next, snd);
    main.append(pad, calc, msg, row);

    const R = o.rounds;
    const st = { i: 0, stars: 0, tries: 0, solved: false, over: false, busy: false, pick: null, t0: 0, done: false, ok: false };
    Kit.state = st;
    const cur = () => R[st.i];

    function start() {
      if (st.i >= R.length) {
        st.over = true;
        document.getElementById("lvl").textContent = "All rounds done";
        document.getElementById("goal").textContent = "";
        pad.innerHTML = ""; calc.textContent = "";
        msg.textContent = `🎉 Well done! ★ ${st.stars} of ${R.length * 3}.`; msg.className = "message good";
        next.hidden = false; next.textContent = "Play again ▶";
        return;
      }
      Object.assign(st, { over: false, tries: 0, solved: false, busy: false, pick: null, t0: 0, done: false, ok: false });
      const r = cur();
      document.getElementById("lvl").textContent = `Round ${st.i + 1} / ${R.length}`;
      document.getElementById("goal").innerHTML = r.goal || "";
      Kit.buttons(pad, r.choices, choose);
      calc.textContent = "";
      msg.textContent = st.i === 0 && o.intro ? o.intro : (r.hint || o.hint || "Choose an answer.");
      msg.className = "message";
      next.hidden = true;
      if (o.start) o.start(r, st);
    }

    function choose(k, btn) {
      if (st.over) { msg.textContent = "All rounds are done. Press Play again."; return; }
      if (st.busy) { msg.textContent = "Wait: the last answer is still running."; return; }
      if (st.solved) { msg.textContent = "This round is done. Press Next round."; return; }
      st.tries++; st.busy = true; st.pick = k; st.t0 = performance.now(); st.done = false;
      pad.querySelectorAll("button").forEach((b) => b.classList.toggle("picked", b === btn));
      const r = cur();
      calc.innerHTML = o.calc ? o.calc(k, r) || "" : "";
      msg.textContent = o.running ? o.running(k, r) : "Checking your answer…"; msg.className = "message";
      if (o.onChoose) o.onChoose(k, r, st);
      Kit.beep(330, 0.25);
      setTimeout(() => {   // decide with a timer, not in draw()
        const res = o.judge ? o.judge(k, r, st) : { ok: k === r.answer, msg: k === r.answer ? r.good : (r.why && r.why[k]) || "Not this one. Try again." };
        st.done = true; st.busy = false; st.ok = res.ok;
        if (res.ok) {
          st.solved = true;
          const got = st.tries === 1 ? 3 : st.tries === 2 ? 2 : 1;
          st.stars += got;
          document.getElementById("stars").textContent = "★ " + st.stars;
          msg.textContent = `✓ ${"★".repeat(got)} ${res.msg || "Right!"}`; msg.className = "message good";
          next.hidden = false; next.textContent = st.i < R.length - 1 ? "Next round ▶" : "Finish ▶";
          Kit.good();
        } else {
          msg.textContent = "✗ " + (res.msg || "Not this one. Try again."); msg.className = "message bad";
          Kit.bad();
        }
      }, o.animMs ?? 900);
    }

    next.addEventListener("click", () => {
      if (st.over) { st.i = 0; st.stars = 0; document.getElementById("stars").textContent = "★ 0"; } else st.i++;
      start();
    });
    snd.addEventListener("click", () => { Kit.sound = !Kit.sound; snd.textContent = "Sound: " + (Kit.sound ? "on" : "off"); });
    start();
    if (cv && o.draw) Kit.loop((now) => { const c = cv.ctx; c.clearRect(0, 0, cv.W, cv.H); o.draw(c, cv.W, cv.H, now, st.over ? null : cur(), st); });
    return { st, cur, start, cv };
  };

  // Small drawing helpers for canvases.
  Kit.text = (c, s, x, y, size = 13, color = "#2a211c", align = "center", weight = 800) => {
    c.fillStyle = color; c.font = `${weight} ${size}px Nunito, system-ui, sans-serif`; c.textAlign = align; c.fillText(s, x, y);
  };
  Kit.rrect = (c, x, y, w, h, r, fill, stroke, lw = 2) => {
    c.beginPath();
    if (c.roundRect) c.roundRect(x, y, w, h, r); else c.rect(x, y, w, h);
    if (fill) { c.fillStyle = fill; c.fill(); }
    if (stroke) { c.strokeStyle = stroke; c.lineWidth = lw; c.stroke(); }
  };
  Kit.arrow = (c, x1, y1, x2, y2, color = "#2F9E44", lw = 3, head = 11) => {
    const a = Math.atan2(y2 - y1, x2 - x1);
    c.strokeStyle = color; c.fillStyle = color; c.lineWidth = lw; c.lineCap = "round";
    c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2 - Math.cos(a) * head * 0.8, y2 - Math.sin(a) * head * 0.8); c.stroke();
    c.beginPath(); c.moveTo(x2, y2);
    c.lineTo(x2 - head * Math.cos(a - 0.45), y2 - head * Math.sin(a - 0.45));
    c.lineTo(x2 - head * Math.cos(a + 0.45), y2 - head * Math.sin(a + 0.45));
    c.closePath(); c.fill();
  };
  // A coordinate grid: returns {X, Y} that map world units to the canvas.
  Kit.grid = (c, W, H, xmin, xmax, ymin, ymax, opts = {}) => {
    const u = Math.min((W - 30) / (xmax - xmin), (H - 30) / (ymax - ymin));
    const ox = (W - u * (xmax - xmin)) / 2 - xmin * u, oy = (H - u * (ymax - ymin)) / 2 + ymax * u;
    const X = (x) => ox + x * u, Y = (y) => oy - y * u;
    c.fillStyle = opts.bg || "#f4faf5"; c.fillRect(0, 0, W, H);
    c.strokeStyle = opts.grid || "#dbeadb"; c.lineWidth = 1;
    for (let i = Math.ceil(xmin); i <= xmax; i++) { c.beginPath(); c.moveTo(X(i), Y(ymin)); c.lineTo(X(i), Y(ymax)); c.stroke(); }
    for (let j = Math.ceil(ymin); j <= ymax; j++) { c.beginPath(); c.moveTo(X(xmin), Y(j)); c.lineTo(X(xmax), Y(j)); c.stroke(); }
    c.strokeStyle = opts.axis || "#9bb8a0"; c.lineWidth = 1.6;
    c.beginPath(); c.moveTo(X(xmin), Y(0)); c.lineTo(X(xmax), Y(0)); c.stroke();
    c.beginPath(); c.moveTo(X(0), Y(ymin)); c.lineTo(X(0), Y(ymax)); c.stroke();
    if (opts.labels !== false) {
      const s = opts.step || 1;
      for (let i = Math.ceil(xmin / s) * s; i <= xmax; i += s) if (i) Kit.text(c, Kit.fmt(i), X(i), Y(0) + 13, 10, "#6b726e", "center", 700);
      for (let j = Math.ceil(ymin / s) * s; j <= ymax; j += s) if (j) Kit.text(c, Kit.fmt(j), X(0) - 5, Y(j) + 4, 10, "#6b726e", "right", 700);
    }
    return { X, Y, u };
  };

  window.Kit = Kit;
})();
