// Sites Lab: a simulator that looks like Google Sites (sites.google.com).
// The Lecture 10 worksheet (Mona's Cakes) uses two parts, chosen by the page
// that loads it (window.SITES_LAB = "pages" or "design"):
//   pages:  the site name, the page title, two new pages (the menu grows);
//   design: a theme, then Preview on a phone, a tablet and a computer.
// Another page can set window.SITES_CFG = { start: { site, title, pages, theme },
// texts: { page: text }, hello, missions: [[html, (S) => true when done]] }
// (Online activity 11: the gym site). Then everything works: Pages › + New
// page, Themes, Insert › Button (a name and a link; S.buttons), Preview
// (S.previewed), Publish with a web address (S.published); a click on a page
// in Pages or in the menu shows that page (S.cur).
(() => {
  const PART = window.SITES_LAB || "pages";
  const CFG = window.SITES_CFG || null;
  const $ = (s, el = document) => el.querySelector(s);
  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
  const btn = (html, title, fn, cls = "") => { const b = h("button", "w-btn " + cls); b.type = "button"; b.innerHTML = html; b.title = title; b.setAttribute("aria-label", title);
    b.addEventListener("click", (e) => { e.stopPropagation(); fn(e); }); return b; };
  const say = (text, bad) => { const m = $("#msg"); m.innerHTML = text; m.className = "message" + (bad ? " bad" : ""); };
  const THEMES = { Simple: ["#ffffff", "#202124", "#1a73e8"], Aristotle: ["#f6efe6", "#3e2723", "#8d6e63"], Diplomat: ["#e8f0fe", "#0b2a5b", "#0b57d0"], Vision: ["#202124", "#ffffff", "#f6b26b"] };
  let S;
  const reset = () => {
    const st = CFG ? CFG.start || {} : PART === "pages" ? {} : { site: "Mona's Cakes", title: "Mona's Cakes", pages: ["Home", "Cakes", "Order"] };
    S = { site: st.site || "", title: st.title || "", pages: [...(st.pages || ["Home"])], cur: 0, panel: CFG ? "Pages" : PART === "pages" ? "Pages" : "Themes", newp: false,
      theme: st.theme || "Simple", device: null, previewed: new Set(), buttons: {}, dialog: null, published: null, pressed: false };
  };
  const root = $("#sites"); root.className = "word web sites";
  root.innerHTML = `<div class="t-address"><span>&#8592; &#8594;</span><b>sites.google.com</b></div><div class="g-top"></div><div class="g-body"><div class="g-page"></div><div class="g-panel"></div></div>`;
  function top() {
    const t = $(".g-top", root); t.innerHTML = "";
    const name = h("input", "g-site"); name.value = S.site; name.placeholder = "Untitled site"; name.setAttribute("aria-label", "Site name");
    name.addEventListener("change", () => { S.site = name.value.trim(); say(`The site name: <b>${S.site}</b>. It shows in the tab of the browser.`); draw(); });
    t.appendChild(name);
    t.appendChild(h("span", "g-gap", ""));
    if (S.published) t.appendChild(h("small", "g-pubd", "Published"));
    t.appendChild(btn("&#128065; Preview", "Preview", () => { S.device = "phone"; S.dialog = null; say("<b>Preview</b>: the site as the visitors see it. Try the phone, the tablet and the computer."); draw(); }, "g-icon"));
    t.appendChild(btn("Publish", "Publish", () => { if (!CFG) { say("<b>Publish</b> puts the site on the web with its own address. You do it in the online activity.", true); return; }
      S.dialog = "publish"; S.device = null; say("Type the <b>web address</b> of the site (no spaces), then <b>Publish</b>."); draw(); }, "g-pub"));
  }
  const text = (name) => (CFG ? (CFG.texts || {})[name] || "" : name === S.pages[0] ? "Fresh cakes, made at home. Order two days before." : "");
  function pageView(el, small) {
    const [bg, fg, acc] = THEMES[S.theme];
    el.style.background = bg; el.style.color = fg;
    const nav = h("div", "g-nav"); nav.style.borderBottomColor = acc;
    nav.appendChild(h("b", "", S.site || "Untitled site"));
    if (small && S.pages.length > 1) nav.appendChild(h("span", "g-burger", "☰"));
    else S.pages.forEach((p, i) => { const a = h("span", "g-link" + (i === S.cur ? " on" : ""), p); a.style.color = i === S.cur ? acc : fg; a.style.cursor = "pointer";
      a.addEventListener("click", () => { S.cur = i; draw(); }); nav.appendChild(a); });
    el.appendChild(nav);
    const page = S.pages[S.cur];
    const banner = h("div", "g-banner"); banner.style.background = acc;
    if (S.cur === 0) {
      const ti = h("input", "g-title"); ti.value = S.title; ti.placeholder = "Your page title"; ti.disabled = !!S.device || (!CFG && PART !== "pages"); ti.setAttribute("aria-label", "Page title");
      ti.addEventListener("change", () => { S.title = ti.value.trim(); say(`The title of the Home page: <b>${S.title}</b>.`); draw(); });
      banner.appendChild(ti);
    } else banner.appendChild(h("div", "g-title g-ptitle", page));
    el.appendChild(banner);
    const tx = text(page); if (tx) el.appendChild(h("p", "g-text", tx));
    const b = S.buttons[page];
    if (b) { const a = btn(b.name, b.name, () => { if (!S.device) { say("In the editor the button does not open. Click <b>Preview</b>, then the button.", true); return; }
      S.pressed = true; say(`&#10003; <b>${b.name}</b> opens <b>${b.link}</b>: the form of the service.`); draw(); }, "g-button"); a.style.background = acc; el.appendChild(a); }
  }
  function body() {
    const pg = $(".g-page", root); pg.innerHTML = ""; pg.className = "g-page";
    if (S.device) {
      const bar = h("div", "g-devs");
      [["phone", "Phone"], ["tablet", "Tablet"], ["laptop", "Large screen"]].forEach(([d, n]) => bar.appendChild(btn(n, n, () => { S.device = d; S.previewed.add(d); say(d === "phone" ? "On a <b>phone</b> the menu becomes ☰ and the text stays one column: easy to read." : `The site on a <b>${n.toLowerCase()}</b>.`); draw(); }, "g-dev" + (S.device === d ? " on" : ""))));
      bar.appendChild(btn("Exit preview", "Exit preview", () => { S.device = null; draw(); }, "g-dev"));
      pg.appendChild(bar);
      const frame = h("div", "g-frame " + S.device); pageView(frame, S.device === "phone"); pg.appendChild(frame);
      S.previewed.add(S.device);
      return;
    }
    if (S.dialog === "publish") {
      const d = h("div", "w-menu g-dialog g-pubdlg"); d.appendChild(h("b", "", "Publish site"));
      d.appendChild(h("small", "", "Web address"));
      const row = h("div", "g-addr"); row.appendChild(h("span", "", "https://sites.google.com/view/"));
      const i = h("input", "g-in"); i.placeholder = "your-address"; i.setAttribute("aria-label", "Web address"); row.appendChild(i); d.appendChild(row);
      const done = () => { const v = i.value.trim().toLowerCase(); if (!v) { say("Type the address first.", true); return; }
        if (/\s/.test(v)) { say("No spaces in a web address: use a dash, for example <b>college-gym</b>.", true); return; }
        S.published = v; S.dialog = null; say(`&#10003; <b>Published</b>: everyone can open <b>sites.google.com/view/${v}</b>. Open it on a phone, too.`); draw(); };
      i.addEventListener("keydown", (e) => { if (e.key === "Enter") done(); });
      d.appendChild(btn("Publish", "Publish now", done, "g-done")); d.appendChild(btn("Cancel", "Cancel", () => { S.dialog = null; draw(); }, "g-dev"));
      pg.appendChild(d);
    }
    const frame = h("div", "g-frame edit"); pageView(frame, false); pg.appendChild(frame);
  }
  function panel() {
    const p = $(".g-panel", root); p.innerHTML = ""; p.hidden = !!S.device; if (S.device) return;
    const tabs = h("div", "g-ptabs"); ["Insert", "Pages", "Themes"].forEach((n) => tabs.appendChild(btn(n, n, () => { S.panel = n; S.newp = false; if (S.dialog === "button") S.dialog = null; draw(); }, "g-ptab" + (S.panel === n ? " on" : "")))); p.appendChild(tabs);
    if (S.panel === "Pages") {
      S.pages.forEach((n, i) => { const d = h("div", "g-pg" + (i === S.cur ? " on" : ""), (i === 0 ? "⌂ " : "▢ ") + n); d.style.cursor = "pointer"; d.addEventListener("click", () => { S.cur = i; draw(); }); p.appendChild(d); });
      p.appendChild(btn("+ New page", "New page", () => { S.newp = true; draw(); }, "g-plus"));
      if (S.newp) { const d = h("div", "w-menu g-dialog"); d.appendChild(h("b", "", "New page")); const i = h("input", "g-in"); i.placeholder = "Name";
        const done = () => { const v = i.value.trim(); if (!v) return; S.pages.push(v); S.newp = false; say(`The page <b>${v}</b> is added: the menu at the top has a link to it.`); draw(); };
        i.addEventListener("keydown", (e) => { if (e.key === "Enter") done(); }); d.appendChild(i); d.appendChild(btn("Done", "Done", done, "g-done")); p.appendChild(d); }
    } else if (S.panel === "Themes") {
      Object.keys(THEMES).forEach((n) => { const b = btn(`<span class='g-sw' style='background:${THEMES[n][0]};border-color:${THEMES[n][2]}'></span>${n}`, n, () => { S.theme = n; say(`The theme <b>${n}</b>: the colours and the fonts of every page change at once.`); draw(); }, "g-theme" + (S.theme === n ? " on" : "")); p.appendChild(b); });
    } else if (!CFG) p.appendChild(h("small", "", "Text box, Images, Embed… Not needed today."));
    else {
      p.appendChild(btn("▭ Button", "Button", () => { S.dialog = "button"; draw(); }, "g-theme"));
      p.appendChild(btn("▣ Images", "Images", () => say("Images: not in these steps.", true), "g-theme"));
      p.appendChild(btn("▤ Text box", "Text box", () => say("Text box: not in these steps.", true), "g-theme"));
      if (S.dialog === "button") {
        const d = h("div", "w-menu g-dialog"); d.appendChild(h("b", "", "Insert button"));
        const n = h("input", "g-in"); n.placeholder = "Name"; n.setAttribute("aria-label", "Button name");
        const l = h("input", "g-in"); l.placeholder = "Link"; l.setAttribute("aria-label", "Button link");
        d.appendChild(n); d.appendChild(l);
        d.appendChild(btn("Insert", "Insert", () => { const nm = n.value.trim(), lk = l.value.trim(); if (!nm || !lk) { say("Type the <b>name</b> of the button and paste the <b>link</b> of the form.", true); return; }
          S.buttons[S.pages[S.cur]] = { name: nm, link: lk }; S.dialog = null; say(`The button <b>${nm}</b> is on the page <b>${S.pages[S.cur]}</b>. Click <b>Preview</b>, then the button.`); draw(); }, "g-done"));
        p.appendChild(d);
      }
    }
  }
  const MISSIONS = CFG && CFG.missions ? CFG.missions.map(([t, f]) => [t, () => f(S)]) : {
    pages: [
      ["Click <b>Untitled site</b> (top left) and type <b>Mona's Cakes</b>; the page title: <b>Mona's Cakes</b>", () => /mona/i.test(S.site) && /mona/i.test(S.title)],
      ["<b>Pages › + New page</b>: <b>Cakes</b>", () => S.pages.some((p) => /cake/i.test(p))],
      ["<b>+ New page</b>: <b>Order</b>: the menu has 3 links", () => S.pages.some((p) => /order/i.test(p)) && S.pages.length >= 3],
    ],
    design: [
      ["<b>Themes</b>: click a theme that you like", () => S.theme !== "Simple"],
      ["<b>Preview</b> (the eye), then <b>Phone</b>: the menu becomes ☰", () => S.previewed.has("phone")],
      ["<b>Large screen</b>: the menu has its three links again", () => S.previewed.has("laptop")],
    ],
  }[PART];
  function status() {
    const list = $("#jobs"); list.innerHTML = ""; let done = 0;
    MISSIONS.forEach(([t, f]) => { const ok = !!f(); done += ok; const li = h("li", ok ? "ok" : ""); li.innerHTML = t; list.appendChild(li); });
    $("#progress").textContent = `${done} of ${MISSIONS.length}`;
    if (done === MISSIONS.length && !status.done) { status.done = true; say(window.SIM_DONE || "&#10003; All steps done. Now do the same steps in Google Sites."); }
  }
  function draw() { top(); body(); panel(); status(); const f = root.querySelector(".g-dialog input"); if (f) f.focus(); }
  $("#reset").addEventListener("click", () => { reset(); status.done = false; say(HELLO); draw(); });
  const HELLO = (CFG && CFG.hello) || (PART === "pages" ? "A blank site. Click <b>Untitled site</b> at the top left and type the name." : "Click <b>Themes</b> on the right, then a theme.");
  reset(); say(HELLO); draw();
})();
