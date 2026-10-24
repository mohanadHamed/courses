// Format Lab: the title gets 20, bold, centred and orange; the text gets 1.15; then Check.
const btn = (t) => [...document.querySelectorAll(".ribbon button")].find((b) => b.textContent === t);
const para = (i) => document.querySelectorAll("#page p")[i];
await wait(600); para(0).click(); await wait(500);
for (const t of ["20", "B", "centre", "orange"]) { btn(t).click(); await wait(550); }
para(1).click(); await wait(400); btn("1.15").click(); await wait(500);
para(2).click(); await wait(400); btn("1.15").click(); await wait(400); btn("B").click(); await wait(500);
click("#check"); await wait(2200);
