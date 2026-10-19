// Grid Strike: strike the targets of stage 1 (one mistake).
const c = document.getElementById("c");
const W = c.clientWidth, padL = W < 420 ? 26 : 34, padT = 22, cell = Math.min((W - padL * 2) / 12, 52), gx0 = (W - cell * 12) / 2;
const at = (x, y) => tap(c, gx0 + (x + 6) * cell, padT + (4 - y) * cell);
const num = (s) => Number(s.replace("−", "-"));
await wait(500); click("#start");
for (let i = 0; i < 5; i++) {
  await wait(1000);
  const m = document.getElementById("target").textContent.match(/\((−?\d+), (−?\d+)\)/);
  if (!m) continue;
  if (i === 2) at(num(m[2]), num(m[1])); else at(num(m[1]), num(m[2]));
  await wait(i === 2 ? 1300 : 500);
}
