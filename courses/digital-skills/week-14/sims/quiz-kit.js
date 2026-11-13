// A step-by-step choice simulator: each step has a question, options, the right
// option, the reason and a hint for each wrong option. `preview(chosen)` draws
// what the student builds (a post, a plan, a page) from the right answers so far.
window.QuizKit = (cfg) => {
  const $ = (id) => document.getElementById(id);
  const chosen = []; let i = 0, right = 0, tries = 0;
  function show() {
    if (cfg.preview) $("preview").innerHTML = cfg.preview(chosen);
    if (i >= cfg.steps.length) { $("task").textContent = cfg.done; $("opts").innerHTML = ""; return; }
    const st = cfg.steps[i]; tries = 0;
    $("task").textContent = `${cfg.label || "Step"} ${i + 1} of ${cfg.steps.length}: ${st.q}`;
    const n = st.opts.length, r = (i * 2 + 1) % n, order = st.opts.map((o, k) => (k + r) % n);
    $("opts").innerHTML = order.map((k) => `<button type="button" class="ghost" data-k="${k}">${st.opts[k]}</button>`).join("");
    document.querySelectorAll("#opts button").forEach((b) => b.addEventListener("click", () => pick(Number(b.dataset.k))));
  }
  function pick(k) {
    const st = cfg.steps[i];
    if (k !== st.right) { tries++; $("msg").textContent = "✗ " + ((st.hints && st.hints[k]) || "Look again."); $("msg").className = "message bad"; return; }
    if (!tries) right++;
    chosen.push(st.opts[k]);
    $("msg").textContent = "✓ " + st.why; $("msg").className = "message good";
    if ($("score")) $("score").textContent = `${right} of ${cfg.steps.length} right the first time`;
    i++; setTimeout(show, cfg.delay || 1300);
  }
  window.QK = { pick: (k) => pick(k), right: () => pick(cfg.steps[i].right) };
  show();
};
