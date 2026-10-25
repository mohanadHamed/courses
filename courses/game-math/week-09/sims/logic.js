// A small parser for logical expressions, for the logic simulators of lectures 17-18.
// Variables: single small letters (p, q, r). Operators: ! (NOT), && (AND), ^ (XOR), || (OR),
// -> (IF-THEN), brackets. The symbols ¬ ∧ ∨ ⊕ → are accepted too. Precedence: ! > && > ^ > || > ->.
//   const e = LG.parse("p && (q || !r)"); e.vars -> ["p","q","r"]; e.eval({p:1,q:0,r:1}) -> true
//   LG.rows(["p","q"]) -> [{p:1,q:1},{p:1,q:0},{p:0,q:1},{p:0,q:0}]
(function () {
  function tokens(src) {
    const s = src.replace(/¬/g, "!").replace(/∧/g, "&&").replace(/∨/g, "||").replace(/⊕/g, "^").replace(/→/g, "->").replace(/\band\b/gi, "&&").replace(/\bor\b/gi, "||").replace(/\bnot\b/gi, "!");
    const t = [], re = /\s*(&&|\|\||->|[!^()]|[a-z])/y;
    let i = 0;
    while (i < s.length) {
      if (/\s/.test(s[i])) { i++; continue; }
      re.lastIndex = i; const m = re.exec(s);
      if (!m) throw new Error("I cannot read “" + s.slice(i, i + 3) + "”");
      t.push(m[1]); i = re.lastIndex;
    }
    return t;
  }
  function parse(src) {
    const T = tokens(src); let i = 0; const vars = new Set();
    const peek = () => T[i], eat = (x) => { if (T[i] !== x) throw new Error(x === ")" ? "a bracket ) is missing" : "unexpected “" + (T[i] || "end") + "”"); i++; };
    function imp() { const a = or(); if (peek() === "->") { i++; const b = imp(); return (v) => !a(v) || b(v); } return a; }
    function or() { let a = xor(); while (peek() === "||") { i++; const l = a, r = xor(); a = (v) => l(v) || r(v); } return a; }
    function xor() { let a = and(); while (peek() === "^") { i++; const l = a, r = and(); a = (v) => l(v) !== r(v); } return a; }
    function and() { let a = not(); while (peek() === "&&") { i++; const l = a, r = not(); a = (v) => l(v) && r(v); } return a; }
    function not() { if (peek() === "!") { i++; const a = not(); return (v) => !a(v); } return atom(); }
    function atom() {
      const t = peek();
      if (t === "(") { i++; const a = imp(); eat(")"); return a; }
      if (t && /^[a-z]$/.test(t)) { i++; vars.add(t); return (v) => !!v[t]; }
      throw new Error(t ? "unexpected “" + t + "”" : "the expression ends too early");
    }
    if (!T.length) throw new Error("the expression is empty");
    const f = imp(); if (i < T.length) throw new Error("unexpected “" + T[i] + "”");
    return { eval: f, vars: [...vars].sort() };
  }
  function rows(vars) {
    const n = vars.length, out = [];
    for (let k = 0; k < 2 ** n; k++) { const r = {}; vars.forEach((v, j) => (r[v] = ((k >> (n - 1 - j)) & 1) ? 0 : 1)); out.push(r); }
    return out;
  }
  const TF = (b) => (b ? "T" : "F");
  window.LG = { parse, rows, TF };
})();
