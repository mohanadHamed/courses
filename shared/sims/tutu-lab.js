// Tutu Lab: the AI Extra of the Digital Skills worksheets, as on tutudocs.com
// (no sign-in): open your own file from the home page, ask the AI Assistant for
// a change (it edits the open file), then File › Download. Fixed answers, no AI.
//
// The page that loads it sets window.TUTU before this script:
//   kind:  "doc" | "sheet" | "slides"
//   file:  the student's file, e.g. "book-fair-Huda.docx"
//   model: the content (see the renderers below)
//   asks:  [{ text, keys: /regex/, done: "what the AI says", apply: (model) => {} }]
// doc:    [{ style: "Title" | "Heading 1" | "Normal", text, color?, bold? } | { table: [[...]] }]
// sheet:  { cols: ["A", "B", …], rows: [[{ v, b?, fill?, color? } or a value, …], …] }
// slides: [{ title, points: [...], sub?, bg?, color? }]
(() => {
  const T = window.TUTU;
  const $ = (s, el = document) => el.querySelector(s);
  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
  const btn = (html, title, fn, cls = "") => { const b = h("button", "w-btn " + cls); b.type = "button"; b.innerHTML = html; b.title = title; b.setAttribute("aria-label", title);
    b.addEventListener("click", (e) => { e.stopPropagation(); fn(e); }); return b; };
  const say = (text, bad) => { const m = $("#msg"); m.innerHTML = text; m.className = "message" + (bad ? " bad" : ""); };
  const EXT = { doc: ".docx", sheet: ".xlsx", slides: ".pptx" }[T.kind];
  const DL = { doc: "Microsoft Word (.docx)", sheet: "Microsoft Excel (.xlsx)", slides: "Microsoft PowerPoint (.pptx)" }[T.kind];
  const APP = { doc: "Word", sheet: "Excel", slides: "PowerPoint" }[T.kind];
  const MENUS = { doc: ["File", "Edit", "View", "Insert", "Format", "Tools", "Help"], sheet: ["File", "Edit", "View", "Insert", "Format", "Data", "Help"],
    slides: ["File", "Edit", "View", "Insert", "Format", "Slide", "Arrange", "Tools", "Help"] }[T.kind];
  const name = T.file.replace(/\.[a-z]+$/, "");
  let s;
  const reset = () => { s = { model: JSON.parse(JSON.stringify(T.model)), uploaded: false, chooser: false, panel: false, text: "", log: [], asked: new Set(), busy: false, menu: null, downloaded: false, fresh: null }; };

  const root = $("#tutu");
  root.className = "word web";
  root.innerHTML = `<div class="t-address"><span>&#8592; &#8594;</span><b>tutudocs.com</b></div><div class="t-top"></div>
    <div class="t-body"><div class="w-canvas"><div class="w-page"></div></div><div class="chat" id="chat"></div></div>
    <div class="w-status"><span class="t-count"></span></div>`;

  // ---------- The content of the file ----------
  function renderDoc(pg) {
    s.model.forEach((p, i) => {
      if (p.table) { const t = h("table", "w-table t-ro"); p.table.forEach((r, ri) => { const tr = h("tr"); r.forEach((v) => { const td = h(ri ? "td" : "th", "", String(v)); tr.appendChild(td); }); t.appendChild(tr); }); pg.appendChild(t); return; }
      const el = h("p", "w-p s-" + p.style.replace(" ", "") + (s.fresh && s.fresh.includes(i) ? " w-new" : ""), p.text);
      if (p.color) el.style.color = p.color; if (p.bold) el.style.fontWeight = "700"; if (p.align) el.style.textAlign = p.align;
      pg.appendChild(el);
    });
  }
  function cellOf(c) { return c !== null && typeof c === "object" ? c : { v: c }; }
  function renderSheet(pg) {
    const m = s.model; const t = h("table", "t-grid");
    const head = h("tr"); head.appendChild(h("th", "t-corner", "")); m.cols.forEach((c) => head.appendChild(h("th", "", c))); t.appendChild(head);
    m.rows.forEach((r, ri) => {
      const tr = h("tr"); tr.appendChild(h("th", "", String(ri + 1)));
      m.cols.forEach((_, ci) => { const c = cellOf(r[ci] === undefined ? "" : r[ci]); const td = h("td", (s.fresh && s.fresh.includes(ri + ":" + ci) ? "w-new" : ""), c.v === undefined ? "" : String(c.v));
        if (c.b) td.style.fontWeight = "700"; if (c.fill) td.style.background = c.fill; if (c.color) td.style.color = c.color; if (typeof c.v === "number") td.style.textAlign = "right"; tr.appendChild(td); });
      t.appendChild(tr);
    });
    pg.classList.add("t-sheet"); pg.appendChild(t);
  }
  function renderSlides(pg) {
    pg.classList.add("t-slides");
    const strip = h("div", "t-strip"); const big = h("div", "t-main");
    s.model.forEach((sl, i) => {
      const card = h("div", "t-slide" + (s.fresh && s.fresh.includes(i) ? " w-new" : ""));
      card.style.background = sl.bg || "#ffffff"; card.style.color = sl.color || "#222";
      card.appendChild(h("b", "", sl.title)); if (sl.sub) card.appendChild(h("small", "", sl.sub));
      if (sl.points) { const ul = h("ul"); sl.points.forEach((x) => ul.appendChild(h("li", "", x))); card.appendChild(ul); }
      const th = h("div", "t-thumb", String(i + 1)); th.appendChild(card.cloneNode(true)); strip.appendChild(th);
      if (i === (s.slide || 0)) big.appendChild(card);
      th.addEventListener("click", () => { s.slide = i; draw(); });
    });
    pg.appendChild(strip); pg.appendChild(big);
  }

  // ---------- tutudocs.com ----------
  function top() {
    const t = $(".t-top", root); t.innerHTML = "";
    if (!s.uploaded) return;
    const bar = h("div", "t-bar");
    bar.appendChild(h("b", "t-name", name));
    bar.appendChild(h("small", "t-saved", "Saved locally · Sign in to save to cloud"));
    bar.appendChild(btn("&#10024; AI Assistant", "AI Assistant", () => { s.panel = !s.panel; say(s.panel ? "The <b>AI assistant</b> opens on the right. Click in <b>Ask AI anything…</b> and type your request." : "The AI assistant is closed."); draw(); }, "t-ai" + (s.panel ? " on" : "")));
    t.appendChild(bar);
    const menus = h("div", "t-menus");
    MENUS.forEach((m) => menus.appendChild(btn(m, m, () => { if (m !== "File") { say(`<b>${m}</b>: not needed today. To download, use <b>File</b>.`, true); return; } s.menu = s.menu ? null : "file"; draw(); }, "t-menu" + (m === "File" && s.menu ? " on" : ""))));
    t.appendChild(menus);
    if (s.menu) {
      const m = h("div", "w-menu t-file");
      ["New", "Open...", "Make a copy", "Share", "Download ›", "Rename", "Save to browser", "Print..."].forEach((it) => {
        const b = btn(it, it, () => { if (it.startsWith("Download")) { s.menu = "download"; draw(); } else say(`<b>${it.replace(" ›", "")}</b>: not in today's steps. Choose <b>Download</b>.`, true); }, "t-item" + (it.startsWith("Download") && s.menu === "download" ? " on" : ""));
        if (it.startsWith("Download")) b.addEventListener("pointerenter", () => { if (s.menu !== "download") { s.menu = "download"; draw(); } });
        m.appendChild(b);
      });
      if (s.menu === "download") {
        const sub = h("div", "w-menu t-sub");
        [DL, "PDF", "HTML", "Plain text"].forEach((it) => sub.appendChild(btn(it, it, () => {
          s.menu = null;
          if (it === DL) { s.downloaded = true; say(`&#10003; <b>${T.file}</b> is in your <b>Downloads</b> folder. Open it: ${APP} shows the changes of the AI.`); }
          else say(`${it}: a different kind of file. Choose the ${APP} file (<b>${EXT}</b>).`, true);
          draw();
        }, "t-item")));
        m.appendChild(sub);
      }
      t.appendChild(m);
    }
  }
  function home(pg) {
    pg.classList.add("t-home");
    pg.appendChild(h("h2", "t-h", "Free online Word, Excel & PowerPoint"));
    pg.appendChild(h("p", "t-sub", "No sign-up · No install · Unlimited use · Free AI every day"));
    pg.appendChild(btn("<span class='t-up'>&#8679;</span><b>Drop a file anywhere on this page, or click to choose</b><small>Word / Excel / PPT / PDF / CSV / TXT all open</small>", "Choose a file", () => { s.chooser = true; draw(); }, "t-drop"));
    if (s.chooser) {
      const o = h("div", "w-menu t-open"); o.innerHTML = "<b>Open</b><div class='t-path'>This PC › <b>Desktop</b></div>";
      o.appendChild(btn(`<span class='c-doc'>${APP[0]}</span> ${T.file}`, T.file, () => { s.chooser = false; s.uploaded = true;
        say("Your file is open in the online editor, with no sign-in. Now click <b>AI Assistant</b> at the top."); draw(); }, "t-filebtn"));
      pg.appendChild(o);
    }
  }
  function chat() {
    const box = $("#chat", root); box.hidden = !(s.uploaded && s.panel); if (box.hidden) return;
    box.innerHTML = `<div class="c-head"><b>AI assistant</b></div><div class="c-log"></div>
      <div class="c-compose"><div class="c-line"><input class="c-input" aria-label="Ask AI anything" placeholder="Ask AI anything…"><button type="button" class="c-send" title="Send" aria-label="Send">&#10148;</button></div>
      <small class="c-try">Type a request, or tap one:</small><div class="c-asks"></div></div>`;
    const log = $(".c-log", box);
    if (!s.log.length) log.appendChild(h("div", "c-hello", "How can I help you?"));
    s.log.forEach((m) => { const d = h("div", "c-msg " + (m.ai ? "ai" : "me")); d.innerHTML = m.html; log.appendChild(d); });
    if (s.busy) log.appendChild(h("div", "c-msg ai c-typing", "Thinking…"));
    const input = $(".c-input", box); input.value = s.text;
    input.addEventListener("input", () => { s.text = input.value; });
    input.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); send(); } });
    $(".c-send", box).addEventListener("click", (e) => { e.stopPropagation(); send(); });
    T.asks.forEach((a) => $(".c-asks", box).appendChild(btn(a.text, "Use this request", () => { s.text = a.text; draw(); $(".c-input", root).focus(); }, "c-ask")));
    log.scrollTop = log.scrollHeight;
  }
  function send() {
    const text = s.text.trim(); if (!text) return;
    if (s.busy) { say("Wait for the answer of the AI, then send the next request.", true); return; }
    s.log.push({ ai: false, html: text.replace(/</g, "&lt;") }); s.text = ""; s.busy = true; draw();
    setTimeout(() => {
      s.busy = false;
      const ask = T.asks.find((a) => a.keys.test(text));
      if (!ask) s.log.push({ ai: true, html: `In this simulator I know ${T.asks.length} requests: tap one of them below. On tutudocs.com you can ask for any change.` });
      else { s.fresh = ask.apply(s.model) || null; s.asked.add(ask); s.log.push({ ai: true, html: ask.done });
        say(`&#10003; The AI changed the file (in yellow). ${s.asked.size < T.asks.length ? "Ask for one more change." : `Now <b>File › Download › ${DL}</b>.`}`); }
      draw();
    }, 1200);
  }

  // ---------- The steps ----------
  const MISSIONS = [
    [`On <b>tutudocs.com</b>: click the box <b>Drop a file…</b> and open <b>${T.file}</b>`, () => s.uploaded],
    ...T.asks.map((a) => [`<b>AI Assistant</b>: ask <b>${a.text}</b>`, () => s.asked.has(a)]),
    [`<b>File › Download › ${DL}</b>`, () => s.downloaded],
  ];
  function status() {
    const list = $("#jobs"); list.innerHTML = ""; let done = 0;
    MISSIONS.forEach(([t, f]) => { const ok = !!f(); done += ok; const li = h("li", ok ? "ok" : ""); li.innerHTML = t; list.appendChild(li); });
    $("#progress").textContent = `${done} of ${MISSIONS.length}`;
    $(".t-count", root).textContent = s.uploaded ? T.file : "tutudocs.com";
    if (done === MISSIONS.length && !status.done) { status.done = true; say("&#10003; All steps done. Now do it on tutudocs.com with your own file: the Extra of your worksheet."); }
  }
  function draw() {
    top();
    const pg = $(".w-page", root); pg.innerHTML = ""; pg.className = "w-page";
    if (!s.uploaded) home(pg); else ({ doc: renderDoc, sheet: renderSheet, slides: renderSlides })[T.kind](pg);
    chat(); status();
  }
  document.addEventListener("click", (e) => { if (s.menu && !e.target.closest(".w-menu")) { s.menu = null; draw(); } });
  $("#reset").addEventListener("click", () => { reset(); status.done = false; say(HELLO); draw(); });
  const HELLO = `This is <b>tutudocs.com</b>: no sign-in. Click the box <b>Drop a file…</b> and choose <b>${T.file}</b> on the Desktop.`;
  reset(); say(HELLO); draw();
})();
