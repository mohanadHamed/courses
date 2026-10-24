// Pitch Room, brief 1: a first pitch with wrong cards, then the right cards.
const rows = [...document.querySelectorAll(".opts")];
const okIndex = [0, 2, 1, 0, 2, 1];   // the first try: some wrong cards
await wait(700);
for (const [i, r] of rows.entries()) { r.querySelectorAll("button")[okIndex[i]].click(); await wait(250); }
click("#go"); await wait(1800);
for (const r of rows) { for (const b of r.querySelectorAll("button")) { if (!r.querySelector("button.bad")) break; b.click(); click("#go"); await wait(120); } }
await wait(2600);
