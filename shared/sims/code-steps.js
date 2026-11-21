// Code Steps: explains a short piece of code (SQL, R) by running it step by
// step on a small example table. Each step lights the line(s) of the code
// that it explains, says what they do in plain words, and shows the table
// after that step. Clicking a line of the code jumps to its step.
// Used by the Big Data labs (courses/big-data/NOTES.md, "Code is explained").
//
// The page sets window.CODE_STEPS before loading this file:
//   { lines: ["SELECT …", …],                 // the code, as the student types it
//     steps: [{ lines: [2], title: "FROM: which table", text: "… <b>…</b> …",
//               head: ["col", …], rows: [["v", …], …],
//               mark: 1,                       // optional: the column to light
//               groups: [0, 0, 1, …] }],       // optional: a colour group per row
//     done: "…" }                             // the message after the last step
(() => {
  const D = window.CODE_STEPS;
  const $ = (s) => document.querySelector(s);
  const GROUP = ["#fff3bf", "#d3f9d8", "#d0ebff", "#ffe3e3", "#e5dbff", "#ffe8cc"];
  let k = 0;
  const seen = new Set([0]);
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function draw() {
    const st = D.steps[k];
    $("#code").innerHTML = D.lines.map((ln, i) =>
      '<div class="cs-line' + (st.lines.includes(i) ? " on" : "") + '" data-i="' + i + '"><span class="cs-n">' + (i + 1) + "</span><code>" + esc(ln) + "</code></div>").join("");
    $("#title").innerHTML = "Step " + (k + 1) + " of " + D.steps.length + " · " + st.title;
    $("#text").innerHTML = st.text;
    const mark = st.mark;
    $("#table").innerHTML = "<tr>" + st.head.map((h, c) => '<th class="' + (c === mark ? "mk" : "") + '">' + esc(h) + "</th>").join("") + "</tr>" +
      st.rows.map((r, i) => '<tr style="' + (st.groups ? "background:" + GROUP[st.groups[i] % GROUP.length] : "") + '">' +
        r.map((v, c) => '<td class="' + (c === mark ? "mk" : "") + '">' + esc(v) + "</td>").join("") + "</tr>").join("");
    $("#rows").textContent = st.rows.length + (st.rows.length === 1 ? " row" : " rows");
    $("#back").disabled = k === 0;
    $("#next").textContent = k === D.steps.length - 1 ? "Start again" : "Next step ▶";
    const ol = $("#jobs"); ol.innerHTML = "";
    D.steps.forEach((s, i) => { const li = document.createElement("li"); li.innerHTML = s.title; if (seen.has(i)) li.className = "ok"; ol.appendChild(li); });
    $("#progress").textContent = seen.size + " of " + D.steps.length + " seen";
    const m = $("#msg");
    if (seen.size === D.steps.length && k === D.steps.length - 1) { m.className = "message good"; m.innerHTML = D.done || "All the lines are explained."; }
    else { m.className = "message"; m.innerHTML = "Click <b>Next step</b>, or click a line of the code."; }
  }
  $("#next").addEventListener("click", () => { k = k === D.steps.length - 1 ? 0 : k + 1; seen.add(k); draw(); });
  $("#back").addEventListener("click", () => { if (k > 0) { k--; seen.add(k); draw(); } });
  $("#code").addEventListener("click", (e) => {
    const line = e.target.closest(".cs-line");
    if (!line) return;
    const i = Number(line.dataset.i);
    const j = D.steps.findIndex((s) => s.lines.includes(i));
    if (j >= 0) { k = j; seen.add(k); draw(); }
  });
  draw();
})();
