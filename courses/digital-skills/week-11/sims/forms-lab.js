// Forms Lab: a simulator that looks like Microsoft Forms in the browser, with
// the order form of the Lecture 9 worksheet (Mona's Cakes): the title, three
// questions (Text, Choice, Date), Preview with a test order, and Responses.
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
  const btn = (html, title, fn, cls = "") => { const b = h("button", "w-btn " + cls); b.type = "button"; b.innerHTML = html; b.title = title; b.setAttribute("aria-label", title);
    b.addEventListener("click", (e) => { e.stopPropagation(); fn(e); }); return b; };
  const say = (text, bad) => { const m = $("#msg"); m.innerHTML = text; m.className = "message" + (bad ? " bad" : ""); };
  const KINDS = [["Choice", "◉"], ["Text", "≡"], ["Rating", "★"], ["Date", "▦"]];
  let S;
  const reset = () => { S = { title: "Untitled form", qs: [], adding: false, tab: "Questions", preview: false, answers: {}, responses: [] }; };
  const root = $("#forms"); root.className = "word web forms";
  root.innerHTML = `<div class="t-address"><span>&#8592; &#8594;</span><b>forms.office.com</b></div><div class="f-top"></div><div class="f-body"></div>`;

  function top() {
    const t = $(".f-top", root); t.innerHTML = "";
    t.appendChild(h("b", "f-brand", "Forms"));
    const tabs = h("div", "f-tabs");
    ["Questions", "Responses"].forEach((n) => tabs.appendChild(btn(n + (n === "Responses" ? ` <span class='f-n'>${S.responses.length}</span>` : ""), n, () => { S.tab = n; S.preview = false; draw(); }, "f-tab" + (S.tab === n && !S.preview ? " on" : ""))));
    t.appendChild(tabs);
    t.appendChild(btn("&#9655; Preview", "Preview", () => { if (!S.qs.length) { say("First add the questions.", true); return; } S.preview = true; S.answers = {}; say("<b>Preview</b>: the form as the customer sees it. Fill in a test order and click <b>Submit</b>."); draw(); }, "f-act"));
    t.appendChild(btn("Collect responses", "Collect responses", () => say("<b>Collect responses</b> gives the link of the form to send to the customers. Not needed today.", true), "f-act f-blue"));
  }
  function editor(b) {
    const card = h("div", "f-card f-head");
    const ti = h("input", "f-title"); ti.value = S.title === "Untitled form" ? "" : S.title; ti.placeholder = "Untitled form";
    ti.addEventListener("change", () => { S.title = ti.value.trim() || "Untitled form"; say(`The title: <b>${S.title}</b>. The customers see it at the top of the form.`); draw(); });
    card.appendChild(ti); card.appendChild(h("small", "", "Click the title to change it."));
    b.appendChild(card);
    S.qs.forEach((q, i) => {
      const c = h("div", "f-card");
      const qi = h("input", "f-q"); qi.value = q.text; qi.placeholder = `${i + 1}. Question`;
      qi.addEventListener("change", () => { q.text = qi.value.trim(); draw(); }); c.appendChild(qi);
      if (q.kind === "Choice") {
        q.opts.forEach((o, k) => { const oi = h("input", "f-opt"); oi.value = o; oi.placeholder = `Option ${k + 1}`; oi.addEventListener("change", () => { q.opts[k] = oi.value.trim(); draw(); }); c.appendChild(oi); });
        c.appendChild(btn("+ Add option", "Add option", () => { q.opts.push(""); draw(); }, "f-link"));
      } else c.appendChild(h("div", "f-ph", { Text: "Enter your answer", Date: "Please input date (dd/MM/yyyy)", Rating: "★ ★ ★ ★ ★" }[q.kind]));
      const foot = h("div", "f-foot"); foot.appendChild(h("small", "", q.kind));
      const req = h("label", "f-req"); const cb = h("input"); cb.type = "checkbox"; cb.checked = q.req; cb.addEventListener("change", () => { q.req = cb.checked; say(q.req ? "<b>Required</b>: the customer must answer this question." : "Not required."); draw(); });
      req.appendChild(cb); req.appendChild(document.createTextNode(" Required")); foot.appendChild(req);
      c.appendChild(foot); b.appendChild(c);
    });
    const add = btn("+ Add new", "Add new", () => { S.adding = !S.adding; draw(); }, "f-add"); b.appendChild(add);
    if (S.adding) { const row = h("div", "f-kinds"); KINDS.forEach(([k, ic]) => row.appendChild(btn(`<span>${ic}</span>${k}`, k, () => {
      S.qs.push({ kind: k, text: "", opts: k === "Choice" ? ["", ""] : [], req: false }); S.adding = false;
      say(`A <b>${k}</b> question. Type the question${k === "Choice" ? ", then the options" : ""}.`); draw(); const ins = root.querySelectorAll(".f-q"); ins[ins.length - 1].focus(); }, "f-kind"))); b.appendChild(row); }
  }
  function preview(b) {
    const card = h("div", "f-card f-head"); card.appendChild(h("h2", "", S.title)); b.appendChild(card);
    S.qs.forEach((q, i) => {
      const c = h("div", "f-card"); c.appendChild(h("b", "", `${i + 1}. ${q.text || "Question"}${q.req ? " *" : ""}`));
      if (q.kind === "Choice") q.opts.filter(Boolean).forEach((o) => { const l = h("label", "f-radio"); const r = h("input"); r.type = "radio"; r.name = "q" + i; r.checked = S.answers[i] === o;
        r.addEventListener("change", () => { S.answers[i] = o; }); l.appendChild(r); l.appendChild(document.createTextNode(" " + o)); c.appendChild(l); });
      else { const inp = h("input", "f-ans"); inp.value = S.answers[i] || ""; inp.placeholder = q.kind === "Date" ? "dd/MM/yyyy" : "Enter your answer"; inp.addEventListener("input", () => { S.answers[i] = inp.value; }); c.appendChild(inp); }
      b.appendChild(c);
    });
    b.appendChild(btn("Submit", "Submit", () => {
      const miss = S.qs.findIndex((q, i) => q.req && !String(S.answers[i] || "").trim());
      if (miss >= 0) { say(`Question ${miss + 1} is <b>Required</b>: answer it first.`, true); return; }
      S.responses.push({ ...S.answers }); S.preview = false; S.tab = "Responses"; say("&#10003; Your test order is sent. <b>Responses</b> shows it; <b>Open results in Excel</b> shows every order in a sheet."); draw(); }, "f-submit"));
  }
  function responses(b) {
    const c = h("div", "f-card"); c.appendChild(h("h2", "", `${S.responses.length} Responses`));
    if (S.responses.length) {
      c.appendChild(btn("Open results in Excel", "Open results in Excel", () => { S.excel = true; say("The responses in a sheet: one row for each order, one column for each question."); draw(); }, "f-act f-green"));
      if (S.excel) { const t = h("table", "t-grid"); const hr = h("tr"); ["ID", ...S.qs.map((q) => q.text || "Question")].forEach((x) => hr.appendChild(h("th", "", x))); t.appendChild(hr);
        S.responses.forEach((r, k) => { const tr = h("tr"); tr.appendChild(h("td", "", String(k + 1))); S.qs.forEach((_, i) => tr.appendChild(h("td", "", r[i] || ""))); t.appendChild(tr); }); c.appendChild(t); }
    } else c.appendChild(h("p", "", "No responses yet. Preview the form and submit a test order."));
    b.appendChild(c);
  }
  const has = (k, re) => S.qs.some((q) => q.kind === k && re.test(q.text));
  const MISSIONS = [
    ["The title: <b>Mona's Cakes: order</b>", () => /mona/i.test(S.title)],
    ["<b>+ Add new › Text</b>: <b>Your name</b>, Required", () => S.qs.some((q) => q.kind === "Text" && /name/i.test(q.text) && q.req)],
    ["<b>Choice</b>: <b>Which cake?</b> with Chocolate, Strawberry, Vanilla", () => S.qs.some((q) => q.kind === "Choice" && /cake/i.test(q.text) && q.opts.filter(Boolean).length >= 3)],
    ["<b>Date</b>: <b>When do you want it?</b>", () => has("Date", /when|date|day/i)],
    ["<b>Preview</b>: a test order, <b>Submit</b>; then <b>Responses</b>", () => S.responses.length > 0],
  ];
  function status() {
    const list = $("#jobs"); list.innerHTML = ""; let done = 0;
    MISSIONS.forEach(([t, f]) => { const ok = !!f(); done += ok; const li = h("li", ok ? "ok" : ""); li.innerHTML = t; list.appendChild(li); });
    $("#progress").textContent = `${done} of ${MISSIONS.length}`;
    if (done === MISSIONS.length && !status.done) { status.done = true; say(window.SIM_DONE || "&#10003; All steps done. Now do the same steps in Microsoft Forms."); }
  }
  function draw() {
    top(); const b = $(".f-body", root); b.innerHTML = "";
    if (S.preview) preview(b); else if (S.tab === "Responses") responses(b); else editor(b);
    status();
  }
  document.addEventListener("click", (e) => { if (S.adding && !e.target.closest(".f-kinds,.f-add")) { S.adding = false; draw(); } });
  $("#reset").addEventListener("click", () => { reset(); status.done = false; say(HELLO); draw(); });
  const HELLO = "A new form. Click <b>Untitled form</b> and type the title <b>Mona's Cakes: order</b>.";
  reset(); say(HELLO); draw();
})();
