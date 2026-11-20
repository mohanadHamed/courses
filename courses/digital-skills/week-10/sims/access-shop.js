// Access Shop: a simulator that looks like Access for Windows, with the
// Products table of the Sunrise shop (shop-db.js, window.SHOP), for Online
// activity 9. One engine, three parts, chosen by the page (window.ACCESS_SHOP):
//   form:   Create › Form, the record arrows, a new record and Save;
//   query:  Create › Query Design, the fields, a criterion, a sort, Run;
//   report: Create › Report, Group & Sort (a group), Totals (Sum of Price).
// The students also use these simulators for the tasks (Access is only on
// Windows), so every step works with any data, not only the one of the steps.
(() => {
  const PART = window.ACCESS_SHOP || "form";
  const $ = (s, el = document) => el.querySelector(s);
  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
  const btn = (html, title, fn, cls = "") => { const b = h("button", "w-btn " + cls); b.type = "button"; b.innerHTML = html; b.title = title; b.setAttribute("aria-label", title);
    b.addEventListener("click", (e) => { e.stopPropagation(); fn(e); }); return b; };
  const say = (text, bad) => { const m = $("#msg"); m.innerHTML = text; m.className = "message" + (bad ? " bad" : ""); };
  const F = window.SHOP.fields;
  const money = (v) => (typeof v === "number" ? v.toFixed(2) : v);
  const cell = (f, v) => String(f === "Price" ? money(v) : v);
  let S;
  function reset() {
    S = { tab: "Home", view: "none", picked: false, rows: window.SHOP.rows.map((r) => [...r]), rec: 0, draft: null, seen: new Set([0]), saved: 0,
      form: false, report: false, q: { fields: [], crit: {}, sort: {}, ran: false }, rep: { group: null, sum: false, pane: false }, menu: null };
  }
  const root = $("#access"); root.className = "word access";
  root.innerHTML = `<div class="w-title"><span class="w-auto">AutoSave <i></i> Off</span><b>shop : Database - Access</b><span class="w-search">Search</span><span class="w-win">&#8211; &#9633; &#10005;</span></div>
    <div class="w-tabs"></div><div class="w-ribbon"></div>
    <div class="w-body"><div class="a-nav"></div><div class="a-main"></div></div><div class="w-status"><span class="a-view"></span></div>`;
  const group = (label, ...items) => { const g = h("div", "w-group"); const row = h("div", "w-row"); items.forEach((i) => row.appendChild(i)); g.appendChild(row); g.appendChild(h("small", "", label)); return g; };
  const TABS = () => ["File", "Home", "Create", "External Data", "Database Tools", "Help"].concat(S.view === "report" ? ["Report Layout Design"] : []);
  function tabs() {
    const bar = $(".w-tabs", root); bar.innerHTML = "";
    TABS().forEach((t) => bar.appendChild(btn(t, t, () => { if (["Home", "Create", "Report Layout Design"].includes(t)) { S.tab = t; S.menu = null; draw(); } else say(`<b>${t}</b>: not needed here.`, true); },
      "w-tab" + (t === S.tab ? " on" : "") + (t === "Report Layout Design" ? " a-ctx" : ""))));
  }
  function ribbon() {
    const r = $(".w-ribbon", root); r.innerHTML = "";
    if (S.tab === "Home") {
      r.appendChild(group("Views", btn("<span class='w-big'>&#9638;</span>View ▾", "View", () => say("View: not needed here.", true), "w-tall")));
      if (S.view === "query") r.appendChild(group("Results", btn("<span class='w-big a-run'>!</span>Run", "Run", run, "w-tall")));
      if (S.view === "form") r.appendChild(group("Records", btn("<span class='w-big'>&#128190;</span>Save", "Save", () => { if (!saveDraft()) say("Nothing new to save. For a new record: the button <b>▶*</b> at the bottom.", true); draw(); }, "w-tall")));
    } else if (S.tab === "Create") {
      r.appendChild(group("Queries", btn("<span class='w-big'>&#9998;</span>Query<br>Design", "Query Design", () => { if (PART !== "query") { say("Today: the <b>" + PART + "</b>.", true); return; }
        S.view = "query"; S.tab = "Home"; say("<b>Query Design</b>: double-click the fields that you want to see."); draw(); }, "w-tall")));
      r.appendChild(group("Forms", btn("<span class='w-big'>&#9636;</span>Form", "Form", () => create("form"), "w-tall")));
      r.appendChild(group("Reports", btn("<span class='w-big'>&#9636;</span>Report", "Report", () => create("report"), "w-tall")));
    } else if (S.tab === "Report Layout Design") {
      const tot = btn("<span class='w-big'>&Sigma;</span>Totals ▾", "Totals", () => { S.menu = S.menu === "tot" ? null : "tot"; draw(); }, "w-tall");
      r.appendChild(group("Grouping & Totals", btn("<span class='w-big'>&#9776;</span>Group<br>&amp; Sort", "Group & Sort", () => { S.rep.pane = !S.rep.pane; S.menu = null;
        say(S.rep.pane ? "The pane <b>Group, Sort, and Total</b> is open under the report: click <b>Add a group</b>." : "The pane is closed."); draw(); }, "w-tall"), tot));
      if (S.menu === "tot") { const m = h("div", "w-menu x-menu");
        m.appendChild(btn("Sum (of Price)", "Sum", () => { S.rep.sum = true; S.menu = null; say("<b>Totals › Sum</b>: the total of the prices" + (S.rep.group ? " of each group, and of the whole report." : " of the whole report.")); draw(); }, "t-item"));
        m.appendChild(btn("Count Records", "Count Records", () => { S.menu = null; say("Today: <b>Sum</b>, the total of the prices.", true); draw(); }, "t-item"));
        tot.parentElement.parentElement.appendChild(m); }
    }
  }
  function create(kind) {
    if (PART !== kind) { say("Today: the <b>" + PART + "</b>.", true); return; }
    if (!S.picked) { say("First click the table <b>Products</b> on the left, then <b>Create › " + (kind === "form" ? "Form" : "Report") + "</b>.", true); return; }
    S[kind] = true; S.view = kind; S.tab = kind === "report" ? "Report Layout Design" : "Home";
    say(kind === "form" ? "A <b>form</b> for Products: one record at a time. The arrows at the bottom go to the next record."
      : "A <b>report</b> of Products, ready to print. Now <b>Group &amp; Sort</b>, then <b>Totals</b>.");
    draw();
  }
  // ---------- Form ----------
  function saveDraft() {
    if (!S.draft) return false;
    if (!String(S.draft.Name || "").trim()) { S.draft = null; return false; }
    const id = Math.max(...S.rows.map((r) => r[0])) + 1;
    const price = Number(String(S.draft.Price || "0").replace(",", "."));
    S.rows.push([id, S.draft.Name.trim(), (S.draft.Type || "").trim(), isNaN(price) ? 0 : price, S.draft.InStock || "Yes"]);
    S.draft = null; S.rec = S.rows.length - 1; S.saved++; S.seen.add(S.rec);
    say(`Record ${S.rows.length} is saved: <b>${S.rows[S.rec][1]}</b> is in the table <b>Products</b> now. The table has <b>${S.rows.length}</b> records.`);
    return true;
  }
  function go(i) { saveDraft(); S.rec = Math.max(0, Math.min(S.rows.length - 1, i)); S.seen.add(S.rec); draw(); }
  function form(m) {
    const card = h("div", "a-form"); card.appendChild(h("div", "a-fhead", "Products"));
    const rec = S.draft ? null : S.rows[S.rec];
    F.forEach((f, k) => { const row = h("label", "a-frow"); row.appendChild(h("span", "", f));
      let inp;
      if (f === "InStock") { inp = h("select", "a-box"); ["Yes", "No"].forEach((x) => { const o = h("option", "", x); if ((rec ? rec[k] : S.draft.InStock || "Yes") === x) o.selected = true; inp.appendChild(o); }); }
      else { inp = h("input", "a-box"); inp.value = rec ? (f === "Price" ? money(rec[k]) : rec[k]) : (f === "ProductID" ? "(New)" : S.draft[f] || ""); }
      inp.disabled = f === "ProductID"; inp.setAttribute("aria-label", f);
      inp.addEventListener("change", () => { if (S.draft) S.draft[f] = inp.value; else { const v = f === "Price" ? Number(inp.value) : inp.value; if (!(f === "Price" && isNaN(v))) S.rows[S.rec][k] = v; } });
      row.appendChild(inp); card.appendChild(row); });
    m.appendChild(card);
    const nav = h("div", "a-recnav"); nav.appendChild(h("span", "", "Record:"));
    nav.appendChild(btn("|◀", "First record", () => go(0))); nav.appendChild(btn("◀", "Previous record", () => go(S.rec - 1)));
    nav.appendChild(h("b", "", S.draft ? `${S.rows.length + 1} of ${S.rows.length + 1}` : `${S.rec + 1} of ${S.rows.length}`));
    nav.appendChild(btn("▶", "Next record", () => go(S.rec + 1))); nav.appendChild(btn("▶|", "Last record", () => go(S.rows.length - 1)));
    nav.appendChild(btn("▶*", "New (blank) record", () => { saveDraft(); S.draft = { InStock: "Yes" }; say("A <b>new, blank record</b>. Type the name, the type and the price, then <b>Save</b> (Home)."); draw(); const i = root.querySelector('.a-form input[aria-label="Name"]'); if (i) i.focus(); }, "a-new"));
    m.appendChild(nav);
  }
  // ---------- Query ----------
  const match = (v, c) => { c = String(c || "").trim().replace(/"/g, ""); if (!c) return true;
    const m = /^(>=|<=|<>|>|<|=)?\s*(.+)$/.exec(c); const op = m[1] || "="; const want = m[2];
    const n = Number(want); const isNum = typeof v === "number" && !isNaN(n);
    const a = isNum ? v : String(v).toLowerCase(), b = isNum ? n : want.toLowerCase();
    return { "=": a === b, "<>": a !== b, ">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b }[op]; };
  function queryRows() {
    let rows = S.rows.filter((r) => Object.entries(S.q.crit).every(([f, c]) => match(r[F.indexOf(f)], c)));
    Object.entries(S.q.sort).forEach(([f, d]) => { if (!d) return; const k = F.indexOf(f);
      rows = [...rows].sort((a, b) => (d === "Ascending" ? 1 : -1) * (typeof a[k] === "number" ? a[k] - b[k] : String(a[k]).localeCompare(String(b[k])))); });
    return rows;
  }
  function run() {
    if (!S.q.fields.length) { say("First double-click the fields that you want to see.", true); return; }
    S.q.ran = true; S.view = "result"; const n = queryRows().length;
    say(`<b>Run</b>: <b>${n}</b> record${n === 1 ? "" : "s"}: only the records that match the criteria, in the order of the sort.`); draw();
  }
  function query(m) {
    const box = h("div", "a-tbl"); box.appendChild(h("b", "", "Products"));
    ["*", ...F].forEach((f) => { const d = h("div", "a-fld" + (S.q.fields.includes(f) ? " on" : ""), f);
      d.addEventListener("dblclick", () => { if (f === "*" || S.q.fields.includes(f) || S.q.fields.length >= 5) return; S.q.fields.push(f); say(`<b>${f}</b> is in the grid: a column of the result.`); draw(); });
      d.addEventListener("click", () => say("Double-click a field to add it to the grid.")); box.appendChild(d); });
    m.appendChild(box);
    const g = h("table", "a-grid q");
    [["Field:", (f) => f], ["Table:", () => "Products"], ["Sort:", null], ["Show:", () => "☑"], ["Criteria:", "crit"]].forEach(([lab, fn]) => {
      const tr = h("tr"); tr.appendChild(h("th", "", lab));
      for (let k = 0; k < Math.max(4, S.q.fields.length); k++) { const f = S.q.fields[k]; const td = h("td");
        if (f && fn === "crit") { const i = h("input", "a-in"); i.value = S.q.crit[f] || ""; i.setAttribute("aria-label", "Criteria " + f);
          i.addEventListener("change", () => { S.q.crit[f] = i.value.trim(); say(S.q.crit[f] ? `Criterion of <b>${f}</b>: <b>${S.q.crit[f]}</b>.` : `No criterion for ${f}.`); draw(); }); td.appendChild(i); }
        else if (f && fn === null) { const sel = h("select", "a-in"); sel.setAttribute("aria-label", "Sort " + f); ["", "Ascending", "Descending"].forEach((x) => { const o = h("option", "", x); if ((S.q.sort[f] || "") === x) o.selected = true; sel.appendChild(o); });
          sel.addEventListener("change", () => { S.q.sort = { [f]: sel.value }; say(`Sort by <b>${f}</b>: <b>${sel.value || "(not sorted)"}</b>. ${sel.value === "Ascending" ? "A to Z, small to big." : sel.value ? "Z to A, big to small." : ""}`); draw(); }); td.appendChild(sel); }
        else if (f) td.textContent = fn(f);
        tr.appendChild(td); }
      g.appendChild(tr); });
    m.appendChild(g);
  }
  function result(m) {
    const t = h("table", "a-grid ds"); const hr = h("tr"); S.q.fields.forEach((f) => hr.appendChild(h("th", "", f))); t.appendChild(hr);
    queryRows().forEach((r) => { const tr = h("tr"); S.q.fields.forEach((f) => tr.appendChild(h("td", "", cell(f, r[F.indexOf(f)])))); t.appendChild(tr); });
    m.appendChild(t); m.appendChild(btn("Back to Design View", "Design View", () => { S.view = "query"; draw(); }, "ghost"));
  }
  // ---------- Report ----------
  function report(m) {
    const p = h("div", "a-report"); p.appendChild(h("div", "a-rtitle", "Products"));
    const t = h("table", "a-rtable"); const cols = F.filter((f) => f !== S.rep.group);
    const hr = h("tr"); if (S.rep.group) hr.appendChild(h("th", "", S.rep.group)); cols.forEach((f) => hr.appendChild(h("th", "", f))); t.appendChild(hr);
    const P = F.indexOf("Price"); const line = (r) => { const tr = h("tr"); if (S.rep.group) tr.appendChild(h("td", "", "")); cols.forEach((f) => tr.appendChild(h("td", f === "Price" ? "num" : "", cell(f, r[F.indexOf(f)])))); return tr; };
    const pIdx = (S.rep.group ? 1 : 0) + cols.indexOf("Price");
    const sumRow = (label, v, cls) => { const tr = h("tr", cls); for (let i = 0; i < hr.children.length; i++) tr.appendChild(h("td", i === pIdx ? "num" : "", i === 0 ? label : i === pIdx ? v.toFixed(2) : "")); return tr; };
    if (S.rep.group) {
      const k = F.indexOf(S.rep.group); [...new Set(S.rows.map((r) => r[k]))].sort().forEach((g) => {
        const gr = h("tr", "a-ghead"); const td = h("td", "", String(g)); td.colSpan = hr.children.length; gr.appendChild(td); t.appendChild(gr);
        const rs = S.rows.filter((r) => r[k] === g); rs.forEach((r) => t.appendChild(line(r)));
        if (S.rep.sum) t.appendChild(sumRow("Total " + g, rs.reduce((s, r) => s + r[P], 0), "a-gsum")); });
    } else S.rows.forEach((r) => t.appendChild(line(r)));
    if (S.rep.sum) t.appendChild(sumRow("Grand Total", S.rows.reduce((s, r) => s + r[P], 0), "a-gtot"));
    p.appendChild(t); m.appendChild(p);
    if (S.rep.pane) { const pane = h("div", "a-gpane"); pane.appendChild(h("b", "", "Group, Sort, and Total"));
      if (S.rep.group) pane.appendChild(h("div", "", `Group on ${S.rep.group} ▾ with A on top`));
      const add = btn("[≡] Add a group", "Add a group", () => { S.menu = S.menu === "grp" ? null : "grp"; draw(); }, "a-add"); pane.appendChild(add);
      if (S.menu === "grp") { const mm = h("div", "w-menu x-menu a-gmenu"); mm.appendChild(h("b", "", "select field"));
        ["Name", "Type", "InStock"].forEach((f) => mm.appendChild(btn(f, f, () => { S.rep.group = f; S.menu = null; say(`<b>Group on ${f}</b>: the records of each ${f.toLowerCase()} stand together, under a heading.`); draw(); }, "t-item")));
        pane.appendChild(mm); }
      m.appendChild(pane); }
  }
  function nav() {
    const n = $(".a-nav", root); n.innerHTML = "<b>All Access Objects</b><small>Tables</small>";
    const t = h("div", "a-obj" + (S.picked ? " on" : ""), "▦ Products"); t.style.cursor = "pointer";
    t.addEventListener("click", () => { S.picked = true; if (S.view === "none") say("The table <b>Products</b> is selected. Now the tab <b>Create</b>."); draw(); }); n.appendChild(t);
    if (S.q.ran) { n.appendChild(h("small", "", "Queries")); n.appendChild(h("div", "a-obj", "▤ Query1")); }
    if (S.form) { n.appendChild(h("small", "", "Forms")); n.appendChild(h("div", "a-obj", "▤ Products")); }
    if (S.report) { n.appendChild(h("small", "", "Reports")); n.appendChild(h("div", "a-obj", "▤ Products")); }
  }
  function main() {
    const m = $(".a-main", root); m.innerHTML = "";
    $(".a-view", root).textContent = { none: "Ready", form: "Form View", query: "Query Design", result: "Datasheet View", report: "Layout View" }[S.view];
    if (S.view === "form") form(m); else if (S.view === "query") query(m); else if (S.view === "result") result(m); else if (S.view === "report") report(m);
    else m.appendChild(h("p", "a-empty", "No object is open."));
  }
  const MISSIONS = {
    form: [
      ["Click <b>Products</b> (left), then <b>Create › Form</b>", () => S.form],
      ["The arrows at the bottom: go to record 3, <b>Bag</b>", () => S.form && S.seen.has(2)],
      ["<b>▶*</b> (New record): <b>Ruler</b>, Paper, 1, Yes; then <b>Home › Save</b>", () => S.rows.some((r) => /ruler/i.test(r[1]))],
    ],
    query: [
      ["<b>Create › Query Design</b>; double-click <b>Name</b>, <b>Type</b> and <b>Price</b>", () => ["Name", "Type", "Price"].every((f) => S.q.fields.includes(f))],
      ["<b>Criteria</b> under Type: <b>Drinks</b>; <b>Sort</b> under Price: <b>Ascending</b>", () => /drinks/i.test(S.q.crit.Type || "") && S.q.sort.Price === "Ascending"],
      ["<b>Run</b> (the red !): 3 drinks, the cheapest first", () => S.q.ran && /drinks/i.test(S.q.crit.Type || "")],
    ],
    report: [
      ["Click <b>Products</b> (left), then <b>Create › Report</b>", () => S.report],
      ["<b>Group &amp; Sort › Add a group › Type</b>", () => S.rep.group === "Type"],
      ["<b>Totals › Sum</b>: the total of each type", () => S.rep.group && S.rep.sum],
    ],
  }[PART];
  function status() {
    const list = $("#jobs"); list.innerHTML = ""; let done = 0;
    MISSIONS.forEach(([t, f]) => { const ok = !!f(); done += ok; const li = h("li", ok ? "ok" : ""); li.innerHTML = t; list.appendChild(li); });
    $("#progress").textContent = `${done} of ${MISSIONS.length}`;
    if (done === MISSIONS.length && !status.done) { status.done = true; say(window.SIM_DONE || "&#10003; All steps done. The tasks use this simulator too: click <b>Start again</b> first."); }
  }
  function draw() { tabs(); ribbon(); nav(); main(); status(); }
  document.addEventListener("click", (e) => { if (S.menu && !e.target.closest(".w-menu")) { S.menu = null; draw(); } });
  const HELLO = { form: "Click the table <b>Products</b> on the left, then the tab <b>Create</b>.", query: "Click the tab <b>Create</b>, then <b>Query Design</b>.",
    report: "Click the table <b>Products</b> on the left, then the tab <b>Create</b>." }[PART];
  $("#reset").addEventListener("click", () => { reset(); status.done = false; say(HELLO); draw(); });
  reset(); say(HELLO); draw();
})();
