// BigQuery Lab 2: a simulator that looks like BigQuery Studio in Chrome, with a
// real SQL engine (shared/sims/bq-engine.js on sql.js): the student makes a
// dataset, loads the CSV file of an online shop into a table, looks at it
// (Schema, Details, Preview) and asks it a question with SELECT … FROM …
// WHERE. Any query works: a change gives what BigQuery would give (its
// errors, rows in any order without ORDER BY, the bytes before the run).
//
// The page chooses the part (window.BQ_LAB2):
//   "load":  an empty project: Create dataset, Create table (Upload), Schema, Details;
//   "all":   the whole worksheet (Tasks 1-3 and Finished early?); it remembers
//            the work of the student in this browser (localStorage).
// ?shot=<name> draws one screen of the worksheet with its orange numbers.
//
// The data: online_retail_2010.csv, 1 row in every 25 of the real file
// (Online Retail II, UCI, CC BY 4.0: 525,461 rows from Dec 2009 to Dec 2010).
(() => {
  const PART = window.BQ_LAB2 || "all";
  const SHOT = new URLSearchParams(location.search).get("shot");
  const PROJECT = "big-data-lab";
  const FILE = "online_retail_2010.csv";
  const VENDOR = "../../../../shared/sims/vendor/";
  const KEY = "bq-lab2-" + PART;
  const $ = (s, el = document) => el.querySelector(s);
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const num = (n) => Number(n).toLocaleString("en-US");
  const fmt = (b) => window.BQEngine.fmtBytes(b);
  const norm = (q) => q.replace(/--[^\n]*/g, "").replace(/\s+/g, " ").replace(/\s*([(),;*=<>])\s*/g, "$1").trim().toLowerCase().replace(/;$/, "");

  // The queries of the worksheet: SELECT … FROM … WHERE, and CREATE TABLE with its columns
  // (business students: no CREATE … AS SELECT, no GROUP BY; courses/big-data/NOTES.md).
  const Q_RETURNS = "SELECT Description, Quantity, Country\nFROM shop.sales\nWHERE Quantity < 0;";
  const Q_CUSTOMERS = "CREATE TABLE shop.customers (\n  customer_id INTEGER,\n  name STRING,\n  city STRING\n);";
  const Q_START = (t) => "SELECT * FROM `big-data-lab." + t + "` LIMIT 1000";
  // Try a change: the changes a student often wants to try, and what they show.
  const CHANGES = [
    { id: "france", label: "Only one country: France", sql: "SELECT Description, Quantity, Country\nFROM shop.sales\nWHERE Country = 'France';",
      say: "<b>WHERE Country = 'France'</b>: only the rows of France. A text value goes between quotes <b>'…'</b>." },
    { id: "noquote", label: "Forget the quotes", sql: "SELECT Description, Quantity, Country\nFROM shop.sales\nWHERE Country = France;",
      say: "Without quotes, BigQuery thinks <b>France</b> is the name of a column, and there is no such column. Text needs quotes: <b>'France'</b>." },
    { id: "big", label: "Big orders: 100 or more", sql: "SELECT Description, Quantity, Price\nFROM shop.sales\nWHERE Quantity >= 100;",
      say: "<b>&gt;=</b> means <i>more than or equal to</i>. These are the big orders: a wholesale customer, maybe." },
    { id: "star", label: "All the columns (*)", sql: "SELECT *\nFROM shop.sales\nWHERE Quantity < 0;",
      say: "<b>*</b> = all the columns. The same rows, more columns. Look at the bytes: * reads more data than three columns." },
    { id: "nowhere", label: "Remove the WHERE line", sql: "SELECT Description, Quantity, Country\nFROM shop.sales;",
      say: "Without <b>WHERE</b>, every row comes back: no filter." },
    { id: "and", label: "Two conditions (AND)", sql: "SELECT Description, Quantity, Country\nFROM shop.sales\nWHERE Country = 'France' AND Quantity < 0;",
      say: "<b>AND</b>: both must be true. The returns of France only." },
    { id: "unknown", label: "Unknown customers", sql: "SELECT Description, Quantity, Customer_ID\nFROM shop.sales\nWHERE Customer_ID IS NULL;",
      say: "<b>null</b> = no value: the shop does not know the customer. <b>IS NULL</b> finds these rows." },
    { id: "badcol", label: "A column name spelled wrong", sql: "SELECT Descripton, Quantity, Country\nFROM shop.sales\nWHERE Quantity < 0;",
      say: "<b>Unrecognized name</b>: there is no such column. BigQuery even says <b>Did you mean Description?</b>" },
    { id: "badtable", label: "A table name spelled wrong", sql: "SELECT Description, Quantity, Country\nFROM shop.sale\nWHERE Quantity < 0;",
      say: "<b>Not found</b>: the table <b>sale</b> is not there. Copy the name from the Explorer: <b>sales</b>." },
  ];
  const IS_CHANGE = (sql) => CHANGES.find((c) => norm(c.sql) === norm(sql));

  let eng, csvText, st;
  const fresh = () => ({ tree: [], open: {}, tabs: [], tab: null, sub: "Schema", sql: "", estimate: null, busy: false, result: null,
    rsub: "Results", page: 0, menu: null, panel: null, form: {}, picker: false, done: [], log: [], tries: [] });
  const done = (k) => st.done.includes(k);
  const mark = (k) => { if (!done(k)) st.done.push(k); };

  // ---------- The steps of each part ----------
  const hasTable = (ds, t) => !!(eng && eng.findTable(ds, t));
  const MISSIONS = {
    load: [
      ["Next to <b>big-data-lab</b>, click <b>⋮</b>, then <b>Create dataset</b>", () => done("menu-ds")],
      ["Dataset ID: <b>shop</b>. Click <b>Create dataset</b>", () => !!(eng && eng.findSet("shop"))],
      ["Next to <b>shop</b>, click <b>⋮</b>, then <b>Create table</b>", () => done("menu-tbl")],
      ["<b>Upload</b>, <b>Browse</b>: the file <b>" + FILE + "</b>", () => done("file")],
      ["Table: <b>sales</b>. Tick <b>Auto detect</b>. Click <b>Create table</b>", () => hasTable("shop", "sales")],
      ["Open <b>sales</b>: <b>Schema</b>, then <b>Details</b>", () => done("Schema") && done("Details")],
    ],
  };
  MISSIONS.all = [
    ["Task 1 · Create the dataset <b>shop</b>", () => !!(eng && eng.findSet("shop"))],
    ["Task 1 · Load <b>" + FILE + "</b> into the table <b>sales</b>", () => hasTable("shop", "sales")],
    ["Task 2 · <b>Schema</b>, <b>Details</b> and <b>Preview</b> of <b>sales</b>", () => done("Schema") && done("Details") && done("Preview")],
    ["Task 3 · Ask: which sales are returns? (<b>Run</b>)", () => done("run-returns")],
    ["Task 3 · <b>Try a change</b>: run 2 changes", () => st.tries.length >= 2],
    ["Finished early? · the empty table <b>customers</b>", () => hasTable("shop", "customers")],
  ];
  const missions = () => MISSIONS[PART];
  const allDone = () => missions().every(([, ok]) => ok());
  function steps() {
    const ol = $("#jobs"); if (!ol) return;
    ol.innerHTML = ""; let k = 0;
    missions().forEach(([t, ok]) => { const li = document.createElement("li"); li.innerHTML = t; if (ok()) { li.className = "ok"; k++; } ol.appendChild(li); });
    $("#progress").textContent = k + " of " + missions().length + " done";
  }
  function say(t, bad) {
    const m = $("#msg"); if (!m) return;
    const end = !bad && allDone();
    m.innerHTML = t + (end ? "<br><b>" + (PART === "all" ? "All done: show your teacher." : "All done: the same steps as Tasks 1 and 2 of your worksheet.") + "</b>" : "");
    m.className = "message" + (bad ? " bad" : end ? " good" : "");
  }

  // ---------- Remember the work (the whole worksheet only) ----------
  function save() {
    if (PART !== "all" || SHOT) return;
    try { localStorage.setItem(KEY, JSON.stringify({ log: st.log, done: st.done, tries: st.tries })); } catch (e) { /* no storage: fine */ }
  }
  function replay(log) {
    for (const x of log) {
      if (x.a === "ds") eng.createDataset(x.id);
      if (x.a === "load") eng.loadCsv(x.ds, x.t, csvText, { autodetect: true });
      if (x.a === "sql") eng.run(x.sql);
    }
  }

  // ---------- Drawing ----------
  const root = $("#bq");
  function grid(head, rows, from = 0) {
    return '<div class="b-scroll"><table class="b-grid"><tr><th>Row</th>' + head.map((h) => "<th>" + esc(h) + "</th>").join("") + "</tr>" +
      rows.map((r, i) => "<tr><td>" + (from + i + 1) + "</td>" + r.map((v) => '<td class="' + (v === "null" ? "nul" : "") + '">' + esc(v) + "</td>").join("") + "</tr>").join("") + "</table></div>";
  }
  function treeHtml() {
    let h = '<li data-node="proj" class="b-node"><span class="ar">⌄</span>' + PROJECT + '<button class="b-dots" data-menu="proj" title="View actions" aria-label="View actions">⋮</button></li>';
    for (const d of eng.datasets()) {
      const open = st.open[d.id] !== false;
      h += '<li data-node="ds:' + d.id + '" class="b-node" style="padding-left:20px"><span class="ar">' + (open ? "⌄" : "›") + "</span>" + esc(d.id) +
        '<button class="b-dots" data-menu="ds:' + d.id + '" title="View actions" aria-label="View actions">⋮</button></li>';
      if (open) for (const t of d.tables) h += '<li data-node="tbl:' + d.id + "." + t.id + '" class="b-node ' + (st.tab === d.id + "." + t.id ? "sel" : "") + '" style="padding-left:40px">▦&nbsp;' + esc(t.id) + "</li>";
    }
    if (!eng.datasets().length) h += '<li class="b-empty">No datasets yet.</li>';
    return h;
  }
  function menuHtml() {
    if (!st.menu) return "";
    const items = st.menu === "proj" ? [["create-ds", "Create dataset"], ["x", "Refresh contents"], ["x", "Copy ID"]]
      : [["create-tbl", "Create table"], ["x", "Open"], ["x", "Share"], ["x", "Copy ID"], ["x", "Delete"]];
    return '<div class="b-menu" style="top:' + (st.menuY || 80) + 'px">' + items.map(([a, t]) => '<button data-act="' + a + '">' + t + "</button>").join("") + "</div>";
  }
  function panelHtml() {
    if (!st.panel) return "";
    const f = st.form;
    if (st.panel === "ds") {
      return '<div class="b-panel"><div class="b-ph"><b>Create dataset</b><button class="b-x" data-act="close" aria-label="Close">✕</button></div><div class="b-pb">' +
        '<label class="b-field"><span>Project ID</span><input value="' + PROJECT + '" disabled></label>' +
        '<label class="b-field"><span>Dataset ID *</span><input id="f-ds" value="' + esc(f.ds || "") + '" placeholder="Letters, numbers and underscores"></label>' +
        '<div class="b-field"><span>Location type</span><div class="b-radio"><label><input type="radio" disabled> Region</label><label><input type="radio" checked disabled> Multi-region: <b>US</b></label></div></div>' +
        '<div class="b-note">Sandbox: tables expire after 60 days.</div>' +
        (f.err ? '<div class="b-err">' + esc(f.err) + "</div>" : "") +
        '</div><div class="b-pf"><button class="b-primary" data-act="do-ds">Create dataset</button><button class="b-btn" data-act="close">Cancel</button></div></div>';
    }
    const src = f.src || "Empty table";
    return '<div class="b-panel"><div class="b-ph"><b>Create table</b><button class="b-x" data-act="close" aria-label="Close">✕</button></div><div class="b-pb">' +
      '<div class="b-sec">Source</div>' +
      '<label class="b-field"><span>Create table from</span><select id="f-src">' + ["Empty table", "Google Cloud Storage", "Upload", "Drive"].map((x) => "<option" + (x === src ? " selected" : "") + ">" + x + "</option>").join("") + "</select></label>" +
      (src === "Upload" ? '<div class="b-field"><span>Select file *</span><div class="b-file"><input value="' + esc(f.file || "") + '" placeholder="No file chosen" readonly><button class="b-btn" data-act="browse">Browse</button></div></div>' +
        '<label class="b-field"><span>File format</span><select id="f-fmt">' + ["CSV", "JSONL (Newline delimited JSON)", "Avro", "Parquet", "ORC"].map((x) => "<option" + ((f.fmt || "CSV") === x ? " selected" : "") + ">" + x + "</option>").join("") + "</select></label>" : "") +
      (src !== "Upload" && src !== "Empty table" ? '<div class="b-note">Not in this lab: choose <b>Upload</b>.</div>' : "") +
      '<div class="b-sec">Destination</div>' +
      '<label class="b-field"><span>Project</span><input value="' + PROJECT + '" disabled></label>' +
      '<label class="b-field"><span>Dataset</span><input value="' + esc(f.ds || "") + '" disabled></label>' +
      '<label class="b-field"><span>Table *</span><input id="f-tbl" value="' + esc(f.tbl || "") + '" placeholder="Letters, numbers and underscores"></label>' +
      '<div class="b-sec">Schema</div>' +
      '<label class="b-check"><input type="checkbox" id="f-auto"' + (f.auto ? " checked" : "") + "> Auto detect</label>" +
      '<div class="b-note">Auto detect reads the first rows of the file: the names of the columns (the header) and the type of each column.</div>' +
      (f.err ? '<div class="b-err">' + esc(f.err) + "</div>" : "") +
      '</div><div class="b-pf"><button class="b-primary" data-act="do-tbl">Create table</button><button class="b-btn" data-act="close">Cancel</button></div></div>';
  }
  function pickerHtml() {
    if (!st.picker) return "";
    const files = [[FILE, "1.9 MB", "CSV file"], ["online_retail_2010.xlsx", "45.6 MB", "Excel workbook"], ["shop_logo.png", "38 KB", "PNG image"]];
    return '<div class="b-dim"><div class="b-dialog b-open"><h4>Open</h4><div class="b-note">This PC › Documents › Lab 2</div>' +
      '<table class="b-files"><tr><th>Name</th><th>Type</th><th>Size</th></tr>' +
      files.map(([n, s, ty]) => '<tr data-file="' + n + '"><td>' + (ty === "CSV file" ? "▤ " : ty === "PNG image" ? "▨ " : "▦ ") + n + "</td><td>" + ty + "</td><td>" + s + "</td></tr>").join("") +
      '</table><div class="b-pf"><button class="b-btn" data-act="pick-cancel">Cancel</button></div></div></div>';
  }
  function tableHtml(id) {
    const [ds, name] = id.split(".");
    const f = eng.findTable(ds, name);
    if (!f) return '<div class="b-pad"><div class="b-note">This table is not there any more.</div></div>';
    const info = f.info;
    let body = "";
    if (st.sub === "Schema") body = '<div class="b-scroll"><table class="b-grid"><tr><th>Field name</th><th>Type</th><th>Mode</th></tr>' +
      info.schema.map((c) => "<tr><td>" + esc(c.name) + '</td><td class="ty">' + c.type + "</td><td>NULLABLE</td></tr>").join("") + "</table></div>";
    if (st.sub === "Details") {
      const exp = new Date(info.created.getTime() + 60 * 864e5);
      body = '<div class="b-h">Table info</div><div class="b-kv"><span>Table ID</span><b>' + PROJECT + "." + f.ds + "." + f.name + "</b><span>Created</span><b>" +
        info.created.toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short" }) + "</b><span>Table expiration</span><b>" + exp.toLocaleDateString("en-US", { dateStyle: "medium" }) +
        ' (sandbox: 60 days)</b><span>Data location</span><b>US</b></div><div class="b-h">Storage info</div><div class="b-kv"><span>Number of rows</span><b class="big" data-mk="rows">' +
        num(info.rows) + '</b><span>Total logical bytes</span><b class="big">' + fmt(info.bytes) + "</b></div>";
    }
    if (st.sub === "Preview") {
      const p = eng.preview(f.ds, f.name, 50);
      body = grid(p.head, p.rows) + '<div class="b-note">Preview is free: it runs no query. It shows the first rows only.</div>';
    }
    return '<div class="b-pad"><div class="b-tool"><h3>' + esc(f.name) + '</h3><button class="b-btn" data-act="query" data-mk="query">Query ⌄</button>' +
      '<span class="b-links">Share &nbsp; Copy &nbsp; Snapshot &nbsp; Delete &nbsp; Export</span></div><div class="b-sub">' +
      ["Schema", "Details", "Preview", "Lineage"].map((t) => '<button data-sub="' + t + '" data-mk="sub-' + t + '" class="' + (st.sub === t ? "on" : "") + '">' + t + "</button>").join("") +
      "</div>" + body + "</div>";
  }
  function estimateHtml() {
    const e = st.estimate;
    if (!e || e.empty) return '<span class="b-valid"></span>';
    if (!e.ok) return '<span class="b-valid err" data-mk="est">⊘ ' + esc(e.error.msg) + "</span>";
    return '<span class="b-valid ok" data-mk="est">' + (e.kind === "create" || e.kind === "define" ? "This statement will process " : e.kind === "drop" ? "This statement will remove a table: " : "This query will process ") +
      (e.kind === "drop" ? "" : fmt(e.bytes) + " when run.") + "</span>";
  }
  function resultHtml() {
    if (st.busy) return '<div class="b-busy">Query running… many computers read their parts of the table at the same time.</div>';
    const r = st.result;
    if (!r) return "";
    if (r.error) return '<div class="b-errbox"><b>⊘ ' + esc(r.error.msg) + "</b>" + (r.error.hint ? '<div class="b-hint">💡 ' + esc(r.error.hint) + "</div>" : "") + "</div>";
    let h = '<div class="b-h">Query results</div><div class="b-sub">' + ["Job information", "Results", "Execution details"].map((t) =>
      '<button data-rsub="' + t + '" data-mk="r-' + t.split(" ")[0] + '" class="' + (st.rsub === t ? "on" : "") + '">' + t + "</button>").join("") + "</div>";
    if (st.rsub === "Job information") {
      h += '<div class="b-kv"><span>Job ID</span><b>' + PROJECT + ":US.bquxjob_" + r.job + '</b><span>Duration</span><b class="big">' + Math.max(0.1, r.ms / 1000).toFixed(1) +
        ' sec</b><span>Bytes processed</span><b class="big">' + fmt(r.bytes) + "</b><span>Bytes billed</span><b>" + (r.bytes ? "10 MB" : "0 B") + "</b>" +
        (r.kind === "create" ? "<span>Destination table</span><b>" + PROJECT + "." + r.created + "</b>" : "") + "</div>" +
        '<div class="b-note">The sandbox gives 1 TB of queries a month. A query is billed 10 MB at least.</div>';
    } else if (st.rsub === "Execution details") {
      h += '<div class="b-note">Not in this lab: click <b>Results</b> or <b>Job information</b>.</div>';
    } else if (r.kind === "create" || r.kind === "drop") {
      h += '<div class="b-done" data-mk="created">' + (r.kind === "drop" ? "This statement removed the table " + PROJECT + "." + esc(r.target) + "."
        : r.skipped ? "The table " + PROJECT + "." + esc(r.created) + " is already there: nothing changed."
        : "This statement " + (r.replaced ? "replaced the table " : "created a new table named ") + PROJECT + "." + esc(r.created) + "." +
          ' <button class="b-btn" data-act="goto" data-t="' + esc(r.created) + '">Go to table</button>') + "</div>";
    } else {
      const per = 50, from = st.page * per, rows = r.rows.slice(from, from + per);
      h += grid(r.head, rows, from) + '<div class="b-pager">Results per page: 50 &nbsp; ' + (r.total ? num(from + 1) + " – " + num(Math.min(r.total, from + per)) : "0") + " of " + num(r.total) +
        ' <button class="b-btn" data-act="prev"' + (st.page ? "" : " disabled") + '>‹</button><button class="b-btn" data-act="next"' + (from + per < r.total ? "" : " disabled") + ">›</button></div>" +
        (r.shuffled ? '<div class="b-note b-warnnote">No ORDER BY: the rows come in any order. Run it again: the order can change.</div>' : "");
    }
    return h;
  }
  function queryHtml() {
    return '<div class="b-pad"><div class="b-run"><button class="b-primary" data-act="run" data-mk="run">▶ Run</button><span class="b-links">Save &nbsp; Share &nbsp; Schedule</span>' +
      estimateHtml() + "</div>" +
      '<div class="b-chips"><span>Type for me:</span><button data-type="returns">Task 3: the returns</button><button data-type="customers">Finished early?</button></div>' +
      '<div class="b-sqlwrap" data-mk="sql"><textarea class="b-sql" spellcheck="false" aria-label="SQL query">' + esc(st.sql) + "</textarea></div>" +
      (PART !== "load" ? '<details class="b-try"' + (st.tryOpen ? " open" : "") + '><summary data-mk="try">Try a change: what happens if…?</summary><div class="b-chips">' +
        CHANGES.map((c) => '<button data-change="' + c.id + '" class="' + (st.tries.includes(c.id) ? "tried" : "") + '">' + esc(c.label) + "</button>").join("") + "</div></details>" : "") +
      resultHtml() + "</div>";
  }
  function homeHtml() {
    return '<div class="b-pad"><div class="b-h" style="font-size:1.3rem;font-weight:400">Welcome to BigQuery Studio</div>' +
      '<div class="b-card"><b>Add your own data</b><small>In the Explorer: ⋮ next to <b>' + PROJECT + "</b> › <b>Create dataset</b>. Then ⋮ next to the dataset › <b>Create table</b>.</small></div>" +
      '<div class="b-card"><b>Run a query</b><small>Open a table, then click <b>Query</b>.</small></div></div>';
  }
  function draw() {
    const tabs = ["Home", ...st.tabs];
    const active = st.tab || "Home";
    let main;
    if (st.tab === "Untitled query") main = queryHtml();
    else if (st.tab) main = tableHtml(st.tab);
    else main = homeHtml();
    const label = (t) => (t === "Home" || t === "Untitled query" ? t : t.split(".")[1]);
    root.innerHTML = '<div class="b-addr"><span>&#8592; &#8594;</span><b>console.cloud.google.com/bigquery</b></div>' +
      '<div class="b-top"><span class="gc">Google Cloud</span><span class="proj">' + PROJECT + ' ⌄</span><span class="srch">Search (/) for resources, docs, products, and more</span><span class="me">S</span></div>' +
      '<div class="b-sand"><span>Sandbox: you are using BigQuery for free, with limits.</span><a>Upgrade</a></div>' +
      '<div class="b-body"><div class="b-exp"><div class="b-exp-head"><b>Explorer</b><button class="b-btn" data-act="add">+ Add data</button></div>' +
      '<ul class="b-tree">' + treeHtml() + "</ul>" + menuHtml() + '</div><div class="b-main"><div class="b-tabs">' +
      tabs.map((t) => '<button class="b-tab ' + (t === active ? "on" : "") + '" data-tab="' + esc(t) + '">' + esc(label(t)) + "</button>").join("") + "</div>" + main + "</div>" +
      panelHtml() + "</div>" + pickerHtml();
    const ta = $(".b-sql", root);
    if (ta) ta.addEventListener("input", () => { st.sql = ta.value; recheck(); });
    const bind = (id, k, ev = "input", f = (el) => el.value) => { const el = $("#" + id, root); if (el) el.addEventListener(ev, () => { st.form[k] = f(el); if (k === "src" || k === "fmt") draw(); }); };
    bind("f-ds", "ds"); bind("f-tbl", "tbl"); bind("f-src", "src", "change"); bind("f-fmt", "fmt", "change"); bind("f-auto", "auto", "change", (el) => el.checked);
    if (st.panel === "ds") { const i = $("#f-ds", root); if (i && !SHOT) i.focus(); i && i.addEventListener("keydown", (e) => { if (e.key === "Enter") act("do-ds"); }); }
    steps();
    if (SHOT) shotMarks();
  }
  let timer = null;
  function recheck() {
    clearTimeout(timer);
    timer = setTimeout(() => {
      st.estimate = eng.check(st.sql);
      const v = $(".b-valid", root);
      if (v) v.outerHTML = estimateHtml();
    }, 250);
  }

  // ---------- Clicks ----------
  function openTable(id, sub = "Schema") {
    if (!st.tabs.includes(id)) st.tabs.push(id);
    st.tab = id; st.sub = sub;
  }
  function act(a, el) {
    if (a === "add") return say("<b>+ Add data</b> has many sources. In this lab: <b>⋮</b> next to <b>" + PROJECT + "</b>, then <b>Create dataset</b>.", true);
    if (a === "x") { st.menu = null; draw(); return say("Not in this lab.", true); }
    if (a === "create-ds") { st.menu = null; st.panel = "ds"; st.form = { ds: "" }; mark("menu-ds"); draw(); return say("Type the <b>Dataset ID</b>: <b>shop</b>. Then click <b>Create dataset</b>."); }
    if (a === "create-tbl") {
      const ds = st.menuDs; st.menu = null; st.panel = "tbl"; st.form = { ds, src: "Empty table", tbl: "", auto: false }; mark("menu-tbl"); draw();
      return say("<b>Create table from</b>: choose <b>Upload</b>, then <b>Browse</b> for the file.");
    }
    if (a === "close") { st.panel = null; st.form = {}; draw(); return; }
    if (a === "do-ds") {
      const id = (st.form.ds || "").trim();
      if (!id) { st.form.err = "Dataset ID is required."; draw(); return say("Type <b>shop</b> in <b>Dataset ID</b>.", true); }
      const r = eng.createDataset(id);
      if (r.error) { st.form.err = r.error; draw(); return say(r.error.startsWith("Dataset IDs") ? "A Dataset ID has no spaces and no <b>-</b>: letters, numbers and <b>_</b> only." : r.error, true); }
      st.log.push({ a: "ds", id }); st.panel = null; st.form = {}; st.open[id] = true; save(); draw();
      return say("The dataset <b>" + esc(id) + "</b> is in the Explorer, under <b>" + PROJECT + "</b>. It is empty: a folder for tables." + (id !== "shop" ? " (The worksheet uses <b>shop</b>.)" : "") +
        " Now: <b>⋮</b> next to it, <b>Create table</b>.");
    }
    if (a === "browse") { st.picker = true; draw(); return; }
    if (a === "pick-cancel") { st.picker = false; draw(); return; }
    if (a === "do-tbl") {
      const f = st.form, name = (f.tbl || "").trim();
      const fail = (m, s) => { f.err = m; draw(); say(s || m, true); };
      if (f.src !== "Upload") return fail("Choose a source: Upload.", "<b>Create table from</b>: choose <b>Upload</b>. An empty table has no rows.");
      if (!f.file) return fail("Select a file.", "Click <b>Browse</b> and choose <b>" + FILE + "</b>.");
      if (f.file !== FILE) return fail("Error while reading data: BigQuery cannot read this file as " + (f.fmt || "CSV") + ".",
        f.file.endsWith(".xlsx") ? "BigQuery does not read <b>Excel</b> files (.xlsx). Save the sheet as <b>CSV</b> first: the file <b>" + FILE + "</b>." : "This is a picture, not data. Choose <b>" + FILE + "</b>.");
      if ((f.fmt || "CSV") !== "CSV") return fail("Error while reading data: the file is not " + f.fmt + ".", "The file ends with <b>.csv</b>: <b>File format: CSV</b>.");
      if (!name) return fail("Table name is required.", "Type the name of the table: <b>sales</b>.");
      const r = eng.loadCsv(f.ds, name, csvText, { autodetect: !!f.auto });
      if (r.error) return fail(r.error, r.error.startsWith("No schema") ? "Tick <b>Auto detect</b>: BigQuery then reads the names and the types of the columns from the file." :
        r.error.startsWith("Invalid") ? "A table name has no spaces and no <b>-</b>: letters, numbers and <b>_</b> only." : r.error);
      st.log.push({ a: "load", ds: f.ds, t: name }); st.panel = null; st.form = {};
      st.busy = true; draw();
      say("Load job running… BigQuery reads the file and writes its rows into the table.");
      setTimeout(() => {
        st.busy = false; openTable(f.ds + "." + name, "Schema"); markSub(); save(); draw();
        say("Load job done: <b>" + num(r.rows) + " rows</b> in the table <b>" + esc(name) + "</b>. Auto detect found <b>" + r.schema.length + " columns</b> and their types: see <b>Schema</b>." +
          (name !== "sales" ? " (The worksheet uses <b>sales</b>.)" : "") + " The header <b>Customer ID</b> became <b>Customer_ID</b>: a column name has no spaces.");
      }, 900);
      return;
    }
    if (a === "query") {
      if (!st.tabs.includes("Untitled query")) st.tabs.push("Untitled query");
      const t = st.tab && st.tab !== "Untitled query" ? st.tab : "shop.sales";
      st.tab = "Untitled query"; st.sql = Q_START(t); st.result = null; mark("tab"); draw(); recheck();
      return say("A short query is ready. Select it all (<b>Ctrl + A</b>) and delete it, then type the query of your worksheet, or click <b>Type for me</b>.");
    }
    if (a === "goto") { openTable(el.dataset.t, "Details"); markSub(); draw(); return say("The new table: <b>Details</b> shows its number of rows."); }
    if (a === "prev" || a === "next") { st.page += a === "next" ? 1 : -1; draw(); return; }
    if (a === "run") return run();
  }
  function markSub() {
    if (!st.tab || st.tab === "Untitled query") return;
    const [, name] = st.tab.split(".");
    mark(st.sub); mark(st.sub + "-" + name);
  }
  function run() {
    if (st.busy) return say("Wait: the query is running.", true);
    if (!st.sql.trim()) return say("The editor is empty: type the query first.", true);
    const text = st.sql;
    st.busy = true; st.result = null; st.page = 0; draw();
    setTimeout(() => {
      const r = eng.run(text);
      st.busy = false; st.result = r; st.rsub = "Results"; r.job = Math.random().toString(36).slice(2, 10);
      const ch = IS_CHANGE(text);
      if (ch && !st.tries.includes(ch.id) && !(ch.id === "again" && !r.error)) st.tries.push(ch.id);
      if (!r.error) {
        if (r.kind === "create" || r.kind === "drop") { st.log.push({ a: "sql", sql: text }); if (r.created) st.open[r.created.split(".")[0]] = true; }
        if (r.kind === "select" && norm(text) === norm(Q_RETURNS)) mark("run-returns");
      }
      save(); st.estimate = eng.check(st.sql); draw();
      if (r.error) return say((ch ? ch.say + "<br>" : "") + "A red message: read it. " + (r.error.hint ? esc(r.error.hint) : ""), !ch);
      if (ch) return say(ch.say + " (" + num(r.total) + " rows.)");
      if (r.kind === "create") return say(r.skipped ? "The table is already there: nothing changed." :
        "A new, <b>empty</b> table: <b>" + esc(r.created) + "</b>. Open it in the Explorer: its <b>Schema</b> shows your columns and their types. It has 0 rows: a file or an app fills it later.");
      if (r.kind === "drop") return say("The table is removed. (In a real project, think twice: there is no undo.)");
      if (norm(text) === norm(Q_RETURNS)) return say("<b>" + num(r.total) + " returns</b>: every row has a negative Quantity. Now open <b>Try a change</b> and try two changes.");
      return say(num(r.total) + " row" + (r.total === 1 ? "" : "s") + " in the answer; " + fmt(r.bytes) + " processed.");
    }, 700);
  }
  root.addEventListener("click", (e) => {
    if (st.picker) {
      const tr = e.target.closest("[data-file]");
      if (tr) { st.form.file = tr.dataset.file; st.picker = false; mark("file"); if (tr.dataset.file === FILE) st.form.fmt = "CSV"; draw();
        return tr.dataset.file === FILE ? say("The file is chosen. <b>File format: CSV</b>. Now the <b>Table</b> name: <b>sales</b>, and tick <b>Auto detect</b>.") : say("Is this the file of the sales? Look at its type.", true); }
    }
    const t = e.target.closest("[data-act],[data-node],[data-sub],[data-tab],[data-rsub],[data-type],[data-menu],[data-change]");
    if (!t) { if (st.menu) { st.menu = null; draw(); } return; }
    if (t.dataset.menu) {
      e.stopPropagation();
      const li = t.closest("li"), box = $(".b-exp", root).getBoundingClientRect();
      st.menu = t.dataset.menu; st.menuDs = st.menu.startsWith("ds:") ? st.menu.slice(3) : null;
      st.menuY = li.getBoundingClientRect().bottom - box.top; draw();
      return say(st.menu === "proj" ? "The menu of the project: click <b>Create dataset</b>." : "The menu of the dataset: click <b>Create table</b>.");
    }
    if (t.dataset.act) return act(t.dataset.act, t);
    if (t.dataset.type) {
      st.sql = t.dataset.type === "returns" ? Q_RETURNS : Q_CUSTOMERS;
      if (st.tab !== "Untitled query") { if (!st.tabs.includes("Untitled query")) st.tabs.push("Untitled query"); st.tab = "Untitled query"; mark("tab"); }
      st.result = null; draw(); recheck();
      return say("Typed. Look at the message on the right of <b>Run</b>: a green tick and the bytes it will read. Then click <b>Run</b>.");
    }
    if (t.dataset.change) {
      const c = CHANGES.find((x) => x.id === t.dataset.change);
      st.sql = c.sql; st.tryOpen = true; st.result = null;
      if (st.tab !== "Untitled query") { if (!st.tabs.includes("Untitled query")) st.tabs.push("Untitled query"); st.tab = "Untitled query"; }
      draw(); recheck();
      return say("The changed query is in the editor. What do you expect? Click <b>Run</b> and see.");
    }
    if (t.dataset.node) {
      const n = t.dataset.node;
      if (n === "proj") return say("Your project. Its <b>⋮</b> button opens its menu.");
      if (n.startsWith("ds:")) { const d = n.slice(3); st.open[d] = st.open[d] === false; draw(); return say("The dataset <b>" + esc(d) + "</b>. Its <b>⋮</b> button opens its menu."); }
      if (n.startsWith("tbl:")) { openTable(n.slice(4), st.tab && st.tab === n.slice(4) ? st.sub : "Schema"); markSub(); save(); draw(); return say(tableSay()); }
    }
    if (t.dataset.sub) { st.sub = t.dataset.sub; markSub(); save(); draw(); return say(tableSay()); }
    if (t.dataset.tab) { st.tab = t.dataset.tab === "Home" ? null : t.dataset.tab; draw(); return; }
    if (t.dataset.rsub) { st.rsub = t.dataset.rsub; draw(); return; }
  });
  function tableSay() {
    const [ds, name] = st.tab.split("."), f = eng.findTable(ds, name);
    if (!f) return "";
    if (st.sub === "Schema") return "<b>Schema</b>: the columns and their <b>types</b>. STRING = text, INTEGER = a whole number, FLOAT = a number with a point, TIMESTAMP = a date and a time.";
    if (st.sub === "Details") return "<b>Details</b>: <b>" + num(f.info.rows) + " rows</b>, " + fmt(f.info.bytes) + "." + (name === "sales" ? " The real file has 525,461 rows; this lab uses 1 row in every 25 of it." : "");
    if (st.sub === "Preview") return "<b>Preview</b>: the first rows, free. Each row is one item sold. A <b>negative Quantity</b> is a return; an empty <b>Customer_ID</b> (null) is an unknown customer.";
    return "Not in this lab.";
  }
  const reset = $("#reset");
  if (reset) reset.addEventListener("click", async () => {
    try { localStorage.removeItem(KEY); } catch (e) { /* fine */ }
    await start(true);
  });

  // ---------- Start ----------
  async function start(clean) {
    root.innerHTML = '<div class="b-pad b-busy">Opening BigQuery…</div>';
    eng = await window.BQEngine.create({ vendor: VENDOR, project: PROJECT });
    if (!csvText) csvText = await (await fetch(FILE)).text();
    st = fresh();
    if (PART === "all" && !clean && !SHOT) {
      try {
        const saved = JSON.parse(localStorage.getItem(KEY) || "null");
        if (saved && saved.log) { replay(saved.log); st.log = saved.log; st.done = saved.done || []; st.tries = saved.tries || []; }
      } catch (e) { /* start empty */ }
    }
    draw();
    if (SHOT) return shot(SHOT);
    say(st.log.length ? "Welcome back: your dataset and your tables are still here (in this browser). <b>Start again</b> empties the project."
      : "Start: in the <b>Explorer</b>, click <b>⋮</b> next to <b>" + PROJECT + "</b>, then <b>Create dataset</b>.");
  }

  // ---------- The screens of the worksheet (?shot=…) ----------
  // Each shot: what to do first, then the elements that get an orange number.
  const SHOTS = {
    "menu-ds": { go: () => { st.menu = "proj"; st.menuY = 64; }, marks: ['[data-menu="proj"]', '[data-act="create-ds"]'] },
    "dataset": { go: () => { st.panel = "ds"; st.form = { ds: "shop" }; }, marks: ["#f-ds", '[data-act="do-ds"]'] },
    "menu-tbl": { go: () => { eng.createDataset("shop"); st.open.shop = true; st.menu = "ds:shop"; st.menuDs = "shop"; st.menuY = 96; }, marks: ['[data-menu="ds:shop"]', '[data-act="create-tbl"]'] },
    "upload": { go: () => { eng.createDataset("shop"); st.open.shop = true; st.panel = "tbl"; st.form = { ds: "shop", src: "Upload", file: FILE, fmt: "CSV", tbl: "", auto: false }; },
      marks: ["#f-src", '[data-act="browse"]', "#f-fmt"] },
    "picker": { go: () => { eng.createDataset("shop"); st.open.shop = true; st.panel = "tbl"; st.form = { ds: "shop", src: "Upload", fmt: "CSV" }; st.picker = true; }, marks: ['[data-file="' + FILE + '"]'] },
    "table": { go: () => { eng.createDataset("shop"); st.open.shop = true; st.panel = "tbl"; st.form = { ds: "shop", src: "Upload", file: FILE, fmt: "CSV", tbl: "sales", auto: true }; },
      marks: ["#f-tbl", "#f-auto", '[data-act="do-tbl"]'], after: () => { const b = $(".b-pb", root); if (b) b.scrollTop = b.scrollHeight; } },
    "schema": { go: () => { loadAll(); openTable("shop.sales", "Schema"); }, marks: ['[data-node="tbl:shop.sales"]', '[data-mk="sub-Schema"]'] },
    "details": { go: () => { loadAll(); openTable("shop.sales", "Details"); }, marks: ['[data-mk="sub-Details"]', '[data-mk="rows"]'] },
    "preview": { go: () => { loadAll(); openTable("shop.sales", "Preview"); }, marks: ['[data-mk="sub-Preview"]'] },
    "where": { go: () => { loadAll(); st.tabs = ["shop.sales", "Untitled query"]; st.tab = "Untitled query"; st.sql = Q_RETURNS; st.estimate = eng.check(Q_RETURNS); st.result = runNow(Q_RETURNS);
      st.result.rows = st.result.rows.slice(0, 6); st.result.total = 514; st.result.shuffled = false; }, marks: ['[data-mk="sql"]', '[data-mk="run"]', '[data-mk="r-Results"]'] },
  };
  function loadAll() { if (!eng.findSet("shop")) eng.createDataset("shop"); if (!eng.findTable("shop", "sales")) eng.loadCsv("shop", "sales", csvText, { autodetect: true }); st.open.shop = true; }
  function runNow(q) { const r = eng.run(q); r.job = "a1b2c3d4"; return r; }
  let shotList = [];
  function shot(name) {
    const s = SHOTS[name]; if (!s) return;
    s.go(); shotList = s.marks; draw();
    if (s.after) s.after();
    document.body.classList.add("shot");
    document.documentElement.dataset.ready = "1";
  }
  function shotMarks() {
    if (new URLSearchParams(location.search).has("poster")) return;
    shotList.forEach((sel, i) => {
      const el = $(sel, root); if (!el) return;
      const b = document.createElement("span"); b.className = "b-mk"; b.textContent = i + 1;
      const host = el.tagName === "TR" ? el.firstElementChild : /^(INPUT|SELECT|TEXTAREA)$/.test(el.tagName) ? el.parentElement : el;
      host.classList.add("b-mkhost"); host.appendChild(b);
    });
  }
  start().catch((e) => { root.innerHTML = '<div class="b-pad b-err">The simulator could not start: ' + esc(e.message) + ". Reload the page.</div>"; });
})();
