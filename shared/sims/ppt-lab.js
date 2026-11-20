// PowerPoint Lab: a simulator that looks like PowerPoint for Windows, with the
// talk of the Lecture 5 worksheet (the book fair). One engine, three parts,
// chosen by the page that loads it (window.PPT_LAB):
//   slides: the Title Slide typed, Home › New Slide › Title and Content, a theme;
//   notes:  three short points on slide 2, the details in the speaker notes;
//   motion: Transitions › Fade › Apply To All, Animations › Appear, the slide show.
// The steps are the steps of the worksheet, so the teacher shows them here first.
(() => {
  const PART = window.PPT_LAB || "slides";
  const $ = (s, el = document) => el.querySelector(s);
  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
  const btn = (html, title, fn, cls = "") => { const b = h("button", "w-btn " + cls); b.type = "button"; b.innerHTML = html; b.title = title; b.setAttribute("aria-label", title);
    b.addEventListener("click", (e) => { e.stopPropagation(); fn(e); }); return b; };
  const say = (text, bad) => { const m = $("#msg"); m.innerHTML = text; m.className = "message" + (bad ? " bad" : ""); };
  const norm = (x) => (x || "").toLowerCase().replace(/[^a-z0-9:·]+/g, " ").trim();

  const THEMES = { "Office Theme": ["#ffffff", "#222222", null], Facet: ["#e7f4e4", "#1f3d28", "#2b7a3b"], Integral: ["#eaf2fb", "#1f2f4c", "#1f4e8c"],
    Ion: ["#1a6e8e", "#ffffff", "#ffd43b"], Retrospect: ["#fbefe3", "#5b2c0b", "#a14f17"], Slice: ["#244a6b", "#ffffff", "#7fb3e0"] };
  const VARIANTS = ["#2b7a3b", "#1f4e8c", "#a14f17", "#6b3fa0"];
  const TRANS = ["None", "Morph", "Fade", "Push", "Wipe", "Split", "Vortex"];
  const ANIMS = ["None", "Appear", "Fade", "Fly In", "Float In", "Wipe", "Zoom"];
  const TITLE = { layout: "Title Slide", title: "Our Book Fair", sub: "Sunrise College · Sunday to Tuesday" };
  const WHEN = { layout: "Title and Content", title: "When and where", points: ["Sunday to Tuesday", "10:00 to 15:00", "The college library"] };

  let st;
  function reset() {
    const slides = PART === "slides" || PART === "post" ? [{ layout: "Title Slide", title: "", sub: "" }]
      : PART === "notes" ? [{ ...TITLE }, { layout: "Title and Content", title: "When and where", points: [], notes: "" }]
      : [{ ...TITLE }, { ...WHEN, notes: "Entry is free for everyone." }];
    st = { slides, cur: PART === "notes" ? 1 : 0, theme: PART === "motion" ? "Facet" : "Office Theme", variant: null, trans: {}, anim: {}, tab: "Home",
      menu: null, edit: null, sel: null, show: null, shown: false, saved: {} };
  }

  // ---------- The missions (the steps of the worksheet) ----------
  const s1 = () => st.slides[1];
  const MISSIONS = {
    slides: [
      ["Slide 1: click <b>Click to add title</b>, type <b>Our Book Fair</b>; the subtitle: <b>Sunrise College · Sunday to Tuesday</b>", () => norm(st.slides[0].title) === "our book fair" && /sunrise college/.test(norm(st.slides[0].sub))],
      ["<b>Home › New Slide ▾ › Title and Content</b>", () => st.slides.some((x, i) => i > 0 && x.layout === "Title and Content")],
      ["<b>Design</b>: click a theme you like", () => st.theme !== "Office Theme"],
    ],
    notes: [
      ["Slide 2: click <b>Click to add text</b>, type three short points: <b>Sunday to Tuesday</b>, <b>10:00 to 15:00</b>, <b>The college library</b>", () => s1().points.length === 3 && s1().points.every((p) => p.trim().split(/\s+/).length <= 8)],
      ["The notes pane: click <b>Click to add notes</b>, type <b>Entry is free for everyone.</b>", () => /entry is free/.test(norm(s1().notes))],
    ],
    post: [
      ["Click <b>Click to add title</b>, type <b>Fresh cakes for your party!</b>", () => /cake/i.test(st.slides[0].title)],
      ["The subtitle, the call to action: <b>Order today on our website</b>", () => /order/i.test(st.slides[0].sub)],
      ["<b>Design</b>: a theme; <b>Insert › Icons</b>: a cake", () => st.theme !== "Office Theme" && !!st.slides[0].icon],
      ["<b>File › Save As</b>: <b>post-Huda</b> as a PowerPoint file, then again as <b>PNG</b>", () => st.saved.pptx && st.saved.png],
    ],
    motion: [
      ["<b>Transitions › Fade › Apply To All</b>", () => st.slides.every((x, i) => st.trans[i] === "Fade")],
      ["Slide 2: click the list, then <b>Animations › Appear</b>", () => st.anim[1] === "Appear"],
      ["<b>Slide Show</b> (or <b>F5</b>): click until the end", () => st.shown],
    ],
  }[PART];

  // ---------- The window ----------
  const root = $("#ppt");
  root.className = "word ppt";
  root.innerHTML = `
    <div class="w-title"><span class="w-auto">AutoSave <i></i> Off</span><b>Presentation1 - PowerPoint</b><span class="w-search">Search</span><span class="w-win">&#8211; &#9633; &#10005;</span></div>
    <div class="w-tabs"></div><div class="w-ribbon"></div>
    <div class="w-body"><div class="p-thumbs"></div><div class="p-main"><div class="p-stage"></div><div class="p-notes"></div></div></div>
    <div class="w-status"><span class="p-count"></span><span>English (United States)</span><span>Notes</span></div>`;
  const TABS = ["File", "Home", "Insert", "Draw", "Design", "Transitions", "Animations", "Slide Show", "Review", "View", "Help"];
  const OPEN = { slides: ["Home", "Design"], notes: ["Home", "View"], motion: ["Home", "Transitions", "Animations", "Slide Show"], post: ["File", "Home", "Insert", "Design"] }[PART];

  function tabs() {
    const bar = $(".w-tabs", root); bar.innerHTML = "";
    TABS.forEach((t) => bar.appendChild(btn(t, t, () => {
      if (t === "Slide Show" && PART === "motion") { startShow(); return; }
      if (t === "File" && PART === "post") { st.menu = "save"; draw(); return; }
      if (OPEN.includes(t)) { st.tab = t; st.menu = null; draw(); }
      else say(`<b>${t}</b>: not needed in this part. Use ${OPEN.map((x) => "<b>" + x + "</b>").join(", ")}.`, true);
    }, "w-tab" + (t === st.tab ? " on" : ""))));
  }
  const group = (label, ...items) => { const g = h("div", "w-group"); const row = h("div", "w-row"); items.forEach((i) => row.appendChild(i)); g.appendChild(row); g.appendChild(h("small", "", label)); return g; };
  function gallery(names, cur, fn, cls, draw1) {
    const g = h("div", "p-gallery");
    names.forEach((n) => { const b = btn(draw1 ? draw1(n) : n, n, () => fn(n), "p-gal " + (cls || "") + (n === cur ? " on" : "")); g.appendChild(b); });
    return g;
  }
  function ribbon() {
    const r = $(".w-ribbon", root); r.innerHTML = "";
    if (st.tab === "Home") {
      const ns = btn("<span class='w-big'>&#9634;</span>New<br>Slide ▾", "New Slide", () => { st.menu = st.menu === "new" ? null : "new"; draw(); }, "w-tall");
      r.appendChild(group("Slides", ns, btn("Layout ▾", "Layout", () => say("Layout changes the plan of the slide that is selected. Today: <b>New Slide ▾</b>.", true))));
      r.appendChild(group("Font", h("span", "w-box", "Aptos (Body) ▾"), h("span", "w-box w-size", "28 ▾"), btn("<b>B</b>", "Bold", () => say("Bold: not in today's steps.", true))));
      r.appendChild(group("Designer", btn("<span class='w-big'>&#10022;</span>Designer", "Designer", () => say("<b>Designer</b> suggests designs for the slide (in Microsoft 365). Today: a theme of the <b>Design</b> tab.", true), "w-tall")));
      if (st.menu === "new") {
        const m = h("div", "w-menu p-layouts"); m.appendChild(h("b", "", "Office Theme"));
        const g = h("div", "p-laygrid");
        ["Title Slide", "Title and Content", "Section Header", "Two Content", "Comparison", "Title Only"].forEach((n) => g.appendChild(btn(`<span class='p-lay ${n.replace(/ /g, "")}'></span>${n}`, n, () => newSlide(n), "p-layb")));
        m.appendChild(g); ns.parentElement.parentElement.appendChild(m);
      }
    } else if (st.tab === "Design") {
      r.appendChild(group("Themes", gallery(Object.keys(THEMES), st.theme, (n) => { st.theme = n; st.variant = null; say(`<b>${n}</b>: all slides changed at once: the same colours, fonts and background.`); draw(); }, "p-theme",
        (n) => `<span class='p-sw' style='background:${THEMES[n][0]};color:${THEMES[n][1]}'>Aa</span>`)));
      r.appendChild(group("Variants", gallery(VARIANTS.map((_, i) => "Variant " + (i + 1)), st.variant, (n) => { if (st.theme === "Office Theme") { say("First choose a theme, then a variant.", true); return; } st.variant = n; say(`<b>${n}</b>: other colours of the same theme.`); draw(); }, "p-var",
        (n) => `<span class='p-vb' style='border-bottom-color:${VARIANTS[+n.slice(-1) - 1]}'></span>`)));
    } else if (st.tab === "View") {
      r.appendChild(group("Show", h("span", "w-item on", "Notes")));
    } else if (st.tab === "Transitions") {
      r.appendChild(group("Transition to This Slide", gallery(TRANS, st.trans[st.cur], (n) => { st.trans[st.cur] = n; say(`<b>${n}</b> on slide ${st.cur + 1}. ${n === "Vortex" ? "A wild effect pulls the eyes away from your message: choose a quiet one." : "Now <b>Apply To All</b>: the same quiet transition on every slide."}`, n === "Vortex"); draw(); }, "p-eff",
        (n) => `<span class='p-ic'></span>${n}`)));
      r.appendChild(group("Timing", h("span", "w-item", "Duration: 01.00"), btn("Apply To All", "Apply To All", () => {
        const t = st.trans[st.cur]; if (!t || t === "None") { say("First click a transition (Fade), then <b>Apply To All</b>.", true); return; }
        st.slides.forEach((_, i) => { st.trans[i] = t; }); say(`<b>Apply To All</b>: every slide now has <b>${t}</b>.`); draw(); })));
    } else if (st.tab === "Insert") {
      const ic = btn("<span class='w-big'>&#9733;</span>Icons", "Icons", () => { st.menu = st.menu === "icons" ? null : "icons"; draw(); }, "w-tall");
      r.appendChild(group("Illustrations", btn("<span class='w-big'>&#9638;</span>Pictures", "Pictures", () => say("Pictures need a file. Today: <b>Icons</b>.", true), "w-tall"), ic));
      if (st.menu === "icons") { const m = h("div", "w-menu p-icons"); m.appendChild(h("b", "", "Icons: cake"));
        ["🎂", "🍰", "🧁", "🎁"].forEach((x) => m.appendChild(btn(`<span class='p-ico'>${x}</span>`, "Icon " + x, () => { st.slides[st.cur].icon = x; st.menu = null; say("The icon is on the slide. A picture makes a post easy to see."); draw(); }, "p-icb")));
        m.appendChild(btn("Insert", "Insert", () => {}, "x-ok")); ic.parentElement.parentElement.appendChild(m); }
    } else if (st.tab === "Animations") {
      r.appendChild(group("Animation", gallery(ANIMS, st.anim[st.cur], (n) => {
        if (st.sel !== "body") { say("First click the list of points on slide 2: an animation is for one thing on the slide.", true); return; }
        st.anim[st.cur] = n; say(`<b>${n}</b>: in the slide show the points come one by one, on a click.`); draw(); }, "p-eff", (n) => `<span class='p-star'></span>${n}`)));
      r.appendChild(group("Timing", h("span", "w-item", "Start: On Click")));
    }
  }

  // ---------- Commands ----------
  function newSlide(layout) {
    st.menu = null;
    const sl = { layout, title: "", points: [], notes: "" };
    st.slides.splice(st.cur + 1, 0, sl); st.cur += 1;
    say(`A new slide with the layout <b>${layout}</b>. ${layout === "Title and Content" ? "Its placeholders: a title and a list of points." : "For a list of points, <b>Title and Content</b> is the usual layout."}`, layout !== "Title and Content");
    draw();
  }
  function startShow() { st.show = { slide: 0, step: 0 }; draw(); }

  // ---------- The slides ----------
  function slideEl(sl, i, big) {
    const [bg, fg, acc] = THEMES[st.theme]; const v = st.variant ? VARIANTS[+st.variant.slice(-1) - 1] : acc;
    const d = h("div", "p-slide" + (big ? " big" : "")); d.style.background = bg; d.style.color = fg;
    if (v) d.style.borderLeft = `${big ? 14 : 5}px solid ${v}`;
    const ph = (field, text, label, cls) => {
      const editing = big && st.edit && st.edit.field === field;
      const el = h("div", "p-ph " + cls + (text ? "" : " empty") + (big && st.sel === field ? " sel" : ""));
      if (editing) {
        const inp = h(field === "body" ? "textarea" : "input", "p-in"); inp.value = field === "body" ? sl.points.join("\n") : text;
        if (field === "body") inp.rows = 4; inp.placeholder = field === "body" ? "One point on each line" : "";
        inp.addEventListener("click", (e) => e.stopPropagation());
        inp.addEventListener("keydown", (e) => { if (e.key === "Enter" && field !== "body") { e.preventDefault(); done(); } if (e.key === "Escape") done(); });
        const done = () => { if (field === "body") sl.points = inp.value.split("\n").map((x) => x.trim()).filter(Boolean); else sl[field] = inp.value.trim(); st.edit = null; feedback(field); draw(); };
        inp.addEventListener("blur", done);
        el.appendChild(inp);
      } else if (field === "body" && sl.points && sl.points.length) {
        const ul = h("ul"); sl.points.forEach((p) => ul.appendChild(h("li", "", p))); el.appendChild(ul);
      } else el.textContent = text || label;
      if (big) el.addEventListener("click", (e) => { e.stopPropagation(); st.sel = field;
        if (PART === "motion") { say(field === "body" ? "The list is selected. Now <b>Animations</b>." : "The title is selected."); draw(); return; }
        st.edit = { field }; draw(); });
      return el;
    };
    if (sl.icon) d.appendChild(h("span", "p-slide-ico", sl.icon));
    if (sl.layout === "Title Slide") { d.classList.add("tslide"); d.appendChild(ph("title", sl.title, "Click to add title", "t")); d.appendChild(ph("sub", sl.sub, "Click to add subtitle", "s")); }
    else { d.appendChild(ph("title", sl.title, "Click to add title", "h")); d.appendChild(ph("body", "", "Click to add text", "b")); }
    return d;
  }
  function feedback(field) {
    const sl = st.slides[st.cur];
    if (field === "body" && sl.points.length > 5) say("Too many points: keep 3 to 5 short points. The details go in the speaker notes.", true);
    else if (field === "body" && sl.points.some((p) => p.split(/\s+/).length > 8)) say("A point of more than 8 words is too long: keep it short and say the rest.", true);
    else say("Typed. The placeholder keeps the look of the theme.");
  }
  function stage() {
    const th = $(".p-thumbs", root); th.innerHTML = "";
    st.slides.forEach((sl, i) => { const t = h("div", "p-thumb" + (i === st.cur ? " on" : "")); t.appendChild(h("span", "", String(i + 1))); t.appendChild(slideEl(sl, i, false));
      if (st.trans[i] && st.trans[i] !== "None") t.appendChild(h("i", "p-star-mark", "★"));
      t.addEventListener("click", () => { st.cur = i; st.edit = null; st.sel = null; draw(); }); th.appendChild(t); });
    const sg = $(".p-stage", root); sg.innerHTML = ""; sg.appendChild(slideEl(st.slides[st.cur], st.cur, true));
    const nt = $(".p-notes", root); nt.innerHTML = "";
    const sl = st.slides[st.cur];
    if (st.edit && st.edit.field === "notes") {
      const inp = h("input", "p-in"); inp.value = sl.notes || ""; inp.placeholder = "Click to add notes";
      const done = () => { sl.notes = inp.value.trim(); st.edit = null; say(sl.notes ? "The <b>speaker notes</b>: what you say. In the slide show, only you see them (Presenter View)." : ""); draw(); };
      inp.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === "Escape") done(); }); inp.addEventListener("blur", done); inp.addEventListener("click", (e) => e.stopPropagation());
      nt.appendChild(inp);
    } else { nt.textContent = sl.notes || "Click to add notes"; nt.classList.toggle("empty", !sl.notes);
      nt.onclick = (e) => { e.stopPropagation(); if (PART === "motion") return; st.edit = { field: "notes" }; draw(); }; }
    $(".p-count", root).textContent = `Slide ${st.cur + 1} of ${st.slides.length}`;
  }
  function show() {
    let ov = $(".p-show"); if (!st.show) { if (ov) ov.remove(); return; }
    if (!ov) { ov = h("div", "p-show"); document.body.appendChild(ov); }
    ov.innerHTML = ""; const sl = st.slides[st.show.slide];
    const pts = sl.points || []; const d = slideEl({ ...sl, points: st.anim[st.show.slide] && st.anim[st.show.slide] !== "None" ? pts.slice(0, st.show.step) : pts }, st.show.slide, false);
    d.classList.add("full", "p-in-" + (st.trans[st.show.slide] || "None").replace(" ", "")); ov.appendChild(d);
    ov.appendChild(h("small", "", "Click: next · Esc: end"));
    ov.onclick = () => {
      const a = st.anim[st.show.slide] && st.anim[st.show.slide] !== "None";
      if (a && st.show.step < (sl.points || []).length) st.show.step += 1;
      else if (st.show.slide < st.slides.length - 1) { st.show.slide += 1; st.show.step = 0; }
      else { st.show = null; st.shown = true; say("&#10003; The end of the slide show. With <b>Fade</b> each slide comes in quietly, and with <b>Appear</b> the points come one by one."); }
      draw();
    };
  }
  document.addEventListener("keydown", (e) => { if (e.key === "F5" && PART === "motion") { e.preventDefault(); startShow(); } if (e.key === "Escape" && st.show) { st.show = null; draw(); } });

  function status() {
    const list = $("#jobs"); list.innerHTML = ""; let done = 0;
    MISSIONS.forEach(([t, f]) => { const ok = !!f(); done += ok; const li = h("li", ok ? "ok" : ""); li.innerHTML = t; list.appendChild(li); });
    $("#progress").textContent = `${done} of ${MISSIONS.length}`;
    if (done === MISSIONS.length && !status.done) { status.done = true; say("&#10003; All steps done. The same steps are in your worksheet: now do them in PowerPoint."); }
  }
  function saveBox() {
    let box = root.querySelector(".p-save"); if (box) box.remove(); if (st.menu !== "save") return;
    box = h("div", "w-menu p-save"); box.innerHTML = "<b>Save As</b><div class='t-path'>This PC › <b>Desktop</b></div>";
    const name = h("input", "x-in"); name.value = "post-Huda"; name.setAttribute("aria-label", "File name");
    const type = h("select", "x-in"); ["PowerPoint Presentation (*.pptx)", "PNG Portable Network Graphics Format (*.png)"].forEach((x) => type.appendChild(h("option", "", x)));
    box.appendChild(h("small", "", "File name:")); box.appendChild(name); box.appendChild(h("small", "", "Save as type:")); box.appendChild(type);
    box.appendChild(btn("Save", "Save", () => { const png = type.selectedIndex === 1; st.saved[png ? "png" : "pptx"] = true; st.menu = null;
      say(png ? "<b>Just This One</b>: the slide is now a picture, <b>post-Huda.png</b>, ready for social media." : "<b>post-Huda.pptx</b> is saved: you can change it later. Now save it again as <b>PNG</b>."); draw(); }, "x-ok"));
    box.addEventListener("click", (e) => e.stopPropagation());
    root.appendChild(box);
  }
  function draw() {
    tabs(); ribbon(); stage(); show(); saveBox(); status();
    const f = root.querySelector(".p-in"); if (f && document.activeElement !== f) f.focus();
  }
  document.addEventListener("click", (e) => { if (st.menu && !e.target.closest(".w-menu")) { st.menu = null; draw(); } });
  $("#reset").addEventListener("click", () => { reset(); status.done = false; say(HELLO); draw(); });
  const HELLO = { slides: "Click <b>Click to add title</b> on the slide and type <b>Our Book Fair</b>.",
    notes: "Slide 2 needs its points: click <b>Click to add text</b> (one point on each line).",
    motion: "Click the <b>Transitions</b> tab.", post: "A post for Mona's Cakes. Click <b>Click to add title</b> and type <b>Fresh cakes for your party!</b>" }[PART];
  reset(); say(HELLO); draw();
})();
