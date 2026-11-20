// Access Lab: a simulator that looks like Access for Windows, with the
// Customers table of the Lecture 8 worksheet. One engine, three parts, chosen
// by the page that loads it (window.ACCESS_LAB):
//   table: Design View (field names and data types), then Datasheet View (records);
//   key:   the primary key, and a relationship from Customers to Orders;
//   query: Create › Query Design, the fields, a criterion, a sort, Run.
(() => {
  const PART = window.ACCESS_LAB || "table";
  const $ = (s, el = document) => el.querySelector(s);
  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
  const btn = (html, title, fn, cls = "") => { const b = h("button", "w-btn " + cls); b.type = "button"; b.innerHTML = html; b.title = title; b.setAttribute("aria-label", title);
    b.addEventListener("click", (e) => { e.stopPropagation(); fn(e); }); return b; };
  const say = (text, bad) => { const m = $("#msg"); m.innerHTML = text; m.className = "message" + (bad ? " bad" : ""); };
  const TYPES = ["Short Text", "Long Text", "Number", "Date/Time", "Currency", "AutoNumber", "Yes/No"];
  const CUST = [{ ID: 1, Name: "Huda", City: "Amman" }, { ID: 2, Name: "Omar", City: "Irbid" }, { ID: 3, Name: "Rana", City: "Amman" }];
  let S;
  function reset() {
    S = { view: PART === "query" ? "query" : PART === "key" ? "design" : "design", tab: "Home",
      fields: PART === "table" ? [{ name: "ID", type: "AutoNumber", key: true }, { name: "", type: "Short Text" }] : [{ name: "ID", type: "AutoNumber", key: PART !== "key" }, { name: "Name", type: "Short Text" }, { name: "City", type: "Short Text" }],
      rows: PART === "table" ? [] : CUST.map((r) => ({ ...r })), sel: null, rel: null, pick: null, rels: false,
      q: { fields: [], crit: {}, sort: {}, ran: false } };
  }
  const root = $("#access"); root.className = "word access";
  root.innerHTML = `<div class="w-title"><span class="w-auto">AutoSave <i></i> Off</span><b>shop-Huda : Database - Access</b><span class="w-search">Search</span><span class="w-win">&#8211; &#9633; &#10005;</span></div>
    <div class="w-tabs"></div><div class="w-ribbon"></div>
    <div class="w-body"><div class="a-nav"></div><div class="a-main"></div></div><div class="w-status"><span class="a-view"></span></div>`;
  const TABS = ["File", "Home", "Create", "External Data", "Database Tools", "Help"];
  const group = (label, ...items) => { const g = h("div", "w-group"); const row = h("div", "w-row"); items.forEach((i) => row.appendChild(i)); g.appendChild(row); g.appendChild(h("small", "", label)); return g; };
  function tabs() {
    const bar = $(".w-tabs", root); bar.innerHTML = "";
    TABS.forEach((t) => bar.appendChild(btn(t, t, () => { if (["Home", "Create", "Database Tools"].includes(t)) { S.tab = t; draw(); } else say(`<b>${t}</b>: not needed here.`, true); }, "w-tab" + (t === S.tab ? " on" : ""))));
  }
  function ribbon() {
    const r = $(".w-ribbon", root); r.innerHTML = "";
    if (S.tab === "Home") {
      r.appendChild(group("Views", btn("<span class='w-big'>&#9638;</span>View ▾", "View", () => { S.menu = !S.menu; draw(); }, "w-tall")));
      if (S.view === "design") r.appendChild(group("Tools", btn("<span class='w-big'>&#128273;</span>Primary<br>Key", "Primary Key", primaryKey, "w-tall")));
      if (S.view === "query") r.appendChild(group("Results", btn("<span class='w-big a-run'>!</span>Run", "Run", run, "w-tall")));
      if (S.menu) { const m = h("div", "w-menu x-menu");
        [["Datasheet View", "datasheet"], ["Design View", "design"]].forEach(([n, v]) => m.appendChild(btn(n, n, () => { S.menu = false; setView(v); }, "t-item")));
        r.firstChild.appendChild(m); }
    } else if (S.tab === "Create") {
      r.appendChild(group("Tables", btn("<span class='w-big'>&#9638;</span>Table", "Table", () => say("A new table: not in today's steps.", true), "w-tall")));
      r.appendChild(group("Queries", btn("<span class='w-big'>&#9638;</span>Query<br>Wizard", "Query Wizard", () => say("Today: <b>Query Design</b>.", true), "w-tall"),
        btn("<span class='w-big'>&#9998;</span>Query<br>Design", "Query Design", () => { S.view = "query"; S.tab = "Home"; say("<b>Query Design</b>: double-click the fields that you want to see."); draw(); }, "w-tall")));
    } else {
      r.appendChild(group("Relationships", btn("<span class='w-big'>&#8644;</span>Relationships", "Relationships", () => { S.view = "rel"; say("The <b>Relationships</b> window. Click <b>ID</b> in Customers, then <b>CustomerID</b> in Orders."); draw(); }, "w-tall")));
    }
  }
  function setView(v) {
    if (v === "datasheet") { const bad = S.fields.filter((f) => f.name).length < 3; if (PART === "table" && bad) { say("First add the fields <b>Name</b> and <b>City</b> (Short Text) in Design View.", true); return; } }
    S.view = v; say(v === "datasheet" ? "<b>Datasheet View</b>: the records. Type one customer in each row; ID counts by itself (AutoNumber)." : "<b>Design View</b>: the fields and their data types."); draw();
  }
  function primaryKey() {
    if (S.sel === null) { say("First click the row of the field <b>ID</b>.", true); return; }
    S.fields.forEach((f, i) => { f.key = i === S.sel; }); say(`<b>${S.fields[S.sel].name}</b> is the primary key: one value for each record, never the same twice.`, S.fields[S.sel].name !== "ID"); draw();
  }
  function run() {
    if (!S.q.fields.length) { say("First double-click the fields <b>Name</b> and <b>City</b>.", true); return; }
    S.q.ran = true; S.view = "result"; say("<b>Run</b>: only the records that match the criterion, in the order of the sort."); draw();
  }
  function nav() {
    const n = $(".a-nav", root); n.innerHTML = "<b>All Access Objects</b><small>Tables</small>";
    n.appendChild(h("div", "a-obj on", "▦ Customers")); if (PART === "key") n.appendChild(h("div", "a-obj", "▦ Orders"));
    if (S.q.ran) { n.appendChild(h("small", "", "Queries")); n.appendChild(h("div", "a-obj", "▤ Query1")); }
  }
  function main() {
    const m = $(".a-main", root); m.innerHTML = "";
    $(".a-view", root).textContent = { design: "Design View", datasheet: "Datasheet View", query: "Query Design", result: "Datasheet View", rel: "Relationships" }[S.view];
    if (S.view === "design") {
      const t = h("table", "a-grid"); t.innerHTML = "<tr><th></th><th>Field Name</th><th>Data Type</th></tr>";
      S.fields.forEach((f, i) => {
        const tr = h("tr", S.sel === i ? "sel" : ""); const k = h("td", "a-key", f.key ? "🔑" : ""); tr.appendChild(k);
        const a = h("td"); const inp = h("input", "a-in"); inp.value = f.name; inp.placeholder = i === S.fields.length - 1 ? "type a field name" : ""; inp.disabled = PART !== "table" || f.name === "ID";
        inp.addEventListener("change", () => { f.name = inp.value.trim(); if (f.name && i === S.fields.length - 1 && S.fields.length < 6) S.fields.push({ name: "", type: "Short Text" }); say(`Field <b>${f.name}</b>. Its data type: what kind of data it holds.`); draw(); });
        inp.addEventListener("focus", () => { S.sel = i; }); a.appendChild(inp); tr.appendChild(a);
        const b = h("td"); const sel = h("select", "a-in"); TYPES.forEach((x) => { const o = h("option", "", x); if (x === f.type) o.selected = true; sel.appendChild(o); });
        sel.disabled = PART !== "table" || f.name === "ID";
        sel.addEventListener("change", () => { f.type = sel.value; say(`${f.name || "The field"}: <b>${f.type}</b>.${f.type !== "Short Text" && (f.name === "Name" || f.name === "City") ? " A name or a city is text: Short Text." : ""}`, f.type !== "Short Text"); draw(); });
        b.appendChild(sel); tr.appendChild(b);
        tr.addEventListener("click", () => { S.sel = i; draw(); });
        t.appendChild(tr);
      });
      m.appendChild(t);
    } else if (S.view === "datasheet" || S.view === "result") {
      const cols = S.view === "result" ? S.q.fields : S.fields.filter((f) => f.name).map((f) => f.name);
      let rows = S.rows;
      if (S.view === "result") { rows = rows.filter((r) => Object.entries(S.q.crit).every(([k, v]) => !v || String(r[k]).toLowerCase() === v.replace(/"/g, "").toLowerCase()));
        Object.entries(S.q.sort).forEach(([k, v]) => { if (v) rows = [...rows].sort((a, b) => (v === "Ascending" ? 1 : -1) * String(a[k]).localeCompare(String(b[k]))); }); }
      const t = h("table", "a-grid ds"); const hr = h("tr"); cols.forEach((c) => hr.appendChild(h("th", "", c))); t.appendChild(hr);
      rows.forEach((r) => { const tr = h("tr"); cols.forEach((c) => tr.appendChild(h("td", "", String(r[c] ?? "")))); t.appendChild(tr); });
      if (S.view === "datasheet" && PART === "table") {
        const tr = h("tr", "new"); cols.forEach((c) => { const td = h("td"); if (c === "ID") td.textContent = "(New)"; else { const i = h("input", "a-in"); i.dataset.c = c; td.appendChild(i);
          i.addEventListener("keydown", (e) => { if (e.key === "Enter" || (e.key === "Tab" && c === cols[cols.length - 1])) { e.preventDefault(); const vals = {}; tr.querySelectorAll("input").forEach((x) => { vals[x.dataset.c] = x.value.trim(); });
            if (Object.values(vals).some(Boolean)) { S.rows.push({ ID: S.rows.length + 1, ...vals }); say(`Record ${S.rows.length} is saved. ID = ${S.rows.length}: AutoNumber counts by itself.`); draw(); $(".a-grid tr.new input", root).focus(); } } }); }
          tr.appendChild(td); }); t.appendChild(tr);
      }
      m.appendChild(t);
      if (S.view === "result") m.appendChild(btn("Back to Design View", "Design View", () => { S.view = "query"; draw(); }, "ghost"));
    } else if (S.view === "query") {
      const box = h("div", "a-tbl"); box.appendChild(h("b", "", "Customers"));
      ["*", "ID", "Name", "City"].forEach((f) => { const d = h("div", "a-fld" + (S.q.fields.includes(f) ? " on" : ""), f);
        d.addEventListener("dblclick", () => { if (f === "*" || S.q.fields.includes(f)) return; S.q.fields.push(f); say(`<b>${f}</b> is in the grid: a column of the result.`); draw(); });
        d.addEventListener("click", () => say("Double-click a field to add it to the grid.")); box.appendChild(d); });
      m.appendChild(box);
      const g = h("table", "a-grid q"); const rowsDef = [["Field:", (f) => f], ["Table:", () => "Customers"], ["Sort:", null], ["Show:", () => "☑"], ["Criteria:", "crit"]];
      rowsDef.forEach(([lab, fn]) => { const tr = h("tr"); tr.appendChild(h("th", "", lab));
        for (let k = 0; k < 3; k++) { const f = S.q.fields[k]; const td = h("td");
          if (f && fn === "crit") { const i = h("input", "a-in"); i.value = S.q.crit[f] || ""; i.addEventListener("change", () => { S.q.crit[f] = i.value.trim(); say(`Criterion of <b>${f}</b>: <b>${S.q.crit[f]}</b>: only the records with this value.`); draw(); }); td.appendChild(i); }
          else if (f && fn === null) { const sel = h("select", "a-in"); ["", "Ascending", "Descending"].forEach((x) => { const o = h("option", "", x); if (S.q.sort[f] === x) o.selected = true; sel.appendChild(o); });
            sel.addEventListener("change", () => { S.q.sort[f] = sel.value; say(`Sort by <b>${f}</b>: <b>${sel.value || "(not sorted)"}</b>.`); draw(); }); td.appendChild(sel); }
          else if (f) td.textContent = fn(f); tr.appendChild(td); }
        g.appendChild(tr); });
      m.appendChild(g);
    } else if (S.view === "rel") {
      const w = h("div", "a-rel");
      const tbl = (name, fs, side) => { const b = h("div", "a-tbl " + side); b.appendChild(h("b", "", name)); fs.forEach((f) => { const d = h("div", "a-fld" + (S.pick && S.pick[0] === name && S.pick[1] === f ? " on" : ""), (name === "Customers" && f === "ID" ? "🔑 " : "") + f);
        d.addEventListener("click", () => pickField(name, f)); b.appendChild(d); }); return b; };
      w.appendChild(tbl("Customers", ["ID", "Name", "City"], "l")); w.appendChild(tbl("Orders", ["OrderID", "CustomerID", "Product"], "r"));
      if (S.rels) w.appendChild(h("div", "a-line", "1 ─────────── ∞"));
      m.appendChild(w);
    }
  }
  function pickField(t, f) {
    if (!S.pick) { S.pick = [t, f]; say(`<b>${t}.${f}</b> is chosen. Now click the field that it joins in the other table.`); draw(); return; }
    const a = S.pick, b = [t, f]; S.pick = null;
    const ok = (a[0] === "Customers" && a[1] === "ID" && b[0] === "Orders" && b[1] === "CustomerID") || (b[0] === "Customers" && b[1] === "ID" && a[0] === "Orders" && a[1] === "CustomerID");
    if (ok) { S.rels = true; say("&#10003; The relationship: <b>Customers.ID</b> (the key) joins <b>Orders.CustomerID</b>. One customer has many orders (1 to ∞)."); }
    else say("These fields do not join the tables. The key of Customers (<b>ID</b>) goes with <b>CustomerID</b> in Orders.", true);
    draw();
  }
  const MISSIONS = {
    table: [
      ["Design View: the field <b>Name</b>, data type <b>Short Text</b>", () => S.fields.some((f) => /^name$/i.test(f.name) && f.type === "Short Text")],
      ["The field <b>City</b>, data type <b>Short Text</b>", () => S.fields.some((f) => /^city$/i.test(f.name) && f.type === "Short Text")],
      ["<b>View › Datasheet View</b>: type 3 customers: Huda, Amman · Omar, Irbid · Rana, Amman", () => S.rows.length >= 3],
    ],
    key: [
      ["Click the row of <b>ID</b>, then <b>Primary Key</b>", () => S.fields.some((f) => f.name === "ID" && f.key)],
      ["<b>Database Tools › Relationships</b>: click <b>ID</b> in Customers, then <b>CustomerID</b> in Orders", () => S.rels],
    ],
    query: [
      ["Double-click <b>Name</b> and <b>City</b>: they go into the grid", () => S.q.fields.includes("Name") && S.q.fields.includes("City")],
      ["<b>Criteria</b> under City: <b>Amman</b>; <b>Sort</b> under Name: <b>Ascending</b>", () => /amman/i.test(S.q.crit.City || "") && S.q.sort.Name === "Ascending"],
      ["<b>Run</b>: 2 customers, Huda and Rana", () => S.q.ran && /amman/i.test(S.q.crit.City || "")],
    ],
  }[PART];
  function status() {
    const list = $("#jobs"); list.innerHTML = ""; let done = 0;
    MISSIONS.forEach(([t, f]) => { const ok = !!f(); done += ok; const li = h("li", ok ? "ok" : ""); li.innerHTML = t; list.appendChild(li); });
    $("#progress").textContent = `${done} of ${MISSIONS.length}`;
    if (done === MISSIONS.length && !status.done) { status.done = true; say(window.SIM_DONE || "&#10003; All steps done. Now do the same steps in Access."); }
  }
  function draw() { tabs(); ribbon(); nav(); main(); status(); }
  document.addEventListener("click", (e) => { if (S.menu && !e.target.closest(".w-menu")) { S.menu = false; draw(); } });
  $("#reset").addEventListener("click", () => { reset(); status.done = false; say(HELLO); draw(); });
  const HELLO = { table: "Design View of the table <b>Customers</b>. Click the empty row and type the field name <b>Name</b>.",
    key: "Click the row of <b>ID</b> (the small square on the left), then <b>Primary Key</b>.", query: "Double-click <b>Name</b>, then <b>City</b>, in the box of the table Customers." }[PART];
  reset(); say(HELLO); draw();
})();
