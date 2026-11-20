// Excel Lab: a simulator that looks like Excel for Windows (the classic ribbon),
// for the Digital Skills lectures and online activities. The page sets
// window.EXCEL_LAB before this script:
//   name:     the file name in the title bar ("Book1")
//   data:     the start cells, rows of values or formulas ("=B2*C2"); row 1 = row 1
//   cols:     how many columns to show (default 6), rows: how many rows (default 10)
//   tabs:     the tabs that work, e.g. ["Home", "Insert", "Data"]
//   missions: [[html, (x) => true when done]]; x gives v(ref) (the value), f(ref)
//             (what is typed), fill(ref), cf, chart, filter, sel
//   hello:    the first message
// Typing: click a cell and type (Enter: down, Tab: right); a formula starts
// with =. The fill handle (the small square of the selected cell): double-click
// it to copy the formula down. Shift + click selects a range.
(() => {
  const C = window.EXCEL_LAB;
  const $ = (s, el = document) => el.querySelector(s);
  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
  const btn = (html, title, fn, cls = "") => { const b = h("button", "w-btn " + cls); b.type = "button"; b.innerHTML = html; b.title = title; b.setAttribute("aria-label", title);
    b.addEventListener("click", (e) => { e.stopPropagation(); fn(e); }); return b; };
  const say = (text, bad) => { const m = $("#msg"); m.innerHTML = text; m.className = "message" + (bad ? " bad" : ""); };
  const NC = C.cols || 6, NR = C.rows || 10;
  const L = (c) => String.fromCharCode(65 + c);
  const ref = (r, c) => L(c) + (r + 1);
  const parse = (a) => { const m = /^\$?([A-Z])\$?(\d+)$/.exec(a.toUpperCase()); return m ? [+m[2] - 1, m[1].charCodeAt(0) - 65] : null; };

  let S;
  function reset() {
    const cells = {};
    (C.data || []).forEach((row, r) => row.forEach((v, c) => { if (v !== "" && v !== null && v !== undefined) cells[ref(r, c)] = { raw: String(v) }; }));
    S = { cells, sel: [0, 0], end: null, edit: null, tab: "Home", menu: null, filter: null, cf: [], chart: null, sorted: null, order: null };
  }

  // ---------- Formulas ----------
  function range(a, b) { const p = parse(a), q = parse(b); const out = [];
    for (let r = Math.min(p[0], q[0]); r <= Math.max(p[0], q[0]); r++) for (let c = Math.min(p[1], q[1]); c <= Math.max(p[1], q[1]); c++) out.push(ref(r, c)); return out; }
  function val(rf, seen = {}) {
    const cell = S.cells[rf.replace(/\$/g, "")]; if (!cell) return 0;
    const raw = cell.raw;
    if (raw[0] !== "=") { const n = Number(raw.replace("%", "")); return raw.trim() !== "" && !isNaN(n) ? (raw.includes("%") ? n / 100 : n) : raw; }
    if (seen[rf]) return "#REF!"; seen[rf] = 1;
    try {
      let ex = raw.slice(1).toUpperCase();
      ex = ex.replace(/(SUM|AVERAGE|MAX|MIN)\(\s*(\$?[A-Z]\$?\d+)\s*:\s*(\$?[A-Z]\$?\d+)\s*\)/g, (_, fn, a, b) => {
        const vs = range(a, b).map((x) => val(x, { ...seen })).filter((x) => typeof x === "number");
        const r = fn === "SUM" ? vs.reduce((s, x) => s + x, 0) : fn === "AVERAGE" ? (vs.length ? vs.reduce((s, x) => s + x, 0) / vs.length : 0) : fn === "MAX" ? Math.max(...vs) : Math.min(...vs);
        return "(" + r + ")"; });
      ex = ex.replace(/\$?[A-Z]\$?\d+/g, (a) => { const x = val(a, { ...seen }); return typeof x === "number" ? "(" + x + ")" : "0"; });
      if (!/^[\d+\-*/().\s]*$/.test(ex)) return "#NAME?";
      const n = Function("return " + ex)();
      return Number.isFinite(n) ? Math.round(n * 1000) / 1000 : "#DIV/0!";
    } catch (e) { return "#NAME?"; }
  }
  const show = (rf) => { const v = val(rf); const cell = S.cells[rf]; if (cell && cell.raw.includes("%") && cell.raw[0] !== "=") return cell.raw; return v === 0 && !cell ? "" : String(v); };
  function shift(raw, dr, dc) { return raw.replace(/(\$?)([A-Z])(\$?)(\d+)/g, (m, d1, col, d2, row) =>
    (d1 ? d1 + col : L(col.charCodeAt(0) - 65 + dc)) + (d2 ? d2 + row : String(+row + dr))); }

  // ---------- The window ----------
  const root = $("#excel"); root.className = "word excel";
  root.innerHTML = `<div class="w-title"><span class="w-auto">AutoSave <i></i> Off</span><b>${C.name || "Book1"} - Excel</b><span class="w-search">Search</span><span class="w-win">&#8211; &#9633; &#10005;</span></div>
    <div class="w-tabs"></div><div class="w-ribbon"></div>
    <div class="x-fbar"><span class="x-name"></span><span class="x-fx">fx</span><span class="x-f"></span></div>
    <div class="x-body"><div class="x-gridwrap"></div><div class="x-chartwrap"></div></div>
    <div class="w-status"><span>Ready</span><span class="x-sum"></span></div>`;
  const TABS = ["File", "Home", "Insert", "Page Layout", "Formulas", "Data", "Review", "View", "Help"];
  const OPEN = C.tabs || ["Home"];
  const group = (label, ...items) => { const g = h("div", "w-group"); const row = h("div", "w-row"); items.forEach((i) => row.appendChild(i)); g.appendChild(row); g.appendChild(h("small", "", label)); return g; };
  function tabs() {
    const bar = $(".w-tabs", root); bar.innerHTML = "";
    TABS.forEach((t) => bar.appendChild(btn(t, t, () => { if (OPEN.includes(t)) { S.tab = t; S.menu = null; draw(); } else say(`<b>${t}</b>: not needed here. Use ${OPEN.map((x) => "<b>" + x + "</b>").join(", ")}.`, true); }, "w-tab" + (t === S.tab ? " on" : ""))));
  }
  const selRange = () => { const a = S.sel, b = S.end || S.sel; return [Math.min(a[0], b[0]), Math.min(a[1], b[1]), Math.max(a[0], b[0]), Math.max(a[1], b[1])]; };
  const lastRow = () => { let m = 0; Object.keys(S.cells).forEach((k) => { m = Math.max(m, parse(k)[0]); }); return m; };
  function ribbon() {
    const r = $(".w-ribbon", root); r.innerHTML = "";
    if (S.tab === "Home") {
      r.appendChild(group("Font", h("span", "w-box", "Aptos Narrow ▾"), h("span", "w-box w-size", "11 ▾"), btn("<b>B</b>", "Bold", () => say("Bold: not in today's steps.", true))));
      r.appendChild(group("Number", h("span", "w-box", "General ▾")));
      const cf = btn("<span class='w-big'>&#9638;</span>Conditional<br>Formatting ▾", "Conditional Formatting", () => { S.menu = S.menu === "cf" ? null : "cf"; draw(); }, "w-tall");
      r.appendChild(group("Styles", cf));
      const sum = btn("<b class='x-sigma'>&Sigma;</b> AutoSum", "AutoSum", autoSum);
      r.appendChild(group("Editing", sum, btn("Sort &amp; Filter ▾", "Sort & Filter", () => { S.menu = S.menu === "sf" ? null : "sf"; draw(); })));
      if (S.menu === "cf") {
        const m = h("div", "w-menu x-menu"); m.appendChild(h("b", "", "Highlight Cells Rules ›"));
        m.appendChild(btn("Greater Than...", "Greater Than", () => { S.menu = "gt"; draw(); }, "t-item"));
        m.appendChild(btn("Less Than...", "Less Than", () => say("Today: <b>Greater Than</b>.", true), "t-item"));
        m.appendChild(btn("Clear Rules", "Clear Rules", () => { S.cf = []; S.menu = null; say("The rules are cleared."); draw(); }, "t-item"));
        cf.parentElement.parentElement.appendChild(m);
      }
      if (S.menu === "gt") {
        const m = h("div", "w-menu x-dialog"); m.innerHTML = "<b>Greater Than</b><div>Format cells that are GREATER THAN:</div>";
        const inp = h("input", "x-in"); inp.value = ""; inp.setAttribute("aria-label", "the number"); m.appendChild(inp);
        m.appendChild(h("div", "", "with Light Red Fill with Dark Red Text"));
        m.appendChild(btn("OK", "OK", () => { const n = Number(inp.value); if (!inp.value || isNaN(n)) { say("Type a number, for example 20.", true); return; }
          const [r1, c1, r2, c2] = selRange(); S.cf.push({ r1, c1, r2, c2, gt: n }); S.menu = null; say(`The cells greater than <b>${n}</b> are red now. Change a number: the colour follows the rule.`); draw(); }, "x-ok"));
        cf.parentElement.parentElement.appendChild(m);
      }
      if (S.menu === "sf") {
        const m = h("div", "w-menu x-menu");
        m.appendChild(btn("Sort Smallest to Largest", "Sort Smallest to Largest", () => sortBy(false), "t-item"));
        m.appendChild(btn("Sort Largest to Smallest", "Sort Largest to Smallest", () => sortBy(true), "t-item"));
        m.appendChild(btn("Filter", "Filter", toggleFilter, "t-item"));
        sum.parentElement.parentElement.appendChild(m);
      }
    } else if (S.tab === "Data") {
      r.appendChild(group("Sort & Filter", btn("A&rarr;Z<br><small>Sort Smallest to Largest</small>", "Sort Smallest to Largest", () => sortBy(false), "w-tall"),
        btn("Z&rarr;A<br><small>Sort Largest to Smallest</small>", "Sort Largest to Smallest", () => sortBy(true), "w-tall"),
        btn("<span class='w-big'>&#9660;</span>Filter", "Filter", toggleFilter, "w-tall" + (S.filter ? " on" : "")),
        btn("Clear", "Clear", () => { if (S.filter) { S.filter.hide = []; say("<b>Clear</b>: all the rows are back."); draw(); } })));
    } else if (S.tab === "Insert") {
      const col = btn("<span class='w-big'>&#9601;&#9603;&#9605;</span>Column ▾", "Insert Column or Bar Chart", () => { S.menu = S.menu === "chart" ? null : "chart"; draw(); }, "w-tall");
      r.appendChild(group("Charts", btn("<span class='w-big'>&#9638;</span>Recommended<br>Charts", "Recommended Charts", () => makeChart("column"), "w-tall"), col,
        btn("<span class='w-big'>&#9684;</span>Pie ▾", "Pie", () => makeChart("pie"), "w-tall")));
      if (S.menu === "chart") { const m = h("div", "w-menu x-menu"); m.appendChild(h("b", "", "2-D Column"));
        m.appendChild(btn("Clustered Column", "Clustered Column", () => makeChart("column"), "t-item")); col.parentElement.parentElement.appendChild(m); }
    } else {
      r.appendChild(group("Function Library", h("span", "w-item", "AutoSum ▾"), h("span", "w-item", "Recently Used ▾")));
    }
  }

  // ---------- Commands ----------
  function autoSum() {
    const [r, c] = S.sel; let top = r - 1; while (top >= 0 && typeof val(ref(top, c)) === "number" && S.cells[ref(top, c)]) top--;
    if (top === r - 1) { say("Click the empty cell <b>under</b> the numbers first, then AutoSum.", true); return; }
    S.cells[ref(r, c)] = { raw: `=SUM(${ref(top + 1, c)}:${ref(r - 1, c)})` }; S.edit = null;
    say(`AutoSum wrote <b>=SUM(${ref(top + 1, c)}:${ref(r - 1, c)})</b>: the total of the cells above.`); draw();
  }
  function dataRows() { const last = lastRow(); const rows = []; for (let r = 1; r <= last; r++) rows.push(r); return rows; }
  function sortBy(desc) {
    S.menu = null; const c = S.sel[1]; const rows = dataRows();
    const recs = rows.map((r) => { const o = {}; for (let k = 0; k < NC; k++) { const cell = S.cells[ref(r, k)]; if (cell) o[k] = cell.raw; } return o; });
    const key = (o) => { const raw = o[c]; const n = Number(raw); return raw === undefined ? -Infinity : isNaN(n) ? raw : n; };
    recs.sort((a, b) => { const x = key(a), y = key(b); const d = typeof x === "number" && typeof y === "number" ? x - y : String(x).localeCompare(String(y)); return desc ? -d : d; });
    rows.forEach((r, i) => { for (let k = 0; k < NC; k++) { delete S.cells[ref(r, k)]; if (recs[i][k] !== undefined) S.cells[ref(r, k)] = { raw: recs[i][k] }; } });
    S.sorted = { col: c, desc }; say(`<b>Sort ${desc ? "Largest to Smallest" : "Smallest to Largest"}</b> by column <b>${L(c)}</b>: whole rows moved together.`); draw();
  }
  function toggleFilter() { S.menu = null; S.filter = S.filter ? null : { col: null, hide: [] };
    say(S.filter ? "<b>Filter</b>: an arrow in each heading. Click the arrow of a column." : "The filter is off: all rows are back."); draw(); }
  function makeChart(type) {
    S.menu = null; const [r1, c1, r2, c2] = selRange();
    if (r2 - r1 < 1 || c2 - c1 < 1) { say("First select the data with its headings: drag from the first heading to the last number.", true); return; }
    S.chart = { type, r1, c1, r2, c2, title: "Chart Title" }; say(`A ${type === "pie" ? "pie" : "column"} chart of the selected cells. Click <b>Chart Title</b> and type a real title.`); draw();
  }

  // ---------- The grid ----------
  function grid() {
    const wrap = $(".x-gridwrap", root); wrap.innerHTML = "";
    const t = h("table", "x-grid"); const head = h("tr"); head.appendChild(h("th", "x-corner", ""));
    for (let c = 0; c < NC; c++) head.appendChild(h("th", S.sel[1] === c ? "on" : "", L(c))); t.appendChild(head);
    const [r1, c1, r2, c2] = selRange();
    for (let r = 0; r < NR; r++) {
      if (S.filter && S.filter.hide.includes(r)) continue;
      const tr = h("tr"); tr.appendChild(h("th", S.sel[0] === r ? "on" : "", String(r + 1)));
      for (let c = 0; c < NC; c++) {
        const rf = ref(r, c); const td = h("td", "");
        const inSel = r >= r1 && r <= r2 && c >= c1 && c <= c2; if (inSel) td.classList.add("in");
        if (S.sel[0] === r && S.sel[1] === c) td.classList.add("cur");
        const v = val(rf);
        S.cf.forEach((rule) => { if (r >= rule.r1 && r <= rule.r2 && c >= rule.c1 && c <= rule.c2 && typeof v === "number" && v > rule.gt) td.classList.add("x-red"); });
        if (S.edit && S.edit[0] === r && S.edit[1] === c) {
          const inp = h("input", "x-in"); inp.value = S.edit.text; td.appendChild(inp);
          inp.addEventListener("input", () => { S.edit.text = inp.value; $(".x-f", root).textContent = inp.value; });
          inp.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === "Tab") { e.preventDefault(); commit(e.key === "Tab" ? [0, 1] : [1, 0]); } if (e.key === "Escape") { S.edit = null; draw(); } });
          inp.addEventListener("click", (e) => e.stopPropagation());
        } else {
          td.textContent = show(rf); if (typeof v === "number") td.classList.add("num");
          if (r === 0 && S.filter && S.cells[rf]) { const a = btn("&#9662;", "Filter " + L(c), () => filterMenu(c), "x-arrow"); td.appendChild(a); }
          if (S.sel[0] === r && S.sel[1] === c && !S.end) { const fh = h("span", "x-fh"); fh.title = "Fill handle: double-click to copy down";
            fh.addEventListener("dblclick", (e) => { e.stopPropagation(); fillDown(); }); td.appendChild(fh); }
        }
        td.addEventListener("mousedown", (e) => { if (e.target.closest(".x-arrow,.x-fh,input")) return;
          if (S.edit) commit(null); if (e.shiftKey) S.end = [r, c]; else { S.sel = [r, c]; S.end = null; S.drag = true; } S.menu = S.menu === "gt" ? "gt" : null; draw(); });
        td.addEventListener("mouseenter", () => { if (S.drag && (S.sel[0] !== r || S.sel[1] !== c)) { S.end = [r, c]; draw(); } });
        td.addEventListener("dblclick", () => startEdit(r, c, S.cells[rf] ? S.cells[rf].raw : ""));
        tr.appendChild(td);
      }
      t.appendChild(tr);
    }
    wrap.appendChild(t);
    if (S.filter && S.filter.col !== null && S.filter.open) wrap.appendChild(filterBox());
    const cur = ref(S.sel[0], S.sel[1]);
    $(".x-name", root).textContent = S.end ? `${ref(r1, c1)}:${ref(r2, c2)}` : cur;
    $(".x-f", root).textContent = S.edit ? S.edit.text : (S.cells[cur] ? S.cells[cur].raw : "");
    const nums = []; for (let r = r1; r <= r2; r++) for (let c = c1; c <= c2; c++) { const v = val(ref(r, c)); if (typeof v === "number" && S.cells[ref(r, c)]) nums.push(v); }
    $(".x-sum", root).textContent = nums.length > 1 ? `Sum: ${nums.reduce((a, b) => a + b, 0)}   Count: ${nums.length}` : "";
  }
  document.addEventListener("mouseup", () => { S.drag = false; });
  function startEdit(r, c, text) { S.sel = [r, c]; S.end = null; S.edit = [r, c]; S.edit.text = text; draw(); }
  function commit(move) {
    const [r, c] = S.edit; const text = S.edit.text.trim();
    if (text) S.cells[ref(r, c)] = { raw: text }; else delete S.cells[ref(r, c)];
    S.edit = null;
    if (text[0] === "=") { const v = val(ref(r, c)); say(typeof v === "number" ? `<b>${text}</b> gives <b>${v}</b>. Change a number that it uses: the result changes by itself.` : `<b>${text}</b>: ${v}. Check the spelling of the formula.`, typeof v !== "number"); }
    if (move) S.sel = [Math.min(NR - 1, r + move[0]), Math.min(NC - 1, c + move[1])];
    draw();
  }
  function fillDown() {
    const [r, c] = S.sel; const src = S.cells[ref(r, c)]; if (!src) return;
    let last = r; const neighbour = c > 0 ? c - 1 : c + 1;
    while (last + 1 < NR && S.cells[ref(last + 1, neighbour)]) last++;
    if (last === r) { say("The fill handle copies down as far as the column next to it has data.", true); return; }
    for (let k = r + 1; k <= last; k++) S.cells[ref(k, c)] = { raw: src.raw[0] === "=" ? shift(src.raw, k - r, 0) : src.raw };
    say(`The formula is copied down to row ${last + 1}. Click ${ref(r + 1, c)}: the references moved one row (${S.cells[ref(r + 1, c)].raw}).`); draw();
  }
  function filterMenu(c) { S.filter.col = c; S.filter.open = true; draw(); }
  function filterBox() {
    const c = S.filter.col; const m = h("div", "w-menu x-filter"); m.appendChild(h("b", "", `Filter: ${show(ref(0, c))}`));
    const vals = [...new Set(dataRows().map((r) => show(ref(r, c))).filter(Boolean))];
    const hidden = new Set(S.filter.hide.map((r) => show(ref(r, c))));
    const boxes = vals.map((v) => { const l = h("label", "x-cb"); const cb = h("input"); cb.type = "checkbox"; cb.checked = !hidden.has(v); l.appendChild(cb); l.appendChild(document.createTextNode(" " + v)); m.appendChild(l); return [v, cb]; });
    m.appendChild(btn("OK", "OK", () => { const keep = new Set(boxes.filter(([, cb]) => cb.checked).map(([v]) => v));
      S.filter.hide = dataRows().filter((r) => !keep.has(show(ref(r, c)))); S.filter.open = false; S.filter.last = [...keep];
      say(`Only the rows of <b>${[...keep].join(", ")}</b> are shown. The other rows are hidden, not deleted.`); draw(); }, "x-ok"));
    return m;
  }
  function chart() {
    const w = $(".x-chartwrap", root); w.innerHTML = ""; if (!S.chart) return;
    const ch = S.chart; const labels = [], vals = [];
    for (let r = ch.r1 + 1; r <= ch.r2; r++) { labels.push(show(ref(r, ch.c1))); const v = val(ref(r, ch.c2)); vals.push(typeof v === "number" ? v : 0); }
    const box = h("div", "x-chart");
    const title = h("div", "x-ctitle", ch.title); box.appendChild(title);
    title.addEventListener("click", () => { const inp = h("input", "x-in"); inp.value = ch.title === "Chart Title" ? "" : ch.title; title.replaceWith(inp); inp.focus();
      const done = () => { ch.title = inp.value.trim() || "Chart Title"; say(ch.title === "Chart Title" ? "Type a real title." : `The chart has a title: <b>${ch.title}</b>.`, ch.title === "Chart Title"); draw(); };
      inp.addEventListener("keydown", (e) => { if (e.key === "Enter") done(); }); inp.addEventListener("blur", done); });
    const max = Math.max(...vals, 1); const COLS = ["#4472c4", "#ed7d31", "#a5a5a5", "#ffc000", "#5b9bd5", "#70ad47"];
    let svg = `<svg viewBox="0 0 320 170" class="x-svg">`;
    if (ch.type === "pie") { let a0 = -Math.PI / 2; const sum = vals.reduce((a, b) => a + b, 0) || 1;
      vals.forEach((v, i) => { const a1 = a0 + (v / sum) * Math.PI * 2; const big = a1 - a0 > Math.PI ? 1 : 0;
        svg += `<path d="M110 85 L${110 + 70 * Math.cos(a0)} ${85 + 70 * Math.sin(a0)} A70 70 0 ${big} 1 ${110 + 70 * Math.cos(a1)} ${85 + 70 * Math.sin(a1)} Z" fill="${COLS[i % 6]}"/>`;
        svg += `<rect x="200" y="${20 + i * 18}" width="10" height="10" fill="${COLS[i % 6]}"/><text x="215" y="${29 + i * 18}" font-size="10">${labels[i]}</text>`; a0 = a1; });
    } else { const bw = 260 / vals.length;
      vals.forEach((v, i) => { const hh = (v / max) * 120; svg += `<rect x="${40 + i * bw + bw * 0.2}" y="${140 - hh}" width="${bw * 0.6}" height="${hh}" fill="#4472c4"/>`;
        svg += `<text x="${40 + i * bw + bw / 2}" y="155" font-size="9" text-anchor="middle">${labels[i]}</text>`; });
      svg += `<line x1="38" y1="140" x2="305" y2="140" stroke="#999"/><text x="34" y="24" font-size="9" text-anchor="end">${max}</text><text x="34" y="143" font-size="9" text-anchor="end">0</text>`; }
    svg += "</svg>"; box.insertAdjacentHTML("beforeend", svg); w.appendChild(box);
  }
  document.addEventListener("keydown", (e) => {
    if (S.edit || S.menu === "gt" || e.target.tagName === "INPUT" || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key.length === 1) { e.preventDefault(); startEdit(S.sel[0], S.sel[1], e.key); setTimeout(() => { const i = $(".x-grid input", root); if (i) { i.focus(); i.setSelectionRange(i.value.length, i.value.length); } }, 0); }
    else if (e.key === "Delete" || e.key === "Backspace") { delete S.cells[ref(S.sel[0], S.sel[1])]; draw(); }
    else if (e.key.startsWith("Arrow")) { const d = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] }[e.key]; e.preventDefault();
      S.sel = [Math.max(0, Math.min(NR - 1, S.sel[0] + d[0])), Math.max(0, Math.min(NC - 1, S.sel[1] + d[1]))]; S.end = null; draw(); }
  });

  // ---------- The steps ----------
  const X = { v: (rf) => val(rf), f: (rf) => (S.cells[rf] ? S.cells[rf].raw : ""), get cf() { return S.cf; }, get chart() { return S.chart; }, get filter() { return S.filter; },
    get sorted() { return S.sorted; }, rows: () => dataRows(), col: (c) => dataRows().map((r) => val(ref(r, c))) };
  function status() {
    const list = $("#jobs"); list.innerHTML = ""; let done = 0;
    C.missions.forEach(([t, f]) => { let ok = false; try { ok = !!f(X); } catch (e) { ok = false; } done += ok; const li = h("li", ok ? "ok" : ""); li.innerHTML = t; list.appendChild(li); });
    $("#progress").textContent = `${done} of ${C.missions.length}`;
    if (done === C.missions.length && !status.done) { status.done = true; say(C.done || "&#10003; All steps done. The same steps are in your worksheet: now do them in Excel."); }
  }
  function draw() {
    tabs(); ribbon(); grid(); chart(); status();
    const i = $(".x-grid input", root) || $(".x-dialog input", root); if (i && document.activeElement !== i) { i.focus(); i.setSelectionRange(i.value.length, i.value.length); }
  }
  document.addEventListener("click", (e) => { if (S.menu && S.menu !== "gt" && !e.target.closest(".w-menu")) { S.menu = null; draw(); } });
  $("#reset").addEventListener("click", () => { reset(); status.done = false; say(C.hello); draw(); });
  reset(); say(C.hello); draw();
})();
