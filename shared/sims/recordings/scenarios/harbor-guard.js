// Harbor Guard: read each order and tap the point (one mistake on purpose).
const c = document.getElementById("c");
const W = c.clientWidth, cell = Math.min((W - 52) / 12, 34), left = (W - cell * 12) / 2, top = 18;
const at = (x, y) => tap(c, left + (x + 6) * cell, top + (8 - y) * cell);
const num = (s) => Number(s.replace("−", "-"));
await wait(500);
click("#start");
for (let round = 0; round < 5; round++) {
  await wait(1100);
  const t = document.getElementById("order").textContent;
  const m = t.match(/\((−?\d+), (−?\d+)\)/);
  const q = t.match(/quadrant (IV|III|II|I)/);
  if (round === 2 && m) at(num(m[2]), num(m[1]));            // swap x and y: a typical mistake
  else if (m) at(num(m[1]), num(m[2]));
  else if (q) { const p = { I: [3, 3], II: [-3, 3], III: [-3, -3], IV: [3, -3] }[q[1]]; at(p[0], p[1]); }
  await wait(round === 2 ? 1200 : 400);
}
