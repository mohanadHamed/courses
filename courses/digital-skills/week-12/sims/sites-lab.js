// Sites Lab: a simulator that looks like Google Sites (sites.google.com), with
// the site of the Lecture 10 worksheet (Mona's Cakes). Two parts, chosen by the
// page that loads it (window.SITES_LAB):
//   pages:  the site name, the page title, two new pages (the menu grows);
//   design: a theme, then Preview on a phone, a tablet and a computer.
(() => {
  const PART = window.SITES_LAB || "pages";
  const $ = (s, el = document) => el.querySelector(s);
  const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
  const btn = (html, title, fn, cls = "") => { const b = h("button", "w-btn " + cls); b.type = "button"; b.innerHTML = html; b.title = title; b.setAttribute("aria-label", title);
    b.addEventListener("click", (e) => { e.stopPropagation(); fn(e); }); return b; };
  const say = (text, bad) => { const m = $("#msg"); m.innerHTML = text; m.className = "message" + (bad ? " bad" : ""); };
  const THEMES = { Simple: ["#ffffff", "#202124", "#1a73e8"], Aristotle: ["#f6efe6", "#3e2723", "#8d6e63"], Diplomat: ["#e8f0fe", "#0b2a5b", "#0b57d0"], Vision: ["#202124", "#ffffff", "#f6b26b"] };
  let S;
  const reset = () => { S = PART === "pages" ? { site: "", title: "", pages: ["Home"], panel: "Pages", newp: false, theme: "Simple", device: null, previewed: new Set() }
    : { site: "Mona's Cakes", title: "Mona's Cakes", pages: ["Home", "Cakes", "Order"], panel: "Themes", newp: false, theme: "Simple", device: null, previewed: new Set() }; };
  const root = $("#sites"); root.className = "word web sites";
  root.innerHTML = `<div class="t-address"><span>&#8592; &#8594;</span><b>sites.google.com</b></div><div class="g-top"></div><div class="g-body"><div class="g-page"></div><div class="g-panel"></div></div>`;
  function top() {
    const t = $(".g-top", root); t.innerHTML = "";
    const name = h("input", "g-site"); name.value = S.site; name.placeholder = "Untitled site"; name.setAttribute("aria-label", "Site name");
    name.addEventListener("change", () => { S.site = name.value.trim(); say(`The site name: <b>${S.site}</b>. It shows in the tab of the browser.`); draw(); });
    t.appendChild(name);
    t.appendChild(h("span", "g-gap", ""));
    t.appendChild(btn("&#128065; Preview", "Preview", () => { S.device = "phone"; say("<b>Preview</b>: the site as the visitors see it. Try the phone, the tablet and the computer."); draw(); }, "g-icon"));
    t.appendChild(btn("Publish", "Publish", () => say("<b>Publish</b> puts the site on the web with its own address. You do it in the online activity.", true), "g-pub"));
  }
  function pageView(el, small) {
    const [bg, fg, acc] = THEMES[S.theme];
    el.style.background = bg; el.style.color = fg;
    const nav = h("div", "g-nav"); nav.style.borderBottomColor = acc;
    nav.appendChild(h("b", "", S.site || "Untitled site"));
    if (small && S.pages.length > 1) nav.appendChild(h("span", "g-burger", "☰"));
    else S.pages.forEach((p, i) => { const a = h("span", "g-link" + (i === 0 ? " on" : ""), p); a.style.color = i === 0 ? acc : fg; nav.appendChild(a); });
    el.appendChild(nav);
    const banner = h("div", "g-banner"); banner.style.background = acc;
    const ti = h("input", "g-title"); ti.value = S.title; ti.placeholder = "Your page title"; ti.disabled = !!S.device || PART !== "pages"; ti.setAttribute("aria-label", "Page title");
    ti.addEventListener("change", () => { S.title = ti.value.trim(); say(`The title of the Home page: <b>${S.title}</b>.`); draw(); });
    banner.appendChild(ti); el.appendChild(banner);
    el.appendChild(h("p", "g-text", "Fresh cakes, made at home. Order two days before."));
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
    const frame = h("div", "g-frame edit"); pageView(frame, false); pg.appendChild(frame);
  }
  function panel() {
    const p = $(".g-panel", root); p.innerHTML = ""; p.hidden = !!S.device; if (S.device) return;
    const tabs = h("div", "g-ptabs"); ["Insert", "Pages", "Themes"].forEach((n) => tabs.appendChild(btn(n, n, () => { S.panel = n; S.newp = false; draw(); }, "g-ptab" + (S.panel === n ? " on" : "")))); p.appendChild(tabs);
    if (S.panel === "Pages") {
      S.pages.forEach((n, i) => p.appendChild(h("div", "g-pg", (i === 0 ? "⌂ " : "▢ ") + n)));
      p.appendChild(btn("+ New page", "New page", () => { S.newp = true; draw(); }, "g-plus"));
      if (S.newp) { const d = h("div", "w-menu g-dialog"); d.appendChild(h("b", "", "New page")); const i = h("input", "g-in"); i.placeholder = "Name";
        const done = () => { const v = i.value.trim(); if (!v) return; S.pages.push(v); S.newp = false; say(`The page <b>${v}</b> is added: the menu at the top has a link to it.`); draw(); };
        i.addEventListener("keydown", (e) => { if (e.key === "Enter") done(); }); d.appendChild(i); d.appendChild(btn("Done", "Done", done, "g-done")); p.appendChild(d); }
    } else if (S.panel === "Themes") {
      Object.keys(THEMES).forEach((n) => { const b = btn(`<span class='g-sw' style='background:${THEMES[n][0]};border-color:${THEMES[n][2]}'></span>${n}`, n, () => { S.theme = n; say(`The theme <b>${n}</b>: the colours and the fonts of every page change at once.`); draw(); }, "g-theme" + (S.theme === n ? " on" : "")); p.appendChild(b); });
    } else p.appendChild(h("small", "", "Text box, Images, Embed… Not needed today."));
  }
  const MISSIONS = {
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
  const HELLO = PART === "pages" ? "A blank site. Click <b>Untitled site</b> at the top left and type the name." : "Click <b>Themes</b> on the right, then a theme.";
  reset(); say(HELLO); draw();
})();
