// BigQuery Lab: a simulator that looks like BigQuery Studio in Chrome, with the
// public table of Chicago taxi trips of the Lab 1 worksheet. One engine, two
// parts, chosen by the page that loads it (window.BQ_LAB = "find" | "query"):
//   find:  + Add data › Public datasets › search › View dataset, then open the
//          table taxi_trips and its Details, Schema and Preview tabs;
//   query: Query on the table, the SQL of the worksheet, the estimate before
//          the run, Run, the Results and the Job information.
// The numbers are examples close to the real table (it may differ a little).
(() => {
  const PART = window.BQ_LAB || "find";
  const $ = (s, el = document) => el.querySelector(s);
  const TABLE = "bigquery-public-data.chicago_taxi_trips.taxi_trips";
  const YEARS = [["2013", "27,217,716"], ["2014", "37,395,436"], ["2015", "32,385,875"], ["2016", "31,759,339"], ["2017", "24,988,003"],
    ["2018", "20,732,088"], ["2019", "16,477,365"], ["2020", "3,889,032"], ["2021", "3,948,724"], ["2022", "6,382,474"], ["2023", "3,767,568"]];
  const PAYS = [["Cash", "100,218,417"], ["Credit Card", "84,320,995"], ["Unknown", "7,936,210"], ["Mobile", "5,016,447"], ["Prcard", "4,731,203"], ["No Charge", "1,105,718"]];
  const COMPANIES = [["Taxi Affiliation Services", "42,113,560"], ["Flash Cab", "21,905,331"], ["Dispatch Taxi Affiliation", "15,224,870"],
    ["Yellow Cab", "13,801,442"], ["Chicago Carriage Cab Corp", "12,560,118"], ["City Service", "9,877,301"]];
  const SCHEMA = [["unique_key", "STRING"], ["taxi_id", "STRING"], ["trip_start_timestamp", "TIMESTAMP"], ["trip_seconds", "INTEGER"],
    ["trip_miles", "FLOAT"], ["fare", "FLOAT"], ["tips", "FLOAT"], ["payment_type", "STRING"], ["company", "STRING"]];
  const PREVIEW = [["2016-02-11 08:15", "780", "9.25", "0.00", "Cash", "Taxi Affiliation Services"],
    ["2016-02-11 08:30", "420", "6.50", "2.00", "Credit Card", "Flash Cab"], ["2016-02-11 08:45", "1260", "21.75", "4.00", "Credit Card", "Sun Taxi"],
    ["2016-02-11 09:00", "300", "5.25", "0.00", "Cash", "Taxi Affiliation Services"], ["2016-02-11 09:15", "900", "12.00", "0.00", "Cash", "Medallion Leasin"]];
  const Q_YEAR = "SELECT EXTRACT(YEAR FROM trip_start_timestamp) AS year,\n  COUNT(*) AS trips\nFROM `" + TABLE + "`\nGROUP BY year\nORDER BY year;";
  const Q_PAY = "SELECT payment_type, COUNT(*) AS trips\nFROM `" + TABLE + "`\nGROUP BY payment_type\nORDER BY trips DESC;";
  const Q_START = "SELECT * FROM `" + TABLE + "` LIMIT 1000";

  let st;
  function reset() {
    st = PART === "find"
      ? { dialog: null, market: null, search: "", tree: ["big-data-lab"], open: false, tabs: [], tab: null, sub: "Schema", done: new Set() }
      : { dialog: null, market: null, tree: ["big-data-lab", "bigquery-public-data", "chicago_taxi_trips", "taxi_trips"], open: true,
          tabs: ["taxi_trips"], tab: "taxi_trips", sub: "Details", sql: "", busy: false, result: null, rsub: "Results", done: new Set() };
  }
  const doneText = () => window.SIM_DONE || (PART === "find" ? "All done: the same steps as Task 2 of your worksheet." : "All done: the same steps as Task 3 of your worksheet.");
  const allDone = () => MISSIONS.every(([, ok]) => ok());
  const say = (t, bad) => {
    const m = $("#msg");
    const end = !bad && allDone();
    m.innerHTML = t + (end ? "<br><b>" + doneText() + "</b>" : "");
    m.className = "message" + (bad ? " bad" : end ? " good" : "");
  };

  const MISSIONS = {
    find: [
      ["In the Explorer, click <b>+ Add data</b>", () => st.done.has("add")],
      ["Click <b>Public datasets</b>", () => st.done.has("public")],
      ["Search <b>chicago taxi</b>, click <b>Chicago Taxi Trips</b>", () => st.done.has("card")],
      ["Click <b>View dataset</b>", () => st.done.has("view")],
      ["Open <b>chicago_taxi_trips</b>, then click the table <b>taxi_trips</b>", () => st.done.has("table")],
      ["Click <b>Details</b>: how many rows?", () => st.done.has("Details")],
    ],
    query: [
      ["On the table, click <b>Query</b>: a new tab opens", () => st.done.has("tab")],
      ["Delete the short query. Type the query of <b>trips in each year</b>", () => st.done.has("typed-year")],
      ["Look at the estimate (<b>will process … GB</b>), then click <b>Run</b>", () => st.done.has("run-year")],
      ["Click <b>Job information</b>: Duration and Bytes processed", () => st.done.has("job")],
    ],
  }[PART];

  function steps() {
    const ol = $("#jobs"); ol.innerHTML = "";
    let k = 0;
    MISSIONS.forEach(([t, ok]) => { const li = document.createElement("li"); li.innerHTML = t; if (ok()) { li.className = "ok"; k++; } ol.appendChild(li); });
    $("#progress").textContent = k + " of " + MISSIONS.length + " done";

  }

  // ---------- Queries: what the editor understands ----------
  const norm = (q) => q.replace(/\s+/g, " ").replace(/\s*([(),;*])\s*/g, "$1").trim().toLowerCase().replace(/;$/, "");
  const KNOWN = [
    { q: Q_YEAR, id: "year", gb: "1.55 GB", head: ["year", "trips"], rows: YEARS, secs: 2 },
    { q: Q_PAY, id: "pay", gb: "1.32 GB", head: ["payment_type", "trips"], rows: PAYS, secs: 2 },
    { q: Q_PAY.replace(/payment_type/g, "company"), id: "company", gb: "2.04 GB", head: ["company", "trips"], rows: COMPANIES, secs: 3 },
    { q: Q_START, id: "all", gb: "75.12 GB", head: ["unique_key", "trip_start_timestamp", "fare", "payment_type"],
      rows: PREVIEW.map((r, i) => ["a7c" + (91 + i) + "e…", r[0], r[2], r[4]]), secs: 6 },
  ];
  const known = (sql) => KNOWN.find((k) => norm(k.q) === norm(sql));
  function estimate(sql) {
    if (!sql.trim()) return ["", ""];
    const k = known(sql);
    if (!k) return ["err", "Check what you typed: compare it with the worksheet, sign by sign."];
    if (k.id === "all") return ["warn", "This query will process 75.12 GB when run. SELECT * reads every column of every row!"];
    return ["ok", "This query will process " + k.gb + " when run."];
  }

  // ---------- Drawing ----------
  const root = $("#bq");
  function esc(t) { return String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
  function grid(head, rows, num = true) {
    return '<table class="b-grid"><tr>' + (num ? "<th>Row</th>" : "") + head.map((h) => "<th>" + esc(h) + "</th>").join("") + "</tr>" +
      rows.map((r, i) => "<tr>" + (num ? "<td>" + (i + 1) + "</td>" : "") + r.map((v) => "<td>" + esc(v) + "</td>").join("") + "</tr>").join("") + "</table>";
  }
  function treeHtml() {
    const items = [];
    const has = (x) => st.tree.includes(x);
    items.push(['<span class="ar">›</span>big-data-lab', "proj"]);
    if (has("bigquery-public-data")) items.push(['<span class="ar">' + (has("chicago_taxi_trips") ? "⌄" : "›") + "</span>bigquery-public-data", "pub"]);
    if (has("bigquery-public-data")) items.push(['&nbsp;&nbsp;&nbsp;<span class="ar">' + (has("taxi_trips") ? "⌄" : "›") + "</span>chicago_taxi_trips", "ds"]);
    if (has("taxi_trips")) items.push(["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▦ taxi_trips", "tbl"]);
    return items.map(([h, id]) => '<li data-node="' + id + '" class="' + (id === "tbl" && st.tab === "taxi_trips" ? "sel" : "") + '">' + h + "</li>").join("");
  }
  function tableHtml() {
    let body = "";
    if (st.sub === "Schema") body = grid(["Field name", "Type", "Mode"], SCHEMA.map((r) => [...r, "NULLABLE"]), false);
    if (st.sub === "Details") body = '<div class="b-h">Table info</div><div class="b-kv"><span>Table ID</span><b>' + TABLE + '</b><span>Data location</span><b>US</b></div>' +
      '<div class="b-h">Storage info</div><div class="b-kv"><span>Number of rows</span><b class="big">208,943,621</b><span>Total logical bytes</span><b class="big">75.12 GB</b></div>';
    if (st.sub === "Preview") body = grid(["trip_start_timestamp", "trip_seconds", "fare", "tips", "payment_type", "company"], PREVIEW) +
      '<div class="b-note">Preview is free: it runs no query. Each row is one taxi trip.</div>';
    return '<div class="b-pad"><div class="b-tool"><h3>taxi_trips</h3><button class="b-btn" data-act="query">Query ⌄</button>' +
      '<span style="color:#1a73e8;font-weight:600">Share &nbsp; Copy &nbsp; Export</span></div><div class="b-sub">' +
      ["Schema", "Details", "Preview", "Lineage"].map((t) => '<button data-sub="' + t + '" class="' + (st.sub === t ? "on" : "") + '">' + t + "</button>").join("") +
      "</div>" + body + "</div>";
  }
  function queryHtml() {
    const [kind, text] = estimate(st.sql);
    let res = "";
    if (st.busy) res = '<div class="b-busy">Query running… many computers read their parts of the table at the same time.</div>';
    else if (st.result) {
      const r = st.result;
      res = '<div class="b-h">Query results</div><div class="b-sub">' + ["Job information", "Results", "Visualization", "JSON"].map((t) =>
        '<button data-rsub="' + t + '" class="' + (st.rsub === t ? "on" : "") + '">' + t + "</button>").join("") + "</div>";
      if (st.rsub === "Results") res += grid(r.head, r.rows) + (r.id === "all" ? '<div class="b-note">LIMIT 1000 shows 1000 rows, but SELECT * still read the whole table: 75.12 GB.</div>' : "");
      else if (st.rsub === "Job information") res += '<div class="b-kv"><span>Start time</span><b>Nov 22, 2026, 10:12:04 AM</b><span>Duration</span><b class="big">' + r.secs +
        ' sec</b><span>Bytes processed</span><b class="big">' + r.gb + '</b><span>Bytes billed</span><b>' + r.gb + "</b></div>" +
        '<div class="b-note">The free sandbox gives 1 TB (about 1000 GB) of queries a month.</div>';
      else res += '<div class="b-note">Not in this lab: click <b>Results</b> or <b>Job information</b>.</div>';
    }
    return '<div class="b-pad"><div class="b-run"><button class="b-primary" data-act="run">▶ Run</button><span style="color:#5f6368;font-weight:600">Save &nbsp; Share</span>' +
      '<span class="b-valid ' + kind + '">' + esc(text) + '</span></div>' +
      '<div class="b-chips">Type for me: <button data-type="year">the query of Task 3 (years)</button><button data-type="pay">finished early? (payment types)</button></div>' +
      '<textarea class="b-sql" spellcheck="false" aria-label="SQL query">' + esc(st.sql) + "</textarea>" + res + "</div>";
  }
  function marketHtml() {
    if (st.market === "search") return '<div class="b-pad"><div class="b-h" style="font-size:1.2rem;font-weight:400">Marketplace</div>' +
      '<input class="b-input" id="mk" placeholder="Search Marketplace" value="' + esc(st.search) + '"> ' +
      '<button class="b-btn" data-act="search" style="margin-top:6px">Search</button>' +
      (/chicago|taxi/i.test(st.search) && st.searched ? '<div class="b-card" data-act="card"><b>Chicago Taxi Trips</b><small>City of Chicago · Datasets</small><small>Taxi trips in Chicago, from 2013. Public dataset.</small></div>' : "") +
      (st.searched && !/chicago|taxi/i.test(st.search) ? '<div class="b-note">No result. Type <b>chicago taxi</b>.</div>' : "") + "</div>";
    return '<div class="b-pad"><div class="b-h" style="font-size:1.2rem;font-weight:400">Chicago Taxi Trips</div><small style="color:#5f6368">City of Chicago · Datasets</small><br><br>' +
      '<button class="b-primary" data-act="view">VIEW DATASET</button><div class="b-h">Overview</div><div>Every taxi trip reported to the City of Chicago: the time, the fare, the tip, the payment type and the company.</div></div>';
  }
  function draw() {
    const tabs = st.market ? ["Marketplace"] : st.tabs;
    const active = st.market ? "Marketplace" : st.tab;
    let main = "";
    if (st.market) main = marketHtml();
    else if (st.tab === "taxi_trips") main = tableHtml();
    else if (st.tab === "Untitled query") main = queryHtml();
    else main = '<div class="b-pad"><div class="b-h" style="font-size:1.3rem;font-weight:400">BigQuery Studio</div><div style="color:#5f6368">Your project <b>big-data-lab</b> is empty. Click <b>+ Add data</b> in the Explorer.</div></div>';
    root.innerHTML = '<div class="b-addr"><span>&#8592; &#8594;</span><b>' + (st.market ? "console.cloud.google.com/marketplace" : "console.cloud.google.com/bigquery") + "</b></div>" +
      '<div class="b-top"><span class="gc">Google Cloud</span><span class="proj">big-data-lab ⌄</span><span class="srch">Search (/) for resources, docs, products, and more</span><span class="me">S</span></div>' +
      '<div class="b-sand"><span>Sandbox: you are using BigQuery for free, with limits.</span><a>Upgrade</a></div>' +
      '<div class="b-body"><div class="b-exp"><div class="b-exp-head"><b>Explorer</b><button class="b-btn" data-act="add">+ Add data</button></div>' +
      '<ul class="b-tree">' + treeHtml() + '</ul></div><div class="b-main"><div class="b-tabs">' +
      tabs.map((t) => '<button class="b-tab ' + (t === active ? "on" : "") + '" data-tab="' + t + '">' + t + "</button>").join("") + "</div>" + main + "</div>" +
      (st.dialog ? '<div class="b-dim"><div class="b-dialog"><h4>Add data</h4><div style="color:#5f6368">Choose where your data comes from.</div>' +
        '<button class="b-opt" data-act="local"><b>Local file</b><small>Upload a CSV or JSON file</small></button>' +
        '<button class="b-opt" data-act="gcs"><b>Google Cloud Storage</b><small>Load files from a bucket</small></button>' +
        '<button class="b-opt" data-act="public"><b>Public datasets</b><small>Free data that Google and others share</small></button>' +
        '<button class="b-btn" data-act="close">Cancel</button></div></div>' : "") + "</div>";
    const ta = $(".b-sql", root);
    if (ta) ta.addEventListener("input", () => { st.sql = ta.value; check(); const [k, t] = estimate(st.sql); const v = $(".b-valid", root); v.className = "b-valid " + k; v.textContent = t; steps(); });
    const mk = $("#mk", root);
    if (mk) { mk.addEventListener("input", () => { st.search = mk.value; st.searched = false; }); mk.addEventListener("keydown", (e) => { if (e.key === "Enter") act("search"); }); }
    steps();
  }
  function check() {
    const k = known(st.sql);
    if (k && k.id === "year") st.done.add("typed-year");
  }

  // ---------- Clicks ----------
  function act(a, el) {
    if (a === "add") {
      if (PART === "query") return say("In this part the table is already open: click <b>Query</b> on the table.", true);
      st.dialog = true; st.done.add("add"); draw(); return say("Where does the data come from? Click <b>Public datasets</b>.");
    }
    if (a === "close") { st.dialog = null; draw(); return; }
    if (a === "local" || a === "gcs") return say("Not today: that loads <b>your own</b> files (Lab 2). Click <b>Public datasets</b>.", true);
    if (a === "public") { st.dialog = null; st.market = "search"; st.searched = false; st.done.add("public"); draw(); setTimeout(() => $("#mk")?.focus(), 30); return say("Type <b>chicago taxi</b> in the search box and press Enter."); }
    if (a === "search") { st.searched = true; draw(); return /chicago|taxi/i.test(st.search) ? say("Click the card <b>Chicago Taxi Trips</b>.") : say("Type <b>chicago taxi</b>.", true); }
    if (a === "card") { st.market = "product"; st.done.add("card"); draw(); return say("Click <b>VIEW DATASET</b>."); }
    if (a === "view") { st.market = null; st.tree = ["big-data-lab", "bigquery-public-data"]; st.done.add("view"); draw();
      return say("BigQuery again: <b>bigquery-public-data</b> is in the Explorer. Click <b>chicago_taxi_trips</b> to open it."); }
    if (a === "query") {
      if (!st.tabs.includes("Untitled query")) st.tabs.push("Untitled query");
      st.tab = "Untitled query"; st.sql = Q_START; st.result = null; st.done.add("tab"); draw();
      return say("A short query is in the new tab. It reads <b>every column</b>: 75 GB! Delete it, then type the query of Task 5.");
    }
    if (a === "run") {
      if (st.busy) return say("Wait: the query is running.", true);
      const k = known(st.sql);
      if (!st.sql.trim()) return say("The editor is empty: type the query first.", true);
      if (!k) return say("A red message: check the query sign by sign. The signs <b>`</b> are on the key under Esc.", true);
      st.busy = true; st.result = null; draw();
      setTimeout(() => {
        st.busy = false; st.result = k; st.rsub = "Results";
        if (k.id === "year") st.done.add("run-year");
        if (k.id === "pay") st.done.add("run-pay");
        draw();
        say(k.id === "all" ? "It ran, but it read <b>75.12 GB</b>: SELECT * reads the whole table. Ask only for the columns you need."
          : k.id === "year" ? "About 200 million rows became <b>11 rows</b>: one for each year. Now click <b>Job information</b>."
          : k.id === "pay" ? "Cash and credit cards: most trips. One row for each way to pay." : "One row for each company, the biggest first.");
      }, 1300);
      return;
    }
  }
  root.addEventListener("click", (e) => {
    const t = e.target.closest("[data-act],[data-node],[data-sub],[data-tab],[data-rsub],[data-type]");
    if (!t) return;
    if (t.dataset.act) return act(t.dataset.act, t);
    if (t.dataset.type) { st.sql = t.dataset.type === "year" ? Q_YEAR : Q_PAY; check(); draw(); return say("Typed. Look at the estimate on the right of <b>Run</b>, then click <b>Run</b>."); }
    if (t.dataset.node) {
      const n = t.dataset.node;
      if (n === "proj") return say("This is your own project: it is still empty.", true);
      if (n === "pub") return say("Open the dataset under it: click <b>chicago_taxi_trips</b>.");
      if (n === "ds") { if (!st.tree.includes("chicago_taxi_trips")) st.tree.push("chicago_taxi_trips", "taxi_trips"); draw(); return say("The dataset holds one table. Click <b>taxi_trips</b>."); }
      if (n === "tbl") { if (!st.tabs.includes("taxi_trips")) st.tabs.push("taxi_trips"); st.tab = "taxi_trips"; st.sub = "Schema"; st.done.add("table"); draw();
        return say("The table is open on <b>Schema</b>: its columns. Click <b>Details</b>."); }
    }
    if (t.dataset.sub) { st.sub = t.dataset.sub; st.done.add(st.sub); draw();
      return say(st.sub === "Details" ? "More than <b>200 million rows</b>, about <b>75 GB</b>. <b>Schema</b> and <b>Preview</b> are free too." : st.sub === "Preview" ? "The first rows: each row is one trip. Preview is free." : st.sub === "Lineage" ? "Not in this lab." : "The columns of the table and their types."); }
    if (t.dataset.tab) { if (t.dataset.tab === "Marketplace") return; st.tab = t.dataset.tab; draw(); return; }
    if (t.dataset.rsub) { st.rsub = t.dataset.rsub; if (st.rsub === "Job information") st.done.add("job"); draw();
      if (st.rsub === "Job information" && st.result) say("<b>" + st.result.gb + "</b> read in about <b>" + st.result.secs + " seconds</b>. One computer would need minutes." + (st.done.has("run-pay") ? "" : " Now the second question: payment types.")); }
  });
  $("#reset").addEventListener("click", () => { reset(); draw(); say(PART === "find" ? "Start: click <b>+ Add data</b> in the Explorer." : "Start: click <b>Query</b> on the table."); });
  reset(); draw();
  say(PART === "find" ? "Start: click <b>+ Add data</b> in the Explorer." : "Start: click <b>Query</b> on the table.");
})();
