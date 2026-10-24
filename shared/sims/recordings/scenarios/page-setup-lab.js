// Page Setup Lab: narrow margins are not enough; landscape fits the table; then a page break after the cover.
const b = (t) => [...document.querySelectorAll(".ribbon button")].find((x) => x.textContent === t).click();
await wait(1200); b("Narrow"); await wait(1500); b("Landscape"); await wait(1300); b("Normal"); await wait(1300); b("Page break"); await wait(2400);
