// Word Lab: a simulator that looks like Word for Windows (the classic ribbon),
// with the notice of the Lecture 4 worksheet. One engine, three parts, chosen by
// the page that loads it (window.WORD_LAB = "format" | "table" | "ai"):
//   format: styles (Title, Heading 1), the Navigation Pane, Center, Bold, a colour;
//   table:  Insert › Table (2 x 4) and the prices typed in its cells;
//   ai:     the Extra of the worksheet: attach the notice to an AI chat, ask for
//           a change, and open the new file (fixed answers, no AI service).
// The steps are the steps of the worksheet, so the teacher shows them here first.
(() => {
  const PART = window.WORD_LAB || "format";
  const $ = (s, el = document) => el.querySelector(s);
  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };

  // ---------- The document ----------
  const P = (text, style = "Normal", extra = {}) => ({ style, align: "left", words: text ? text.split(" ").map((t) => ({ t, b: false, c: null })) : [], ...extra });
  function start() {
    if (PART === "format") return [P("Book Fair", "Plain"), P("When and where", "Plain"), P("Sunday to Tuesday, 10:00 to 15:00, in the college library.", "Plain"), P("Entry is free.", "Plain"), P("Prices", "Plain")];
    const done = [P("Book Fair", "Title", { align: "center" }), P("When and where", "Heading 1"), P("Sunday to Tuesday, 10:00 to 15:00, in the college library."), P("Entry is free."), P("Prices", "Heading 1")];
    done[3].words[2].b = true; done[3].words[2].c = "#e03131";
    if (PART === "table") return [...done, P("")];
    return [...done, { table: [["Book", "Price (JD)"], ["Novel", "3"], ["Dictionary", "5"], ["Notebook", "1"]] }];
  }
  // The AI chat of the "ai" part: the file attached, the requests sent, the changes opened.
  let chat;
  const ASKS = [
    { id: 1, text: "Make the title Book Fair blue, and add a row to the table: Magazine, 2.", keys: /blue|magazine|row/i,
      apply: () => { doc[0].words.forEach((w) => { w.c = "#1c7ed6"; }); table().table.push(["Magazine", "2"]); return "The title is blue, and the table has a new row: Magazine, 2."; } },
    { id: 2, text: "Add a heading About the fair and two short sentences that invite students.", keys: /about|sentence|paragraph|invite/i,
      apply: () => { doc.push(P("About the fair", "Heading 1", { fresh: true }), P("Come and find a new book to read!", "Normal", { fresh: true }), P("Bring your friends: entry is free.", "Normal", { fresh: true })); return "A new heading and two sentences are at the end."; } },
  ];
  let doc, caret, sel, typing, nav, tab, menu;
  function reset() { doc = start(); caret = PART === "table" ? 5 : null; sel = null; typing = false; nav = false; tab = "Home"; menu = null;
    chat = { attached: false, text: "", log: [{ ai: true, html: "Hi! Attach a file and tell me what to change." }], opened: new Set(), busy: false }; }

  // ---------- The missions (the steps of the worksheet) ----------
  const wordsOf = (p) => p.words.map((w) => w.t).join(" ");
  const find = (text) => doc.find((p) => !p.table && wordsOf(p).replace(/[.!]$/, "") === text);
  const table = () => doc.find((p) => p.table);
  const cell = (r, c) => { const t = table(); return t && t.table[r] && t.table[r][c] !== undefined ? t.table[r][c].trim().toLowerCase() : ""; };
  const MISSIONS = {
    format: [
      ["<b>Book Fair</b>: click in it, then <b>Styles › Title</b>", () => find("Book Fair")?.style === "Title"],
      ["<b>When and where</b> and <b>Prices</b>: <b>Heading 1</b>", () => find("When and where")?.style === "Heading 1" && find("Prices")?.style === "Heading 1"],
      ["<b>View › Navigation Pane</b>: the headings on the left", () => nav],
      ["<b>Book Fair</b>: <b>Center</b>", () => find("Book Fair")?.align === "center"],
      ["<b>free</b>: double-click it, then <b>B</b> and a <b>red</b> colour", () => { const p = find("Entry is free"); if (!p) return false; const w = p.words[2]; return w.b && w.c === "#e03131" && p.words.every((x, i) => i === 2 || !x.b); }],
    ],
    table: [
      ["<b>Insert › Table</b>: 2 across, 4 down (<b>2x4 Table</b>)", () => { const t = table(); return t && t.table.length === 4 && t.table[0].length === 2; }],
      ["The first row: <b>Book</b> | <b>Price (JD)</b>", () => cell(0, 0) === "book" && cell(0, 1).replace(/\s/g, "") === "price(jd)"],
      ["Novel 3 · Dictionary 5 · Notebook 1 (<b>Tab</b>: the next cell)", () => cell(1, 0) === "novel" && cell(1, 1) === "3" && cell(2, 0) === "dictionary" && cell(2, 1) === "5" && cell(3, 0) === "notebook" && cell(3, 1) === "1"],
    ],
    ai: [
      ["<b>Attach</b> your file to the chat: <b>book-fair-Huda.docx</b>", () => chat.attached],
      ["Ask: <b>the title blue, and a row: Magazine, 2</b>. Then open the new file", () => chat.opened.has(1)],
      ["Ask: <b>a heading About the fair and two sentences</b>. Then open the new file", () => chat.opened.has(2)],
    ],
  }[PART];

  // ---------- The window ----------
  const root = $("#word");
  root.innerHTML = `
    <div class="w-title"><span class="w-auto">AutoSave <i></i> Off</span><b>Document1 - Word</b><span class="w-search">Search</span><span class="w-win">&#8211; &#9633; &#10005;</span></div>
    <div class="w-tabs"></div>
    <div class="w-ribbon"></div>
    <div class="w-body"><div class="w-nav"></div><div class="w-canvas"><div class="w-page"></div></div></div>
    <div class="w-status"><span>Page 1 of 1</span><span class="w-count"></span><span>English (United States)</span></div>`;
  const TABS = ["File", "Home", "Insert", "Draw", "Design", "Layout", "References", "Mailings", "Review", "View", "Help"];
  const say = (text, bad) => { const m = $("#msg"); m.innerHTML = text; m.className = "message" + (bad ? " bad" : ""); };

  function tabs() {
    const bar = $(".w-tabs", root); bar.innerHTML = "";
    TABS.forEach((t) => {
      const b = h("button", "w-tab" + (t === tab ? " on" : ""), t); b.type = "button";
      b.addEventListener("click", () => {
        if (["Home", "Insert", "View"].includes(t)) { tab = t; menu = null; draw(); }
        else say(`<b>${t}</b>: not needed today. Use <b>Home</b>, <b>Insert</b> or <b>View</b>.`, true);
      });
      bar.appendChild(b);
    });
  }
  const group = (label, ...items) => { const g = h("div", "w-group"); const row = h("div", "w-row"); items.forEach((i) => row.appendChild(i)); g.appendChild(row); g.appendChild(h("small", "", label)); return g; };
  const btn = (html, title, fn, cls = "") => { const b = h("button", "w-btn " + cls); b.type = "button"; b.innerHTML = html; b.title = title; b.setAttribute("aria-label", title); b.addEventListener("click", (e) => { e.stopPropagation(); fn(e); }); return b; };
  const lines = (kind) => { const w = { left: [16, 11, 16, 9], center: [16, 10, 16, 10], right: [16, 11, 16, 9], justify: [16, 16, 16, 16] }[kind];
    return `<svg width="18" height="16" viewBox="0 0 18 16">${w.map((l, i) => { const x = kind === "left" || kind === "justify" ? 1 : kind === "center" ? 1 + (16 - l) / 2 : 17 - l; return `<rect x="${x}" y="${1 + i * 4}" width="${l}" height="1.6" fill="#323130"/>`; }).join("")}</svg>`; };

  function ribbon() {
    const r = $(".w-ribbon", root); r.innerHTML = "";
    const curStyle = caret !== null && doc[caret] && !doc[caret].table ? doc[caret].style : null;
    if (tab === "Home") {
      r.appendChild(group("Clipboard", btn("<span class='w-big'>&#128203;</span>Paste", "Paste", () => say("Paste: not needed here.", true), "w-tall"), btn("&#9986; Cut", "Cut", cut)));
      const colour = btn("<b class='w-a'>A</b><span class='w-bar'></span>&#9662;", "Font Color", () => { menu = menu === "color" ? null : "color"; draw(); }, "w-color");
      r.appendChild(group("Font",
        h("span", "w-box", "Calibri (Body) ▾"), h("span", "w-box w-size", "11 ▾"),
        btn("<b>B</b>", "Bold", () => fontCmd("b")), btn("<i>I</i>", "Italic", () => say("Italic: not in today's steps.", true)),
        btn("<u>U</u>", "Underline", () => say("Underline: not in today's steps.", true)), colour));
      r.appendChild(group("Paragraph", ...["left", "center", "right", "justify"].map((k) => btn(lines(k), { left: "Align Left", center: "Center", right: "Align Right", justify: "Justify" }[k], () => align(k), caret !== null && doc[caret] && doc[caret].align === k ? "on" : ""))));
      const styles = h("div", "w-styles");
      [["Normal", "AaBbCcDd"], ["No Spacing", "AaBbCcDd"], ["Heading 1", "AaBbCc"], ["Heading 2", "AaBbCcD"], ["Title", "AaB"]].forEach(([n, s]) => {
        const b = btn(`<span class="w-sample s-${n.replace(" ", "")}">${s}</span><span>${n}</span>`, n, () => style(n), "w-style" + (curStyle === n || (curStyle === "Plain" && n === "Normal") ? " on" : ""));
        styles.appendChild(b);
      });
      r.appendChild(group("Styles", styles));
      if (menu === "color") {
        const m = h("div", "w-menu w-colors"); m.appendChild(h("b", "", "Standard Colors"));
        const row = h("div", "w-row");
        [["Dark Red", "#c00000"], ["Red", "#e03131"], ["Orange", "#f59f00"], ["Yellow", "#ffd43b"], ["Green", "#2f9e44"], ["Blue", "#1c7ed6"], ["Dark Blue", "#1f3a93"], ["Purple", "#7048e8"], ["Black", "#000000"]].forEach(([n, c]) => {
          const b = btn("", n, () => { menu = null; fontCmd("c", c === "#000000" ? null : c, n); }, "w-swatch"); b.style.background = c; row.appendChild(b);
        });
        m.appendChild(row); colour.parentElement.parentElement.appendChild(m);
      }
    } else if (tab === "Insert") {
      r.appendChild(group("Pages", h("span", "w-item", "Cover Page"), h("span", "w-item", "Blank Page"), h("span", "w-item", "Page Break")));
      const t = btn("<span class='w-big'>&#9638;</span>Table ▾", "Table", () => { menu = menu === "table" ? null : "table"; draw(); }, "w-tall");
      r.appendChild(group("Tables", t));
      r.appendChild(group("Illustrations", btn("<span class='w-big'>&#128444;</span>Pictures", "Pictures", () => say("Pictures: not in today's steps.", true), "w-tall"), btn("<span class='w-big'>&#9711;</span>Shapes", "Shapes", () => say("Shapes: not in today's steps.", true), "w-tall")));
      if (menu === "table") t.parentElement.parentElement.appendChild(tableGrid());
    } else {
      const box = h("label", "w-check"); const c = h("input"); c.type = "checkbox"; c.checked = nav;
      c.addEventListener("change", () => { nav = c.checked; say(nav ? "The <b>Navigation Pane</b> shows the lines with a <b>heading style</b>. The title and the normal text are not in it." : "The Navigation Pane is closed."); draw(); });
      box.appendChild(c); box.appendChild(document.createTextNode(" Navigation Pane"));
      const ruler = h("label", "w-check"); ruler.innerHTML = "<input type='checkbox' disabled> Ruler";
      r.appendChild(group("Views", h("span", "w-item on", "Print Layout"), h("span", "w-item", "Web Layout")));
      r.appendChild(group("Show", ruler, box));
    }
  }

  function tableGrid() {
    const m = h("div", "w-menu w-grid"); const label = h("b", "", "Insert Table"); m.appendChild(label);
    const g = h("div", "w-cells");
    for (let r = 0; r < 6; r++) for (let c = 0; c < 8; c++) {
      const d = h("button", "w-cell"); d.type = "button"; d.dataset.r = r; d.dataset.c = c; d.setAttribute("aria-label", `${c + 1}x${r + 1} Table`);
      const light = () => { g.querySelectorAll(".w-cell").forEach((x) => x.classList.toggle("on", +x.dataset.r <= r && +x.dataset.c <= c)); label.textContent = `${c + 1}x${r + 1} Table`; };
      d.addEventListener("pointerenter", light); d.addEventListener("focus", light);
      d.addEventListener("click", (e) => { e.stopPropagation(); insertTable(c + 1, r + 1); });
      g.appendChild(d);
    }
    m.appendChild(g); return m;
  }

  // ---------- Commands ----------
  function need(what) {
    if (what === "caret" && caret === null) { say("First <b>click in a line</b> of the page.", true); return false; }
    if (what === "word" && !sel) { say("First <b>select a word</b>: double-click it.", true); return false; }
    return true;
  }
  function style(n) {
    if (!need("caret")) return;
    const p = doc[caret]; if (p.table) return;
    p.style = n === "No Spacing" ? "Normal" : n;
    say(`<b>${n}</b>: the whole line <b>${wordsOf(p) || "(empty)"}</b> changed with one click. ${n.startsWith("Heading") ? "A heading also goes into the <b>Navigation Pane</b>." : ""}`);
    draw();
  }
  function align(k) {
    if (!need("caret")) return;
    doc[caret].align = k;
    say(`<b>${k === "center" ? "Center" : k}</b> moved <b>the whole line</b>: a click in the line was enough (paragraph formatting).`);
    draw();
  }
  function fontCmd(kind, value, name) {
    if (!sel) { if (caret !== null) say("Bold and colour change <b>only the selected words</b>. First double-click the word.", true); else need("word"); return; }
    const w = doc[sel.p].words[sel.w];
    if (kind === "b") { w.b = !w.b; say(`<b>Bold</b> changed <b>only the word "${w.t.replace(/[.,!]/g, "")}"</b>: font formatting changes only the selection.`); }
    else { w.c = value; say(`<b>${name}</b>: only the selected word changed colour.`); }
    draw();
  }
  function cut() {
    if (sel) { const p = doc[sel.p]; p.words.splice(sel.w, 1); sel = null; say("<b>Cut</b> took the selected word away."); draw(); return; }
    if (!need("caret")) return;
    const removed = wordsOf(doc[caret]);
    doc.splice(caret, 1); caret = null;
    say(`<b>Cut</b> took the line away: <i>${removed}</i>`);
    draw();
  }
  function insertTable(cols, rows) {
    menu = null;
    if (caret === null) { say("First <b>click in the empty line</b> under <b>Prices</b>.", true); draw(); return; }
    const t = { table: Array.from({ length: rows }, () => Array(cols).fill("")) };
    if (doc[caret].words.length === 0) doc.splice(caret, 0, t); else doc.splice(caret + 1, 0, t);
    say(`A table of <b>${cols} columns</b> and <b>${rows} rows</b>. Click in the first cell and type. <b>Tab</b> goes to the next cell.` + (cols === 2 && rows === 4 ? "" : " (The worksheet needs 2x4: click <b>Start again</b>.)"), !(cols === 2 && rows === 4));
    draw();
    const first = $(".w-page input", root); if (first) first.focus();
  }

  // Typing over a selected word (the time 17:00 -> 15:00).
  document.addEventListener("keydown", (e) => {
    if (!sel || e.target.tagName === "INPUT" || e.ctrlKey || e.metaKey || e.altKey) return;
    const w = doc[sel.p].words[sel.w];
    if (e.key.length === 1 && e.key !== " ") { w.t = typing ? w.t + e.key : e.key; typing = true; e.preventDefault(); draw(); }
    else if (e.key === "Backspace") { w.t = typing ? w.t.slice(0, -1) : ""; typing = true; e.preventDefault(); draw(); }
    else if (e.key === "Enter" || e.key === "Escape") { sel = null; typing = false; draw(); }
  });

  // ---------- The page ----------
  const SPELL = { studnets: ["students", "student's", "students'"] };
  function page() {
    const pg = $(".w-page", root); pg.innerHTML = "";
    doc.forEach((p, i) => {
      if (p.table) {
        const t = h("table", "w-table");
        p.table.forEach((row, r) => { const tr = h("tr"); row.forEach((v, c) => { const td = h("td"); const inp = h("input"); inp.value = v; inp.setAttribute("aria-label", `row ${r + 1}, column ${c + 1}`);
          inp.addEventListener("input", () => { p.table[r][c] = inp.value; status(); }); td.appendChild(inp); tr.appendChild(td); }); t.appendChild(tr); });
        pg.appendChild(t); return;
      }
      const el = h("p", "w-p s-" + p.style.replace(" ", "") + (caret === i ? " caret" : "") + (p.fresh ? " w-new" : ""));
      el.style.textAlign = p.align;
      if (!p.words.length) el.innerHTML = "&nbsp;";
      p.words.forEach((w, k) => {
        const bare = w.t.replace(/[.,!]/g, "");
        const s = h("span", "w-w" + (sel && sel.p === i && sel.w === k ? " sel" : "") + (SPELL[bare] ? " w-spell" : ""), w.t);
        if (w.b) s.style.fontWeight = "700"; if (w.c) s.style.color = w.c;
        s.addEventListener("dblclick", (e) => { e.stopPropagation(); sel = { p: i, w: k }; caret = i; typing = false; menu = null; say(`<b>"${bare}"</b> is selected. Now use a button of <b>Home › Font</b>.`); draw(); });
        const spell = (e) => { e.preventDefault(); e.stopPropagation(); menu = { spell: { p: i, w: k, x: e.clientX, y: e.clientY } }; draw(); };
        if (SPELL[bare]) { s.addEventListener("contextmenu", spell); s.addEventListener("click", (e) => { if (e.pointerType === "touch") spell(e); }); }
        el.appendChild(s); if (k < p.words.length - 1) el.appendChild(document.createTextNode(" "));
      });
      el.addEventListener("click", () => { caret = i; sel = null; typing = false; menu = null; say(`The cursor is in <b>${wordsOf(p) || "the empty line"}</b>.`); draw(); });
      pg.appendChild(el);
    });
    if (menu && menu.spell) {
      const { p, w } = menu.spell; const word = doc[p].words[w]; const bare = word.t.replace(/[.,!]/g, "");
      const m = h("div", "w-menu w-context");
      SPELL[bare].forEach((s, n) => m.appendChild(btn(n === 0 ? `<b>${s}</b>` : s, s, () => { word.t = word.t.replace(bare, s); menu = null; say(`Fixed: <b>${s}</b>. The red line is gone.`); draw(); })));
      ["Ignore All", "Add to Dictionary"].forEach((s) => m.appendChild(btn(s, s, () => { menu = null; say("Choose the right spelling: <b>students</b>.", true); draw(); })));
      pg.appendChild(m);
      const anchor = pg.querySelectorAll(".w-p")[p].querySelectorAll(".w-w")[w];
      m.style.left = Math.min(anchor.offsetLeft, pg.clientWidth - 190) + "px"; m.style.top = anchor.offsetTop + anchor.offsetHeight + 4 + "px";
    }
  }
  function navPane() {
    const n = $(".w-nav", root); n.hidden = !nav; if (!nav) return;
    n.innerHTML = "<b>Navigation</b><div class='w-navtabs'><u>Headings</u> Pages Results</div>";
    doc.filter((p) => !p.table && p.style.startsWith("Heading")).forEach((p) => n.appendChild(h("div", "w-navh" + (p.style === "Heading 2" ? " h2" : ""), wordsOf(p))));
  }
  function status() {
    const n = doc.reduce((a, p) => a + (p.table ? p.table.flat().filter((v) => v.trim()).length : p.words.length), 0);
    $(".w-count", root).textContent = n + " words";
    const list = $("#jobs"); list.innerHTML = "";
    let done = 0;
    MISSIONS.forEach(([t, f], i) => { const ok = !!f(); done += ok; const li = h("li", ok ? "ok" : ""); li.innerHTML = t; list.appendChild(li); });
    $("#progress").textContent = `${done} of ${MISSIONS.length}`;
    if (done === MISSIONS.length && !status.done) { status.done = true; say(PART === "ai" ? "&#10003; All steps done. Now try it with a real AI assistant and your own notice (the Extra of your worksheet)." : "&#10003; All steps done. The same steps are in your worksheet: now do them in Word."); }
  }
  // ---------- The AI chat ("ai" part) ----------
  function chatBox() {
    const box = $("#chat"); if (!box) return;
    box.innerHTML = `<div class="c-head"><span class="c-dot"></span><b>AI assistant</b><small>ChatGPT, Gemini, Claude, Copilot…</small></div><div class="c-log"></div>
      <div class="c-compose"><div class="c-files"></div><div class="c-line"><button type="button" class="c-attach" title="Attach a file" aria-label="Attach a file">&#128206;</button>
      <input class="c-input" aria-label="Your message" placeholder="Type, or choose a request below"><button type="button" class="c-send" title="Send" aria-label="Send">&#10148;</button></div>
      <div class="c-asks"></div></div>`;
    const log = $(".c-log", box);
    chat.log.forEach((m) => { const d = h("div", "c-msg " + (m.ai ? "ai" : "me")); d.innerHTML = m.html; log.appendChild(d);
      if (m.file) { const f = btn(`<span class="c-doc">W</span><span><b>${m.file}</b><small>Word document · click to open</small></span>`, "Download and open", () => openFile(m), "c-file" + (chat.opened.has(m.ask) ? " done" : "")); d.appendChild(f); } });
    if (chat.busy) log.appendChild(h("div", "c-msg ai c-typing", "…"));
    if (chat.attached) { const f = h("span", "c-chip"); f.innerHTML = "<span class='c-doc'>W</span> book-fair-Huda.docx"; $(".c-files", box).appendChild(f); }
    const input = $(".c-input", box); input.value = chat.text;
    input.addEventListener("input", () => { chat.text = input.value; });
    input.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); send(); } });
    $(".c-attach", box).addEventListener("click", (e) => { e.stopPropagation(); if (chat.attached) { say("The file is attached already."); return; }
      chat.attached = true; say("<b>Attached:</b> book-fair-Huda.docx, the file that you saved on the Desktop. Now ask for a change."); draw(); });
    $(".c-send", box).addEventListener("click", (e) => { e.stopPropagation(); send(); });
    ASKS.forEach((a) => $(".c-asks", box).appendChild(btn(a.text, "Use this request", () => { chat.text = a.text; draw(); $(".c-input").focus(); }, "c-ask")));
    log.scrollTop = log.scrollHeight;
  }
  function send() {
    const text = chat.text.trim(); if (!text || chat.busy) return;
    chat.log.push({ ai: false, html: (chat.attached ? "<span class='c-chip small'><span class='c-doc'>W</span> book-fair-Huda.docx</span><br>" : "") + text.replace(/</g, "&lt;") });
    chat.text = ""; chat.busy = true; draw();
    setTimeout(() => {
      chat.busy = false;
      const ask = ASKS.find((a) => a.keys.test(text));
      if (!chat.attached) chat.log.push({ ai: true, html: "I can't see your notice yet. Click the <b>attach</b> button (&#128206;) and choose your Word file, then ask again." });
      else if (!ask) chat.log.push({ ai: true, html: "In this simulator I know two requests: choose one of them below. In a real AI chat, you can ask for any change." });
      else chat.log.push({ ai: true, html: "Done! Here is your notice with the change:", file: `book-fair-Huda (${ask.id + 1}).docx`, ask: ask.id });
      draw();
    }, 900);
  }
  function openFile(m) {
    if (chat.opened.has(m.ask)) { say("This file is open already: look at the page."); return; }
    const ask = ASKS.find((a) => a.id === m.ask);
    doc.forEach((p) => { delete p.fresh; });
    const what = ask.apply(); chat.opened.add(ask.id);
    say(`&#10003; <b>${m.file}</b> is open in Word. ${what}`);
    draw();
  }

  function draw() { tabs(); ribbon(); page(); navPane(); chatBox(); status(); }
  document.addEventListener("click", (e) => { if (menu && !e.target.closest(".w-menu")) { menu = null; draw(); } });
  $("#reset").addEventListener("click", () => { reset(); status.done = false; say(HELLO); draw(); });
  const HELLO = { format: "Click in the line <b>Book Fair</b>. Then click <b>Title</b> in <b>Home › Styles</b>.",
    table: "The cursor is in the empty line under <b>Prices</b>. Click the <b>Insert</b> tab.",
    ai: "Your notice is saved on the Desktop. Click the attach button (&#128206;) of the AI chat." }[PART];
  reset(); say(HELLO); draw();
})();
