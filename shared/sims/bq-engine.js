// BQ Engine: real SQL with the rules of Google BigQuery, in the browser, for the
// BigQuery simulators of Big Data Labs 2-3 (courses/big-data). The SQL runs on
// SQLite (sql.js, vendor/sql-wasm.*, MIT); this file gives it the look and the
// rules of BigQuery, so a student who changes the query of the worksheet gets
// what BigQuery would give:
//   - CREATE TABLE shop.t (name STRING, …): an empty table with its columns;
//   - names: `big-data-lab.shop.sales`, shop.sales; a dataset is an attached
//     database; a table without its dataset is an error, as in BigQuery;
//   - BigQuery functions: EXTRACT, COUNTIF, FORMAT_DATE/FORMAT_TIMESTAMP,
//     DATE_TRUNC, SAFE_DIVIDE; "text" is a string; / always divides as FLOAT;
//   - BigQuery errors: Unrecognized name … Did you mean …?, Not found: Table …,
//     Syntax error … at [line:col], a column neither grouped nor aggregated,
//     Already Exists, no DML in the free sandbox;
//   - no ORDER BY: the rows come in any order (shuffled on every run), as on a
//     cluster where many computers finish at different times;
//   - the estimate before the run: the bytes of the columns that the query
//     reads (BigQuery stores every column apart), 0 B for COUNT(*) alone.
//
//   const eng = await BQEngine.create({ vendor: "../../../../shared/sims/vendor/" });
//   eng.createDataset("shop"); eng.loadCsv("shop", "sales", csvText, { autodetect: true });
//   eng.check(sql) → { ok, bytes, kind } or { ok: false, error: { msg, hint, line, col } }
//   eng.run(sql)   → { kind, head, rows, total, bytes, ms, shuffled, created, error }
(() => {
  const PROJECT_DEFAULT = "big-data-lab";
  const AGG = new Set(["COUNT", "SUM", "AVG", "MIN", "MAX", "COUNTIF", "ANY_VALUE", "STRING_AGG", "ARRAY_AGG", "LOGICAL_AND", "LOGICAL_OR", "STDDEV", "VARIANCE"]);
  const KEYWORDS = new Set(["SELECT", "FROM", "WHERE", "GROUP", "BY", "ORDER", "HAVING", "LIMIT", "AS", "AND", "OR", "NOT", "NULL", "IS", "IN",
    "LIKE", "BETWEEN", "CASE", "WHEN", "THEN", "ELSE", "END", "DISTINCT", "ASC", "DESC", "JOIN", "ON", "LEFT", "RIGHT", "INNER", "OUTER",
    "CREATE", "TABLE", "REPLACE", "DROP", "IF", "EXISTS", "WITH", "UNION", "ALL", "TRUE", "FALSE", "CAST", "EXTRACT", "OFFSET", "INTERVAL",
    "NULLS", "FIRST", "LAST", "OVER", "PARTITION", "CROSS", "FULL", "USING", "EXCEPT", "INTERSECT", "ESCAPE", "ROWS", "RANGE", "UNBOUNDED", "PRECEDING", "FOLLOWING", "CURRENT", "ROW"]);

  // ---------- Tokens ----------
  // Each token: { t: kind, v: text, p: offset in the statement }.
  function tokenize(s) {
    const out = [];
    let i = 0;
    while (i < s.length) {
      const c = s[i], p = i;
      if (/\s/.test(c)) { i++; continue; }
      if (c === "-" && s[i + 1] === "-" || c === "#") { while (i < s.length && s[i] !== "\n") i++; continue; }
      if (c === "/" && s[i + 1] === "*") { const e = s.indexOf("*/", i + 2); i = e < 0 ? s.length : e + 2; continue; }
      if (c === "'" || c === '"') {
        let j = i + 1, v = "";
        while (j < s.length && s[j] !== c) { if (s[j] === "\\" && j + 1 < s.length) { v += s[j + 1]; j += 2; } else v += s[j++]; }
        if (j >= s.length) { out.push({ t: "bad", v: "unclosed string", p }); return out; }
        out.push({ t: "str", v, p }); i = j + 1; continue;
      }
      if (c === "`") {
        const e = s.indexOf("`", i + 1);
        if (e < 0) { out.push({ t: "bad", v: "unclosed backtick", p }); return out; }
        out.push({ t: "bt", v: s.slice(i + 1, e), p }); i = e + 1; continue;
      }
      if (/[0-9]/.test(c) || c === "." && /[0-9]/.test(s[i + 1] || "")) {
        let j = i; while (j < s.length && /[0-9.eE]/.test(s[j])) j++;
        out.push({ t: "num", v: s.slice(i, j), p }); i = j; continue;
      }
      if (/[A-Za-z_]/.test(c)) {
        let j = i; while (j < s.length && /[A-Za-z0-9_]/.test(s[j])) j++;
        out.push({ t: "w", v: s.slice(i, j), p }); i = j; continue;
      }
      const two = s.slice(i, i + 2);
      if (["<=", ">=", "<>", "!=", "||"].includes(two)) { out.push({ t: "op", v: two, p }); i += 2; continue; }
      out.push({ t: "op", v: c, p }); i++;
    }
    return out;
  }
  const up = (tk) => tk && tk.t === "w" ? tk.v.toUpperCase() : null;
  // The index of the ")" that closes the "(" at i.
  function closing(tk, i) {
    let d = 0;
    for (let j = i; j < tk.length; j++) { if (tk[j].v === "(" && tk[j].t === "op") d++; if (tk[j].v === ")" && tk[j].t === "op" && --d === 0) return j; }
    return -1;
  }
  // Split tokens a..b at the commas of depth 0.
  function splitArgs(tk, a, b) {
    const parts = []; let d = 0, s = a;
    for (let j = a; j < b; j++) {
      const v = tk[j].t === "op" ? tk[j].v : "";
      if (v === "(") d++; else if (v === ")") d--; else if (v === "," && d === 0) { parts.push([s, j]); s = j + 1; }
    }
    parts.push([s, b]);
    return parts;
  }

  // Split the editor text into statements at the ";" outside strings and comments.
  function statements(text) {
    const out = []; let i = 0, s = 0;
    while (i < text.length) {
      const c = text[i];
      if (c === "'" || c === '"' || c === "`") { const e = text.indexOf(c, i + 1); i = e < 0 ? text.length : e + 1; continue; }
      if (c === "-" && text[i + 1] === "-" || c === "#") { while (i < text.length && text[i] !== "\n") i++; continue; }
      if (c === "/" && text[i + 1] === "*") { const e = text.indexOf("*/", i + 2); i = e < 0 ? text.length : e + 2; continue; }
      if (c === ";") { out.push({ sql: text.slice(s, i), at: s }); s = i + 1; }
      i++;
    }
    out.push({ sql: text.slice(s), at: s });
    return out.filter((x) => tokenize(x.sql).length);
  }

  function lineCol(text, off) {
    const before = text.slice(0, off).split("\n");
    return [before.length, before[before.length - 1].length + 1];
  }
  const qid = (n) => '"' + String(n).replace(/"/g, '""') + '"';
  // A column name for SQLite: [name] (never read as a text value, as "name" can be).
  const col = (n) => "[" + String(n).replace(/]/g, "") + "]";
  const qstr = (v) => "'" + String(v).replace(/'/g, "''") + "'";
  function lev(a, b) {
    a = a.toLowerCase(); b = b.toLowerCase();
    const d = Array.from({ length: a.length + 1 }, (_, i) => [i, ...Array(b.length).fill(0)]);
    for (let j = 1; j <= b.length; j++) d[0][j] = j;
    for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++)
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    return d[a.length][b.length];
  }
  function closest(name, list) {
    let best = null, bd = 99;
    list.forEach((x) => { const d = lev(name, x); if (d < bd) { bd = d; best = x; } });
    return bd <= Math.max(2, Math.floor(name.length / 3)) && best.toLowerCase() !== name.toLowerCase() ? best : null;
  }
  function fmtBytes(n) {
    if (n < 1024) return n + " B";
    const u = ["KB", "MB", "GB", "TB"]; let i = -1;
    do { n /= 1024; i++; } while (n >= 1024 && i < u.length - 1);
    return n.toFixed(2) + " " + u[i];
  }
  // The type of a column from its values (the auto detect of a CSV load).
  const TS = /^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(:\d{2}(\.\d+)?)?$/;
  function detect(values) {
    let n = 0, isInt = true, isNum = true, isTs = true, isDate = true, isBool = true;
    for (const v of values) {
      if (v === "" || v === null) continue;
      n++;
      if (!/^-?\d+$/.test(v)) isInt = false;
      if (!/^-?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$/.test(v)) isNum = false;
      if (!TS.test(v)) isTs = false;
      if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) isDate = false;
      if (!/^(true|false)$/i.test(v)) isBool = false;
    }
    if (!n) return "STRING";
    return isInt ? "INTEGER" : isNum ? "FLOAT" : isTs ? "TIMESTAMP" : isDate ? "DATE" : isBool ? "BOOLEAN" : "STRING";
  }
  // A CSV text → rows of strings (quotes, commas and new lines inside quotes).
  function parseCsv(text) {
    const rows = []; let row = [], f = "", q = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (q) { if (c === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; continue; }
      if (c === '"') q = true;
      else if (c === ",") { row.push(f); f = ""; }
      else if (c === "\n" || c === "\r") { if (c === "\r" && text[i + 1] === "\n") i++; row.push(f); rows.push(row); row = []; f = ""; }
      else f += c;
    }
    if (f !== "" || row.length) { row.push(f); rows.push(row); }
    return rows.filter((r) => r.length > 1 || r[0] !== "");
  }
  // A column name of BigQuery: letters, numbers and _ (a space becomes _).
  const bqName = (h, i) => (h.trim().replace(/[^A-Za-z0-9_]+/g, "_").replace(/^(\d)/, "_$1") || "string_field_" + i);

  class Engine {
    constructor(SQL, o) {
      this.db = new SQL.Database();
      this.project = o.project || PROJECT_DEFAULT;
      this.sets = {};       // dataset → { created, tables: { name → info } }
    }
    // ---------- Datasets and tables ----------
    createDataset(id) {
      if (!/^[A-Za-z0-9_]{1,1024}$/.test(id)) return { error: "Dataset IDs must be alphanumeric (plus underscores) and must be at most 1024 characters long." };
      if (/^(main|temp)$/i.test(id)) return { error: "This name is kept for the simulator. Choose another one." };
      if (this.findSet(id)) return { error: "Already Exists: Dataset " + this.project + ":" + id };
      this.db.run("ATTACH DATABASE ':memory:' AS " + qid(id));
      this.sets[id] = { created: new Date(), tables: {} };
      return { ok: true };
    }
    findSet(id) { return Object.keys(this.sets).find((k) => k.toLowerCase() === String(id).toLowerCase()) || null; }
    findTable(ds, t) {
      const s = this.findSet(ds); if (!s) return null;
      const k = Object.keys(this.sets[s].tables).find((x) => x.toLowerCase() === String(t).toLowerCase());
      return k ? { ds: s, name: k, info: this.sets[s].tables[k] } : null;
    }
    datasets() {
      return Object.keys(this.sets).map((id) => ({ id, created: this.sets[id].created,
        tables: Object.keys(this.sets[id].tables).map((n) => Object.assign({ id: n }, this.sets[id].tables[n])) }));
    }
    // Load a CSV text into a new table: the first row is the header (auto detect).
    loadCsv(ds, table, text, o = {}) {
      const s = this.findSet(ds);
      if (!s) return { error: "Not found: Dataset " + this.project + ":" + ds };
      if (!/^[A-Za-z0-9_]{1,1024}$/.test(table)) return { error: "Invalid table name: use letters, numbers and underscores only (no spaces, no -)." };
      if (this.findTable(s, table)) return { error: "Already Exists: Table " + this.project + ":" + s + "." + table };
      if (!o.autodetect) return { error: "No schema specified on job or table." };
      const t0 = performance.now();
      const all = parseCsv(text), head = all[0], rows = all.slice(1);
      const names = head.map(bqName);
      const sample = (c) => rows.slice(0, 500).map((r) => r[c]);
      const types = names.map((_, c) => detect(sample(c)));
      // A column that looks like a number in the first rows but not later is a string.
      types.forEach((ty, c) => { if (ty !== "STRING" && detect(rows.map((r) => r[c])) !== ty) types[c] = detect(rows.map((r) => r[c])); });
      const sqlType = { INTEGER: "INTEGER", FLOAT: "REAL", BOOLEAN: "INTEGER" };
      this.db.run("CREATE TABLE " + qid(s) + "." + qid(table) + " (" + names.map((n, c) => qid(n) + " " + (sqlType[types[c]] || "TEXT")).join(", ") + ")");
      const st = this.db.prepare("INSERT INTO " + qid(s) + "." + qid(table) + " VALUES (" + names.map(() => "?").join(",") + ")");
      this.db.run("BEGIN");
      for (const r of rows) {
        st.run(names.map((_, c) => {
          const v = r[c];
          if (v === undefined || v === "") return null;
          if (types[c] === "INTEGER" || types[c] === "FLOAT") return Number(v);
          if (types[c] === "BOOLEAN") return /^true$/i.test(v) ? 1 : 0;
          return v;
        }));
      }
      this.db.run("COMMIT");
      st.free();
      const info = this.describe(s, table, names.map((n, c) => ({ name: n, type: types[c] })));
      return { ok: true, rows: info.rows, schema: info.schema, bytes: info.bytes, ms: performance.now() - t0, header: head };
    }
    // Measure a table: its rows and the bytes of each column (BigQuery sizes:
    // a STRING is 2 bytes + its text, a number or a time 8 bytes, NULL 0).
    describe(ds, table, schema) {
      const T = qid(ds) + "." + qid(table);
      const sizes = schema.map((c) => c.type === "STRING"
        ? "COALESCE(SUM(CASE WHEN " + qid(c.name) + " IS NULL THEN 0 ELSE 2 + length(CAST(" + qid(c.name) + " AS BLOB)) END), 0)"
        : "COUNT(" + qid(c.name) + ") * 8");
      const r = this.db.exec("SELECT COUNT(*)" + (sizes.length ? ", " + sizes.join(", ") : "") + " FROM " + T)[0].values[0];
      const colBytes = {}; schema.forEach((c, i) => { colBytes[c.name.toLowerCase()] = r[i + 1]; });
      const info = { schema, rows: r[0], colBytes, bytes: r.slice(1).reduce((a, b) => a + b, 0), created: new Date() };
      this.sets[ds].tables[table] = info;
      return info;
    }
    preview(ds, table, n = 50) {
      const f = this.findTable(ds, table); if (!f) return null;
      const res = this.db.exec("SELECT * FROM " + qid(f.ds) + "." + qid(f.name) + " LIMIT " + n)[0];
      return { head: f.info.schema.map((c) => c.name), rows: res ? res.values.map((r) => r.map((v, i) => this.show(v, f.info.schema[i].type))) : [] };
    }
    show(v, type) {
      if (v === null || v === undefined) return "null";
      if (typeof v === "number") {
        if (type !== "FLOAT" && Number.isInteger(v)) return String(v);
        const x = Number(v.toPrecision(12));
        return Number.isInteger(x) ? x.toFixed(1) : String(x);
      }
      if (type === "TIMESTAMP" && TS.test(v)) return v.replace(/^(\S+ \d\d:\d\d)$/, "$1:00") + " UTC";
      return String(v);
    }
    // ---------- One statement ----------
    // Parse a statement: its kind, the table it creates, the tables it reads,
    // and the SQL for SQLite. Returns { error } on a BigQuery error.
    prepare(stmt, at, text) {
      const tk = tokenize(stmt);
      const err = (msg, tok, hint) => {
        const [line, col] = lineCol(text, at + (tok ? tok.p : 0));
        return { error: { msg: msg + (tok !== undefined ? " at [" + line + ":" + col + "]" : ""), hint, line, col } };
      };
      const bad = tk.find((x) => x.t === "bad");
      if (bad) return err(bad.v === "unclosed string" ? "Syntax error: Unclosed string literal" : "Syntax error: Unclosed identifier literal", bad,
        bad.v === "unclosed string" ? "A text value needs a quote ' at its start and at its end." : "A long name needs a backtick ` at its start and at its end.");
      let i = 0, kind = "select", target = null, replace = false, ifExists = false;
      const k0 = up(tk[0]);
      if (["INSERT", "UPDATE", "DELETE", "MERGE", "TRUNCATE"].includes(k0))
        return err("Billing has not been enabled for this project. Enable billing at https://console.cloud.google.com/billing. DML queries are not allowed in the free tier. Set up a billing account to remove this restriction.", undefined,
          "The free sandbox cannot change the rows of a table (" + k0 + "). Load a file into a table instead.");
      // CREATE [OR REPLACE] TABLE name AS SELECT …
      if (k0 === "CREATE") {
        i = 1;
        if (up(tk[1]) === "OR" && up(tk[2]) === "REPLACE") { replace = true; i = 3; }
        if (up(tk[i]) !== "TABLE") return err("Syntax error: Expected keyword TABLE but got " + (tk[i] ? '"' + tk[i].v + '"' : "end of statement"), tk[i] || tk[0],
          "This lab makes tables only: CREATE TABLE shop.new_name (column TYPE, …)");
        i++;
        if (up(tk[i]) === "IF" && up(tk[i + 1]) === "NOT" && up(tk[i + 2]) === "EXISTS") { ifExists = true; i += 3; }
        const nm = this.readName(tk, i); if (nm.error) return err(nm.error, tk[i], nm.hint);
        target = nm; i = nm.next;
        if (!this.findSet(target.ds)) return err("Not found: Dataset " + this.project + ":" + target.ds + " was not found in location US", tk[nm.at],
          "Create the dataset first, or check its name in the Explorer.");
        // CREATE TABLE name (column TYPE, …): an empty table with its columns.
        if (tk[i] && tk[i].v === "(") {
          const e = closing(tk, i);
          if (e < 0) return err("Syntax error: Unexpected end of script", tk[tk.length - 1], "The list of columns needs its closing bracket ).");
          if (e + 1 < tk.length) return err("Syntax error: Unexpected " + this.what(tk[e + 1]), tk[e + 1]);
          const cols = [];
          for (const [a, b] of splitArgs(tk, i + 1, e)) {
            if (a >= b) return err("Syntax error: Unexpected \",\"", tk[a - 1] || tk[i], "One column between two commas: its name, then its type.");
            const n = tk[a];
            if (n.t !== "w" && n.t !== "bt") return err("Syntax error: Unexpected " + this.what(n), n, "Each column: its name, then its type (STRING, INTEGER, FLOAT, DATE, TIMESTAMP).");
            const ty = tk[a + 1];
            if (!ty || ty.t !== "w") return err("Syntax error: Expected a type after the column " + n.v, ty || n, "Write the type after the name: " + n.v + " STRING.");
            const T = { STRING: "STRING", INT64: "INTEGER", INTEGER: "INTEGER", INT: "INTEGER", FLOAT64: "FLOAT", FLOAT: "FLOAT", NUMERIC: "NUMERIC",
              BIGNUMERIC: "BIGNUMERIC", BOOL: "BOOLEAN", BOOLEAN: "BOOLEAN", DATE: "DATE", TIMESTAMP: "TIMESTAMP", DATETIME: "DATETIME", TIME: "TIME" }[ty.v.toUpperCase()];
            if (!T) return err("Type not found: " + ty.v, ty, "BigQuery has its own types: STRING (text), INTEGER, FLOAT, DATE, TIMESTAMP.");
            if (cols.some((c) => c.name.toLowerCase() === n.v.toLowerCase())) return err("Duplicate column name: " + n.v, n, "Each column of a table has its own name.");
            if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(n.v)) return err("Invalid field name \"" + n.v + "\"", n, "A column name has letters, numbers and _ only: no spaces.");
            cols.push({ name: n.v, type: T });
          }
          if (!cols.length) return err("Syntax error: Unexpected \")\"", tk[e], "Write at least one column: its name, then its type.");
          return { kind: "define", target, cols, replace, ifExists, reads: [] };
        }
        if (up(tk[i]) !== "AS") return err("Syntax error: Expected \"(\" or keyword AS but got " + (tk[i] ? '"' + tk[i].v + '"' : "end of statement"), tk[i] || tk[tk.length - 1],
          "After the name of the new table: its columns in brackets, for example (name STRING, city STRING).");
        i++; kind = "create";
      } else if (k0 === "DROP") {
        if (up(tk[1]) !== "TABLE") return err("This simulator drops tables only: DROP TABLE shop.name", tk[1] || tk[0]);
        i = 2; if (up(tk[2]) === "IF" && up(tk[3]) === "EXISTS") { ifExists = true; i = 4; }
        const nm = this.readName(tk, i); if (nm.error) return err(nm.error, tk[i], nm.hint);
        if (nm.next < tk.length) return err("Syntax error: Unexpected " + this.what(tk[nm.next]), tk[nm.next]);
        if (!this.findTable(nm.ds, nm.table) && !ifExists) return err("Not found: Table " + this.project + ":" + nm.ds + "." + nm.table + " was not found in location US", tk[i]);
        return { kind: "drop", target: nm, ifExists, reads: [] };
      } else if (k0 !== "SELECT" && k0 !== "WITH" && !(tk[0].v === "(")) {
        return err("Syntax error: Unexpected " + this.what(tk[0]), tk[0], "A query starts with SELECT (or CREATE TABLE).");
      }
      const body = tk.slice(i);
      if (!body.length) return err("Syntax error: Unexpected end of statement", tk[tk.length - 1]);
      const tr = this.translate(body, err);
      if (tr.error) return tr;
      return Object.assign({ kind, target, replace, ifExists }, tr);
    }
    what(t) { return !t ? "end of script" : t.t === "w" ? (KEYWORDS.has(t.v.toUpperCase()) ? "keyword " + t.v.toUpperCase() : 'identifier "' + t.v + '"') : t.t === "str" ? "string literal" : '"' + t.v + '"'; }
    // A table name at tk[i]: `project.dataset.table`, `dataset.table`, dataset.table.
    readName(tk, i) {
      const t = tk[i];
      if (!t) return { error: "Syntax error: Unexpected end of statement" };
      let parts, next = i + 1;
      if (t.t === "bt") parts = t.v.split(".");
      else if (t.t === "w") {
        parts = [t.v];
        while (tk[next] && tk[next].v === "." && tk[next + 1] && (tk[next + 1].t === "w" || tk[next + 1].t === "bt")) { parts.push(...tk[next + 1].v.split(".")); next += 2; }
        if (tk[next] && tk[next].v === "-") return { error: 'Syntax error: Table name contains \'-\' character. It needs to be quoted with backticks', hint: "A name with - (big-data-lab) goes inside backticks: `big-data-lab.shop.sales`." };
      } else return { error: "Syntax error: Unexpected " + this.what(t) };
      if (parts.length === 3) {
        if (parts[0] !== this.project) return { error: "Not found: Dataset " + parts[0] + ":" + parts[1] + " was not found in location US", hint: "Your project is " + this.project + "." };
        parts = parts.slice(1);
      }
      if (parts.length === 1) return { error: 'Table "' + parts[0] + '" must be qualified with a dataset (e.g. dataset.table).', hint: "Write the dataset before the table, with a dot: shop." + parts[0] + "." };
      if (parts.length !== 2 || parts.some((x) => !x)) return { error: "Invalid table name: " + parts.join(".") };
      return { ds: parts[0], table: parts[1], next, at: i };
    }
    // BigQuery SQL (the SELECT part) → SQLite SQL, with the BigQuery checks.
    translate(tk, err) {
      const reads = [];
      const out = [];
      const s = (a, b) => this.emit(tk.slice(a, b), reads, err);
      // The checks of the top SELECT: every column grouped or aggregated.
      const g = this.groupCheck(tk, err);
      if (g && g.error) return g;
      const r = s(0, tk.length);
      if (r.error) return r;
      out.push(r.sql);
      // ORDER BY at depth 0 (not inside a subquery or a function).
      let d = 0, ordered = false;
      tk.forEach((t, j) => { if (t.v === "(" && t.t === "op") d++; else if (t.v === ")" && t.t === "op") d--; else if (d === 0 && up(t) === "ORDER" && up(tk[j + 1]) === "BY") ordered = true; });
      return { sql: out.join(" "), reads, ordered, tokens: tk };
    }
    // Emit tokens as SQLite text: names, strings, BigQuery functions.
    emit(tk, reads, err) {
      const out = [];
      for (let j = 0; j < tk.length; j++) {
        const t = tk[j], U = up(t), nx = tk[j + 1];
        if (t.t === "str") { out.push(qstr(t.v)); continue; }
        if (t.t === "num") { out.push(t.v); continue; }
        // A table name after FROM or JOIN.
        const prev = up(tk[j - 1]);
        if ((prev === "FROM" || prev === "JOIN") && (t.t === "bt" || t.t === "w" && nx && nx.v === ".")) {
          const nm = this.readName(tk, j);
          if (nm.error) return err(nm.error, t, nm.hint);
          const f = this.findTable(nm.ds, nm.table);
          if (!this.findSet(nm.ds)) return err("Not found: Dataset " + this.project + ":" + nm.ds + " was not found in location US", t,
            (() => { const c = closest(nm.ds, Object.keys(this.sets)); return c ? "Did you mean the dataset " + c + "?" : "Check the name of the dataset in the Explorer."; })());
          if (!f) {
            const c = closest(nm.table, Object.keys(this.sets[this.findSet(nm.ds)].tables));
            return err("Not found: Table " + this.project + ":" + this.findSet(nm.ds) + "." + nm.table + " was not found in location US", t,
              c ? "Did you mean the table " + c + "? Check the spelling, letter by letter." : "Check the name of the table in the Explorer.");
          }
          reads.push(f);
          out.push(qid(f.ds) + "." + qid(f.name));
          j = nm.next - 1; continue;
        }
        if ((prev === "FROM" || prev === "JOIN") && t.t === "w" && nx && nx.v === "-")
          return err("Syntax error: Table name contains '-' character. It needs to be quoted with backticks", t,
            "A name with - (big-data-lab) goes inside backticks: `big-data-lab.shop.sales`. The key ` is under Esc.");
        if ((prev === "FROM" || prev === "JOIN") && t.t === "w" && !KEYWORDS.has(U))
          return err('Table "' + t.v + '" must be qualified with a dataset (e.g. dataset.table).', t, "Write the dataset before the table, with a dot: shop." + t.v + ".");
        if (t.t === "bt") { out.push(col(t.v)); continue; }
        if (t.t === "op") { out.push(t.v === "/" ? "* 1.0 /" : t.v === "!=" ? "<>" : t.v); continue; }
        // Functions of BigQuery that SQLite does not have.
        if (t.t === "w" && nx && nx.v === "(") {
          const e = closing(tk, j + 1);
          if (e < 0) return err("Syntax error: Unexpected end of script", tk[tk.length - 1], "Every ( needs its ).");
          const inner = tk.slice(j + 2, e);
          const sub = (a) => { const r = this.emit(a, reads, err); return r.error ? r : r.sql; };
          let rep = null;
          if (U === "EXTRACT") {
            const part = up(inner[0]);
            if (up(inner[1]) !== "FROM") return err("Syntax error: Expected keyword FROM", inner[1] || t, "EXTRACT(YEAR FROM column)");
            const x = sub(inner.slice(2)); if (x.error) return x;
            const F = { YEAR: "%Y", MONTH: "%m", DAY: "%d", HOUR: "%H", MINUTE: "%M", SECOND: "%S" };
            if (F[part]) rep = "CAST(strftime('" + F[part] + "', " + x + ") AS INTEGER)";
            else if (part === "DAYOFWEEK") rep = "(CAST(strftime('%w', " + x + ") AS INTEGER) + 1)";
            else if (part === "QUARTER") rep = "((CAST(strftime('%m', " + x + ") AS INTEGER) + 2) / 3)";
            else if (part === "DATE") rep = "date(" + x + ")";
            else return err("A valid date part name is required but found " + (inner[0] ? inner[0].v : ""), inner[0] || t, "Use YEAR, MONTH, DAY, HOUR or DAYOFWEEK.");
          } else if (U === "COUNTIF") {
            const x = sub(inner); if (x.error) return x;
            rep = "SUM(CASE WHEN " + x + " THEN 1 ELSE 0 END)";
          } else if (U === "FORMAT_DATE" || U === "FORMAT_TIMESTAMP" || U === "FORMAT_DATETIME") {
            const a = splitArgs(inner, 0, inner.length);
            if (a.length < 2) return err("No matching signature for function " + U, t, U + "('%Y-%m', column)");
            const f = sub(inner.slice(a[0][0], a[0][1])), x = sub(inner.slice(a[1][0], a[1][1]));
            if (f.error) return f; if (x.error) return x;
            rep = "strftime(" + f + ", " + x + ")";
          } else if (U === "DATE_TRUNC" || U === "TIMESTAMP_TRUNC" || U === "DATETIME_TRUNC") {
            const a = splitArgs(inner, 0, inner.length);
            const x = sub(inner.slice(a[0][0], a[0][1])); if (x.error) return x;
            const part = a[1] ? up(inner[a[1][0]]) : null;
            const M = { MONTH: "'start of month'", YEAR: "'start of year'", DAY: "'start of day'" };
            if (!M[part]) return err("A valid date part name is required", t, U + "(column, MONTH)");
            rep = (U === "DATE_TRUNC" ? "date(" : "datetime(") + x + ", " + M[part] + ")";
          } else if (U === "SAFE_DIVIDE") {
            const a = splitArgs(inner, 0, inner.length);
            const x = sub(inner.slice(a[0][0], a[0][1])), y = a[1] ? sub(inner.slice(a[1][0], a[1][1])) : { error: 1 };
            if (x.error || y.error) return x.error ? x : err("No matching signature for function SAFE_DIVIDE", t);
            rep = "(CASE WHEN (" + y + ") = 0 THEN NULL ELSE (" + x + ") * 1.0 / (" + y + ") END)";
          } else if (U === "CAST") {
            const asAt = inner.findIndex((x) => up(x) === "AS");
            if (asAt > 0) {
              const x = sub(inner.slice(0, asAt)); if (x.error) return x;
              const ty = up(inner[asAt + 1]);
              const T = { STRING: "TEXT", INT64: "INTEGER", INTEGER: "INTEGER", FLOAT64: "REAL", FLOAT: "REAL", NUMERIC: "REAL", DATE: "TEXT", TIMESTAMP: "TEXT" };
              rep = (ty === "DATE" ? "date(" + x + ")" : "CAST(" + x + " AS " + (T[ty] || "TEXT") + ")");
            }
          }
          if (rep !== null) { out.push(rep); j = e; continue; }
        }
        out.push(t.t === "w" && !KEYWORDS.has(U) && !(nx && nx.v === "(") && !(tk[j - 1] && tk[j - 1].v === ".") && !(nx && nx.v === ".") ? col(t.v) : t.v);
      }
      return { sql: out.join(" ") };
    }
    // BigQuery: in a query with GROUP BY or an aggregate (COUNT, SUM …), every
    // column of the SELECT list is grouped or inside an aggregate.
    groupCheck(tk, err) {
      // The top SELECT … FROM, and the GROUP BY list (depth 0).
      let d = 0, sel = -1, from = -1, gb = -1, gbEnd = tk.length;
      tk.forEach((t, j) => {
        if (t.t === "op" && t.v === "(") d++; else if (t.t === "op" && t.v === ")") d--;
        else if (d === 0) {
          const U = up(t);
          if (U === "SELECT" && sel < 0) sel = j;
          else if (U === "FROM" && sel >= 0 && from < 0) from = j;
          else if (U === "GROUP" && up(tk[j + 1]) === "BY" && gb < 0) gb = j + 2;
          else if (gb >= 0 && gbEnd === tk.length && j > gb && ["HAVING", "ORDER", "LIMIT", "UNION", "QUALIFY", "WINDOW"].includes(U)) gbEnd = j;
        }
      });
      if (sel < 0) return null;
      const end = from < 0 ? (gb >= 0 ? gb - 2 : tk.length) : from;
      let start = sel + 1; if (up(tk[start]) === "DISTINCT") start++;
      const items = splitArgs(tk, start, end).map(([a, b]) => {
        let e = b, alias = null;
        if (b - a >= 2 && up(tk[b - 2]) === "AS" && tk[b - 1].t !== "op") { alias = tk[b - 1].v; e = b - 2; }
        else if (b - a >= 2 && (tk[b - 1].t === "w" || tk[b - 1].t === "bt") && !KEYWORDS.has(up(tk[b - 1]) || "") && tk[b - 2].t !== "op" && tk[b - 2].v !== ".") { alias = tk[b - 1].v; e = b - 1; }
        return { a, e, alias, toks: tk.slice(a, e) };
      });
      const hasAgg = (toks) => toks.some((t, j) => t.t === "w" && AGG.has(t.v.toUpperCase()) && toks[j + 1] && toks[j + 1].v === "(");
      const anyAgg = items.some((it) => hasAgg(it.toks));
      if (gb < 0 && !anyAgg) return null;
      const key = (toks) => toks.map((t) => (t.t === "w" || t.t === "bt" ? t.v.toLowerCase() : t.v)).join(" ");
      const groups = gb < 0 ? [] : splitArgs(tk, gb, gbEnd).map(([a, b]) => tk.slice(a, b));
      const gkeys = new Set(groups.map(key));
      groups.forEach((g) => { if (g.length === 1 && g[0].t === "num") { const it = items[Number(g[0].v) - 1]; if (it) gkeys.add(key(it.toks)); } });
      for (const it of items) {
        if (hasAgg(it.toks)) continue;
        if (it.toks.length === 1 && it.toks[0].v === "*") {
          if (gb >= 0 || anyAgg) return err("SELECT * expression references columns which are neither grouped nor aggregated", it.toks[0],
            "With GROUP BY or COUNT, name the columns: the grouped column and the counts, not *.");
          continue;
        }
        const ok = gkeys.has(key(it.toks)) || it.alias && gkeys.has(it.alias.toLowerCase());
        const col = it.toks.find((t) => (t.t === "w" && !KEYWORDS.has(t.v.toUpperCase()) && !(tk[tk.indexOf(t) + 1] && tk[tk.indexOf(t) + 1].v === "(")) || t.t === "bt");
        if (!ok && col) {
          return err("SELECT list expression references column " + col.v + " which is neither grouped nor aggregated", col,
            gb < 0 ? "COUNT gives one number for all the rows, so the column " + col.v + " has no single value. Add GROUP BY " + col.v + ": one row for each " + col.v + "."
              : "Each row of the answer is one group. Add " + col.v + " to GROUP BY, or put it inside COUNT, SUM, MIN or MAX.");
        }
      }
      return null;
    }
    // The bytes that a statement reads: the columns it names, of the tables it reads.
    bytesOf(p) {
      let n = 0;
      const toks = p.tokens || [];
      for (const f of p.reads) {
        const cols = f.info.schema.map((c) => c.name.toLowerCase());
        const used = new Set();
        toks.forEach((t, j) => {
          // * = all the columns after SELECT, a comma, DISTINCT or "t." (not COUNT(*), not a × b).
          const pv = toks[j - 1];
          if (t.t === "op" && t.v === "*" && pv && (["SELECT", "DISTINCT"].includes(up(pv)) || pv.v === "," || pv.v === ".")) cols.forEach((c) => used.add(c));
          if ((t.t === "w" || t.t === "bt") && cols.includes(t.v.toLowerCase())) used.add(t.v.toLowerCase());
        });
        used.forEach((c) => { n += f.info.colBytes[c] || 0; });
      }
      return n;
    }
    // ---------- The editor ----------
    // Check the text of the editor without running it (the estimate of BigQuery).
    check(text) {
      const st = statements(text);
      if (!st.length) return { ok: false, empty: true };
      let bytes = 0, kind = "select";
      for (const s of st) {
        const p = this.prepare(s.sql, s.at, text);
        if (p.error) return { ok: false, error: p.error };
        kind = p.kind;
        if (p.kind === "drop" || p.kind === "define") continue;
        try { this.db.prepare(p.sql).free(); } catch (e) { return { ok: false, error: this.sqliteError(e, s, text, p) }; }
        bytes += this.bytesOf(p);
      }
      return { ok: true, bytes, kind, many: st.length > 1 };
    }
    // Run the text of the editor: every statement, the result of the last one.
    run(text) {
      const t0 = performance.now();
      const st = statements(text);
      if (!st.length) return { error: { msg: "The editor is empty.", hint: "Type a query first." } };
      let res = null, bytes = 0;
      for (const s of st) {
        const p = this.prepare(s.sql, s.at, text);
        if (p.error) return { error: p.error };
        if (p.kind === "drop") {
          const f = this.findTable(p.target.ds, p.target.table);
          if (f) { this.db.run("DROP TABLE " + qid(f.ds) + "." + qid(f.name)); delete this.sets[f.ds].tables[f.name]; }
          res = { kind: "drop", target: (f ? f.ds + "." + f.name : p.target.ds + "." + p.target.table) };
          continue;
        }
        if (p.kind === "define") {
          const ds = this.findSet(p.target.ds), old = this.findTable(ds, p.target.table);
          if (old && p.ifExists && !p.replace) { res = { kind: "create", created: ds + "." + old.name, skipped: true }; continue; }
          if (old && !p.replace) return { error: { msg: "Already Exists: Table " + this.project + ":" + ds + "." + old.name, hint: "This table is already there. Choose a new name." } };
          if (!/^[A-Za-z0-9_]{1,1024}$/.test(p.target.table)) return { error: { msg: "Invalid table name: " + p.target.table, hint: "Use letters, numbers and _ only." } };
          const name = old ? old.name : p.target.table;
          if (old) { this.db.run("DROP TABLE " + qid(ds) + "." + qid(old.name)); delete this.sets[ds].tables[old.name]; }
          const SQ = { INTEGER: "INTEGER", FLOAT: "REAL", NUMERIC: "REAL", BIGNUMERIC: "REAL", BOOLEAN: "INTEGER" };
          this.db.run("CREATE TABLE " + qid(ds) + "." + qid(name) + " (" + p.cols.map((c) => qid(c.name) + " " + (SQ[c.type] || "TEXT")).join(", ") + ")");
          const info = this.describe(ds, name, p.cols);
          res = { kind: "create", created: ds + "." + name, replaced: !!old, rows: info.rows };
          continue;
        }
        bytes += this.bytesOf(p);
        if (p.kind === "create") {
          const ds = this.findSet(p.target.ds), old = this.findTable(ds, p.target.table);
          if (old && p.ifExists && !p.replace) { res = { kind: "create", created: ds + "." + old.name, skipped: true }; continue; }
          if (old && !p.replace) return { error: { msg: "Already Exists: Table " + this.project + ":" + ds + "." + old.name, hint: "This table is already there. Choose a new name, or write CREATE OR REPLACE TABLE to make it again." } };
          const name = old ? old.name : p.target.table;
          if (!/^[A-Za-z0-9_]{1,1024}$/.test(name)) return { error: { msg: "Invalid table name: " + name, hint: "Use letters, numbers and _ only." } };
          let colsTypes;
          try {
            const probe = this.db.prepare(p.sql);
            colsTypes = this.resultNames(probe.getColumnNames());
            probe.free();
            this.db.run("DROP TABLE IF EXISTS " + qid(ds) + "." + qid("__new"));
            this.db.run("CREATE TABLE " + qid(ds) + "." + qid("__new") + " AS " + p.sql);
          } catch (e) { return { error: this.sqliteError(e, s, text, p) }; }
          if (old) { this.db.run("DROP TABLE " + qid(ds) + "." + qid(old.name)); delete this.sets[ds].tables[old.name]; }
          this.db.run("ALTER TABLE " + qid(ds) + "." + qid("__new") + " RENAME TO " + qid(name));
          // Rename the columns to their BigQuery names (f0_ for an expression without a name).
          const real = this.db.exec("PRAGMA " + qid(ds) + ".table_info(" + qid(name) + ")")[0].values.map((r) => r[1]);
          real.forEach((c, i) => { if (c !== colsTypes[i]) this.db.run("ALTER TABLE " + qid(ds) + "." + qid(name) + " RENAME COLUMN " + qid(c) + " TO " + qid(colsTypes[i])); });
          const schema = colsTypes.map((c) => ({ name: c, type: this.typeOf(ds, name, c, p.reads) }));
          const info = this.describe(ds, name, schema);
          res = { kind: "create", created: ds + "." + name, replaced: !!old, rows: info.rows };
          continue;
        }
        let r;
        try { r = this.db.exec(p.sql)[0]; } catch (e) { return { error: this.sqliteError(e, s, text, p) }; }
        let head, rows;
        if (r) { head = this.resultNames(r.columns); rows = r.values; }
        else {
          const probe = this.db.prepare(p.sql); head = this.resultNames(probe.getColumnNames()); probe.free(); rows = [];
        }
        let shuffled = false;
        if (!p.ordered && rows.length > 1) {
          for (let i = rows.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [rows[i], rows[j]] = [rows[j], rows[i]]; }
          shuffled = true;
        }
        const known = {};
        p.reads.forEach((f) => f.info.schema.forEach((c) => { known[c.name.toLowerCase()] = c.type; }));
        const types = head.map((h, c) => {
          if (known[h.toLowerCase()]) return known[h.toLowerCase()];
          const v = rows.find((row) => row[c] !== null);
          return !v ? "STRING" : typeof v[c] === "number" ? (rows.some((row) => typeof row[c] === "number" && !Number.isInteger(row[c])) ? "FLOAT" : "INTEGER") : "STRING";
        });
        res = { kind: "select", head, total: rows.length, rows: rows.map((row) => row.map((v, c) => this.show(v, types[c]))), shuffled };
      }
      return Object.assign(res, { bytes, ms: performance.now() - t0 });
    }
    // The names of the columns of a result, as BigQuery names them.
    resultNames(cols) {
      let k = 0;
      return cols.map((c) => (/^[A-Za-z_][A-Za-z0-9_]*$/.test(c) ? c : "f" + k++ + "_"));
    }
    typeOf(ds, table, col, reads) {
      for (const f of reads) { const c = f.info.schema.find((x) => x.name.toLowerCase() === col.toLowerCase()); if (c) return c.type; }
      const r = this.db.exec("SELECT typeof(" + qid(col) + "), " + qid(col) + " FROM " + qid(ds) + "." + qid(table) + " WHERE " + qid(col) + " IS NOT NULL LIMIT 200")[0];
      if (!r) return "STRING";
      const ts = r.values.map((v) => v[0]);
      if (ts.every((x) => x === "integer")) return "INTEGER";
      if (ts.every((x) => x === "integer" || x === "real")) return "FLOAT";
      if (r.values.every((v) => TS.test(String(v[1])))) return "TIMESTAMP";
      if (r.values.every((v) => /^\d{4}-\d{2}-\d{2}$/.test(String(v[1])))) return "DATE";
      return "STRING";
    }
    // An error of SQLite → the error that BigQuery would give.
    sqliteError(e, s, text, p) {
      const m = String(e.message || e);
      const at = (word) => {
        const toks = tokenize(s.sql);
        const t = toks.find((x) => x.v.toLowerCase() === String(word).toLowerCase());
        const [line, col] = lineCol(text, s.at + (t ? t.p : 0));
        return { tag: " at [" + line + ":" + col + "]", line, col };
      };
      let r;
      if ((r = m.match(/no such column: (?:\S+\.)?"?([^"\s]+)"?/))) {
        const name = r[1], cols = [].concat(...(p.reads || []).map((f) => f.info.schema.map((c) => c.name)));
        const c = closest(name, cols), w = at(name);
        return { msg: "Unrecognized name: " + name + (c ? "; Did you mean " + c + "?" : "") + w.tag, line: w.line, col: w.col,
          hint: c ? "There is no column " + name + ". The column is called " + c + " (see Schema)."
            : new RegExp("=\\s*" + name + "\\b").test(s.sql) ? "A text value needs quotes: '" + name + "'. Without them, BigQuery looks for a column " + name + "."
            : "There is no column " + name + " in this table. See its columns in Schema." };
      }
      if ((r = m.match(/no such function: (\w+)/))) { const w = at(r[1]); return { msg: "Function not found: " + r[1] + w.tag, line: w.line, col: w.col, hint: "Check the name of the function, letter by letter." }; }
      if ((r = m.match(/near "([^"]+)": syntax error/))) {
        r[1] = r[1].replace(/^\[|\]$/g, "");
        const w = at(r[1]), kw = KEYWORDS.has(r[1].toUpperCase());
        return { msg: "Syntax error: Unexpected " + (kw ? "keyword " + r[1].toUpperCase() : /^\W$/.test(r[1]) ? '"' + r[1] + '"' : 'identifier "' + r[1] + '"') + w.tag, line: w.line, col: w.col,
          hint: "Look just before this place: a missing comma, a word spelled wrong, or a line in the wrong order (SELECT, FROM, WHERE, GROUP BY, ORDER BY)." };
      }
      if (/incomplete input/.test(m)) return { msg: "Syntax error: Unexpected end of script", hint: "The query stops too early: something is missing at the end." };
      if ((r = m.match(/misuse of aggregate(?: function)? (\w+)/))) { const w = at(r[1]); return { msg: "Aggregate function " + r[1].toUpperCase() + " not allowed in WHERE clause" + w.tag, line: w.line, col: w.col, hint: "WHERE filters single rows. To filter groups by their COUNT or SUM, use HAVING after GROUP BY." }; }
      if (/wrong number of arguments/.test(m)) return { msg: "No matching signature for function: " + m.replace(/.*function /, ""), hint: "Check the values inside the brackets of the function." };
      return { msg: "Error: " + m, hint: "Compare the query with the worksheet, sign by sign." };
    }
  }

  async function create(o = {}) {
    const SQL = await window.initSqlJs({ locateFile: (f) => (o.vendor || "") + f });
    return new Engine(SQL, o);
  }
  window.BQEngine = { create, fmtBytes, parseCsv, statements };
})();
