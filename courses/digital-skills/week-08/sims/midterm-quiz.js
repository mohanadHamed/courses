// The practice exam of midterm-prep.qmd: 30 random questions from
// midterm-bank.js (7 + 7 + 8 + 8 from Units 1–4), 50 minutes, one try per
// question. Each answer is marked at once, with its reason in English and
// Arabic; the mark comes at the end. The attempt is kept in this browser
// (localStorage, inside try/catch), so a reload does not lose it.
(() => {
  const BANK = window.MIDTERM_BANK || [];
  const UNITS = window.MIDTERM_UNITS || {};
  const PICK = { 1: 7, 2: 7, 3: 8, 4: 8 };
  const N = Object.values(PICK).reduce((a, b) => a + b, 0);
  const MINUTES = 50;
  const KEY = "ds-midterm-prep-v1";
  const SIG = BANK.length + ":" + BANK.map((b) => b.q.length).join(".").slice(0, 400);
  const LETTERS = ["A", "B", "C", "D"];
  const app = document.getElementById("mq-app");
  if (!app) return;

  let st = null; // {sig, ids, orders, answers, start, end, cur, finished}
  let timer = null;

  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const shuffle = (a) => { const b = a.slice(); for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) { /* private window: no saving */ } };
  const load = () => { try { const s = JSON.parse(localStorage.getItem(KEY) || "null"); return s && s.sig === SIG ? s : null; } catch (e) { return null; } };
  const clear = () => { try { localStorage.removeItem(KEY); } catch (e) { /* nothing */ } };

  // ---------------------------------------------------------------- start
  function intro() {
    stopTimer();
    const counts = Object.keys(PICK).map((u) => BANK.filter((b) => b.u == u).length);
    app.innerHTML = `
      <div class="mq-card mq-intro">
        <h2>Before you start · قبل أن تبدأ</h2>
        <ul class="mq-facts">
          <li><b>${N} questions</b>, chosen at random from a bank of <b>${BANK.length}</b> questions on Units 1–4.</li>
          <li><b>${MINUTES} minutes</b>. The clock starts when you tap Start, and the exam ends by itself when the time is up.</li>
          <li>Every question is in <b>simple English</b>. The reason of every answer is in English and Arabic.</li>
          <li><b>One try</b> for each question: tap one answer. The page tells you at once if it is right, and why, in English and Arabic.</li>
          <li>Each question is <b>1 mark</b>. Your mark (out of ${N}) shows at the end.</li>
          <li>Every new exam has new questions. Nothing is sent: the mark is only for you.</li>
        </ul>
        <ul class="mq-facts" dir="rtl" lang="ar">
          <li><b>${N} سؤالاً</b> تُختار عشوائياً من بنك فيه <b>${BANK.length}</b> سؤالاً عن الوحدات من 1 إلى 4.</li>
          <li><b>${MINUTES} دقيقة</b>، ويبدأ الوقت عند الضغط على Start، وينتهي الامتحان تلقائياً عند انتهاء الوقت.</li>
          <li>الأسئلة <b>بالإنجليزية البسيطة</b>، وسبب كل إجابة بالعربية والإنجليزية.</li>
          <li><b>محاولة واحدة</b> لكل سؤال: تظهر فوراً صحة الإجابة مع السبب بالعربية والإنجليزية، ثم الإجابة الصحيحة.</li>
          <li>لكل سؤال <b>علامة واحدة</b>، وتظهر علامتك من ${N} في النهاية.</li>
          <li>كل امتحان جديد فيه أسئلة جديدة، ولا يُرسل شيء: العلامة لك فقط.</li>
        </ul>
        <p class="mq-units">${Object.keys(PICK).map((u, i) => `<span>${esc(UNITS[u] || "Unit " + u)}: ${PICK[u]} questions (bank ${counts[i]})</span>`).join("")}</p>
        <button type="button" class="mq-btn mq-primary" id="mq-start">Start the exam · ابدأ الامتحان ▶</button>
      </div>`;
    document.getElementById("mq-start").addEventListener("click", begin);
  }

  function begin() {
    const ids = [];
    Object.keys(PICK).forEach((u) => {
      const pool = BANK.map((b, i) => (b.u == u ? i : -1)).filter((i) => i >= 0);
      ids.push(...shuffle(pool).slice(0, PICK[u]));
    });
    const order = shuffle(ids);
    st = {
      sig: SIG, ids: order,
      orders: order.map(() => shuffle([0, 1, 2, 3])),
      answers: order.map(() => null),
      start: Date.now(), end: null, cur: 0, finished: false,
    };
    save();
    render();
    startTimer();
  }

  // ---------------------------------------------------------------- timer
  const left = () => Math.max(0, st.start + MINUTES * 60000 - Date.now());
  function fmt(ms) { const s = Math.ceil(ms / 1000); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`; }
  function tick() {
    if (!st || st.finished) return stopTimer();
    const ms = left();
    const el = document.getElementById("mq-clock");
    if (el) { el.textContent = fmt(ms); el.classList.toggle("mq-low", ms < 5 * 60000); }
    if (ms <= 0) finish(true);
  }
  function startTimer() { stopTimer(); tick(); timer = setInterval(tick, 1000); }
  function stopTimer() { if (timer) clearInterval(timer); timer = null; }

  // ---------------------------------------------------------------- exam
  const qOf = (k) => BANK[st.ids[k]];
  const isRight = (k) => st.answers[k] === 0; // option 0 of the bank is right
  const answered = () => st.answers.filter((a) => a !== null).length;
  const rightCount = () => st.answers.filter((a) => a === 0).length;

  function render() {
    const k = st.cur, b = qOf(k), a = st.answers[k];
    const nav = st.ids.map((_, i) => {
      const cls = st.answers[i] === null ? "" : (isRight(i) ? " mq-ok" : " mq-no");
      return `<button type="button" class="mq-num${cls}${i === k ? " mq-here" : ""}" data-go="${i}" aria-label="Question ${i + 1}">${i + 1}</button>`;
    }).join("");
    const opts = st.orders[k].map((oi, pos) => {
      let cls = "";
      if (a !== null) { if (oi === 0) cls = " mq-right"; else if (oi === a) cls = " mq-wrong"; else cls = " mq-off"; }
      return `<button type="button" class="mq-opt${cls}" data-opt="${oi}" ${a !== null ? "disabled" : ""}><span class="mq-letter">${LETTERS[pos]}</span><span>${esc(b.o[oi])}</span></button>`;
    }).join("");
    app.innerHTML = `
      <div class="mq-bar">
        <span class="mq-time">⏱ <b id="mq-clock">${fmt(left())}</b></span>
        <span>Answered <b>${answered()}</b> / ${N}</span>
        <button type="button" class="mq-btn mq-finish" id="mq-end">Finish · إنهاء</button>
      </div>
      <div class="mq-nav">${nav}</div>
      <div class="mq-card">
        <p class="mq-meta">Question ${k + 1} of ${N} · ${esc(UNITS[b.u] || "Unit " + b.u)}</p>
        <p class="mq-q">${esc(b.q)}</p>
        <div class="mq-opts">${opts}</div>
        <div id="mq-fb">${a !== null ? feedback(k) : `<p class="mq-hint">Tap one answer. You have one try. · اختر إجابة واحدة، لديك محاولة واحدة.</p>`}</div>
        <div class="mq-move">
          <button type="button" class="mq-btn" id="mq-prev" ${k === 0 ? "disabled" : ""}>◀ Previous</button>
          ${k < N - 1 ? `<button type="button" class="mq-btn mq-primary" id="mq-next">Next ▶</button>`
                      : `<button type="button" class="mq-btn mq-primary" id="mq-last">Finish the exam ▶</button>`}
        </div>
      </div>`;
    app.querySelectorAll("[data-go]").forEach((el) => el.addEventListener("click", () => go(+el.dataset.go)));
    app.querySelectorAll("[data-opt]").forEach((el) => el.addEventListener("click", () => choose(+el.dataset.opt)));
    document.getElementById("mq-prev").addEventListener("click", () => go(k - 1));
    const nx = document.getElementById("mq-next"); if (nx) nx.addEventListener("click", () => go(k + 1));
    const ls = document.getElementById("mq-last"); if (ls) ls.addEventListener("click", () => finish(false));
    document.getElementById("mq-end").addEventListener("click", () => finish(false));
  }

  function feedback(k) {
    const b = qOf(k), ok = isRight(k);
    const pos = st.orders[k].indexOf(0);
    return `<div class="mq-fb ${ok ? "mq-fb-ok" : "mq-fb-no"}">
      <p class="mq-verdict">${ok ? "✓ Right answer · إجابة صحيحة" : "✗ Wrong answer · إجابة خاطئة"}</p>
      ${ok ? "" : `<p class="mq-correct">The right answer is <b>${LETTERS[pos]}: ${esc(b.o[0])}</b> · <span dir="rtl" lang="ar">الإجابة الصحيحة: ${LETTERS[pos]}</span></p>`}
      <p class="mq-why"><b>Why:</b> ${esc(b.en)}</p>
      <p class="mq-why" dir="rtl" lang="ar"><b>السبب:</b> ${esc(b.ar)}</p>
    </div>`;
  }

  function choose(oi) {
    if (st.finished || st.answers[st.cur] !== null) return; // one try only
    if (left() <= 0) return finish(true);
    st.answers[st.cur] = oi;
    save();
    render();
    const fb = document.getElementById("mq-fb");
    if (fb && fb.scrollIntoView) fb.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  function go(k) {
    if (k < 0 || k >= N) return;
    st.cur = k; save(); render();
    const top = app.getBoundingClientRect().top + window.scrollY - 70;
    if (window.scrollY > top) window.scrollTo({ top, behavior: "smooth" });
  }

  // ---------------------------------------------------------------- end
  function finish(timeUp) {
    if (!st || st.finished) return;
    const open = N - answered();
    if (!timeUp && open > 0 &&
        !window.confirm(`You have ${open} question(s) with no answer. They get 0 marks. Finish the exam now?\nلديك ${open} سؤال بلا إجابة. هل تريد إنهاء الامتحان الآن؟`)) return;
    st.finished = true; st.end = Date.now(); st.timeUp = !!timeUp;
    save(); stopTimer(); results();
  }

  function results() {
    const mark = rightCount(), pct = Math.round((mark / N) * 100);
    const used = Math.min(MINUTES * 60000, (st.end || Date.now()) - st.start);
    const msg = pct >= 80 ? ["Excellent! You are ready.", "ممتاز! أنت جاهز للامتحان."]
      : pct >= 60 ? ["Good. Study the questions you missed, then try a new exam.", "جيد. راجع الأسئلة التي أخطأت فيها، ثم جرّب امتحاناً جديداً."]
      : ["Study the review PDF and the units below, then try a new exam.", "راجع ملف المراجعة والوحدات أدناه، ثم جرّب امتحاناً جديداً."];
    const rows = Object.keys(PICK).map((u) => {
      const ks = st.ids.map((_, k) => k).filter((k) => qOf(k).u == u);
      return `<tr><td>${esc(UNITS[u] || "Unit " + u)}</td><td><b>${ks.filter(isRight).length}</b> / ${ks.length}</td></tr>`;
    }).join("");
    const review = st.ids.map((_, k) => {
      const b = qOf(k), a = st.answers[k];
      const mine = a === null ? "no answer · بلا إجابة" : esc(b.o[a]);
      const cls = a === null ? "mq-skip" : (isRight(k) ? "mq-ok" : "mq-no");
      return `<li class="${cls}"><p class="mq-q">${k + 1}. ${esc(b.q)}</p>
        <p>Your answer: <b>${mine}</b>${isRight(k) ? " ✓" : ""}</p>
        ${isRight(k) ? "" : `<p>Right answer: <b>${esc(b.o[0])}</b></p>`}
        <p class="mq-why"><b>Why:</b> ${esc(b.en)}</p>
        <p class="mq-why" dir="rtl" lang="ar"><b>السبب:</b> ${esc(b.ar)}</p></li>`;
    }).join("");
    app.innerHTML = `
      <div class="mq-card mq-result">
        ${st.timeUp ? `<p class="mq-timeup">⏱ Time is up! · انتهى الوقت</p>` : ""}
        <p class="mq-big">Your mark: <b>${mark} / ${N}</b></p>
        <p class="mq-big-ar" dir="rtl" lang="ar">علامتك: <b>${mark} من ${N}</b> (${pct}%)</p>
        <p>${msg[0]}<br><span dir="rtl" lang="ar">${msg[1]}</span></p>
        <p class="mq-meta">Time used: ${fmt(used)} of ${MINUTES}:00 · Answered ${answered()} of ${N}</p>
        <table class="mq-table"><thead><tr><th>Unit</th><th>Right</th></tr></thead><tbody>${rows}</tbody></table>
        <button type="button" class="mq-btn mq-primary" id="mq-again">Start a new exam · امتحان جديد ▶</button>
      </div>
      <details class="mq-card mq-review" ${mark < N ? "open" : ""}>
        <summary>Review your answers · راجع إجاباتك</summary>
        <ol class="mq-list">${review}</ol>
      </details>`;
    document.getElementById("mq-again").addEventListener("click", () => { clear(); st = null; intro(); app.scrollIntoView({ behavior: "smooth" }); });
    app.scrollIntoView({ behavior: "smooth" });
  }

  // ---------------------------------------------------------------- boot
  st = load();
  if (!st) intro();
  else if (st.finished) results();
  else if (left() <= 0) { render(); finish(true); }
  else { render(); startTimer(); }
  document.addEventListener("visibilitychange", () => { if (!document.hidden) tick(); });
})();
