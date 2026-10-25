// A small spreadsheet for the Excel simulators: cells, formulas, relative and
// absolute references, copy down, number formats and a few functions
// (SUM, AVERAGE, MAX, MIN, COUNT, ROUND, IF, SUMIF, COUNTIF, AVERAGEIF).
// It works like Excel for what the lessons teach; it is not Excel.
//
//   const s = MiniSheet.create(element, { rows, cols, data: { A1: "Item", B2: 3, C2: "=B2*2" },
//              formats: { C2: "0.00" }, locked: ["A1"], widths: { A: 130 }, tasks: [...] });
//   s.value("C2"), s.raw("C2"), s.set("C2", "=B2*3"), s.select("C2")
// A task is { q, check(s) -> true/false, ok } and is checked after every change.
(() => {
  const COL = (i) => String.fromCharCode(65 + i);
  const IDX = (c) => c.charCodeAt(0) - 65;
  const ERR = (e) => ({ err: e });
  const isErr = (v) => v && typeof v === "object" && "err" in v;

  function tokenize(src) {
    const t = [], re = /\s*(\$?[A-Z]\$?\d+(?::\$?[A-Z]\$?\d+)?|\d+(?:\.\d+)?%?|"[^"]*"|[A-Z]+(?=\()|<=|>=|<>|[-+*/^(),:<>=&])/gy;
    let m, pos = 0;
    while (pos < src.length) {
      re.lastIndex = pos; m = re.exec(src);
      if (!m) { if (/\s/.test(src[pos])) { pos++; continue; } throw "#NAME?"; }
      t.push(m[1]); pos = re.lastIndex;
    }
    return t;
  }

  function parse(src) {
    const T = tokenize(src.replace(/"[^"]*"|[^"]+/g, (m) => (m[0] === '"' ? m : m.toUpperCase())));
    let i = 0;
    const peek = () => T[i], eat = (x) => { if (T[i] !== x) throw "#VALUE!"; i++; };
    function cmp() {
      let a = add();
      while (["=", "<", ">", "<=", ">=", "<>"].includes(peek())) { const op = T[i++]; const b = add(); a = { op, a, b }; }
      return a;
    }
    function add() { let a = mul(); while (peek() === "+" || peek() === "-") { const op = T[i++]; a = { op, a, b: mul() }; } return a; }
    function mul() { let a = pow(); while (peek() === "*" || peek() === "/") { const op = T[i++]; a = { op, a, b: pow() }; } return a; }
    function pow() { let a = unary(); while (peek() === "^") { i++; a = { op: "^", a, b: unary() }; } return a; }
    function unary() { if (peek() === "-") { i++; return { op: "neg", a: unary() }; } if (peek() === "+") { i++; return unary(); } return atom(); }
    function atom() {
      const x = T[i++];
      if (x === undefined) throw "#VALUE!";
      if (x === "(") { const e = cmp(); eat(")"); return e; }
      if (/^\d/.test(x)) return { num: x.endsWith("%") ? parseFloat(x) / 100 : parseFloat(x) };
      if (x[0] === '"') return { str: x.slice(1, -1) };
      if (/^\$?[A-Z]\$?\d+:/.test(x)) { const [p, q] = x.split(":"); return { range: [p.replace(/\$/g, ""), q.replace(/\$/g, "")] }; }
      if (/^\$?[A-Z]\$?\d+$/.test(x)) return { ref: x.replace(/\$/g, "") };
      if (/^[A-Z]+$/.test(x)) {
        eat("("); const args = [];
        if (peek() !== ")") { args.push(cmp()); while (peek() === ",") { i++; args.push(cmp()); } }
        eat(")"); return { fn: x, args };
      }
      throw "#NAME?";
    }
    const e = cmp();
    if (i !== T.length) throw "#VALUE!";
    return e;
  }

  // Move the relative parts of every reference by (dr rows, dc columns), as Excel does when copying.
  function shift(formula, dr, dc) {
    return formula.replace(/(\$?)([A-Z])(\$?)(\d+)/g, (m, cAbs, c, rAbs, r, off, str) => {
      if (/[A-Z]/.test(str[off - 1] || "")) return m;   // part of a function name
      const nc = cAbs ? c : COL(IDX(c) + dc), nr = rAbs ? +r : +r + dr;
      return nr < 1 || IDX(nc) < 0 ? "#REF!" : `${cAbs}${nc}${rAbs}${nr}`;
    });
  }

  function fmt(v, f) {
    if (isErr(v)) return v.err;
    if (v === "" || v === null || v === undefined) return "";
    if (typeof v === "boolean") return v ? "TRUE" : "FALSE";
    if (typeof v !== "number") return String(v);
    if (f === "%") return (Math.round(v * 1000) / 10).toString() + "%";
    if (f === "0.00") return v.toFixed(2);
    if (f === "0") return Math.round(v).toString();
    if (f === "JOD") return v.toFixed(2) + " JD";
    return String(Math.round(v * 1e6) / 1e6);
  }

  function create(el, o) {
    const S = { data: Object.assign({}, o.data || {}), formats: Object.assign({}, o.formats || {}), sel: o.select || "A1" };
    const R = o.rows || 8, C = o.cols || 5, locked = new Set(o.locked || []);
    let stack = new Set();
    S.raw = (a) => (S.data[a] === undefined ? "" : String(S.data[a]));
    S.formula = (a) => S.raw(a).replace(/\s+/g, "").toUpperCase();
    function val(a) {
      const r = S.data[a];
      if (r === undefined || r === "") return "";
      if (typeof r === "number") return r;
      const s = String(r);
      if (s[0] !== "=") return isNaN(+s) || s.trim() === "" ? s : +s;
      if (stack.has(a)) return ERR("#REF!");
      stack.add(a);
      try { return ev(parse(s.slice(1))); } catch (e) { return ERR(typeof e === "string" ? e : "#VALUE!"); } finally { stack.delete(a); }
    }
    S.value = (a) => { stack = new Set(); return val(a); };
    const cells = (rg) => { const out = []; const c0 = IDX(rg[0][0]), c1 = IDX(rg[1][0]), r0 = +rg[0].slice(1), r1 = +rg[1].slice(1); for (let r = Math.min(r0, r1); r <= Math.max(r0, r1); r++) for (let c = Math.min(c0, c1); c <= Math.max(c0, c1); c++) out.push(COL(c) + r); return out; };
    const num = (v) => { if (isErr(v)) throw v.err; if (v === "") return 0; if (typeof v === "boolean") return v ? 1 : 0; if (typeof v !== "number") throw "#VALUE!"; return v; };
    function flat(args) { const out = []; args.forEach((a) => { if (a.range) cells(a.range).forEach((c) => out.push(val(c))); else out.push(ev(a)); }); return out; }
    const nums = (args) => flat(args).filter((v) => { if (isErr(v)) throw v.err; return typeof v === "number"; });
    function crit(c) {
      const m = String(c).match(/^(<=|>=|<>|<|>|=)?(.*)$/), op = m[1] || "=", x = isNaN(+m[2]) || m[2] === "" ? m[2].toUpperCase() : +m[2];
      return (v) => { const y = typeof x === "number" ? v : String(v).toUpperCase(); return op === "=" ? y === x : op === "<>" ? y !== x : op === "<" ? y < x : op === ">" ? y > x : op === "<=" ? y <= x : y >= x; };
    }
    const FN = {
      SUM: (a) => nums(a).reduce((s, x) => s + x, 0),
      AVERAGE: (a) => { const n = nums(a); if (!n.length) throw "#DIV/0!"; return n.reduce((s, x) => s + x, 0) / n.length; },
      MAX: (a) => { const n = nums(a); return n.length ? Math.max(...n) : 0; },
      MIN: (a) => { const n = nums(a); return n.length ? Math.min(...n) : 0; },
      COUNT: (a) => nums(a).length,
      ROUND: (a) => { const k = Math.pow(10, num(ev(a[1] || { num: 0 }))); return Math.round(num(ev(a[0])) * k) / k; },
      IF: (a) => { const c = ev(a[0]); if (isErr(c)) throw c.err; return c ? ev(a[1]) : a[2] ? ev(a[2]) : false; },
      SUMIF: (a) => { const rc = cells(a[0].range), test = crit(ev(a[1])), sc = a[2] ? cells(a[2].range) : rc; return rc.reduce((s, c, k) => s + (test(val(c)) ? num(val(sc[k])) : 0), 0); },
      COUNTIF: (a) => { const test = crit(ev(a[1])); return cells(a[0].range).filter((c) => test(val(c))).length; },
      AVERAGEIF: (a) => { const rc = cells(a[0].range), test = crit(ev(a[1])), sc = a[2] ? cells(a[2].range) : rc; const v = rc.map((c, k) => (test(val(c)) ? num(val(sc[k])) : null)).filter((x) => x !== null); if (!v.length) throw "#DIV/0!"; return v.reduce((s, x) => s + x, 0) / v.length; },
    };
    function ev(e) {
      if ("num" in e) return e.num;
      if ("str" in e) return e.str;
      if (e.ref) { if (IDX(e.ref[0]) >= C || +e.ref.slice(1) > R) throw "#REF!"; const v = val(e.ref); if (isErr(v)) throw v.err; return v; }
      if (e.range) throw "#VALUE!";
      if (e.fn) { if (!FN[e.fn]) throw "#NAME?"; return FN[e.fn](e.args); }
      if (e.op === "neg") return -num(ev(e.a));
      const a = ev(e.a), b = ev(e.b);
      switch (e.op) {
        case "+": return num(a) + num(b);
        case "-": return num(a) - num(b);
        case "*": return num(a) * num(b);
        case "/": if (num(b) === 0) throw "#DIV/0!"; return num(a) / num(b);
        case "^": return Math.pow(num(a), num(b));
        case "=": return a === b; case "<>": return a !== b;
        case "<": return a < b; case ">": return a > b; case "<=": return a <= b; case ">=": return a >= b;
      }
      throw "#VALUE!";
    }

    // The look: a name box and a formula bar, then the grid.
    el.classList.add("msheet");
    el.innerHTML = `<div class="ms-bar"><span class="ms-name"></span><span class="ms-fx">fx</span><input class="ms-in" type="text" autocomplete="off" spellcheck="false" aria-label="Formula bar"><button type="button" class="ms-ok">Enter</button></div><div class="ms-wrap"><table class="ms-grid"></table></div><div class="ms-tools"></div>`;
    const tbl = el.querySelector(".ms-grid"), inp = el.querySelector(".ms-in"), nameBox = el.querySelector(".ms-name");
    let html = "<tr><th></th>" + Array.from({ length: C }, (_, c) => `<th style="${o.widths && o.widths[COL(c)] ? "min-width:" + o.widths[COL(c)] + "px" : ""}">${COL(c)}</th>`).join("") + "</tr>";
    for (let r = 1; r <= R; r++) html += `<tr><th>${r}</th>` + Array.from({ length: C }, (_, c) => `<td data-a="${COL(c)}${r}"></td>`).join("") + "</tr>";
    tbl.innerHTML = html;
    tbl.addEventListener("click", (e) => { const td = e.target.closest("td"); if (td) S.select(td.dataset.a); });
    S.select = (a) => { S.sel = a; nameBox.textContent = a; inp.value = S.raw(a); inp.readOnly = locked.has(a); render(); };
    S.set = (a, v) => {
      if (locked.has(a)) { o.say && o.say("This cell is part of the data. Choose another cell."); return; }
      const t = String(v).trim();
      if (t === "") delete S.data[a]; else S.data[a] = t[0] === "=" ? t : isNaN(+t) ? t : +t;
      render(); check(); o.onChange && o.onChange(S);
    };
    inp.addEventListener("keydown", (e) => { if (e.key === "Enter") { S.set(S.sel, inp.value); const r = +S.sel.slice(1); if (r < R) S.select(S.sel[0] + (r + 1)); } });
    el.querySelector(".ms-ok").addEventListener("click", () => S.set(S.sel, inp.value));
    // Copy the selected cell down as far as the column on its left has data, like a
    // double-click on the fill handle in Excel.
    S.copyDown = () => {
      const a = S.sel, f = S.raw(a); if (!f) { o.say && o.say("The selected cell is empty: there is nothing to copy."); return; }
      const nb = a[0] === "A" ? "B" : COL(IDX(a[0]) - 1);
      let last = +a.slice(1); while (last < R && S.raw(nb + (last + 1)) !== "") last++;
      for (let r = +a.slice(1) + 1; r <= last; r++) if (!locked.has(a[0] + r)) S.data[a[0] + r] = f[0] === "=" ? shift(f, r - +a.slice(1), 0) : f;
      if (S.formats[a]) for (let r = +a.slice(1) + 1; r <= last; r++) S.formats[a[0] + r] = S.formats[a];
      render(); check(); o.onChange && o.onChange(S);
    };
    S.format = (a, f) => { S.formats[a] = f; render(); check(); };
    function render() {
      tbl.querySelectorAll("td").forEach((td) => {
        const a = td.dataset.a, v = S.value(a);
        td.textContent = fmt(v, S.formats[a]);
        td.className = (a === S.sel ? "sel " : "") + (typeof v === "number" ? "num " : "") + (isErr(v) ? "err " : "") + (locked.has(a) ? "lk " : "") + (S.raw(a)[0] === "=" ? "fx " : "") + (o.bold && o.bold.includes(a) ? "b" : "");
      });
    }
    // Tasks, one after the other.
    let ti = 0;
    const tools = el.querySelector(".ms-tools");
    function check() {
      if (!o.tasks || ti >= o.tasks.length) return;
      const t = o.tasks[ti];
      let ok = false; try { ok = !!t.check(S); } catch (_) { ok = false; }
      if (ok) { ti++; o.onTask && o.onTask(t, ti, o.tasks.length); showTask(); }
    }
    function showTask() { if (o.taskEl) o.taskEl.innerHTML = o.tasks && ti < o.tasks.length ? `<b>Task ${ti + 1} / ${o.tasks.length}:</b> ${o.tasks[ti].q}` : o.tasks ? "🎉 All tasks are done. Try your own formulas." : ""; }
    S.tools = tools;
    S.render = render; S.check = check;
    S.taskIndex = () => ti;
    S.shift = shift;
    S.select(S.sel); showTask();
    return S;
  }

  const css = document.createElement("style");
  css.textContent = `
    .msheet { border: 1.5px solid #c3d9c7; border-radius: 10px; overflow: hidden; background: #fff; }
    .msheet .ms-bar { display: flex; align-items: center; gap: 6px; padding: 6px; background: #f1f8f3; border-bottom: 1px solid #c3d9c7; }
    .msheet .ms-name { min-width: 3em; padding: 4px 6px; background: #fff; border: 1px solid #c3d9c7; border-radius: 6px; font-weight: 800; text-align: center; }
    .msheet .ms-fx { font-style: italic; font-weight: 800; color: #217346; }
    .msheet .ms-in { flex: 1; min-width: 0; font: inherit; font-weight: 700; padding: 5px 8px; border: 1px solid #c3d9c7; border-radius: 6px; }
    .msheet .ms-ok { padding: 5px 10px; }
    .msheet .ms-wrap { overflow-x: auto; }
    .msheet table { border-collapse: collapse; width: 100%; font-variant-numeric: tabular-nums; font-size: .92rem; }
    .msheet th { background: #f1f3f5; color: #495057; font-weight: 700; padding: 3px 6px; border: 1px solid #dee2e6; font-size: .8rem; }
    .msheet td { border: 1px solid #e9ecef; padding: 5px 7px; min-width: 64px; height: 1.6em; cursor: pointer; white-space: nowrap; }
    .msheet td.num { text-align: right; }
    .msheet td.lk { background: #fbfcfb; }
    .msheet td.b { font-weight: 800; }
    .msheet td.fx { color: #1864ab; }
    .msheet td.err { color: #c92a2a; font-weight: 800; }
    .msheet td.sel { outline: 2.5px solid #217346; outline-offset: -2px; }
    .msheet .ms-tools { display: flex; flex-wrap: wrap; gap: 6px; padding: 6px; border-top: 1px solid #e9ecef; }
    .msheet .ms-tools:empty { display: none; }
    .msheet .ms-tools button { padding: 5px 10px; font-size: .9rem; }
  `;
  document.head.appendChild(css);
  window.MiniSheet = { create, shift, fmt };
})();
